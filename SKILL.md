---
name: system-design-and-plan
description: Produces a rigorous, evidence-backed engineering plan for a new system or large feature before code exists — the document corpus (architecture, data model, flows, stack, dependencies, roadmap, granular backlog, design system, security, ADRs, agent rules), verified external facts, derived estimates, and machine-checked docs. Use when the user asks for a deep plan, system design, architecture, technical roadmap, effort estimate, staffing/calendar estimate, granular task breakdown, design docs, ADRs, or "plan this properly".
---

# System Design and Plan

## What this produces

A reviewable design corpus that a team or an agent can implement from, before any code is written. The output is the specification: decisions recorded with their rejected alternatives, external facts cited, estimates derived from the backlog, and limitations stated in the product rather than discovered later.

## When to use it

Use for: a new system or product; a multi-week feature; any work with irreversible choices (language, storage, licensing, distribution); "plan this properly"; estimating effort for staffing; onboarding contributors who will read the docs instead of asking questions.

Do not use for: a single-file change, a bug fix, a spike whose whole purpose is to learn by building, or when the user has asked for code now and understands it will be scaffolded. Say so and offer the lighter path.

## Non-negotiable principles

| # | Principle | Enforcement |
| --- | --- | --- |
| P1 | **Evidence before claims.** Never assert a version, endpoint, price, quota, licence, or benchmark from memory. Verify it against a primary source or mark it `unverified` in the document | A verification-status section in every research file |
| P2 | **Decisions are records, not prose.** Every load-bearing choice gets an ADR with context, decision, consequences, rejected alternatives, and how it will be verified | `references/decision-records.md` |
| P3 | **One fact, one place.** Decisions in ADRs, structure in ARCHITECTURE, behaviour in FLOWS, data in DATA_MODEL, work in TASKS. Link, never duplicate | A reviewer should be able to delete any duplicated paragraph and lose nothing |
| P4 | **Numbers are derived, not asserted.** Task counts, effort, budgets, and dataset sizes come from a script or a measurement | `scripts/backlog-stats.py`; reconcile every total across the corpus |
| P5 | **Scope is tiered and honestly priced.** Core, full quality bar, and post-1.0 roadmap are separate totals with a stated calendar conversion and contingency | Never present one number as "the estimate" |
| P6 | **Cross-cutting concerns get a seam on day one.** Content gating, accounts, observability, i18n, accessibility, permissions: define the interface in 1.0 even if the feature is later, because retrofitting through a finished read path is the expensive version | A named task in the early phase, and a stated reason in its ADR |
| P7 | **Limitations are stated in the product.** "What we refuse" tables, accepted-risk rows, best-effort labels, degraded-mode documents. No silent gaps | A limitations section in README and SECURITY |
| P8 | **Unknowns become time-boxed spikes.** Anything that could invalidate a decision gets an ID, a question, a time box, and the decision it unblocks | A spike table, referenced by the ADRs it can overturn |
| P9 | **Docs are machine-checked.** Links resolve, fences balance, diagrams parse, schemas validate, invariants map to tests, tasks have IDs and acceptance criteria | `scripts/check-docs.py` plus the structural rules in `references/artifacts.md` |
| P10 | **Ask before big work.** Lock the three to five decisions that will appear in every document with the user first; asking costs one round trip, guessing costs the corpus | A decision question before writing |

## The process

### Phase 0 — Recon (minutes, not hours)

Before writing anything: current directory and repo state, whether a git repo exists, available toolchain and versions, disk and network reachability of the sources you will need, and any existing conventions in the tree. Gate: you know what you are building on and what you cannot do here.

### Phase 1 — Lock the load-bearing decisions

Identify the three to five choices that will appear in every file — platform or shell, language, runtime, storage, distribution, and the working name. Ask the user with options, one-line trade-offs, and a recommendation first. Gate: no document names a stack that was not agreed. Renaming later is cheap only if the name was never written into fifty files.

### Phase 2 — Evidence, in parallel with the anchor document

Dispatch research as parallel subagents, one per domain, each with the strict brief in `references/research-briefs.md`. While they run, write the anchor document (ARCHITECTURE) yourself: it needs your judgement and the research will refine it.

Ask for evidence, not summaries. A brief that says "research X" returns prose; a brief that says "resolve every crate against crates.io with a User-Agent, give the licence you read, and list what you could not verify" returns something you can build on. Gate: every external fact is cited or marked unverified.

### Phase 3 — Write the corpus in dependency order

ARCHITECTURE first (structure and the module map), then DATA_MODEL, FLOWS, TECH_STACK and DEPENDENCIES, PLAN, TASKS, DESIGN_SYSTEM, SECURITY, AGENTS.md, README. Write ADRs as decisions happen, not as a retrospective. Per-file required sections and prohibitions: `references/artifacts.md`.

### Phase 4 — Self-correct against the evidence

Research will contradict something you wrote. When it does:

1. Fix the document that owns the fact.
2. If it was a **recorded decision**, do not edit history: write a superseding ADR and add `Superseded in part by ADR n` to the original.
3. Tell the user which of your own claims turned out wrong, and what changed. This is the highest-value part of the whole exercise and should never be quietly dropped.

### Phase 5 — Reconcile the numbers

Run `scripts/backlog-stats.py`. Then grep the corpus for every stale figure and fix it — totals appear in PLAN, TASKS, README, and often an ADR. Re-derive after **every** scope change, including ones the user adds late; a plan whose totals disagree with its own backlog is worse than no estimate.

### Phase 6 — Machine-check

Run `scripts/check-docs.py`. It validates relative links, **anchor fragments**, code-fence parity, and diagram openers; ambiguous anchors and repeated headings are warnings, not failures, because structured repetition (one block per subject) is legitimate.

If a checker is noisy about legitimate structure, fix the checker rather than the corpus, and if it misses something you had to eyeball, add the check — the tooling is the part of this process that survives.

Then confirm by inspection: every invariant names a test, every task has an ID, acceptance criteria, dependencies, and an estimate, every phase has exit criteria, every ADR has rejected alternatives and a verification path, every risk has a mitigation and a trigger.

### Phase 7 — Handover

AGENTS.md rules, the spike table, roadmap tiers, refused-scope tables, and a presentation of the one or two artifacts that matter most. State what you need from the user next and what you deliberately did not do.

## Artifact division of labour

| File | Question it answers | Must not contain |
| --- | --- | --- |
| README | What is this, is it for me, how do I run it, what is the legal position | Architecture detail; roadmap phase detail beyond a table |
| ARCHITECTURE | How the system is structured and why; module map, contracts, budgets, platform matrix, spikes | Schema DDL; step-by-step flows; a decision's rejected alternatives |
| DATA_MODEL | What is stored, with what invariants, indices, retention, migration policy | Business rules that live in code; provider detail |
| FLOWS | What happens over time, including failure paths and state machines | Data definitions; UI styling |
| TECH_STACK | Why each technology, and what it beat | Pinned versions |
| DEPENDENCIES | Exact verified versions, licences, obligations, update policy | Rationale essays |
| PLAN | Phases, exit criteria, effort model, risk register, release checklist, deferred work | Individual tasks |
| TASKS | Granular work with IDs, acceptance criteria, dependencies, estimates, critical path | Rationale for architecture |
| DESIGN_SYSTEM | Tokens, motion, components, theming, accessibility | Implementation code |
| SECURITY | Threat catalogue, controls, accepted risks, reporting policy | Feature roadmap |
| AGENTS.md | Numbered rules that bind every change, human or agent | Tutorial prose |
| ADRs | One decision each, with alternatives and verification | Anything that is not a decision |
| research/ | Evidence snapshots with verification status | Recommendations the design has not adopted yet |

Full templates: `references/artifacts.md`.

## Estimation protocol

- Label each task `XS` 0.5d, `S` 1d, `M` 2.5d, `L` 4.5d, `XL` 8d; split anything larger than five ideal days before starting it.
- Sum with a script, per epic and per tier. Never hand-count.
- Three tiers, always: **core** (usable and shippable), **full quality bar** (every gate, every platform), **post-1.0 roadmap** (committed but excluded from 1.0 totals). Quote all three.
- Add contingency explicitly (a stated percentage, not a feeling) and give a calendar conversion with its assumption written down: effective days per person-year, then a table for one, two, and three people.
- Compare the result against reality: lines of code for comparable systems, or a known project's timeline. If your number is an order of magnitude off either way, you have mislabelled your tasks.
- Re-baseline after the first phase with measured velocity rather than defending the original number.

## Self-review before declaring done

1. Recon done, decisions locked with the user, name fixed.
2. Every external fact cited or marked unverified; every licence read from a primary source.
3. Every load-bearing decision has an ADR with rejected alternatives.
4. No fact duplicated across files; each document answers only its own question.
5. Every invariant is numbered and names its test; every task has ID, acceptance criteria, dependencies, estimate.
6. Totals derived by script, reconciled everywhere they appear, tiered, with a calendar model.
7. Cross-cutting seams present in 1.0 even where the feature is later.
8. Limitations, refusals, and accepted risks written down.
9. Spikes listed with questions, time boxes, and the decision each unblocks.
10. `check-docs.py` clean; `backlog-stats.py` matches the quoted totals.
11. Corrections to your own earlier claims reported to the user.

## Anti-patterns this skill exists to prevent

- Versions, quotas, endpoint shapes, or licences recalled from memory and written as fact.
- One enormous document instead of a corpus with a division of labour, so every reader loads everything.
- A single effort number with no tiers, no contingency, and no calendar assumption.
- Tasks without acceptance criteria, which are wishes rather than work.
- Cross-cutting concerns deferred, then retrofitted through a finished read path.
- Security or parental controls implemented in the UI layer, where they are a filter rather than a boundary.
- Decisions changed silently in a document instead of superseded in a record.
- Limitations discovered by the user in production because nobody wrote them down.
- Documents that cannot be checked, so drift is inevitable.

## Supporting files

- `references/artifacts.md` — the corpus, per-file templates, task and phase conventions.
- `references/decision-records.md` — ADR template, supersession protocol, invariant, threat, and refusal registries.
- `references/research-briefs.md` — the evidence-first research protocol and copy-paste briefs.
- `scripts/check-docs.py` — links, anchor fragments, code fences, diagram blocks.
- `scripts/backlog-stats.py` — task counts, effort roll-up, tier totals.
