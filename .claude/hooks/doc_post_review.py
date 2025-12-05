#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Post-review workflow suggestion hook for documentation files.

This hook runs after /doc-review slash command operations.
It suggests workflow promotion when documents pass quality gates.

Hook Type: PostToolUse
Matcher: SlashCommand.*/doc-review.*
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


def get_tool_result() -> str:
    """Read tool result from environment as string."""
    return os.environ.get("CLAUDE_TOOL_RESULT", "")


def extract_review_results(result_text: str) -> dict:
    """
    Extract review results from /doc-review output.

    Looks for patterns like:
    - "Score: 85/100 (B)"
    - "Grade: A"
    - "ready_for_publish": true
    - "passed": true
    """
    results = {
        "score": None,
        "grade": None,
        "passed": False,
        "ready_for_publish": False,
        "document_path": None,
    }

    # Try to find score pattern: "Score: XX/100 (X)" or "score": XX
    score_match = re.search(r'[Ss]core["\s:]+(\d+)/100\s*\(([A-F])\)', result_text)
    if score_match:
        results["score"] = int(score_match.group(1))
        results["grade"] = score_match.group(2)
    else:
        # Try JSON-style pattern
        json_score = re.search(r'"score"\s*:\s*(\d+)', result_text)
        if json_score:
            results["score"] = int(json_score.group(1))

    # Try to find grade pattern if not found above
    if not results["grade"]:
        grade_match = re.search(r'[Gg]rade["\s:]+([A-F])', result_text)
        if grade_match:
            results["grade"] = grade_match.group(1)

    # Check for passed status
    if re.search(r'"passed"\s*:\s*true', result_text, re.IGNORECASE):
        results["passed"] = True
    elif results["score"] and results["score"] >= 80:
        results["passed"] = True

    # Check for ready_for_publish
    if re.search(r'"ready_for_publish"\s*:\s*true', result_text, re.IGNORECASE):
        results["ready_for_publish"] = True
    elif results["grade"] in ["A", "B"]:
        results["ready_for_publish"] = True

    # Try to extract document path
    doc_match = re.search(r'[Dd]ocument["\s:]+["\']?([^\s"\']+\.md)', result_text)
    if doc_match:
        results["document_path"] = doc_match.group(1)

    return results


def detect_workflow_stage(document_path: str) -> str:
    """Detect workflow stage from document path."""
    if not document_path:
        return "unknown"

    if "/rough_draft/" in document_path:
        return "rough_draft"
    elif "/pending_approval/" in document_path:
        return "pending_approval"
    elif "/approved_final/" in document_path:
        return "approved_final"
    else:
        return "unknown"


def get_next_stage(current_stage: str) -> str:
    """Get the next workflow stage."""
    stages = {
        "rough_draft": "pending_approval",
        "pending_approval": "approved_final",
        "approved_final": None,  # Already at final
    }
    return stages.get(current_stage)


def suggest_next_action(document_path: str, results: dict) -> str:
    """Generate promotion suggestion based on review results."""
    if not results.get("ready_for_publish"):
        return ""

    current_stage = detect_workflow_stage(document_path)
    next_stage = get_next_stage(current_stage)

    if not next_stage:
        return ""  # Already at final stage

    grade = results.get("grade", "?")
    score = results.get("score", "?")

    suggestion_parts = [
        f"Document passed review with Grade {grade} ({score}/100).",
        "",
        f"Ready for promotion from {current_stage} to {next_stage}.",
        "",
        "Suggested next step:",
        f"  /doc-promote {document_path}",
    ]

    if current_stage == "pending_approval":
        suggestion_parts.append("")
        suggestion_parts.append("Note: Promoting to approved_final requires --force flag")
        suggestion_parts.append("(confirms stakeholder approval has been received)")

    return "\n".join(suggestion_parts)


def main():
    """Main hook entry point."""
    tool_input = get_tool_input()
    result_text = get_tool_result()

    # Extract the command being run
    command = tool_input.get("command", "")

    # Only process /doc-review commands
    if "/doc-review" not in command and "/doc:doc-review" not in command:
        return

    # Extract review results from output
    results = extract_review_results(result_text)

    # If we can't determine the document path from results, try to extract from command
    if not results["document_path"]:
        # Try to extract path from command args
        path_match = re.search(r'/doc-review\s+([^\s]+)', command)
        if path_match:
            results["document_path"] = path_match.group(1)

    # Generate suggestion if document passed review
    if results.get("ready_for_publish") and results.get("document_path"):
        suggestion = suggest_next_action(results["document_path"], results)
        if suggestion:
            print(json.dumps({
                "feedback": suggestion
            }))


if __name__ == "__main__":
    main()
