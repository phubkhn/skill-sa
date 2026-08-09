# Standard 00 — The SA Journey

The journey is the same regardless of domain, industry, or technology. Only the *content* of each artifact changes.

## Phases

| # | Phase | Question it answers | Primary artifact | Standard |
|---|---|---|---|---|
| 0 | Init | Where do architecture artifacts live? | `sa-config.yaml` + scaffold | 19 |
| 1 | Intake | What problem, for whom, inside what boundary? | `sa-intent.md` | 02 |
| 2 | Drivers | What must be true for this to be a *good* solution? | `architecture-drivers.md` | 03 |
| 3 | Impact | What already exists and what does this disturb? | `impact-analysis.md` | 04 |
| 4 | Decisions | Which options did we choose and why? | `ADR-NNNN-*.md` | 05 |
| 5 | HLD | What are the parts and how are they arranged? | context / container / component views | 06 |
| 6 | Flows | How does it behave at runtime? | sequence diagrams | 07 |
| 7 | LLD | How is each part built inside? | `<component>.yaml` | 08 |
| 8 | Interfaces | What is the contract between parts? | OpenAPI / AsyncAPI / schema | 09 |
| 9 | Data | Who owns which data, and for how long? | data model + migration plan | 10 |
| 10 | Security | How can this be attacked, and what stops it? | threat model + controls | 11 |
| 11 | Observability | How will we know it is working? | signals + SLOs | 12 |
| 12 | Resilience | What happens when a part fails? | failure modes + capacity | 13 |
| 13 | Risk | What might still go wrong? | risk register + trade-off log | 14 |
| 14 | Review | Is this design fit to build? | design review report | 15 |
| 15 | Handoff | Can a team start on Monday? | dev handoff package | 16 |
| 16 | Trace | Why does this line of design exist? | traceability report | 17 |

## Dependency graph

```
intake ──> drivers ──> impact ──> adr ──┬──> hld ──> flow ──> lld ──> interface
                                        │                              │
                                        ├──> data ─────────────────────┤
                                        ├──> security ─────────────────┤
                                        ├──> observability ────────────┤
                                        └──> resilience ───────────────┘
                                                                       │
                                        risk <──────────────────────────┘
                                                       │
                                                    review ──> handoff
```

Phases 9–12 (data, security, observability, resilience) run **in parallel** with 5–8, not after them. Designing them last is the single most common cause of rework.

## Gates

A gate is a hard stop. Everything else in this skill set is a warning.

| Gate | Position | Passes when |
|---|---|---|
| **G1 — Problem understood** | before `gen-impact-analysis` | intent has scope + at least one in/out-of-scope boundary + named stakeholders; drivers has ≥1 measurable scenario per prioritised quality attribute |
| **G2 — Design baseline** | before `gen-lld` | at least one accepted ADR covering the primary structural decision; HLD context + container views exist and match the ADR |
| **G3 — Contract frozen** | before `gen-handoff` | every component in HLD has an LLD and an interface spec; every flow references only components that exist in HLD |
| **G4 — Fit to build** | before implementation starts | `review-design` verdict is `READY` with zero open blockers; every risk rated High has a mitigation or an explicit acceptance with an owner |

A gate failure is reported, not worked around. If the user chooses to proceed anyway, record it as an accepted risk in the risk register with the user named as the accepting party.

## Iteration

The journey is not waterfall. On any change:

1. Re-run `intake` (or edit intent) — the change starts there or it isn't real.
2. Re-run `impact` — it tells you which downstream artifacts became stale.
3. Re-run only the stale artifacts. `impact-analysis.md` is the authority on what is stale, not memory.
4. Re-run `review-design` before re-handoff.

## Anti-patterns this journey exists to prevent

| Anti-pattern | Where it gets caught |
|---|---|
| Diagram with no decision behind it | G2, review §Decisions |
| "Non-functionals to be confirmed later" | G1, drivers standard |
| Component with no owner of its data | data standard, review §Ownership |
| Contract designed after implementation started | G3 |
| Failure behaviour unspecified | resilience standard, review §Resilience |
| Design that can't be observed in production | observability standard, review §Observability |
| Untraceable requirement drift | traceability standard, `/sa:trace` |
