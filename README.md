# skill-sa

A generic **Solution Architect** skill set for Claude Code and Cowork.
Domain-agnostic, vendor-agnostic, language-agnostic — it designs *systems*, not any particular business.

**17 skills** covering the full SA journey · **21 standards** defining what good looks like · **17 artifact templates** · **4 quality gates**.

---

## Install

### Option A — plugin marketplace (recommended)

```
/plugin marketplace add phubkhn/skill-sa
/plugin install sa@skill-sa
```

Skills then appear as `sa:intake`, `sa:hld`, `sa:review`, …

### Option B — drop-in, no install step

```bash
git clone https://github.com/phubkhn/skill-sa.git ~/.claude/skills/skill-sa
```

Claude Code discovers any folder under a skills directory that contains `.claude-plugin/plugin.json` and loads it on the next session as `skill-sa@skills-dir` — no marketplace, no install command. Use `~/.claude/skills/` for every project, or `<repo>/.claude/skills/` for one project.

### Option C — vendored into a project

```bash
git clone https://github.com/phubkhn/skill-sa.git .claude/skills/skill-sa
```

Commit it, and every teammate gets the same architecture method with the repository.

Verify with `/plugin` or `claude plugin list`.

---

## Quick start

```
sa:init            # scaffold docs/architecture + sa-config.yaml
sa:intake          # what problem, for whom, inside what boundary
sa:drivers         # measurable quality-attribute scenarios
sa:impact          # what this disturbs                        [gate G1]
sa:adr             # record the structural decisions
sa:hld             # C4 context / container / component
sa:flow            # runtime sequences, including failures
sa:lld             # per-component internals                   [gate G2]
sa:interface       # OpenAPI + AsyncAPI contracts
sa:data sa:security sa:observability sa:resilience   # in parallel with the above
sa:risk            # consolidated, owned risk register
sa:review          # evidence-based verdict
sa:handoff         # implementation-ready package              [gates G3, G4]
sa:trace           # why does this exist / what is now stale
```

Every generating skill stops for a **Change Summary** and writes nothing until you confirm.

---

## The journey

```
init → intake → drivers → impact → adr → hld → flow → lld → interface
                                     ↘ data · security · observability · resilience ↙
                                                  risk → review → handoff → trace
```

Data, security, observability and resilience run **in parallel** with the design steps, not after them.

| Skill | Produces | Standard |
|---|---|---|
| `init` | `sa-config.yaml`, `docs/architecture/**` | 19 |
| `intake` | `00-context/sa-intent.md` | 02 |
| `drivers` | `00-context/architecture-drivers.md` | 03 |
| `impact` | `01-analysis/impact-analysis.md` | 04 |
| `adr` | `02-decisions/ADR-NNNN-*.md` | 05 |
| `hld` | `03-hld/*.puml` + catalogues | 06, 18 |
| `flow` | `04-flows/*.puml` + narrative | 07, 18 |
| `lld` | `05-lld/<component>.yaml` | 08 |
| `interface` | `06-interfaces/*.yaml` | 09 |
| `data` | `07-data/*` | 10 |
| `security` | `08-crosscutting/security-design.md` | 11 |
| `observability` | `08-crosscutting/observability-design.md` | 12 |
| `resilience` | `08-crosscutting/resilience-design.md` | 13 |
| `risk` | `01-analysis/risk-register.md` | 14 |
| `review` | `09-review/design-review-<date>.md` | 15 |
| `handoff` | `10-handoff/dev-handoff-<date>.md` | 16 |
| `trace` | `_logs/.trace-index.md` + report | 17 |

---

## Skill reference — inputs and outputs

Paths are relative to `docs-root` in `sa-config.yaml` (default `docs/architecture/`).
Every generating skill also reads `skills/method/SKILL.md` + `standards/01-workflow-protocol.md`, appends to `_logs/.design-log`, and **stops for your confirmation before writing anything**. Those are omitted below to keep the tables readable.

### 0 · `init`

| | |
|---|---|
| **Argument** | optional scope slug, kebab-case (e.g. `checkout-revamp`) |
| **Reads** | existing `sa-config.yaml`, if any |
| **Asks you** | scope slug · docs root · diagram tool · contract formats · which optional steps are in play |
| **Writes** | `sa-config.yaml` (repo root) · the full `docs/architecture/**` tree · `_logs/.design-log` · `_logs/.trace-index.md` · `docs/architecture/README.md` |
| **Gate** | — |
| **Standard** | 19 (layout, naming, versioning), 00 (journey) |

### 1 · `intake`

| | |
|---|---|
| **Argument** | scope slug |
| **Reads** | whatever requirement sources you point at — tickets, notes, docs, transcripts; existing `sa-intent.md` on update |
| **Asks you** | 8 mandatory questions: what breaks today and what it costs · what is out of scope · who decides and who can veto · what already exists that this must live with · which constraints are imposed vs chosen · what "done well" looks like in 6 months · what was tried before and why it failed · the deadline and what drives it |
| **Writes** | `00-context/sa-intent.md` · `00-context/stakeholders.md` |
| **Gate** | — |
| **Standard** | 02 |
| **Refuses to** | put solution language in the problem statement · leave the out-of-scope list empty · invent an answer instead of logging an open question |

### 2 · `drivers`

| | |
|---|---|
| **Argument** | scope slug |
| **Reads** | `00-context/sa-intent.md` (concerns, constraints, success criteria) · existing ADRs, so settled numbers are not re-litigated |
| **Asks you** | any missing **measure** — the numbers behind each quality attribute; a forced ranking if more than 5 attributes land High/High |
| **Writes** | `00-context/architecture-drivers.md` — six-part scenarios, a full 18-attribute sweep, the priority matrix, the conflict list, the unknown-measure list |
| **Gate** | — |
| **Standard** | 03 |
| **Refuses to** | accept an attribute described only with adjectives · invent an SLO |

### 3 · `impact`

| | |
|---|---|
| **Argument** | scope slug |
| **Reads** | `00-context/sa-intent.md` · `00-context/architecture-drivers.md` · existing `03-hld/**`, `05-lld/**`, `06-interfaces/**` · your answer on where current-state knowledge lives if the repo has no docs |
| **Writes** | `01-analysis/impact-analysis.md` — baseline · impacted elements (including `None (verified)` rows) · new elements · contract/data/operational/organisational impact · **stale artifact list with the refresh command** · effort and sequencing · unknowns · candidate risks |
| **Gate** | **G1** — scope has a non-empty out-of-scope list, stakeholders named, ≥1 measurable scenario per High/High attribute |
| **Standard** | 04 |
| **Key behaviour** | blast-radius walk: one hop outward from each touched element — callers, callees, data readers, event consumers, co-deployed units — repeated until a hop adds nothing new |

### 4 · `adr`

| | |
|---|---|
| **Argument** | the decision in a few words; if omitted, it lists open decisions from the drivers' conflict list and the impact analysis' unknowns and asks which to record |
| **Reads** | `00-context/architecture-drivers.md` (the evaluation axes) · `01-analysis/impact-analysis.md` · **all existing ADRs**, to detect a decision already made or contradicted |
| **Asks you** | what alternative you rejected, if you offer only one option · whether the deciders have actually agreed (Proposed vs Accepted) |
| **Writes** | `02-decisions/ADR-NNNN-<slug>.md` · a row in `02-decisions/adr-index.md` · the status line of a superseded ADR |
| **Gate** | — |
| **Standard** | 05 |
| **Refuses to** | write an ADR with fewer than 2 genuine options · omit the negative consequences · bundle two decisions in one record |

### 5 · `hld`

| | |
|---|---|
| **Argument** | scope slug, optionally a view: `context` \| `container` \| `component <container>` (default: context + container) |
| **Reads** | `00-context/*` · `01-analysis/impact-analysis.md` · every **Accepted** ADR (a still-Proposed structural ADR is flagged) |
| **Writes** | `03-hld/system-context.puml` · `03-hld/container-<system>.puml` · `03-hld/component-<container>.puml` · element catalogue + relationship catalogue (incl. a filled **failure-behaviour** column) |
| **Gate** | — |
| **Standard** | 06, 18 |
| **Key behaviour** | runs 6 coupling checks before writing — sync fan-out > 3, > 5 round trips per user action, shared data store, container-level cycles, god component, orphan elements — and reports elements that trace to no driver |

### 6 · `flow`

| | |
|---|---|
| **Argument** | `<flow-name>`; if omitted it proposes the flow list from the selection criteria in standard 07 |
| **Reads** | `03-hld/*` element catalogue (participant names must match exactly) · `00-context/architecture-drivers.md` · `02-decisions/*` |
| **Writes** | `04-flows/<flow-name>.puml` · the narrative table (steps, timeouts, retries, idempotency, failure behaviour, emitted signals) |
| **Gate** | — |
| **Standard** | 07, 18 |
| **Refuses to** | use a participant absent from the HLD · leave a cross-boundary call without a timeout · show a retry on a non-idempotent operation · ship a flow with only a happy path |

### 7 · `lld`

| | |
|---|---|
| **Argument** | `<component>`; if omitted it lists HLD containers that have no LLD yet |
| **Reads** | `03-hld/*` (this component's catalogue rows) · every `04-flows/*` it participates in · `07-data/*` ownership rows · `02-decisions/*` · `00-context/architecture-drivers.md` |
| **Writes** | `05-lld/<component>.yaml` — responsibilities · **non-responsibilities** · provides/consumes · owns vs references data · state machines · concurrency and idempotency · configuration · failure modes · constraints · changelog |
| **Gate** | **G2** — ≥1 Accepted ADR on the primary structural decision, and the HLD agrees with it |
| **Standard** | 08 |
| **Refuses to** | leave a consumed dependency without reason, failure-behaviour and timeout · leave an orphan responsibility or an unowned operation |

### 8 · `interface`

| | |
|---|---|
| **Argument** | `<component>` and optionally `sync` \| `async` \| `both` (default both) |
| **Reads** | `05-lld/<component>.yaml` (`provides` is the authority on what exists) · `04-flows/*` (what consumers actually need) · `07-data/*` (fields, sensitivity) · existing specs on update |
| **Asks you** | the named consumer of any operation that has none · a migration plan per consumer before writing a MAJOR change |
| **Writes** | `06-interfaces/<component>-api.yaml` (OpenAPI) · `06-interfaces/<component>-events.yaml` (AsyncAPI) · `06-interfaces/schemas/*` |
| **Gate** | — |
| **Standard** | 09 |
| **Key behaviour** | classifies every change as PATCH / MINOR / MAJOR **per named consumer**, never deletes an operation (deprecate + sunset date + replacement), and verifies the document parses and every `$ref` resolves |

### 9 · `data`

| | |
|---|---|
| **Argument** | scope slug |
| **Reads** | `00-context/*` (vocabulary) · `03-hld/*` (boundaries) · `04-flows/*` (access patterns, consistency points) · `05-lld/*` (`owns` / `references`) |
| **Writes** | `07-data/data-model.puml` · `07-data/data-ownership.md` · `07-data/migration-plan.md` |
| **Gate** | — |
| **Standard** | 10, 18 |
| **Refuses to** | let two components write the same entity (escalates to an ADR) · classify sensitivity at table level instead of attribute level · leave an entity without a retention answer · write a migration with no rollback and no explicit point of no return |

### 10 · `security`

| | |
|---|---|
| **Argument** | scope slug |
| **Reads** | `03-hld/*` (trust boundaries) · `04-flows/*` (where credentials and data move) · `06-interfaces/*` (entry points) · `07-data/*` (what is worth stealing) · `00-context/architecture-drivers.md` |
| **Writes** | `08-crosscutting/security-design.md` — assets · trust boundaries · STRIDE table per boundary · controls · identity & access incl. per-operation permissions · secrets · encryption · privacy · audit · compliance · residual risks |
| **Gate** | — |
| **Standard** | 11 |
| **Refuses to** | leave a threat without a control or a signed acceptance · put a secret value in any artifact · skip the fail-closed behaviour when the authz system is down |

### 11 · `observability`

| | |
|---|---|
| **Argument** | scope slug |
| **Reads** | `00-context/architecture-drivers.md` (numbers become SLOs) · `04-flows/*` (instrumentation hooks already noted) · `05-lld/*` · `08-crosscutting/resilience-design.md` (failure modes needing detection) |
| **Writes** | `08-crosscutting/observability-design.md` — SLI/SLO table · correlation propagation incl. async and batch · log schema and redaction · metrics · traces · async signals (lag, DLQ, message age) · **failure-detection coverage** · alerts with owner and runbook · dashboards · retention/cost/access |
| **Gate** | — |
| **Standard** | 12 |
| **Reports** | failure modes with no detecting signal, and SLOs whose SLI is not actually computable |

### 12 · `resilience`

| | |
|---|---|
| **Argument** | scope slug |
| **Reads** | `00-context/architecture-drivers.md` (availability, RTO/RPO, load) · `03-hld/*` relationship catalogue · `04-flows/*` (declared timeouts and retries) · `05-lld/*` |
| **Writes** | `08-crosscutting/resilience-design.md` — availability targets · dependency criticality map · failure-mode table · degradation modes · tactics · capacity table · recovery · operability · verification plan |
| **Gate** | — |
| **Standard** | 13 |
| **Reports** | dependencies whose availability ceiling breaches your target · calls with no timeout · timeout budgets that do not nest · capacity numbers that are assumed rather than measured |

### 13 · `risk`

| | |
|---|---|
| **Argument** | scope slug |
| **Reads** | everything under `docs/architecture` — it **sweeps**, it does not brainstorm: risky assumptions, `Unknown (investigate)` rows, ADR negative consequences, security residuals, failure-mode residuals, unverified measures, overridden gates, third-party dependencies, expired open items |
| **Asks you** | a **named person** for every risk (team names are rejected), and a signature for every acceptance |
| **Writes** | `01-analysis/risk-register.md` + the trade-off log |
| **Gate** | — |
| **Standard** | 14 |
| **Reports** | High-exposure risks with no mitigation · mitigations that correspond to no design change or work item |

### 14 · `review`

| | |
|---|---|
| **Argument** | scope slug, optionally `--dimension <n>` to review one dimension (the scope limit is recorded in the report) |
| **Reads** | everything under `docs/architecture` |
| **Writes** | `09-review/design-review-<YYYY-MM-DD>.md` only — **it never modifies a design artifact** |
| **Gate** | — |
| **Standard** | 15, 20 |
| **Key behaviour** | 12 mechanical consistency checks · quality-bar pass per artifact · driver coverage with the **mechanism** named · findings carry `path:line` evidence or are demoted to Observations · the verdict is computed from severity counts (any Blocker → NOT READY) |

### 15 · `handoff`

| | |
|---|---|
| **Argument** | scope slug |
| **Reads** | all **Accepted** artifacts · the latest design review · the risk register |
| **Writes** | `10-handoff/dev-handoff-<YYYY-MM-DD>.md` — artifact index · work packages · build order **with the reason** · non-negotiables citing their ADR · free choices · prerequisites · verification plan per driver · definition of done incl. dashboards, alerts, runbooks · open items · risks · escalation route |
| **Gate** | **G3** every component has an LLD and an interface spec, every flow references only existing components · **G4** review verdict READY (or all conditions closed) and every High risk mitigated or signed off |
| **Standard** | 16 |
| **Refuses to** | link a Draft artifact as if it were agreed |

### 16 · `trace`

| | |
|---|---|
| **Arguments** | `<scope>` rebuild the index · `<TR-scope-NNN>` show everything one decision touched · `--orphans` · `--stale` · `--coverage` |
| **Reads** | every artifact header block · `_logs/.design-log` · `00-context/architecture-drivers.md` (for `--coverage`) |
| **Writes** | `_logs/.trace-index.md` only — plus a report to the conversation |
| **Gate** | — |
| **Standard** | 17 |
| **Reports** | `--orphans` artifacts with no trace-id and trace-ids with no origin · `--stale` artifacts whose upstream moved after they did, with the refresh command (it never regenerates them — that is your call) · `--coverage` drivers addressed nowhere, and design elements addressing no driver |

### Reading order to learn the method

1. `skills/method/SKILL.md` — the hub: journey, gates, hard rules
2. `skills/method/standards/00-sa-journey.md` — phases, dependency graph, the anti-patterns each gate catches
3. `skills/method/standards/01-workflow-protocol.md` — the nine phases every skill executes, and the Change Summary format
4. `skills/method/standards/20-quality-bar.md` — the definition of done for every artifact type
5. Then any step standard `02`–`16`, each ending in its own checklist

---

## How it is built

Three layers, so each answers exactly one question:

| Layer | Where | Answers |
|---|---|---|
| Skills | `skills/<name>/SKILL.md` | *what do I do* |
| Standards | `skills/method/standards/` | *what good looks like* |
| Templates + checklists | `skills/method/templates/`, `## Checklist` in each standard | *how do I prove it is done* |

The nine-phase execution protocol (resolve → load → inputs → mode → gate → **Change Summary** → **stop** → write + log → report) is written once in `standards/01-workflow-protocol.md`, so each skill contains only its own method.

### Gates

| Gate | Before | Passes when |
|---|---|---|
| G1 | `impact` | scope has a non-empty out-of-scope list, stakeholders named, ≥1 measurable scenario per high-priority attribute |
| G2 | `lld` | ≥1 Accepted ADR on the primary structural decision; HLD agrees with it |
| G3 | `handoff` | every component has an LLD and an interface spec; every flow references only existing components |
| G4 | implementation | review verdict READY, no open blockers; every High risk mitigated or formally accepted |

Gates are the only hard stops — everything else warns. An overridden gate becomes an accepted risk naming the person who overrode it.

---

## Repository layout

```
.claude-plugin/
  plugin.json          # plugin manifest
  marketplace.json     # lets the repo act as its own marketplace
skills/
  method/              # the hub: operating rules + reference library
    SKILL.md
    standards/         # 21 standards, each ending in its checklist
    templates/         # 17 artifact skeletons
  init/ intake/ drivers/ impact/ adr/ hld/ flow/ lld/ interface/
  data/ security/ observability/ resilience/ risk/ review/ handoff/ trace/
```

## Design principles

- **Decisions before diagrams.** A diagram not backed by an ADR is a drawing.
- **No number, no driver.** "Highly available" is not a requirement; "99.9% monthly, RTO ≤ 15 min" is.
- **Verified-no-impact is written down.** Absence from a table is not evidence of absence.
- **Every artifact is traceable** to the change that caused it, and reports what it makes stale.
- **Confirm before writing.** Always.
- **Unknowns are recorded, never invented.**

## Not included

No schema validation of generated OpenAPI/AsyncAPI/PlantUML beyond parse and `$ref` checks, and no CI hooks. Contributions welcome.

## Licence

MIT — see [LICENSE](LICENSE).
