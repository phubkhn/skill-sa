---
name: method
description: The Solution Architect operating method — journey, gates, execution protocol, standards library and artifact templates. Read this before running any other sa skill. Use when the user asks how the SA process works, which step comes next, what standard applies, or wants an overview of the architecture method.
allowed-tools: Read, Grep, Glob
---

# SA Method

The shared contract for every `sa` skill. Read this file, then the step standard, before producing anything.

## The journey

```
init → intake → drivers → impact → options → adr → hld → flow → lld → interface
                                                 ↘ data · security · resilience → observability · cost ↙
                                                            risk → review → handoff → trace
```

**This diagram is the full journey, not a mandatory sequence.** Which of these steps actually run is decided by the `profile` in `sa-config.yaml` (Standard 21) — a `light` change legitimately runs four of them. Reading this diagram as a to-do list is how the method gets abandoned.

Data, security, resilience, observability and cost run **in parallel** with hld/flow/lld/interface — not after them. Designing them last is the most common source of rework. Resilience runs **before** observability: you cannot design a signal for a failure mode that has not been written down yet.

| Skill | Step | Question it answers |
|---|---|---|
| `sa:init` | 0 | Where do architecture artifacts live? |
| `sa:intake` | 1 | What problem, for whom, inside what boundary? |
| `sa:drivers` | 2 | What must be true for this to be a *good* solution? |
| `sa:impact` | 3 | What already exists and what does this disturb? |
| `sa:options` | 3b | Which whole-solution shapes did we compare, and why this one? |
| `sa:adr` | 4 | Which options did we choose, and why? |
| `sa:hld` | 5 | What are the parts, how are they arranged, and where do they run? |
| `sa:flow` | 6 | How does it behave at runtime? |
| `sa:lld` | 7 | How is each part built inside? |
| `sa:interface` | 8 | What is the contract between parts? |
| `sa:data` | 9 | Who owns which data, and for how long? |
| `sa:security` | 10 | How can this be attacked, and what stops it? |
| `sa:resilience` | 11 | What happens when a part fails? |
| `sa:observability` | 12 | How will we know it is working? |
| `sa:cost` | 13 | What does this cost to build and to run? |
| `sa:risk` | 14 | What might still go wrong? |
| `sa:review` | 15 | Is this design fit to build? |
| `sa:handoff` | 16 | Can a team start on Monday? |
| `sa:trace` | 17 | Why does this line of design exist? |

Canonical skill names, full dependency graph, the two-pass rule and the gates: `standards/00-sa-journey.md`.

## Routing — which skill for which request

Match on what the user is asking for, not on which word they used. Several skills touch the same vocabulary; the right-hand column is what actually separates them.

| The user asks… | Skill | Not this, because… |
|---|---|---|
| "how available must this be / what's our SLO target" | `sa:drivers` | not `sa:resilience` — drivers *sets* the target, resilience *designs to* it |
| "what happens when X goes down" | `sa:resilience` | not `sa:drivers` — the target already exists; this is the failure design |
| "how will we know it broke" | `sa:observability` | not `sa:resilience` — resilience names the failure, observability detects it |
| "what are the components" | `sa:hld` | not `sa:lld` — inside one component is LLD |
| "how does a request move through it" | `sa:flow` | not `sa:hld` — static structure vs behaviour over time |
| "where does it run / which region / what network" | `sa:hld` (deployment view) | not `sa:resilience` — placement first, failure behaviour second |
| "who owns this data" | `sa:data` | not `sa:lld` — LLD *claims*, data design *decides* (two-pass rule) |
| "should we use A or B for this whole thing" | `sa:options` | not `sa:adr` — options compares solution shapes, ADR records one decision |
| "why did we choose A" | `sa:adr` | not `sa:options` — recording a decision, not making one |
| "what will this change break" | `sa:impact` | not `sa:review` — forward-looking blast radius vs judging a finished design |
| "is this design any good" | `sa:review` | not `sa:impact` — evidence-based verdict on what exists |
| "what could go wrong" | `sa:risk` | not `sa:review` — risk sweeps and owns; review judges and finds |
| "what does this cost" | `sa:cost` | needs the resilience capacity table first |
| "why does this component exist" | `sa:trace` | not `sa:adr` — trace follows the id, ADR holds the reasoning |
| "what's now out of date" | `sa:trace --stale` | not `sa:impact` — impact predicts staleness, trace detects it |
| "threat model this" | `sa:security` | not `sa:review` — review checks that security was done, it does not do it |

**Ambiguous requests.** If the request could be two skills, say which two and why, then ask — do not silently pick. Running the wrong step produces a plausible artifact in the wrong place, which is worse than a question.

**Requests that are not SA work at all.** Reviewing source code, writing SQL, debugging a running system, CI configuration, distributed tracing setup, generating `CLAUDE.md` — none of these are this skill set, even though the words overlap. Say so rather than producing an architecture document nobody asked for.

## Read order (every skill, every time)

1. `sa-config.yaml` at the repo root. Absent → tell the user to run `sa:init`.
2. `standards/01-workflow-protocol.md` — the nine execution phases, mandatory.
   `standards/26-operating-guardrails.md` — the write boundary and behavioural limits, mandatory.
3. `standards/21-tailoring.md` — whether this step is required at the configured profile.
4. The step standard named in that skill's metadata table.
5. The upstream artifacts the skill declares as inputs.

Never generate an artifact before its declared inputs have been read.

## Execution protocol (summary — full text in standard 01)

`P1 resolve args → P2 load standards + config → P3 load inputs → P4 detect mode → P5 gate check → P6 Change Summary → P7 STOP for confirmation → P8 write + log → P9 report + checklist`

## Gates

| Gate | Before | Passes when |
|---|---|---|
| G1 | `sa:impact` | scope has a non-empty out-of-scope list, stakeholders named, ≥1 measurable scenario per **H/H** attribute |
| G2 | `sa:lld` | ≥1 Accepted ADR on the primary structural decision; HLD exists and agrees with it |
| G3 | `sa:handoff` | every component has an LLD, and an interface spec or a written `N/A — <reason>`; every flow references only existing components |
| G4 | implementation | review verdict READY with no open blockers; every High risk mitigated or formally accepted |

Gates are the only hard stops. Everything else warns. An overridden **or config-disabled** gate is recorded as an accepted risk naming the person responsible.

## Hard rules

- **Never write a file before the user confirms the Change Summary.** This is the tool-call boundary — everything before it is a proposal, everything after it is a real change. Standard 26 governs it.
- **The Change Summary declares the exact file list**, and P9 flags any write that was not on it.
- **Never invent facts to fill a template.** Unknowns become OPEN items with an owner and a date.
- **Every claim about the existing system carries a source** — `path:line`, a named document, or a named person and date. Without one it is written as an Assumption, not a fact.
- **Never silently drop content on update.** Edit in place, append to changelogs, mark removals deprecated.
- **Never touch artifacts outside `<docs-root>`** (from `sa-config.yaml`; default `docs/architecture/`).
- **Every artifact carries a trace-id** propagated from origin — copy forward, never reissue.
- **Assumption ≠ requirement.** Assumptions are labelled and, if risky, pushed to the risk register.
- **Same inputs, same output.** Do not re-word or re-order sections no input touched.
- **A passed checklist is completeness, not verification.** The same reasoning wrote the artifact and ticked the list.
- **Never weaken a requirement or invent an input so a run can finish.** One corrective attempt, then escalate.
- **Artifact prose follows `language` in `sa-config.yaml`; identifiers stay English kebab-case.**
- **When blocked, stop:** state the missing input, who owns it, and the assumption you would otherwise have to make.

## Writing style for artifacts

Decision first, rationale second, alternatives third. Tables over prose wherever content is enumerable. Concrete numbers over adjectives — "p99 < 300 ms at 500 rps", never "fast". No filler, no restating headings as content.

## Reference library

| Path | Contents |
|---|---|
| `standards/00-sa-journey.md` | canonical skill names, journey, dependency graph, two-pass rule, gates, anti-patterns |
| `standards/01-workflow-protocol.md` | the nine execution phases, config honouring, header equivalence, log format |
| `standards/02`–`16` | one standard per journey step, each ending in its `## Checklist` |
| `standards/17-traceability-and-change.md` | trace ids, change classification, staleness propagation |
| `standards/18-diagram-conventions.md` | C4 usage, PlantUML rules, sequence and data diagram rules |
| `standards/19-naming-and-structure.md` | repository layout, naming, versioning, status lifecycle |
| `standards/20-quality-bar.md` | definition of done per artifact type |
| `standards/21-tailoring.md` | which artifacts are required at which project profile |
| `standards/22-deployment-view.md` | deployment / infrastructure view |
| `standards/23-cost-standard.md` | build and run cost model |
| `standards/24-verification-standard.md` | test strategy and fitness functions |
| `standards/25-options-standard.md` | whole-solution options comparison before ADRs |
| `standards/26-operating-guardrails.md` | how this skill set must behave: write boundary, scope declaration, tool permissions, independent verification, bounded recovery |
| `templates/` | one skeleton per artifact — copy, do not improvise structure |
| `../../examples/` | one worked end-to-end example; read it if unsure what "done" looks like |
