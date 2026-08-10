# Design Review — express-lane — 2026-03-14

| Field | Value |
|---|---|
| Reviewer | M. Haddad |
| Profile | standard |
| Scope reviewed | all artifacts under `docs/architecture` as of commit `a3f19c2` |
| Artifacts + versions | intent v2, drivers v2, impact v1, ADR-0001/0002/0003, container-orders v2, flow client-submit-express-order v1, LLD order-intake v1.1, interfaces v1.0.0, data-design v1, security v1, resilience v1, observability v1, risk v2 |
| Verdict | **READY WITH CONDITIONS** |

## Verdict

READY WITH CONDITIONS — no Blockers, 3 Majors.

| # | Condition | Owner | By |
|---|---|---|---|
| 1 | Resolve the `reporting-warehouse` unknown (F-001) — it is the only unassessed blast-radius element | Data team lead | 2026-03-21 |
| 2 | Write the client migration plan for the two breaking consumers (F-003) | A. Mensah | 2026-03-21 |
| 3 | State the DLQ drain procedure and its owner in the runbook (F-004) | P. Lindqvist | 2026-03-28 |

## Findings

| ID | Severity | Dimension | Finding | Evidence | Standard/Driver violated | Recommendation | Owner |
|---|---|---|---|---|---|---|---|
| F-001 | Major | 3 Consistency | `reporting-warehouse` remains `Unknown (investigate)`; the blast-radius walk is therefore incomplete and one consumer's exposure is unassessed | `01-analysis/impact-analysis.md:34` | Standard 04 rule 3 | contact the Data team; convert to `Change`, `None (verified)` or a named risk | Data team lead |
| F-002 | Minor | 6 Data integrity | Two components write `orders-db`. The column sets are disjoint and documented, but "one writer per store" is stated as absolute in Standard 10 rule 2 | `03-hld/container-orders-catalogue.md:41`, `05-lld/order-intake.yaml:62` | Standard 10 rule 2 | acceptable as designed, but record it in the trade-off log so the exception is deliberate rather than inherited | J. Okafor |
| F-003 | Major | 5 Contract soundness | Two consumers take a breaking change (`201` → `202`); Standard 09 rule 3 requires a migration plan per consumer before the MAJOR change is written, and none exists | `01-analysis/impact-analysis.md:47`, `06-interfaces/order-intake-api.yaml:1` | Standard 09 rule 3 | write the per-consumer migration plan, including the release-coordination sequence | A. Mensah |
| F-004 | Major | 10 Operability | The DLQ is designed and alerted on, but no drain procedure exists. The first poison message will be handled by improvisation at 3am | `08-crosscutting/observability-design.md:71` | Standard 16 rule 7 | write runbook RB-014 and name its owner before handoff | P. Lindqvist |
| F-005 | Minor | 9 Observability | The end-to-end message age signal is defined but has no alert threshold | `08-crosscutting/observability-design.md:48` | Standard 12 rule 7 | set a threshold or delete the signal | P. Lindqvist |
| O-001 | Observation | 11 Simplicity | The outbox adds a moving part. It is justified by RPO 0 and the analysis is sound; noted only because a future reader will ask why a direct publish was not used | `05-lld/order-intake.yaml:52` | — | consider a sentence in ADR-0001 | — |

## Driver coverage

| Driver | Satisfied? | Mechanism in the design | Evidence | Confidence |
|---|---|---|---|---|
| QA-PERF-01 (p99 < 800 ms) | Yes | acknowledgement bounded by a 120 ms local write plus an 80 ms publish; budget allocated per hop with deliberate headroom | `03-hld/container-orders-catalogue.md:48` | High — spike measured p99 ≈ 90 ms |
| QA-AVAIL-01 (accept while fulfilment down) | Yes | durable topic buffers; intake has no synchronous dependency on fulfilment | `04-flows/client-submit-express-order.puml:78` | High |
| QA-AVAIL-01 (RPO 0) | Yes | order and outbox row written in one transaction before acknowledgement | `05-lld/order-intake.yaml:52` | High |
| QA-DATA-01 (dedup) | Yes | unique index on `idempotency_key`; the database arbitrates the race, not application logic | `05-lld/order-intake.yaml:97` | High |
| Observability | Partial | lag, DLQ and message-age signals defined; one lacks a threshold (F-005) | `08-crosscutting/observability-design.md:48` | Medium |

## Consistency matrix results

| # | Check | Result | Detail |
|---|---|---|---|
| 1 | Every HLD element has an LLD where required | PASS | `recon-batch` and `fulfilment-service` out of scope, stated |
| 2 | Every LLD responsibility has an interface operation | PASS | R1–R4 all mapped |
| 3 | Every interface operation maps to a responsibility | PASS | |
| 4 | Flow participants exist in HLD with identical names | PASS | 5/5 match |
| 5 | Every event published has ≥1 declared consumer | PASS | `order.accepted` → `fulfilment-service` |
| 6 | Every event consumed is published somewhere | PASS | |
| 7 | Every entity has exactly one owner | PASS with note | see F-002 |
| 8 | Field names consistent across specs | PASS | |
| 9 | No container-level cycles | PASS | |
| 10 | Every ADR referenced is Accepted | PASS | 0001, 0002, 0003 all Accepted |
| 11 | Every driver appears in ≥1 artifact | PASS | |
| 12 | Every High risk has a mitigation or acceptance | PASS | R1–R3 all owned |
| 13 | Every artifact carries a trace-id | PASS | all 13 |
| 14 | No artifact stale against its upstream | PASS | |
| 15 | No seed contradicts its authority | PASS | LLD v1.1 reconciled with data-design v1 on 2026-03-12 |
| 16 | Every container appears on exactly one node group | N/A | no deployment view required at `standard` profile |
| 17 | Per-hop latency budgets sum within the driver target | PASS | 120 + 80 + 600 headroom = 800 ms |
| 18 | Every element has an interface spec path or a written `N/A` | PASS | 3 specs, 3 justified `N/A` |
| 19 | Every driver has a verification row with a numeric threshold | FAIL | observability driver has no threshold — F-005 |

## What is good

The ADR is the strongest artifact here. Option B is a real option, argued at its best, and rejected for a reason that survives scrutiny — it fails QA-AVAIL-01 structurally, not for want of effort. Reviewers see straw men constantly; this is not one.

The flow's failure paths do the work the diagram exists for. The distinction between "publish fails before commit" and "publish fails after commit" is exactly the case that produces lost orders in systems that have not thought about it, and it is drawn explicitly.

The out-of-scope list is specific enough to be enforceable, including the reason `partner-gateway` was excluded.

## Not required at this profile

`solution-options.md` and `cost-model.md` — conditional at `standard` profile and not triggered. Deployment view not required at this profile. Their absence is not a gap.

## Not reviewed

Fulfilment-service internals; the existing pricing and inventory path; the security posture of the OIDC provider itself; anything under `partner-gateway`.
