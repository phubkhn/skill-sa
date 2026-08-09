# Standard 13 — Resilience, Capacity & Operability

**Artifact:** `08-crosscutting/resilience-design.md`
**Purpose:** decide what happens when things fail — because they will — and prove the system fits the load.

## Required content

| Section | Content |
|---|---|
| Availability targets | per capability, with the measurement definition, RTO and RPO |
| Dependency map | every dependency with criticality: hard (cannot function) / soft (degrades) / optional |
| Failure mode analysis | table below, one row per credible failure |
| Degradation modes | what the system still does when each dependency is down |
| Resilience tactics | timeouts, retries + backoff + jitter, circuit breakers, bulkheads, rate limiting, backpressure, caching, queuing, idempotency, dead-lettering |
| Capacity | expected and peak load, per-component sizing, headroom, scaling trigger and limit |
| Recovery | backup/restore, failover procedure, data reconciliation after split-brain, replay procedures |
| Operability | deployment strategy, rollback, feature flags, config change safety, runbooks needed |
| Verification | how resilience will be tested — load, chaos, failover drill, restore drill |

## Failure mode table

| ID | Failure | Trigger | Blast radius | Detection | Automatic response | Manual response | User-visible effect | Residual risk |
|---|---|---|---|---|---|---|---|---|

Cover at minimum: each dependency unavailable · each dependency slow · partial network failure · data store failover · message broker unavailable · consumer lag/backlog · poison message · duplicate delivery · clock skew · deploy of a bad version · configuration error · resource exhaustion (cpu/memory/connections/disk) · region or zone loss (if applicable).

## Rules

1. **Every remote call has an explicit timeout.** No unbounded waits, anywhere.
2. **Retry only idempotent operations**, always with backoff and jitter, always with a cap. State the total time budget.
3. **Timeout budgets must nest.** A caller's timeout must exceed the sum of its callee's retry budget — or the retries are pointless.
4. **Design the degraded mode, not just the failure.** "Returns 500" is a failure mode, not a design.
5. **Backpressure over buffering.** Unbounded queues convert an outage into a longer outage.
6. **Isolate blast radius** — bulkheads per dependency or per tenant, so one failure does not consume all capacity.
7. **Capacity numbers cite their source.** Measured, extrapolated, or assumed — say which.
8. **Recovery procedures are tested, not documented.** State the drill cadence.
9. **Every automated response has a manual override.**

## Capacity table

| Component | Unit of work | Expected | Peak | Per-instance capacity | Instances | Headroom | Scaling trigger | Source of numbers |
|---|---|---|---|---|---|---|---|---|

## Checklist

Self-assess against this list before reporting the artifact done. Report pass/fail **per item** — never a silent pass. A failed item becomes an OPEN item with an owner; it is not deleted to make the list pass.

- [ ] Availability target per capability, with RTO and RPO
- [ ] Every dependency classified hard/soft/optional
- [ ] Availability ceiling from hard dependencies computed and checked against the target
- [ ] Failure mode table covers the full standard list
- [ ] Every failure row has detection, automatic response, manual response, user-visible effect
- [ ] Degradation mode designed per dependency — not just "returns an error"
- [ ] **Every remote call has an explicit timeout**
- [ ] Retries only on idempotent operations, with backoff, jitter, cap, and a total budget
- [ ] Timeout budgets nest across every call chain
- [ ] Circuit breakers and bulkheads placed where blast radius requires
- [ ] Backpressure designed instead of unbounded buffering
- [ ] Capacity table complete, with every number labelled measured/extrapolated/assumed
- [ ] Scaling trigger and ceiling stated
- [ ] Backup, restore, failover, and reconciliation procedures defined
- [ ] Deployment, rollback, feature flags, and config-change safety stated
- [ ] Verification plan with cadence (load, chaos, failover drill, restore drill)
- [ ] Every automated response has a manual override
