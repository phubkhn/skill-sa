# ADR-0001 — Decouple order acceptance from fulfilment

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-03-02 |
| Deciders | J. Okafor, A. Mensah, P. Lindqvist, K. Bauer |

## Decision question

How should the system durably accept an order within 800 ms when fulfilment may be unavailable?

## Context

The current synchronous call to fulfilment has a p99 of 3.8 seconds and makes acceptance unavailable whenever fulfilment is down. The design requires p99 acknowledgement under 800 ms, RPO 0 for accepted orders, and safe duplicate retries.

## Options considered

| Option | Driver fit | Cost and risk | Reversibility |
|---|---|---|---|
| Durable asynchronous intake | Meets latency and outage-independence; dedup on write path | New service/topic; clients adopt 202 semantics; eventual consistency | Medium |
| Optimise synchronous fulfilment | Smallest delivery change | Cannot accept during fulfilment outage; needs unexplained 4.75× latency improvement | High |
| Do nothing | No build cost | 1.9% duplicates and abandonment continue | Immediate |

## Decision

We will let `order-intake` atomically persist the order and an outbox record, return `202 Accepted`, and publish `order.accepted` to `order-events` for asynchronous fulfilment.

## Consequences

**Positive:** acknowledgement no longer depends on fulfilment; accepted orders cannot be lost; duplicate retries return the original order.

**Negative:** clients must distinguish accepted from fulfilled; users can observe eventual consistency; the teams must operate consumer lag, a DLQ and a poison-message procedure.

Reverting requires coordinated client and fulfilment changes. Reconsider if acknowledgement must mean fulfilment completed.

## Compliance

An architecture test must prevent synchronous calls from the submission path to `fulfilment-service`. Load and outage tests must demonstrate p99 < 800 ms and continued acceptance while fulfilment is stopped.

## Related

`architecture-brief.md` §3–§6; `hld/container-orders.puml`; `flows/client-submit-express-order.puml`.
