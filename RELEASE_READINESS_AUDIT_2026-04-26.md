# Release readiness audit (April 26, 2026)

## Scope and method

This audit evaluates whether `spec-driven-docs-system` is ready for an official public release based on:

- Existing repository standards and guidance in `AGENTS.md`.
- Automated checks available in the repository.
- Release-operational expectations (security, versioning, distribution, and governance).

Commands executed during this audit:

```bash
npm test
npm run test:e2e
npm audit --audit-level=moderate
rg -n "TODO|placeholder|TBD|FIXME" --glob '!node_modules/**'
test -f CHANGELOG.md
test -f SECURITY.md
test -f .github/workflows/release.yml
test -f .github/dependabot.yml
```

## Audit result

Status: **Not yet ready for official release**.

The core framework quality checks pass, but release operations are incomplete. The project appears mature for pilot usage,
beta usage, or controlled adoption, but not fully prepared for a formal release process.

## What is release-ready today

### Quality and functional validation

- Smoke suite passes fully (`npm test`) including:
  - JSON validation.
  - Hook execution coverage.
  - Markdown linting.
- End-to-end workflow validation passes (`npm run test:e2e`) including:
  - Clean clone install.
  - Spec creation for `api`, `design`, and `manual`.
  - Draft generation.
  - Hook validation.
  - Promotion to `pending_approval`.

### CI baseline

- CI workflow exists at `.github/workflows/ci.yml`.
- CI runs smoke tests and isolated install checks on push/PR to `main`.
- Workflow uses least-privilege permissions (`contents: read`).

### Documentation baseline

- Public-facing docs exist: `README.md`, `CONTRIBUTING.md`, `FAQ.md`, User Guide, and governance docs.
- Command surface appears documented and present under `.claude/commands/doc/`.

## Gaps that should be closed before official release

### Blockers

1. **No formal release workflow automation**
   - Missing `.github/workflows/release.yml` (or equivalent tag/release pipeline).
   - No reproducible release artifact process.

2. **No public changelog**
   - Missing `CHANGELOG.md`.
   - No explicit historical release notes baseline.

3. **No security disclosure policy**
   - Missing `SECURITY.md`.
   - No documented vulnerability intake/response process.

### High priority

1. **Dependency vulnerability scanning is not operational in this environment**
   - `npm audit` failed due to registry endpoint access (`403 Forbidden`), so vulnerability status is unknown from this run.
   - Add CI-integrated dependency scanning (Dependabot and/or additional scanners) so release gating does not depend on
     local network conditions.

2. **No automated dependency update policy**
   - Missing `.github/dependabot.yml`.
   - Increases drift and delayed patching risk.

3. **Release gate definition is implicit, not explicit**
   - Quality gates exist for document lifecycle, but there is no dedicated release checklist file that defines
     go/no-go criteria for publishing this framework itself.

### Medium priority

1. **No pinned runtime compatibility matrix in release docs**
   - CI uses Node 20 and Python 3.11, but support policy by version range is not clearly published as a release contract.

2. **No signed release/tag guidance**
   - If this project is distributed broadly, signed tags/releases should be considered for trust and supply-chain hygiene.

## Recommended path to release

### Phase 1: Close blockers (required)

- Add `CHANGELOG.md` with an initial release section.
- Add `SECURITY.md` with contact path, SLA targets, and severity handling.
- Add `.github/workflows/release.yml` with tag-triggered release checks and publication steps.

### Phase 2: Strengthen security and maintenance (required)

- Add `.github/dependabot.yml` for npm and GitHub Actions updates.
- Add CI step(s) for vulnerability and secret scanning to enforce a release gate.
- Define a fallback process when vulnerability feeds are unreachable.

### Phase 3: Formalize release governance (recommended)

- Create `RELEASE_CHECKLIST.md` with mandatory pre-release checks:
  - `npm test` pass.
  - `npm run test:e2e` pass.
  - lint pass.
  - vulnerability scan pass.
  - docs updated.
  - changelog updated.
  - version bump reviewed.
- Document versioning policy (SemVer expectations and deprecation approach).

## Proposed go/no-go decision

- **Go for beta/limited rollout:** Yes.
- **Go for official public release:** No, until blocker items above are completed.
