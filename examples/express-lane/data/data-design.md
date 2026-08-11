# Data Design — express-lane

## Ownership

| Entity | Authoritative owner and writer | Readers | Retention |
|---|---|---|---|
| Order | `order-intake` | clients, `fulfilment-service`, `recon-batch` | 7 years; tax obligation |
| IdempotencyKey | `order-intake` | `order-intake` only | 30 days rolling |
| ProcessedStateEvent | `order-intake` | `order-intake` only | 30 days rolling |

`order-intake` is the only writer to these entities. `fulfilment-service` changes order status through the idempotent internal API; it never writes `orders-db` directly.

## Classification and lifecycle

`Order.customerId` is confidential personal data. Order items are confidential business data. Idempotency keys and processed event IDs are internal identifiers. All data remains in-region.

Orders move through `accepted → processing → fulfilled | rejected`. Deletion occurs after the seven-year retention period through the existing Orders retention job. Idempotency and processed-event records expire automatically after 30 days.

## Consistency

Acceptance is strongly consistent: the order and outbox record commit in one database transaction before the 202 response. Fulfilment is eventually consistent. The normal target is under five minutes; consumer lag above five minutes alerts the Fulfilment team. Internal state updates are idempotent by `eventId`.

## Migration

No historical data migration is required. The new columns and tables use expand-contract deployment. The old synchronous path remains available until web and mobile clients accept the 202 semantics, then is removed in a later release. During coexistence, `order-intake` is the source of truth for newly submitted orders; the existing path remains authoritative only for submissions received through it. Coexistence ends by 2026-05-15.
