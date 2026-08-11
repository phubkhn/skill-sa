# Core SA Flow

The default flow is deliberately small:

```text
architect → decide and describe → review
              ├─ adr
              ├─ hld
              ├─ flow
              ├─ interface
              └─ data
```

`/sa:architect` is the entry point. It frames the problem, drivers, current-state impact, options, recommendation, proposed structure, cross-cutting concerns, and delivery implications in the conversation or one architecture brief.

Create a specialised artifact only when it has a consumer:

| Artifact | Create when |
|---|---|
| ADR | A consequential or contested choice must survive beyond the conversation |
| HLD | People need a shared static model of boundaries, dependencies, or deployment |
| Flow | Runtime order, failure paths, consistency, or timeouts are non-obvious |
| Interface | Another team or system needs a versioned contract |
| Data design | Ownership, retention, consistency, or migration crosses a boundary |
| Review | A design is about to guide implementation or needs independent challenge |

Do not require artifacts in sequence. Dependencies are evidence requirements, not gates: an HLD needs a decision basis, a flow needs named participants, an interface needs named consumers, and a review needs a stated scope.

## Extended concerns

Security, resilience, observability, cost, risk, and delivery are always considered proportionally in the architecture brief and review. Use the extended standards library when one of them is unusually risky, regulated, or explicitly requested; do not create six separate documents by default.

## Change handling

On a design change:

1. Update the architecture brief or explain the changed recommendation.
2. Update only the specialised artifacts affected by that change.
3. Re-run review when the change is consequential or crosses team boundaries.

Keep the architecture brief as the source of shared context and update only the specialised artifacts affected by the change.
