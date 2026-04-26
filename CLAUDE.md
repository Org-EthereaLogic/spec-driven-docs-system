# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code framework for specification-driven technical documentation. It provides 8 slash commands, 4 specialized AI agents, and 3 document templates for creating, reviewing, and maintaining documentation at scale.

## Core Workflow

```text
/doc-plan "Topic" --type api|design|manual  → Creates specification in specs/docs/
/doc-write specs/docs/topic-spec.md         → Generates to spec_driven_docs/rough_draft/
/doc-review spec_driven_docs/rough_draft/...→ Validates quality (A-F grading)
After review passes                         → Move to pending_approval/
After stakeholder approval                  → Move to approved_final/
```

**Document Workflow:** `rough_draft/` → `pending_approval/` → `approved_final/`

## Key Commands

| Command | Purpose |
|---------|---------|
| `/doc-plan` | Create document specification with requirement gathering |
| `/doc-write` | Generate document from spec (spawns doc-writer agent) |
| `/doc-review` | Validate quality with auto-fix option (`--fix`) |
| `/doc-sync` | Synchronize terminology across a documentation suite |
| `/doc-batch` | Batch operations: `generate`, `review` with `--parallel` |
| `/doc-status` | View documentation dashboard |
| `/doc-improve` | Learn patterns from successful documents |
| `/doc-promote` | Move documents between workflow stages with quality gate verification |
| `/doc-flow` | Auto-orchestrate full pipeline (plan → write → review → promote) with smart model selection and daily caching |
| `/doc-config` | View and manage configuration (`list`, `get`, `set`, `validate`) |
| `/doc-interactive` | Guided step-by-step documentation creation using AskUserQuestion at each decision point |

## Agent Architecture

### Documentation Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| doc-orchestrator | Opus | Strategy, planning, multi-doc coordination |
| doc-writer | Sonnet | Document generation from specifications |
| doc-reviewer | Sonnet | Quality validation, consistency enforcement |
| doc-librarian | Haiku | Quick consistency checks, cross-references |

### Utility Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| workspace-cleanup | Haiku | Workspace maintenance, temp file removal |
| prompt-enhance-agent | Sonnet | Prompt clarity and structure enhancement |

Agent definitions: `.claude/agents/`

## Directory Structure

```text
.claude/
├── agents/              # Agent definitions (doc-orchestrator, doc-writer, etc.)
├── prompts/             # Conversation archives and prompt templates
├── plugins/             # Plugin extensions (commands, agents, templates, hooks)
│   └── _example/        # Example plugin skeleton
├── commands/doc/        # Slash command implementations
│   └── _doc-helpers/    # Internal helper commands
├── docs/
│   ├── config/          # quality-gates.json (with quality_profiles), consistency-rules.json
│   ├── expertise/       # patterns.json, anti-patterns.json, domain-knowledge.json
│   ├── suites/          # Documentation suite manifests
│   └── templates/       # api-docs.md, design-docs.md, user-manual.md, adr.md, rfc.md, openapi.md
└── hooks/               # Pre/post write validation (Python); shared utilities in hook_utils.py
specs/docs/              # Document specifications (input to /doc-write)
spec_driven_docs/        # Generated documentation output
├── rough_draft/         # Initial generation output
├── pending_approval/    # Reviewed, awaiting stakeholder approval
└── approved_final/      # Production-ready documentation
app_docs/                # End-user documentation (User Guide, tutorials)
```

## Quality System

- **4 Quality Gates:** spec_completeness → content_quality → consistency → final_approval
- **Grading:** A (90-100 approved), B (80-89 approved with notes), C (70-79 iterate), D (60-69 required), F (<60 blocked)
- **Quality Profiles:** Per-doc-type thresholds in `quality-gates.json` → `quality_profiles` (api 85, design 80, manual 75, quickstart 75, adr 80, rfc 82). The manual profile accepts section aliases (e.g. "Quickstart" satisfies "Getting Started"); the quickstart profile has no required section names.
- **Hooks:** `doc_pre_write.py` blocks writes with forbidden patterns; `doc_post_write.py` runs post-validation; `doc_post_review.py` suggests promotion on passing review
- **Shared utilities:** `hook_utils.py` provides common config loading, environment parsing, and structured feedback formatting

## Mandatory Directives (from DIRECTIVES.md)

- **Complete implementation only** - No placeholders, ellipsis, TODO/FIXME, NotImplementedError
- **No simulation** - Real operations, no mocked/fake data
- **Fix implementation, not tests** - TDD integrity must be maintained
- **Explore before acting** - Read and understand files before proposing edits
- **Avoid overengineering** - Only changes directly requested
- **Parallel tool calls** - Execute independent operations simultaneously

## Codacy Integration

When editing files, run Codacy analysis:

- Provider: `gh`
- Organization: `Org-EthereaLogic`
- Repository: `spec-driven-docs-system`

After any `edit_file` operation, immediately run `codacy_cli_analyze` on modified files.

## Configuration Files

| File | Purpose |
|------|---------|
| `.claude/docs/config/quality-gates.json` | Gate definitions and scoring formula |
| `.claude/docs/config/consistency-rules.json` | Terminology and style enforcement |
| `.claude/docs/expertise/patterns.json` | Effective documentation patterns |
| `.claude/docs/expertise/anti-patterns.json` | Patterns to avoid |
| `.claude/docs/expertise/domain-knowledge.json` | Project terminology |

## Creating New Documentation

1. Plan: `/doc-plan "Feature X API" --type api`
2. Review spec: Read `specs/docs/feature-x-api-spec.md`
3. Generate: `/doc-write specs/docs/feature-x-api-spec.md`
4. Validate: `/doc-review spec_driven_docs/rough_draft/api/feature-x.md --fix`
5. Approve: Move to `spec_driven_docs/pending_approval/` after review passes (Grade A/B)
6. Publish: Move to `spec_driven_docs/approved_final/` after stakeholder approval

## Suite Operations

Suites group related documents for batch processing:

```text
/doc-batch my-suite generate --parallel   # Generate all docs
/doc-batch my-suite review                # Review all docs
/doc-sync my-suite --fix                  # Fix consistency issues
```

Suite manifests: `.claude/docs/suites/{suite-id}/manifest.json`
