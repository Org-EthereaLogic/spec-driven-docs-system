# Operator User Manual

**Status:** Draft
**Author:** Anthony G. Johnson II
**Audience:** Business development operator (founder, SDR, consultant, recruiter, growth operator)
**Created:** 2026-05-08
**Last Updated:** 2026-05-08
**Suite:** ai-powered-lead-gen-mvp
**Related:** [Reviewer and Approver Guide](./reviewer-guide.md), [MVP Demo Quickstart](./demo-quickstart.md), [System Architecture](../design/architecture.md), [ADR-0001 Human-in-the-Loop](../adrs/0001-human-in-the-loop.md), [ADR-0006 Prospect Dossier](../adrs/0006-dossier-source-notes.md)

## Introduction

### What this guide covers

The AI-Powered Lead Generation MVP is a Human-in-the-loop workflow that turns a campaign brief into approval-ready outreach. It does the structured, repetitive parts - account research, dossier writing, message drafting, Guardrail checks - while you decide what's worth approving. Every artifact passes through the Reviewer / approver group before it can be marked ready for use.

This guide is for the Business development operator: the person running campaigns, evaluating prospects, and shepherding Prospect packages through the workflow. If you are a reviewer, see the [Reviewer and Approver Guide](./reviewer-guide.md). If you are running a demo, see the [MVP Demo Quickstart](./demo-quickstart.md).

### What success looks like

The canonical MVP demo scope is:

- **Minimum:** 1 target company and 1 prospect, processed end-to-end and approved.
- **Preferred:** 1 target company and 2 prospects from that same company, so reviewers can evaluate coordinated buying-committee messaging.

The principle behind this scope: quality over volume. The MVP is designed to prove the workflow on a small, well-researched sample before scaling. Steady-state capacity (up to 10 companies per week and up to 5 prospects per company) is the eventual ceiling, not the demo's target.

### Who this guide is not for

If you need to evaluate a Prospect package (approve, reject, or request revision), the Reviewer and Approver Guide is yours. If you are building or extending the workflow itself, the [System Architecture](../design/architecture.md), [Data Model](../design/data-model.md), and [Quality Guardrails](../design/guardrails-readiness.md) design documents are the reference.

## Getting Started

### Pre-flight checklist

Before starting a campaign run, confirm:

- [ ] **ICP** is selected (one of the FR-002 categories: engineering leaders at Series A, founders at Series A, engineering leaders at enterprise, HR / people leaders for recruiting workflows).
- [ ] **Offer** is chosen (GovForge, Drift Sentinel, Booply, lead generation platform, agentic AI engineering services, or recruiting lead generation system).
- [ ] **Conversion goal** is stated in plain language (what action do you want the prospect to take).
- [ ] **Approval owner** is identified - the Reviewer / approver group member accountable for final sign-off on this campaign.
- [ ] **Source data access** is configured. If a data provider is configured (per OQ-001 outcome), Semantic account discovery is available; otherwise the workflow uses manual target-company entry.

You are ready to begin when every checklist item is checked, the workflow runner is reachable, and the assigned approval owner has confirmed they will be available to review during this run.

### Where the workflow lives

The MVP's deliverable format (notebook, CLI, web UI, or service) is an open Phase 0 decision (OQ-002). This guide describes operator actions in workflow terms rather than UI terms; the specific clicks change with the format, but the actions and their order do not.

## Core Concepts

These terms appear across the workflow and across this manual. Use them consistently when discussing a Prospect package with reviewers.

| Term | What it means |
|------|---------------|
| **Campaign** | The configured initiative: ICP, offer, buyer role, conversion goal, approval owner. Every artifact in a run is bound to a campaign. |
| **Target company** | An organization selected for research and outreach. Synonym: target account. |
| **Prospect** | A specific person at a target company. Distinct from a buyer role (the role they play in the buying process). |
| **Prospect dossier** | The canonical structured research record for a prospect. Includes confirmed facts (with source refs), assumptions, company context, and personalization angles. |
| **Personalization hook** | A professional, publicly appropriate detail used to make outreach relevant. Each hook is classified: professional, company-relevant, role-relevant, or excluded. |
| **First-touch email** | The opening message in a cadence. |
| **Multi-channel cadence** | The planned sequence of outreach touches. MVP-required channels are email and manual follow-up task. LinkedIn, phone, and voicemail are MVP-optional. |
| **Guardrail** | A validation check that prevents or flags low-quality, unsafe, inaccurate, or unsupported output. May be blocking or non-blocking. |
| **Readiness score** | A 0-100 score indicating whether a Prospect package is ready for manual outreach. MVP-ready threshold is 80. |
| **Review** | The Human-in-the-loop approval gate. Per ADR-0001, no outreach exits the workflow without explicit reviewer action. |
| **Prospect package** | The complete reviewable bundle for one prospect: dossier, hooks, messages, cadence, Guardrail results, Review. |

**How these fit together:** A Campaign owns one or more Target companies; each company yields one or more Prospects; each Prospect has exactly one Prospect package, which bundles the Prospect dossier, the Personalization hooks, the First-touch email, the Multi-channel cadence, the Guardrail results, the Readiness score, and the Review. The Prospect package is the unit of approval — reviewers act on packages, not on individual artifacts.

### The two rules that change everything

1. **Score is necessary but not sufficient.** A Readiness score of 80 or higher does not approve a Prospect package. Per [ADR-0001](../adrs/0001-human-in-the-loop.md), explicit reviewer action is required regardless of score.
2. **Every fact has a source.** Per [ADR-0006](../adrs/0006-dossier-source-notes.md), every confirmed fact in a Prospect dossier carries a `source_ref`. Inferences live in the assumptions list, never in confirmed facts.

## How-To Guides

### 4.1 Set up a campaign

**Steps:**

1. Open the campaign creation flow and supply the required fields per FR-001:
    - Campaign name
    - Description
    - ICP category (FR-002)
    - Buyer role (the role you're trying to reach)
    - Buyer-role-to-ICP rationale (one sentence on why this role fits this ICP)
    - Offer and offer details (FR-003)
    - Conversion goal
    - Approval owner
2. Save the Campaign record. The system validates that all required fields are present and blocks downstream steps if any are missing.

**Verify before moving on:**

- The selected offer aligns with the ICP (e.g., Booply for HR / people leaders).
- The approval owner is reachable; they are about to receive Prospect packages.

**Flag if:**

- The campaign mixes unrelated offers without an explicit multi-offer setup.
- The conversion goal is vague ("reach out") rather than concrete ("schedule a 30-minute discovery call").

**Outcome:** A persisted Campaign record bound to the run; downstream steps unlock.

### 4.2 Select a target company

**Steps (manual path):**

1. Enter the target company directly. Required: name and reason for fit.
2. Add the website or profile URL, industry, and size or stage band when available.
3. Approve the Company record to unlock prospect identification.

**Steps (Semantic account discovery path):**

1. Describe the target account profile in natural language.
2. Review the structured criteria the system extracts; edit if it misread the description.
3. Inspect the banded candidate list returned by the data provider.
4. Approve a high-confidence candidate (>=80), open a needs-review candidate (60-79) for closer inspection, or refine the description if no candidate reaches 60.

**What the system does:** Creates a Company record, attaches it to the campaign, marks `approval_status: pending` until you approve or reject.

**Verify before moving on:**

- The reason for fit reflects the campaign's ICP, not generic industry signals.
- The website or profile URL is correct - this is the seed for prospect identification later.

**Flag if:**

- Semantic account discovery returns no candidate above 60. Refine your criteria; do not lower the bar.
- A high-confidence candidate has a missing `source_ref` for the firmographic claims.

**Outcome:** An approved Company record on the campaign, ready for prospect identification.

### 4.3 Identify prospects

**Steps:**

1. From the approved Company record, ask the system to identify prospects.
2. Wait for the candidate list (per FR-006, the system attempts up to 5 prospects).
3. Review each candidate's name, title, profile URL, suspected buyer role, and reason for relevance.
4. Approve the prospect(s) you want to advance. For the MVP demo, approve 1 (minimum) or 2 from the same company (preferred).

**What the system does:** Returns prospect candidates ranked by alignment to the campaign ICP. Roles aligned to the buyer role are prioritized.

**Verify before moving on:**

- Each candidate's title actually exists at the target company in their profile.
- The reason for relevance is concrete - "leads platform engineering at the team building [project]" is better than "engineering leader."

**Flag if:**

- Fewer than the expected count of prospects are found. The workflow proceeds with what's available; check whether the data source is current.

**Outcome:** One or two approved Prospect records advancing to validation.

### 4.4 Validate prospect-company alignment

**Steps:**

1. Open the prospect's record and review the system-assigned `validation_status` (`confirmed`, `mismatch`, or `needs_review`).
2. Spot-check at least one entry in `validation_source_refs` to confirm the source genuinely supports the alignment.
3. For `needs_review` status, investigate the source materials before deciding.
4. Confirm, mark `mismatch`, or replace the prospect.

**What the system does:** Compares the prospect's current employer against the target company per FR-007 and records `validation_status` plus `validation_source_refs`.

**Verify before moving on:**

- The validation source is recent enough to be trustworthy for the role.
- A `needs_review` status is a yellow flag; do not advance without resolving it.

**Flag if:**

- The validation source is more than 6 months old for a fast-moving role.
- The prospect appears at multiple companies in the source materials and the system picked one without explanation.

**Outcome:** Each advancing prospect has `validation_status: confirmed` with a recent source ref.

### 4.5 Review the Prospect dossier

**Steps:**

1. Open the generated Prospect dossier and read each FR-008 section in order: professional background, current role and responsibilities, company context, business challenges, public interests or signals, personalization angles.
2. Spot-check at least three entries in `confirmed_facts` against their `source_ref` values.
3. Read the `assumptions` list and confirm each carries a stated basis - assumptions must not appear in `confirmed_facts`.
4. Verify that the FR-009 research checklist meets the threshold (currently 6 of 9 categories, with categories 1-2 - current company, current role - mandatory).
5. Approve the Prospect dossier or send it back for regeneration.

**What the system produces:** A dossier with explicit separation of confirmed facts from inferred assumptions. Every confirmed fact carries a `source_ref` per ADR-0006; missing source refs cause the dossier-generation step to fail rather than emit a soft warning.

**Verify before moving on:**

- Source refs you spot-checked actually contain the claimed facts.
- Personalization angles derive from `confirmed_facts`, not from the assumptions list.

**Flag if:**

- A confirmed fact's source ref does not actually contain the fact.
- An "assumption" reads as a fact in the personalization angles or message draft.
- Sensitive personal details have crept in (medical, family, political, religious). These should be excluded by default per NFR-003.

**Outcome:** An approved Prospect dossier that downstream personalization and message generation can rely on.

### 4.6 Approve personalization hooks

**Steps:**

1. Open the candidate hooks the system recommends.
2. Inspect each hook's classification (`professional`, `company_relevant`, `role_relevant`, or `excluded`).
3. Verify each hook ties to a `source_ref` for the underlying detail.
4. Approve hooks that are professional or company-relevant.
5. Revise role-relevant borderline cases or replace them with role context.
6. Confirm that excluded hooks are not attached to any message.

**What the system produces:** Hooks classified per NFR-003. Excluded hooks are blocked automatically.

**Verify before moving on:**

- If no safe hook exists, the system fell back to role or company context. This is acceptable - do not pressure the system to invent hooks.

**Flag if:**

- A hook references something the prospect did not actually do or say (drift from the source).
- A hook walks the line on appropriateness. When in doubt, replace it with role context.

**Outcome:** A short list of approved hooks, each tied to a `source_ref`, ready for first-touch generation.

### 4.7 Review the first-touch email

**Steps:**

1. Read the generated email start to finish - subject, opening, value proposition, and call to action.
2. Confirm the opening references the right prospect at the right company.
3. For every claim in the body, click through to its `source_ref` (in the message's `claims` field) and confirm the source supports the claim.
4. Scan for unresolved placeholder variables (`{first_name}`, `[company]`); none should remain.
5. Verify the tone matches the campaign's offer per FR-012 (frames a buyer problem, risk, or opportunity rather than generic sales copy).
6. For coordinated multi-buyer messaging (preferred 1+2 demo): per FR-013, confirm that messages share campaign theme and offer but differ per prospect's role, that no two messages are identical, and that company-level facts are consistent across both.
7. Approve the email or send it back for revision.

**What the system produces:** A first-touch email with subject and body per FR-011, including at least one approved personalization element when available.

**Flag if:**

- A claim cannot be traced to a `source_ref`. This is the unsupported-claim case the Guardrails should catch (see 4.9), but reviewers will catch survivors.
- The wrong-person/company Guardrail flagged a sentence and you are unsure how to resolve it; bring it to the reviewer with context.

**Outcome:** An approved first-touch email with every claim grounded in a source ref and zero unresolved variables.

### 4.8 Review the multi-channel cadence

**Steps:**

1. Walk through each cadence step in order. Each step has a channel, timing, purpose, and suggested copy or talking point.
2. Confirm MVP-optional channels (LinkedIn, phone, voicemail) are marked optional or removed if they are not part of the approved demo scope.
3. Confirm each step's purpose is concrete and distinct from the others (no two messages making the same point).
4. For phone or voicemail steps, verify the talking point or script does not reference assumptions as facts.
5. Approve the cadence or revise individual steps.

**What the system produces:** A cadence built around MVP-required channels (email, manual follow-up task) plus any approved MVP-optional channels.

**Flag if:**

- A no-response final follow-up step appears without your opt-in (FR-014 is MVP-optional).
- A step's timing does not give the prospect realistic time to respond between touches.

**Outcome:** An approved cadence ready to package for review.

### 4.9 Resolve Guardrail findings

**What you see:** Guardrail findings are presented in two groups - blocking (must resolve before approval) and non-blocking (require override or revision). Each finding identifies the location and the offending content.

**Blocking findings to expect:**

- **Schema validation** failure - rare; usually means the runner caught the LLM producing invalid JSON.
- **Missing source-ref** in a Prospect dossier confirmed fact or message claim.
- **Broken variable** - an unresolved `{first_name}` or `[company]` token.
- **Wrong person / wrong company** - the message names someone or somewhere that does not match the approved Prospect or Company record.
- **Excluded personalization** - a hook the system flagged as inappropriate.

**Non-blocking findings to expect:**

- **Unsupported claim** (MVP baseline) - a claim in the message that does not match a Prospect dossier `source_ref` or an Approved claims library entry. Reviewer will see this in the Review step; you can revise now or pass it through.
- **Wrong person / company** with `needs_review` status when the system cannot decide.

**Steps:**

1. Read the blocking findings list. For each blocking finding, fix the underlying content (regenerate the dossier, re-write the message, replace the hook) and re-run the affected step.
2. Re-check the Guardrail panel; the previously blocking finding should clear or be replaced by a fresh result.
3. Read the non-blocking findings list. For each, decide: revise the content now, or leave it for the reviewer to override with a recorded reason.
4. Confirm no blocking findings remain before submitting for Review.

**Do not:**

- Override a blocking finding by claiming reviewer authority you don't have. Blocking findings cannot be overridden by the operator.
- Try to bypass the wrong-person Guardrail by editing the prospect record to match the message - this is the wrong direction.

**Outcome:** Zero unresolved blocking Guardrails on the Prospect package; non-blocking findings either revised or carried forward for reviewer judgment.

### 4.10 Submit for Review

**Steps:**

1. Confirm the Prospect package shows a Readiness score and zero unresolved blocking Guardrails.
2. Submit the package to the Reviewer / approver group via the Review step.
3. The system locks the package against further operator edits and notifies the assigned approval owner.

**What you do not do:** You do not approve your own work. Per ADR-0001, approval requires a reviewer with the explicit authority and identity recorded.

**Outcome:** The Prospect package's `package_status` becomes `ready` (eligible for review). It will move to `approved`, `rejected`, or back to `revision_requested` based on the reviewer's action.

## Troubleshooting

| Issue | What to try first |
|-------|-------------------|
| Semantic account discovery returns no candidate above 60. | Refine the natural-language description with more concrete signals (industry, size band, growth signal). Do not lower the threshold. |
| Prospect-company validation fails. | Re-check the source. If the prospect genuinely moved, replace them. If the source is stale, find a recent confirmation; do not override on a hunch. |
| Research checklist is below threshold (currently 6 of 9, categories 1-2 mandatory). | Identify which categories are missing. For categories you have direct knowledge of, supply the facts as `user_provided` so the dossier can carry them with that explicit marker. |
| Guardrail blocks approval and you can't tell why. | Read the finding's location and offending content. If it's a wrong-person flag, compare the message sentence against the Prospect record. If it's a missing-source-ref flag on a claim, find the evidence or remove the claim. |
| Readiness score is below 80 and you don't know which dimension is weak. | Look at the score breakdown. The scorer surfaces missing or weak areas. Address the weakest dimension first; do not bulk-edit. |
| Coordinated multi-buyer messages look too similar. | Re-generate the lower-coverage prospect's message with stronger role-specific framing. Check that the personalization hooks differ. |
| Reviewer rejected the Prospect package. | Read their feedback in the Review record. Address each item; do not assume one reason explains the rejection. Re-submit when ready. |

## Reference

### Glossary (operator subset)

- **Approved claim** - a factual statement that has passed source-note validation. Available for reuse across messages in the campaign.
- **Confirmed fact** - a dossier statement with a `source_ref`. Distinct from an assumption.
- **Personalization hook** - a professional, publicly appropriate detail tied to a `source_ref`.
- **Prospect dossier** - the canonical structured research record per prospect. Not "research dossier" or "structured dossier."
- **Readiness score** - 0-100 score; >=80 is the MVP-ready threshold. Score is necessary but not sufficient for approval.
- **Source ref** - a URL, document or transcript identifier, Approved claim library entry, or `user_provided` marker that grounds a factual claim.

### MVP-required vs MVP-optional channels

| Channel | Status |
|---------|--------|
| Email | MVP-required |
| Manual follow-up task | MVP-required |
| LinkedIn connection request | MVP-optional |
| Phone call | MVP-optional |
| Voicemail | MVP-optional |
| No-response final follow-up | MVP-optional (operator opt-in) |

### Cross-references

- [Reviewer and Approver Guide](./reviewer-guide.md) - what happens after you submit.
- [MVP Demo Quickstart](./demo-quickstart.md) - canonical demo run for stakeholder walkthroughs.
- [System Architecture](../design/architecture.md) - the workflow's structure and component boundaries.
- [Data Model](../design/data-model.md) - the data objects you see (Campaign, Company, Prospect, etc.).
- [Quality Guardrails and Readiness Scoring Design](../design/guardrails-readiness.md) - why each Guardrail exists and how it scores.
- [ADR-0001 Human-in-the-Loop](../adrs/0001-human-in-the-loop.md) - the approval rule.
- [ADR-0006 Prospect Dossier and Source-Noted Facts](../adrs/0006-dossier-source-notes.md) - the source-ref rule.
