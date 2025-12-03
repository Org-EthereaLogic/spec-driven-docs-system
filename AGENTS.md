# Repository Guidelines

## Project Structure & Module Organization
`.claude/` hosts the agent definitions, slash commands, hooks, and quality configs that drive this framework. `specs/docs/` keeps document templates and working specifications; `docs/` contains the generated manuals plus the User Guide (`docs/User-Guide/User-Guide.md`). `prompt/` stores prompt variants, and `chat/` holds interaction scaffolding. Store new assets there so CLI tooling can discover them.

## Build, Test, and Development Commands
- `/doc-plan "<topic>" --type {api,design,manual}`: capture intent and outline requirements before writing.
- `/doc-write specs/docs/<spec>.md`: generate the document from the spec via the Writer agent.
- `/doc-review docs/<path>.md [--fix]`: run all quality gates and optionally auto-fix low-risk issues.
- `/doc-sync <suite>`: validate cross-document links and metadata through the Librarian agent.
- `/doc-batch <suite> <action>`: bulk-plan, write, or review suites (add `--parallel` for concurrent work).
- `/doc-status [suite]`: check the dashboard to confirm gate statuses.
- `/doc-improve`: surface past lessons for future specs.
Run these at repo root so `.claude/` assets resolve.

## Coding Style & Naming Conventions
Adhere to `.claude/docs/config/consistency-rules.json`: use sentence-case headings, dash-style lists, fenced code blocks with language hints, inline links, and max 120-character lines. Avoid forbidden terms (`TODO`, `placeholder`, `example.com`, etc.) and enforce preferred terminology (use “endpoint” instead of “route”, “request” instead of “API call”). Keep Markdown indentation consistent (two spaces for nested bullets) and follow the required sections (e.g., Overview/Authentication/Endpoints/Error Handling for APIs).

## Testing Guidelines
Testing is the documentation lifecycle: each spec must satisfy the `spec_completeness`, `content_quality`, `consistency`, and `final_approval` gates defined in `.claude/docs/config/quality-gates.json`. Run `/doc-review` after major edits, follow with `/doc-status` to confirm no blockers, and use `--fix` when auto-fixes exist. Ensure major sections exceed ~50 words, all internal links resolve, and required templates remain intact before marking a change ready.

## Commit & Pull Request Guidelines
Commits follow the existing imperative style (`Add directive guidance`, `Fix Claude hooks`). PRs should summarize what changed, mention the commands you ran (`/doc-review`, `/doc-status`, etc.), and link the relevant spec or issue. If documentation layout changed, add rendered path or screenshot references to `docs/`. Confirm the quality gates pass before requesting review, and note any unresolved follow-ups in the PR description.

## Agent Coordination & Quality Tips
Think in agent phases: the Orchestrator (`/doc-plan`) defines goals, the Writer (`/doc-write`) drafts content, the Reviewer (`/doc-review`) enforces the gates, and the Librarian (`/doc-sync`) keeps suites aligned. Keep spec paths (`specs/docs/<name>.md`) synchronized with document paths (`docs/<type>/<name>.md`) so batches and dashboards track progress predictably.
