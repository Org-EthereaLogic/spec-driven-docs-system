#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Pre-write validation hook for documentation files.

Runs before Write tool operations on documentation files (.md under tracked
docs directories). Validates that documentation writes follow project standards.

Hook Type: PreToolUse
Matcher: (Write|Edit).*(spec_driven_docs|app_docs|docs)/.*\\.md$
"""

import json
import re
import sys
from pathlib import Path

# Allow `from hook_utils import ...` regardless of cwd at invocation.
sys.path.insert(0, str(Path(__file__).parent))

from hook_utils import (  # noqa: E402
    format_blocking_feedback,
    format_warning_feedback,
    get_project_dir,
    get_tool_input,
    is_documentation_file,
    load_consistency_rules,
)


def check_forbidden_patterns(content: str, rules: dict) -> list:
    """Check content for forbidden patterns.

    Uses word-boundary matching for short placeholder terms (foo, bar, baz)
    to avoid false positives like 'foobar' or 'toolbar'.
    """
    issues = []
    forbidden = rules.get("forbidden_patterns", {}).get("patterns", [])
    word_boundary_patterns = {"foo", "bar", "baz"}

    for pattern in forbidden:
        pattern_lower = pattern.lower()
        content_lower = content.lower()

        if pattern_lower in word_boundary_patterns:
            regex = r'\b' + re.escape(pattern_lower) + r'\b'
            if re.search(regex, content_lower):
                issues.append(f"Forbidden pattern found: '{pattern}'")
        else:
            if pattern_lower in content_lower:
                issues.append(f"Forbidden pattern found: '{pattern}'")

    return issues


def _fenced_code_spans(content: str) -> list:
    """Return list of (start, end) character offsets covering fenced code blocks.

    Recognizes both backtick (```) and tilde (~~~) fences. The end offset is
    inclusive of the closing fence line. An unterminated opener spans to EOF.
    """
    spans = []
    fence_re = re.compile(r'(?m)^[ \t]{0,3}(`{3,}|~{3,})')
    pos = 0
    while True:
        opener = fence_re.search(content, pos)
        if not opener:
            break
        marker = opener.group(1)
        body_start = opener.start()
        line_end = content.find('\n', opener.end())
        search_from = line_end + 1 if line_end != -1 else len(content)
        closer_re = re.compile(
            r'(?m)^[ \t]{0,3}' + re.escape(marker[0]) + r'{' + str(len(marker)) + r',}\s*$'
        )
        closer = closer_re.search(content, search_from)
        if not closer:
            spans.append((body_start, len(content)))
            break
        close_line_end = content.find('\n', closer.end())
        span_end = close_line_end if close_line_end != -1 else len(content)
        spans.append((body_start, span_end))
        pos = span_end + 1
    return spans


def _is_inside_spans(pos: int, spans: list) -> bool:
    """Return True if pos lies within any (start, end) span."""
    for start, end in spans:
        if start <= pos < end:
            return True
    return False


def is_valid_protocol_ellipsis(content: str, ellipsis_pos: int) -> bool:
    """Check if an ellipsis at the given position is valid Protocol/ABC syntax.

    Valid PEP 544 ellipsis must:
    1. Appear as a standalone statement (just '...' on its own line)
    2. Be preceded by 'def' within the recent lookback window
    3. Be inside a class that inherits from Protocol or ABC
    """
    lines = content[:ellipsis_pos].split('\n')
    if not lines:
        return False

    current_line_start = content.rfind('\n', 0, ellipsis_pos) + 1
    current_line_end = content.find('\n', ellipsis_pos)
    if current_line_end == -1:
        current_line_end = len(content)
    current_line = content[current_line_start:current_line_end].strip()

    if current_line != '...':
        return False

    lookback_lines = lines[-10:] if len(lines) >= 10 else lines
    lookback_text = '\n'.join(lookback_lines)

    has_def = bool(re.search(r'\bdef\s+\w+', lookback_text))
    if not has_def:
        return False

    has_protocol_context = bool(re.search(
        r'class\s+\w+\s*\([^)]*\b(Protocol|ABC)\b[^)]*\)',
        lookback_text
    ))

    return has_protocol_context


def check_ellipsis_patterns(content: str) -> list:
    """Check for ellipsis patterns that indicate incomplete content.

    Ellipsis is allowed inside fenced code blocks (comments, spread operators,
    range syntax, Protocol bodies). In prose, ellipsis is also allowed when
    immediately preceded by a sentence-ending word (e.g., "...wait, what?")
    but flagged when it appears to indicate omitted content.
    """
    issues = []
    code_spans = _fenced_code_spans(content)
    for match in re.finditer(r'\.\.\.', content):
        pos = match.start()
        if _is_inside_spans(pos, code_spans):
            continue
        if is_valid_protocol_ellipsis(content, pos):
            continue
        line_num = content[:pos].count('\n') + 1
        issues.append(f"Line {line_num}: Ellipsis '...' detected - may indicate incomplete content")
    return issues


def check_placeholder_content(content: str) -> list:
    """Check for placeholder content that shouldn't be in final docs."""
    issues = []
    placeholders = [
        "TODO", "FIXME", "TBD", "XXX", "HACK", "WIP",
        "[your", "<your", "{your",
        "lorem ipsum", "example.com",
    ]

    for placeholder in placeholders:
        if placeholder.lower() in content.lower():
            issues.append(f"Placeholder content detected: '{placeholder}'")

    issues.extend(check_ellipsis_patterns(content))
    return issues


def check_code_blocks(content: str) -> list:
    """Check that code blocks have language hints."""
    issues = []
    lines = content.split("\n")
    in_code_block = False

    for i, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            if not in_code_block:
                lang_hint = line.strip()[3:].strip()
                if not lang_hint:
                    issues.append(f"Line {i}: Code block missing language hint")
                in_code_block = True
            else:
                in_code_block = False

    return issues


def validate_documentation_write(file_path: str, content: str) -> dict:
    """Validate a documentation write operation.

    Returns dict with 'valid', 'issues', and 'warnings' keys.
    """
    project_dir = get_project_dir()
    rules = load_consistency_rules(project_dir)

    issues = []
    warnings = []

    issues.extend(check_forbidden_patterns(content, rules))
    issues.extend(check_placeholder_content(content))
    warnings.extend(check_code_blocks(content))

    word_count = len(content.split())
    if word_count < 50:
        warnings.append(f"Document has only {word_count} words - seems incomplete")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
    }


def main():
    """Main hook entry point."""
    tool_input = get_tool_input()
    file_path = tool_input.get("file_path", "")
    content = tool_input.get("content", "")

    if not is_documentation_file(file_path):
        print(json.dumps({"continue": True}))
        return

    result = validate_documentation_write(file_path, content)

    if not result["valid"]:
        print(json.dumps({
            "continue": False,
            "feedback": format_blocking_feedback(result["issues"], result["warnings"]),
        }))
    else:
        response = {"continue": True}
        if result["warnings"]:
            response["feedback"] = format_warning_feedback(result["warnings"])
        print(json.dumps(response))


if __name__ == "__main__":
    main()
