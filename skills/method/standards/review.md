# Architecture Review

A review judges the design against its own goals and explicit quality rules. It does not require a fixed document set and does not edit the design.

## Review dimensions

1. Problem and scope clarity
2. Driver satisfaction and measurable mechanisms
3. Consistency across decisions, structure, flows, contracts, and data
4. Security and privacy
5. Resilience and failure behaviour
6. Observability and operability
7. Simplicity and justified complexity
8. Cost direction and proportionality
9. Deployment and migration feasibility
10. Buildability and unresolved decisions

## Findings

Every finding includes severity, evidence, violated driver/decision/contract/rule, impact, recommendation, and owner when known. Without evidence or an explicit rule, record an Observation.

| Severity | Meaning | Verdict effect |
|---|---|---|
| Blocker | Unsafe or impossible to build; a critical driver cannot be met | NOT READY |
| Major | Likely incident or material rework | READY WITH CONDITIONS |
| Minor | Valuable correction that does not block | none |
| Observation | Advice or future consideration | none |

Any Blocker means `NOT READY`. Otherwise any Major means `READY WITH CONDITIONS`. Otherwise the verdict is `READY`.

## Checklist

- [ ] Scope and artifacts reviewed are stated
- [ ] Important drivers map to concrete mechanisms
- [ ] Cross-artifact consistency was checked
- [ ] All ten dimensions were considered proportionally
- [ ] Every finding has evidence and a rule or driver
- [ ] Verdict follows severity mechanically
- [ ] Conditions have an owner and next action
- [ ] Strengths and unreviewed areas are stated
- [ ] No design artifact was edited
