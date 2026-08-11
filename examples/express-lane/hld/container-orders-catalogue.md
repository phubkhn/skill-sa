# HLD Catalogue — express-lane

## Elements

| Element | Responsibility | Owner | Data / contract |
|---|---|---|---|
| `order-intake` | Accept, deduplicate, persist and expose order status | Orders | Owns Order and IdempotencyKey; `interfaces/order-intake-api.yaml` |
| `order-events` | Durable handoff of accepted orders | Platform | `interfaces/order-intake-events.yaml` |
| `orders-db` | Store order state, keys and outbox | Orders | Storage only; no public contract |
| `fulfilment-service` | Process accepted orders | Fulfilment | Consumes `order.accepted`; updates through intake API |
| `recon-batch` | Safety-net duplicate reconciliation | Operations | Read-only access to replica |

## Relationships

| From → to | Mechanism and purpose | Failure behaviour |
|---|---|---|
| client → `order-intake` | HTTPS; submit and query | Client retries with the same idempotency key |
| `order-intake` → `orders-db` | JDBC; commit order + key + outbox atomically; 120 ms budget | Fail fast with 503; no acknowledgement before commit |
| `order-intake` → `order-events` | Kafka outbox relay; publish acceptance | Relay retries; acknowledgement remains valid |
| `order-events` → `fulfilment-service` | Kafka; at-least-once delivery | Consumer dedups; poison messages go to DLQ |
| `fulfilment-service` → `order-intake` | HTTPS; idempotent state update; 500 ms timeout | Three bounded retries, then DLQ |
| `recon-batch` → `orders-db` | JDBC read replica | Retry on next scheduled run |

## Structural checks

- One writer per entity: `order-intake`.
- No synchronous fulfilment dependency on the acknowledgement path.
- No container-level dependency cycle on the user request path.
- `recon-batch` is pre-existing and unchanged; it remains as a safety net.
