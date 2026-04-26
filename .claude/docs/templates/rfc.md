# RFC Template - Request for Comments

## Purpose

A formal proposal for a substantial change, new capability, or major architectural shift. RFCs answer four questions in order: what is being proposed, why it matters, how it will work, and what could go wrong. Unlike ADRs (which capture a decision after it is made), RFCs invite discussion and may evolve before acceptance.

## Target Audience

- Technical stakeholders and reviewers
- Team leads and engineering managers
- Anyone affected by the proposed change

## Filename Convention

`RFC-NNNN-short-kebab-title.md`

Four-digit zero-padded number to leave room for many proposals.

## Required Sections

1. Abstract (mandatory standalone paragraph)
2. Motivation
3. Detailed Design
4. Drawbacks
5. Alternatives
6. Unresolved Questions (required even if empty - signals the proposal is in active discussion)

## Style Guidelines

- The Abstract must stand alone. A reader should understand the proposal from the Abstract without reading further.
- Detailed Design is the longest section. Cover the technical specifics: APIs, data structures, migration plan, rollout strategy.
- Drawbacks is mandatory and must be honest. A proposal with no drawbacks is incompletely analyzed.
- Unresolved Questions empty array signals "no open issues, ready for vote." Items in this list block acceptance.
- Use second-level headings (`##`) for the six required sections. Use third-level headings within Detailed Design as needed.

---

## Template Body

```markdown
# RFC-NNNN: [Proposal Title]

**Author(s):** [Name(s)]
**Status:** Draft | Under Review | Accepted | Rejected | Withdrawn
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD

## Abstract

A single self-contained paragraph (3-5 sentences) that explains what this RFC proposes and why. A reader who reads only this paragraph should know whether the proposal is relevant to them and roughly what it does.

## Motivation

Why are we doing this? What problem does it solve? What is broken or missing today?

Cover:

- The current state and its limitations
- Concrete examples of where the current state falls short
- Why now (what changed, what triggered this proposal)

## Detailed Design

This is the technical specification. Cover everything an implementer needs to know.

Suggested subsections (use as needed):

### Overview

A higher-level walkthrough of the design before diving into specifics.

### API Changes

New, modified, or deprecated APIs. Show signatures and example usage.

### Data Model

New or changed data structures, schemas, or storage formats.

### Migration

If this affects existing systems or data, how will the migration work? What is the rollback plan?

### Rollout Plan

Phased deployment, feature flags, gradual enablement.

## Drawbacks

Why might we NOT do this? Consider:

- Implementation cost
- Maintenance burden
- Performance impact
- Breaking changes
- User-facing complexity

Be honest. Drawbacks are not weaknesses - they are evidence that the proposal has been analyzed thoroughly.

## Alternatives

What other approaches were considered? For each:

- What was the alternative
- Why it was rejected
- What would change about this RFC if the alternative were chosen instead

Include the "do nothing" alternative explicitly.

## Unresolved Questions

Open questions that need to be answered before this RFC can be accepted. List them as a numbered list, or write `None` if there are no open questions.

1. [Open question 1]
2. [Open question 2]
```

---

## When to Use RFC vs ADR

| Use RFC when... | Use ADR when... |
|-----------------|-----------------|
| The decision is still open | The decision has been made |
| You want broad input | You are recording a choice |
| The change is substantial | The change is constrained |
| Implementation will take weeks+ | Implementation is straightforward |

## Anti-Bloat Warning

Do NOT add:

- Sections beyond the 6 required (use subsections within Detailed Design)
- Approval signatures or voting tables (track those externally)
- Speculative future work not directly relevant to this proposal
