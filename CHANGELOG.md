# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Tests: added a "Codex Hook Parity" check to `tests/smoke.sh` that
  byte-compares each `.claude/hooks/*.py` against its `.codex/hooks/`
  counterpart (forward and orphan directions). The git-ignored `.codex`
  mirror sits outside version control and so silently fell behind the
  tracked `.claude` sources across several merges; only `.codex/hooks.json`
  carries machine-specific absolute paths, so the `.py` logic is portable
  and must stay byte-identical. The mirror is regenerated locally and is
  absent in CI and non-Codex checkouts, so its absence is a clean skip
  rather than a failure (PR \#45)

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

- Hooks: the post-write internal-link check in `doc_post_write.py` no longer
  reports links to planned-but-not-yet-generated suite siblings as broken
  links. During incremental suite generation a document can legitimately link
  to a sibling that is declared in a suite manifest but not yet written;
  `check_internal_links()` flagged every missing target as a `Broken link`
  consistency issue, producing false positives. The check now loads every
  manifest `output_path` via the new `hook_utils.load_suite_output_paths()`
  helper and routes missing-but-planned targets to non-blocking suggestions
  ("Planned sibling not yet generated"), while genuinely unknown missing
  targets remain broken-link issues so real mistakes are still caught. Smoke
  tests cover both the planned-sibling and genuine-broken cases (PR \#51)
- Hooks: the pre-write code-block language-hint check in `doc_pre_write.py`
  now flags tilde (`~~~`) fences, not just backtick (` ``` `) fences.
  `check_code_blocks()` previously split content into lines and only matched
  openers starting with ` ``` `, so a tilde-fenced block with no language tag
  was silently skipped. It now reuses `_fenced_code_spans()` — the same helper
  the ellipsis check relies on — and inspects each opening fence line, so both
  fence styles receive the identical "missing language hint" warning. Smoke
  tests cover the tilde-fence-without-language case (PR \#47)
- Hooks: the post-write internal-link check in `doc_post_write.py` no
  longer flags Markdown image embeds as broken document links.
  `check_internal_links()` matched `[...](...)`, which also captured image
  syntax `![alt](src)`, so an image whose asset is generated later (e.g.
  `![Architecture overview](assets/missing-diagram.png)`) was reported as a
  broken link. The link regex now uses a negative lookbehind `(?<!!)` to
  skip image embeds while ordinary links are still validated. Smoke tests
  cover the missing-image-asset case (PR \#43)
- Hooks: the post-write header-hierarchy check in `doc_post_write.py` now
  ignores Markdown headings inside fenced code blocks. `check_header_hierarchy()`
  scanned raw Markdown, so a fenced `bash` block containing a shebang
  (`#!/usr/bin/env bash`, read as h1) followed by a comment like
  `### Internal setup` (read as h3) produced a false-positive "Header
  hierarchy skipped from h1 to h3" suggestion. It now scans
  `_strip_code_regions(content)` — the same helper `check_terminology()`
  uses — which blanks code regions to equal-length whitespace, so
  real-header line numbers stay accurate and genuine prose-level skips are
  still flagged. Smoke tests cover the code-fenced-heading case (PR \#41)
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

- Docs: moved the FAQ and release checklist into `docs/`, added a project docs
  index, added a reports index under `app_docs/reports/`, and added
  `.github/CODEOWNERS` for maintainer review routing.
- Codacy: bumped `.codacy/codacy.yaml` to current CLI tooling — dropped the
  `java` runtime and `pmd`/`semgrep`, added `opengrep`, and bumped
  `lizard`/`pylint`/`trivy` versions (PR \#29)
- Repo hygiene: ignore `.codex/` and `.agents/` — auto-generated external
  agent-platform artifacts that carry machine-specific absolute paths and
  templated cross-project references, so they are not portable repo
  content (PR \#29)
- Hooks: centralized the hook word/score thresholds and removed dead code.
  `hook_utils.py` now defines `MIN_DOCUMENT_WORDS` (50), `MAX_PARAGRAPH_WORDS`
  (200), and `DEFAULT_PUBLISH_THRESHOLD` (80), plus `get_publish_threshold()`
  which reads `grades.B.min` from `quality-gates.json`. `doc_post_review.py`
  now derives its score-only publish/readiness threshold from that helper
  instead of a hardcoded `80`, so the configured Grade B minimum is honored.
  `doc_post_write.py` uses the shared paragraph threshold and drops the dead
  `seen_lines` set (per-pass line indices are already unique). `doc_pre_write.py`
  removes the unreachable non-fenced Protocol-ellipsis handler — valid code
  examples belong inside fenced blocks, which `_fenced_code_spans()` already
  allows — and hoists `content.lower()` out of the forbidden-pattern loop. A
  smoke regression asserts post-review honors a configured Grade B threshold
  (PR \#49)

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
