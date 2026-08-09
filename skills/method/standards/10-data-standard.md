# Standard 10 — Data Design

**Artifacts:** `07-data/data-model.puml`, `data-ownership.md`, `migration-plan.md`
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

## Anti-patterns

- A data model with no owner column
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
