# Generated Technical Documentation

This directory contains technical documentation **generated** by the Spec-Driven Docs System.

## Document Workflow

Generated documents move through three stages:

```text
rough_draft/ → pending_approval/ → approved_final/
```

| Stage | Description | Quality Level | Audience |
|-------|-------------|---------------|----------|
| **rough_draft/** | Initial output from `/doc-write` | Unreviewed, may have issues | Doc authors only |
| **pending_approval/** | Passed `/doc-review` quality gates | High quality, awaiting stakeholder sign-off | Review team |
| **approved_final/** | Approved by stakeholders | Production-ready, publishable | Public/end-users |

## Directory Structure

```text
spec_driven_docs/
├── README.md               # This file
├── rough_draft/            # Initial generation output
│   ├── api/                # API documentation
│   ├── design/             # Design documents
│   └── guides/             # User manuals and guides
├── pending_approval/       # Same structure as rough_draft
└── approved_final/         # Same structure as rough_draft
```

## Workflow Instructions

### 1. Generate Document (rough_draft stage)

```bash
/doc-write specs/docs/your-spec.md
# Output: spec_driven_docs/rough_draft/[category]/[document].md
```

### 2. Review Document

```bash
/doc-review spec_driven_docs/rough_draft/[category]/[document].md --fix
# If grade is A or B, document is ready for approval workflow
```

### 3. Move to Pending Approval

After passing review:

```bash
git mv spec_driven_docs/rough_draft/[category]/[document].md \
       spec_driven_docs/pending_approval/[category]/[document].md
git commit -m "docs: Move [document] to pending approval"
```

### 4. Stakeholder Approval

- Share document from `pending_approval/` with stakeholders
- Collect feedback and iterate if needed
- Once approved, move to final stage

### 5. Move to Approved Final

After stakeholder approval:

```bash
git mv spec_driven_docs/pending_approval/[category]/[document].md \
       spec_driven_docs/approved_final/[category]/[document].md
git commit -m "docs: Publish [document] to approved final"
```

## Quality Gates

Documents must pass these quality gates before moving to pending_approval:

- **Spec Completeness:** All required sections present
- **Content Quality:** No placeholders, complete examples, accurate information
- **Consistency:** Terminology and style match project standards
- **Final Approval:** Grade A (90-100) or B (80-89)

## Important Notes

- **Do not** manually edit documents in `rough_draft/` - regenerate from specs
- **Do** iterate on specs, not generated documents
- **Track changes** in git for audit trail
- **Maintain structure** consistency across all three stages
