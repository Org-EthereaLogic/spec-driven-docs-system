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


def check_placeholder_content(content: str) -> list[str]:
    """Check for placeholder content that shouldn't be in final docs."""
    issues = []
    placeholders = [
        "TODO",
        "FIXME",
        "TBD",
        "XXX",
        "[your",
        "<your",
        "{your",
        "lorem ipsum",
        "example.com",
        "...",  # Ellipsis often indicates incomplete content
    ]

    for placeholder in placeholders:
        if placeholder.lower() in content.lower():
            issues.append(f"Placeholder content detected: '{placeholder}'")

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
