# Standard 24 — Verification & Fitness Functions

**Artifact:** the Verification section of `10-handoff/dev-handoff-<date>.md`, plus the `Compliance / verification` section of every ADR
**Purpose:** a driver that cannot be proven met is a wish, and a decision with no compliance mechanism decays the week after it is made.

This standard defines *how* architecture gets verified. What is verified comes from Standard 03 (drivers) and Standard 05 (ADR compliance).

## Two things are verified

| What | Against | Mechanism |
|---|---|---|
| **Drivers** — does the built system meet the measured scenarios? | `architecture-drivers.md` | test type + tool + threshold, run at a stated point |
| **Decisions** — does the built system still obey the ADRs? | `02-decisions/*` | fitness function, ideally automated in CI |

Functional correctness is the team's business. This standard covers only the architectural properties.

## Verification plan table

One row per driver. Lives in the handoff.

| Driver | What proves it | Test type | Tool | Threshold | Environment | When it runs | Owner |
|---|---|---|---|---|---|---|---|
| QA-PERF-01 | p99 latency under 500 rps | load test | <tool> | p99 < 300 ms | prod-like | pre-release + nightly | |
| QA-AVAIL-01 | recovery after primary loss | failover drill | manual runbook | RTO ≤ 15 min | staging | quarterly | |

## Test types at the architecture level

| Type | Proves | Notes |
|---|---|---|
| Contract test | provider and consumer still agree | run in both pipelines; a contract test only in the provider's pipeline proves nothing |
| Load / stress test | performance and capacity scenarios | must run against production-like topology, not a single instance |
| Soak test | resource leaks, unbounded growth | the only way to catch slow saturation |
| Chaos experiment | designed degradation actually happens | start with the dependency the design says is soft |
| Failover / restore drill | RTO and RPO | a restore procedure never executed is a document, not a capability |
| Security test | threat controls | authz matrix, input validation at boundaries, secret exposure |
| Observability test | the failure is detectable | inject the failure, assert the alert fires |
| Migration rehearsal | the migration plan works | full dress rehearsal on a production-sized copy before cutover |

## Fitness functions

A fitness function is an automated, repeatable check that an architectural property still holds. Each ADR's `Compliance / verification` section names one.

| Property | Example fitness function |
|---|---|
| Dependency direction | build fails if module A imports module B |
| No shared database | schema access audit; build fails on a second writer |
| Async integration where the ADR says async | lint the contract set for a sync call on that path |
| Public contract compatibility | spec diff against the last release; MAJOR change fails without a migration plan |
| Latency budget per hop | assertion in the load test, not just an end-to-end assertion |
| No secrets in artifacts | repository scan in CI |
| Every service emits the core log schema | log schema validation in the pipeline |

**A fitness function that has never failed has never been tested.** Introduce each one with a deliberate violation to confirm it fires.

## Rules

1. **Every driver has exactly one row in the verification plan.** A driver with no row is not verifiable and should not have passed the drivers checklist.
2. **Threshold, not direction.** "Latency should improve" is not a threshold; "p99 < 300 ms at 500 rps" is.
3. **Name the environment.** A performance result from a non-production-like environment proves nothing about production.
4. **State when it runs.** Once, pre-release, nightly, quarterly — a test with no cadence runs once and then never again.
5. **Every ADR has a compliance mechanism**, and it is automated wherever the property is mechanically checkable. "Review will catch it" is the weakest possible answer and must be justified.
6. **Verification is designed at handoff, not discovered at the end.** If a driver cannot be verified with the tools the team has, that is a finding now, not a surprise later.
7. **A failed fitness function blocks the merge**, or it is decoration. State the enforcement level: blocking, warning, or reporting.
8. **Drills have owners and dates.** Restore and failover drills that are "planned" are not verification.

## Checklist

Self-assess against this list before reporting the artifact done. Report pass/fail **per item** — never a silent pass. A failed item becomes an OPEN item with an owner; it is not deleted to make the list pass.

- [ ] Every driver has a verification row with test type, tool, threshold, environment, cadence, owner
- [ ] Every threshold is a number, not a direction
- [ ] Contract tests run in both provider and consumer pipelines
- [ ] Load tests specified against a production-like topology
- [ ] Every failure mode marked "detectable" has an observability test that proves it
- [ ] Restore and failover drills scheduled with a named owner
- [ ] Migration rehearsal planned where a migration exists
- [ ] Every ADR has a compliance mechanism named
- [ ] Mechanically checkable properties have an automated fitness function
- [ ] Each fitness function states its enforcement level (blocking / warning / reporting)
- [ ] Each fitness function has been proven to fire on a deliberate violation
- [ ] Drivers that cannot be verified with available tooling are raised as findings
