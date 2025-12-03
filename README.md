# Spec-Driven Technical Document Creation System

A Claude Code framework for creating, reviewing, and maintaining technical documentation at scale using a specification-first approach.

---

## Essential Understanding

**Spec-Driven Docs System** is a documentation framework that runs within Claude Code. It provides:

- **7 slash commands** for the complete documentation lifecycle
- **4 specialized AI agents** optimized for different documentation tasks
- **3 document templates** for API, design, and user manual documentation
- **Quality gates and consistency rules** for professional-grade output

### How It Works

```text
1. PLAN    →  /doc-plan creates a specification from your topic
2. WRITE   →  /doc-write generates the document from the spec
3. REVIEW  →  /doc-review validates quality and consistency
4. ITERATE →  Fix issues or regenerate until approved
```

The specification-first approach ensures documentation quality by defining requirements before generation, enabling validation at every step.

---

## Quick Start (5 Minutes)

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

### Your First Document

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
   /doc-review docs/api/user-authentication.md
   ```

### Verify Installation

Run `/doc-status` to see your documentation dashboard. If you see the status output, the system is ready.

---

## Documentation

| Document | Purpose |
|----------|---------|
| [User Guide](docs/User-Guide/User-Guide.md) | Comprehensive guide to all features |

### Related Documentation

| Document | Purpose |
|----------|---------|
| [DIRECTIVES.md](DIRECTIVES.md) | Mandatory anti-shortcut directives for complete implementation |
| [CLAUDE.md](CLAUDE.md) | Project guidance for Claude Code sessions |
| [AGENTS.md](AGENTS.md) | Repository guidelines and agent coordination |

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Commands** | 7 slash commands for planning, writing, reviewing, syncing, batching, status, and learning |
| **Agents** | 4 specialized AI agents: Orchestrator (Opus), Writer (Sonnet), Reviewer (Sonnet), Librarian (Haiku) |
| **Templates** | 3 document types: API documentation, design documents, user manuals |
| **Quality System** | 4 quality gates, consistency rules, terminology enforcement, scoring (A-F grades) |
| **Suites** | Organize related documents for batch operations and cross-reference management |

---

## Command Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `/doc-plan` | Create document specification | `/doc-plan "REST API" --type api` |
| `/doc-write` | Generate document from spec | `/doc-write specs/docs/api-spec.md` |
| `/doc-review` | Validate document quality | `/doc-review docs/api/users.md --fix` |
| `/doc-sync` | Synchronize suite consistency | `/doc-sync my-suite` |
| `/doc-batch` | Batch operations across suite | `/doc-batch my-suite generate` |
| `/doc-status` | View documentation dashboard | `/doc-status my-suite` |
| `/doc-improve` | Learn from successful docs | `/doc-improve` |

### Common Workflows

**Single Document:**

```bash
/doc-plan "Feature X" --type manual
/doc-write specs/docs/feature-x-spec.md
/doc-review docs/guides/feature-x.md
```

**Suite Batch Processing:**

```bash
/doc-batch api-docs generate --parallel
/doc-batch api-docs review
/doc-sync api-docs --fix
```

---

## How Everything Connects

```text
                    ┌─────────────────┐
                    │   /doc-plan     │
                    │  (Orchestrator) │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Specification  │
                    │   (specs/docs/) │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   /doc-write    │
                    │    (Writer)     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Document     │
                    │    (docs/)      │
                    └────────┬────────┘
                             │
                             ▼
┌─────────────┐     ┌─────────────────┐     ┌─────────────┐
│  /doc-sync  │◄────│   /doc-review   │────►│ /doc-improve│
│ (Librarian) │     │   (Reviewer)    │     │(Orchestrator│
└─────────────┘     └─────────────────┘     └─────────────┘
```

---

## Agent Architecture

The system uses specialized Claude agents to scale document processing:

| Agent | Model | Purpose |
|-------|-------|---------|
| **doc-orchestrator** | Opus | Strategy, requirement analysis, multi-document coordination |
| **doc-writer** | Sonnet | Technical document generation from specifications |
| **doc-reviewer** | Sonnet | Quality validation, accuracy checking, consistency enforcement |
| **doc-librarian** | Haiku | Quick consistency checks, cross-references, index maintenance |

### Agent Integration

- `/doc-plan` spawns **doc-orchestrator** for requirement gathering
- `/doc-write` spawns **doc-writer** for content generation
- `/doc-review` spawns **doc-reviewer** for quality validation
- `/doc-sync` spawns **doc-librarian** for cross-reference checks
- `/doc-batch` coordinates multiple agents for parallel processing

---

## Quality Grades

Documents are scored on a 0-100 scale:

| Grade | Score | Status |
|-------|-------|--------|
| A | 90-100 | Approved |
| B | 80-89 | Approved with notes |
| C | 70-79 | Iteration recommended |
| D | 60-69 | Iteration required |
| F | <60 | Blocked |

---

## Project Structure

```text
your-project/
├── .claude/
│   ├── agents/              # AI agent definitions
│   │   ├── doc-orchestrator.md
│   │   ├── doc-writer.md
│   │   ├── doc-reviewer.md
│   │   └── doc-librarian.md
│   ├── commands/doc/        # Slash command definitions
│   │   ├── doc-plan.md
│   │   ├── doc-write.md
│   │   ├── doc-review.md
│   │   ├── doc-batch.md
│   │   ├── doc-sync.md
│   │   ├── doc-status.md
│   │   ├── doc-improve.md
│   │   └── _doc-helpers/
│   ├── docs/
│   │   ├── config/          # Quality gates, consistency rules
│   │   ├── expertise/       # Patterns, anti-patterns, domain knowledge
│   │   ├── suites/          # Documentation suite manifests
│   │   └── templates/       # Document type templates
│   └── hooks/               # Pre/post write validation
├── specs/docs/              # Document specifications
└── docs/                    # Generated documentation
    └── User-Guide/          # This user guide
```

---

## Configuration

### Consistency Rules

Located at `.claude/docs/config/consistency-rules.json`:

- Terminology enforcement (preferred terms vs alternatives)
- Style rules (header case, list style, code blocks)
- Forbidden patterns (placeholders, incomplete markers)

### Quality Gates

Located at `.claude/docs/config/quality-gates.json`:

- Spec completeness checks
- Content quality validation
- Consistency verification
- Final approval criteria

### Expertise Store

Located at `.claude/docs/expertise/`:

- `patterns.json`: Effective documentation patterns
- `anti-patterns.json`: Patterns to avoid
- `domain-knowledge.json`: Project-specific terminology

---

## Mandatory Directives

This project enforces strict anti-shortcut directives for all AI-generated content. See [DIRECTIVES.md](DIRECTIVES.md) for complete details.

**Key requirements:**

- Complete implementation only - no placeholders, ellipsis, TODO/FIXME
- No simulation - all operations must be real, no mocked data
- Fix implementation, not tests - TDD integrity must be maintained

---

## Getting Help

- **Full Documentation:** [User Guide](docs/User-Guide/User-Guide.md)
- **Command Help:** Run any command without arguments for usage information
- **Quality Issues:** Use `/doc-review <doc> --fix` for auto-fixable issues

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Command not found | Ensure `.claude/commands/doc/` exists |
| Template not found | Check `.claude/docs/templates/` directory |
| Quality gate failures | Run `/doc-review <doc>` to see specific issues |
| Suite not found | Verify suite manifest in `.claude/docs/suites/` |

---

## License

MIT
