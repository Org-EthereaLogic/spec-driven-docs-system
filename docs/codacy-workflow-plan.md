# Codacy MCP Server Integration Workflow

Comprehensive workflow for AI behavior when interacting with Codacy's MCP Server, ensuring compliance with all mandatory rules and critical protocols.

## Configuration & Context

When calling ANY Codacy tool that accepts these parameters, ALWAYS use:

| Parameter      | Value                      |
|----------------|----------------------------|
| `provider`     | `gh`                       |
| `organization` | `Org-EthereaLogic`         |
| `repository`   | `spec-driven-docs-system`  |

**Constraint:** Avoid calling `git remote -v` unless absolutely necessary.

**Conditional Rule:** Only send `provider`, `organization`, and `repository` if the project is a git repository.

---

## Critical Post-Edit Actions

> **CRITICAL RULE** - Failure to follow constitutes workflow failure.

**RULE: After ANY successful `edit_file` or `reapply` operation**

### Immediate Actions Required

1. Run `codacy_cli_analyze` tool from Codacy's MCP Server for EACH edited file
2. Use these parameters:
   - `rootPath`: workspace path (standard file system path, NOT URL-encoded)
   - `file`: path of the edited file
   - `tool`: leave empty/unset
3. If issues found in new edits, propose AND apply fixes
4. Repeat for each modified file

### Verification Checkpoint

After EVERY response where file edits occurred:

- Verify `codacy_cli_analyze` was executed for all edited files
- Do NOT wait for user to request analysis
- Do NOT require user reminder to run the tool

---

## Dependency & Security Protocols

> **CRITICAL RULE** - This is a blocking operation.

- **RULE: Dependencies and Security Checks with Trivy**

### Trigger Conditions (ANY of these)

- Running `npm install`, `yarn install`, `pnpm install`
- Adding dependencies to `package.json`
- Adding requirements to `requirements.txt`
- Adding dependencies to `pom.xml`
- Adding dependencies to `build.gradle`
- Any other package manager operation

--- ### Immediate Actions Required

1. STOP before continuing other tasks
2. Run `codacy_cli_analyze` with:
   - `rootPath`: workspace path
   - `tool`: `"trivy"`
   - `file`: leave empty/unset

### If Vulnerabilities Found

1. **HALT** all other operations immediately
2. Propose fixes for security issues
3. Apply fixes automatically where possible
4. Resume original task ONLY after security issues resolved

### Example Sequence

```bash
Action: npm install react-markdown
   |
MUST DO: Run codacy_cli_analyze with tool="trivy"
   |
ONLY THEN: Continue with other tasks
```

---

## Error Handling & Troubleshooting

### Scenario 1: Codacy CLI Not Installed

When `codacy_cli_analyze` fails due to missing CLI:

1. ASK user: "Codacy CLI is not installed. Would you like me to install it now?"
2. WAIT for user response (do not proceed without answer)
3. IF "yes": Run `codacy_cli_install` tool, then resume original task
4. IF "no": Inform user they can disable automatic analysis in extension settings

### Scenario 2: MCP Server Unreachable / No Tools Available

Suggest these steps in order:

1. Try resetting the MCP on the extension
2. For VSCode users:
   - Review Copilot > MCP settings in GitHub
   - Navigate to: Settings > Copilot > Enable MCP servers in Copilot
   - Personal: <https://github.com/settings/copilot/features>
   - Organization: <https://github.com/organizations/{org-name}/settings/copilot/features>
   - Note: Organization settings require admin/owner privileges
3. If none work, contact Codacy support

### Scenario 3: 404 Error on Repository/Organization Parameters

When a Codacy tool returns 404:

1. OFFER to run `codacy_setup_repository` tool (do NOT run automatically)
2. ASK user for confirmation
3. IF user accepts: Run `codacy_setup_repository`
4. Retry the failed action exactly ONCE
5. NEVER auto-run `codacy_setup_repository` without user consent

---

## General Usage Rules

### MUST DO

- Repeat analysis steps for EACH modified file
- "Propose fixes" = suggest AND automatically apply where possible
- Use standard, non-URL-encoded file system paths for `rootPath`
- Run `codacy_cli_analyze` proactively (don't wait for user prompts)

### MUST NOT DO

| Forbidden Action | Reason |
|------------------|--------|
| Manual CLI installation (brew, npm, npx, etc.) | Use `codacy_cli_install` tool instead |
| Analyze duplicated code metrics | Not in scope |
| Analyze code complexity metrics | Different from complexity issues |
| Analyze code coverage | Not in scope |
| Run `codacy_setup_repository` without user consent | Security/authorization requirement |
| Wait for user to remind about analysis | Must be proactive |

### Complexity Guidance

- **Complexity ISSUES**: DO address and fix
- **Complexity METRICS**: IGNORE (they are different concepts)

---

## Critical Rules Summary

These rules constitute **WORKFLOW FAILURE** if ignored:

| Rule | Trigger | Required Action |
|------|---------|-----------------|
| Post-Edit Analysis | After `edit_file` or `reapply` | Run `codacy_cli_analyze` for each file |
| Security Scan | After any package manager operation | Run `codacy_cli_analyze` with `tool="trivy"` |
| Blocking on Vulnerabilities | Trivy finds issues | HALT all work until resolved |
| User Consent for Setup | 404 on repo/org params | Ask before running `codacy_setup_repository` |
| CLI Installation Prompt | CLI not installed | Ask user, wait for response |
