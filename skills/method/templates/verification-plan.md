# Verification Plan — <scope>

<!-- Forms the Verification section of 10-handoff/dev-handoff-<date>.md. Standard 24. -->

## 1. Driver verification

One row per driver. A driver with no row is not verifiable and should not have passed the drivers checklist.

| Driver | What proves it | Test type | Tool | Threshold (a number) | Environment | When it runs | Owner |
|---|---|---|---|---|---|---|---|
| QA-PERF-01 | p99 latency at target load | load test | | p99 < <n> ms at <n> rps | prod-like | pre-release + nightly | |
| QA-AVAIL-01 | recovery after primary loss | failover drill | | RTO ≤ <n> min | staging | quarterly | |

<!-- "Should improve" is not a threshold. Name the environment: a result from a
     non-production-like environment proves nothing about production. -->

## 2. Fitness functions

One per ADR whose property is mechanically checkable.

| ADR | Property held | Fitness function | Where it runs | Enforcement | Proven to fire? |
|---|---|---|---|---|---|
| ADR-0001 | | | CI | blocking \| warning \| reporting | yes/no + date |

<!-- A fitness function that has never failed has never been tested.
     Introduce each with a deliberate violation. -->

## 3. Contract tests

| Contract | Provider | Consumers | Runs in provider pipeline | Runs in consumer pipeline |
|---|---|---|---|---|
| | | | | |

<!-- A contract test only in the provider's pipeline proves nothing. -->

## 4. Drills

| Drill | Scope | Cadence | Owner | Last run | Next run |
|---|---|---|---|---|---|
| Restore from backup | | | | | |
| Failover | | | | | |
| Migration rehearsal | | once, pre-cutover | | | |

## 5. Observability verification

| Failure mode | Detecting signal | How the detection is tested | Owner |
|---|---|---|---|
| | | inject and assert the alert fires | |

## 6. Gaps

Drivers that cannot be verified with the tooling the team has. Each is a finding now, not a surprise later.

| Driver | Why it cannot be verified | What would be needed | Owner |
|---|---|---|---|
| | | | |
