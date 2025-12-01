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

---

## Template Selection Guide

| If documenting... | Use Template | Type ID |
|-------------------|--------------|---------|
| REST API endpoints | api-docs | `api` |
| GraphQL schema | api-docs | `api` |
| Authentication flows | api-docs | `api` |
| System architecture | design-docs | `design` |
| Feature design | design-docs | `design` |
| Technical RFC | design-docs | `design` |
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

---

## Extensibility Notes

The template system is designed for extension:

- **Domain-specific templates** can be added (e.g., `security-review.md`, `runbook.md`)
- **Project-specific templates** can override defaults by placing in project's `.claude/docs/templates/`
- **Template inheritance** is supported by referencing a base template and overriding sections
