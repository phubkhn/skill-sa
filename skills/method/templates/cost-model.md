# Cost Model — <scope>

<!-- Header block — copy from standards/01-workflow-protocol.md, phase P8 -->

**Currency:** <CUR>  ·  **Time base:** monthly unless stated  ·  **Basis:** capacity table in `08-crosscutting/resilience-design.md` v<N>

<!-- No capacity table means no cost model. Say so rather than pricing a guess. -->

## 1. Cost drivers

The handful of variables that actually move the number. Everything else is noise.

| Driver | Current value | Source | Sensitivity (what a 2× change does) |
|---|---|---|---|
| | | | |

## 2. Build cost (one-off)

| Item | Basis | Amount | Confidence |
|---|---|---|---|
| Engineering effort | <person-weeks × rate> | | estimated |
| One-off licences | | | quoted |
| Migration & dual-run | | | |
| Initial data transfer | | | |
| **Total** | | | |

## 3. Run cost (recurring)

| Component group | Resource | Unit | Qty (expected) | Qty (peak) | Unit cost | Monthly (expected) | Monthly (peak) | Source |
|---|---|---|---|---|---|---|---|---|
| | compute | | | | | | | |
| | storage | | | | | | | |
| | egress | | | | | | | |
| | inter-zone traffic | | | | | | | |
| | telemetry ingestion | | | | | | | |
| | backup storage | | | | | | | |
| | non-production envs | | | | | | | |
| | licences | | | | | | | |
| | operating headcount | | | | | | | |
| **Total** | | | | | | | | |

<!-- Egress, inter-zone traffic, telemetry and non-production are where cost models are wrong. -->

## 4. Projection

| Horizon | Volume basis | Monthly run cost | Cumulative |
|---|---|---|---|
| Today | | | |
| 12 months | data design growth rate | | |
| 36 months | data design growth rate | | |

## 5. Unit economics

| Unit | Definition | Cost per unit (expected) | Cost per unit (at 36m volume) |
|---|---|---|---|
| | | | |

## 6. Cost of the quality targets

The table stakeholders actually act on: what each target costs, and what buying a lower one saves.

| Driver | Current target | Attributable monthly cost | One notch lower | Saving | What is lost |
|---|---|---|---|---|---|
| Availability | | | | | |
| Retention | | | | | |
| Latency | | | | | |

## 7. Option comparison

<!-- One row per option in 01-analysis/solution-options.md, including "do nothing". -->

| Option | Build | Run (36m) | Total | Note |
|---|---|---|---|---|
| | | | | |

## 8. Optimisation levers

| Lever | Saving | Quality cost | When it can be pulled | Reversible |
|---|---|---|---|---|
| | | | | |

## 9. Assumptions & confidence

| # | Assumption | Label | Source / formula | Risk if wrong |
|---|---|---|---|---|
| | | measured \| quoted \| estimated | | |

## 10. Cost controls

| Item | Value |
|---|---|
| Budget owner (named person) | |
| Monthly budget | |
| Alert thresholds | |
| Allocation tagging scheme | |
| Review cadence | |
