# Contributing

The skill's own rules apply to the skill: evidence for factual claims, no new document without a reason the existing ones cannot carry, and small pull requests.

## Checks

CI runs all of these on every push and pull request. Run them locally before opening one:

```bash
python3 scripts/check-docs.py . --strict
claude plugin validate . --strict
npm pack --dry-run
```

`check-docs.py` validates relative links, anchor fragments, code-fence parity, and diagram blocks. `claude plugin validate` is the authoritative check on `.claude-plugin/`, and it inspects `plugin.json` as well as the marketplace entry — a broken manifest passes a JSON parse, so run it. The `npm pack` dry run confirms the tarball still contains every skill file and nothing that belongs to the repository rather than the package.

## Releasing

Releases are automated by [`.github/workflows/release.yml`](./.github/workflows/release.yml), which authenticates to npm with OIDC trusted publishing. There is no `NPM_TOKEN` secret to store, rotate, or leak, and a provenance attestation is generated automatically.

1. Bump `version` in **both** [`package.json`](./package.json) and [`.claude-plugin/plugin.json`](./.claude-plugin/plugin.json). The release fails if either disagrees with the other or with the tag, so a half-bump cannot ship.
2. Commit, then tag and push:

```bash
git tag v1.0.1
git push origin v1.0.1
```

A tag publishes a version that is **not yet on npm**. Tagging an already-published version fails the release rather than republishing it, so the release after a manual first publish is the *next* version: `1.0.0` by hand, then `v1.0.1` through CI.

The workflow re-runs the checks, refuses a version already on npm, publishes, and creates the GitHub Release.

### Why the first publish is manual

npm only lets you configure a trusted publisher on a package that already exists, so `1.0.0` was published by hand. That version carries no provenance attestation; CI releases do.

### npm rules that are easy to get wrong

- The trusted publisher must have **"Allow `npm publish`"** ticked. Configurations created after 2026-09-03 default to allowing `npm stage publish` only, so a workflow that runs `npm publish` fails without that box.
- Its required fields are the **GitHub** owner and repository — `DavidNgugi` / `system-design-and-plan-skill` — not the npm account that owns the package, which is `devdavid`.
- A new configuration must complete its **first successful publish within two days**. That publish validates it and binds it to the repository's immutable identity. An expired configuration cannot be edited, only deleted and replaced.
- npm **rejects trusted-publishing tokens from `pull_request_target` and `issue_comment`** events, which is why the release triggers on a tag push rather than a pull request.
- Trusted publishing needs npm 11.5.1 or newer and Node 22.14.0 or newer. The workflow pins Node 24 and checks the npm version explicitly, so an old npm fails with a clear message instead of a misleading 404 on `PUT`.

### Hardening

Once publishing works, set the package's npm **Settings → Publishing access** to **Require two-factor authentication and disallow tokens**. That blocks long-lived tokens without affecting trusted publishers, leaving the workflow as the only way to publish.

## Licence

MIT — see [LICENSE](./LICENSE).
