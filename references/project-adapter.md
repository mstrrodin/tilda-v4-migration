# Project adapter

This skill intentionally does not assume a framework, deployment provider, analytics platform, or repository layout. Map its capabilities onto the target project before implementation.

## Discover project capabilities

Inspect repository documentation, package manifests, task runners, CI workflows, and deployment runbooks. Locate an existing command or process for each applicable capability:

| Capability | Examples of evidence |
|---|---|
| Donor inventory | export parser, HTML analyzer, saved snapshot |
| Content coverage | section manifest, source-to-component map |
| Asset localization | importer, optimizer, content-addressed media store |
| Metadata validation | title, description, canonical, robots checks |
| Application checks | typecheck, lint, unit tests, integration tests |
| Render verification | build, SSR/static snapshot, browser smoke |
| Redirect mapping | versioned route map or redirect registry |
| Preflight | donor crawl, target health, form-presence checks |
| Deployment proof | exact revision, package ID, deploy receipt |
| Public smoke | DNS, TLS, redirect hop, target response checks |

Prefer established project commands. If a capability is missing, report the gap before adding new tooling; create a helper only when it will be reused or materially reduces migration risk.

## Recommended migration config

Use [../examples/migration-config.example.yaml](../examples/migration-config.example.yaml) as a non-secret working record. Adapt field names to the repository if it already has a canonical format.

The important properties are:

- exact donor and target identity, including whether the topology is a same-origin rehost or canonical consolidation;
- selected page mode and source availability;
- ownership of DNS, TLS, proxy, deployment, and analytics;
- explicit cutover authorization state;
- commands that provide evidence for each gate;
- rollback notes per external layer;
- comparable lead and visibility definitions.

## Authorization model

Treat authorization as action-specific and current. Authorization to implement a page does not imply authorization to deploy it, alter DNS, submit forms, or change search-console settings.

Record authorization as a boolean only for session routing; the human request remains the source of truth. Do not persist credentials or approval tokens in the migration config.

## Evidence model

Use exact artifacts where possible:

- commit SHA or immutable package identifier;
- CI run and named checks;
- deployment receipt;
- public HTTP response chain;
- DNS answer from a public resolver;
- timestamped analytics export with documented filters.

Green CI, a merge, a local proxy test, or one successful page response proves only its own layer.
