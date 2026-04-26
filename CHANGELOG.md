# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- CI/release: replaced `gitleaks-action` binary-download workaround with
  official action (`gitleaks/gitleaks-action@v2.3.9`, SHA-pinned) now that a
  paid license is configured via `GITLEAKS_LICENSE` repository secret
- CI: added `workflow_dispatch` trigger to `ci.yml` to allow manual runs from
  the GitHub Actions UI
- CI: removed unsupported `config-path` input from `gitleaks-action` — the
  action auto-discovers `.gitleaks.toml` from the repository root
- Docs: corrected stale counts in `CLAUDE.md`, `README.md`,
  `tests/isolated-test-plan.md`, and `IMPROVEMENT_OPPORTUNITIES.md`
  (8→11 slash commands, 3→6 document templates)

### Dependencies

- Bump `actions/checkout` 4→6, `actions/setup-node` 4→6,
  `actions/setup-python` 5→6 (Dependabot, PRs \#18–20)

## [1.0.0] - 2026-04-26

### Added

- Core slash command suite: `/doc-plan`, `/doc-write`, `/doc-review`, `/doc-sync`,
  `/doc-batch`, `/doc-status`, `/doc-improve`, `/doc-promote`, `/doc-flow`,
  `/doc-config`, `/doc-interactive`
- Four specialized AI agents: `doc-orchestrator` (Opus), `doc-writer` (Sonnet),
  `doc-reviewer` (Sonnet), `doc-librarian` (Haiku)
- Three document templates: `api-docs.md`, `design-docs.md`, `user-manual.md`;
  plus `adr.md`, `rfc.md`, `openapi.md`
- Four-stage quality gate system (spec_completeness → content_quality →
  consistency → final_approval) with A–F grading
- Per-doc-type quality profiles (`api`, `design`, `manual`, `quickstart`, `adr`,
  `rfc`) with configurable score thresholds
- Pre/post-write hook pipeline (`doc_pre_write.py`, `doc_post_write.py`,
  `doc_post_review.py`) with shared `hook_utils.py`
- End-to-end workflow validation script (`tests/e2e_clone_and_flow.sh`)
- Smoke test suite covering JSON validation, hook execution, and Markdown linting
- CI workflow (`.github/workflows/ci.yml`) with smoke tests and isolated install
  checks on push/PR to `main`
- Plugin extension skeleton (`.claude/plugins/_example/`)
- Public-facing docs: `README.md`, `CONTRIBUTING.md`, `FAQ.md`, User Guide,
  `AGENTS.md`, `CONSTITUTION.md`, `DIRECTIVES.md`
- Section aliases for the `manual` quality profile (e.g. "Quickstart" satisfies
  "Getting Started")
- `quickstart` quality profile with no mandatory section names

### Fixed

- Markdownlint-clean output enforced as a binding contract in the doc-writer agent
- Smoke lint failure message clarified; hook regression tests added

[Unreleased]: https://github.com/Org-EthereaLogic/spec-driven-docs-system/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Org-EthereaLogic/spec-driven-docs-system/releases/tag/v1.0.0
