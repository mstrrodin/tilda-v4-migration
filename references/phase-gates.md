# Migration phase gates

Read only the sections needed for the current phase and selected page mode.

## Working record

Keep a short, non-secret record for the migration:

```yaml
donor_url: https://donor.example.com/page/
target_url: https://www.example.com/page/
topology: canonical-consolidation
donor_kind: host
mode: native-rebuild
source_available: live-page
cutover_authorized: false
```

Never store passwords, API tokens, customer data, private keys, or production form payloads in the record.

## 0. Inventory

Inspect without mutation:

- exact donor and target URLs;
- current HTTP status, canonical tags, robots directives, sitemap presence, and redirect behavior;
- page sections, copy, media, forms, metadata, structured data, and internal links;
- existing target implementation and duplicate content;
- application build and deploy workflow;
- migration topology and ownership of DNS, TLS, proxy, redirect, and search-console settings;
- analytics definitions used for before/after comparison.

**Gate:** the page mode is supported by evidence. Unknown access or unavailable source data is recorded explicitly.

## 1A. Native rebuild

Build the page with the destination application's components and data model.

Before implementation:

1. Capture a structural and visual inventory of donor sections.
2. Record one to three central claims.
3. Select destination components based on visual behavior and content semantics, not source class names alone.
4. Identify donor content versus optional new SEO or UX material.
5. Plan asset localization and metadata migration.

During implementation:

- preserve meaning and important source wording;
- avoid borrowing unrelated category assets or claims;
- document intentionally omitted donor sections;
- remove legacy duplicates only after unique content has a visible destination;
- verify any project-specific minimum-content thresholds before hiding legacy text.

**Gate:** every meaningful donor section is mapped or intentionally excluded, every central claim remains visible, and no required unique content was lost.

## 1B. Faithful import

Use the best available Tilda source, in descending order of preference:

1. authorized API export;
2. complete static export;
3. archived HTML and assets;
4. a live-page capture only when licensing and access permit it.

Process the export deterministically:

- remove duplicate global navigation, footer, cookie, and popup elements;
- scope imported CSS to the page container;
- localize required assets and rewrite their references;
- preserve videos, forms, and meaningful hidden content deliberately;
- wrap the result in the destination application's metadata, navigation, and lead-flow conventions;
- compare processed output with the source and explain material differences.

**Gate:** no unexplained content loss, no second global header or footer, imported CSS is isolated, and required assets are available from controlled locations.

## 1C. Finish incomplete

Inventory each visible legacy paragraph or section and classify it:

1. duplicate of the new layout — remove or hide;
2. unique and useful — keep visible;
3. important but structurally misplaced — move into an appropriate component, then remove the duplicate source.

Do not apply overlap reports automatically. Similar wording can still contain the only occurrence of an important claim.

**Gate:** duplication is removed without dropping unique meaning, and the page still satisfies project-specific content and SEO validators.

## 2. Verify

Discover and run the repository's own equivalents of:

- type check or compile;
- unit and integration tests;
- content, metadata, asset, link, and structured-data validation;
- production build or static rendering;
- desktop and mobile browser smoke checks.

Do not submit production forms as a routine test. For browser checks, inspect field presence, validation behavior, configured endpoints, and safe non-submitting states.

**Gate:** required checks pass. An unavailable check is reported as unavailable, not passed.

## 3. Release application pages

Track these states separately:

1. local changes;
2. committed branch;
3. code review;
4. merged revision;
5. deployed revision or package;
6. preview or public target verification, as the topology permits.

**Gate:** the exact deployed revision or package and a deployment receipt are known. For a canonical consolidation whose target is already live, verify it publicly. For a same-origin rehost before DNS cutover, verify the new server through a controlled preview or resolution override; public verification belongs to the cutover gate.

## 4. Routing preflight

Choose the applicable topology.

### Same-origin rehost

The public hostname and canonical URLs stay the same; DNS or hosting changes move traffic to the new application. Check:

- important paths exist on the new application;
- canonical URLs remain unchanged;
- responses do not introduce accidental redirects or loops;
- query-dependent behavior still works when required;
- conversion pages still expose the intended lead mechanism.

### Canonical consolidation

The donor moves to a different canonical origin or path. Prepare a deterministic donor-to-target URL map. Check:

- every important live donor URL has a specific destination;
- target pages return a successful response;
- query strings are preserved when required;
- there are no redirect chains or loops;
- conversion pages still expose the intended lead mechanism;
- catch-all behavior is explicit and does not erase important page context;
- shared-host path donors use path-scoped rules only.

Generate proxy configuration from the map when the project supports it. Avoid hand-editing generated files. This mapping step is not applicable to a same-origin rehost unless paths also change.

**Gate:** path parity is verified for a same-origin rehost, or mapping coverage, target health, and generated configuration are verified for a consolidation.

## 5. Authorized cutover

Proceed only after explicit authorization for the external mutations involved.

Recommended order:

1. capture current DNS and proxy state for rollback;
2. verify the exact record or path rule to change;
3. configure TLS and the serving or redirecting virtual host or path rule;
4. detect conflicting host rules before proxy reload;
5. validate proxy configuration, then reload;
6. run a local server smoke test;
7. change DNS when required;
8. run a public DNS and HTTPS smoke test without local resolution overrides;
9. update search-console site-move settings only when the canonical origin changes and the platform supports that operation.

**Gate:** public HTTPS requests reach the new application and return the intended content for a same-origin rehost; for a consolidation, they make the intended permanent redirect in one hop, preserve required query data, and end on a healthy target.

## 6. Observe

During the agreed observation window, inspect:

- routing or redirect errors and unexpected paths;
- canonical page availability;
- form, quiz, calculator, and lead events using consistent definitions;
- organic visibility and index coverage;
- traffic unexpectedly falling into a catch-all destination.

Do not compare a legacy thank-you-page goal with modern form-open or click events as if they were the same lead definition. Record periods, filters, attribution, and deduplication rules.

**Gate:** critical errors are absent and monitoring ownership is clear. For a consolidation, permanent redirects remain in place.

## Definition of done

A domain migration is complete only when all applicable items are evidenced:

- selected page mode implemented and validated;
- canonical pages publicly served from the intended release;
- important paths preserved for a same-origin rehost, or meaningful donor URLs mapped for a consolidation;
- public DNS reaches the intended infrastructure;
- TLS is valid, and any required permanent redirect completes in one hop;
- required query strings survive;
- final targets respond successfully;
- lead mechanisms remain present without unsafe test submissions;
- search-console and observation work are accounted for;
- remaining limitations are explicit.
