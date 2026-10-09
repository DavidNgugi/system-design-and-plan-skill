# Decision records, invariants, and refusal registries

## When to write an ADR

Write one when a choice is **load-bearing and contested**: it constrains other work, is expensive to reverse, or someone will reasonably ask "why not X?". Do not write one for a choice with an obvious answer or a local convention.

## ADR template

```markdown
# ADR NNNN — Title as a decision, not a topic

- **Status:** Accepted | Proposed (pending SPIKE-n) | Superseded by ADR nnnn
- **Date:** YYYY-MM-DD
- **Evidence:** the primary sources you actually read, with URLs, and the date
- **Verification:** the spike or test that will confirm it
- **Related:** neighbouring decisions

## Context
The forces. Facts, not preferences, and each with its source. State the constraint that makes
the decision necessary and the alternatives that exist.

## Decision
Numbered, imperative, specific. "Ship the ordinary GPL build as a separate executable" beats
"prefer permissive licensing". Include the rules that follow from the decision, because those
are what implementers actually obey.

## Consequences
Positive, then a genuinely negative list with mitigations. An ADR with no costs listed is a
sales pitch and will be trusted less, not more.

## Alternatives rejected
A table: alternative, and why it lost. Include the tempting one you rejected, with the reason —
that is the row a future maintainer will search for.

## Verification
The experiment or measurement that would prove the decision wrong, and what would replace it.
```

## Supersession protocol

1. A recorded decision never changes in place. Write a new ADR that states what it supersedes.
2. Add `Superseded in part by ADR nnnn` to the affected part of the original, naming the section.
3. Update every document that restated the old decision, and grep for its distinctive phrases — they hide in platform matrices, task rows, and the README.
4. Keep the correction visible: tell the reader what changed and why.

## Invariant registry

Invariants are the contract between the schema, the domain, and the tests. Number them `I1..In` and give each a mechanism and a proving test.

```
| # | Invariant | Enforced by |
| I1 | Exactly one external id row per (provider, value) | UNIQUE index |
| I2 | A suppressed notification always records why | CHECK constraint |
```

Rules: an invariant with no mechanism is a wish; an invariant with no test is documentation drift waiting to happen; a new invariant is added with the migration that enforces it.

## Threat catalogue

Numbered `T1..Tn`. Each row: the threat in one line, and the control. Then three things that are usually missing:

- **Accepted risks**, with the honest reason and the compensating measure. An empty accepted-risk table means nobody looked.
- **Rejected by design**, so that "why don't you just…" has an answer that predates the question.
- The **release checklist** that proves the controls still hold.

## Refusal tables

A short table of things the system will not do, each with a technical reason. This is the cheapest way to prevent scope drift, and it is where a plan earns credibility: "no, and here is why" is more useful than silence.

## Corrections log

Keep a running note of claims that research overturned, and report them to the user at the end of the work. A plan that was never wrong is a plan that never checked anything.
