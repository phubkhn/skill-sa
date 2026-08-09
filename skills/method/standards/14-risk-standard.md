# Standard 14 — Risk & Trade-off Management

**Artifact:** `01-analysis/risk-register.md`
**Purpose:** make uncertainty visible and owned, instead of discovered later.

## Risk register format

| ID | Risk (condition → consequence) | Category | Probability | Impact | Exposure | Owner | Response | Mitigation / action | Trigger to escalate | Review date | Status | Trace ID |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

- **Statement form:** "*Because <fact>, <event> may occur, resulting in <consequence>.*" A risk that is not conditional is either a fact or a fear.
- **Probability / Impact:** High / Medium / Low, each with a stated meaning in this project — not universal adjectives.
- **Exposure:** P × I, used only to sort.
- **Response:** Avoid · Mitigate · Transfer · Accept. Accept requires a named human.
- **Status:** Open · Mitigating · Accepted · Closed · Realised.

## Categories

Technical · Integration · Data · Security · Performance/Capacity · Operational · Dependency/Third-party · Organisational · Schedule · Cost · Compliance · Assumption-based

## Sources of risk (sweep these when generating)

1. Every `risky` assumption from intake and every generated artifact
2. Every `Unknown (investigate)` row in impact analysis
3. Every negative consequence in an accepted ADR
4. Every residual risk in the security design
5. Every residual risk in the failure-mode table
6. Every driver whose measure is unverified
7. Every gate that was overridden
8. Every dependency owned by another team or vendor

## Trade-off log

Architecture is the sum of its trade-offs. Record them where they are not big enough for an ADR:

| ID | Trade-off | Gained | Given up | Drivers favoured | Drivers sacrificed | Revisit when |
|---|---|---|---|---|---|---|

## Rules

1. **Every risk has one named owner.** Team names are not owners.
2. **Every risk has a review date.** A register that is never reviewed is a document, not a control.
3. **Accepted risks are signed** — who accepted, when, on what basis.
4. **Realised risks are not deleted** — mark `Realised` and link the incident. This is how estimates improve.
5. **Mitigations produce work.** If a mitigation has no corresponding task or design change, it is a wish.

## Checklist

Self-assess against this list before reporting the artifact done. Report pass/fail **per item** — never a silent pass. A failed item becomes an OPEN item with an owner; it is not deleted to make the list pass.

- [ ] All nine candidate sources swept, not brainstormed
- [ ] Every risk phrased conditionally (because X, Y may occur, resulting in Z)
- [ ] Probability and impact scales defined for this project
- [ ] Duplicates merged across artifacts, sources linked
- [ ] Every risk has **one named person** as owner
- [ ] Every risk has a response (avoid/mitigate/transfer/accept)
- [ ] Every accepted risk names the accepter and the date
- [ ] Every mitigation corresponds to a real design change or work item
- [ ] Every risk has a review date
- [ ] Escalation trigger stated for High-exposure risks
- [ ] Realised risks retained and linked to their incident
- [ ] Trade-off log updated with drivers favoured and sacrificed
