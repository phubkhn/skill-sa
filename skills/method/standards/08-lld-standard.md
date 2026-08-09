# Standard 08 — Low-Level Design

**Artifact:** `05-lld/<component>.yaml`
**Purpose:** enough internal design that a team can implement without re-deciding architecture — and no more.

## Structure

```yaml
component: <name>
version: "<MAJOR.MINOR>"
status: Draft | In Review | Accepted | Superseded
trace-id: <TR-...>
owner-team: <team>

purpose: >
  One paragraph. What this component is responsible for, in business terms.

responsibilities:            # what it owns; each maps to >=1 interface operation
  - id: R1
    description: <...>
    satisfies-drivers: [QA-PERF-01]

non-responsibilities:        # explicit — prevents scope drift
  - <what this component deliberately does not do, and who does>

interfaces:
  provides:
    - name: <operation or endpoint>
      kind: sync-api | async-event | scheduled | cli
      spec: 06-interfaces/<component>-api.yaml#/paths/...
      implements: R1
  consumes:
    - name: <upstream operation/event>
      from: <component>
      reason: <why this dependency exists>
      failure-behaviour: fail-fast | retry | fallback | degrade | queue
      timeout: <value>

data:
  owns:                      # this component is the only writer
    - entity: <Name>
      store: <logical store>
      retention: <period + trigger>
      sensitivity: public | internal | confidential | restricted
  references:                # read-only copies / lookups
    - entity: <Name>
      source: <owning component>
      freshness: <staleness tolerance>

state-machines:
  - entity: <Name>
    states: [<...>]
    transitions:
      - from: <s1>
        to: <s2>
        trigger: <event/command>
        guard: <condition>

internal-structure:          # C4 L3/L4 — only what is non-obvious
  - element: <module/class/layer>
    responsibility: <...>

concurrency:
  model: <threading/async model>
  shared-state: <what is shared and how it is protected>
  ordering-guarantees: <...>
  idempotency: <how repeat invocations are handled>

configuration:
  - key: <name>
    purpose: <...>
    default: <...>
    secret: true | false

failure-modes:               # cross-check against 08-crosscutting/resilience-design.md
  - mode: <what fails>
    detection: <how we know>
    handling: <what happens>
    user-visible-effect: <...>

constraints:
  - <business rule, compliance rule, SLA, hard limit>

open-items:
  - item: <...>
    owner: <...>
    by: <date>

changelog:
  - version: "<N.M>"
    date: <YYYY-MM-DD>
    author: <name>
    changes: <what and why>
```

## Rules

1. **Responsibilities map 1:1 to interface operations.** A responsibility with no operation is dead; an operation with no responsibility is unowned.
2. **Non-responsibilities are mandatory.** Most scope creep is a component quietly absorbing a neighbour's job.
3. **Owns vs references is a hard distinction.** Only the owner writes. Everyone else declares freshness tolerance.
4. **Every consumed dependency states failure behaviour and timeout.** No exceptions — this is where outages are designed in or out.
5. **State machines are explicit** wherever an entity has more than two states.
6. **No implementation detail that a competent team should choose freely.** Don't specify variable names, class hierarchies, or library versions unless a driver forces it.
7. **Idempotency is stated for every non-safe operation**, not left to the implementer.

## Depth heuristic

Include a detail if: removing it would cause two teams to make incompatible assumptions, or it is required to satisfy a named driver. Otherwise leave it out.

## Checklist

Self-assess against this list before reporting the artifact done. Report pass/fail **per item** — never a silent pass. A failed item becomes an OPEN item with an owner; it is not deleted to make the list pass.

- [ ] Purpose stated in business terms
- [ ] Every responsibility has an ID and the drivers it satisfies
- [ ] Non-responsibilities listed, with who owns them instead
- [ ] Responsibilities map 1:1 to provided operations — no orphans either way
- [ ] Every consumed dependency has reason, failure-behaviour, and timeout
- [ ] Owned data has a single writer, retention, and sensitivity
- [ ] Referenced data has a freshness tolerance
- [ ] State machines defined for entities with >2 states
- [ ] Concurrency model, shared state, ordering, and idempotency stated
- [ ] Config keys listed; secrets flagged; no secret values present
- [ ] Failure modes reconciled with the resilience design (not duplicated inconsistently)
- [ ] Constraints traced to a PRD/driver/compliance source
- [ ] No detail a competent team should choose freely
- [ ] Changelog entry prepended; version incremented correctly
