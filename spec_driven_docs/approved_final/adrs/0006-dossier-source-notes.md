# ADR-0006: Establish Prospect Dossier as Canonical Term and Require Source-Noted Facts

**Status:** Accepted
**Date:** 2026-05-08
**Deciders:** Product / technical lead, reviewer / approver group

## Context

Source materials for the AI-Powered Lead Generation MVP referred to the structured research record per prospect by several names: "research dossier," "structured dossier," "research record." Used interchangeably across PRD sections, user stories, schemas, and UI mockups, the variation drifted between writers and across documents. The cost is paid by reviewers, who lose time reconciling synonyms instead of evaluating content, and by integrators, who cannot pattern-match a single field name across the workflow.

Separately, FR-008 and NFR-002 require that every factual claim in the record reference a source note, source ID, or explicit user-provided marker. The MVP's quality story depends on this: one of the failure modes the product exists to prevent is unsupported claims that read as confirmed facts. Reviewers approving outreach need to audit each claim against its evidence at a glance; without inline source references they cannot.

These two requirements - terminology consistency and source-noted facts - are coupled. The canonical term anchors everything that consumes it: schemas, Guardrails, reviewer training, UI labels, and the source-ref enforcement itself. If the term drifts, so does the field name carrying its source ref. Treating them as one decision keeps the anchor and the rule aligned.

## Decision

"Prospect dossier" is the canonical term for the structured research record per prospect. It is used in MVP documentation, code identifiers, schema field names, UI labels, reviewer materials, and any artifact the team produces. Other phrasings - "research dossier," "structured dossier," "research record" - are not used except when explicitly defining the canonical term inside a glossary context.

Every factual claim in a Prospect dossier carries a `source_ref`. The reference may be a URL, a document or transcript identifier, an entry in the Approved claim library, or the explicit literal `user_provided` for facts the operator entered manually. Inferences are flagged with a distinct field and are never presented as confirmed facts.

Schema validation enforces both halves of this decision. A Prospect dossier whose schema lacks the canonical field names is rejected at validation. A claim missing its `source_ref` (or the explicit `user_provided` marker, or a `confirmed_fact: false` flag for inferences) causes the dossier-generation step to fail rather than emit a soft warning. The failure surfaces in the workflow run log with the offending claim identified.

## Consequences

### Positive

- Terminology consistency across the entire suite, reducing cognitive load on reviewers and integrators.
- Reviewers can audit dossier claims by scanning source refs inline rather than reconstructing provenance.
- Reduces the unsupported-claim failure mode at the data-model layer, before it can reach Guardrails or human review.
- Improves stakeholder confidence in demo output by making evidence visible per claim.

### Negative

- Strict source-ref enforcement makes some dossiers thinner: facts the generator cannot ground are dropped or flagged rather than included. This is intended, but it changes the visible "completeness" of dossiers compared to a permissive baseline.
- Writers quoting source materials in generated docs must rename references when the source uses an alternate term.

### Neutral

- The forbidden-substitution rule lives in the suite manifest's `project_glossary` and is enforced by the doc-reviewer agent.
- Drives reviewer-guide content: reviewers are trained to look for `source_ref` and to challenge any claim presented as fact without one.
- Inference flagging is a first-class data-model concept, not a comment in prose.

## Alternatives Considered

| Alternative | Why not chosen |
|-------------|----------------|
| Allow synonyms ("research dossier," "structured dossier") in different doc types | Cross-doc terminology drift is a known anti-pattern. The cost is paid every time a reviewer or integrator reads the suite. |
| Require `source_ref` only for high-confidence claims | Reintroduces the unsupported-claim failure mode for everything else. The whole point of the rule is to prevent inferences from masquerading as facts. |
