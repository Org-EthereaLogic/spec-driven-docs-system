# E2E Test Logging Specification

**Version:** 1.0
**Created:** 2025-12-03
**Purpose:** Define systematic logging requirements for spec-driven documentation system E2E tests

---

## 1. Overview

### 1.1 Goals

This specification ensures E2E tests capture sufficient data to:

1. **Debug failures** - Trace exact point of failure with full context
2. **Learn patterns** - Extract successful patterns for expertise files
3. **Track corrections** - Document fixes applied during testing for backport
4. **Measure improvement** - Compare iterations to quantify system learning
5. **Reproduce issues** - Provide enough detail to recreate any problem

### 1.2 Logging Principles

| Principle | Description |
|-----------|-------------|
| **Structured over prose** | Use JSON objects, not free-text descriptions |
| **Immutable append** | Never modify past entries; add new entries with references |
| **Causally linked** | Every correction links to the issue that triggered it |
| **Diff-aware** | Capture before/after state for all modifications |
| **Timestamp everything** | ISO 8601 format with timezone |

---

## 2. Log File Structure

### 2.1 Primary Log File

**Location:** `{project}/design_documents/test_progress.json`

```json
{
  "test_plan_version": "string",
  "current_phase": "number",
  "phase_name": "string",
  "last_checkpoint": "ISO8601 timestamp",

  "documents": { },
  "commands_executed": [ ],
  "agents_invoked": [ ],
  "review_iterations": [ ],
  "issues_encountered": [ ],
  "corrections_applied": [ ],
  "patterns_learned": [ ],
  "batch_operations": [ ],
  "sync_results": { },
  "improve_results": { },
  "final_sign_off": { },
  "backport_notes": { }
}
```

### 2.2 Supplementary Log Files (Optional)

For large test runs, split into:

| File | Contents |
|------|----------|
| `test_progress.json` | Summary and current state |
| `test_commands.jsonl` | Append-only command log (JSON Lines format) |
| `test_reviews.jsonl` | Detailed review results |
| `test_corrections.jsonl` | All corrections with diffs |

---

## 3. Schema Definitions

### 3.1 Command Execution Log

**Trigger:** Every slash command invocation

```json
{
  "command_id": "CMD-{sequential_number}",
  "command": "/doc:{command_name}",
  "args": "string - full argument string",
  "timestamp_start": "ISO8601",
  "timestamp_end": "ISO8601",
  "duration_ms": "number",
  "status": "success | failed | partial",
  "doc_id": "string | null",
  "agent_spawned": "string | null",
  "result": {
    "type": "generate | review | sync | batch | status | improve",
    "output_path": "string | null",
    "output_lines": "number | null",
    "score": "number | null",
    "grade": "string | null",
    "blockers": "number",
    "warnings": "number",
    "suggestions": "number",
    "auto_fixes_applied": "number"
  },
  "error": {
    "type": "string | null",
    "message": "string | null",
    "stack_trace": "string | null"
  },
  "triggered_by": "CMD-{id} | user | batch-{id} | null",
  "triggers": ["CMD-{id}", "..."]
}
```

### 3.2 Agent Invocation Log

**Trigger:** Every agent spawn via Task tool

```json
{
  "invocation_id": "AGT-{sequential_number}",
  "agent": "doc-writer | doc-reviewer | doc-librarian | doc-orchestrator",
  "model": "sonnet | opus | haiku",
  "doc_id": "string",
  "timestamp_start": "ISO8601",
  "timestamp_end": "ISO8601",
  "duration_ms": "number",
  "status": "success | failed | timeout",
  "iteration": "number - 1-indexed iteration count for this doc",
  "input": {
    "spec_path": "string | null",
    "doc_path": "string | null",
    "config_files_read": ["string", "..."]
  },
  "output": {
    "lines_generated": "number | null",
    "sections_created": "number | null",
    "diagrams_created": "number | null"
  },
  "tokens": {
    "input": "number | null",
    "output": "number | null"
  },
  "triggered_by_command": "CMD-{id}"
}
```

### 3.3 Review Iteration Log

**Trigger:** Every `/doc-review` completion

```json
{
  "iteration_id": "REV-{doc_id}-{iteration_number}",
  "doc_id": "string",
  "doc_path": "string",
  "spec_path": "string | null",
  "iteration": "number",
  "timestamp": "ISO8601",
  "score_before": "number | null - from previous iteration",
  "score_after": "number",
  "grade": "A | B | C | D | F",
  "passed": "boolean",
  "gates_checked": [
    {
      "gate": "spec_completeness | content_quality | consistency | final_approval",
      "passed": "boolean",
      "score": "number",
      "weight": "number"
    }
  ],
  "issues_found": [
    {
      "issue_id": "ISS-{number}",
      "severity": "blocker | warning | suggestion",
      "category": "spec_compliance | content_quality | terminology | style | structure",
      "rule_id": "string - from quality-gates.json",
      "location": {
        "line_start": "number | null",
        "line_end": "number | null",
        "section": "string | null"
      },
      "description": "string",
      "detected_value": "string | null - the actual problematic content",
      "expected_value": "string | null - what was expected",
      "auto_fixable": "boolean",
      "auto_fixed": "boolean",
      "fix_applied": "string | null - description of fix"
    }
  ],
  "iteration_required": "boolean",
  "next_action": "approve | iterate | escalate | manual_review"
}
```

### 3.4 Issue Log

**Trigger:** Any blocker or significant warning encountered

```json
{
  "issue_id": "ISS-{sequential_number}",
  "timestamp_detected": "ISO8601",
  "timestamp_resolved": "ISO8601 | null",
  "severity": "blocker | warning | info",
  "category": "spec_compliance | content_quality | terminology | style | system_behavior | configuration",
  "source": {
    "phase": "number",
    "command_id": "CMD-{id}",
    "doc_id": "string | null",
    "review_iteration": "REV-{id} | null"
  },
  "description": "string - clear description of the issue",
  "evidence": {
    "file": "string | null",
    "line_range": "string | null - e.g., '1089-1091'",
    "content_sample": "string | null - truncated sample of problematic content",
    "rule_violated": "string | null - reference to quality gate rule"
  },
  "status": "open | investigating | resolved | wont_fix | deferred",
  "resolution": {
    "type": "document_fix | config_fix | system_fix | false_positive | by_design",
    "description": "string",
    "correction_id": "COR-{id} | null"
  },
  "root_cause": "string | null - analysis of why this happened",
  "prevention": "string | null - how to prevent recurrence"
}
```

### 3.5 Correction Log

**Trigger:** Any fix applied to resolve an issue

```json
{
  "correction_id": "COR-{sequential_number}",
  "timestamp": "ISO8601",
  "issue_id": "ISS-{id} - the issue this corrects",
  "type": "document_edit | config_update | template_fix | rule_exception | pattern_addition",
  "target": {
    "file": "string - path to modified file",
    "repository": "string - which repo (target project or upstream)"
  },
  "change": {
    "description": "string",
    "before": "string | null - content before (truncated if large)",
    "after": "string | null - content after (truncated if large)",
    "diff_summary": "string | null - e.g., '+15 lines, -3 lines'",
    "sections_affected": ["string", "..."]
  },
  "validation": {
    "tested": "boolean",
    "test_result": "pass | fail | null",
    "score_improvement": "number | null - points gained"
  },
  "backport_required": "boolean",
  "backport_status": "pending | applied | not_applicable",
  "learned_pattern": {
    "pattern_id": "string | null - if this created a new pattern",
    "anti_pattern_id": "string | null - if this identified an anti-pattern"
  }
}
```

### 3.6 Pattern Learning Log

**Trigger:** `/doc-improve` execution or manual pattern identification

```json
{
  "learning_id": "LRN-{sequential_number}",
  "timestamp": "ISO8601",
  "source": {
    "command_id": "CMD-{id} | null",
    "documents_analyzed": ["string", "..."],
    "corrections_referenced": ["COR-{id}", "..."]
  },
  "patterns_added": [
    {
      "pattern_id": "string",
      "category": "api-documentation | design-documentation | user-manual | all",
      "description": "string",
      "effectiveness_score": "number 0.0-1.0",
      "source_document": "string",
      "example": "string | null"
    }
  ],
  "patterns_reinforced": [
    {
      "pattern_id": "string",
      "previous_usage_count": "number",
      "new_usage_count": "number",
      "effectiveness_delta": "number"
    }
  ],
  "anti_patterns_added": [
    {
      "anti_pattern_id": "string",
      "category": "string",
      "description": "string",
      "severity": "blocker | warning | suggestion",
      "detection_pattern": "string",
      "correction": "string",
      "source_issue": "ISS-{id} | null"
    }
  ],
  "terminology_added": [
    {
      "term": "string",
      "definition": "string",
      "source": "string"
    }
  ],
  "expertise_version_before": "string",
  "expertise_version_after": "string"
}
```

### 3.7 Batch Operation Log

**Trigger:** `/doc-batch` execution

```json
{
  "batch_id": "BATCH-{sequential_number}",
  "operation": "generate | review",
  "timestamp_start": "ISO8601",
  "timestamp_end": "ISO8601",
  "duration_ms": "number",
  "parallel": "boolean",
  "continue_on_error": "boolean",
  "documents": [
    {
      "doc_id": "string",
      "dependency_level": "number - 0 = no deps, higher = more deps",
      "status": "success | failed | skipped",
      "command_id": "CMD-{id}",
      "error": "string | null"
    }
  ],
  "summary": {
    "total": "number",
    "succeeded": "number",
    "failed": "number",
    "skipped": "number",
    "total_lines": "number | null",
    "average_score": "number | null"
  }
}
```

---

## 4. Logging Triggers

### 4.1 Automatic Triggers

| Event | Log Entry | Required Fields |
|-------|-----------|-----------------|
| Slash command starts | `commands_executed` append | command_id, command, args, timestamp_start |
| Slash command completes | `commands_executed` update | timestamp_end, status, result |
| Agent spawned | `agents_invoked` append | All fields |
| Review completes | `review_iterations` append | All fields including issues_found |
| Blocker detected | `issues_encountered` append | issue_id through evidence |
| Fix applied | `corrections_applied` append | All fields |
| Batch starts | `batch_operations` append | batch_id, operation, documents list |
| `/doc-improve` runs | `patterns_learned` append | All fields |

### 4.2 Manual Triggers

These require explicit logging calls:

| Event | When to Log |
|-------|-------------|
| Root cause identified | After analyzing why an issue occurred |
| Prevention strategy | After determining how to avoid recurrence |
| Backport decision | When deciding if fix needs upstream |
| False positive | When issue was incorrectly flagged |

---

## 5. Data Relationships

```
┌─────────────────┐
│ commands_executed│
└────────┬────────┘
         │ triggers
         ▼
┌─────────────────┐      ┌──────────────────┐
│ agents_invoked  │      │ review_iterations │
└────────┬────────┘      └────────┬─────────┘
         │                        │ contains
         │                        ▼
         │               ┌──────────────────┐
         │               │ issues_encountered│
         │               └────────┬─────────┘
         │                        │ resolved_by
         │                        ▼
         │               ┌──────────────────┐
         └──────────────►│corrections_applied│
                         └────────┬─────────┘
                                  │ creates
                                  ▼
                         ┌──────────────────┐
                         │ patterns_learned │
                         └──────────────────┘
```

---

## 6. Query Examples

### 6.1 Find All Corrections for a Specific Issue Type

```python
def find_corrections_by_category(log: dict, category: str) -> list:
    issue_ids = [
        iss["issue_id"]
        for iss in log["issues_encountered"]
        if iss["category"] == category
    ]
    return [
        cor for cor in log["corrections_applied"]
        if cor["issue_id"] in issue_ids
    ]
```

### 6.2 Calculate Iteration Efficiency

```python
def iteration_efficiency(log: dict, doc_id: str) -> dict:
    iterations = [
        rev for rev in log["review_iterations"]
        if rev["doc_id"] == doc_id
    ]
    if not iterations:
        return None

    return {
        "doc_id": doc_id,
        "total_iterations": len(iterations),
        "initial_score": iterations[0]["score_after"],
        "final_score": iterations[-1]["score_after"],
        "improvement": iterations[-1]["score_after"] - iterations[0]["score_after"],
        "issues_resolved": sum(
            len([i for i in rev["issues_found"] if i["auto_fixed"]])
            for rev in iterations
        )
    }
```

### 6.3 Extract Backport Candidates

```python
def get_backport_candidates(log: dict) -> list:
    return [
        {
            "correction_id": cor["correction_id"],
            "file": cor["target"]["file"],
            "description": cor["change"]["description"],
            "issue": cor["issue_id"]
        }
        for cor in log["corrections_applied"]
        if cor["backport_required"] and cor["backport_status"] == "pending"
    ]
```

---

## 7. Retention and Archival

### 7.1 Active Test

- Keep full `test_progress.json` in project
- Update in real-time during test execution

### 7.2 Post-Test

| Action | Timing |
|--------|--------|
| Archive to `test_archives/{date}_{suite_id}/` | On test completion |
| Extract learnings to expertise files | Via `/doc-improve` |
| Apply backports to upstream | Before next test cycle |
| Summarize in test report | For stakeholder review |

### 7.3 Aggregation

For multi-test analysis:

```json
{
  "aggregate_stats": {
    "tests_run": "number",
    "total_documents": "number",
    "total_issues": "number",
    "issues_by_category": { },
    "corrections_by_type": { },
    "average_iterations_to_pass": "number",
    "most_common_issues": [ ],
    "most_effective_patterns": [ ]
  }
}
```

---

## 8. Integration Points

### 8.1 Hooks

The logging system should integrate with Claude Code hooks:

```python
# doc_pre_write.py - Log command start
def log_command_start(command: str, args: str) -> str:
    return json.dumps({
        "command_id": generate_id("CMD"),
        "command": command,
        "args": args,
        "timestamp_start": datetime.utcnow().isoformat() + "Z"
    })

# doc_post_write.py - Log command completion
def log_command_complete(command_id: str, result: dict) -> None:
    # Append to test_progress.json
    pass
```

### 8.2 Agent Reporting

Agents should return structured results:

```json
{
  "status": "success",
  "output": {
    "path": "...",
    "lines": 1505,
    "sections": 12,
    "diagrams": 3
  },
  "issues_detected": [ ],
  "suggestions": [ ]
}
```

---

## 9. Validation

### 9.1 Log Integrity Checks

Run after each phase:

| Check | Validation |
|-------|------------|
| Referential integrity | All `*_id` references resolve |
| Temporal consistency | Timestamps are monotonically increasing |
| Status consistency | No `resolved` issues without `correction_id` |
| Completeness | No `null` required fields |

### 9.2 Schema Validation

Use JSON Schema to validate log structure:

```bash
# Validate test_progress.json against schema
jsonschema -i test_progress.json e2e-test-logging-schema.json
```

---

## 10. Example: Complete Issue-to-Pattern Flow

```json
{
  "issues_encountered": [{
    "issue_id": "ISS-004",
    "severity": "blocker",
    "category": "system_behavior",
    "description": "Protocol ellipsis flagged as placeholder",
    "evidence": {
      "rule_violated": "no_placeholders",
      "content_sample": "def process(self, data: Any) -> Result:\n    ..."
    },
    "status": "resolved",
    "resolution": {
      "type": "config_fix",
      "correction_id": "COR-001"
    },
    "root_cause": "Quality gate lacks context awareness for PEP 544",
    "prevention": "Added anti-pattern to detect future false positives"
  }],

  "corrections_applied": [{
    "correction_id": "COR-001",
    "issue_id": "ISS-004",
    "type": "rule_exception",
    "target": {
      "file": ".claude/docs/config/quality-gates.json"
    },
    "change": {
      "description": "Added python_protocol_ellipsis exception",
      "after": "{ \"exceptions\": [{ \"id\": \"python_protocol_ellipsis\", ... }] }"
    },
    "validation": {
      "tested": true,
      "test_result": "pass",
      "score_improvement": 23
    },
    "backport_required": true,
    "learned_pattern": {
      "anti_pattern_id": "false-positive-protocol-ellipsis"
    }
  }],

  "patterns_learned": [{
    "learning_id": "LRN-001",
    "corrections_referenced": ["COR-001"],
    "anti_patterns_added": [{
      "anti_pattern_id": "false-positive-protocol-ellipsis",
      "category": "design-documentation",
      "description": "Flagging valid Python Protocol/ABC ellipsis as placeholder",
      "severity": "blocker",
      "source_issue": "ISS-004"
    }]
  }]
}
```

---

## Appendix A: ID Generation

| Prefix | Scope | Format | Example |
|--------|-------|--------|---------|
| CMD | Per test | Sequential | CMD-001, CMD-002 |
| AGT | Per test | Sequential | AGT-001 |
| REV | Per document | `{doc_id}-{iteration}` | REV-04-sdd-2 |
| ISS | Per test | Sequential | ISS-004 |
| COR | Per test | Sequential | COR-001 |
| LRN | Per test | Sequential | LRN-001 |
| BATCH | Per test | Sequential | BATCH-001 |

## Appendix B: Severity Definitions

| Severity | Definition | Action Required |
|----------|------------|-----------------|
| **blocker** | Prevents approval; must be resolved | Immediate fix or config change |
| **warning** | Should be addressed; can be deferred | Fix before production |
| **suggestion** | Optional improvement | Consider for future |
| **info** | Informational only | No action needed |
