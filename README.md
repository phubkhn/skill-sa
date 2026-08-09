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
