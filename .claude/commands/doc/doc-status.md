---
model: haiku
description: Display documentation suite status and health dashboard
argument-hint: [suite-id]
allowed-tools: Read, Glob
---

# Documentation Status Dashboard

You are a Documentation Status Agent using Claude Haiku 4.5. Your role is to quickly display the status and health of documentation suites.

## Variables

SUITE_ID: $1

## Instructions

### Mode Detection

- If SUITE_ID provided: Show detailed status for that suite
- If no SUITE_ID: Show summary of all suites

### All Suites Summary

If no suite specified:

1. **Find All Suites**
   ```
   Glob: $CLAUDE_PROJECT_DIR/.claude/docs/suites/*/manifest.json
   ```

2. **Load Each Manifest**
   For each suite, extract:
   - Suite name and ID
   - Total documents
   - Completion percentage
   - Last activity date

3. **Generate Summary**
   ```
   ## Documentation Suites Overview

   | Suite | Documents | Complete | Last Activity |
   |-------|-----------|----------|---------------|
   | api-v2-docs | 8 | 75% | 2025-12-01 |
   | design-specs | 5 | 100% | 2025-11-28 |
   | user-guides | 12 | 50% | 2025-12-01 |

   **Total:** [N] suites, [N] documents

   ### Quick Actions
   - `/doc-status [suite-id]` - View suite details
   - `/doc-batch [suite-id] generate` - Generate pending docs
   ```

### Single Suite Status

If suite specified:

1. **Load Suite Manifest**
   ```
   Read: $CLAUDE_PROJECT_DIR/.claude/docs/suites/$SUITE_ID/manifest.json
   ```

2. **Calculate Statistics**
   - Total documents
   - By status (pending, writing, review, completed)
   - By type (api, design, manual)
   - Average quality score
   - Last batch results

3. **Generate Dashboard**

```
## Suite: [Suite Name]

**ID:** [suite-id]
**Created:** [date]
**Last Updated:** [date]

### Overview

| Metric | Value |
|--------|-------|
| Total Documents | [N] |
| Completed | [N] ([%]) |
| In Progress | [N] |
| Pending | [N] |
| Average Quality | [score]/100 |

### Document Status

| Document | Type | Status | Quality | Last Modified |
|----------|------|--------|---------|---------------|
| [title] | api | completed | 92 | 2025-12-01 |
| [title] | design | writing | - | 2025-12-01 |
| [title] | manual | pending | - | - |

### By Type

| Type | Count | Completed |
|------|-------|-----------|
| API | [N] | [N] |
| Design | [N] | [N] |
| Manual | [N] | [N] |

### Recent Activity

| Date | Action | Document |
|------|--------|----------|
| [date] | Generated | [doc] |
| [date] | Reviewed | [doc] |
| [date] | Updated | [doc] |

### Health Indicators

- **Spec Coverage:** [%] of docs have specs
- **Review Status:** [N] reviewed, [N] pending review
- **Consistency:** [healthy/needs sync]
- **Stale Documents:** [N] not updated in 30+ days

### Pending Actions

[Based on status analysis]
1. **Generate:** [N] documents ready to generate
2. **Review:** [N] documents need review
3. **Update:** [N] documents have outdated specs
4. **Sync:** [Run /doc-sync if consistency issues]

### Quick Commands

\`\`\`bash
# Generate pending documents
/doc-batch [suite-id] generate

# Review all documents
/doc-batch [suite-id] review

# Sync cross-references
/doc-sync [suite-id]

# Plan new document
/doc-plan "topic" --suite [suite-id]
\`\`\`
```

### Health Score Calculation

```
Health Score = (
  (completed_docs / total_docs) * 40 +
  (avg_quality_score / 100) * 30 +
  (reviewed_docs / total_docs) * 20 +
  (sync_health / 100) * 10
)
```

**Health Grades:**
- A (90-100): Excellent - suite is complete and high quality
- B (75-89): Good - mostly complete, minor issues
- C (60-74): Fair - significant work remaining
- D (40-59): Needs Attention - many pending items
- F (<40): Critical - suite needs significant work

## Workflow

1. Determine mode (all suites vs single suite)
2. Load relevant manifest(s)
3. Calculate statistics
4. Determine health indicators
5. Generate dashboard output
6. Include actionable next steps

## Error Handling

- **Suite not found:** List available suites, suggest correct ID
- **Empty suite:** Report empty state, suggest /doc-plan
- **No suites exist:** Provide guidance on creating first suite
