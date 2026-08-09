---
name: data
description: Design the data model, ownership, classification, lifecycle, consistency and migration plan. Use when the user asks about data modelling, data ownership, retention, or a database migration plan.
---

# SA — Design the data model, ownership, lifecycle and migration

| | |
|---|---|
| Journey step | 9 — Data |
| Produces | 07-data/data-model.puml, 07-data/data-ownership.md, 07-data/migration-plan.md |
| Inputs | 00-context/*, 03-hld/*, 04-flows/*, 05-lld/* |
| Gate | none |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/10-data-standard.md`, `../method/standards/18-diagram-conventions.md` |

**Method contract:** read `../method/SKILL.md` and `../method/standards/01-workflow-protocol.md` before acting. All nine execution phases (P1–P9) are defined there and are mandatory.

**Checklist:** the `## Checklist` section of `../method/standards/10-data-standard.md` — self-assess item by item in P9.

---

Follow `../method/standards/01-workflow-protocol.md` P1–P9.

**P3:** read intent (domain vocabulary), HLD (component boundaries), flows (access patterns and consistency points), LLDs (`owns` / `references`).

**Method:**

1. Build the **conceptual model** — entities, relationships, cardinality, technology-free.
2. Assign **exactly one owning component per entity**. Any entity with two writers is stopped and escalated to an ADR.
3. Classify **every attribute**: sensitivity level, PII flag, regulatory tag. Attribute level, not table level.
4. Derive **access patterns** from the flows: query, frequency, latency budget, result size. Model to fit these; a model chosen before the queries is a guess.
5. Define **lifecycle** per entity: creation, mutation, archival, deletion, retention period, legal basis.
6. Define **consistency** per cross-component relationship: strong or eventual; if eventual, the tolerated window and the reconciliation mechanism (outbox, saga, CDC, reconciliation job) — named, not implied.
7. Record **volume and growth** with the source of the numbers.
8. State **integrity rules** and where each is enforced.
9. Decide **identifiers**: format, generation point, external exposure.
10. If existing data must change, write the **migration plan**: strategy, ordered reversible steps, backfill (volume/duration/throttle/restart), validation before cutover, rollback with the explicit point of no return, downtime or the zero-downtime argument, dual-run duration, cleanup with a named confirmer.
11. State how data reaches analytics/reporting and the freshness contract.

**P9:** report ownership conflicts, unclassified attributes, and entities lacking a retention answer, then `Next: /sa:gen-security-design`.
