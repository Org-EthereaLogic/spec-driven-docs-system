# Release Checklist

Mandatory go/no-go criteria for every release of `spec-driven-docs-system`.
Copy this checklist into the release tracking issue or PR, check items off as
verified, and obtain a second-maintainer sign-off before tagging.

---

## Pre-release checklist

### Automated validation (CI must be green on `main`)

- [ ] `npm test` passes — JSON validation, hook execution, markdownlint
- [ ] `npm run test:e2e` passes — clean-clone install, spec creation, draft
  generation, hook validation, promotion to `pending_approval`
- [ ] `npm run lint:md` passes with zero issues
- [ ] Dependency vulnerability audit clean — `npm audit --audit-level=moderate`
  with no unresolved moderate-or-higher CVEs
- [ ] Secret scanning (gitleaks) passes with no detected secrets

### Documentation

- [ ] `CHANGELOG.md` — new release section added above `[Unreleased]`, entries
  accurate and complete
- [ ] Public-facing docs (`README.md`, `FAQ.md`, User Guide, command docs under
  `.claude/commands/doc/`) reflect any changed behavior
- [ ] New or changed commands have updated help text
- [ ] New agent definitions in `.claude/agents/` include `description`, `model`,
  and `tools` fields
- [ ] `SECURITY.md` supported versions table updated if support policy changed

### Code hygiene

- [ ] No `TODO`, `FIXME`, `TBD`, `placeholder`, or `NotImplementedError` in
  deliverable files (hooks, commands, templates, agent definitions)
- [ ] All hook scripts exit with correct codes and structured output per
  `hook_utils.py` conventions

### Version and mechanics

- [ ] `package.json` version bumped following the [Versioning Policy](#versioning-policy)
- [ ] Tag will be created from `main` HEAD (not a feature branch)
- [ ] Tag format is `vMAJOR.MINOR.PATCH` (e.g. `v1.1.0`)

---

## Release execution

1. Ensure all pre-release items above are checked.
2. Push the version tag: `git tag v<version> && git push origin v<version>`
3. Confirm `release.yml` runs to completion — `validate` and `security` jobs
   green, `publish` job creates the GitHub Release.
4. Review auto-generated release notes for accuracy before making the release public.

---

## Post-release checklist

- [ ] `[Unreleased]` section in `CHANGELOG.md` is empty and ready for the next cycle
- [ ] Dependabot PRs reviewed; merged or deferred within one week of release
- [ ] Release announced in relevant channels (if applicable)

---

## Versioning policy

This project follows [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

### Version increment rules

| Change type | Bump | Examples |
| --- | --- | --- |
| Breaking change to command interface, hook contract, or agent API | **Major** (`X.0.0`) | Renamed slash command, removed command flag, changed hook exit-code contract, renamed workflow directories |
| New backward-compatible feature — commands, agents, templates, quality profiles, config options | **Minor** (`1.X.0`) | New `/doc-interactive` command, new `rfc` quality profile, new template |
| Bug fixes, doc corrections, test improvements, dependency patches | **Patch** (`1.1.X`) | Fix incorrect hook pattern, correct README example, bump markdownlint version |

### What counts as a breaking change

- Removing or renaming a slash command
- Removing or renaming a hook script that users may invoke directly
- Changing the schema of `quality-gates.json` or `consistency-rules.json` in a
  way that invalidates existing configurations
- Removing or renaming an agent definition that users reference by name
- Renaming the document workflow directories (`rough_draft/`, `pending_approval/`,
  `approved_final/`)
- Changing hook exit-code semantics or structured output format

### Deprecation policy

1. A feature targeted for removal is marked **deprecated** in a minor release.
2. The deprecation and its planned removal version are documented in `CHANGELOG.md`.
3. The feature is removed no earlier than the **next major release**.
4. A replacement is provided at the time of the deprecation announcement where possible.

Pre-release suffixes (`-alpha.N`, `-beta.N`, `-rc.N`) may be used for significant
new versions under broader testing. Pre-release versions are not subject to the
deprecation timeline.

### Runtime compatibility matrix

| Runtime | Minimum | CI-tested |
| --- | --- | --- |
| Node.js | 18 | 20 |
| Python | 3.9 | 3.11 |
| Claude Code CLI | latest stable | latest stable |

Support for older runtimes within the minimums above is best-effort.
Compatibility fixes are accepted as patch releases when they do not add complexity.
The CI matrix is updated at each major release to advance the tested baseline.
