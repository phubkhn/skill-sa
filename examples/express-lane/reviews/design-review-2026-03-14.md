# Design Review — express-lane — 2026-03-14

| Field | Value |
|---|---|
| Reviewer | M. Haddad |
| Scope | Express-order acceptance and fulfilment handoff |
| Artifacts reviewed | architecture brief, ADR-0001, HLD + catalogue, submission flow, API, event contract, data design |
| Verdict | READY WITH CONDITIONS |

## Verdict

READY WITH CONDITIONS — no Blockers, one Major.

Condition: the Fulfilment team must write and exercise the DLQ drain runbook before production.

## Findings

| ID | Severity | Finding | Evidence | Rule / driver | Recommendation | Owner |
|---|---|---|---|---|---|---|
| F-001 | Major | Poison messages are detected and routed to a DLQ, but recovery is still an open procedure. | `flows/client-submit-express-order.puml`, “Poison message”; `architecture-brief.md` §8 | Operability: a designed failure needs an executable recovery path | Write the drain, replay and validation procedure; exercise it once in staging | Fulfilment team |
| F-002 | Minor | Alert thresholds are proposed but not yet validated under representative load. | `architecture-brief.md` §8 | D1 and operability | Validate ack latency and lag thresholds during the 500-concurrent test | Orders team |

## Driver coverage

| Driver | Mechanism | Evidence | Confidence |
|---|---|---|---|
| D1 p99 acknowledgement < 800 ms | User path contains one bounded database transaction; publish and fulfilment are off-path | HLD catalogue §Relationships; submission flow steps 1–7 | Medium until load test |
| D2 accept while fulfilment is unavailable, RPO 0 | Commit order and outbox atomically before 202; Kafka buffers fulfilment outage | ADR-0001; submission flow “Publish or fulfilment unavailable” | High |
| D3 duplicate rate < 0.01% | Client idempotency key plus unique owned record; duplicate returns original order | API `Idempotency-Key`; submission flow “Duplicate submission” | High |

## Consistency

- ADR, HLD and flow all keep fulfilment off the acknowledgement path.
- Participant and contract names agree across HLD, flow, OpenAPI and AsyncAPI.
- `order-intake` is the sole writer of Order state; fulfilment uses the internal API.
- 202 semantics are explicit in the brief, ADR and API example.

## What is good

The design is small and directly tied to three drivers. The transactional outbox has a specific purpose—RPO 0 without synchronous fulfilment—and the retry and ownership rules are explicit at each boundary.

## Not reviewed

Fulfilment internals, pricing and inventory, partner submission, production capacity, and the implementation of the existing retention job.
