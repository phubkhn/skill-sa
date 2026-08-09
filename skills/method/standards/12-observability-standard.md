# Standard 12 — Observability Design

**Artifact:** `08-crosscutting/observability-design.md`
**Purpose:** a system you cannot see is a system you cannot operate. Design the signals with the architecture.

## Required content

| Section | Content |
|---|---|
| Service level objectives | per user-facing capability: SLI definition, SLO target, measurement window, error budget |
| Signals | logs, metrics, traces, events — what each carries and why |
| Correlation | the trace/correlation id, where it is generated, and how it propagates across every boundary including async |
| Instrumentation points | per flow step and per interface operation |
| Dashboards | who looks at what, to answer which question |
| Alerts | symptom-based, tied to SLOs, with an owner and a runbook link |
| Failure detection | one row per failure mode from the resilience design → the signal that reveals it |
| Retention & cost | how long each signal is kept, and the volume/cost implication |
| Access | who can see production telemetry; PII handling in logs |

## SLI/SLO table

| Capability | SLI (how measured) | SLO | Window | Error budget | Owner |
|---|---|---|---|---|---|

## Signal design rules

1. **Instrument for questions, not for coverage.** Each signal exists to answer a stated operational question.
2. **The four golden signals** — latency, traffic, errors, saturation — for every user-facing path, minimum.
3. **Structured logs only.** Key–value/JSON with a fixed core schema: timestamp, level, service, version, traceId, spanId, event, outcome.
4. **Correlation id propagates everywhere**, including message headers, batch files, and scheduled jobs. A trace that stops at the queue is not a trace.
5. **No PII or secrets in logs.** State the redaction approach.
6. **Alert on symptoms, diagnose with causes.** Cause-based alerts page people for things users never noticed.
7. **Every alert has a runbook** and a named owner, or it gets deleted.
8. **Business-level signals matter** — a technically healthy system doing zero work is an outage.
9. **Observability of async is explicit:** queue depth, consumer lag, DLQ size, redelivery counts, end-to-end age.

## Coverage checklist

- [ ] Every interface operation has latency + error-rate metrics
- [ ] Every dependency call has success/failure/timeout metrics and a circuit state where applicable
- [ ] Every state machine transition is observable
- [ ] Every background job reports start, end, duration, outcome, and records processed
- [ ] Every failure mode in `resilience-design.md` has a detecting signal
- [ ] Deployment/version is a dimension on key metrics
- [ ] Health/readiness semantics defined and distinguished

## Checklist

Self-assess against this list before reporting the artifact done. Report pass/fail **per item** — never a silent pass. A failed item becomes an OPEN item with an owner; it is not deleted to make the list pass.

- [ ] Every user-facing capability has an SLI that is actually computable
- [ ] Every SLO has a target, window, error budget, and owner
- [ ] SLOs derive from drivers, not from instinct
- [ ] Correlation id generation point defined
- [ ] Correlation propagates across sync, async, batch, and scheduled boundaries
- [ ] Golden signals (latency, traffic, errors, saturation) covered for every user-facing path
- [ ] Structured logging with a fixed core schema
- [ ] PII and secret redaction approach stated
- [ ] Async signals covered: queue depth, consumer lag, DLQ size, redelivery, message age
- [ ] Every state machine transition observable
- [ ] Every background job reports start, end, duration, outcome, volume
- [ ] Every failure mode in the resilience design has a detecting signal
- [ ] Every alert is symptom-based, owned, and has a runbook and an expected action
- [ ] Deployment/version is a dimension on key metrics
- [ ] Health vs readiness semantics distinguished
- [ ] Retention, volume, cost, and access stated per signal
- [ ] No signal exists without a question it answers
