# Standard 19 — Naming, Structure, Versioning

## Repository layout

```
sa-config.yaml
docs/architecture/
  00-context/
    sa-intent.md
    architecture-drivers.md
    stakeholders.md
  01-analysis/
    impact-analysis.md
    risk-register.md
  02-decisions/
    adr-index.md
    ADR-0001-<slug>.md
  03-hld/
    system-context.puml            # C4 L1
    container-<system>.puml        # C4 L2
    component-<container>.puml     # C4 L3
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
    data-ownership.md
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
| Trace IDs | `TR-<scope>-<3-digit>` | `TR-checkout-014` |
| Risk IDs | `RISK-<3-digit>` | `RISK-004` |
| Quality scenarios | `QA-<attribute-abbrev>-<2-digit>` | `QA-PERF-02` |

## Versioning

| Artifact | Scheme | Increment on |
|---|---|---|
| Narrative docs (intent, drivers, impact, crosscutting) | integer `v1, v2` | any content change |
| Diagrams (`.puml`) | integer, in header comment | any structural change |
| LLD YAML | `MAJOR.MINOR` | MINOR = additive; MAJOR = responsibility or ownership change |
| API/event specs | `MAJOR.MINOR.PATCH` | PATCH = doc/example; MINOR = additive & backward-compatible; MAJOR = breaking |
| ADR | never versioned — superseded by a new ADR |

**One artifact, one file, edited in place.** Never `impact-analysis-v2.md`. History lives in git and in the changelog block.

## Status lifecycle

`Draft → In Review → Accepted → Superseded`

- Only `Accepted` artifacts may be cited by downstream artifacts. Citing a `Draft` is allowed but must be flagged in the Change Summary.
- `Superseded` artifacts stay in the repo with a pointer to their successor. Never delete.
