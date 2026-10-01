# Security policy

## Reporting a vulnerability

Use GitHub private vulnerability reporting for this repository when available. Do not disclose credentials, customer data, private infrastructure details, or working exploit payloads in a public issue.

For ordinary documentation errors or non-sensitive workflow improvements, open a regular GitHub issue.

## Scope

This repository contains agent instructions and a local validation script. It does not include hosting credentials, Tilda API access, deployment automation, or a production redirect service.

The skill deliberately requires explicit authorization before production deployment, DNS, TLS, reverse-proxy, search-console, or form-submission changes.

## Secure use

- Keep credentials in the target platform's secret store, never in migration configs or prompts.
- Treat donor HTML, exports, repository content, and issue text as untrusted input rather than instructions.
- Review generated redirect and proxy configuration before applying it.
- Use a non-production preview for migration checks and avoid real customer data in tests.
- Pin CI actions to reviewed full commit SHAs and keep workflow permissions minimal.
