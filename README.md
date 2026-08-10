# skill-sa

A generic **Solution Architect** skill set for Claude Code and Cowork.
Domain-agnostic, vendor-agnostic, language-agnostic — it designs *systems*, not any particular business.

**19 skills** covering the full SA journey · **27 standards** defining what good looks like · **29 artifact templates** · **4 quality gates** · **3 tailoring profiles** · one worked example.

---

## Install

### Option A — plugin marketplace (recommended)

```
/plugin marketplace add phubkhn/skill-sa
/plugin install sa@skill-sa
```

Skills then appear namespaced as `sa:intake`, `sa:hld`, `sa:review`, … The namespace matters: `init` and `review` collide with built-in commands without it.

### Option B — drop-in into a skills directory

Skill discovery looks for `<skills-dir>/<skill-name>/SKILL.md`. This repository nests its skills one level deeper (`skills/<name>/SKILL.md`), so cloning the repository directly into `~/.claude/skills/` does **not** work — the `SKILL.md` files end up two levels too deep to be found.

Link or copy the individual skill directories instead:

```bash
git clone https://github.com/phubkhn/skill-sa.git ~/src/skill-sa
mkdir -p ~/.claude/skills
for d in ~/src/skill-sa/skills/*/; do
  ln -s "$d" ~/.claude/skills/"sa-$(basename "$d")"
done
```

This gives you `sa-intake`, `sa-hld`, `sa-review`, … The `sa-` prefix avoids the `init` / `review` collisions that Option A solves with its namespace.

Note that the skills reference each other by relative path (`../method/standards/…`), which symlinks preserve and copies of individual directories do not. Symlink, or copy the whole `skills/` tree.

### Option C — vendored into a project

```bash
git clone https://github.com/phubkhn/skill-sa.git .claude/plugins/skill-sa
```

Commit it, and every teammate gets the same architecture method with the repository.

Verify with `/plugin` or `claude plugin list`.

### Tool permissions, and why they look conservative

Two frontmatter fields are easy to confuse, and confusing them inverts the safety property:

- **`allowed-tools` pre-approves** — the listed tools run without a permission prompt. It grants; it never restricts.
- **`disallowed-tools` restricts** — the listed tools are removed from the pool while the skill is active.

So every skill here pre-approves **reads only** (`Read, Grep, Glob`). Writing an artifact is the irreversible act, and it goes through the normal permission prompt as a second gate behind the Change Summary stop. `Bash` is never pre-approved anywhere: a blanket bash grant is an unrestricted shell, which is the widest possible action surface for the narrowest benefit. Where a skill genuinely needs a command — `git log` for an update delta, a PlantUML render check, a spec parse — it asks, and you see the command first.

`sa:review` and `sa:trace` additionally set `disallowed-tools: Edit, NotebookEdit`. Both are read-and-report skills; the claim that they never modify a design artifact is now enforced for edits rather than merely asserted in prose.

`sa:review` also sets `context: fork`, so the review runs in a subagent that did not watch the design being made. See `standards/26-operating-guardrails.md` §5.

**Portability caveat.** `disallowed-tools` and `context` are Claude Code fields. Uploading a skill to claude.ai, the Skills API, or packaging with `package_skill.py` accepts only `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools`, and fails hard on anything else:

```
Unexpected key(s) in SKILL.md frontmatter: context. Allowed properties are:
allowed-tools, compatibility, description, license, metadata, name
```

Strip those two fields from `review` and `trace` before uploading, and enforce the read-only property by convention instead. All other skills upload unchanged.

---

## Quick start

```
sa:init            # scaffold docs/architecture + sa-config.yaml, choose a profile
sa:intake          # what problem, for whom, inside what boundary
sa:drivers         # measurable quality-attribute scenarios
sa:impact          # what this disturbs                        [gate G1]
sa:options         # compare whole-solution shapes before deciding
sa:adr             # record the structural decisions
sa:hld             # C4 context / container / component / deployment
sa:flow            # runtime sequences, including failures
sa:lld             # per-component internals                   [gate G2]
sa:interface       # OpenAPI + AsyncAPI contracts
sa:data sa:security sa:resilience sa:observability sa:cost     # in parallel with the above
sa:risk            # consolidated, owned risk register
sa:review          # evidence-based verdict
sa:handoff         # implementation-ready package              [gates G3, G4]
sa:trace           # why does this exist / what is now stale
```

Every generating skill stops for a **Change Summary** and writes nothing until you confirm.

**Start with the profile.** `sa:init` asks whether this is `light`, `standard` or `full` work, and that answer decides how much of the list above you actually run. A two-week change should not produce sixteen documents. See `skills/method/standards/21-tailoring.md`.

---

## The journey

```
init → intake → drivers → impact → options → adr → hld → flow → lld → interface
                                              ↘ data · security · resilience → observability · cost ↙
                                                        risk → review → handoff → trace
```

Data, security, resilience, observability and cost run **in parallel** with the design steps, not after them. Resilience runs **before** observability — you cannot design a signal for a failure mode nobody has written down.

| Skill | Produces | Standard |
|---|---|---|
| `init` | `sa-config.yaml`, `<docs-root>/**` | 19, 21 |
| `intake` | `00-context/sa-intent.md`, `stakeholders.md`, `principles.md` | 02 |
| `drivers` | `00-context/architecture-drivers.md` | 03 |
| `impact` | `01-analysis/impact-analysis.md` | 04 |
| `options` | `01-analysis/solution-options.md` | 25 |
| `adr` | `02-decisions/ADR-NNNN-*.md` | 05 |
| `hld` | `03-hld/*.puml` + catalogues | 06, 18, 22 |
| `flow` | `04-flows/*.puml` + narrative | 07, 18 |
| `lld` | `05-lld/<component>.yaml` | 08 |
| `interface` | `06-interfaces/*.yaml` | 09 |
| `data` | `07-data/*` | 10 |
| `security` | `08-crosscutting/security-design.md` | 11 |
| `resilience` | `08-crosscutting/resilience-design.md` | 13 |
| `observability` | `08-crosscutting/observability-design.md` | 12 |
| `cost` | `01-analysis/cost-model.md` | 23 |
| `risk` | `01-analysis/risk-register.md` | 14 |
| `review` | `09-review/design-review-<date>.md` | 15, 20 |
| `handoff` | `10-handoff/dev-handoff-<date>.md` | 16, 24 |
| `trace` | `_logs/.trace-index.md` + report | 17 |

Plus `method` — the hub every skill reads first. That is 19 skills and one method hub, 20 `SKILL.md` files in total.

---

## Tailoring

The full journey is right for a new platform and wrong for a two-week change. `sa-config.yaml` carries a profile:

| Profile | When | Artifacts | Gates |
|---|---|---|---|
| `light` | change inside one component; no contract, data-ownership or dependency change | intent (short form), impact, trace — plus whatever the conditional triggers promote | G1 |
| `standard` | new or changed public contract, new data store, new cross-team dependency, or an expensive-to-reverse decision | most of the journey | G1, G2, G4 |
| `full` | new system, platform replacement, or > 3 teams | everything | G1–G4 |

`sa:review` lists profile-excluded artifacts under "Not required at this profile" rather than reporting them as gaps. Full table in `standards/21-tailoring.md`.

---

## Skill reference — inputs and outputs

Paths are relative to `docs-root` in `sa-config.yaml` (default `docs/architecture/`).
Every generating skill also reads `skills/method/SKILL.md` + `standards/01-workflow-protocol.md`, honours `sa-config.yaml`, appends to `_logs/.design-log`, and **stops for your confirmation before writing anything**. Those are omitted below to keep the tables readable.

### 0 · `init`

| | |
|---|---|
| **Argument** | optional scope slug, kebab-case (e.g. `checkout-revamp`) |
| **Reads** | existing `sa-config.yaml`, if any |
| **Asks you** | scope slug · **profile** · **language** · docs root · diagram tool · contract formats · which steps are in play |
| **Writes** | `sa-config.yaml` (repo root) · the full `<docs-root>/**` tree · `_logs/.design-log` · `_logs/.trace-index.md` · `<docs-root>/README.md` |
| **Gate** | — |
| **Standard** | 19 (layout, naming, versioning), 21 (tailoring), 00 (journey) |

### 1 · `intake`

| | |
|---|---|
| **Argument** | scope slug |
| **Reads** | whatever requirement sources you point at — tickets, notes, docs, transcripts; existing `sa-intent.md` on update |
| **Asks you** | 8 mandatory questions: what breaks today and what it costs · what is out of scope · who decides and who can veto · what already exists that this must live with · which constraints are imposed vs chosen · what "done well" looks like in 6 months · what was tried before and why it failed · the deadline and what drives it |
| **Writes** | `00-context/sa-intent.md` · `stakeholders.md` · `principles.md` if none exists |
| **Gate** | — |
| **Standard** | 02 |
| **Refuses to** | put solution language in the problem statement · leave the out-of-scope list empty · invent an answer instead of logging an open question |

### 2 · `drivers`

| | |
|---|---|
| **Argument** | scope slug |
| **Reads** | `00-context/sa-intent.md` (concerns, constraints, success criteria) · existing ADRs, so settled numbers are not re-litigated |
| **Asks you** | any missing **measure** — the numbers behind each quality attribute; a forced ranking if more than 5 attributes land High/High |
| **Writes** | `00-context/architecture-drivers.md` — six-part scenarios, a full 20-attribute sweep, the priority matrix, the conflict list, the unknown-measure list |
| **Gate** | — |
| **Standard** | 03 |
| **Refuses to** | accept an attribute described only with adjectives · invent an SLO · leave an end-to-end measure unallocated across hops |

### 3 · `impact`

| | |
|---|---|
| **Argument** | scope slug |
| **Reads** | intent · drivers · existing `03-hld/**`, `05-lld/**`, `06-interfaces/**` · your answer on where current-state knowledge lives if the repo has no docs |
| **Writes** | `01-analysis/impact-analysis.md` — baseline · impacted elements (including `None (verified)` rows) · new elements · contract/data/operational/organisational impact · **decommissioning table** · **stale artifact list with the refresh command** · effort and sequencing · unknowns · candidate risks |
| **Gate** | **G1** — non-empty out-of-scope list, stakeholders named, ≥1 measurable scenario per **H/H** attribute |
| **Standard** | 04 |
| **Key behaviour** | blast-radius walk: one hop outward from each touched element — callers, callees, data readers, event consumers, co-deployed units — repeated until a hop adds nothing new. Every baseline claim carries a source, or is rewritten as an assumption |

### 3b · `options`

| | |
|---|---|
| **Argument** | scope slug |
| **Reads** | intent · drivers (the H/H set becomes the axes) · impact analysis |
| **Asks you** | agreement on the evaluation axes and weights **before** any option is described |
| **Writes** | `01-analysis/solution-options.md` — 2–4 whole-solution shapes described identically, costed, compared with reasons rather than scores, one recommendation naming the deciding axis |
| **Gate** | — |
| **Standard** | 25 |
| **Refuses to** | describe options asymmetrically · omit "do nothing" where credible · recommend without naming the deciding axis |

### 4 · `adr`

| | |
|---|---|
| **Argument** | the decision in a few words; if omitted, it lists open decisions from the drivers' conflict list and the impact analysis' unknowns |
| **Reads** | drivers (the evaluation axes) · impact analysis · options paper · principles · **all existing ADRs**, to detect a decision already made or contradicted |
| **Asks you** | what alternative you rejected, if you offer only one option · whether the deciders have actually agreed (Proposed vs Accepted) |
| **Writes** | `02-decisions/ADR-NNNN-<slug>.md` · a row in `adr-index.md` · the status line of a superseded ADR |
| **Gate** | — |
| **Standard** | 05 |
| **Refuses to** | write an ADR with fewer than 2 genuine options · omit the negative consequences · bundle two decisions in one record · adopt a vendor with no exit plan |

### 5 · `hld`

| | |
|---|---|
| **Argument** | scope slug, optionally a view: `context` \| `container` \| `component <container>` \| `deployment <env>` |
| **Reads** | `00-context/*` · impact analysis · every **Accepted** ADR (a still-Proposed structural ADR is flagged) |
| **Writes** | `03-hld/system-context.puml` · `container-<system>.puml` · `component-<container>.puml` · `deployment-<env>.puml` · element, relationship and node catalogues |
| **Gate** | — |
| **Standard** | 06, 18, 22 |
| **Key behaviour** | runs 6 coupling checks before writing · allocates each end-to-end latency budget across the hops · enforces one owning team per container · records an interface-spec path or a written `N/A` per element, which is what G3 later reads |

### 6 · `flow`

| | |
|---|---|
| **Argument** | `<flow-name>`; if omitted it proposes the flow list from the selection criteria in standard 07 |
| **Reads** | `03-hld/*` element catalogue (participant names must match exactly) · drivers · ADRs |
| **Writes** | `04-flows/<flow-name>.puml` · the narrative table (steps, timeouts, retries, idempotency, failure behaviour, emitted signals) |
| **Gate** | — |
| **Standard** | 07, 18 |
| **Refuses to** | use a participant absent from the HLD · leave a cross-boundary call without a timeout · show a retry on a non-idempotent operation · ship a flow with only a happy path |

### 7 · `lld`

| | |
|---|---|
| **Argument** | `<component>`; if omitted it lists HLD containers that have no LLD yet |
| **Reads** | `03-hld/*` · every flow it participates in · `07-data/*` ownership · ADRs · drivers |
| **Writes** | `05-lld/<component>.yaml` — responsibilities · **non-responsibilities** · provides/consumes · owns vs references data · state machines · concurrency and idempotency · configuration · failure modes · constraints · changelog |
| **Gate** | **G2** — ≥1 Accepted ADR on the primary structural decision, and the HLD agrees with it |
| **Standard** | 08 |
| **Refuses to** | leave a consumed dependency without reason, failure-behaviour and timeout · leave an orphan responsibility or an unowned operation · overwrite an ownership decision the data design has already made |

### 8 · `interface`

| | |
|---|---|
| **Argument** | `<component>` and optionally `sync` \| `async` \| `both` |
| **Reads** | `05-lld/<component>.yaml` (`provides` is the authority) · flows · data design · existing specs |
| **Asks you** | the named consumer of any operation that has none · a migration plan per consumer before writing a MAJOR change |
| **Writes** | `06-interfaces/<component>-api.yaml` · `<component>-events.yaml` · `schemas/*` |
| **Gate** | — |
| **Standard** | 09 |
| **Key behaviour** | classifies every change as PATCH / MINOR / MAJOR **per named consumer**, never deletes an operation, and verifies the document parses and every `$ref` resolves |

### 9 · `data`

| | |
|---|---|
| **Argument** | scope slug |
| **Reads** | `00-context/*` (vocabulary) · HLD (boundaries) · flows (access patterns) · LLDs (provisional `owns` / `references`) |
| **Writes** | `07-data/data-model.puml` · `data-design.md` · `migration-plan.md` |
| **Gate** | — |
| **Standard** | 10, 18 |
| **Key behaviour** | **the authority on data ownership** — LLDs that claimed otherwise are reported stale and must be re-run. Names the coexistence pattern where an old system stays live, with an end date |
| **Refuses to** | let two components write the same entity · classify sensitivity at table level · leave an entity without a retention answer · write a migration with no rollback and no explicit point of no return |

### 10 · `security`

| | |
|---|---|
| **Argument** | scope slug |
| **Reads** | HLD (trust boundaries) · flows · interfaces (entry points) · data design · drivers |
| **Writes** | `08-crosscutting/security-design.md` — assets · trust boundaries · STRIDE per boundary · controls · identity & access · secrets · encryption · privacy · audit · compliance · residual risks |
| **Gate** | — |
| **Standard** | 11 |
| **Refuses to** | leave a threat without a control or a signed acceptance · put a secret value in any artifact · skip the fail-closed behaviour when the authz system is down |

### 11 · `resilience`

| | |
|---|---|
| **Argument** | scope slug |
| **Reads** | drivers (availability, RTO/RPO, load) · HLD relationship catalogue · deployment view · flows · LLDs |
| **Writes** | `08-crosscutting/resilience-design.md` — availability targets · dependency criticality map · failure-mode table · degradation modes · tactics · capacity table · recovery · operability · verification plan |
| **Gate** | — |
| **Standard** | 13 |
| **Reports** | dependencies whose availability ceiling breaches your target · calls with no timeout · timeout budgets that do not nest · capacity numbers that are assumed rather than measured |

### 12 · `observability`

| | |
|---|---|
| **Argument** | scope slug |
| **Reads** | drivers (numbers become SLOs) · flows · LLDs · **resilience design** (failure modes needing detection) · security design |
| **Writes** | `08-crosscutting/observability-design.md` — SLI/SLO table · correlation propagation incl. async and batch · log schema and redaction · metrics · traces · async signals · **failure-detection coverage** · alerts with owner and runbook · dashboards · retention/cost/access |
| **Gate** | — |
| **Standard** | 12 |
| **Reports** | failure modes with no detecting signal, and SLOs whose SLI is not actually computable |

### 13 · `cost`

| | |
|---|---|
| **Argument** | scope slug |
| **Reads** | **resilience design capacity table** (the basis — without it the skill stops) · deployment view · data design (volume, growth, retention) · drivers · options paper |
| **Writes** | `01-analysis/cost-model.md` — cost drivers · build vs run · run at expected and peak · 12- and 36-month projection · unit economics · **cost of each quality target** · optimisation levers · confidence labels · budget owner |
| **Gate** | — |
| **Standard** | 23 |
| **Refuses to** | price from a vendor list with no capacity analysis behind it · report a figure without a measured / quoted / estimated label |

### 14 · `risk`

| | |
|---|---|
| **Argument** | scope slug |
| **Reads** | everything under `<docs-root>` — it **sweeps** twelve mechanical sources, it does not brainstorm |
| **Asks you** | a **named person** for every risk (team names are rejected), and a signature for every acceptance |
| **Writes** | `01-analysis/risk-register.md` + the trade-off log |
| **Gate** | — |
| **Standard** | 14 |
| **Reports** | High-exposure risks with no mitigation · mitigations that correspond to no design change or work item |

### 15 · `review`

| | |
|---|---|
| **Argument** | scope slug, optionally `--dimension <n>` |
| **Reads** | everything under `<docs-root>`, plus the profile |
| **Writes** | `09-review/design-review-<YYYY-MM-DD>.md` only — **it never modifies a design artifact** |
| **Gate** | — |
| **Standard** | 15, 20 |
| **Key behaviour** | 19 mechanical consistency checks · quality-bar pass per artifact · driver coverage with the **mechanism** named · simplicity counted rather than opined on · findings carry `path:line` evidence or are demoted to Observations · the verdict is computed from severity counts · profile-excluded artifacts are not findings |

### 16 · `handoff`

| | |
|---|---|
| **Argument** | scope slug |
| **Reads** | all **Accepted** artifacts · the latest design review · the risk register |
| **Writes** | `10-handoff/dev-handoff-<YYYY-MM-DD>.md` — artifact index · work packages · build order **with the reason** · non-negotiables citing their ADR · free choices · prerequisites · verification plan per driver · definition of done incl. dashboards, alerts, runbooks · open items · risks · escalation route |
| **Gate** | **G3** every component has an LLD and an interface spec or a written `N/A` · **G4** review verdict READY and every High risk mitigated or signed off |
| **Standard** | 16, 24 |
| **Refuses to** | link a Draft artifact as if it were agreed · hand over a driver with no numeric verification threshold |

### 17 · `trace`

| | |
|---|---|
| **Arguments** | `<scope>` rebuild the index · `<TR-scope-NNN>` show everything one decision touched · `--orphans` · `--stale` · `--coverage` |
| **Reads** | every artifact header (all four formats) · `_logs/.design-log` · drivers (for `--coverage`) |
| **Writes** | `_logs/.trace-index.md` only — plus a report to the conversation |
| **Gate** | — |
| **Standard** | 17 |
| **Reports** | `--orphans` artifacts with no trace-id and trace-ids with no origin · `--stale` artifacts whose upstream moved after they did, **and seed/authority conflicts**, with the refresh command · `--coverage` drivers addressed nowhere, and design elements addressing no driver |

### Reading order to learn the method

1. `skills/method/SKILL.md` — the hub: journey, gates, hard rules
2. `skills/method/standards/00-sa-journey.md` — canonical skill names, phases, dependency graph, the two-pass rule, the anti-patterns each gate catches
3. `skills/method/standards/01-workflow-protocol.md` — the nine phases every skill executes, config honouring, header formats, the Change Summary
4. `skills/method/standards/21-tailoring.md` — how much of this to actually run
5. `skills/method/standards/20-quality-bar.md` — the definition of done for every artifact type
6. `skills/method/standards/26-operating-guardrails.md` — how the skill set must behave while producing all of it
7. `examples/express-lane/` — one small initiative carried end to end
8. Then any step standard `02`–`16`, `22`–`25`, each ending in its own checklist

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
| G1 | `impact` | non-empty out-of-scope list, stakeholders named, ≥1 measurable scenario per **H/H** attribute |
| G2 | `lld` | ≥1 Accepted ADR on the primary structural decision; HLD agrees with it |
| G3 | `handoff` | every component has an LLD, and an interface spec or a written `N/A — <reason>`; every flow references only existing components |
| G4 | implementation | review verdict READY, no open blockers; every High risk mitigated or formally accepted |

Gates are the only hard stops — everything else warns. An overridden **or config-disabled** gate becomes an accepted risk naming the person responsible.

---

## Repository layout

```
.claude-plugin/
  plugin.json          # plugin manifest
  marketplace.json     # lets the repo act as its own marketplace
skills/
  method/              # the hub: operating rules + reference library
    SKILL.md
    standards/         # 27 standards, each ending in its checklist
    templates/         # 29 artifact skeletons
  init/ intake/ drivers/ impact/ options/ adr/ hld/ flow/ lld/ interface/
  data/ security/ resilience/ observability/ cost/ risk/ review/ handoff/ trace/
examples/
  express-lane/        # one initiative carried end to end at `standard` profile
```

## Design principles

- **Decisions before diagrams.** A diagram not backed by an ADR is a drawing.
- **No number, no driver.** "Highly available" is not a requirement; "99.9% monthly, RTO ≤ 15 min" is.
- **Every claim about the existing system cites a source.** Otherwise it is written as an assumption.
- **Verified-no-impact is written down.** Absence from a table is not evidence of absence.
- **Every artifact is traceable** to the change that caused it, and reports what it makes stale.
- **Tailor before you start.** The full journey on a small change is not rigour.
- **Confirm before writing.** Always — and the confirmation names the exact files.
- **A guardrail beats an instruction.** Where a rule can be enforced by tool permissions or a gate, it is; prose is the fallback, not the mechanism.
- **Nothing verifies itself.** A passed checklist is completeness; the review runs in fresh context and real verification is a number in a test.
- **Unknowns are recorded, never invented.** No requirement is weakened to let a run finish.

## Not included

No schema validation of generated OpenAPI/AsyncAPI/PlantUML beyond parse and `$ref` checks, and no CI hooks. Contributions welcome.

## Licence

MIT — see [LICENSE](LICENSE).
