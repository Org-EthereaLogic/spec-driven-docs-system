# ADR-0001: Use the spec-driven-docs-system plugin path, not fork-edits

**Status:** Accepted
**Date:** 2026-04-26
**Deciders:** SDLC Pro architecture lead

## Context

SDLC Pro integrates with spec-driven-docs-system v1.0.0 to author the documentation that precedes each autonomous build. Earlier design drafts proposed two fork-edits to upstream files: a complexity-classifier hook injected into the doc-orchestrator agent definition, and a post-promotion webhook injected near the git commit step in the doc-promote command definition. Both edits were precise single-section additions, but each created a permanent obligation to track the upstream release cadence and resolve merge conflicts on every release.

The v1.0.0 release surfaced an extension contract that earlier snapshots did not have: a plugin directory under `.claude/plugins/` with a JSON-schema-validated `plugin.json` manifest. Plugins are auto-discovered by filesystem scan, declare what they install (commands, agents, templates, or hooks), and can declare dependencies on other plugins. The contract is enforced by `plugin.schema.json`, so a malformed plugin fails at load time rather than at runtime.

The forces at play were: avoiding upstream-tracking burden, preserving the ability to upgrade spec-driven-docs-system without merge work, keeping the integration boundary auditable, and using the upstream-recommended extension path now that one existed.

## Decision

We will integrate SDLC Pro with spec-driven-docs-system v1.0.0 by registering two plugins under `.claude/plugins/`: `sdlc-intake`, which materializes a v1.0.0 suite manifest from a story payload and invokes `/doc-flow --auto-promote`, and `sdlc-promote`, which wraps `/doc-promote` and posts the approved-doc payload to the Spec-to-TaskSpec bridge. Both plugin manifests conform to `plugin.schema.json`.

We will not fork-edit any upstream agent definition, slash-command file, hook, template, or configuration file. If a future requirement cannot be satisfied through the plugin contract, the response is to upstream a contract extension as a pull request rather than to fork.

## Consequences

### Positive

- Survives upstream releases without merge conflicts; the integration boundary is two discrete plugin directories rather than diffs scattered across upstream files.
- Plugin manifests are JSON-schema-validated at load time, so contract drift surfaces immediately rather than at runtime.
- The integration is auditable as a small set of files under `.claude/plugins/sdlc-intake/` and `.claude/plugins/sdlc-promote/`, each with a manifest declaring its scope.

### Negative

- The plugin contract may not cover every desired extension surface. Some integrations may require upstream contract changes, which carry their own coordination cost.
- Two plugins must be maintained instead of two single-section fork-edits; the absolute volume of integration code is slightly larger.

### Neutral

- Plugin discovery is filesystem-driven; no install command is needed beyond placing the directories under `.claude/plugins/`.

## Alternatives considered

| Alternative | Why not chosen |
|-------------|----------------|
| Fork-edit the doc-orchestrator and doc-promote files directly | Creates a permanent upstream-tracking burden, merge conflicts on every release, and an integration that is invisible inside diffs. |
| Run a sidecar process that polls workflow stage transitions and reacts | Duplicates the plugin contract with worse latency and observability; adds a separate process to operate. |
| Skip the doc-system entirely and reimplement the doc-authoring loop inside SDLC Pro | Discards a working v1.0.0 release built for exactly this purpose; reinvents quality gates, hooks, and templates. |
