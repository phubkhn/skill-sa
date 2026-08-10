# ADR-0001 — Decouple order acceptance from fulfilment using a durable event handoff

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-03-02 |
| Deciders | J. Okafor (SA), A. Mensah (Orders), P. Lindqvist (Fulfilment), K. Bauer (Platform) |
| Trace ID | TR-express-lane-001 |
| Drivers addressed | QA-PERF-01, QA-AVAIL-01, F1 |

## Context

Acknowledgement latency is currently bounded by `fulfilment-service` processing time (p99 3.8 s at peak), because `order-service` calls it synchronously before responding. QA-PERF-01 requires p99 < 800 ms and QA-AVAIL-01 requires orders to be accepted while fulfilment is unavailable. Neither is reachable while the acknowledgement waits on downstream work.

Constraints: the existing Kubernetes platform (PLT-004) and a Kafka cluster the platform team already operates. RPO for accepted orders is 0 — an accepted order may never be lost.

What makes this hard: acknowledging before processing changes what the acknowledgement *means* to two first-party clients that currently treat `201 Created` as "this order exists and will be fulfilled".

## Decision

We will accept orders in a dedicated `order-intake` service that persists the order durably and publishes `order.accepted` to a Kafka topic, and `fulfilment-service` will consume that topic asynchronously.

## Options considered

| Option | Summary | Pros | Cons | Why not chosen |
|---|---|---|---|---|
| **A — Async handoff via durable topic** (chosen) | intake persists, publishes, acknowledges | meets both H/H drivers; fulfilment outage does not block acceptance; natural place for dedup | new topic to operate; acknowledgement semantics change for clients; eventual consistency visible to users | — |
| B — Optimise the synchronous path | profile and tune `fulfilment-service`, add caching, raise pod count | no contract change; no new component; smallest delivery risk | p99 3.8 s → 800 ms is a 4.75× improvement with no identified mechanism; and it does not address QA-AVAIL-01 at all, since fulfilment being down still blocks acceptance | cannot meet QA-AVAIL-01 under any amount of tuning — the coupling is the problem, not the speed |
| C — Do nothing | accept the duplicate rate; expand manual reconciliation | zero delivery cost | 1.9% duplicate rate and 3.4× abandonment persist and grow with volume; reconciliation cost scales linearly | the cost of doing nothing already exceeds the cost of A within two quarters |

Option B was the team's initial preference and is not a straw man: it is cheaper, safer to deliver, and would plausibly have satisfied QA-PERF-01 alone. It fails only because QA-AVAIL-01 requires acceptance to survive a fulfilment outage, which no amount of tuning provides.

## Evaluation against drivers

| Driver | Option A | Option B | Option C |
|---|---|---|---|
| QA-PERF-01 (p99 < 800 ms) | met — acknowledgement bounded by a local write plus a publish, ~90 ms measured in the spike | uncertain — requires 4.75× improvement with no identified mechanism | not met |
| QA-AVAIL-01 (accept while fulfilment down) | met — the topic buffers | **not met** — synchronous coupling remains | not met |
| QA-DATA-01 (dedup) | met — dedup at intake, on the write path | possible but retrofitted into a hot synchronous path | not met |
| Cost efficiency | one new service, one topic on an existing cluster | lowest | zero build, rising operational cost |
| Delivery risk | highest — three teams, two breaking client contracts | low | none |

## Consequences

**Positive** — acceptance latency becomes a property of intake alone and is therefore predictable. Fulfilment can be restarted, scaled or deployed without rejecting orders. Dedup lives on the write path, where it can be made correct.

**Negative** — the acknowledgement no longer means the order will be fulfilled, and two first-party clients must change to understand that. Users can observe a window in which an order exists but has not been processed; support must be briefed. Operating a consumer means operating consumer lag, a DLQ, and a poison-message procedure that did not previously exist. Failures now surface asynchronously, where they are harder to attribute to a submission.

**Neutral / follow-on** — `recon-batch` will find fewer duplicates but needs no change. A status endpoint is needed so clients can resolve the acknowledgement into an outcome (ADR-0003).

**What becomes harder later** — reverting to a synchronous model would require both clients to change back. Any future requirement for a synchronous fulfilment answer at submission time is now expensive.

## Compliance / verification

Fitness function, blocking, in CI: an architecture test asserts that no code path in `order-intake` performs a synchronous call to `fulfilment-service`. Proven to fire by a deliberate violation on 2026-03-05.

## Related

Drivers QA-PERF-01, QA-AVAIL-01, F1 · impact analysis §4 (contract impact) · ADR-0002 (dedup mechanism) · ADR-0003 (order status endpoint)
