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

    Excludes valid Protocol/ABC abstract method ellipsis (PEP 544).
    """
    issues = []
    for match in re.finditer(r'\.\.\.', content):
        pos = match.start()
        if not is_valid_protocol_ellipsis(content, pos):
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
