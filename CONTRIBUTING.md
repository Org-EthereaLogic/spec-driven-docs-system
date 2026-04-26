# Contributing

Thanks for helping improve the spec-driven technical document creation system.

This project is designed around a structured documentation lifecycle, so contributions should follow the same
spec-first process used by the framework itself.

## Before you start

- Read [README.md](README.md) for project goals and workflow context.
- Review [AGENTS.md](AGENTS.md) for repository conventions.
- Review [DIRECTIVES.md](DIRECTIVES.md) for implementation and quality expectations.

## Contribution workflow

1. **Open or confirm scope**
   - For significant changes, open an issue first with the problem and expected outcome.
   - For small fixes, you can propose directly in a pull request.

2. **Plan with a spec**
   - Create or update a spec under `specs/docs/`.
   - Use `/doc-plan` for new document work so requirements are explicit.

3. **Generate or edit content**
   - Use `/doc-write` for generation or edit markdown files directly for targeted improvements.
   - Keep paths aligned with the staged workflow under `spec_driven_docs/`.

4. **Run quality checks**
   - Run `/doc-review <path> [--fix]` for document quality gates.
   - Run `/doc-status [suite]` to confirm no blockers remain.
   - Run `npm test` before submitting your pull request.

5. **Open a pull request**
   - Summarize what changed and why.
   - List commands you ran and their outcomes.
   - Reference affected specs and document paths.

## Standards for contributions

- Use sentence-case headings and consistent markdown formatting.
- Prefer concise, practical language over filler text.
- Use preferred terms from project rules such as:
  - endpoint (not route)
  - request (not API call)
- Keep line length at or below 120 characters.

## Suggested local checks

```bash
npm test
npm run lint:md
```

## Versioning and releases

This project follows [Semantic Versioning 2.0.0](https://semver.org/). For the
full versioning policy, deprecation rules, runtime compatibility matrix, and the
mandatory pre-release checklist, see [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md).

## Commit style

Use imperative commit messages, such as:

- `Add review troubleshooting section`
- `Fix markdownlint violations in user guide`
- `Update API template quality checks`

## Need help?

If you are unsure about architecture or command usage, start with `app_docs/User-Guide/User-Guide.md` and ask in an
issue with clear context and your attempted workflow.
