---
name: resilience
description: Design failure behaviour, degradation modes, timeouts, retries, capacity and recovery. Use when the user asks about resilience, high availability, failure handling, capacity planning, or disaster recovery.
---

# SA — Design failure behaviour, capacity and operability

| | |
|---|---|
| Journey step | 12 — Resilience |
| Produces | 08-crosscutting/resilience-design.md |
| Inputs | 00-context/architecture-drivers.md, 03-hld/*, 04-flows/*, 05-lld/* |
| Gate | none |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/13-resilience-standard.md` |

**Method contract:** read `../method/SKILL.md` and `../method/standards/01-workflow-protocol.md` before acting. All nine execution phases (P1–P9) are defined there and are mandatory.

**Checklist:** the `## Checklist` section of `../method/standards/13-resilience-standard.md` — self-assess item by item in P9.

---

Follow `../method/standards/01-workflow-protocol.md` P1–P9.

**P3:** read drivers (availability, RTO/RPO, load numbers), HLD relationship catalogue (the `failure behaviour` column), flows (timeouts and retries already declared), LLDs (dependencies and failure modes).

**Method:**

1. **Availability targets** per capability, with the measurement definition, RTO and RPO.
2. **Dependency map:** every dependency classified hard / soft / optional. A "hard" dependency caps your availability at its own — state the resulting ceiling and check it against the driver. If the arithmetic fails the target, that is a finding, not a footnote.
3. **Failure mode analysis:** one row per credible failure, covering the full list in Standard 13 (dependency down, dependency slow, store failover, broker down, consumer lag, poison message, duplicate delivery, clock skew, bad deploy, config error, resource exhaustion, zone/region loss). Each row: trigger, blast radius, detection, automatic response, manual response, user-visible effect, residual risk.
4. **Degradation modes:** what the system still does when each dependency is down. "Returns an error" is a failure, not a design — decide whether to queue, cache, default, or shed.
5. **Tactics:** timeouts (every remote call, no exceptions), retries with backoff and jitter and a cap (idempotent operations only), circuit breakers, bulkheads, rate limiting, backpressure over unbounded buffering, idempotency, dead-lettering. Verify **timeout budgets nest** across every call chain in the flows.
6. **Capacity table:** expected/peak load, per-instance capacity, instance count, headroom, scaling trigger and ceiling, with the source of each number labelled measured / extrapolated / assumed.
7. **Recovery:** backup and restore, failover procedure, post-split-brain reconciliation, replay procedures.
8. **Operability:** deployment strategy, rollback, feature flags, safe config change, runbooks required.
9. **Verification:** load test, chaos experiment, failover drill, restore drill — with cadence.

**P9:** report dependencies whose availability ceiling breaches the target, calls with no timeout, and assumed capacity numbers, then `Next: /sa:gen-risk-register`.
