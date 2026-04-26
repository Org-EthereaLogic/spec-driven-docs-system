# Spec-driven technical document creation system

[![Tests](https://img.shields.io/badge/tests-smoke%20suite-blue)](tests/smoke.sh)
[![Markdown lint](https://img.shields.io/badge/markdownlint-enabled-brightgreen)](package.json)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Spec-first workflow](https://img.shields.io/badge/workflow-spec--first-purple)](specs/docs/README.md)
[![Claude Code](https://img.shields.io/badge/platform-Claude%20Code-orange)](CLAUDE.md)

Create high-quality technical documentation faster with a spec-first workflow for Claude Code.

Most documentation projects fail because teams jump straight into writing, then discover gaps in scope, voice, structure,
and consistency late in review. This framework prevents that by making planning mandatory, generating from explicit specs,
and enforcing quality gates before promotion.

In 5 minutes, plan a document, generate a draft, and run quality review using built-in slash commands.

---

## Why teams use this project

- Define requirements before generation to reduce rewrites
- Standardize output across all document types
- Catch issues early with automated quality gates
- Scale work with specialized AI agents

## How it works

```text
1. PLAN    →  /doc-plan creates a specification from your topic
2. WRITE   →  /doc-write generates the document from the spec
3. REVIEW  →  /doc-review validates quality and consistency
4. ITERATE →  Fix issues or regenerate until approved
5. PROMOTE →  /doc-promote moves the document through workflow stages
```

The specification-first approach ensures quality by defining requirements before generation and validating at every step.

For a one-command shortcut through the full pipeline, use `/doc-flow "Topic" --type api --auto-promote` — it runs plan → write → review → promote in sequence with smart model selection and daily caching of spec analysis. New users can start with `/doc-interactive` for a guided walkthrough.

---

## In practice

<p align="center">
  <img src="app_docs/assets/readme-cli-preview.svg" alt="CLI workflow preview" width="960" />
</p>

This preview shows the typical workflow: plan a specification, generate a draft, review it against
quality gates, then promote it through the workflow.

---

## Quick start (5 minutes)

### Prerequisites

- Claude Code CLI installed and configured
- A project directory for your documentation

### Installation

Copy the framework files to your project:

```bash
# Copy the .claude configuration directory
cp -r .claude /path/to/your/project/

# Copy the specs directory for document specifications
cp -r specs /path/to/your/project/
```

### Try it now

1. **Plan your document:**

   ```bash
   /doc-plan "User Authentication API" --type api
   ```

2. **Generate the document:**

   ```bash
   /doc-write specs/docs/user-authentication-api-spec.md
   ```

3. **Review the output:**

   ```bash
   /doc-review spec_driven_docs/rough_draft/api/user-authentication.md
   ```

4. **Promote the document through the workflow:**

   ```bash
   /doc-promote spec_driven_docs/rough_draft/api/user-authentication.md --to pending_approval
   ```

### Verify installation

Run `/doc-status` to see your documentation dashboard. If you see status output, the system is ready.

For a local clone-based end-to-end check, run `npm run test:e2e`. This test clones the repository into a temporary
directory, installs dependencies, runs the smoke suite, generates three sample documents, runs the hooks, and verifies
promotion into `pending_approval/`.

---

## Documentation

| Document | Purpose |
|----------|---------|
| [User Guide](app_docs/User-Guide/User-Guide.md) | Comprehensive guide to all features |
| [FAQ](FAQ.md) | Common questions about setup, workflow, and quality gates |
| [Contributing](CONTRIBUTING.md) | Contribution workflow, standards, and quality expectations |

### Related documentation

| Document | Purpose |
|----------|---------|
| [DIRECTIVES.md](DIRECTIVES.md) | Mandatory anti-shortcut directives for complete implementation |
| [CLAUDE.md](CLAUDE.md) | Project guidance for Claude Code sessions |
| [AGENTS.md](AGENTS.md) | Repository guidelines and agent coordination |

---

## Key concepts

| Concept | Description |
|---------|-------------|
| **Commands** | 8 slash commands for the full workflow |
| **Agents** | 4 specialized AI agents with distinct roles |
| **Templates** | 3 document types: API docs, design docs, manuals |
| **Quality system** | 4 gates with A-F grading and consistency enforcement |
| **Suites** | Group docs for batch operations |

## Command reference

| Command | Purpose | Example |
|---------|---------|---------|
| `/doc-flow` | Auto pipeline | `/doc-flow "REST API" --type api --auto-promote` |
| `/doc-interactive` | Guided creation | `/doc-interactive` |
| `/doc-plan` | Create specification | `/doc-plan "REST API" --type api` |
| `/doc-write` | Generate from spec | `/doc-write specs/docs/api-spec.md` |
| `/doc-review` | Validate quality | `/doc-review spec_driven_docs/rough_draft/api/users.md` |
| `/doc-sync` | Sync suite consistency | `/doc-sync my-suite` |
| `/doc-batch` | Batch operations | `/doc-batch my-suite generate` |
| `/doc-status` | View dashboard | `/doc-status my-suite` |
| `/doc-improve` | Learn patterns | `/doc-improve` |
| `/doc-promote` | Promote document | `/doc-promote <path> --to pending_approval` |
| `/doc-config` | Manage configuration | `/doc-config get quality_profiles.api.min_score` |

### Common workflows

**Single document:**

```bash
/doc-plan "Feature X" --type manual
/doc-write specs/docs/feature-x-spec.md
/doc-review spec_driven_docs/rough_draft/guides/feature-x.md
/doc-promote spec_driven_docs/rough_draft/guides/feature-x.md --to pending_approval
```

**Suite batch processing:**

```bash
/doc-batch api-docs generate --parallel
/doc-batch api-docs review
/doc-sync api-docs --fix
```

---

## How everything connects

```text
       ┌──────────────┐
       │  /doc-plan   │
       │(Orchestrator)│
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │Specification │
       │(specs/docs/) │
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │ /doc-write   │
       │  (Writer)    │
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │  Document    │
       │(rough_draft/)│
       └──────┬───────┘
              │
              ▼
 ┌──────────┐ ┌──────────────┐ ┌────────────────┐
 │/doc-sync │◄│/doc-review   │►│ /doc-improve   │
 │(Librarian)│ │(Reviewer)    │ │(Orchestrator) │
 └──────────┘ └──────────────┘ └────────────────┘
```

---

## Agent architecture

The system uses specialized Claude agents to scale document processing:

| Agent | Model | Purpose |
|-------|-------|---------|
| **doc-orchestrator** | Opus | Strategy & multi-document coordination |
| **doc-writer** | Sonnet | Generate docs from specifications |
| **doc-reviewer** | Sonnet | Quality & consistency validation |
| **doc-librarian** | Haiku | Cross-reference & consistency checks |

### Agent integration

- `/doc-plan` spawns **doc-orchestrator** for requirement gathering
- `/doc-write` spawns **doc-writer** for content generation
- `/doc-review` spawns **doc-reviewer** for quality validation
- `/doc-sync` spawns **doc-librarian** for cross-reference checks
- `/doc-batch` coordinates agents for parallel processing
- `/doc-promote` validates gates and moves documents: `rough_draft/` → `pending_approval/` → `approved_final/`

### Utility agents

| Agent | Model | Purpose |
|-------|-------|---------|
| **workspace-cleanup** | Haiku | Maintenance & file organization |
| **prompt-enhance-agent** | Sonnet | Clarify and structure prompts |

Utility agents handle development hygiene and prompt engineering tasks.

---

## Quality grades

| Grade | Score | Status |
|-------|-------|--------|
| A | 90-100 | Approved |
| B | 80-89 | Approved with notes |
| C | 70-79 | Iteration recommended |
| D | 60-69 | Iteration required |
| F | <60 | Blocked |

---

## Project structure

```text
.
├── .claude/                 # Commands, agents, hooks, templates, and quality rules
├── specs/docs/              # Input specifications
├── spec_driven_docs/        # Generated output by workflow stage
│   ├── rough_draft/
│   ├── pending_approval/
│   └── approved_final/
├── app_docs/                # End-user documentation
│   └── User-Guide/          # Framework user guide
├── prompt/                  # Prompt engineering resources
└── README.md                # This file
```

---

## License

MIT. See [LICENSE](LICENSE).
