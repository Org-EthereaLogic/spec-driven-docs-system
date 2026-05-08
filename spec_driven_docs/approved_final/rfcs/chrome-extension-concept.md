# RFC-0003: Chrome Extension Browser Workflow Concept

**Author:** Anthony G. Johnson II
**Status:** Draft
**Created:** 2026-05-08
**Last Updated:** 2026-05-08
**Suite:** ai-powered-lead-gen-mvp
**Related:** [System Architecture](../design/architecture.md), [Data Model](../design/data-model.md)

## Abstract

This RFC explores how an approved Prospect package could surface inside the operator's existing browser context (LinkedIn, company website, email), the surface area FR-019 calls "exploratory." Three options are compared: a full Chrome extension, a lightweight bookmarklet or local prototype, and "no extension" with reviewer-side export. The recommendation is to ship a non-blocking lightweight prototype (Option B) for the MVP demo, defer a production extension (Option A) to post-MVP, and treat plain-text export (Option C) as the always-available baseline. OQ-003 (whether a mock is required for the MVP demo) remains open and gates the recommendation.

## Motivation

Operators do not work in a dedicated tool. They live in LinkedIn profile pages, the data provider, the company website, and the email client. The MVP currently treats outreach generation as a structured pipeline and ends at "approved Prospect package." The unanswered question is how the operator transports that approved content from the workflow's Review step to the place they actually act on it.

The MVP can succeed without a browser surface - operators can copy-paste from the Review console - but stakeholders have asked how a richer hand-off would work, and the source planning context flagged a Chrome workflow as an aspirational direction. Without an explicit RFC, the team risks either over-investing in a production extension or building nothing and looking unprepared for the question.

The trigger now: Phase 0 must close OQ-003, and the answer drives Phase 2 scope.

## Detailed Design

### Overview

Three options, ordered from lowest to highest scope:

| Option | Scope | MVP demo fit |
|--------|-------|--------------|
| C - No extension | Plain-text or markdown export from the Review step; operator pastes manually. | Always available. Baseline. |
| B - Lightweight prototype / bookmarklet | A bookmarklet or local script reads the URL of the page the operator is on; the workflow looks up an approved Prospect package whose `prospect.profile_url` or `company.website` matches; if found, shows the approved messages in a side panel. Read-only. | Recommended for the demo as a non-blocking exploratory mock. |
| A - Full Chrome extension | Production-grade extension with packaged install, autocomplete, manifest permissions, and ongoing maintenance. | Out of scope for MVP. Phase 3 or post-MVP. |

### Option B: Lightweight prototype / bookmarklet

Behavior:

1. Operator clicks the bookmarklet on any page (typically a LinkedIn profile or a company site).
2. The prototype reads `window.location.href` and sends it to the workflow's lookup endpoint.
3. The workflow searches approved Prospect packages whose `prospect.profile_url` or `company.website` matches the URL (exact match first; domain-and-path heuristic second).
4. If a match is found, a side panel renders the approved Messages, the `personalization_used` array, and the `approval_status`. Read-only.
5. If no match is found, the prototype displays "No approved Prospect package matches this page."

Permissions: read the current URL only; no DOM injection beyond the side panel; no auto-fill, no auto-send, no clipboard write.

Implementation cost: bookmarklet form is hours-to-days; a local browser-extension-style prototype is days-to-weeks. Either form satisfies the demo concept.

### Option A: Full Chrome extension (deferred)

Capabilities the production extension would add over Option B:

- Persistent install via the Chrome Web Store with a managed permissions manifest.
- Detection of the prospect being viewed without bookmarklet click (passive matching against the current page URL).
- Inline diff against the page (e.g., warn if the loaded LinkedIn profile is for a different person than the approved Prospect package's `prospect`).
- Update notifications when an approved package's `approval_status` changes.

Cost: weeks-to-months including security review; ongoing maintenance for Chrome API churn. This is post-MVP work; mentioning it here records the direction without committing to it.

### Option C: No extension (baseline)

The Review step exposes an export action that produces plain text or markdown for the approved Messages, the cadence steps, and the `personalization_used` references. Operators paste manually. This option is always available regardless of which other option is shipped.

### Security considerations (any option)

- The prototype must never auto-fetch unapproved content. The lookup endpoint MUST verify that the returned package has `package_status: approved`.
- The prototype must never auto-send or auto-submit on the host page.
- The prototype must never inject content into the host page beyond the side panel; reads only.
- Permissions surface MUST be minimal: URL read, side-panel UI, fetch to the workflow's lookup endpoint.

### Recommendation

If OQ-003 resolves to "demo requires an extension story," ship Option B as a non-blocking exploratory mock for Phase 2. If OQ-003 resolves to "demo does not require it," ship only Option C and revisit Option B post-MVP. Option A is post-MVP regardless.

## Drawbacks

- Even Option B adds engineering scope mid-MVP. The Phase 2 critical path is end-to-end demo readiness; an extension prototype competes with that.
- Browser permissions surface requires care. A bookmarklet that misbehaves on LinkedIn can damage operator trust quickly.
- Operators may form expectations that production extension work will follow. Communicating "exploratory mock only" is not always heard.
- Demo-time bugs in the prototype distract from the workflow's quality story, the actual point of the demo.

## Alternatives

| Alternative | Why not chosen |
|-------------|----------------|
| Do nothing (Option C only) | Acceptable if OQ-003 resolves that way. Rejected as the recommendation only because stakeholders have asked the question. |
| Build the full extension first (Option A) | Production scope is post-MVP; would crowd Phase 2's critical path and risk demo readiness. |
| Mobile-app surface | Operators work in browsers, not mobile, for outreach prep. A mobile surface solves a different problem. |
| Native macOS / Windows app for the side panel | Higher install friction than a bookmarklet; same security review overhead as Option A. |

## Unresolved Questions

1. OQ-003 - is a Chrome extension mock required for the MVP demo, or is plain-text export from the Review step sufficient? The recommendation depends on the answer.
2. Should the prototype be permissioned (browser extension form) or permission-less (bookmarklet form) for the demo? Bookmarklet has lower friction but fewer capabilities.
3. Should the prototype include LinkedIn-specific behavior (e.g., highlight the prospect's name on the profile page) or stay channel-agnostic? LinkedIn-specific increases value but also increases scope.
4. Does the side panel need to live inside Chrome at all? A separate floating window invoked from a system shortcut may achieve the same demo effect with less browser-API risk.
