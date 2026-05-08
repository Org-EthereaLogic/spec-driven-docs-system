# RFC-0002: Unsupported-Claim Detection Strategy

**Author:** Anthony G. Johnson II
**Status:** Draft
**Created:** 2026-05-08
**Last Updated:** 2026-05-08
**Suite:** ai-powered-lead-gen-mvp
**Related:** [Quality Guardrails and Readiness Scoring Design](../design/guardrails-readiness.md), [Data Model](../design/data-model.md)

## Abstract

This RFC proposes a strategy for detecting unsupported claims in generated outreach beyond the MVP baseline. The MVP baseline (a non-blocking warning when a claim lacks a `source_ref` from the Prospect dossier or an entry in the Approved claims library) catches obvious failures but is blind to paraphrased evidence ("they raised a Series B" against a source that says "secured $50M in funding") and to plausible-but-unsourced claims. This RFC compares three candidate detectors - extended string match, embedding-similarity, and an LLM judge - and recommends a phased rollout that ships the string-match baseline in Phase 2 and adds the LLM judge as a blocking decision-maker in Phase 3.

## Motivation

The MVP's quality story depends on every factual claim in approved outreach being grounded in evidence (NFR-002). Schema-level enforcement catches claims with no `source_ref` at all - those are easy. The hard cases are claims that paraphrase real evidence (which the baseline rejects as unsupported) and claims that read as factual but have no underlying evidence at all (which the baseline only catches if the writer also forgot the `source_ref` plumbing).

Reviewers can catch paraphrased evidence and unsupported plausible-sounding claims, but each one is a friction point. With multiple prospects per Prospect package and multiple claims per message, reviewer attention becomes the bottleneck the MVP exists to support, not stress. A deeper detector reduces reviewer load on the cases that are most prone to fatigue.

The trigger for this RFC now: the MVP demo will surface whether the baseline is enough, but the team needs the next step ready to implement if reviewers report fatigue. Designing under demo pressure produces worse results than designing in advance.

## Detailed Design

### Overview

The detector runs as a Guardrail at the end of First-Touch Email Generation and against every Cadence step Message that contains a `claims` array. It returns one Guardrail result per Message with per-claim status:

- `supported` - claim is grounded in evidence (Prospect dossier `source_ref` or Approved claims library entry).
- `unsupported` - no evidence found; reviewer must revise, remove, or override.
- `needs_review` - evidence exists but the match is partial or paraphrased; reviewer must confirm or reject.

### Candidate 1: Extended string match (MVP baseline, ships Phase 2)

Case- and stem-normalized substring match against the Prospect dossier's `confirmed_facts` and the Approved claims library entries scoped to the campaign. Matches that pass set status to `supported`; misses set status to `unsupported`. Findings include the matched evidence ID for transparency.

Cost: low. Determinism: high. Recall on paraphrase: poor.

### Candidate 2: Embedding similarity (deferred unless Candidate 3 is insufficient)

Sentence-level embeddings of each claim and each piece of evidence; cosine similarity scored against a tunable threshold (initial baseline: 0.78). Above-threshold matches are `needs_review`; reviewer confirms or rejects.

Cost: medium - requires an embedding model and a per-evidence embedding cache. Determinism: deterministic given fixed weights, but threshold tuning is empirical. Recall on paraphrase: good.

### Candidate 3: LLM judge (ships Phase 3, blocking decision-maker)

A structured-output LLM call asks "is this claim supported by the provided evidence?" The prompt receives the claim plus the candidate evidence (top-K from extended string match plus the Approved claims library); the model returns a per-claim verdict (`supported`, `unsupported`, `needs_review`) with a one-sentence rationale.

Cost: high per call, scales with claim count. Determinism: lower than rule-based but acceptable when the model output is structured and validated. Recall and precision on paraphrase: highest of the three.

### Recommended phased rollout

1. **Phase 2 (MVP demo):** Candidate 1 only. Status is non-blocking; flagged claims surface in the Review step for reviewer judgment. This matches the baseline already documented in `guardrails-readiness.md`.
2. **Phase 3 (post-demo refinement):** Add Candidate 3 as the blocking decision-maker for claims Candidate 1 marks as unsupported. Candidate 1 stays as a cheap pre-filter to keep cost bounded.
3. **Optional later:** Candidate 2 is added only if Phase 3 evidence shows that the LLM judge alone misses paraphrase cases that embedding similarity catches.

### Approved claims library shape

The library is a campaign-scoped collection. Each entry:

| Field | Type | Description |
|-------|------|-------------|
| `claim_id` | string | Primary key. |
| `campaign_id` | string | Scoping campaign. |
| `claim_text` | string | The canonical claim text. |
| `evidence_ref` | string | `source_ref` for the claim's evidence. |
| `valid_for_offer` | array | Offer codes for which this claim is approved. |
| `valid_for_icp` | array | ICP codes for which this claim is approved. |
| `last_reviewed` | string | ISO-8601 timestamp of last reviewer / approver group review. |

Curation is a joint operator + reviewer responsibility; the library is bootstrapped from claims confirmed during the first MVP demo.

### Failure modes

| Failure | Behavior |
|---------|----------|
| LLM judge unavailable | Fall back to Candidate 1; non-blocking warning surfaces in Review. |
| Approved claims library empty | All non-dossier claims are evaluated against the dossier alone; missing matches surface as `unsupported` or `needs_review`. |
| Claim text has no recognizable subject | Detector marks `needs_review` with finding `unparseable_claim`; reviewer judges. |

## Drawbacks

- **LLM judge cost and latency.** Each Message can contain multiple claims; cost scales linearly. Mitigation: pre-filter via Candidate 1 so the judge only evaluates ambiguous cases.
- **Embedding model footprint** if Candidate 2 is adopted later. Adds operational surface area (model versioning, cache invalidation).
- **Library curation overhead.** Falls on operators and reviewers; if curation lags, the detector loses precision over time.
- **Confidence ≠ correctness.** Marking a claim `supported` because the LLM judge agreed does not guarantee factual correctness. Communicating this to reviewers without eroding their trust in the system is non-trivial.

## Alternatives

| Alternative | Why not chosen |
|-------------|----------------|
| Do nothing - rely on reviewers | Defers quality entirely to reviewers; the MVP exists to support them, not to dump fatigue on them. |
| Per-claim citation links in the message UI alone | Useful supplement, but does not detect missing or unsupported claims; only displays what is already there. |
| Candidate 2 alone (embeddings) | Tuning is harder than the LLM judge for similar effort; threshold drift across topics is well-documented. |
| Ship Candidate 3 in Phase 2 (block immediately) | Risks delaying the demo on unsupported-claim noise; better to learn what reviewers flag in Candidate 1 first. |

## Unresolved Questions

1. Does the MVP demo require Candidate 3 by Phase 2 instead of Phase 3? Depends on `guardrails-readiness.md` Q3 (reviewer / approver group's confidence in the baseline).
2. What is the per-claim cost ceiling for the LLM judge? The answer determines whether the judge can run on every claim or only on Candidate 1's `unsupported` flags.
3. Is `needs_review` sufficient for borderline cases, or should a fourth `supported_with_paraphrase` status exist to distinguish "evidence is present but worded differently" from "evidence is partial"?
4. How is the Approved claims library bootstrapped? Pre-demo seeding from sales / partnerships leader? Post-demo curation only? Hybrid?
