# Pending Approval Documentation

This directory contains documentation that has **passed quality review** and is awaiting **stakeholder approval**.

## Purpose

Documents in pending_approval:

- Have passed `/doc-review` quality gates (Grade A or B)
- Are technically accurate and complete
- Follow project style and consistency standards
- **Await business/stakeholder sign-off** before publication

## Quality Level

**High Quality** - Technically reviewed and approved

These documents are suitable for stakeholder review but not yet approved for public release.

## Approval Process

### Who Approves?

Depending on document type:

- **API Documentation:** API product owner, engineering lead
- **Design Documents:** Architect, engineering manager, relevant stakeholders
- **User Manuals:** Product manager, UX lead, support team

### Approval Criteria

Stakeholders review for:

- **Business alignment:** Does it match product strategy?
- **Completeness:** Does it cover all necessary topics?
- **Audience fit:** Is the tone and depth appropriate?
- **Accuracy:** Are claims and examples correct?

### Approval Workflow

1. **Share document** from this directory with stakeholders
2. **Collect feedback** via comments, review tools, or meetings
3. **Iterate if needed** (move back to rough_draft, update spec, regenerate)
4. **Get explicit approval** (email, Slack, review tool sign-off)
5. **Move to approved_final** once approved

## Moving Documents

### To Approved Final (after approval)

```bash
git mv spec_driven_docs/pending_approval/[category]/[document].md \
       spec_driven_docs/approved_final/[category]/[document].md
git commit -m "docs: Publish [document] after stakeholder approval"
```

### Back to Rough Draft (if changes needed)

```bash
git mv spec_driven_docs/pending_approval/[category]/[document].md \
       spec_driven_docs/rough_draft/[category]/[document].md
git commit -m "docs: Move [document] back to rough draft for revision"
# Update spec, regenerate, re-review
```

## File Organization

```text
pending_approval/
├── api/                    # API documentation
├── design/                 # Design documents
└── guides/                 # User manuals
```

Maintain the same categorization as rough_draft and approved_final.
