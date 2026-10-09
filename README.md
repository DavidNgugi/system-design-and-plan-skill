# System Design and Plan

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

### Into your user-level skills directory

```bash
git clone <this-repo> ~/.agents/skills/system-design-and-plan
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

<details>
<summary><strong>Via the skills CLI</strong></summary>

```bash
npx skills@latest add OWNER/REPO
```

Replace `OWNER/REPO` with the published location once this repository has one.

</details>

The sync script is one-way on purpose: the checkout is the source of truth, `~/.agents/skills` is an installed copy. Edit here, commit, then sync. It compares by content checksum, so an unchanged skill reports `already in sync`, and it refuses to install a tree containing an empty file.

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
references/artifacts.md         required sections per document, task and phase conventions
references/decision-records.md  ADR template, supersession, invariant/threat/refusal registries
references/research-briefs.md   the evidence-first protocol and copy-paste brief template
scripts/check-docs.py           links, anchors, fences, diagram openers
scripts/backlog-stats.py        task counts and effort roll-up
scripts/sync-to-user.sh         install the checkout into ~/.agents/skills (repo copies only)
```

## Requirements

No runtime dependencies. The checkers need Python 3.8 or newer; the sync script needs bash and `rsync`.

## Contributing

The skill's own rules apply to the skill. Small pull requests, evidence for factual claims, no new document without a reason the existing ones cannot carry. Run both checkers before opening one:

```bash
scripts/check-docs.py . --strict
```

## Licence

MIT — see [LICENSE](./LICENSE).
