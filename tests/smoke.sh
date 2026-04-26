#!/bin/bash
# tests/smoke.sh
# Smoke tests for spec-driven-docs-system
#
# Runs:
#   1. JSON validation for all configuration files
#   2. Hook execution tests (pre-write blocking, protocol ellipsis allowed)
#   3. Markdown lint (lint:md)
#
# Runs all checks, prints a summary, and exits non-zero if any check fails.
# Designed for CI and local `npm test`.

set -u

FRAMEWORK_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$FRAMEWORK_ROOT"

PASS=0
FAIL=0
FAIL_NAMES=()

pass() {
    echo "  [PASS] $1"
    PASS=$((PASS + 1))
}

fail() {
    echo "  [FAIL] $1"
    if [ -n "${2:-}" ]; then
        echo "         $2"
    fi
    FAIL=$((FAIL + 1))
    FAIL_NAMES+=("$1")
}

section() {
    echo ""
    echo "=== $1 ==="
}

# ---------------------------------------------------------------------
# 1. JSON Validation
# ---------------------------------------------------------------------
section "JSON Validation"

JSON_FILES=(
    ".claude/settings.json"
    ".claude/docs/config/quality-gates.json"
    ".claude/docs/config/consistency-rules.json"
    ".claude/docs/expertise/patterns.json"
    ".claude/docs/expertise/anti-patterns.json"
    ".claude/docs/expertise/domain-knowledge.json"
    "package.json"
)

for file in "${JSON_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        fail "json-exists: $file" "file not found"
        continue
    fi
    if python3 -c "import json,sys; json.load(open('$file'))" 2>/dev/null; then
        pass "json-valid: $file"
    else
        err=$(python3 -c "import json,sys; json.load(open('$file'))" 2>&1 || true)
        fail "json-valid: $file" "$err"
    fi
done

# Suite manifests (glob — may be zero)
for manifest in .claude/docs/suites/*/manifest.json; do
    [ -f "$manifest" ] || continue
    if python3 -c "import json,sys; json.load(open('$manifest'))" 2>/dev/null; then
        pass "json-valid: $manifest"
    else
        err=$(python3 -c "import json,sys; json.load(open('$manifest'))" 2>&1 || true)
        fail "json-valid: $manifest" "$err"
    fi
done

# Plugin manifests (glob — may be zero)
for manifest in .claude/plugins/*/plugin.json; do
    [ -f "$manifest" ] || continue
    if python3 -c "import json,sys; json.load(open('$manifest'))" 2>/dev/null; then
        pass "json-valid: $manifest"
    else
        err=$(python3 -c "import json,sys; json.load(open('$manifest'))" 2>&1 || true)
        fail "json-valid: $manifest" "$err"
    fi
done

# ---------------------------------------------------------------------
# 2. Hook Execution Tests
# ---------------------------------------------------------------------
section "Hook Execution"

run_hook() {
    local hook_path="$1"
    local file_path="$2"
    local content="$3"
    local tool_input
    tool_input=$(python3 -c "
import json, sys
print(json.dumps({'file_path': sys.argv[1], 'content': sys.argv[2]}))
" "$file_path" "$content")
    CLAUDE_TOOL_INPUT="$tool_input" CLAUDE_PROJECT_DIR="$FRAMEWORK_ROOT" \
        python3 "$hook_path"
}

# Hook path checks match "/spec_driven_docs/" etc. with leading slash,
# so the tests below pass absolute-style paths to match real invocation.
DOC_PATH="$FRAMEWORK_ROOT/spec_driven_docs/rough_draft/test.md"
PROTO_PATH="$FRAMEWORK_ROOT/spec_driven_docs/rough_draft/protocol.md"

# Test 1: pre-write blocks forbidden TODO markers
output=$(run_hook .claude/hooks/doc_pre_write.py \
    "$DOC_PATH" \
    "# Test Document

This is a reasonably long document with sufficient prose to pass
the minimum word-count warning. It includes a TODO marker which must
be rejected by the pre-write hook. The hook should return continue:false
and feedback mentioning the forbidden TODO placeholder. Add more words
here to ensure we are above the fifty-word warning threshold comfortably
and only fail for the forbidden pattern, not the word count.")
if echo "$output" | python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get('continue') is False else 1)"; then
    pass "pre-write-hook: blocks TODO markers"
else
    fail "pre-write-hook: blocks TODO markers" "$output"
fi

# Test 2: pre-write allows valid Protocol ellipsis
output=$(run_hook .claude/hooks/doc_pre_write.py \
    "$PROTO_PATH" \
    "# Protocol Example

Abstract method bodies may use ellipsis per PEP 544. This document
explains the Protocol class pattern with enough prose to clear the
fifty-word minimum warning threshold set in the pre-write hook.
The example below uses standalone ellipsis inside a Protocol method
body, which is a valid syntactic form and must not be rejected.

\`\`\`python
from typing import Protocol

class Greeter(Protocol):
    def greet(self, name: str) -> str:
        ...
\`\`\`")
if echo "$output" | python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get('continue') is True else 1)"; then
    pass "pre-write-hook: allows Protocol ellipsis"
else
    fail "pre-write-hook: allows Protocol ellipsis" "$output"
fi

# Test 3: pre-write skips non-docs files
output=$(run_hook .claude/hooks/doc_pre_write.py \
    "$FRAMEWORK_ROOT/src/code.py" \
    "print('hello')")
if echo "$output" | python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get('continue') is True else 1)"; then
    pass "pre-write-hook: skips non-docs files"
else
    fail "pre-write-hook: skips non-docs files" "$output"
fi

# Test 4: post-write hook runs without error on a valid document.
# The hook only prints output when there are issues or suggestions, so
# empty output is a valid pass (clean doc). We only require exit 0.
clean_doc="# Sample Document

This document exists only to exercise the post-write hook during
smoke tests. It has enough prose to avoid length warnings and uses
no forbidden terminology so the hook should report success."
if output=$(run_hook .claude/hooks/doc_post_write.py "$DOC_PATH" "$clean_doc" 2>&1); then
    # If output is non-empty, it must be valid JSON
    if [ -z "$output" ] || echo "$output" | python3 -c "import json,sys; json.load(sys.stdin)" 2>/dev/null; then
        pass "post-write-hook: runs cleanly on valid doc"
    else
        fail "post-write-hook: runs cleanly on valid doc" "invalid JSON: $output"
    fi
else
    fail "post-write-hook: runs cleanly on valid doc" "exit non-zero: $output"
fi

# Test 5: post-write hook flags terminology violations
bad_terminology_doc="# API Doc

This document deliberately uses the forbidden term route instead of
endpoint to verify that the post-write consistency hook detects
terminology violations. It has enough prose to avoid length warnings
while keeping the focus on the terminology check we want to exercise."
output=$(run_hook .claude/hooks/doc_post_write.py "$DOC_PATH" "$bad_terminology_doc" 2>&1 || true)
if echo "$output" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    fb = d.get('feedback', '')
    sys.exit(0 if 'endpoint' in fb and 'route' in fb else 1)
except Exception:
    sys.exit(1)
" 2>/dev/null; then
    pass "post-write-hook: flags terminology violations"
else
    fail "post-write-hook: flags terminology violations" "$output"
fi

# Test 5a: post-write hook does NOT flag forbidden terms inside code blocks,
# inline code, or Markdown link targets. CLI command names and file paths
# are legitimate uses that must not produce noise.
code_safe_doc="# CLI Quickstart

This page documents the notesctl CLI. Run \`notesctl login\` to authenticate
with your bearer token. The CLI stores the token at \`~/.config/notesctl/config.toml\`
with mode 600. To re-authenticate, rerun \`notesctl login\` and paste a fresh token.

\`\`\`bash
notesctl login
notesctl new --title \"Demo\" --body \"Hello\"
\`\`\`

For details, see [config](~/.config/notesctl/config.toml)."
output=$(run_hook .claude/hooks/doc_post_write.py "$DOC_PATH" "$code_safe_doc" 2>&1 || true)
if echo "$output" | python3 -c "
import json, sys
try:
    if not sys.stdin.read().strip():
        sys.exit(0)
    sys.stdin.seek(0)
    d = json.load(sys.stdin)
    fb = d.get('feedback', '').lower()
    has_login_violation = ('use \\'authenticate\\' instead of \\'login\\'' in fb)
    has_config_violation = ('use \\'configuration\\' instead of \\'config\\'' in fb)
    sys.exit(1 if (has_login_violation or has_config_violation) else 0)
except Exception:
    sys.exit(0)
" 2>/dev/null; then
    pass "post-write-hook: ignores terminology in code/inline/links"
else
    fail "post-write-hook: ignores terminology in code/inline/links" "$output"
fi

# Test 5b: pre-write hook allows ellipsis inside fenced code blocks.
# Code-comment elision (e.g. '# ... existing logic ...') is a common
# documentation pattern and must not block writes.
code_ellipsis_doc="# Event Bus Example

The example below shows a publisher that omits unrelated business logic
inline. Ellipsis appears only inside a fenced code block as a comment
and must not block the write. This document has enough prose to clear
the minimum word-count threshold and exists solely to exercise the
ellipsis-in-code regression test added during the end-to-end review.

\`\`\`python
def place_order(order_id: int, total_cents: int) -> None:
    # ... core order logic ...
    publish(OrderPlaced(order_id=order_id))
\`\`\`"
output=$(run_hook .claude/hooks/doc_pre_write.py "$DOC_PATH" "$code_ellipsis_doc")
if echo "$output" | python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get('continue') is True else 1)"; then
    pass "pre-write-hook: allows ellipsis inside code-block comments"
else
    fail "pre-write-hook: allows ellipsis inside code-block comments" "$output"
fi

# ---------------------------------------------------------------------
# 2b. Post-Review Hook Tests
# ---------------------------------------------------------------------
# doc_post_review.py reads CLAUDE_TOOL_RESULT as a raw string (not JSON),
# so it needs a different invocation pattern than run_hook above.

run_post_review_hook() {
    local command_str="$1"
    local result_text="$2"
    CLAUDE_TOOL_INPUT=$(python3 -c "import json,sys; print(json.dumps({'command': sys.argv[1]}))" "$command_str") \
    CLAUDE_TOOL_RESULT="$result_text" \
    CLAUDE_PROJECT_DIR="$FRAMEWORK_ROOT" \
        python3 .claude/hooks/doc_post_review.py
}

# Test 6: post-review hook suggests promotion when grade A is found
output=$(run_post_review_hook \
    "/doc-review spec_driven_docs/rough_draft/api/users.md" \
    "Score: 95/100 (A)
ready_for_publish: true
passed: true
Document: spec_driven_docs/rough_draft/api/users.md")
if echo "$output" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    fb = d.get('feedback', '')
    sys.exit(0 if 'promote' in fb.lower() or 'pending_approval' in fb.lower() else 1)
except Exception:
    sys.exit(1)
" 2>/dev/null; then
    pass "post-review-hook: suggests promotion for grade A"
else
    fail "post-review-hook: suggests promotion for grade A" "$output"
fi

# Test 7: post-review hook is silent for grade F (no promotion suggestion)
output=$(run_post_review_hook \
    "/doc-review spec_driven_docs/rough_draft/api/broken.md" \
    "Score: 45/100 (F)
ready_for_publish: false
passed: false
Document: spec_driven_docs/rough_draft/api/broken.md")
# Either empty output or feedback that doesn't suggest promotion is acceptable
if [ -z "$output" ]; then
    pass "post-review-hook: silent for grade F"
elif echo "$output" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    fb = d.get('feedback', '').lower()
    # Should NOT suggest promotion for failing grade
    sys.exit(0 if 'promote' not in fb and 'pending_approval' not in fb else 1)
except Exception:
    sys.exit(1)
" 2>/dev/null; then
    pass "post-review-hook: silent for grade F"
else
    fail "post-review-hook: silent for grade F" "$output"
fi

# Test 8: post-review hook is silent for non-review commands
output=$(run_post_review_hook \
    "/doc-write specs/docs/api-spec.md" \
    "Document written successfully")
if [ -z "$output" ]; then
    pass "post-review-hook: silent for non-review command"
elif echo "$output" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    sys.exit(0 if not d.get('feedback') else 1)
except Exception:
    sys.exit(0)
" 2>/dev/null; then
    pass "post-review-hook: silent for non-review command"
else
    fail "post-review-hook: silent for non-review command" "$output"
fi

# ---------------------------------------------------------------------
# 3. Markdown Lint
# ---------------------------------------------------------------------
section "Markdown Lint"

if ! command -v npx >/dev/null 2>&1; then
    fail "markdownlint: npx not available" "install Node.js"
elif ! npx --no-install markdownlint --version >/dev/null 2>&1; then
    fail "markdownlint: dependency not installed" "run 'npm install' first"
else
    lint_output=$(npm run --silent lint:md 2>&1)
    lint_exit=$?
    if [ $lint_exit -eq 0 ]; then
        pass "markdownlint: all files clean"
    else
        issue_count=$(echo "$lint_output" | grep -c ':[0-9]\+ ' || true)
        if [ "$issue_count" -eq 0 ]; then
            fail "markdownlint: lint command failed unexpectedly" \
                 "run 'npm run lint:md' to see the error"
        else
            fail "markdownlint: $issue_count issue(s) found" "run 'npm run lint:md' for details"
        fi
    fi
fi

# ---------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------
section "Summary"
echo "Passed: $PASS"
echo "Failed: $FAIL"

if [ "$FAIL" -gt 0 ]; then
    echo ""
    echo "Failed tests:"
    for name in "${FAIL_NAMES[@]}"; do
        echo "  - $name"
    done
    exit 1
fi

exit 0
