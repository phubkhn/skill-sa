# Standard 19 — Naming, Structure, Versioning

## Repository layout

Paths below are relative to `docs-root` in `sa-config.yaml`. **`docs/architecture/` is the default value, not a constant** — never hard-code it in an artifact or a skill.

```
sa-config.yaml
<docs-root>/
  README.md
  00-context/
    sa-intent.md
    architecture-drivers.md
    stakeholders.md
    principles.md
  01-analysis/
    impact-analysis.md
    solution-options.md
    cost-model.md
    risk-register.md
  02-decisions/
    adr-index.md
    ADR-0001-<slug>.md
  03-hld/
    system-context.puml            # C4 L1
    container-<system>.puml        # C4 L2
    component-<container>.puml     # C4 L3
    deployment-<environment>.puml  # runtime placement — standard 22
  04-flows/
    <flow-name>.puml
  05-lld/
    <component>.yaml               # C4 L4
  06-interfaces/
    <component>-api.yaml           # OpenAPI 3.x (sync)
    <component>-events.yaml        # AsyncAPI 2.x (async)
    schemas/<Model>.yaml           # shared schemas
  07-data/
    data-model.puml
    data-design.md                 # ownership, classification, lifecycle, consistency
    migration-plan.md
  08-crosscutting/
    security-design.md
    observability-design.md
    resilience-design.md
  09-review/
    design-review-<YYYY-MM-DD>.md
  10-handoff/
    dev-handoff-<YYYY-MM-DD>.md
  _logs/
    .design-log
    .trace-index.md
    .failure-log                   # how this method failed, and the guardrail it produced
```

## Naming rules

| Thing | Rule | Example |
|---|---|---|
| Files & directories | kebab-case, no spaces, no dates except where the artifact is point-in-time | `order-service.yaml` |
| Components/containers | noun or noun-phrase, singular, no tech suffix unless it *is* the tech | `pricing-engine`, not `pricing-engine-v2-new` |
| Flows | `<actor>-<intent>` | `client-submit-request` |
| ADRs | `ADR-<4-digit>-<slug>` | `ADR-0007-async-messaging` |
| Events | `<entity>.<past-tense-verb>` | `order.placed` |
| Endpoints | plural resource nouns, verbs only in HTTP method | `POST /orders` |
| Trace IDs | `<trace-prefix>-<scope>-<3-digit>` | `TR-checkout-014` |
| Risk IDs | `RISK-<scope>-<3-digit>` | `RISK-checkout-004` |
| Quality scenarios | `QA-<attribute-abbrev>-<2-digit>` | `QA-PERF-02` |
| Work packages | `WP-<2-digit>` | `WP-03` |
| Review findings | `FINDING-<3-digit>` | `FINDING-007` |

Risk IDs carry the scope for the same reason trace IDs do: two initiatives running in one repository would otherwise both allocate `RISK-004` and the register would silently merge them.

## Versioning

| Artifact | Scheme | Increment on |
|---|---|---|
| Narrative docs (intent, drivers, impact, crosscutting) | integer `v1, v2` | any content change |
| Diagrams (`.puml`) | integer, in header comment | any structural change |
| LLD YAML | `MAJOR.MINOR` | MINOR = additive; MAJOR = responsibility or ownership change |
| API/event specs | `MAJOR.MINOR.PATCH` | PATCH = doc/example; MINOR = additive & backward-compatible; MAJOR = breaking |
| ADR | never versioned — superseded by a new ADR |

**ADR exception to the header block.** An ADR carries `Status`, `Date`, `Deciders`, `Trace ID` and `Drivers addressed`, but **no `Version` and no changelog** — it is immutable once Accepted, so there is nothing to version. Quality-bar item U1 is satisfied for an ADR by those five fields. A `Version` row on an ADR is a sign someone edited a decision in place, which rule 1 of Standard 05 forbids.

**One artifact, one file, edited in place.** Never `impact-analysis-v2.md`. History lives in git and in the changelog block.

## Status lifecycle

`Draft → In Review → Accepted → Superseded`

- Only `Accepted` artifacts may be cited by downstream artifacts. Citing a `Draft` is allowed but must be flagged in the Change Summary.
- `Superseded` artifacts stay in the repo with a pointer to their successor. Never delete.

## Language

`language` in `sa-config.yaml` sets the language of artifact **prose**: narrative, rationale, descriptions, table cell text.

These stay English kebab-case regardless of `language`, because they are cross-referenced mechanically and appear in code:

- file and directory names
- element, container, component and node names
- flow names
- event names and field names
- all IDs (`QA-…`, `ADR-…`, `TR-…`, `RISK-…`, `R1`, `WP-…`)
- enum values (`Accepted`, `None (verified)`, `hard`/`soft`/`optional`, `Draft`, …)
- section headings in templates

Mixing languages inside an identifier, or translating an enum value, breaks every grep-based check in this skill set.
