# Worked example — express-lane

This example shows the simplified flow for a cross-team change that alters a public contract.

1. `/sa:architect` creates one `architecture-brief.md` containing the problem, measurable drivers, current-state impact, options, recommendation, cross-cutting concerns and delivery implications.
2. The design justifies specialised artifacts for one durable decision, one container view, one significant runtime flow, API and event contracts, and cross-boundary data ownership.
3. `/sa:review` reviews only those files and cites stable sections. Every referenced file is present in the example.

## Files

| File | Why it exists |
|---|---|
| `architecture-brief.md` | Shared design baseline and recommendation |
| `decisions/ADR-0001-async-order-intake.md` | Consequential async-acceptance decision |
| `hld/container-orders.puml` | Cross-team boundaries and dependencies |
| `hld/container-orders-catalogue.md` | Relationship details that would clutter the diagram |
| `flows/client-submit-express-order.puml` | Failure, retry and durability behaviour |
| `interfaces/order-intake-api.yaml` | Client and fulfilment contract |
| `interfaces/order-intake-events.yaml` | At-least-once event contract |
| `data/data-design.md` | Single-writer ownership, lifecycle and coexistence |
| `reviews/design-review-2026-03-14.md` | Evidence-based readiness verdict |

`sa-config.yaml` is included only to demonstrate optional configuration. The same work could start without it.
