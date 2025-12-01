#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Post-write consistency check hook for documentation files.

This hook runs after Write tool operations on documentation files.
It performs consistency checks and flags potential issues for review.

Hook Type: PostToolUse
Matcher: Write.*docs/.*\\.md$
"""

import json
import os
import re
from pathlib import Path


def get_tool_input() -> dict:
    """Read tool input from environment."""
    tool_input_str = os.environ.get("CLAUDE_TOOL_INPUT", "{}")
    try:
        return json.loads(tool_input_str)
    except json.JSONDecodeError:
        return {}


def get_tool_result() -> dict:
    """Read tool result from environment."""
    result_str = os.environ.get("CLAUDE_TOOL_RESULT", "{}")
    try:
        return json.loads(result_str)
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


def check_terminology(content: str, rules: dict) -> list[str]:
    """Check content for terminology violations."""
    issues = []
    terminology = rules.get("terminology", {}).get("enforced_terms", {})

    for correct_term, forbidden_variants in terminology.items():
        for variant in forbidden_variants:
            # Case-insensitive search with word boundaries
            pattern = r'\b' + re.escape(variant) + r'\b'
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(
                    f"Terminology: Use '{correct_term}' instead of '{variant}'"
                )

    return issues


def check_internal_links(content: str, file_path: str) -> list[str]:
    """Check that internal markdown links are valid."""
    issues = []
    project_dir = get_project_dir()

    # Find all markdown links
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(link_pattern, content)

    for link_text, link_target in matches:
        # Skip external links
        if link_target.startswith(('http://', 'https://', 'mailto:')):
            continue

        # Skip anchor-only links
        if link_target.startswith('#'):
            continue

        # Resolve relative path
        current_dir = Path(file_path).parent
        target_path = current_dir / link_target.split('#')[0]

        # Check if target file exists
        if not target_path.exists() and not (project_dir / link_target.split('#')[0]).exists():
            issues.append(f"Broken link: [{link_text}]({link_target})")

    return issues


def check_header_hierarchy(content: str) -> list[str]:
    """Check that header levels don't skip (e.g., h1 to h3)."""
    issues = []
    lines = content.split('\n')

    current_level = 0
    for i, line in enumerate(lines, 1):
        if line.startswith('#'):
            # Count the header level
            level = len(line) - len(line.lstrip('#'))
            if level > 6:
                continue  # Not a valid header

            # Check for skipped levels
            if current_level > 0 and level > current_level + 1:
                issues.append(
                    f"Line {i}: Header hierarchy skipped from h{current_level} to h{level}"
                )

            current_level = level

    return issues


def check_document_consistency(file_path: str, content: str) -> dict:
    """
    Perform post-write consistency checks on documentation.

    Returns:
        dict with 'issues' and 'suggestions' keys
    """
    project_dir = get_project_dir()
    rules = load_consistency_rules(project_dir)

    issues = []
    suggestions = []

    # Check terminology
    term_issues = check_terminology(content, rules)
    issues.extend(term_issues)

    # Check internal links
    link_issues = check_internal_links(content, file_path)
    issues.extend(link_issues)

    # Check header hierarchy
    header_issues = check_header_hierarchy(content)
    suggestions.extend(header_issues)  # Header issues are suggestions, not blocking

    # Check for very long paragraphs (potential readability issue)
    paragraphs = content.split('\n\n')
    for i, para in enumerate(paragraphs, 1):
        word_count = len(para.split())
        if word_count > 200 and not para.strip().startswith('```'):
            suggestions.append(
                f"Paragraph {i} has {word_count} words - consider breaking up for readability"
            )

    return {
        "issues": issues,
        "suggestions": suggestions,
    }


def format_feedback(issues: list[str], suggestions: list[str]) -> str:
    """Format issues and suggestions into feedback string."""
    parts = []

    if issues:
        parts.append("Consistency issues found:")
        for issue in issues:
            parts.append(f"  - {issue}")

    if suggestions:
        if parts:
            parts.append("")
        parts.append("Suggestions for improvement:")
        for suggestion in suggestions:
            parts.append(f"  - {suggestion}")

    return "\n".join(parts)


def main():
    """Main hook entry point."""
    tool_input = get_tool_input()
    tool_result = get_tool_result()

    file_path = tool_input.get("file_path", "")
    content = tool_input.get("content", "")

    # Only check documentation files
    if not file_path or "/docs/" not in file_path or not file_path.endswith(".md"):
        # Not a docs file, no feedback needed
        return

    # Check if write was successful
    result_str = str(tool_result)
    if "error" in result_str.lower() or "failed" in result_str.lower():
        # Write failed, don't add more feedback
        return

    # Perform consistency check
    result = check_document_consistency(file_path, content)

    # Only provide feedback if there are issues or suggestions
    if result["issues"] or result["suggestions"]:
        feedback = format_feedback(result["issues"], result["suggestions"])

        # PostToolUse hooks can provide feedback but don't block
        print(json.dumps({
            "feedback": feedback
        }))


if __name__ == "__main__":
    main()
