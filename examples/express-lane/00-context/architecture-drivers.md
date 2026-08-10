# Architecture Drivers — express-lane

| Field | Value |
|---|---|
| Artifact | Architecture Drivers |
| Version | 2 |
| Status | Accepted |
| Last Updated | 2026-02-24 |
| Updated By | J. Okafor |
| Trace ID | TR-express-lane-001 |
| Change Type | Update |
| Ref | none |

## 1. Structure-shaping functionality

| ID | Capability | Why it shapes structure |
|---|---|---|
| F1 | Accept and acknowledge an order while downstream processing is unavailable | forces the acknowledgement to be decoupled from fulfilment — this is the whole design |
| F2 | Recognise a resubmitted order as the same order | forces an idempotency key in the contract and a dedup store at intake |

## 2. Quality attribute scenarios

### QA-PERF-01 — Performance (Business: H | Difficulty: H)

| Part | Value |
|---|---|
| Source | submitting client |
| Stimulus | submits an order |
| Environment | peak window, 500 concurrent submissions |
| Artifact | submission and acknowledgement path |
| Response | order is durably recorded and acknowledged |
| Measure | **p99 acknowledgement latency < 800 ms; p99.9 < 2 s; 0 requests dropped** |

**Rationale** — 800 ms from R. Silva (product), 2026-02-24, resolving Q1: below 1 s clients do not perceive waiting, and the current client timeout is 30 s so the headroom is large.
**Tactics** — decouple acknowledgement from downstream processing; bounded intake queue with backpressure.
**Verify by** — load test at 500 concurrent, prod-like topology, pre-release and nightly.

### QA-AVAIL-01 — Availability (Business: H | Difficulty: H)

| Part | Value |
|---|---|
| Source | any client |
| Stimulus | submits an order while the fulfilment pipeline is unavailable |
| Environment | fulfilment down, intake healthy |
| Artifact | submission path |
| Response | order is accepted and acknowledged; processing resumes when fulfilment recovers |
| Measure | **99.9% monthly acceptance success; RTO ≤ 15 min; RPO = 0 (no accepted order lost)** |

**Rationale** — RPO 0 is non-negotiable: an accepted order that vanishes is worse than a rejected one. Source: operations lead, 2026-02-19.
**Tactics** — durable write before acknowledgement; queue-based handoff to fulfilment.
**Verify by** — chaos experiment killing the fulfilment consumer during load; failover drill quarterly.

### QA-DATA-01 — Data integrity (Business: H | Difficulty: M)

| Part | Value |
|---|---|
| Source | client with an unreliable network |
| Stimulus | resubmits an order it believes failed, within 24 h |
| Environment | normal or peak |
| Artifact | intake dedup |
| Response | the resubmission returns the original order's acknowledgement; no second order is created |
| Measure | **duplicate order rate < 0.01% of peak-window submissions; dedup window ≥ 24 h** |

**Rationale** — current rate 1.9%; < 0.01% is roughly one per fortnight, absorbable by existing reconciliation.
**Verify by** — integration test replaying identical submissions; duplicate-rate metric with an alert.

### Attribute sweep

| Attribute | In play | Note |
|---|---|---|
| Performance | yes | QA-PERF-01 |
| Scalability | yes | covered by QA-PERF-01's peak figure |
| Availability | yes | QA-AVAIL-01 |
| Reliability | yes | QA-DATA-01 |
| Resilience / recoverability | yes | QA-AVAIL-01 |
| Security | N/A — no change to the authentication model or data classification; existing controls apply unchanged (confirmed K. Bauer, 2026-02-20) |
| Privacy | N/A — no new personal data collected or exposed |
| Auditability | yes (M/L) | acceptance events must be auditable; existing audit log extended |
| Modifiability | N/A — no anticipated variation in this path |
| Testability | yes (M/M) | the async path must be testable without a live fulfilment pipeline |
| Deployability | N/A — existing pipeline |
| Operability / observability | yes (H/M) | new async path needs lag and DLQ visibility |
| Portability | N/A — platform is a given constraint |
| Interoperability | yes (M/L) | client contract changes semantically |
| Usability | N/A — no UI change beyond copy |
| Accessibility | N/A — no UI change |
| Localisation | N/A — single locale |
| Compliance | N/A — in-region constraint already satisfied |
| Cost efficiency | yes (M/M) | new broker and consumer add run cost |
| Sustainability | N/A — not reported on by this organisation |

## 3. Priority matrix

| Attribute | Business importance | Architectural difficulty | Quadrant |
|---|---|---|---|
| Performance | H | H | **H/H** |
| Availability | H | H | **H/H** |
| Data integrity | H | M | H/M |
| Observability | H | M | H/M |
| Testability | M | M | M/M |
| Cost efficiency | M | M | M/M |
| Auditability | M | L | M/L |
| Interoperability | M | L | M/L |

Two attributes in H/H. Within the ≤5 guidance; no forced ranking needed.

## 4. Conflict log

| Conflict | Attributes | Resolution | ADR |
|---|---|---|---|
| Acknowledging before processing means acknowledging something that may later fail | QA-PERF-01 vs QA-AVAIL-01 semantics | acknowledgement means *accepted*, not *fulfilled*; the contract and the client copy must both say so | ADR-0001 |
| A 24 h dedup window costs storage and adds a lookup to the hot path | QA-DATA-01 vs QA-PERF-01 | dedup lookup budgeted at ≤ 50 ms of the 800 ms | ADR-0002 |

## 5. Unknown measures

None outstanding. Q1 resolved on 2026-02-24, which is what unblocked G1.
