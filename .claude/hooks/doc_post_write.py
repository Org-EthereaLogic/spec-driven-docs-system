#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Post-write consistency check hook for documentation files.

Runs after Write tool operations on documentation files. Performs consistency
checks and surfaces issues for review (cannot block).

Hook Type: PostToolUse
Matcher: (Write|Edit).*(spec_driven_docs|app_docs|docs)/.*\\.md$
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from hook_utils import (  # noqa: E402
    get_project_dir,
    get_tool_input,
    get_tool_result,
    is_documentation_file,
    load_consistency_rules,
)


def check_terminology(content: str, rules: dict) -> list:
    """Check content for terminology violations."""
    issues = []
    terminology = rules.get("terminology", {}).get("enforced_terms", {})

    for correct_term, forbidden_variants in terminology.items():
        for variant in forbidden_variants:
            pattern = r'\b' + re.escape(variant) + r'\b'
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(
                    f"Terminology: Use '{correct_term}' instead of '{variant}'"
                )

    return issues


def check_internal_links(content: str, file_path: str) -> list:
    """Check that internal markdown links are valid."""
    issues = []
    project_dir = get_project_dir()

    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(link_pattern, content)

    for link_text, link_target in matches:
        if link_target.startswith(('http://', 'https://', 'mailto:')):
            continue
        if link_target.startswith('#'):
            continue

        current_dir = Path(file_path).parent
        target_path = current_dir / link_target.split('#')[0]

        if not target_path.exists() and not (project_dir / link_target.split('#')[0]).exists():
            issues.append(f"Broken link: [{link_text}]({link_target})")

    return issues


def check_header_hierarchy(content: str) -> list:
    """Check that header levels don't skip (e.g., h1 to h3)."""
    issues = []
    lines = content.split('\n')

    current_level = 0
    for i, line in enumerate(lines, 1):
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            if level > 6:
                continue
            if current_level > 0 and level > current_level + 1:
                issues.append(
                    f"Line {i}: Header hierarchy skipped from h{current_level} to h{level}"
                )
            current_level = level

    return issues


def check_document_consistency(file_path: str, content: str) -> dict:
    """Perform post-write consistency checks on documentation."""
    project_dir = get_project_dir()
    rules = load_consistency_rules(project_dir)

    issues = []
    suggestions = []

    issues.extend(check_terminology(content, rules))
    issues.extend(check_internal_links(content, file_path))
    suggestions.extend(check_header_hierarchy(content))

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


def format_feedback(issues: list, suggestions: list) -> str:
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

    if not is_documentation_file(file_path):
        return

    result_str = str(tool_result)
    if "error" in result_str.lower() or "failed" in result_str.lower():
        return

    result = check_document_consistency(file_path, content)

    if result["issues"] or result["suggestions"]:
        feedback = format_feedback(result["issues"], result["suggestions"])
        print(json.dumps({"feedback": feedback}))


if __name__ == "__main__":
    main()
