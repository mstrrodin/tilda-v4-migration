# Tilda to VPS Migration Skill

A reusable Codex skill for moving pages and domains from Tilda to a self-managed application and VPS without treating page rebuild, deployment, DNS cutover, redirects, and analytics as one opaque operation.

The workflow supports three page strategies:

- **Native rebuild** — reinterpret the donor page into maintainable application components.
- **Faithful import** — preserve the Tilda page's design and copy as closely as practical while isolating imported markup and CSS.
- **Finish incomplete** — remove legacy duplication from a migration that is already partly implemented.

## What this skill provides

- evidence-first inventory and mode selection;
- content, media, metadata, SEO, and lead-flow preservation gates;
- a strict boundary between repository work and production mutations;
- path-parity checks for same-origin rehosts and redirect-map checks for canonical consolidations;
- public DNS, TLS, redirect, and target verification;
- comparable before/after measurement guidance.

It does not provide Tilda credentials, hosting access, a universal exporter, or permission to change production infrastructure.

## Install

Copy or clone this directory into either a project-local skill directory:

```text
<project>/.agents/skills/tilda-v4-migration/
```

or your Codex skills directory:

```text
~/.codex/skills/tilda-v4-migration/
```

The directory containing `SKILL.md` is the skill root.

## Use

Invoke it explicitly:

```text
Use $tilda-v4-migration to audit this Tilda donor and prepare a native rebuild.
```

Or ask naturally:

```text
Plan a staged migration of https://donor.example.com/ to our VPS without changing DNS yet.
```

For a real project, first adapt the workflow to existing commands using [references/project-adapter.md](references/project-adapter.md). A safe starter record is available at [examples/migration-config.example.yaml](examples/migration-config.example.yaml).

## Safety model

The skill requires separate, explicit authorization before production deployment, DNS, TLS, reverse-proxy, permanent redirect, search-console, or production-form mutations. It also distinguishes:

- local implementation;
- reviewed or merged code;
- deployed release;
- publicly verified canonical pages;
- publicly verified donor redirects.

Missing analytics evidence is reported as unverified, never converted into zero.

## Validate

Run the dependency-free package validator:

```bash
python3 scripts/validate.py
```

It checks the skill frontmatter, UI metadata, local Markdown links, required package files, unfinished placeholders, and executable bit on the validator itself.

## Repository layout

```text
.
├── SKILL.md
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── PUBLISHING.md
├── agents/openai.yaml
├── examples/migration-config.example.yaml
├── references/phase-gates.md
├── references/project-adapter.md
├── scripts/validate.py
└── .github/workflows/validate.yml
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Keep the skill provider-neutral and avoid adding organization-specific domains, credentials, infrastructure addresses, analytics IDs, or repository paths.

For repository settings, release naming, and the final public checklist, see [PUBLISHING.md](PUBLISHING.md).

## License

MIT. See [LICENSE](LICENSE).
