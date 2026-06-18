# FAQ

## What problem does this system solve?

It helps teams produce consistent technical documentation by enforcing a spec-first process: plan requirements,
generate drafts, review against quality gates, and only then promote content.

## Do I need to use every slash command?

No. For a single document, the minimum effective flow is usually:

1. `/doc-plan`
2. `/doc-write`
3. `/doc-review`
4. `/doc-promote`

Use `/doc-sync`, `/doc-batch`, and `/doc-status` when working across suites or multiple files.

## Where should I put new files?

Use these paths so tooling can discover your work:

- Specs: `specs/docs/`
- First output: `spec_driven_docs/rough_draft/`
- Reviewed content: `spec_driven_docs/pending_approval/`
- Final content: `spec_driven_docs/approved_final/`

## How do I know a document is ready?

Run `/doc-review` and then `/doc-status`. A document is ready to promote when quality gates are clear and no blockers
are reported.

## What checks should I run before opening a pull request?

At minimum:

```bash
npm test
```

Optional but recommended:

```bash
npm run lint:md
```

## Can I edit generated markdown manually?

Yes. Manual edits are expected for clarity and domain accuracy. Re-run `/doc-review` after substantive changes so the
quality gates reflect your final content.

## Why does this repo emphasize specs so heavily?

Specs reduce ambiguity, improve consistency across contributors, and make agent output more predictable and easier to
review.

## Is this tied to one documentation type?

No. The framework supports API documentation, design documents, and user manuals with dedicated templates and review
criteria.
