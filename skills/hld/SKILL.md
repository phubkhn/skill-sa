---
name: hld
description: Produce C4 context, container and component diagrams with element and relationship catalogues and coupling checks. Use when the user asks for a high-level design, system architecture diagram, C4 views, or a deployment / infrastructure view.
allowed-tools: Read, Grep, Glob
---

# SA — Produce context, container and component views

| | |
|---|---|
| Journey step | 5 — HLD |
| Produces | 03-hld/system-context.puml, 03-hld/container-<system>.puml, 03-hld/component-<container>.puml, 03-hld/deployment-<environment>.puml, element + relationship + node catalogues |
| Inputs | 00-context/*, 01-analysis/impact-analysis.md, 02-decisions/* |
| Gate | none |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/06-hld-standard.md`, `../method/standards/18-diagram-conventions.md`, `../method/standards/22-deployment-view.md` |

**Method contract:** read `../method/SKILL.md`, `../method/standards/01-workflow-protocol.md` and `../method/standards/26-operating-guardrails.md` before acting. All nine execution phases (P1–P9) are mandatory, as is the write boundary at P7.

**Checklist:** the `## Checklist` section of `../method/standards/06-hld-standard.md` — self-assess item by item in P9.

## When to use

- "what are the components", "draw the architecture", "C4 diagram", "system context"
- "where does it run", "which regions", "what's the network topology" — the deployment view
- After the structural ADRs are Accepted; the HLD encodes decisions, it does not make them

## When not to use

| Request | Use instead |
|---|---|
| "how does a request flow through it" | `sa:flow` — static structure vs behaviour over time |
| "what's inside this component" | `sa:lld` |
| "should it be async or sync" | `sa:adr` — decide first, then draw; a diagram is not a decision |
| infrastructure-as-code, Kubernetes manifests | not this skill set — the deployment *view*, not the deployment |

---

Follow `../method/standards/01-workflow-protocol.md` P1–P9.

Arguments: $ARGUMENTS — scope, optionally a view (`context|container|component <container>|deployment <environment>`). Default: context + container, plus deployment when the profile requires it (Standard 21).

**P3:** read intent, drivers, impact analysis, and every `Accepted` ADR. If a structural ADR is still `Proposed`, say so — the HLD will encode a decision that is not yet agreed.

**Method:**

1. **Context view:** system boundary, every human role with their goal, every external system with direction and nature of exchange, trust boundary.
2. **Container view:** decompose by responsibility and rate of change. Every container gets a responsibility, an owned-data statement, and a technology. Every relationship gets direction, protocol, sync/async, purpose, and failure behaviour.
3. **Component view:** only for containers whose internals are non-obvious.

3b. **Deployment view** (per `../method/standards/22-deployment-view.md`, one diagram per environment): place every container on exactly one node group; state region/zone, instance range, scaling trigger and failure domain per node; give every network path a protocol, an encryption statement and a latency budget; name the other tenants of any shared infrastructure; record where non-production differs from production. A container that appears on no node is not deployed — that is a finding, not an omission.
4. Run the **coupling checks** from Standard 06 (fan-out, chattiness, shared store, cycles, god component, orphans) and report every failure in the Change Summary — before writing.
5. Verify each element traces to at least one driver. Report elements that do not; they are candidates for deletion.
6. Verify the diagram matches the ADRs (sync vs async, ownership, topology). Any mismatch is a stop-and-ask.
7. Produce the **element catalogue** and **relationship catalogue** tables alongside the diagram (and the **node catalogue** with the deployment view). The element catalogue carries the interface-spec disposition for each element — a spec path, or `N/A — <reason>`; gate G3 reads this column.
8. **Allocate the NFR budget:** split each end-to-end latency and availability driver across the hops in the relationship catalogue. If the hop budgets plus overhead exceed the target, that is a finding now — report it in the Change Summary.
9. **One owning team per container.** A container two teams deploy is a finding: either split it or consolidate ownership, and record the choice in an ADR.

**P8:** `../method/templates/hld-catalogue.md` for the element and relationship catalogues, `../method/templates/deployment-catalogue.md` for the deployment view. Diagram header comment per Standard 18. Update mode: modify only affected elements, preserve the rest verbatim. Validate `@startuml/@enduml` balance, no duplicate or undeclared aliases.

**P9:** report coupling-check results and untraced elements, then `Next: sa:flow <flow-name>` for each structure-shaping scenario.
