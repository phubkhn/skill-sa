# Impact Analysis — express-lane

| Field | Value |
|---|---|
| Artifact | Impact Analysis |
| Version | 1 |
| Status | Accepted |
| Last Updated | 2026-02-26 |
| Updated By | J. Okafor |
| Trace ID | TR-express-lane-001 |
| Change Type | Initial |
| Ref | none |

**Gate G1:** PASSED — out-of-scope list non-empty (6 items), stakeholders named with concerns, both H/H attributes have measured scenarios.

## 1. Baseline

Source of current-state knowledge: repository `src/orders/` read on 2026-02-25, plus A. Mensah (order-service owner) confirming behaviour on 2026-02-11. No existing architecture documentation — this analysis establishes the baseline.

- `order-service` (`src/orders/`, Java, 4 pods) exposes `POST /orders`, writes synchronously to `orders-db`, then calls `fulfilment-service` synchronously before returning. The acknowledgement therefore waits on fulfilment — this is the root cause.
- `orders-db` (PostgreSQL 15, single primary + read replica). Sole writer: `order-service` (`src/orders/repo.java:1`–`:340`, no other write path found).
- `fulfilment-service` — synchronous consumer today; p99 processing 3.8 s at peak (Grafana `fulfilment-latency`, February).
- `recon-batch` — nightly, reads `orders-db` replica, flags duplicates.
- `partner-gateway` — separate submission path, out of scope.

## 2. Impacted elements

| Element | Type | Impact | Nature of change | Breaking? | Owner team | Effort | Trace ID |
|---|---|---|---|---|---|---|---|
| `order-service` | component | Change | submission path becomes async; loses the synchronous fulfilment call | No (see contract impact) | Orders | M | TR-express-lane-001 |
| `order-intake` | component | Add | new: validates, dedups, persists, publishes | — | Orders | L | TR-express-lane-001 |
| `order-events` | broker topic | Add | new topic carrying `order.accepted` | — | Platform | S | TR-express-lane-001 |
| `orders-db` | data store | Change | new `idempotency_key` column + index; new `intake_status` | No | Orders | S | TR-express-lane-001 |
| `fulfilment-service` | component | Change | becomes an event consumer instead of being called synchronously | No — same payload | Fulfilment | M | TR-express-lane-001 |
| `recon-batch` | component | None (verified) | reads only `orders` table columns unchanged by this work; verified by reading `batch/recon.sql:12`–`:48` and confirmed with the Ops owner 2026-02-25 | — | Ops | — | TR-express-lane-001 |
| `partner-gateway` | component | None (verified) | writes via its own path to `order-service`'s internal API, which is unchanged; verified `src/partner/client.java:88` | — | Partners | — | TR-express-lane-001 |
| `reporting-warehouse` | system | Unknown (investigate) | unclear whether its ETL reads `orders` on a schedule that assumes fulfilment has completed | ? | Data | ? | TR-express-lane-001 |

## 3. New elements required

| Element | Type | Why |
|---|---|---|
| `order-intake` | service | owns acceptance and dedup; the decoupling point |
| `order-events` | topic | durable handoff to fulfilment |
| `idempotency_key` index | database index | dedup lookup within the 50 ms budget |

## 4. Contract impact

| Interface | Consumer | Change | Breaking for this consumer? |
|---|---|---|---|
| `POST /orders` | web client | response now `202 Accepted` with a status URL, not `201 Created` with a fulfilled order | **Yes** — the client branches on 201 |
| `POST /orders` | mobile client | as above | **Yes** |
| `POST /orders` | `partner-gateway` | unchanged — uses the internal API | No |

Two breaking consumers. Both are first-party and release on the same cycle; a migration plan per consumer is required before the interface spec is written (Standard 09 rule 3).

## 5. Data impact

New column `idempotency_key VARCHAR(64)` with a unique partial index, and `intake_status`. Backfill: `intake_status` defaults to `'fulfilled'` for existing rows — 4.2 M rows, expand-contract, reversible. No data is moved or deleted.

## 6. Operational impact

New service to deploy, monitor and page on. New broker topic — the platform team has an existing Kafka cluster, so no new infrastructure class, but consumer lag and DLQ become new things to watch. Two new alerts, one new dashboard, one new runbook (DLQ drain).

## 7. Organisational impact

Three teams: Orders (both changed components), Fulfilment (consumer rewrite), Platform (topic provisioning). Sequencing constraint: the topic must exist before either side can be tested, so Platform's work is on the critical path despite being the smallest.

## 8. Decommissioning

| Element | Who still calls it | How they stop | Migration deadline | Switch-off date | Data disposition | Confirms nothing reads it |
|---|---|---|---|---|---|---|
| synchronous `order-service` → `fulfilment-service` call | `order-service` only | removed in the same release that adds the consumer | 2026-05-01 | 2026-05-15 | n/a — no data | A. Mensah |

## 9. Stale artifacts

None — no prior design artifacts exist.

## 10. Effort & sequencing

| # | Work | Depends on | Size |
|---|---|---|---|
| 1 | Provision `order-events` topic | — | S |
| 2 | Build `order-intake` | 1 | M |
| 3 | Fulfilment consumer | 1 | M |
| 4 | Client migration (web, mobile) | 2 | M |
| 5 | Remove synchronous call | 3, 4 | S |

2 and 3 parallelise. 5 must be last.

## 11. Candidate risks

- R1 — `reporting-warehouse` impact unknown; if its ETL assumes fulfilment completion, the change breaks reporting silently (from the `Unknown (investigate)` row)
- R2 — two breaking client contracts requiring coordinated release (from §4)
- R3 — peak concurrency assumption A1 unvalidated beyond 18 months (from intent)
