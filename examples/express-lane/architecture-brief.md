# Architecture Brief — express-lane

| Field | Value |
|---|---|
| Status | Accepted |
| Updated | 2026-03-12 |
| Owner | J. Okafor |
| Sources | `src/orders/`; Grafana `fulfilment-latency`; A. Mensah, 2026-02-11 |

## 1. Problem and outcome

At the 11:00–13:00 peak, order acknowledgement takes 4–40 seconds because submission waits for fulfilment. Clients time out and retry, producing a 1.9% duplicate rate and 12 minutes of manual reconciliation per duplicate.

The outcome is to durably accept an order within a bounded time even when fulfilment is unavailable, without creating duplicates on retry.

## 2. Scope

**In:** client submission and status contract, deduplication, durable acceptance, handoff to fulfilment, and order-state updates.

**Out:** pricing, inventory, fulfilment internals, historical-order migration, partner submission, and UI work beyond acknowledgement wording.

## 3. Drivers and constraints

| ID | Driver or constraint | Target / effect | Source |
|---|---|---|---|
| D1 | Acknowledgement latency | p99 < 800 ms at 500 concurrent submissions | Product, 2026-02-24 |
| D2 | Acceptance availability | Accept while fulfilment is unavailable; RPO 0 for accepted orders | Operations, 2026-02-19 |
| D3 | Duplicate prevention | < 0.01% duplicates; recognise retries for at least 24 h | Current 1.9% baseline |
| C1 | Platform | Existing Kubernetes and Kafka platform | PLT-004 |
| C2 | Data residency | Order data stays in-region | DPA clause 7.2 |

## 4. Current state and impact

`order-service` currently writes the order, calls `fulfilment-service` synchronously, and responds only after fulfilment. Source: `src/orders/`, confirmed by A. Mensah on 2026-02-11. Fulfilment p99 is 3.8 s at peak, so tuning alone cannot make acceptance independent of a fulfilment outage.

The change affects the web and mobile clients, the Orders and Fulfilment teams, `orders-db`, and the platform-owned Kafka cluster. The partner path and nightly reconciliation job remain unchanged; reconciliation continues as a safety net.

## 5. Options and recommendation

| Option | Strengths | Costs / risks | Reversibility |
|---|---|---|---|
| Durable asynchronous intake | Meets D1 and D2; dedup occurs on the write path | New service/topic; acknowledgement semantics change; eventual consistency | Medium: clients and fulfilment must migrate back |
| Optimise the synchronous path | Smallest delivery change; no new component | Cannot accept while fulfilment is down; requires unexplained 4.75× latency improvement | High |
| Do nothing | No build cost | Duplicate and abandonment costs continue to grow | Immediate |

**Recommendation:** accept and deduplicate orders in `order-intake`, commit the order and outbox record atomically, then hand off to fulfilment through `order-events`.

**Deciding trade-off:** only asynchronous durable acceptance meets D2; tuning cannot remove the synchronous availability dependency.

**What would change the decision:** a requirement that acknowledgement must mean fulfilment completed rather than order accepted.

## 6. Proposed architecture

`order-intake` owns order acceptance and status. It exposes `POST /orders` and `GET /orders/{id}`, writes `Order` and `IdempotencyKey` to `orders-db`, and publishes `order.accepted` from a transactional outbox. `fulfilment-service` consumes the event and updates state through an internal idempotent endpoint owned by `order-intake`.

See `hld/container-orders.puml` and `flows/client-submit-express-order.puml`.

## 7. Interfaces and data

| Boundary / entity | Producer or owner | Consumers | Contract / consistency / lifecycle |
|---|---|---|---|
| Order API | `order-intake` | web, mobile, fulfilment | `interfaces/order-intake-api.yaml`; 202 means accepted, not fulfilled |
| `order.accepted` | `order-intake` | `fulfilment-service` | `interfaces/order-intake-events.yaml`; at-least-once, consumer dedup by `orderId` |
| `Order` | `order-intake` | clients, fulfilment, reconciliation | single writer; 7-year retention |
| `IdempotencyKey` | `order-intake` | none outside intake | unique; 30-day rolling retention |

## 8. Cross-cutting concerns

| Concern | Design response | Remaining gap |
|---|---|---|
| Security | Existing OIDC; client and internal scopes separated; data stays in-region | Threat model not needed: no new trust boundary beyond the existing authenticated API and platform Kafka |
| Resilience | Transactional outbox; safe client retries; at-least-once consumer; bounded internal update retries | DLQ drain procedure must be written before production |
| Observability | Ack latency, duplicate rate, outbox lag, consumer lag, DLQ depth | Alert thresholds must be validated in load test |
| Cost | One small stateless service and one topic on existing platforms | Measure run cost during the spike; no separate cost model justified |
| Delivery | Platform topic first; intake and fulfilment can then proceed in parallel; clients migrate before old path removal | Three-team release coordination |

## 9. Decisions, risks, and open questions

| Type | Item | Owner / next action |
|---|---|---|
| Decision | Decouple acceptance with durable event handoff | `decisions/ADR-0001-async-order-intake.md` |
| Risk | Clients may interpret 202 as fulfilment complete | Orders team: update contract examples and release notes |
| Risk | Poison messages can stall fulfilment | Fulfilment team: write and test DLQ drain runbook |
| Assumption | Peak concurrency remains ≤ 500 for the first release | Product: validate quarterly |

## 10. Recommended next steps

1. Close the DLQ runbook condition from the architecture review.
2. Run a 500-concurrent load test and a fulfilment-outage test before release.
