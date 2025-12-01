# Spec-Driven Technical Document Creation System

A comprehensive documentation system for Claude Code that enables specification-driven document generation, review, and batch operations.

## Features

- **Specification-First Workflow**: Create detailed specs before generating documents
- **Template-Based Generation**: Consistent output using API, Design, and Manual templates
- **Quality Gates**: Automated validation with configurable quality thresholds
- **Batch Operations**: Process multiple documents with dependency resolution
- **Consistency Enforcement**: Terminology rules and forbidden pattern detection
- **Pre/Post Write Hooks**: Automatic validation before and after document writes

## Installation

1. Copy the `.claude` directory to your project root:
   ```bash
   cp -r .claude /path/to/your/project/
   ```

2. Copy the `specs` directory for specification storage:
   ```bash
   cp -r specs /path/to/your/project/
   ```

3. Ensure hooks are registered in your `.claude/settings.json`:
   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Write.*docs/.*\\.md$",
           "hooks": [".claude/hooks/doc_pre_write.py"]
         }
       ],
       "PostToolUse": [
         {
           "matcher": "Write.*docs/.*\\.md$",
           "hooks": [".claude/hooks/doc_post_write.py"]
         }
       ]
     }
   }
   ```

## Commands

| Command | Description |
|---------|-------------|
| `/doc-plan <topic>` | Create a document specification |
| `/doc-write <spec-path>` | Generate document from specification |
| `/doc-review <doc-path>` | Review document quality and consistency |
| `/doc-batch <suite> <op>` | Batch operations across a suite |
| `/doc-sync <suite>` | Synchronize cross-references |
| `/doc-status [suite]` | Display documentation status |
| `/doc-improve` | Update expertise from recent work |

## Document Types

- **API Documentation** (`api`): Endpoint references, authentication, error handling
- **Design Documents** (`design`): Architecture decisions, trade-offs, implementation plans
- **User Manuals** (`manual`): Getting started guides, tutorials, troubleshooting

## Agents

The system uses specialized Claude agents to scale document processing. Each agent has its own context window and expertise:

| Agent | Model | Purpose |
|-------|-------|---------|
| **doc-orchestrator** | Opus | High-level strategy, requirement analysis, multi-document coordination |
| **doc-writer** | Sonnet | Technical document generation from specifications |
| **doc-reviewer** | Sonnet | Quality validation, accuracy checking, consistency enforcement |
| **doc-librarian** | Haiku | Quick consistency checks, cross-references, index maintenance |

### Agent Integration

- `/doc-plan` → spawns **doc-orchestrator** for requirement gathering
- `/doc-write` → spawns **doc-writer** for content generation
- `/doc-review` → spawns **doc-reviewer** for quality validation
- `/doc-sync` → spawns **doc-librarian** for cross-reference checks
- `/doc-batch` → coordinates multiple agents for parallel processing

## Directory Structure

```
.claude/
├── agents/                  # Specialized sub-agents
│   ├── doc-orchestrator.md  # Strategy and coordination
│   ├── doc-writer.md        # Document generation
│   ├── doc-reviewer.md      # Quality validation
│   └── doc-librarian.md     # Cross-reference management
├── commands/doc/            # Slash commands
│   ├── doc-plan.md
│   ├── doc-write.md
│   ├── doc-review.md
│   ├── doc-batch.md
│   ├── doc-sync.md
│   ├── doc-status.md
│   ├── doc-improve.md
│   └── _doc-helpers/        # Internal helper commands
├── docs/
│   ├── config/              # Consistency rules, quality gates
│   ├── expertise/           # Patterns, anti-patterns, domain knowledge
│   ├── templates/           # Document templates
│   └── suites/              # Suite manifests
└── hooks/
    ├── doc_pre_write.py     # Pre-write validation
    └── doc_post_write.py    # Post-write consistency checks

specs/docs/                   # Document specifications
```

## Quick Start

1. **Plan a document**:
   ```
   /doc-plan "API Reference for User Service" --type api
   ```

2. **Generate the document**:
   ```
   /doc-write specs/docs/user-service-api-spec.md
   ```

3. **Review the output**:
   ```
   /doc-review docs/api/user-service.md --spec specs/docs/user-service-api-spec.md
   ```

## Configuration

### Consistency Rules (`.claude/docs/config/consistency-rules.json`)
- Terminology enforcement (preferred terms vs alternatives)
- Style rules (header case, list style, code blocks)
- Forbidden patterns (placeholders, incomplete markers)

### Quality Gates (`.claude/docs/config/quality-gates.json`)
- Spec completeness checks
- Content quality validation
- Consistency verification
- Final approval criteria

### Expertise Store (`.claude/docs/expertise/`)
- `patterns.json`: Effective documentation patterns
- `anti-patterns.json`: Patterns to avoid
- `domain-knowledge.json`: Project-specific terminology

## License

MIT
