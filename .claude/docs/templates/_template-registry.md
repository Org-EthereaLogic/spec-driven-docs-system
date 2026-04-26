# Document Template Registry

## Purpose
This registry catalogs available document templates and provides metadata for template discovery and selection.

---

## Available Templates

### api-docs
- **File:** `api-docs.md`
- **Type ID:** `api`
- **Description:** Template for REST API, GraphQL, and programmatic interface documentation
- **Target Audience:** Developers integrating with APIs
- **Required Sections:** Overview, Authentication, Endpoints, Error Handling, Rate Limits, Changelog
- **Key Features:**
  - Request/response examples
  - Parameter tables
  - Error code documentation
  - Authentication patterns

### design-docs
- **File:** `design-docs.md`
- **Type ID:** `design`
- **Description:** Template for system architecture, technical designs, and architectural decisions
- **Target Audience:** Engineering teams, architects, technical reviewers
- **Required Sections:** Problem Statement, Goals & Non-Goals, Proposed Solution, Alternatives Considered, Implementation Plan, Risks & Mitigations, Open Questions
- **Key Features:**
  - Architecture diagrams
  - Decision records
  - Trade-off analysis
  - Implementation phases

### user-manual
- **File:** `user-manual.md`
- **Type ID:** `manual`
- **Description:** Template for end-user documentation, guides, and how-to content
- **Target Audience:** End users, administrators, support staff
- **Required Sections:** Introduction, Getting Started, Core Concepts, How-To Guides, Troubleshooting, Reference
- **Key Features:**
  - Task-oriented instructions
  - Progressive disclosure
  - Troubleshooting matrix
  - Quick start guides

### adr (template variant)
- **File:** `adr.md`
- **Type ID:** `adr`
- **Description:** Architecture Decision Record - captures a single decision with context and consequences
- **Target Audience:** Engineering team, future maintainers, technical reviewers
- **Required Sections:** Status, Context, Decision, Consequences, Alternatives Considered
- **Key Features:**
  - Short format (300-800 words)
  - Status field with defined values (Proposed, Accepted, Deprecated, Superseded)
  - Filename convention: `ADR-NNN-short-title.md`
  - Write-once historical record (amend by superseding)

### rfc (template variant)
- **File:** `rfc.md`
- **Type ID:** `rfc`
- **Description:** Request for Comments - formal proposal for substantial changes
- **Target Audience:** Technical stakeholders, team leads, anyone affected by the change
- **Required Sections:** Abstract, Motivation, Detailed Design, Drawbacks, Alternatives, Unresolved Questions
- **Key Features:**
  - Standalone Abstract section
  - Mandatory Drawbacks analysis
  - Filename convention: `RFC-NNNN-short-title.md`
  - Status workflow: Draft → Under Review → Accepted/Rejected/Withdrawn

### openapi (template variant)
- **File:** `openapi.md`
- **Type ID:** `openapi`
- **Description:** Schema-first API reference in OpenAPI conceptual style
- **Target Audience:** External developers, integration teams, developer portal maintainers
- **Required Sections:** Overview, Authentication, Operations, Schemas, Errors, Rate Limits
- **Key Features:**
  - Schema-first format
  - Strict per-operation structure
  - Reusable schema definitions
  - Runnable examples required

---

## Template Selection Guide

| If documenting... | Use Template | Type ID |
|-------------------|--------------|---------|
| REST API endpoints | api-docs | `api` |
| GraphQL schema | api-docs | `api` |
| Authentication flows | api-docs | `api` |
| Public developer portal API reference | openapi | `openapi` |
| System architecture | design-docs | `design` |
| Feature design | design-docs | `design` |
| A single architectural choice already made | adr | `adr` |
| A formal proposal still under discussion | rfc | `rfc` |
| User guide | user-manual | `manual` |
| Admin guide | user-manual | `manual` |
| Tutorial | user-manual | `manual` |
| Installation guide | user-manual | `manual` |

---

## Template Metadata Schema

Each template should be parseable for automation:

```json
{
  "id": "string - unique template identifier",
  "file": "string - relative path to template file",
  "type_id": "string - short identifier for CLI/API usage",
  "description": "string - brief template description",
  "target_audience": ["array of audience types"],
  "required_sections": ["array of required section names"],
  "optional_sections": ["array of optional section names"],
  "style_rules": {
    "code_examples": "boolean - requires code examples",
    "diagrams": "boolean - requires diagrams",
    "tables": "boolean - prefers tabular data"
  }
}
```

---

## Adding New Templates

To add a new document template:

1. **Create the template file** in `/Users/etherealogic/Dev/.claude/docs/templates/`
   - Use existing templates as a guide
   - Include Purpose, Target Audience, Required Sections, Optional Sections, Style Guidelines

2. **Register the template** by adding an entry to this file
   - Add to "Available Templates" section
   - Add to "Template Selection Guide" table

3. **Update consistency rules** if the new template has unique requirements
   - Add required sections to `/docs/config/consistency-rules.json`

4. **Test the template** by generating a document
   - Run `/doc-plan "test topic" --type [new-type]`
   - Verify all sections are properly structured

---

## Template Versioning

Templates are versioned alongside the documentation system:

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-01 | Initial templates: api-docs, design-docs, user-manual |
| 1.1 | 2026-04-25 | Added template variants: adr, rfc, openapi |

---

## Extensibility Notes

The template system is designed for extension:

- **Domain-specific templates** can be added (e.g., `security-review.md`, `runbook.md`)
- **Project-specific templates** can override defaults by placing in project's `.claude/docs/templates/`
- **Template inheritance** is supported by referencing a base template and overriding sections
- **Template variants** (adr, rfc, openapi) are selected via `generation_config.template_variant` in suite manifests; the value must match a registered `type_id`
- **Quality enforcement** for variants is configured in `quality-gates.json` under `quality_profiles` keyed by `type_id`
