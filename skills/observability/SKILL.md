---
name: observability
description: Design SLOs, SLIs, logs, metrics, traces, correlation propagation and alerting. Use when the user asks about observability, monitoring, SLOs, alerting, or how the system will be operated and diagnosed.
---

# SA — Design SLOs, signals, correlation and alerting

| | |
|---|---|
| Journey step | 11 — Observability |
| Produces | 08-crosscutting/observability-design.md |
| Inputs | 00-context/architecture-drivers.md, 04-flows/*, 05-lld/*, 08-crosscutting/resilience-design.md |
| Gate | none |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/12-observability-standard.md` |

**Method contract:** read `../method/SKILL.md` and `../method/standards/01-workflow-protocol.md` before acting. All nine execution phases (P1–P9) are defined there and are mandatory.

**Checklist:** the `## Checklist` section of `../method/standards/12-observability-standard.md` — self-assess item by item in P9.

---

Follow `../method/standards/01-workflow-protocol.md` P1–P9.

**P3:** read drivers (availability/performance numbers become SLOs), flows (instrumentation points and the observability hooks already noted), LLDs (state machines, jobs, dependencies), resilience design (failure modes needing detection).

**Method:**

1. **SLOs from drivers, not from instinct.** For each user-facing capability: SLI definition (how it is actually computed), target, measurement window, error budget, owner.
2. **Signals:** for each of logs, metrics, traces, business events — what it carries and which question it answers. Delete any signal with no question.
3. **Correlation:** where the trace id is generated, and how it propagates across *every* boundary — including message headers, batch files, and scheduled jobs. A trace that stops at the queue is incomplete; say how it continues.
4. **Instrumentation points:** per flow step and per interface operation. Golden signals (latency, traffic, errors, saturation) minimum for every user-facing path.
5. **Log schema:** fixed core fields; structured only; redaction approach for PII and secrets.
6. **Async observability:** queue depth, consumer lag, DLQ size, redelivery count, end-to-end message age.
7. **Alerts:** symptom-based and tied to SLOs; each with owner, runbook, and the action it expects. Alerts with no action get deleted at design time, not at 3am.
8. **Detection coverage:** one row per failure mode in the resilience design → the signal that reveals it. Any failure mode with no signal is a finding.
9. **Dashboards:** per audience, per question.
10. **Retention, cost and access**, including who may see production telemetry.

**P9:** report undetectable failure modes and SLOs without a computable SLI, then `Next: /sa:gen-resilience`.
