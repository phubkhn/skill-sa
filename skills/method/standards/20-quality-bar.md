# Standard 20 — Quality Bar (Definition of Done per artifact)

Applies to every artifact before it may be marked `Accepted`. If an item cannot be satisfied, it becomes an `OPEN` item with an owner — not a silent omission.

## Two lists, one of them authoritative

There are two places that describe when an artifact is done, and it matters which one wins:

| | Where | Status |
|---|---|---|
| **Universal items U1–U9** | this file, below | **authoritative** — they apply to every artifact and appear nowhere else |
| **Per-artifact items** | the `## Checklist` at the end of each step standard | **authoritative** — the full, detailed list the producing skill self-assesses against |
| Per-artifact summary | the table further down this file | **not authoritative** — a reviewer's quick reference, deliberately shorter |

The summary table exists so `sa:review` can sweep many artifacts without opening every standard. It is a condensation, not a second standard. **Where the summary and a standard's checklist disagree, the checklist wins**, and the disagreement is a defect in this file to be fixed rather than a judgement call.

Do not add a new requirement here. Add it to the owning standard's checklist, then summarise it here if it is worth a reviewer's attention.

## Universal (all artifacts)

| # | Criterion |
|---|---|
| U1 | Header complete: version, status, date, author, trace-id, change-type, ref. **Any of the four equivalent header formats** in Standard 01 satisfies this — markdown table, PlantUML comment, OpenAPI/AsyncAPI `x-` fields, or LLD YAML top-level keys. ADRs are exempt from `Version` (Standard 19). |
| U2 | Every claim is either derived from a cited input or listed as an assumption |
| U3 | No placeholder text, no `TBD` without an owner and a by-when date |
| U4 | Terminology matches the glossary; the same thing has the same name everywhere |
| U5 | Traceable up (which driver caused this) and down (which artifacts depend on it) |
| U6 | Readable by someone who joins the project tomorrow with no verbal context |
| U7 | Logged in `_logs/.design-log` |
| U8 | Every claim about the *existing* system carries a source — `path:line`, a named document, or a named person and date |
| U9 | Prose in the configured `language`; all identifiers and enum values in English kebab-case |

## Per-artifact summary (reviewer's quick reference — not authoritative)

The owning standard's `## Checklist` is the real list. These are the items a reviewer should notice first.

| Artifact | Must additionally satisfy | Full checklist |
|---|---|---|
| Intent | scope boundary stated as both in-scope and out-of-scope; named stakeholders with their concern; constraints separated into given vs chosen | std 02 |
| Drivers | every quality attribute has ≥1 scenario in `stimulus → environment → response → measure` form with a number; attributes are ranked, not all "high" | std 03 |
| Impact analysis | every affected element has an impact type (add/change/remove/none-verified); "verified no impact" is stated explicitly, not implied by absence | std 04 |
| Solution options | ≥2 shapes described identically, each costed; recommendation names the deciding axis | std 25 |
| ADR | ≥2 real alternatives with consequences; decision is one sentence; consequences include the negative ones | std 05 |
| HLD | every element has a stated responsibility; every relationship has a direction, a protocol, and a purpose; no unlabelled arrows | std 06 |
| Deployment view | every container placed on exactly one node group; failure domain per node; encryption and latency budget per network path | std 22 |
| Flow | happy path + at least one failure path; every participant exists in the HLD; timeouts/retries shown where they apply | std 07 |
| LLD | responsibilities map 1:1 to interface operations; data owned vs referenced is explicit; every dependency has a stated reason | std 08 |
| Interface spec | error responses defined; auth stated; idempotency stated for non-safe operations; versioning strategy stated; examples for every schema | std 09 |
| Data design | one owner per data element; retention and deletion stated; PII/sensitivity classified; migration is reversible or has a stated why-not | std 10 |
| Security | threats enumerated by a method (e.g. STRIDE) per trust boundary; every threat has a control or an accepted risk | std 11 |
| Resilience | every dependency has a defined failure behaviour; capacity numbers with their source; degradation modes described | std 13 |
| Observability | every SLO has a measurable SLI; every failure mode in resilience design has a detecting signal | std 12 |
| Cost model | build and run separated; run given at expected and peak; every figure labelled measured/quoted/estimated | std 23 |
| Risk register | every risk has probability, impact, owner, mitigation, and review date | std 14 |
| Review report | verdict + blocker list; every checklist item has an explicit pass/fail | std 15 |
| Handoff | a new team can identify what to build first, and how to know it works; every driver has a verification row with a numeric threshold | std 16, 24 |
| Principles | each principle has a rationale and a stated implication; no principle nobody could disagree with | std 02 |

Rows are in journey order, so a reviewer sweeping the tree reads them in the order the artifacts were produced.

## Self-assessment output format

Score is `passed / (9 universal + n items in the owning standard's checklist)`. The denominator comes from that checklist, not from the summary row above.

```
Quality bar: 26/28  (9 universal + 19 from standard 09's checklist)
FAILED U3 — "TBD" in §Rate limits with no owner            → assign an owner or remove before Accepted
FAILED std-09 — no idempotency stated on POST /orders      → decide the mechanism and restate
```

Never report a score without having evaluated every item, and never adjust the denominator to make the ratio look better.
