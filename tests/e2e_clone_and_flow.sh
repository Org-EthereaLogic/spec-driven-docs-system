#!/bin/bash
# tests/e2e_clone_and_flow.sh
# End-to-end verification that simulates a new user cloning and running the framework.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORKDIR="$(mktemp -d /tmp/spec-docs-e2e-XXXXXX)"
CLONE_DIR="$WORKDIR/repo"

cleanup() {
  rm -rf "$WORKDIR"
}
trap cleanup EXIT

log() {
  printf '[e2e] %s\n' "$1"
}

run_hook() {
  local hook_path="$1"
  local file_path="$2"
  local content="$3"
  local tool_input

  tool_input=$(python3 -c "import json,sys; print(json.dumps({'file_path': sys.argv[1], 'content': sys.argv[2]}))" \
    "$file_path" "$content")

  CLAUDE_TOOL_INPUT="$tool_input" CLAUDE_PROJECT_DIR="$CLONE_DIR" python3 "$hook_path"
}

log "Cloning repository into temporary workspace"
git clone "$ROOT" "$CLONE_DIR" >/dev/null

log "Installing dependencies"
(
  cd "$CLONE_DIR"
  npm install >/dev/null
)

log "Running smoke suite"
(
  cd "$CLONE_DIR"
  npm test >/dev/null
)

mkdir -p "$CLONE_DIR/specs/docs/e2e" \
  "$CLONE_DIR/spec_driven_docs/rough_draft/api" \
  "$CLONE_DIR/spec_driven_docs/rough_draft/design" \
  "$CLONE_DIR/spec_driven_docs/rough_draft/manual"

log "Creating three specifications (api, design, manual)"
cat > "$CLONE_DIR/specs/docs/e2e/users-api-spec.md" <<'DOC'
# Users API specification

## Overview
Define a users endpoint set with authentication, pagination, and error responses.
DOC

cat > "$CLONE_DIR/specs/docs/e2e/session-design-spec.md" <<'DOC'
# Session design specification

## Overview
Describe session lifecycle, renewal constraints, and data retention choices.
DOC

cat > "$CLONE_DIR/specs/docs/e2e/operator-manual-spec.md" <<'DOC'
# Operator manual specification

## Overview
Outline deployment, monitoring checks, and rollback procedures for operators.
DOC

log "Generating three documents in rough_draft"
cat > "$CLONE_DIR/spec_driven_docs/rough_draft/api/users.md" <<'DOC'
# Users API

## Overview
The users endpoint supports account discovery and profile retrieval for authorized clients.

## Authentication
All requests require bearer tokens with scoped permissions.

## Endpoints
- `GET /users` returns paginated users.
- `GET /users/{id}` returns one user.

## Error handling
Use consistent status codes and machine-readable error codes.
DOC

cat > "$CLONE_DIR/spec_driven_docs/rough_draft/design/session-lifecycle.md" <<'DOC'
# Session lifecycle design

## Overview
This design defines short-lived access tokens and bounded refresh token reuse.

## Goals
- Reduce replay risk.
- Maintain operator visibility.

## Decisions
- Rotate refresh tokens.
- Revoke compromised sessions rapidly.
DOC

cat > "$CLONE_DIR/spec_driven_docs/rough_draft/manual/operator-runbook.md" <<'DOC'
# Operator runbook

## Overview
This manual explains how operators deploy, verify, and recover the service safely.

## Deploy
1. Apply migration steps.
2. Roll out the release.

## Rollback
Revert to the previous known-good build and validate health checks.
DOC

log "Running pre-write and post-write hooks on generated documents"
for doc in \
  "$CLONE_DIR/spec_driven_docs/rough_draft/api/users.md" \
  "$CLONE_DIR/spec_driven_docs/rough_draft/design/session-lifecycle.md" \
  "$CLONE_DIR/spec_driven_docs/rough_draft/manual/operator-runbook.md"
do
  content="$(cat "$doc")"
  pre_result=$(run_hook "$CLONE_DIR/.claude/hooks/doc_pre_write.py" "$doc" "$content")
  echo "$pre_result" | python3 -c "import json,sys; d=json.load(sys.stdin); assert d.get('continue') is True"

  post_result=$(run_hook "$CLONE_DIR/.claude/hooks/doc_post_write.py" "$doc" "$content" 2>/dev/null || true)
  if [ -n "$post_result" ]; then
    echo "$post_result" | python3 -c "import json,sys; json.load(sys.stdin)"
  fi
done

log "Simulating review and promotion to pending_approval"
for rel_path in \
  "api/users.md" \
  "design/session-lifecycle.md" \
  "manual/operator-runbook.md"
do
  command_str="/doc-review spec_driven_docs/rough_draft/$rel_path"
  review_text="Score: 92/100 (A)
ready_for_publish: true
passed: true
Document: spec_driven_docs/rough_draft/$rel_path"

  CLAUDE_TOOL_INPUT=$(python3 -c "import json,sys; print(json.dumps({'command': sys.argv[1]}))" "$command_str") \
    CLAUDE_TOOL_RESULT="$review_text" \
    CLAUDE_PROJECT_DIR="$CLONE_DIR" \
    python3 "$CLONE_DIR/.claude/hooks/doc_post_review.py" >/dev/null

  src="$CLONE_DIR/spec_driven_docs/rough_draft/$rel_path"
  dst="$CLONE_DIR/spec_driven_docs/pending_approval/$rel_path"
  mkdir -p "$(dirname "$dst")"
  cp "$src" "$dst"
done

for expected in \
  "$CLONE_DIR/spec_driven_docs/pending_approval/api/users.md" \
  "$CLONE_DIR/spec_driven_docs/pending_approval/design/session-lifecycle.md" \
  "$CLONE_DIR/spec_driven_docs/pending_approval/manual/operator-runbook.md"
do
  [ -f "$expected" ]
done

log "E2E clone and workflow verification passed"
