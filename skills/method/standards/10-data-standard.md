# Standard 10 — Data Design

**Artifacts:** `07-data/data-model.puml`, `07-data/data-design.md`, `07-data/migration-plan.md`
**Templates:** `templates/data-design.md`, `templates/migration-plan.md`
**Purpose:** data outlives every service that touches it. Design it deliberately.

## Required content

| Section | Content |
|---|---|
| Conceptual model | entities, relationships, cardinality — technology-free |
| Ownership | for each entity: the single owning component, the writers, the readers, the access path |
| Classification | sensitivity per attribute: public / internal / confidential / restricted; PII flags; regulatory tags |
| Lifecycle | creation, mutation, archival, deletion — with retention period and legal basis |
| Consistency | per relationship: strong or eventual; if eventual, the tolerated window and the reconciliation mechanism |
| Volume & growth | current rows/size, growth rate, projected 12–36 months |
| Access patterns | the queries that matter, with expected frequency and latency budget |
| Storage decisions | store type per entity group, with the ADR that justifies it |
| Integrity | keys, uniqueness, referential rules, and where they are enforced (DB vs application) |
| Migration | see below |
| Reporting/analytics | how data leaves the operational store, and the freshness contract |

## Rules

1. **One writer per data element.** Multiple writers require an ADR and an explicit conflict-resolution rule.
2. **No shared database between components.** Sharing a store is sharing a schema — that is one component wearing two names.
3. **Every entity has a retention and deletion answer**, including "kept forever, because <legal basis>".
4. **PII is identified at attribute level**, not "this table has some PII".
5. **Access patterns drive the model.** Model chosen before knowing the queries is a guess.
6. **Cross-store consistency is designed, not hoped for** — name the mechanism (outbox, saga, CDC, reconciliation job).
7. **Identifiers:** state format, generation point, and whether they are exposed externally. Never expose a sequential internal id in a public contract without deciding to.

## Migration plan requirements

| Item | Requirement |
|---|---|
| Strategy | big-bang / expand-contract / dual-write / CDC-backfill — with the reason |
| Steps | ordered, each independently deployable and reversible where possible |
| Backfill | volume, duration, throttling, restartability |
| Validation | how correctness is proven before cutover (row counts, checksums, sampling, shadow reads) |
| Rollback | exact procedure and the point of no return, stated explicitly |
| Downtime | required window, or the argument for zero-downtime |
| Dual-run | how long both paths run, and who decides to stop |
| Cleanup | when the old structure is dropped, and who confirms nothing reads it |

## Coexistence with the system being replaced

A migration plan moves data. A coexistence plan governs the period — usually much longer than anyone budgets — where the old and the new system are both live. State which pattern is in use and what it implies:

| Pattern | What it means | What it demands |
|---|---|---|
| Strangler fig | new system takes over capability by capability behind a routing layer | the routing rule, per capability, and who can change it |
| Anti-corruption layer | a translation boundary keeps the legacy model out of the new one | where the layer lives, what it translates, when it is deleted |
| Dual-write | both systems are written to during transition | the reconciliation mechanism and the drift alarm — dual-write without reconciliation silently diverges |
| Read replica / CDC | new system reads a projection of legacy data | freshness contract and what happens when the pipeline stalls |
| Big-bang cutover | one switch, one moment | the rollback window and the point of no return |

Every coexistence pattern states: **which system is the source of truth for each entity during the transition**, how conflicts are resolved, and the date the arrangement ends. A coexistence period with no end date is the new permanent architecture, and should be designed as one.

## Anti-patterns

- A data model with no owner column
- Dual-write with no reconciliation job and no drift metric
- A coexistence arrangement with no stated end date
- Retention "as per policy" with no policy referenced
- Migration with no rollback and no stated point of no return
- Analytics reading directly from the operational store with no contract

## Checklist

Self-assess against this list before reporting the artifact done. Report pass/fail **per item** — never a silent pass. A failed item becomes an OPEN item with an owner; it is not deleted to make the list pass.

- [ ] Conceptual model is technology-free with cardinality on every relationship
- [ ] Exactly one owning component per entity
- [ ] Every attribute classified for sensitivity; PII flagged at attribute level
- [ ] Access patterns derived from actual flows, with frequency and latency budget
- [ ] Model fits the access patterns
- [ ] Every entity has retention, deletion rule, and legal basis
- [ ] Cross-component consistency stated as strong or eventual, with a named mechanism
- [ ] Eventual-consistency windows and their visible effects stated
- [ ] Volume and growth numbers carry their source
- [ ] Integrity rules state where they are enforced
- [ ] Identifier format, generation point, and external exposure decided
- [ ] Storage choices reference an ADR
- [ ] Analytics/downstream path has a freshness contract
- [ ] Migration plan present where existing data changes
- [ ] Migration is reversible, or the point of no return is explicit
- [ ] Migration has pre-cutover validation and a named cleanup confirmer
- [ ] Coexistence pattern named where an old system stays live, with the source of truth per entity, the conflict rule, and an end date
