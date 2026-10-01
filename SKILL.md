---
name: tilda-v4-migration
description: "Plan and execute staged migrations from Tilda to a self-managed VPS, including faithful imports, native component rebuilds, unfinished migration cleanup, redirect preparation, explicitly authorized cutover, and post-launch verification. Use when moving Tilda pages or domains while preserving content, SEO signals, lead flows, and rollback options."
---

# Tilda V4 Migration

Treat migration as a sequence of evidence-backed states:

`inventory → classify → build → verify → release → preflight → cutover → observe`

Do not collapse local completion, a merged change, deployment, DNS cutover, and a working public redirect into a single "done" state.

## Start with inventory

Collect these inputs before editing anything:

- donor URL and canonical target URL;
- topology: same-origin rehost or consolidation onto a different canonical origin;
- donor kind: full host or path within a shared host;
- available Tilda source: API export, static export, saved HTML, or live page only;
- application stack, build commands, deploy path, and redirect owner;
- forms and analytics definitions that must survive migration;
- whether production cutover is explicitly authorized.

Inspect the repository for existing importers, page models, component libraries, redirect maps, validators, and deployment runbooks. Reuse verified project mechanisms instead of inventing parallel ones. Read [references/project-adapter.md](references/project-adapter.md) when mapping this workflow onto a repository.

## Choose one page mode

Classify each page independently:

| Mode | Use when | Main trade-off |
|---|---|---|
| **Native rebuild** | The page should become maintainable application components | Best integration; requires editorial and visual interpretation |
| **Faithful import** | The original Tilda design and copy should remain close to 1:1 | Highest fidelity; imported markup and CSS need isolation |
| **Finish incomplete** | A new layout exists but legacy content still duplicates or conflicts with it | Smallest change; requires careful overlap review |

Do not infer that an old version label means a broken page. Inspect rendered structure, content coverage, and current behavior first.

## Preserve meaning, not only structure

For every page:

1. Inventory meaningful sections, media, metadata, forms, structured data, and internal links.
2. Read the donor as an editor and record one to three key claims the page exists to communicate.
3. Map every meaningful donor section to a destination component or document why it is intentionally omitted.
4. Keep source-backed copy distinct from newly written SEO or UX additions.
5. Localize required assets and preserve attribution or licensing records where applicable.

Structural coverage does not prove that the page's central message survived.

## Test without creating production leads

Unless the user explicitly authorizes a controlled submission, do not submit real or synthetic contact data. Verify forms through rendered fields, handlers, endpoint configuration, validation states, and non-mutating UI checks.

Run the repository's relevant type checks, tests, content validators, build, and browser smoke checks. Verify at least:

- one intended H1 and correct metadata;
- expected sections and key claims are visible;
- images and media load;
- mobile and desktop layouts remain usable;
- structured data is valid when present;
- no unintended legacy-content duplication remains;
- forms are present and wired without submitting them.

Use [references/phase-gates.md](references/phase-gates.md) for mode-specific gates and the definition of done.

## Keep production mutations behind an authorization gate

Repository preparation and read-only preflight do not authorize external mutations. Require explicit user authorization immediately before changing any of the following:

- production deployment;
- DNS records;
- certificates or reverse-proxy configuration;
- permanent redirects on a live host;
- search-console site-move settings;
- production form submissions.

Before cutover, define rollback per changed layer and classify the topology:

- For a **same-origin rehost**, preserve the public hostname and URL paths. Verify that public DNS reaches the new server and that existing URLs still return their intended content without accidental redirects.
- For a **canonical consolidation**, prepare an exact URL map, validate every important target, preserve query strings, and require the intended permanent redirect in one hop. A path donor on a shared host must never receive a host-wide redirect.

Local proxy smoke tests do not prove that public DNS reaches the new server. Declare cutover complete only after the applicable public HTTPS behavior is verified.

## Report states and evidence

Report each layer separately:

| Layer | Example states |
|---|---|
| Donor inventory | complete / incomplete / unavailable |
| Page implementation | local / review / merged |
| Validation | passed / failed / unavailable |
| Application release | not deployed / deployed / preview-verified / publicly verified |
| Routing or redirect | drafted / installed / publicly verified / not applicable |
| Observation | not started / active / complete |

If evidence is missing, say `unverified`. Do not convert missing lead, conversion, or visibility data into zero.
