# Standard 15 — Design Review

**Artifact:** `09-review/design-review-<YYYY-MM-DD>.md`
**Purpose:** an evidence-based judgement on whether the design is fit to build.

## Review is not a discussion

The reviewer evaluates artifacts against standards and drivers, produces findings with severity, and issues a verdict. Opinions without a standard or driver reference are recorded as `Observation`, not `Finding`.

## Review dimensions

| # | Dimension | Asks |
|---|---|---|
| 1 | Completeness | does every required artifact exist at the required quality bar? |
| 2 | Driver satisfaction | can each prioritised quality scenario be met by this design? show the mechanism |
| 3 | Internal consistency | do the artifacts agree with each other? |
| 4 | Decision integrity | is every significant structural choice backed by an ADR, and does the design match it? |
| 5 | Contract soundness | are interfaces complete, versioned, error-defined, consumer-validated? |
| 6 | Data integrity | single ownership, retention, migration reversibility |
| 7 | Security posture | threats covered per boundary; no orphan threats |
| 8 | Resilience | every dependency has failure behaviour; degradation designed |
| 9 | Observability | every failure mode detectable; SLOs measurable |
| 10 | Operability | deployable, rollback-able, runbook-able |
| 11 | Simplicity | is anything here not justified by a driver? |
| 12 | Traceability | every element traces up to a driver and down to work |
| 13 | Buildability | can a team start from this without further architecture decisions? |

## Consistency matrix (mechanical checks)

| Check | Fail |
|---|---|
| Every HLD element has an LLD (where required) | missing LLD |
| Every LLD responsibility has an interface operation | orphan responsibility |
| Every interface operation maps to a responsibility | unowned operation |
| Every flow participant exists in HLD with the same name | name drift |
| Every event published has ≥1 declared consumer, or a stated reason | orphan event |
| Every event consumed is published by some component | phantom event |
| Every entity has exactly one owner | shared ownership |
| Field names consistent across all specs | vocabulary drift |
| No cyclic dependencies at container level | cycle |
| Every ADR referenced by the design is `Accepted` | design on a `Proposed` ADR |
| Every driver appears in ≥1 artifact | unaddressed driver |
| Every High risk has a mitigation or signed acceptance | unmanaged risk |

## Finding severity

| Severity | Meaning | Effect on verdict |
|---|---|---|
| **Blocker** | design cannot be built safely / a driver cannot be met | verdict = NOT READY |
| **Major** | will cause rework or an incident; must be fixed before the affected work starts | verdict = READY WITH CONDITIONS |
| **Minor** | should be fixed; does not block | none |
| **Observation** | opinion or future consideration | none |

## Report structure

```markdown
# Design Review — <scope> — <date>
| Reviewer | Scope reviewed | Artifacts + versions | Verdict |

## Verdict
READY | READY WITH CONDITIONS | NOT READY
Conditions: <numbered, each with owner and by-when>

## Findings
| ID | Severity | Dimension | Finding | Evidence (file:line) | Standard/Driver violated | Recommendation | Owner |

## Driver coverage
| Driver | Satisfied? | Mechanism in the design | Evidence | Confidence |

## Consistency matrix results
| Check | Result | Detail |

## What is good
<explicitly — reviewers who only find faults are ignored>

## Not reviewed
<scope limits — what this review does not cover>
```

## Rules

1. **Every finding cites evidence** — file and location. No unfalsifiable findings.
2. **Every finding cites the standard or driver it violates.** Otherwise it is an Observation.
3. **The reviewer does not edit the design.** Findings go back to the author.
4. **Verdict is mechanical**, derived from severity counts — not from mood.
5. **State what was not reviewed.** An unstated scope limit reads as approval.

## Checklist

Self-assess against this list before reporting the artifact done. Report pass/fail **per item** — never a silent pass. A failed item becomes an OPEN item with an owner; it is not deleted to make the list pass.

- [ ] Artifact inventory complete with versions and statuses
- [ ] Quality bar evaluated per artifact, item by item
- [ ] All 12 consistency-matrix checks run and reported
- [ ] Driver coverage table names the **mechanism** for each satisfied driver
- [ ] All 13 review dimensions covered
- [ ] Every finding cites evidence (`path:line`)
- [ ] Every finding cites the standard or driver violated
- [ ] Items without evidence recorded as Observations, not Findings
- [ ] Severity assigned per finding
- [ ] Verdict computed mechanically from severity counts
- [ ] Conditions listed with owner and by-when (for READY WITH CONDITIONS)
- [ ] "What is good" section non-empty
- [ ] "Not reviewed" scope limits stated
- [ ] No design artifact was modified by this review
