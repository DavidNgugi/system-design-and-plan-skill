# Evidence-first research protocol

## Rules for any research brief

1. **Primary sources only.** Registries, upstream source, official documentation, the standard itself. Not blog summaries, not recollection.
2. **Ask for the mechanism, not the conclusion.** "Where is sequential download implemented, in which file, and which library call does it make?" returns something verifiable; "does it support streaming?" returns an opinion.
3. **Demand explicit licences, read from the file.** Exact SPDX identifier and the URL you read it from.
4. **Require a verification-status section** listing what could not be verified and why. An honest gap is worth more than a plausible guess.
5. **Forbid invention.** State plainly: never invent a version, endpoint, field, or benchmark; mark it `unverified` instead.
6. **Bound the output.** A line target and "terse, cite URLs, no filler" keeps the result usable.
7. **One domain per agent**, and say which file to write to and to create nothing else.

## Brief template

```
You are researching <domain> for a new <kind of system>. Context: <two sentences on the stack and constraints>.

You have network access. Verify against primary sources: <registries, upstream source, official docs>.
If a lookup fails, say so explicitly instead of guessing.

Deliverable: exactly one file at <absolute path> (mkdir -p first).

For every <artifact>: the verified version or value, the licence read from its own file, the
maintenance signal, and a one-line verdict.

Special investigations, where the mechanism matters:
1. <question> — cite the file and the call.
2. <question> — state limits and failure modes.

Constraints: plain markdown, terse, tables where they help, every non-obvious claim carries a URL,
no emoji, no filler. End with a "Verification status" section listing what you could not verify.

Do not write any other file.
```

## Using the results

- Read the evidence yourself before adopting a conclusion; briefs are inputs, not verdicts.
- When a finding contradicts a written claim, fix the owning document and tell the user.
- Prefer the fact that changes a design decision over the fact that merely confirms one, and lead with it in your summary.
- Record the verification date in the ADR that depends on it; these facts rot.

## Common domains for a system plan

Reference implementations (what to steal, what to avoid, with licences); dependency and version matrix; external APIs and their real limits; platform conventions and design guidance; skills or tooling available; protocol specifications; pricing and quota reality; dataset sizes measured rather than estimated; security advisories and threat reports.
