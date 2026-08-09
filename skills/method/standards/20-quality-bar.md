# Standard 20 — Quality Bar (Definition of Done per artifact)

Applies to every artifact before it may be marked `Accepted`. If an item cannot be satisfied, it becomes an `OPEN` item with an owner — not a silent omission.

## Universal (all artifacts)

| # | Criterion |
|---|---|
| U1 | Header block complete: version, status, date, author, trace-id, change-type |
| U2 | Every claim is either derived from a cited input or listed as an assumption |
| U3 | No placeholder text, no `TBD` without an owner and a by-when date |
| U4 | Terminology matches the glossary; the same thing has the same name everywhere |
| U5 | Traceable up (which driver caused this) and down (which artifacts depend on it) |
| U6 | Readable by someone who joins the project tomorrow with no verbal context |
| U7 | Logged in `_logs/.design-log` |

## Per-artifact additions

| Artifact | Must additionally satisfy |
|---|---|
| Intent | scope boundary stated as both in-scope and out-of-scope; named stakeholders with their concern; constraints separated into given vs chosen |
| Drivers | every quality attribute has ≥1 scenario in `stimulus → environment → response → measure` form with a number; attributes are ranked, not all "high" |
| Impact analysis | every affected element has an impact type (add/change/remove/none-verified); "verified no impact" is stated explicitly, not implied by absence |
| ADR | ≥2 real alternatives with consequences; decision is one sentence; consequences include the negative ones |
| HLD | every element has a stated responsibility; every relationship has a direction, a protocol, and a purpose; no unlabelled arrows |
| Flow | happy path + at least one failure path; every participant exists in the HLD; timeouts/retries shown where they apply |
| LLD | responsibilities map 1:1 to interface operations; data owned vs referenced is explicit; every dependency has a stated reason |
| Interface spec | error responses defined; auth stated; idempotency stated for non-safe operations; versioning strategy stated; examples for every schema |
| Data design | one owner per data element; retention and deletion stated; PII/sensitivity classified; migration is reversible or has a stated why-not |
| Security | threats enumerated by a method (e.g. STRIDE) per trust boundary; every threat has a control or an accepted risk |
| Observability | every SLO has a measurable SLI; every failure mode in resilience design has a detecting signal |
| Resilience | every dependency has a defined failure behaviour; capacity numbers with their source; degradation modes described |
| Risk register | every risk has probability, impact, owner, mitigation, and review date |
| Review report | verdict + blocker list; every checklist item has an explicit pass/fail |
| Handoff | a new team can identify what to build first, and how to know it works |

## Self-assessment output format

```
Quality bar: 24/26
FAILED U3 — "TBD" in §Capacity with no owner  → assign or remove before Accepted
FAILED Interface — no idempotency stated on POST /x → decide and restate
```
