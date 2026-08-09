# Standard 04 — Impact Analysis

**Artifact:** `01-analysis/impact-analysis.md`
**Purpose:** state what already exists, what this change disturbs, and what is now stale.

## Required sections

| Section | Content |
|---|---|
| Baseline | the current-state architecture relevant to this change — components, integrations, data stores, contracts |
| Impacted elements | table below; one row per element, **including elements verified as unaffected** |
| New elements required | components, interfaces, data stores, infrastructure that do not yet exist |
| Contract impact | every interface whose consumers are affected, with breaking/non-breaking classification |
| Data impact | schema changes, migrations, backfills, retention changes |
| Operational impact | deployment, runbooks, monitoring, on-call, capacity, cost |
| Organisational impact | which teams must do work; cross-team dependencies |
| Stale artifacts | existing design documents invalidated by this change |
| Effort & sequencing | rough size per element and the order constraints between them |
| Risk summary | pointer to risk register entries created by this analysis |

## Impacted element table

| Element | Type | Impact | Nature of change | Breaking? | Owner team | Effort | Trace ID |
|---|---|---|---|---|---|---|---|
| `order-service` | component | Change | new endpoint + new event | No | Payments | M | TR-x-004 |
| `legacy-batch` | component | None (verified) | checked: no shared data path | — | Ops | — | TR-x-004 |

**Impact values:** `Add` · `Change` · `Remove` · `None (verified)` · `Unknown (investigate)`

## Rules

1. **"Verified no impact" must be written down.** Absence from the table is not evidence of absence of impact — it is evidence you didn't look.
2. **Breaking changes are classified against consumers, not against the code.** A field addition is breaking if a consumer validates strictly.
3. **Unknowns are first-class.** `Unknown (investigate)` with an owner is a valid row; a confident guess is not.
4. **Blast radius before effort.** Estimate what could break before estimating how long it takes.
5. **Every removal needs a decommissioning path** — who calls it today, how they stop, when it is switched off.
6. **Stale artifacts are named with paths**, so the SA can re-run exactly those steps.

## Blast radius heuristic

For each impacted element, walk one hop outward: who calls it, who it calls, who reads its data, who consumes its events, who deploys with it. Stop when a hop yields no new element. Anything reached is in the table.

## Anti-patterns

- An impact analysis that lists only what the team already planned to change
- Effort estimates without sequencing constraints (parallelisable vs strictly ordered)
- No mention of rollback

## Checklist

Self-assess against this list before reporting the artifact done. Report pass/fail **per item** — never a silent pass. A failed item becomes an OPEN item with an owner; it is not deleted to make the list pass.

- [ ] Baseline states the source of current-state knowledge
- [ ] Blast-radius walk performed to a hop that added nothing new
- [ ] Elements verified as unaffected are listed explicitly with evidence
- [ ] Every impacted row has impact type, nature, owner team, effort
- [ ] Breaking changes classified per named consumer, not per schema
- [ ] Data impact includes migration need and reversibility
- [ ] Operational impact covers deploy, monitoring, on-call, capacity, cost
- [ ] Organisational impact names the teams and the sequencing constraints
- [ ] Stale artifacts listed by path with the refresh command
- [ ] Every removal has a decommissioning path
- [ ] Rollback considered
- [ ] Unknowns recorded as `Unknown (investigate)` with owner, not guessed
- [ ] Candidate risks emitted to the risk register
