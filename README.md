# System Design and Plan

[![CI](https://github.com/DavidNgugi/system-design-and-plan-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/DavidNgugi/system-design-and-plan-skill/actions/workflows/ci.yml)
[![npm version](https://img.shields.io/npm/v/system-design-and-plan-skill)](https://www.npmjs.com/package/system-design-and-plan-skill)
[![npm downloads](https://img.shields.io/npm/dm/system-design-and-plan-skill)](https://www.npmjs.com/package/system-design-and-plan-skill)
[![Licence](https://img.shields.io/npm/l/system-design-and-plan-skill)](./LICENSE)

An agent skill that produces the engineering plan a project deserves **before** anyone writes code: the architecture, the data model, the flows, the decisions with the alternatives they beat, a tiered effort model, a granular backlog, and the rules that bind every later change.

Not a template pack. A process with gates — evidence before claims, decisions recorded rather than remembered, numbers derived from the backlog instead of asserted, and documents that can be machine-checked.

It was extracted from a real planning exercise: a 36-document corpus, 19 decision records, a 472-task core backlog, and more than a dozen external facts that were wrong when first written and were corrected against primary sources.

## What it produces

| Document | The question it answers |
| --- | --- |
| `README.md` | What is this, is it for me, how do I run it, what is the legal position |
| `ARCHITECTURE.md` | How the system is structured and why: module map, contracts, budgets, platform matrix, spikes |
| `DATA_MODEL.md` | What is stored, with which invariants, indices, retention, and migration policy |
| `FLOWS.md` | What happens over time, including failure paths and state machines |
| `TECH_STACK.md` | Why each technology, and what it beat |
| `DEPENDENCIES.md` | Exact verified versions, licences, obligations, update policy |
| `PLAN.md` | Phases, exit criteria, effort model, risk register, release checklist |
| `TASKS.md` | Granular work with IDs, acceptance criteria, dependencies, estimates, critical path |
| `DESIGN_SYSTEM.md` | Tokens, motion, components, theming, accessibility |
| `SECURITY.md` | Threat catalogue, controls, accepted risks, reporting policy |
| `AGENTS.md` | Numbered rules that bind every change, human or agent |
| `adr/*.md` | One load-bearing decision each, with alternatives and a verification path |
| `research/*.md` | Evidence snapshots with an explicit verification status |

The corpus has a division of labour, and that is the point: **one fact lives in one place**. Decisions in ADRs, structure in ARCHITECTURE, behaviour in FLOWS, data in DATA_MODEL, work in TASKS. A reviewer should be able to delete any duplicated paragraph and lose nothing.

## How it works

Seven phases, each with a gate:

1. **Recon.** Repo state, toolchain, disk, network reachability of the sources you will need. Gate: you know what you are building on.
2. **Lock the load-bearing decisions.** The three to five choices that will appear in every file — platform, language, storage, distribution, name. Ask with options, trade-offs, and a recommendation. Gate: no document names a stack that was not agreed.
3. **Evidence, in parallel with the anchor document.** Dispatch research as parallel agents with a brief that demands primary sources, explicit licences, and a "what I could not verify" section. Write `ARCHITECTURE.md` yourself while they run.
4. **Self-correct against the evidence.** When a finding contradicts something you wrote, fix the owning document. If it was a *recorded decision*, supersede it in a new ADR and mark the original. Tell the user which of your own claims were wrong.
5. **Reconcile the numbers.** Derive totals with `scripts/backlog-stats.py`, then propagate them everywhere they are quoted.
6. **Machine-check.** Run `scripts/check-docs.py`. Confirm every invariant names a test and every task has acceptance criteria.
7. **Handover.** Rules file, spike table, roadmap tiers, refused-scope tables, and the one or two artifacts that matter most.

## The principles it enforces

| # | Principle |
| --- | --- |
| P1 | **Evidence before claims.** Never assert a version, endpoint, quota, licence, or benchmark from memory. Verify, or mark it `unverified` in the document |
| P2 | **Decisions are records.** Every load-bearing choice gets an ADR with consequences and rejected alternatives |
| P3 | **One fact, one place.** Link, never duplicate |
| P4 | **Numbers are derived.** Task counts and effort come from a script or a measurement |
| P5 | **Scope is tiered and honestly priced.** Core, full quality bar, and post-1.0 roadmap are separate totals with a calendar model |
| P6 | **Cross-cutting concerns get a seam on day one.** Gating, accounts, observability, i18n, accessibility: the interface exists in 1.0 even when the feature is later |
| P7 | **Limitations are stated in the product.** Refused-scope tables, accepted risks, best-effort labels, degraded modes |
| P8 | **Unknowns become time-boxed spikes**, each naming the decision it could overturn |
| P9 | **Docs are machine-checked.** Links, anchors, fences, diagrams, schemas, invariants |
| P10 | **Ask before big work.** Lock the decisions with the user first; guessing costs the whole corpus |

## Install

Pick **one** channel. They all end the same way — a directory holding `SKILL.md`, `references/` and `scripts/` wherever the agent looks — and two of them claim the same path, so the second silently owns the files while the first keeps trying to manage them.

### Any agent, via the skills CLI

```bash
npx skills add DavidNgugi/system-design-and-plan-skill
```

Verified against this repository: the CLI finds exactly one skill, `system-design-and-plan`, and copies the whole bundle. Without `-g` it installs to `./.agents/skills/` in the current project; with `-g`, to `~/.agents/skills/`, which is the canonical location and where DSH reads it.

`-a` chooses which agent additionally gets a link to that canonical copy; it does not move the canonical copy. Agents that already scan `~/.agents/skills` need no flag at all — see [Where a skill has to land](#where-a-skill-has-to-land).

### Claude Code, Codex and Copilot, from the plugin marketplace

```bash
claude plugin marketplace add DavidNgugi/system-design-and-plan-skill
claude plugin install system-design-and-plan@davidngugi

codex plugin marketplace add DavidNgugi/system-design-and-plan-skill
codex plugin add system-design-and-plan@davidngugi

copilot plugin marketplace add DavidNgugi/system-design-and-plan-skill
copilot plugin install system-design-and-plan@davidngugi
```

One pair of manifests serves all three — [marketplace.json](./.claude-plugin/marketplace.json) and [plugin.json](./.claude-plugin/plugin.json) — because Codex and Copilot both read `.claude-plugin/` alongside their own directories. Neither file declares a `skills` list, and that omission is what makes the root `SKILL.md` load as a single skill in all three.

`claude plugin validate . --strict` is the check, and it passes. Claude Code pins an installed plugin to `version` in [plugin.json](./.claude-plugin/plugin.json) until you change it, so **bump that field whenever the skill changes** or the plugin channel keeps serving the old copy. The update commands are `claude plugin update`, `codex plugin marketplace upgrade` and `copilot plugin update`.

### From npm, for tooling

```bash
npm install system-design-and-plan-skill
```

The published tarball is the skill itself — `SKILL.md`, `references/`, `scripts/` and `.claude-plugin/` — with no runtime dependencies and no install scripts. It exists so a marketplace entry can name an immutable version instead of a git ref:

```json
{
  "source": {
    "source": "npm",
    "package": "system-design-and-plan-skill",
    "version": "^1.0.0"
  }
}
```

There is no `bin`, so `npx system-design-and-plan-skill` does nothing useful. Use one of the channels above to install the skill for an agent.

### Into your user-level skills directory

```bash
git clone https://github.com/DavidNgugi/system-design-and-plan-skill ~/.agents/skills/system-design-and-plan
```

Or, from an existing checkout, let the sync script do it:

```bash
scripts/sync-to-user.sh --dry-run   # show what would change
scripts/sync-to-user.sh             # install
```

<details>
<summary><strong>Into a single project instead</strong></summary>

Copy the directory to `.agents/skills/system-design-and-plan/` inside the repo so the whole team gets it with the checkout, and commit it.

</details>

The sync script is one-way on purpose: the checkout is the source of truth, `~/.agents/skills` is an installed copy. Edit here, commit, then sync. It compares by content checksum, so an unchanged skill reports `already in sync`, and it refuses to install a tree containing an empty file.

**Do not point the sync script at a skill the CLI installed.** Both own `~/.agents/skills/system-design-and-plan`. The CLI fingerprints each skill's directory in `~/.agents/.skill-lock.json` and expects to update that directory itself; the sync script `rsync --delete`s it from the checkout. Run both and `npx skills update` reports drift on a skill it believes it manages, while the two overwrite each other's files. One channel per directory.

### Where a skill has to land

Agents scan different directories, so a global install is visible to some and invisible to others unless they are named:

| Agent | Directories scanned | A `-g` install |
| --- | --- | --- |
| DSH | `~/.agents/skills`, `~/.dsh/skills`, `<project>/.agents/skills`, `<project>/.dsh/skills` | visible, no flag needed |
| Copilot | `~/.agents/skills`, `~/.copilot/skills`, `<project>/.agents/skills` | visible, no flag needed |
| Gemini CLI | `~/.gemini/skills`, `<project>/.agents/skills` | needs `-a gemini-cli` |
| Claude Code | `~/.claude/skills`, `<project>/.claude/skills` | needs `-a claude-code` |
| Codex | `~/.codex/skills`, `<project>/.agents/skills` | needs `-a codex` |

DSH merges its local roots by rank — nearest first, `<project>/.dsh/skills`, `<project>/.agents/skills`, configured custom directories, `~/.dsh/skills`, `~/.agents/skills` — and keeps the nearest copy of a duplicate name silently. An installed skill and a project copy therefore resolve to one entry, not two.

## The scripts

Both are optional. They exist because unchecked documents drift.

### `scripts/check-docs.py`

Validates a markdown corpus: relative links resolve, **anchor fragments** exist and are unambiguous, code fences balance, and every diagram block opens with a known type.

```bash
scripts/check-docs.py .
scripts/check-docs.py . --strict   # treat warnings as failures
scripts/check-docs.py . --json
```

Warnings rather than failures are used for repeated headings, because structured repetition (one block per subject) is legitimate — but it makes that heading's anchor ambiguous, which is worth knowing.

### `scripts/backlog-stats.py`

Parses a task table and rolls it up by epic, phase, and tier, so the numbers in your plan can be derived rather than counted by hand.

```bash
scripts/backlog-stats.py docs/TASKS.md
scripts/backlog-stats.py docs/TASKS.md --phases "0:0-4,1:5-9,2:10-15"
scripts/backlog-stats.py docs/TASKS.md --core "1:1-13,3:1-10" --contingency 0.3
```

Expects rows shaped like `| PFX-E12-03 | description | acceptance | deps | M |`, with estimates from `XS 0.5`, `S 1`, `M 2.5`, `L 4.5`, `XL 8` ideal days.

## Why it exists

| Failure mode | The fix in this skill |
| --- | --- |
| Versions, quotas, and licences recalled from memory and written as fact | Evidence-first research briefs that forbid invention and require a verification-status section |
| One enormous document, so every reader loads everything | A corpus with a division of labour and a rule against duplication |
| A single effort number with no tiers and no calendar assumption | Core / full-bar / post-1.0 totals, explicit contingency, a stated effective-days-per-year model |
| Tasks that are wishes rather than work | Every task has an ID, observable acceptance criteria, dependencies, and an estimate |
| A cross-cutting concern deferred, then retrofitted through a finished read path | A seam in 1.0, with the reason recorded in the ADR that defers the feature |
| Security, parenting, or permissions implemented in the UI layer | Boundaries in the query layer, failing closed, with a leak-audit spike |
| Decisions changed silently in a document | Supersession: a new ADR, a marked original, and the correction reported |
| Documents nobody can check, so drift is inevitable | Checkers for links, anchors, diagrams, schemas, and the backlog roll-up |

**Not for:** a single-file change, a bug fix, or a prototype whose whole purpose is to learn by building. For those, write the code.

## Layout

```
SKILL.md                        the process: principles, phases, protocols, self-review
.claude-plugin/marketplace.json the catalog Claude Code, Codex and Copilot register
.claude-plugin/plugin.json      plugin metadata; no skills list, so the root SKILL.md is the skill
references/artifacts.md         required sections per document, task and phase conventions
references/decision-records.md  ADR template, supersession, invariant/threat/refusal registries
references/research-briefs.md   the evidence-first protocol and copy-paste brief template
scripts/check-docs.py           links, anchors, fences, diagram openers
scripts/backlog-stats.py        task counts and effort roll-up
scripts/sync-to-user.sh         install the checkout into ~/.agents/skills (repo copies only)
package.json                    npm packaging; its version must match plugin.json
.github/workflows/ci.yml        doc checkers, manifest validation, tarball contents
.github/workflows/release.yml   tag -> npm publish over OIDC -> GitHub Release
.github/dependabot.yml          monthly bump of the workflow action majors
```

## Requirements

No runtime dependencies. The checkers need Python 3.8 or newer; the sync script needs bash and `rsync`.

## Contributing

The skill's own rules apply to the skill. Small pull requests, evidence for factual claims, no new document without a reason the existing ones cannot carry. Run both checkers before opening one:

```bash
scripts/check-docs.py . --strict
```

If you touch `.claude-plugin/`, validate it too and bump `version` in [plugin.json](./.claude-plugin/plugin.json) whenever the skill's behaviour changes, because that field is what pins users to a release:

```bash
claude plugin validate . --strict
```

## Releasing

Publishing is automated by [release.yml](./.github/workflows/release.yml), which authenticates to npm with OIDC trusted publishing: there is no `NPM_TOKEN` secret to store or rotate, and provenance is generated automatically.

1. Bump `version` in **both** [package.json](./package.json) and [plugin.json](./.claude-plugin/plugin.json). The release fails if those two disagree with each other or with the tag, so a half-bump cannot ship.
2. Commit, then tag and push:

```bash
git tag v1.0.1
git push origin v1.0.1
```

The workflow re-runs the checks, refuses a version that is already on npm, publishes, and creates the GitHub Release. The very first version was published by hand, because npm only lets you configure a trusted publisher on a package that already exists.

A tag publishes a version that is **not yet on npm**. Tagging a version that is already published fails the release rather than republishing it, so the release after a manual first publish is the *next* version — `1.0.0` by hand, then `v1.0.1` through CI.

Three npm rules matter here, and each is easy to get wrong. The trusted publisher must have **"Allow npm publish"** ticked — configurations created after 2026-09-03 default to allowing `npm stage publish` only, so a workflow that runs `npm publish` fails without that box. A new configuration must complete its **first successful publish within two days**, which is what validates it and binds it to the repository's immutable identity; an expired configuration cannot be edited, only deleted and replaced. And npm **rejects trusted-publishing tokens from `pull_request_target` and `issue_comment`** events, which is why the release triggers on a tag push rather than a pull request.

Its required fields are the *GitHub* owner and repository — `DavidNgugi` / `system-design-and-plan-skill` — not the npm account that owns the package, which is `devdavid`. Trusted publishing needs npm 11.5.1 or newer and Node 22.14.0 or newer, so the workflow pins Node 24 and fails early on an older npm rather than making you debug a misleading 404.

Once publishing works, harden the package under its npm **Settings → Publishing access** by selecting **Require two-factor authentication and disallow tokens**. That blocks long-lived tokens without affecting trusted publishers.

## Licence

MIT — see [LICENSE](./LICENSE).
