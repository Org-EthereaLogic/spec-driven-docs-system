#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Shared utilities for documentation hooks.

Centralizes the helpers previously duplicated across doc_pre_write.py and
doc_post_write.py: environment parsing, project-root resolution, configuration
loading, file-path filtering, and structured feedback formatting.
"""

import json
import os
from pathlib import Path


VALID_DOC_PATHS = ["/spec_driven_docs/", "/app_docs/", "/docs/"]


def get_tool_input() -> dict:
    """Read tool input from environment as a dict (empty dict on failure)."""
    tool_input_str = os.environ.get("CLAUDE_TOOL_INPUT", "{}")
    try:
        return json.loads(tool_input_str)
    except json.JSONDecodeError:
        return {}


def get_tool_result() -> dict:
    """Read tool result from environment as a dict (empty dict on failure)."""
    result_str = os.environ.get("CLAUDE_TOOL_RESULT", "{}")
    try:
        return json.loads(result_str)
    except json.JSONDecodeError:
        return {}


def get_project_dir() -> Path:
    """Resolve the Claude project directory."""
    return Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))


def load_consistency_rules(project_dir: Path) -> dict:
    """Load .claude/docs/config/consistency-rules.json (empty dict on failure)."""
    rules_path = project_dir / ".claude" / "docs" / "config" / "consistency-rules.json"
    if rules_path.exists():
        try:
            with open(rules_path) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def load_quality_profiles(project_dir: Path) -> dict:
    """Load quality_profiles section from quality-gates.json (empty dict on failure)."""
    gates_path = project_dir / ".claude" / "docs" / "config" / "quality-gates.json"
    if gates_path.exists():
        try:
            with open(gates_path) as f:
                data = json.load(f)
                return data.get("quality_profiles", {})
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def is_documentation_file(file_path: str) -> bool:
    """Return True if file_path is a markdown file under a tracked docs directory."""
    if not file_path or not file_path.endswith(".md"):
        return False
    return any(p in file_path for p in VALID_DOC_PATHS)


# Mapping of issue prefixes to actionable fix hints. Hints are matched by
# checking whether the issue string starts with the listed prefix.
_FIX_HINTS = [
    ("Forbidden pattern", "Remove or replace this placeholder before saving."),
    ("Placeholder content", "Replace with finalized content; placeholders block writes."),
    ("Ellipsis", "Replace with real content, or verify this is a Protocol/ABC method body."),
    ("Code block missing language hint", "Add a language hint, e.g. ```python or ```bash."),
    ("Terminology", "Use the project's preferred term per consistency-rules.json."),
    ("Broken link", "Fix the path or remove the link."),
    ("Header hierarchy", "Avoid skipping levels; promote the heading or add an intermediate one."),
]


def _fix_hint_for(issue: str) -> str:
    """Return an actionable fix hint for a known issue type, or empty string."""
    for prefix, hint in _FIX_HINTS:
        if prefix.lower() in issue.lower():
            return hint
    return ""


def format_blocking_feedback(issues: list, warnings: list) -> str:
    """Format issues and warnings into a numbered, actionable feedback block.

    Issues get a numbered '[N]' prefix and a 'Fix:' line when a hint is known.
    Warnings are listed flat under a separate header.
    """
    issue_count = len(issues)
    parts = [f"Documentation write blocked - {issue_count} issue(s):", ""]

    for idx, issue in enumerate(issues, 1):
        parts.append(f"  [{idx}] {issue}")
        hint = _fix_hint_for(issue)
        if hint:
            parts.append(f"      Fix: {hint}")
        parts.append("")

    if warnings:
        parts.append(f"{len(warnings)} warning(s) (non-blocking):")
        for warning in warnings:
            parts.append(f"  - {warning}")

    return "\n".join(parts).rstrip() + "\n"


def format_warning_feedback(warnings: list) -> str:
    """Format non-blocking warnings into a feedback block."""
    parts = [f"Documentation warnings ({len(warnings)} non-blocking):"]
    for warning in warnings:
        parts.append(f"  - {warning}")
    return "\n".join(parts) + "\n"
