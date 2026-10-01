# Security audit — 2026-10-01

## Executive summary

The public package was reviewed as a Codex instruction bundle with a dependency-free Python validator and one GitHub Actions workflow. No secrets, private infrastructure data, PII, or critical/high-risk vulnerabilities were found.

Three defense-in-depth findings were fixed:

1. GitHub Actions dependencies used mutable major-version tags and checkout retained credentials.
2. The package validator did not explicitly reject symbolic links.
3. The migration instructions did not explicitly classify donor exports and HTML as untrusted, non-executable input.

After remediation, the package passes its validator, negative security tests, `actionlint`, `gitleaks`, and AgentShield.

## Scope

- `SKILL.md`, supporting Markdown, example YAML, and UI metadata;
- `scripts/validate.py` and its negative tests;
- `.github/workflows/validate.yml`;
- public GitHub repository settings relevant to secrets and protected changes.

This was a focused project-maintainer review, not a third-party penetration test or certification.

## Findings

### SEC-001 — Mutable GitHub Actions references

- **Severity:** Medium
- **Status:** Fixed
- **Risk:** A mutable action tag can move to different code, increasing CI supply-chain exposure.
- **Remediation:** Pin `actions/checkout` and `actions/setup-python` to reviewed full commit SHAs, disable persisted checkout credentials, use read-only contents permission, and set a job timeout.

### SEC-002 — Symbolic links were not explicitly rejected

- **Severity:** Low
- **Status:** Fixed
- **Risk:** A future contribution could add a symlink that points outside the intended package tree or bypasses assumptions about ordinary text files.
- **Remediation:** Reject every symbolic link before reading package files and cover the behavior with a negative test.

### SEC-003 — Donor executable content needed an explicit trust boundary

- **Severity:** Medium
- **Status:** Fixed
- **Risk:** A faithful import could carry over donor scripts, inline event handlers, trackers, or unreviewed third-party embeds, while malicious text could be mistaken for agent instructions.
- **Remediation:** Treat donor pages and exports as inert, untrusted data; never follow embedded instructions; remove executable content by default and reimplement required behavior through reviewed components or an explicit allowlist.

## Verification

- AgentShield 1.6.0: grade A, score 100, zero findings across the one applicable Codex configuration file;
- gitleaks: zero leaks across repository history and working tree;
- GitHub secret scanning: enabled, zero alerts at review time;
- GitHub push protection: enabled;
- private vulnerability reporting: enabled;
- `actionlint`: passed;
- package validator and nine negative security tests: passed;
- relative links and YAML syntax: passed.

## Limitations

- The repository has no runtime service and no third-party Python dependencies, so dependency and dynamic application scans are not applicable.
- Code-scanning and Dependabot alert endpoints were unavailable because there is no supported dependency or code-scanning setup.
- Operational safety still depends on users preserving the skill's explicit authorization gates for deploy, DNS, proxy, search-console, and form mutations.
