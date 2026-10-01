# Publishing checklist

This directory is designed to become the root of a standalone public repository.

## Suggested repository metadata

- **Name:** `tilda-v4-migration`
- **Description:** `Codex skill for staged Tilda-to-VPS migrations with content, SEO, redirect, cutover, and monitoring gates.`
- **Topics:** `codex-skill`, `tilda`, `website-migration`, `vps`, `seo`, `redirects`, `devops`
- **License:** MIT
- **Initial release:** `v0.1.0`

## Before making the repository public

1. Run `python3 scripts/validate.py`.
2. Review the complete staged file list, including dotfiles.
3. Confirm there are no credentials, customer data, private hostnames, infrastructure addresses, analytics IDs, private repository URLs, or absolute local paths.
4. Confirm the Git history contains only this public package. Do not publish it by pushing the parent repository's history.
5. Enable GitHub private vulnerability reporting if it is available for the repository.
6. Protect the default branch and require the `Validate skill` workflow for pull requests.
7. Create the `v0.1.0` release from the reviewed default-branch commit.

## Standalone publication

Create the public repository from this directory, not from its private parent. A typical sequence is:

```bash
cd open-source/tilda-v4-migration
git init
git add .
git commit -m "feat: publish tilda v4 migration skill"
```

Create and push the GitHub repository only after the user explicitly authorizes publication. The final public reread should confirm the README, license, workflow, and release tag from GitHub itself.
