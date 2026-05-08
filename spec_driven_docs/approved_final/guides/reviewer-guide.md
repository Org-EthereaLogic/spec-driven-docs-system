# Reviewer and Approver Guide

**Status:** Draft
**Author:** Anthony G. Johnson II
**Audience:** Reviewer / approver group
**Created:** 2026-05-08
**Last Updated:** 2026-05-08
**Suite:** ai-powered-lead-gen-mvp
**Related:** [Operator User Manual](./operator-manual.md), [Quality Guardrails and Readiness Scoring Design](../design/guardrails-readiness.md), [ADR-0001 Human-in-the-Loop](../adrs/0001-human-in-the-loop.md), [ADR-0006 Prospect Dossier](../adrs/0006-dossier-source-notes.md)

## Introduction

### Why this role exists

Per [ADR-0001](../adrs/0001-human-in-the-loop.md), no outreach exits the AI-Powered Lead Generation MVP without explicit reviewer approval. You are the last line of defense against the failure modes the workflow is designed to prevent: wrong-person and wrong-company references, unsupported claims, sensitive personalization, and Prospect dossiers that look authoritative but lack evidence.

A Readiness score of 80 or higher is necessary but not sufficient. The score is a heuristic; you are the judgment. This guide is the playbook for that judgment.

### Who this guide is not for

If you run campaigns and produce Prospect packages, see the [Operator User Manual](./operator-manual.md). If you build or extend the workflow, see the [System Architecture](../design/architecture.md), [Data Model](../design/data-model.md), and [Quality Guardrails](../design/guardrails-readiness.md) design documents.

## Getting Started

### What arrives in your queue

When an operator submits a Prospect package, you receive:

- **Package summary** - campaign, target company, prospect, Readiness score, and Guardrail status overview.
- **Prospect dossier** - confirmed facts with source refs, assumptions with their basis, company context, business challenges, personalization angles.
- **Personalization hooks** - each classified as `professional`, `company_relevant`, `role_relevant`, or `excluded`.
- **First-touch email** - subject, body, claims with source refs.
- **Multi-channel cadence** - the planned sequence of touches.
- **Guardrail findings** - grouped by blocking and non-blocking.
- **Readiness score** - 0-100 with a breakdown across dimensions.

Nothing is approved until you take explicit action. The Prospect package's `package_status` remains `ready` (or `not_ready` if a blocking Guardrail is open) until your action records `approved`, `rejected`, or `revision_requested`.

## Core Concepts for Reviewers

### Readiness score interpretation

| Band | What it means for your decision |
|------|---------------------------------|
| `<60` low | The Prospect package is not ready. Operator should address weak areas before re-submitting. |
| `60-79` needs review | Substantive issues remain. Read carefully; common pattern is one weak dimension dragging an otherwise strong package. |
| `>=80` high | Eligible for approval. Spot-check before approving; the score is a heuristic, not a verdict. |

### Blocking vs non-blocking Guardrails

Blocking Guardrails are listed first in your view. The Prospect package cannot be approved while any blocking Guardrail is unresolved. Common blocking findings:

- **Schema validation** failure (the runner caught invalid JSON).
- **Missing source-ref** on a Prospect dossier confirmed fact or message claim.
- **Broken variable** - an unresolved `{first_name}` or `[company]` token.
- **Wrong person / wrong company** confirmed mismatch.
- **Excluded personalization** - a hook the system flagged as inappropriate.

Non-blocking Guardrails surface as warnings:

- **Unsupported claim** (MVP baseline) - a claim that did not match a Prospect dossier `source_ref` or an Approved claim library entry.
- **Wrong person / company** with `needs_review` when the system cannot decide.

You can override a non-blocking finding with a recorded reason. You cannot override a blocking finding; the operator must fix the underlying content.

### Source refs

Per [ADR-0006](../adrs/0006-dossier-source-notes.md), every confirmed fact in a Prospect dossier carries a `source_ref` (URL, document or transcript identifier, Approved claim library entry, or `user_provided` marker). Inferences live in the assumptions list, never in confirmed facts. Spot-checking source refs is your single most effective quality lever.

### Confirmed facts versus assumptions

Confirmed facts are statements with evidence. Assumptions are inferences with stated bases. Messages should not present assumptions as evidence-backed claims. When a message says "you've been scaling the engineering team" - that's a fact only if the dossier shows it as a confirmed fact with a `source_ref`. If it's in `assumptions`, the message should soften it ("you may have been scaling") or remove it.

### The override audit trail

Every override writes to the Review record's `overrides` field. Each entry: `{ guardrail_result_id, reason }` plus your reviewer identity and timestamp. The override rate is itself a quality signal; if you find yourself overriding the same Guardrail repeatedly with the same reason, that's a Guardrail tuning problem, not a reviewer pattern.

## How-To Guides

### 4.1 Evaluate a Prospect dossier

**What to do:**

- Read the **confirmed facts** list. For at least three facts, click the source ref and confirm the source actually contains that fact.
- Read the **assumptions** list. Confirm each assumption's basis is reasonable; flag any that read as facts.
- Check the **personalization angles**. Each should derive from a confirmed fact or an Approved claim library entry, not from an assumption.
- Confirm the **research checklist** meets threshold. The default is 6 of 9 categories with categories 1-2 (current company, current role) mandatory, subject to OQ-005.

**Reject or request revision if:**

- A confirmed fact's source ref does not contain the fact.
- An assumption appears as a fact in the personalization angles or message body.
- The research checklist threshold is not met without a strong `user_provided` rationale.

**Result:** A clear judgment on whether the dossier's confirmed facts are evidence-grounded and the assumptions are honestly labeled - the foundation that downstream personalization and message claims rely on.

### 4.2 Evaluate Personalization hooks

**What to do:**

- Confirm no hooks are classified as `excluded` and somehow still attached to a message.
- For role-relevant hooks, judge professional appropriateness. The line is: would this make sense in a cold introduction at a conference?
- Confirm each hook ties to a `source_ref` for the underlying detail.

**Reject or request revision if:**

- A hook references something the prospect did not actually do or say (drift from source).
- A hook walks the line on appropriateness (medical, family, political, religious, etc.).

**Result:** Approved hooks are professional, source-grounded, and appropriate; excluded hooks are not attached to any message.

### 4.3 Evaluate the first-touch email and cadence

**What to do:**

- Read the email subject and body once for tone, once for accuracy.
- For each claim in the body, confirm the `source_ref` resolves to evidence that supports the claim. Paraphrased evidence is a yellow flag - check whether the paraphrase is faithful.
- Confirm the prospect and company references in every sentence. The Guardrails catch most mismatches; you catch the rest.
- Walk through the cadence. Each step's purpose should be distinct from the others; no two messages should make the same point.
- For coordinated multi-buyer Prospect packages (preferred 1+2 demo), compare the two messages side by side. They share campaign theme; they differ in role-specific framing. Company-level facts are consistent across both.

**Reject or request revision if:**

- A claim's source does not actually support it.
- A wrong-person reference slipped past the Guardrail.
- A non-blocking unsupported-claim finding has no plausible evidence; the operator did not address it.

**Result:** Every claim in the email and cadence is grounded; person and company references are correct; the cadence is distinct step by step and tone-appropriate to the campaign.

### 4.4 Resolve Guardrail findings

**For blocking findings:**

- You cannot override. Reject or request revision; the operator fixes the underlying content and re-runs the step.
- Write a clear feedback note for the operator. "Wrong-company reference in cadence step 3" is more actionable than "fix the cadence."

**For non-blocking findings:**

- Read the finding's location and offending content.
- Decide: override (with a recorded reason) or send back for revision.
- If you override, write the reason for future reviewers. "The Approved claims library does not yet contain this verbatim, but the underlying Q3 funding announcement was sourced for the dossier" is useful; "looks fine" is not.

**Result:** Every Guardrail finding is either resolved (operator fixed and re-ran) or recorded (reviewer override with reason). No blocking finding remains open.

### 4.5 Record the FR-028 quality rating

After approving or rejecting, record the FR-028 ratings:

- **Research quality** - 1-5.
- **Personalization quality** - 1-5.
- **Message usefulness** - 1-5.

Low ratings (1 or 2) require a reason. Strong outputs (4 or 5 across the board) can be saved as reference examples for later calibration. The MVP target is an average of 4.0 or higher across reviewed demo outputs.

**Result:** A persisted FR-028 rating per dimension on the Review record, contributing to the suite's calibration data and feeding the MVP success metric.

### 4.6 Approve, reject, or request revision

**Approve:** Records `status: approved` on the Review record with your identity and timestamp. The Prospect package's `package_status` becomes `approved`. The operator is notified and can export per FR-027.

**Reject:** Records `status: rejected` with feedback. The Prospect package returns to the operator. Use rejection when the package is fundamentally wrong (wrong prospect, wrong company, ICP mismatch); use revision request for fixable issues.

**Request revision:** Records `status: revision_requested` with specific feedback. Lighter than rejection; signals that the package is recoverable.

Per ADR-0001, your identity and timestamp are recorded on every action. Overrides are also recorded. There is no anonymous review.

**Result:** The Review record's `status` field reflects your decision; the Prospect package's `package_status` updates accordingly; the audit trail captures who decided what and why.

## Decision Reference

| Situation | Required action |
|-----------|-----------------|
| Blocking Guardrail unresolved | Cannot approve. Reject or request revision; operator fixes and re-runs. |
| Score `>=80`, no blocking findings, source-ref spot-check passes | Approve and record reviewer identity. |
| Score `>=80` but a confirmed fact lacks plausible source | Reject or request revision. This is the unsupported-claim case ADR-0001 anticipates. |
| Score `60-79`, weak research dimension only | Request revision; identify which checklist categories are missing. |
| Score `<60` | Reject; the package is not ready for review-quality attention. Operator addresses weak areas first. |
| Non-blocking unsupported-claim finding, evidence in dossier paraphrases the claim | Override with a clear reason. |
| Non-blocking unsupported-claim finding, no plausible evidence | Reject the claim; either remove from message or supply evidence. |
| Wrong-person Guardrail flagged with `needs_review` | Investigate. If the message clearly refers to the wrong person, reject. If the reference is genuinely ambiguous, override only with a written rationale. |
| Coordinated multi-buyer messages are nearly identical | Request revision; messages must differ per buyer role per FR-013. |

## Common Pitfalls

### Rubber-stamping high scores

A Readiness score of 90 looks like a green light. It is not. The most common reviewer error is to skim the dossier, see the score, and approve. This is exactly the failure mode ADR-0001 was written to prevent.

**How to spot it in yourself:** If you approve a package in under two minutes, you probably skipped the source-ref spot-check. Re-open it.

### Over-overriding non-blocking findings

Non-blocking Guardrails exist because they catch real failures often enough to be worth seeing. If you are overriding the same Guardrail (e.g., unsupported-claim) on every package, the system is telling you something - either the Guardrail is mistuned (raise this in change management) or the operator is consistently producing claims without source refs (raise this with the operator).

**How to spot it in yourself:** Check the override-rate signal in your Review records over the last week. If it's climbing, investigate.

### Skipping source-ref spot-checks

The dossier can carry sources that look right at a glance but don't actually contain the claimed facts. Skipping the spot-check renders the entire `source_ref` rule (ADR-0006) ceremonial.

**How to spot it in yourself:** Pick three confirmed facts from each dossier you review. Click their source refs. If you didn't do this in the last review, you're skipping.

### Not writing actionable feedback

"Fix this" is not feedback. "Wrong-company reference in cadence step 3, second sentence: the message says 'Acme' but the prospect works at Beta Inc per the validated Prospect record" is feedback the operator can act on.

**How to spot it in yourself:** Read your last rejection feedback. If the operator would need to come back and ask "what specifically?" - rewrite it.

## Reference

### Glossary (reviewer subset)

- **Approved claim** - a factual statement that has passed source-note validation; available for reuse across messages in the campaign.
- **Approved claim library** - the curated set of Approved claims for a campaign. Curation is operator + reviewer responsibility.
- **Blocking Guardrail** - a finding that prevents approval until the operator fixes the underlying content. Cannot be overridden by the reviewer.
- **Non-blocking Guardrail** - a finding that requires reviewer judgment: override with a recorded reason, or request revision.
- **Override** - reviewer action that records `{ guardrail_result_id, reason }` against a non-blocking finding. Audit-tracked.
- **Prospect package** - the complete reviewable bundle for one prospect; `package_id` is the integration point.
- **Readiness score** - 0-100; necessary but not sufficient for approval per ADR-0001.

### Cross-references

- [Operator User Manual](./operator-manual.md) - what the operator was working with before the package reached you.
- [Quality Guardrails and Readiness Scoring Design](../design/guardrails-readiness.md) - what each Guardrail checks and how the score is computed.
- [ADR-0001 Human-in-the-Loop](../adrs/0001-human-in-the-loop.md) - the approval rule and its rationale.
- [ADR-0006 Prospect Dossier and Source-Noted Facts](../adrs/0006-dossier-source-notes.md) - the source-ref rule and its rationale.
- [Data Model](../design/data-model.md) - the Review record's fields and the override audit trail shape.
