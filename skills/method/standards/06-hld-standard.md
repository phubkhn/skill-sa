# Standard 06 — High-Level Design (C4 L1–L3)

**Artifacts:** `03-hld/system-context.puml`, `container-<system>.puml`, `component-<container>.puml`
**Purpose:** show the parts, their responsibilities, and how they are arranged — and nothing more.

## Views and what each must contain

### L1 System Context
- The system as a single box with a one-line purpose
- Every human/role that interacts with it, with their goal
- Every external system it exchanges data with, with the direction and nature of exchange
- Trust boundary marked

### L2 Container
- Every independently deployable/runnable unit: services, apps, jobs, data stores, message brokers, gateways
- Per container: responsibility, technology, and what it owns
- Every relationship: direction, protocol, purpose, sync/async
- Where state lives, and which container owns it

### L3 Component (per container that warrants it)
- Internal building blocks and their responsibilities
- Which component implements which interface operation
- Dependencies inward/outward
- Only produce this for containers with non-obvious internals

## Decomposition rules

1. **Decompose by responsibility and rate of change**, not by technical layer. A box named "business logic layer" is not a design.
2. **One owner per capability.** Two components owning the same capability is a defect, not a style.
3. **Data ownership is exclusive.** One writer per data element; everyone else reads via a contract.
4. **Dependencies point one way.** Cycles between containers are a finding; if unavoidable, they need an ADR.
5. **Every element traces to a driver.** A component that satisfies no driver should not exist.
6. **The diagram must match the ADRs.** If the ADR says async, the diagram shows dotted lines.

## Coupling checks (run before finishing)

| Check | Fail condition |
|---|---|
| Fan-out | one container synchronously calls > 3 others in a single request path |
| Chatty integration | a single user action produces > 5 network round trips |
| Shared database | two containers write the same store |
| Cyclic dependency | A → B → A at container level |
| Godot component | one container holds > 40% of the responsibilities |
| Orphan | element with no inbound and no outbound relationship |

## Documentation alongside the diagram

Every HLD diagram ships with an element catalogue:

| Element | Type | Responsibility | Owns (data) | Technology | Drivers addressed |
|---|---|---|---|---|---|

And a relationship catalogue:

| From | To | Protocol | Sync/Async | Purpose | Failure behaviour |
|---|---|---|---|---|---|

The `Failure behaviour` column is not optional — it is where resilience design begins.

## Update discipline

In update mode: preserve untouched parts of the diagram byte-for-byte, change only affected elements, bump the version comment, and state the delta in the changelog. Never regenerate a diagram from scratch to "clean it up" without saying so.

## Checklist

Self-assess against this list before reporting the artifact done. Report pass/fail **per item** — never a silent pass. A failed item becomes an OPEN item with an owner; it is not deleted to make the list pass.

- [ ] Diagram header comment complete (artifact, version, date, author, trace, changes)
- [ ] Levels not mixed within a diagram
- [ ] Every element has a one-line responsibility
- [ ] Every relationship has direction, label, protocol, and purpose
- [ ] Sync vs async visually distinct; legend present
- [ ] External systems outside the trust boundary
- [ ] ≤ ~12 elements per diagram
- [ ] Data ownership stated per container; no store shared by two containers
- [ ] Relationship catalogue includes a failure-behaviour column, filled
- [ ] Coupling checks run and reported: fan-out, chattiness, cycles, god component, orphans
- [ ] Every element traces to ≥1 driver, or is flagged for deletion
- [ ] Diagram agrees with every Accepted ADR
- [ ] Update mode preserved untouched elements verbatim
- [ ] `@startuml/@enduml` balanced; no duplicate or undeclared aliases
