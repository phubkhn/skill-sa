# Standard 21 — Tailoring

A seventeen-step journey applied to a two-week change is not rigour, it is theatre — and it is the reason method sets get abandoned. This standard says how much of the journey a given piece of work actually needs.

The profile is set once per initiative in `sa-config.yaml`:

```yaml
profile: light | standard | full
```

Every skill reads it in P2 and states it in the Change Summary.

## Choosing the profile

Answer these; the highest matching row wins.

| If any of these is true | Profile |
|---|---|
| New system, platform replacement, new business capability, or > 3 teams involved | `full` |
| New or changed **public contract**, new data store, new cross-team dependency, or a decision that is expensive to reverse | `standard` |
| Change inside one component, no contract change, no data ownership change, no new dependency | `light` |

Two ways to get this wrong, both common:

- **Under-tailoring** — running `light` on something that changes a contract. The tell is the impact analysis listing consumers outside your team. Escalate to `standard` the moment that happens; do not finish the light run.
- **Over-tailoring** — running `full` because it feels safer. It is not safer; it produces sixteen documents nobody reads, and the review then cannot distinguish the two that mattered.

## Required artifacts per profile

`R` = required · `C` = conditional (required only when the trigger applies) · `—` = not required

| Step | Artifact | light | standard | full | Conditional trigger |
|---|---|---|---|---|---|
| init | `sa-config.yaml` + scaffold | R | R | R | |
| intake | `sa-intent.md` | R (short form) | R | R | |
| intake | `stakeholders.md` | — | R | R | |
| drivers | `architecture-drivers.md` | C | R | R | any quality attribute is at risk |
| impact | `impact-analysis.md` | R | R | R | |
| options | `solution-options.md` | — | C | R | ≥2 credible whole-solution shapes exist |
| adr | `ADR-NNNN-*.md` | C | R | R | any decision that is expensive to reverse |
| hld | context + container views | C | R | R | the change adds or moves a container |
| hld | component view | — | C | C | container internals are non-obvious |
| hld | deployment view | — | C | R | runtime placement, region or network changes |
| flow | `<flow>.puml` + narrative | C | R | R | the change alters runtime behaviour across components |
| lld | `<component>.yaml` | — | R | R | |
| interface | OpenAPI / AsyncAPI | C | R | R | the change touches a contract |
| data | `data-design.md` | C | R | R | the change touches persisted data |
| data | `migration-plan.md` | C | C | C | existing data must change |
| security | `security-design.md` | C | R | R | new entry point, new data class, or new trust boundary |
| resilience | `resilience-design.md` | C | R | R | new remote dependency or changed availability target |
| observability | `observability-design.md` | C | R | R | new failure mode or new user-facing capability |
| cost | `cost-model.md` | — | C | R | new infrastructure or a > 20% change in run cost |
| risk | `risk-register.md` | C | R | R | any risky assumption exists |
| review | `design-review-<date>.md` | — | R | R | |
| handoff | `dev-handoff-<date>.md` | C | R | R | another team implements it |
| trace | `.trace-index.md` | R | R | R | |

## Gates per profile

| Profile | Gates enforced |
|---|---|
| `light` | G1 |
| `standard` | G1, G2, G4 |
| `full` | G1, G2, G3, G4 |

## Rules

1. **A skill excluded by the profile may still be run manually.** Tailoring reduces what is *required*, never what is *permitted*.
2. **`sa:review` does not report a profile-excluded artifact as missing.** It lists it under "Not required at profile `<p>`" — visible, but not a finding.
3. **A conditional trigger that fires promotes the artifact to required.** The skill that discovers the trigger says so and records it; it does not quietly skip.
4. **The profile is recorded in every Change Summary and in the review report.** A review with no stated profile cannot be interpreted later.
5. **Escalating profile mid-initiative is normal.** Record it as an `Update` to `sa-config.yaml` with the reason; do not backfill artifacts that the earlier profile legitimately skipped unless they are now required.
6. **`light` short-form intent** means: problem statement, in/out of scope, stakeholders, constraints. The rest of Standard 02 is optional at this profile — but the out-of-scope list is still non-empty, because that is what G1 checks.

## Checklist

Self-assess against this list before reporting the artifact done. Report pass/fail **per item** — never a silent pass. A failed item becomes an OPEN item with an owner; it is not deleted to make the list pass.

- [ ] `profile` present in `sa-config.yaml`
- [ ] Profile matches the selection table (no under- or over-tailoring)
- [ ] Every required artifact for the profile exists, or is an OPEN item with an owner
- [ ] Every conditional trigger that fired has been promoted to required and recorded
- [ ] Gates enforced match the profile table
- [ ] Profile stated in the Change Summary of every run
- [ ] Any mid-initiative profile change recorded with its reason
