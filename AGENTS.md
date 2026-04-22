# Repository Guidelines

## Project Structure & Module Organization

`.claude/` hosts the agent definitions, slash commands, hooks, and quality configs that drive this framework. `specs/docs/` keeps document templates and working specifications. `spec_driven_docs/` contains generated documents through three workflow stages: `rough_draft/` (initial `/doc-write` output), `pending_approval/` (reviewed, awaiting stakeholder sign-off), and `approved_final/` (production-ready). `app_docs/` holds the framework User Guide (`app_docs/User-Guide/User-Guide.md`). `prompt/` stores prompt engineering references. Store new assets in the directory that matches their role so CLI tooling can discover them.

## Build, Test, and Development Commands

- `/doc-plan "<topic>" --type {api,design,manual}`: capture intent and outline requirements before writing.
- `/doc-write specs/docs/<spec>.md`: generate the document from the spec via the Writer agent (output lands in `spec_driven_docs/rough_draft/`).
- `/doc-review spec_driven_docs/rough_draft/<path>.md [--fix]`: run all quality gates and optionally auto-fix low-risk issues.
- `/doc-sync <suite>`: validate cross-document links and metadata through the Librarian agent.
- `/doc-batch <suite> <action>`: bulk-plan, write, or review suites (add `--parallel` for concurrent work).
- `/doc-status [suite]`: check the dashboard to confirm gate statuses.
- `/doc-improve`: surface past lessons for future specs.
- `/doc-promote <path> --to {pending_approval,approved_final}`: move a reviewed document to the next workflow stage.
- `npm test`: run the repository smoke suite (JSON validation, hook tests, markdownlint).
- `npm run lint:md`: run markdownlint across every tracked markdown file.

Run commands at the repo root so `.claude/` assets resolve.

## Coding Style & Naming Conventions

Adhere to `.claude/docs/config/consistency-rules.json`: use sentence-case headings, dash-style lists, fenced code blocks with language hints, inline links, and max 120-character lines. Avoid forbidden terms (`TODO`, `placeholder`, `example.com`, etc.) and enforce preferred terminology (use “endpoint” instead of “route”, “request” instead of “API call”). Keep Markdown indentation consistent (two spaces for nested bullets) and follow the required sections (e.g., Overview/Authentication/Endpoints/Error Handling for APIs).

## Testing Guidelines

Testing is the documentation lifecycle plus a thin native test suite. Each spec must satisfy the `spec_completeness`, `content_quality`, `consistency`, and `final_approval` gates defined in `.claude/docs/config/quality-gates.json`. Run `/doc-review` after major edits, follow with `/doc-status` to confirm no blockers, and use `--fix` when auto-fixes exist. Run `npm test` before opening a pull request so JSON validation, hook tests, and markdownlint all pass. Major sections should describe outcomes clearly (the minimum section count was relaxed in `quality-gates.json` v1.1 to favor clarity over exhaustiveness).

## Commit & Pull Request Guidelines

Commits follow the existing imperative style (`Add directive guidance`, `Fix Claude hooks`). PRs should summarize what changed, mention the commands you ran (`/doc-review`, `/doc-status`, `npm test`, etc.), and link the relevant spec or issue. If documentation layout changed, reference the affected paths in `spec_driven_docs/`. Confirm quality gates and `npm test` pass before requesting review, and note any unresolved follow-ups in the PR description.

## Agent Coordination & Quality Tips

Think in agent phases: the Orchestrator (`/doc-plan`) defines goals, the Writer (`/doc-write`) drafts content, the Reviewer (`/doc-review`) enforces the gates, and the Librarian (`/doc-sync`, `/doc-promote`) keeps suites aligned and moves documents through stages. Keep spec paths (`specs/docs/<name>.md`) synchronized with generated paths (`spec_driven_docs/<stage>/<type>/<name>.md`) so batches and dashboards track progress predictably.
