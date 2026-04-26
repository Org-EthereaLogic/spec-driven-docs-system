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


def _strip_code_regions(content: str) -> str:
    """Return content with code regions blanked out for prose-only checks.

    Strips fenced code blocks (``` and ~~~), inline code spans (any number of
    backticks), and Markdown link targets `](target)`. Replaces stripped
    regions with whitespace of equal length so line numbers and surrounding
    offsets are preserved.

    The link-target strip prevents file paths embedded in links (e.g.
    `[config](~/.config/notesctl)`) from being terminology-checked.
    """

    def _blank(match):
        return re.sub(r'[^\n]', ' ', match.group(0))

    fenced_re = re.compile(
        r'(?ms)^[ \t]{0,3}(`{3,}|~{3,}).*?(?:^[ \t]{0,3}\1\s*$|\Z)'
    )
    inline_re = re.compile(r'(`+)(?:(?!\1).)+?\1', re.DOTALL)
    link_target_re = re.compile(r'\]\(([^)]+)\)')

    cleaned = fenced_re.sub(_blank, content)
    cleaned = inline_re.sub(_blank, cleaned)
    cleaned = link_target_re.sub(_blank, cleaned)
    return cleaned


def check_terminology(content: str, rules: dict) -> list:
    """Check prose for terminology violations.

    Inspects only prose - code blocks, inline code, and Markdown link targets
    are blanked out first so CLI command names (`notesctl login`) and file
    paths (`~/.config/notesctl/config.toml`) are not flagged as forbidden
    variants of enforced terms. Each issue includes a line number and a
    snippet so the user can judge verb-vs-noun ambiguity (e.g. "Route all
    events" is a verb usage, not a violation).
    """
    issues = []
    terminology = rules.get("terminology", {}).get("enforced_terms", {})
    prose = _strip_code_regions(content)
    lines = prose.split('\n')

    for correct_term, forbidden_variants in terminology.items():
        for variant in forbidden_variants:
            pattern = re.compile(r'\b' + re.escape(variant) + r'\b', re.IGNORECASE)
            seen_lines = set()
            for i, line in enumerate(lines, 1):
                if pattern.search(line):
                    if i in seen_lines:
                        continue
                    seen_lines.add(i)
                    snippet = line.strip()
                    if len(snippet) > 80:
                        snippet = snippet[:77] + "..."
                    issues.append(
                        f"Terminology (line {i}): Use '{correct_term}' instead of '{variant}' - \"{snippet}\""
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
