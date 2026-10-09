# Artifact templates

Required sections per document. A section that does not apply is deleted, not left as a heading with "N/A" under it.

## ARCHITECTURE

1. Scope, and explicit **non-goals** with a reason each (a non-goal someone disagrees with is a decision waiting to happen).
2. Design principles, numbered, each with how it is *enforced* (a test, a lint, a check) rather than how it is intended.
3. System context: who and what the system talks to, as a diagram plus a trust-boundary table.
4. Container and process view: what runs, where, in which language, with the lifetime of each part.
5. Module map: crate or package graph, one row per module with responsibility, allowed dependencies, and hard rules.
6. Frontend architecture: routing, state ownership, and the rules that keep it fast.
7. Contracts between layers: the command and event surface, the error model, payload limits, versioning.
8. Data model summary (pointer to DATA_MODEL).
9. Pointers to the flows (pointer to FLOWS) with the constraint each imposes.
10. Concurrency and resource model: pools, budgets, backpressure, cancellation.
11. Caching: tiers, lifetimes, what may be dropped without loss.
12. Security architecture: controls per boundary, pointer to SECURITY.
13. Extensibility: the ports, what a new adapter must implement, what is explicitly not extensible.
14. Performance architecture: budgets with the gate that enforces each.
15. Degradation and error model: a behaviour per failure mode.
16. Observability.
17. Cross-platform or cross-environment matrix, including known gaps stated plainly.
18. Packaging, distribution, updates.
19. Testing architecture: what is tested at which layer, and the fixture policy.
20. Repository layout.
21. Open spikes, each with a question, time box, and the decision it unblocks.

## DATA_MODEL

1. Conventions (naming, units, types, enum representation).
2. Entity relationship diagram.
3. Schema, grouped by area, as DDL, with the reasoning behind the non-obvious choices as prose beside it.
4. Invariants, numbered `I1..In`, each with the mechanism that enforces it and the test that proves it. This table is the contract between the schema and the code.
5. The queries the schema is shaped for, with expected costs.
6. Migration policy: append-only, fixture upgrades, expand-contract for breaking changes, backup, pragmas.
7. Retention and maintenance per table.
8. Disk accounting model with real numbers.

## FLOWS

One section per flow, each with: a numbered sequence diagram; the invariants the flow must preserve; the failure paths; and the tests that prove it, including the boundary cases.
Then the state machines, each with its terminal states and the guarantees at each transition.

## TECH_STACK

One row per layer: the choice, the rejected alternatives, and the decisive reason. Then sections for the layers where the trade-off is subtle, an explicit "what this stack costs us" list, and the version and upgrade policy.

## DEPENDENCIES

1. Version policy (ranges vs exact pins, MSRV, lockfiles, update cadence).
2. Runtime dependencies, grouped by function, with version, licence, and purpose.
3. Deliberately **not** used, with the reason and what is used instead. This table prevents the same argument twice.
4. Development and CI tools.
5. Bundled or redistributed components, with the obligations.
6. Licence obligations for statically linked dependencies.
7. Known risks and unverified items.

## PLAN

1. Delivery strategy: the four or five rules that govern ordering (walking skeleton, vertical slices, contract before adapter, risk first).
2. Phases: for each, a deliverable table, exit criteria written as observable facts, and its effort.
3. Milestone dependency rationale: why each thing cannot move earlier or later.
4. Effort model: tiered totals, contingency, calendar conversion with its assumption, what actually shrinks the number, and a re-baseline instruction.
5. Risk register: risk, likelihood, impact, mitigation, and an early-warning trigger.
6. Release checklist: the gates that must pass to ship.
7. Deliberately deferred list, with the prerequisite for revisiting each.
8. Definition of done, per task.
9. Development metrics worth watching.

## TASKS

- Task IDs, stable forever, never renumbered: `<PREFIX>-E<epic>-<nn>`.
- One row per task: ID, task, acceptance criteria, dependencies, estimate, and platform where relevant.
- Acceptance criteria must be observable and testable, not "works well".
- Every task implicitly includes its tests, error handling, logging, and documentation updates, stated once at the top.
- Epics have a one-line purpose. Phases have exit criteria in PLAN, not repeated here.
- A critical-path graph, and a roll-up table derived by script.
- Post-1.0 roadmap work is separated and excluded from the 1.0 totals.

## DESIGN_SYSTEM

Brand and mark rules; colour tokens with contrast requirements and how they are validated; typography per platform; space, shape, elevation; motion tokens with the rules for using them; component inventory with required behaviour; theming and the theme file format; platform adaptation obligations; iconography; accessibility requirements; asset pipeline and validation. Close with the specific rules that keep the interface from feeling like a web page, as review-blocking items.

## SECURITY

Reporting policy and supported versions; assets; trust boundaries; a threat catalogue with numbered threats `T1..Tn`, each with its control; controls by area; **accepted risks**, each with the reason it is accepted and the compensating measure; what is rejected by design; the release security checklist.

## AGENTS.md

Numbered rules `R1..Rn`, grouped: quality, architecture, testing, documentation, security, process. Each rule must be checkable by a reviewer. Add: repository layout, the command list, a mechanical edge-case checklist, code standards per language, performance discipline, how agents should work, and the review checklist. Rules are binding on humans and agents alike.
