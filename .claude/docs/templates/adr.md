# ADR Template - Architecture Decision Record

## Purpose

A short document that captures a single architectural decision: the context that motivated it, the choice that was made, and the consequences that follow. ADRs are write-once historical records, not living documents - once accepted, they are amended through superseding rather than edits.

## Target Audience

- Engineering team members making future related decisions
- Engineers onboarding to the project
- Technical reviewers and architects auditing the design history

## Filename Convention

`ADR-NNN-short-kebab-title.md`

Where `NNN` is a zero-padded sequential number (e.g., `ADR-007-use-postgres-for-events.md`). Numbers are never reused, even if an ADR is deprecated or superseded.

## Required Sections

1. Status
2. Context
3. Decision
4. Consequences
5. Alternatives Considered

## Status Field Values

- `Proposed` - Under discussion, not yet accepted
- `Accepted` - Approved and in effect
- `Deprecated` - No longer recommended but not actively replaced
- `Superseded by ADR-NNN` - Replaced by a newer decision

## Style Guidelines

- Length: 300-800 words. A decision that requires more than 800 words is probably two decisions; split it.
- Heading hierarchy: H1 for title, H2 for sections only. Avoid H3 unless absolutely necessary.
- No diagrams required. If a diagram clarifies the decision, use a single Mermaid block.
- Write in past tense for Context (what was happening) and present tense for Decision (what we do now).
- Be specific. "We will use Postgres" beats "We will use a relational database."

## Anti-Bloat Warning

Do NOT add:

- Implementation plans (those belong in design docs)
- Detailed code samples (link to the implementation instead)
- Long lists of people who agreed (one Deciders line is enough)
- Hypothetical future considerations not relevant to the current decision

---

## Template Body

```markdown
# ADR-NNN: [Decision Title in Imperative Voice]

**Status:** Proposed
**Date:** YYYY-MM-DD
**Deciders:** [Names or roles, comma-separated]

## Context

What is the issue or situation that motivates this decision? What forces are at play - technical, organizational, business? Describe the current state and why it needs to change.

Keep this to 2-4 paragraphs. The reader should understand the problem without needing to read other documents first.

## Decision

The response to these forces. State the decision in full, declarative sentences.

> We will [do X] using [Y approach] because [Z key reason].

Include enough specifics that an engineer reading this in 2 years can understand exactly what was chosen, not just the general direction.

## Consequences

### Positive

- [Concrete benefit 1]
- [Concrete benefit 2]

### Negative

- [Concrete trade-off 1]
- [Concrete trade-off 2]

### Neutral

- [Side effect with no clear valence]

## Alternatives Considered

| Alternative | Why not chosen |
|-------------|----------------|
| [Alt 1] | [Specific reason rooted in this context] |
| [Alt 2] | [Specific reason rooted in this context] |
```

---

## Examples of Good ADR Topics

- Database engine selection
- Authentication mechanism choice
- API versioning strategy
- Library or framework adoption
- Service decomposition boundaries
- Caching strategy

## Examples of Bad ADR Topics

- Implementation details ("how we built feature X")
- Style preferences ("naming conventions")
- Operational decisions ("when to deploy")
- Anything reversible without significant cost
