#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Pre-write validation hook for documentation files.

This hook runs before Write tool operations on documentation files (.md in docs/).
It validates that documentation writes follow project standards.

Hook Type: PreToolUse
Matcher: Write.*docs/.*\\.md$
"""

import json
import os
import re
import sys
from pathlib import Path


def get_tool_input() -> dict:
    """Read tool input from environment."""
    tool_input_str = os.environ.get("CLAUDE_TOOL_INPUT", "{}")
    try:
        return json.loads(tool_input_str)
    except json.JSONDecodeError:
        return {}


def get_project_dir() -> Path:
    """Get the Claude project directory."""
    return Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))


def load_consistency_rules(project_dir: Path) -> dict:
    """Load consistency rules configuration."""
    rules_path = project_dir / ".claude" / "docs" / "config" / "consistency-rules.json"
    if rules_path.exists():
        try:
            with open(rules_path) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def check_forbidden_patterns(content: str, rules: dict) -> list[str]:
    """Check content for forbidden patterns.

    Uses word-boundary matching for short placeholder terms (foo, bar, baz)
    to avoid false positives like 'foobar' or 'toolbar'.
    """
    issues = []
    forbidden = rules.get("forbidden_patterns", {}).get("patterns", [])

    # Patterns that need word-boundary matching to avoid false positives
    word_boundary_patterns = {"foo", "bar", "baz"}

    for pattern in forbidden:
        pattern_lower = pattern.lower()
        content_lower = content.lower()

        if pattern_lower in word_boundary_patterns:
            # Use word boundaries for short placeholder terms
            regex = r'\b' + re.escape(pattern_lower) + r'\b'
            if re.search(regex, content_lower):
                issues.append(f"Forbidden pattern found: '{pattern}'")
        else:
            # Use substring matching for other patterns
            if pattern_lower in content_lower:
                issues.append(f"Forbidden pattern found: '{pattern}'")

    return issues


def is_valid_protocol_ellipsis(content: str, ellipsis_pos: int) -> bool:
    """
    Check if an ellipsis at the given position is valid Protocol/ABC syntax.

    Valid PEP 544 ellipsis must:
    1. Appear as a standalone statement (just '...' on its own line or after whitespace)
    2. Be preceded by 'def' within 5 lines
    3. Be inside a class that inherits from Protocol or ABC

    This is a heuristic check for documentation containing code examples.
    """
    lines = content[:ellipsis_pos].split('\n')
    if not lines:
        return False

    # Get the line containing the ellipsis
    current_line_start = content.rfind('\n', 0, ellipsis_pos) + 1
    current_line_end = content.find('\n', ellipsis_pos)
    if current_line_end == -1:
        current_line_end = len(content)
    current_line = content[current_line_start:current_line_end].strip()

    # Check if ellipsis is standalone (just '...' possibly with whitespace)
    if current_line != '...':
        return False

    # Look back up to 10 lines for 'def' and class context
    lookback_lines = lines[-10:] if len(lines) >= 10 else lines
    lookback_text = '\n'.join(lookback_lines)

    # Check for 'def' within recent lines (indicates method body)
    has_def = bool(re.search(r'\bdef\s+\w+', lookback_text))
    if not has_def:
        return False

    # Check for Protocol or ABC class context
    # Look for class definition with Protocol or ABC inheritance
    has_protocol_context = bool(re.search(
        r'class\s+\w+\s*\([^)]*\b(Protocol|ABC)\b[^)]*\)',
        lookback_text
    ))

    return has_protocol_context


def check_ellipsis_patterns(content: str) -> list[str]:
    """
    Check for ellipsis patterns that indicate incomplete content.

    Excludes valid Protocol/ABC abstract method ellipsis (PEP 544).
    """
    issues = []

    # Find all ellipsis occurrences
    for match in re.finditer(r'\.\.\.', content):
        pos = match.start()

        # Check if this is valid Protocol/ABC syntax
        if not is_valid_protocol_ellipsis(content, pos):
            # Get line number for better error message
            line_num = content[:pos].count('\n') + 1
            issues.append(f"Line {line_num}: Ellipsis '...' detected - may indicate incomplete content")

    return issues


def check_placeholder_content(content: str) -> list[str]:
    """Check for placeholder content that shouldn't be in final docs."""
    issues = []
    placeholders = [
        "TODO",
        "FIXME",
        "TBD",
        "XXX",
        "HACK",
        "WIP",
        "[your",
        "<your",
        "{your",
        "lorem ipsum",
        "example.com",
    ]

    for placeholder in placeholders:
        if placeholder.lower() in content.lower():
            issues.append(f"Placeholder content detected: '{placeholder}'")

    # Check ellipsis patterns separately with Protocol/ABC exception
    ellipsis_issues = check_ellipsis_patterns(content)
    issues.extend(ellipsis_issues)

    return issues


def check_code_blocks(content: str) -> list[str]:
    """Check that code blocks have language hints."""
    issues = []
    lines = content.split("\n")
    in_code_block = False

    for i, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            if not in_code_block:
                # Opening code block - check for language hint
                lang_hint = line.strip()[3:].strip()
                if not lang_hint:
                    issues.append(f"Line {i}: Code block missing language hint")
                in_code_block = True
            else:
                in_code_block = False

    return issues


def validate_documentation_write(file_path: str, content: str) -> dict:
    """
    Validate a documentation write operation.

    Returns:
        dict with 'valid', 'issues', and 'warnings' keys
    """
    project_dir = get_project_dir()
    rules = load_consistency_rules(project_dir)

    issues = []  # Blocking issues
    warnings = []  # Non-blocking warnings

    # Check for forbidden patterns
    forbidden_issues = check_forbidden_patterns(content, rules)
    issues.extend(forbidden_issues)

    # Check for placeholder content
    placeholder_issues = check_placeholder_content(content)
    issues.extend(placeholder_issues)

    # Check code blocks (warning only, not blocking)
    code_issues = check_code_blocks(content)
    warnings.extend(code_issues)

    # Check minimum content length for documentation
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

    # Only validate documentation files (support multiple doc directories)
    valid_doc_paths = ["/spec_driven_docs/", "/app_docs/", "/docs/"]
    if not file_path or not any(p in file_path for p in valid_doc_paths) or not file_path.endswith(".md"):
        # Not a docs file, allow write
        print(json.dumps({"continue": True}))
        return

    # Validate the write
    result = validate_documentation_write(file_path, content)

    if not result["valid"]:
        # Block the write with feedback
        feedback = "Documentation validation failed:\n"
        for issue in result["issues"]:
            feedback += f"  - {issue}\n"
        if result["warnings"]:
            feedback += "\nWarnings:\n"
            for warning in result["warnings"]:
                feedback += f"  - {warning}\n"

        print(json.dumps({
            "continue": False,
            "feedback": feedback
        }))
    else:
        # Allow the write, but include warnings as feedback
        response = {"continue": True}
        if result["warnings"]:
            feedback = "Documentation warnings (non-blocking):\n"
            for warning in result["warnings"]:
                feedback += f"  - {warning}\n"
            response["feedback"] = feedback

        print(json.dumps(response))


if __name__ == "__main__":
    main()
