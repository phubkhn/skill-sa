# HLD Catalogue — container — express-lane

| Field | Value |
|---|---|
| Artifact | HLD Catalogue (container) |
| Version | 2 |
| Status | Accepted |
| Last Updated | 2026-03-06 |
| Updated By | J. Okafor |
| Trace ID | TR-express-lane-001 |
| Change Type | Update |
| Ref | none |

Accompanies `container-orders.puml` v2.

## Elements

| Element | Type | Responsibility | Owns (data) | Technology | Owning team | Interface spec | Drivers addressed |
|---|---|---|---|---|---|---|---|
| `order-intake` | service | Accept, validate, dedup and durably record an order, then publish its acceptance | `Order` (write), `IdempotencyKey` | Java / Spring | Orders | `06-interfaces/order-intake-api.yaml` | QA-PERF-01, QA-AVAIL-01, QA-DATA-01 |
| `order-service` | service | Serve order state and manage the order lifecycle after acceptance | `OrderState` | Java / Spring | Orders | `06-interfaces/order-service-api.yaml` | QA-AVAIL-01 |
| `order-events` | topic | Durable handoff of acceptance to downstream processing | — | Kafka | Platform | `06-interfaces/order-intake-events.yaml` | QA-AVAIL-01 |
| `orders-db` | data store | Persist orders and idempotency keys | — (storage for the above) | PostgreSQL 15 | Orders | `N/A — data store, no programmatic contract of its own` | QA-AVAIL-01 |
| `fulfilment-service` | service | Process accepted orders | `Fulfilment` | Java | Fulfilment | `N/A — consumer only, publishes no contract in this scope` | — |
| `recon-batch` | job | Nightly duplicate reconciliation | — | Python | Ops | `N/A — scheduled job, no callable interface` | — |

## Relationships

| From | To | Protocol | Sync/Async | Purpose | Latency budget | Failure behaviour |
|---|---|---|---|---|---|---|
| client | `order-intake` | HTTPS | sync | submit an order | 800 ms (end-to-end driver) | client retries with the same idempotency key |
| `order-intake` | `orders-db` | JDBC | sync | durable write + dedup lookup | 120 ms (50 ms dedup + 70 ms write) | fail-fast, return 503; no acknowledgement is issued |
| `order-intake` | `order-events` | Kafka | async | publish acceptance | 80 ms | transactional outbox — the order is written and the publish is retried; acceptance is never lost |
| `order-events` | `fulfilment-service` | Kafka | async | deliver acceptance | n/a (not on the ack path) | at-least-once; consumer dedups on `orderId`; poison messages to DLQ |
| `fulfilment-service` | `order-service` | HTTPS | sync | update order state | 500 ms | retry with backoff, cap 3; then DLQ |
| client | `order-service` | HTTPS | sync | poll order status | 300 ms | fail-fast |
| `recon-batch` | `orders-db` | JDBC (replica) | sync | nightly read | n/a | job retries next night |

**Budget allocation:** 800 ms end-to-end = 120 ms database + 80 ms publish + 600 ms network, TLS, serialisation and headroom. Measured in the spike at p99 ≈ 90 ms total, so the headroom is deliberate rather than tight.

## Coupling checks

| Check | Result |
|---|---|
| Sync fan-out > 3 | PASS — `order-intake` synchronously calls one element |
| > 5 round trips per user action | PASS — 2 |
| Shared data store | PASS — `orders-db` has one writer on the intake path (`order-intake`); `order-service` writes only `OrderState`, a disjoint set. Reviewed and confirmed acceptable; see review finding F-002 |
| Container-level cycle | PASS — none |
| God component | PASS — largest holds 3 of 9 responsibilities |
| Orphan element | PASS — none |

## Elements tracing to no driver

`recon-batch` traces to no driver in this scope. It pre-exists and is unchanged; not a deletion candidate.
