# Proportional Delivery

Tailor by outcome, not by a mandatory project profile.

| Situation | Default mode | Typical result |
|---|---|---|
| Explore an idea or diagnose a design concern | `quick` | conversation answer |
| Align one team on a meaningful change | `brief` | one architecture brief |
| Preserve a decision or cross-team boundary | `artifact` | brief plus only the needed ADR, view, flow, contract, or data design |
| Prepare a consequential design for implementation | `artifact` + review | focused artifact set and review report |

## Promotion triggers

Promote a concern into a specialised artifact when any of these applies:

- the decision is costly to reverse, contested, or surprising → ADR
- boundaries or deployment cannot be understood reliably from prose → HLD
- runtime failure or consistency behaviour is non-obvious → flow
- another team or external consumer depends on a contract → interface
- ownership, retention, or migration crosses a component boundary → data design
- the design guides implementation across teams or carries material risk → review

Everything else stays in the architecture brief.

`sa-config.yaml` may set a preferred mode, but it never blocks a skill from running.
