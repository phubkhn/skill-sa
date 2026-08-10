# Standard 03 — Architecture Drivers & Quality Attributes

**Artifact:** `00-context/architecture-drivers.md`
**Purpose:** convert vague quality talk into testable scenarios that actually drive structure.

## The four driver types

| Type | Definition | Example |
|---|---|---|
| Functional drivers | the small subset of functionality that shapes structure (not the whole backlog) | "must accept submissions while downstream is offline" |
| Quality attributes | measurable properties of the system | availability, latency, throughput, security, modifiability |
| Constraints | non-negotiable givens | "must run on-prem", "must reuse existing identity provider" |
| Concerns | things stakeholders worry about that aren't yet requirements | "we may need a second region later" |

Only functional requirements that **change the structure** belong here. Everything else lives in the requirements backlog.

## Quality attribute scenario format (mandatory)

Every quality attribute needs at least one scenario in this six-part form:

| Part | Meaning |
|---|---|
| **Source** | who or what generates the stimulus |
| **Stimulus** | the event arriving at the system |
| **Environment** | system state when it arrives (normal, peak, degraded, under attack) |
| **Artifact** | what part of the system is stimulated |
| **Response** | what the system must do |
| **Measure** | the number that makes it testable |

Written form:

```
QA-PERF-01 (Performance | Priority: H/H)
Source:      external client
Stimulus:    submits a request
Environment: peak load, 500 concurrent sessions
Artifact:    request-handling path
Response:    request is accepted and acknowledged
Measure:     p99 end-to-end latency < 300 ms; 0 dropped requests
Rationale:   <why this number — cite the stakeholder or regulation>
Tactics:     <architectural tactics chosen to satisfy it>
Verify by:   <load test / trace / synthetic monitor>
```

## Attributes to consider (checklist — record N/A explicitly)

Performance · Scalability · Availability · Reliability · Resilience/Recoverability · Security · Privacy · Auditability · Modifiability/Extensibility · Testability · Deployability · Operability/Observability · Portability · Interoperability · Usability · **Accessibility** · **Localisation/Internationalisation** · Compliance · Cost efficiency · Sustainability

Twenty attributes. Accessibility and localisation are separated from Usability deliberately: both are frequently legal obligations rather than preferences, and both shape structure (content model, text externalisation, locale-aware storage and formatting) in ways a general usability goal does not.

**Sustainability** is in the sweep because it is increasingly reported on, not because it always applies. If it does not, mark it `N/A — <reason>` like any other attribute. If it does, express it as a measure — energy or carbon per unit of work, or utilisation floor — not as an intention.

## Prioritisation

Rank each attribute on two axes and record both:

- **Business importance:** H / M / L
- **Architectural difficulty:** H / M / L

Design effort goes to **H/H first**. If more than ~5 attributes are H/H, the prioritisation is wrong — push back before designing.

## Rules

1. **No number, no driver.** "Highly available" is not a driver; "99.9% monthly, ≤ 15 min RTO" is.
2. **Every number has a rationale and a source.** Invented SLOs create invented architecture.
3. **Attributes conflict.** Record the conflicts explicitly (e.g. consistency vs availability, security vs usability) — they become ADRs.
4. **Every driver is traceable** to a stakeholder concern or a constraint from intake.
5. **Drivers are reviewed at every change.** A change that alters no driver rarely justifies structural change.
6. **End-to-end measures are allocated, not just stated.** A driver expressed end-to-end (latency, availability) must be split into a per-hop budget in the HLD relationship catalogue (Standard 06 rule 8). An unallocated end-to-end number cannot be designed against and cannot be tested per component — it only fails at the very end, when it is most expensive.

## Output tables

**Driver summary**

| ID | Attribute | Scenario (short) | Measure | Bus. importance | Arch. difficulty | Trace ID |
|---|---|---|---|---|---|---|

**Conflict log**

| Conflict | Attributes | Resolution | ADR |
|---|---|---|---|

## Checklist

Self-assess against this list before reporting the artifact done. Report pass/fail **per item** — never a silent pass. A failed item becomes an OPEN item with an owner; it is not deleted to make the list pass.

- [ ] Every quality attribute in the sweep table is either in play or marked N/A with a reason
- [ ] Every in-play attribute has ≥1 six-part scenario
- [ ] Every scenario has a **number** in its Measure
- [ ] Every number has a rationale and a named source
- [ ] Every driver traces to a stakeholder concern or a constraint
- [ ] Attributes ranked on business importance × architectural difficulty
- [ ] ≤5 attributes in the H/H quadrant (or the overload was raised with the user)
- [ ] Structure-shaping functionality separated from the general backlog
- [ ] Conflicts between attributes listed, each with a resolution or an ADR
- [ ] Unknown measures listed with owner and date; those on **H/H attributes** flagged as G1 blockers, the rest as open items
- [ ] Verification method stated per scenario (Standard 24)
- [ ] Every end-to-end measure allocated to a per-hop budget, or flagged for the HLD to allocate
- [ ] No attribute described only with adjectives
