# Observability Design — <scope>

<!-- Header block — copy from standards/01-workflow-protocol.md, phase P8 -->

## 1. Service level objectives
| Capability | SLI (how computed) | SLO | Window | Error budget | Owner |
|---|---|---|---|---|---|

## 2. Correlation
| Item | Value |
|---|---|
| Correlation id generated at | |
| Propagated via (sync) | |
| Propagated via (async) | |
| Propagated via (batch/scheduled) | |
| Gaps | |

## 3. Log schema
| Field | Type | Always present | Notes |
|---|---|---|---|
<!-- timestamp, level, service, version, traceId, spanId, event, outcome, ... -->

**Redaction:** <PII and secret handling>

## 4. Metrics
| Metric | Type | Dimensions | Question it answers | Golden signal |
|---|---|---|---|---|

## 5. Traces
| Span | Emitted by | Attributes | Sampling |
|---|---|---|---|

## 6. Async signals
| Signal | Source | Threshold | Meaning |
|---|---|---|---|
<!-- queue depth, consumer lag, DLQ size, redelivery count, end-to-end age -->

## 7. Failure detection coverage
| Failure mode (from resilience design) | Detecting signal | Detection latency | Alert |
|---|---|---|---|

## 8. Alerts
| Alert | Condition | Symptom or cause | Severity | Owner | Runbook | Expected action |
|---|---|---|---|---|---|---|

## 9. Dashboards
| Dashboard | Audience | Question it answers | Panels |
|---|---|---|---|

## 10. Retention, cost, access
| Signal | Retention | Est. volume | Est. cost | Who can access |
|---|---|---|---|---|
