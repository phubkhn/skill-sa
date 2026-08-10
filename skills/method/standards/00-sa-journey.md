# Standard 00 — The SA Journey

The journey is the same regardless of domain, industry, or technology. Only the *content* of each artifact changes.

## Canonical skill names

This table is the **single source of truth** for skill names. No other file may name a skill that is not in this table, and no other file may spell one differently.

| Skill | Journey step | Primary artifact | Standard |
|---|---|---|---|
| `sa:init` | 0 | `sa-config.yaml` + scaffold | 19 |
| `sa:intake` | 1 | `00-context/sa-intent.md` | 02 |
| `sa:drivers` | 2 | `00-context/architecture-drivers.md` | 03 |
| `sa:impact` | 3 | `01-analysis/impact-analysis.md` | 04 |
| `sa:options` | 3b | `01-analysis/solution-options.md` | 25 |
| `sa:adr` | 4 | `02-decisions/ADR-NNNN-*.md` | 05 |
| `sa:hld` | 5 | `03-hld/*.puml` + catalogues | 06, 18, 22 |
| `sa:flow` | 6 | `04-flows/*.puml` + narrative | 07, 18 |
| `sa:lld` | 7 | `05-lld/<component>.yaml` | 08 |
| `sa:interface` | 8 | `06-interfaces/*.yaml` | 09 |
| `sa:data` | 9 | `07-data/*` | 10 |
| `sa:security` | 10 | `08-crosscutting/security-design.md` | 11 |
| `sa:resilience` | 11 | `08-crosscutting/resilience-design.md` | 13 |
| `sa:observability` | 12 | `08-crosscutting/observability-design.md` | 12 |
| `sa:cost` | 13 | `01-analysis/cost-model.md` | 23 |
| `sa:risk` | 14 | `01-analysis/risk-register.md` | 14 |
| `sa:review` | 15 | `09-review/design-review-<date>.md` | 15, 20 |
| `sa:handoff` | 16 | `10-handoff/dev-handoff-<date>.md` | 16, 24 |
| `sa:trace` | 17 | `_logs/.trace-index.md` | 17 |

Outside a plugin install the `sa:` namespace is absent; the skill is then addressed by its bare name (`intake`, `hld`, …). The bare name after the colon never changes.

## Phases

| # | Phase | Question it answers | Primary artifact | Standard |
|---|---|---|---|---|
| 0 | Init | Where do architecture artifacts live? | `sa-config.yaml` + scaffold | 19 |
| 1 | Intake | What problem, for whom, inside what boundary? | `sa-intent.md` | 02 |
| 2 | Drivers | What must be true for this to be a *good* solution? | `architecture-drivers.md` | 03 |
| 3 | Impact | What already exists and what does this disturb? | `impact-analysis.md` | 04 |
| 3b | Options | Which whole-solution shapes did we compare? | `solution-options.md` | 25 |
| 4 | Decisions | Which options did we choose and why? | `ADR-NNNN-*.md` | 05 |
| 5 | HLD | What are the parts and how are they arranged? | context / container / component / deployment views | 06, 22 |
| 6 | Flows | How does it behave at runtime? | sequence diagrams | 07 |
| 7 | LLD | How is each part built inside? | `<component>.yaml` | 08 |
| 8 | Interfaces | What is the contract between parts? | OpenAPI / AsyncAPI / schema | 09 |
| 9 | Data | Who owns which data, and for how long? | data design + migration plan | 10 |
| 10 | Security | How can this be attacked, and what stops it? | threat model + controls | 11 |
| 11 | Resilience | What happens when a part fails? | failure modes + capacity | 13 |
| 12 | Observability | How will we know it is working? | signals + SLOs | 12 |
| 13 | Cost | What does this cost to build and to run? | cost model | 23 |
| 14 | Risk | What might still go wrong? | risk register + trade-off log | 14 |
| 15 | Review | Is this design fit to build? | design review report | 15 |
| 16 | Handoff | Can a team start on Monday? | dev handoff package | 16 |
| 17 | Trace | Why does this line of design exist? | traceability report | 17 |

**Resilience precedes observability.** Failure modes must exist before signals can be designed to detect them. This ordering is deliberate; do not restore the alphabetical/old order.

## Dependency graph

```
intake ──> drivers ──> impact ──> options ──> adr ──┬──> hld ──> flow ──> lld ──> interface
                                                    │            ↑                  │
                                                    ├──> data ───┴──────────────────┤
                                                    ├──> security ──────────────────┤
                                                    ├──> resilience ──> observability
                                                    └──> cost ──────────────────────┤
                                                                                    │
                                                    risk <───────────────────────────┘
                                                              │
                                                           review ──> handoff ──> trace
```

Phases 9–13 (data, security, resilience, observability, cost) run **in parallel** with 5–8, not after them. Designing them last is the single most common cause of rework.

## Two-pass rule (resolving the circular inputs)

Three pairs of steps legitimately need each other's output. Each pair has a designated **seed** and a designated **authority**. The seed guesses; the authority decides; the seed is then re-run in Update mode.

| Pair | Seed (runs first, may be provisional) | Authority (decides) | After the authority runs |
|---|---|---|---|
| `lld` ↔ `data` | `lld` declares provisional `owns` / `references` | `data` fixes the single owner per entity | re-run `lld` in Update mode; any conflict is an ADR, not a silent edit |
| `flow` ↔ `resilience` | `flow` declares provisional timeouts and retries | `resilience` sets the nested timeout budget | re-run `flow` in Update mode |
| `resilience` ↔ `observability` | none — strict order | `resilience` produces failure modes; `observability` consumes them | no second pass needed |

A seed artifact whose authority has since run and disagrees with it is **stale** (Standard 17), and `sa:review` reports it as a Major finding.

## Gates

A gate is a hard stop. Everything else in this skill set is a warning.

| Gate | Position | Passes when |
|---|---|---|
| **G1 — Problem understood** | before `sa:impact` | intent has a scope with a **non-empty out-of-scope list** and named stakeholders; drivers has ≥1 measurable scenario for every attribute in the **H/H quadrant** (high business importance × high architectural difficulty) |
| **G2 — Design baseline** | before `sa:lld` | at least one `Accepted` ADR covering the primary structural decision; HLD context + container views exist and agree with that ADR |
| **G3 — Contract frozen** | before `sa:handoff` | every HLD component has an LLD, **and** an interface spec **or** an `N/A — <reason>` entry in the element catalogue; every flow references only components that exist in the HLD |
| **G4 — Fit to build** | before implementation starts | latest `sa:review` verdict is `READY` (or `READY WITH CONDITIONS` with every condition closed); every risk rated High has a mitigation or an explicit acceptance with a named accepter |

**G1 is defined once, here, as H/H.** Any other file stating a different threshold is wrong.

**Interface spec `N/A` is legitimate** for elements that expose no programmatic contract: data stores, CDNs, UI shells with no public API, and third-party systems outside the build. The reason must be written in the element catalogue, not assumed.

A gate failure is reported, not worked around. If the user chooses to proceed anyway, record it as an accepted risk in the risk register with the user named as the accepting party. Gates disabled in `sa-config.yaml` (`gates: {G2: false}`) are skipped, but skipping still writes the accepted risk — a disabled gate is a decision, not an absence.

## Iteration

The journey is not waterfall. On any change:

1. Re-run `sa:intake` (or edit intent) — the change starts there or it isn't real.
2. Re-run `sa:impact` — it tells you which downstream artifacts became stale.
3. Re-run only the stale artifacts. `impact-analysis.md` is the authority on what is stale, not memory.
4. Re-run `sa:review` before re-handoff.

## Anti-patterns this journey exists to prevent

| Anti-pattern | Where it gets caught |
|---|---|
| Diagram with no decision behind it | G2, review §Decisions |
| "Non-functionals to be confirmed later" | G1, drivers standard |
| One option presented as if it were the only one | `sa:options`, ADR standard rule 2 |
| Component with no owner of its data | data standard, review §Ownership |
| Contract designed after implementation started | G3 |
| Failure behaviour unspecified | resilience standard, review §Resilience |
| Design that can't be observed in production | observability standard, review §Observability |
| A design nobody costed | cost standard, review §Cost |
| Untraceable requirement drift | traceability standard, `sa:trace` |
| Full 17-step ceremony on a two-week change | tailoring standard 21 |
