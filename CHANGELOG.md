# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Security

- Tests: hardened `tests/setup-isolated-test.sh` against destructive
  `rm -rf`. The script previously accepted an arbitrary test root and
  deleted it unchecked, so `./tests/setup-isolated-test.sh ~` (or `/`,
  or the repo root) could wipe important directories. It now resolves the
  requested root with `realpath` (python3 fallback) and refuses unsafe
  targets — empty, `/`, `$HOME`, the framework root, and anything not
  under `/tmp/` — before any destructive or setup operation. realpath
  resolution also defeats symlink-escape attempts (PR \#27)

### Fixed

- Hooks: de-duplicated pre-write blocking issues in `doc_pre_write.py`.
  `check_placeholder_content()` re-flagged placeholder terms (TODO, FIXME,
  TBD, XXX, HACK, WIP, lorem ipsum, example.com, `[your`/`<your`/`{your`)
  that `check_forbidden_patterns()` already reports from
  `consistency-rules.json`, so a single offending term produced duplicate
  blocking issues. The function now delegates only to the contextual
  ellipsis check, and `validate_documentation_write()` de-dupes issues
  while preserving order. All previously hardcoded placeholders remain
  covered by `forbidden_patterns`, so no validation coverage is lost. The
  smoke TODO case now asserts exactly `1 issue(s)` (PR \#39)
- Hooks: the post-review promotion hook now recognizes the namespaced
  `/doc:doc-review` command form in addition to plain `/doc-review`. The
  `.claude/settings.json` PostToolUse matcher and the fallback
  command-path extraction in `doc_post_review.py` previously matched only
  the plain form, so namespaced invocations never fired the hook or had
  their document path recovered from the command — passing reviews
  produced no promotion suggestion. Smoke tests cover both forms (PR \#33)
- Hooks: tightened the post-review result parser in `doc_post_review.py`
  to prevent false-positive promotion suggestions. Grade parsing is now
  anchored so substrings like "downgrade B" no longer register as Grade
  B; `passed`/`ready_for_publish` are parsed as explicit booleans whose
  `false` values veto promotion; score-only readiness derives from a
  shared `PUBLISH_THRESHOLD` (80) when no grade is present; and the final
  suggestion is gated on both `passed` and `ready_for_publish`. The hook
  also shares `get_tool_input` from `hook_utils` instead of duplicating
  it. Smoke tests cover the downgrade-text, explicit `passed: false`, and
  JSON score-only cases (PR \#37)
- CI/release: replaced `gitleaks-action` binary-download workaround with
  the official `gitleaks/gitleaks-action` (SHA-pinned in the workflow;
  corresponds to `v2.3.9`) now that a paid license is configured via
  `GITLEAKS_LICENSE` repository secret
- CI: added `workflow_dispatch` trigger to `ci.yml` to allow manual runs from
  the GitHub Actions UI
- CI: removed unsupported `config-path` input from `gitleaks-action` — the
  action auto-discovers `.gitleaks.toml` from the repository root
- Docs: corrected stale counts in `CLAUDE.md`, `README.md`,
  `tests/isolated-test-plan.md`, and `app_docs/reports/IMPROVEMENT_OPPORTUNITIES.md`
  (8→11 slash commands, 3→6 document templates)
- Hooks: scoped the pre/post doc-write hooks to generated and app docs
  only. The matchers previously caught any markdown under a `/docs/`
  path, which incorrectly captured framework templates (`.claude/docs/`)
  and input specifications (`specs/docs/`) — editing those triggered
  placeholder/forbidden-pattern validation meant only for generated
  output. `hook_utils.py` now drops the broad `/docs/` entry and adds an
  explicit `EXCLUDED_DOC_PATHS` guard, and `.claude/settings.json` uses a
  negative lookahead so only `spec_driven_docs/` and `app_docs/` match
  (PR \#31)

### Changed

- Codacy: bumped `.codacy/codacy.yaml` to current CLI tooling — dropped the
  `java` runtime and `pmd`/`semgrep`, added `opengrep`, and bumped
  `lizard`/`pylint`/`trivy` versions (PR \#29)
- Repo hygiene: ignore `.codex/` and `.agents/` — auto-generated external
  agent-platform artifacts that carry machine-specific absolute paths and
  templated cross-project references, so they are not portable repo
  content (PR \#29)

### Dependencies

- Bump `markdownlint-cli` 0.48→0.49 to clear moderate `npm audit`
  findings in transitive deps — `js-yaml` (GHSA-h67p-54hq-rp68) and
  `markdown-it` (GHSA-6v5v-wf23-fmfq); a follow-on `npm audit fix`
  bumped `brace-expansion` (GHSA-jxxr-4gwj-5jf2). `npm audit
  --audit-level=moderate` now reports 0 vulnerabilities (PR \#35)
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
