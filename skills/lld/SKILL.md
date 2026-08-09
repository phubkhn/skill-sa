---
name: lld
description: Produce the internal design of one component: responsibilities, non-responsibilities, interfaces, data ownership, state machines, concurrency, failure modes. Use when the user asks for low-level design or detailed component design.
---

# SA — Produce the internal design for one component

| | |
|---|---|
| Journey step | 7 — LLD |
| Produces | 05-lld/<component>.yaml |
| Inputs | 03-hld/*, 04-flows/*, 02-decisions/*, 00-context/architecture-drivers.md, 07-data/* |
| Gate | G2 (before running) |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/08-lld-standard.md` |

**Method contract:** read `../method/SKILL.md` and `../method/standards/01-workflow-protocol.md` before acting. All nine execution phases (P1–P9) are defined there and are mandatory.

**Checklist:** the `## Checklist` section of `../method/standards/08-lld-standard.md` — self-assess item by item in P9.

---

Follow `../method/standards/01-workflow-protocol.md` P1–P9.

Arguments: $ARGUMENTS — `<component>`. If absent, list components from the HLD container view that have no LLD yet.

**P5 Gate G2:** ≥1 `Accepted` ADR covering the primary structural decision, and HLD context + container views exist and agree with it.

**P3:** read the HLD element + relationship catalogue rows for this component, every flow it participates in, its data ownership rows, and the ADRs that constrain it.

**Method:**

1. Derive **responsibilities** from the HLD responsibility statement plus every flow step this component performs. Each gets an ID and the drivers it satisfies.
2. Write **non-responsibilities** explicitly — what neighbours own.
3. List `provides` and `consumes` interfaces. Every consumed dependency **must** carry `reason`, `failure-behaviour`, and `timeout` — taken from the flows and the resilience design; if absent there, decide now and feed it back.
4. Split data into `owns` (sole writer, with retention and sensitivity) and `references` (with freshness tolerance). A component owning nothing and referencing everything is a coordination smell — flag it.
5. Model state machines for any entity with more than two states.
6. Specify concurrency: model, shared state, ordering guarantees, idempotency.
7. List configuration keys, marking secrets — values never appear.
8. Fill failure modes; cross-check against `08-crosscutting/resilience-design.md` and reconcile differences rather than duplicating.
9. Keep out anything a competent team should choose freely.

**P8:** `../method/templates/lld.yaml`. Update mode: edit in place, prepend changelog entry, bump MINOR (additive) or MAJOR (responsibility/ownership change).

**P9:** report responsibility↔interface coverage (any orphan on either side is a defect), then `Next: /sa:gen-interface <component>`.
