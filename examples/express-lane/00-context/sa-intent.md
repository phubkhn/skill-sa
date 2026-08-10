# Solution Intent — express-lane

| Field | Value |
|---|---|
| Artifact | Solution Intent |
| Version | 2 |
| Status | Accepted |
| Last Updated | 2026-02-18 |
| Updated By | J. Okafor |
| Trace ID | TR-express-lane-001 |
| Change Type | Update |
| Ref | none |

## 1. Problem statement

Orders submitted during the 11:00–13:00 peak are acknowledged between 4 and 40 seconds after submission. Above roughly 300 concurrent submissions the acknowledgement can exceed the client's own 30-second timeout, at which point the client resubmits. In February, 1.9% of peak-window orders were duplicates created this way; each one costs approximately 12 minutes of manual reconciliation, and two reached fulfilment before being caught.

Customers who experience a slow acknowledgement abandon at 3.4× the baseline rate.

## 2. Desired outcome

A submitting client learns within a bounded, predictable time that its order has been accepted, during the peak window, without the system having completed downstream processing first. Duplicate orders caused by client resubmission fall to effectively zero.

Judged by: duplicate-order rate in the peak window, and peak-window abandonment rate.

## 3. Scope

**In scope**

- The submission and acknowledgement path for orders
- Duplicate detection at intake
- The client-facing contract for submission

**Out of scope**

- Order fulfilment, pricing and inventory logic — unchanged
- The batch reconciliation job — it keeps its current schedule and behaviour
- Any change to the customer-facing UI beyond the acknowledgement copy
- Migration of the existing order history
- The partner-integration path (`partner-gateway`) — partners submit through a different contract with different tolerances, and bringing them in would double the scope
- Non-peak-window performance — it is already within target

## 4. Actors & stakeholders

See `stakeholders.md`. Summary: submitting clients (want a fast, trustworthy acknowledgement), operations (want the duplicate reconciliation work to stop), the fulfilment team (want no change to what reaches them), and the platform team (must operate whatever this becomes).

## 5. Existing landscape

| Element | Disposition | Note |
|---|---|---|
| `order-service` | integrate | current synchronous submission endpoint; source: `src/orders/` and A. Mensah, 2026-02-11 |
| `orders-db` (PostgreSQL) | integrate | order storage; sole writer is `order-service` |
| `partner-gateway` | avoid | explicitly out of scope |
| `recon-batch` | avoid | nightly duplicate reconciliation; will have less to do, needs no change |

## 6. Constraints

**Given**

| Constraint | Source |
|---|---|
| Must run on the existing Kubernetes platform | Platform team standard PLT-004 |
| Must reuse the existing OIDC identity provider | Security policy SEC-011 |
| Order data stays in-region | Legal, DPA clause 7.2 |

**Chosen**

| Constraint | Chosen by | Revisit when |
|---|---|---|
| PostgreSQL remains the system of record for orders | this design | a driver requires write throughput above 2,000/s |

## 7. Assumptions

| # | Assumption | Safe / risky |
|---|---|---|
| A1 | Peak concurrency will not exceed 800 within 18 months | risky — → risk register |
| A2 | Clients will adopt a new acknowledgement semantic within one release cycle | risky — → risk register |
| A3 | The existing OIDC provider can issue tokens for a new service without a procurement step | safe — confirmed by K. Bauer, 2026-02-12 |

## 8. Success criteria (architectural)

- Acknowledgement latency is bounded by design, not by downstream load
- The submission path has one, and only one, writer of order records
- Duplicate submission is handled at intake, not by a downstream batch job

## 9. Open questions

| # | Question | Owner | By |
|---|---|---|---|
| Q1 | What acknowledgement latency do clients actually need — is 500 ms materially better than 2 s for them? | R. Silva (product) | 2026-02-25 |
| Q2 | Does any consumer depend on the acknowledgement implying downstream completion? | A. Mensah | 2026-02-22 |

## 10. Glossary

| Term | Meaning here |
|---|---|
| Acknowledgement | the system's confirmation that an order has been durably accepted; **not** a statement that it has been fulfilled |
| Peak window | 11:00–13:00 local time on business days |
| Duplicate | two order records originating from one client intent |
