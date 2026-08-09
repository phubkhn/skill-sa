---
name: hld
description: Produce C4 context, container and component diagrams with element and relationship catalogues and coupling checks. Use when the user asks for a high-level design, system architecture diagram, or C4 views.
---

# SA — Produce context, container and component views

| | |
|---|---|
| Journey step | 5 — HLD |
| Produces | 03-hld/system-context.puml, 03-hld/container-<system>.puml, 03-hld/component-<container>.puml, element + relationship catalogues |
| Inputs | 00-context/*, 01-analysis/impact-analysis.md, 02-decisions/* |
| Gate | none |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/06-hld-standard.md`, `../method/standards/18-diagram-conventions.md` |

**Method contract:** read `../method/SKILL.md` and `../method/standards/01-workflow-protocol.md` before acting. All nine execution phases (P1–P9) are defined there and are mandatory.

**Checklist:** the `## Checklist` section of `../method/standards/06-hld-standard.md` — self-assess item by item in P9.

---

Follow `../method/standards/01-workflow-protocol.md` P1–P9.

Arguments: $ARGUMENTS — scope, optionally a view (`context|container|component <container>`). Default: context + container.

**P3:** read intent, drivers, impact analysis, and every `Accepted` ADR. If a structural ADR is still `Proposed`, say so — the HLD will encode a decision that is not yet agreed.

**Method:**

1. **Context view:** system boundary, every human role with their goal, every external system with direction and nature of exchange, trust boundary.
2. **Container view:** decompose by responsibility and rate of change. Every container gets a responsibility, an owned-data statement, and a technology. Every relationship gets direction, protocol, sync/async, purpose, and failure behaviour.
3. **Component view:** only for containers whose internals are non-obvious.
4. Run the **coupling checks** from Standard 06 (fan-out, chattiness, shared store, cycles, god component, orphans) and report every failure in the Change Summary — before writing.
5. Verify each element traces to at least one driver. Report elements that do not; they are candidates for deletion.
6. Verify the diagram matches the ADRs (sync vs async, ownership, topology). Any mismatch is a stop-and-ask.
7. Produce the **element catalogue** and **relationship catalogue** tables alongside the diagram.

**P8:** diagram header comment per Standard 18. Update mode: modify only affected elements, preserve the rest verbatim. Validate `@startuml/@enduml` balance, no duplicate or undeclared aliases.

**P9:** report coupling-check results and untraced elements, then `Next: /sa:gen-flow <flow-name>` for each structure-shaping scenario.
