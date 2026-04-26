# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 1.x     | Yes       |

Older versions are not supported. Please upgrade to the latest release before
reporting a vulnerability.

## Reporting a vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Report vulnerabilities by emailing:

**<anthony.johnsonii@etherealogic.ai>**

Include in your report:

- A description of the vulnerability and its potential impact
- Steps to reproduce or a proof-of-concept (if available)
- The version(s) affected
- Any suggested mitigations you are aware of

You will receive an acknowledgement within **2 business days**.

## Severity levels and response SLAs

| Severity | Criteria | Initial triage | Target patch |
| -------- | -------- | -------------- | ------------ |
| Critical | Remote code execution, credential exposure, supply-chain compromise | 24 hours | 7 days |
| High | Significant data exposure, privilege escalation | 48 hours | 14 days |
| Medium | Limited impact, requires non-default configuration | 5 business days | 30 days |
| Low | Minimal impact, defense-in-depth issues | 10 business days | Next release |

SLAs begin when the report is acknowledged. If a patch requires coordination
with upstream dependencies, the timeline may be extended — we will communicate
any delay to the reporter.

## Disclosure policy

We follow a coordinated disclosure model:

1. Reporter submits vulnerability privately.
2. We acknowledge within 2 business days.
3. We investigate, develop a fix, and agree on a disclosure date with the reporter.
4. We publish a patched release and a security advisory on GitHub.
5. Reporter may publish details after the patched release is available or after
   90 days from initial report (whichever comes first), unless an extension is
   mutually agreed upon.

## Scope

This policy covers:

- The slash command implementations under `.claude/commands/`
- The hook scripts under `.claude/hooks/`
- CI/CD workflow definitions under `.github/workflows/`
- The test suite and install scripts under `tests/`

**Out of scope:** vulnerabilities in third-party dependencies should be reported
directly to those projects. We will, however, update dependencies promptly upon
being notified of relevant CVEs.

## Security best practices for users

- Pin GitHub Actions to specific commit SHAs in any workflows you derive from
  this project.
- Review hook scripts before enabling them in your environment — hooks execute
  shell commands.
- Do not store secrets or credentials in document specifications or generated
  outputs committed to version control.
