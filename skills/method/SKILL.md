---
name: method
description: The Solution Architect operating method — journey, gates, execution protocol, standards library and artifact templates. Read this before running any other sa skill. Use when the user asks how the SA process works, which step comes next, what standard applies, or wants an overview of the architecture method.
---

# SA Method

The shared contract for every `sa` skill. Read this file, then the step standard, before producing anything.

## The journey

```
init → intake → drivers → impact → adr → hld → flow → lld → interface
                                     ↘ data · security · observability · resilience ↙
                                                  risk → review → handoff → trace
```

Data, security, observability and resilience run **in parallel** with hld/flow/lld/interface — not after them. Designing them last is the most common source of rework.

| Skill | Step | Question it answers |
|---|---|---|
| `init` | 0 | Where do architecture artifacts live? |
| `intake` | 1 | What problem, for whom, inside what boundary? |
| `drivers` | 2 | What must be true for this to be a *good* solution? |
| `impact` | 3 | What already exists and what does this disturb? |
| `adr` | 4 | Which options did we choose, and why? |
| `hld` | 5 | What are the parts and how are they arranged? |
| `flow` | 6 | How does it behave at runtime? |
| `lld` | 7 | How is each part built inside? |
| `interface` | 8 | What is the contract between parts? |
| `data` | 9 | Who owns which data, and for how long? |
| `security` | 10 | How can this be attacked, and what stops it? |
| `observability` | 11 | How will we know it is working? |
| `resilience` | 12 | What happens when a part fails? |
| `risk` | 13 | What might still go wrong? |
| `review` | 14 | Is this design fit to build? |
| `handoff` | 15 | Can a team start on Monday? |
| `trace` | 16 | Why does this line of design exist? |

Full definition, dependency graph and gates: `standards/00-sa-journey.md`.

## Read order (every skill, every time)

1. `sa-config.yaml` at the repo root. Absent → tell the user to run the `init` skill.
2. `standards/01-workflow-protocol.md` — the nine execution phases, mandatory.
3. The step standard named in that skill's metadata table.
4. The upstream artifacts the skill declares as inputs.

Never generate an artifact before its declared inputs have been read.

## Execution protocol (summary — full text in standard 01)

`P1 resolve args → P2 load standards → P3 load inputs → P4 detect mode → P5 gate check → P6 Change Summary → P7 STOP for confirmation → P8 write + log → P9 report + checklist`

## Gates

| Gate | Before | Passes when |
|---|---|---|
| G1 | `impact` | scope has a non-empty out-of-scope list, stakeholders named, ≥1 measurable scenario per high-priority attribute |
| G2 | `lld` | ≥1 Accepted ADR on the primary structural decision; HLD exists and agrees with it |
| G3 | `handoff` | every component has an LLD and an interface spec; every flow references only existing components |
| G4 | implementation | review verdict READY with no open blockers; every High risk mitigated or formally accepted |

Gates are the only hard stops. Everything else warns. An overridden gate is recorded as an accepted risk naming the person who overrode it.

## Hard rules

- **Never write a file before the user confirms the Change Summary.**
- **Never invent facts to fill a template.** Unknowns become OPEN items with an owner and a date.
- **Never silently drop content on update.** Edit in place, append to changelogs, mark removals deprecated.
- **Never touch artifacts outside `docs/architecture/`.**
- **Every artifact carries a trace-id** propagated from origin — copy forward, never reissue.
- **Assumption ≠ requirement.** Assumptions are labelled and, if risky, pushed to the risk register.
- **When blocked, stop:** state the missing input, who owns it, and the assumption you would otherwise have to make.

## Writing style for artifacts

Decision first, rationale second, alternatives third. Tables over prose wherever content is enumerable. Concrete numbers over adjectives — "p99 < 300 ms at 500 rps", never "fast". No filler, no restating headings as content.

## Reference library

| Path | Contents |
|---|---|
| `standards/00-sa-journey.md` | journey, dependency graph, gates, anti-patterns |
| `standards/01-workflow-protocol.md` | the nine execution phases, header block, log format |
| `standards/02`–`16` | one standard per journey step, each ending in its `## Checklist` |
| `standards/17-traceability-and-change.md` | trace ids, change classification, staleness propagation |
| `standards/18-diagram-conventions.md` | C4 usage, PlantUML rules, sequence and data diagram rules |
| `standards/19-naming-and-structure.md` | repository layout, naming, versioning, status lifecycle |
| `standards/20-quality-bar.md` | definition of done per artifact type |
| `templates/` | one skeleton per artifact — copy, do not improvise structure |
