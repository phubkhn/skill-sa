# Standard 18 — Diagram Conventions

Diagrams are **written as text** (PlantUML) so they diff, review, and version like code. No binary diagram files in the repository.

## Model: C4

| Level | Diagram | Audience | Question |
|---|---|---|---|
| L1 | System Context | everyone | what is the system, who uses it, what does it talk to? |
| L2 | Container | technical | what are the deployable/runnable parts? |
| L3 | Component | implementers | what is inside one container? |
| L4 | Code / detail | implementers | expressed as LLD YAML, not a diagram |

Do not mix levels in one diagram. A container diagram that shows classes is a container diagram that will not be maintained.

## Mandatory header comment (every `.puml`)

```
' Artifact: <context|container|component|sequence|data>
' Version: <N>
' Last updated: <YYYY-MM-DD>
' Updated by: <name>
' Trace ID: <TR-...>
' Changes: <what changed | "Initial">
```

## Element rules

| Rule | Why |
|---|---|
| Every element has a one-line responsibility in its description | an unlabelled box is unreviewable |
| Every relationship has: direction, label (what/why), and technology/protocol | "A → B" tells the reader nothing |
| Sync vs async is visually distinct — solid `-->` sync, dotted `..>` async/event | the single most important runtime distinction |
| External systems sit outside all boundary/package elements | keeps the trust boundary legible |
| Max ~12 elements per diagram — beyond that, decompose | past ~12, nobody reads it |
| Colour carries meaning or is not used | decorative colour misleads |
| Legend on every diagram that uses more than one line style | |

## Sequence diagram rules

| Rule |
|---|
| Participants must exist as elements in the corresponding HLD diagram, with identical names |
| Show the trigger and the terminal state — a flow with no ending is incomplete |
| Every external call shows its timeout and retry policy (as a note if not as a message) |
| At least one `alt`/`group` covering the primary failure path |
| Async publish shows the topic/queue name; async consume shows the subscriber |
| Long-running/background work shown explicitly, not implied |

## Data diagram rules

| Rule |
|---|
| Show ownership boundaries — which component owns which entity |
| Cardinality on every relationship |
| Mark sensitive/PII attributes |
| Do not model physical indexes/partitions here — that belongs in LLD |

## Rendering

Keep diagrams valid: after generating, verify balanced `@startuml/@enduml`, no undeclared aliases, no duplicate alias definitions. If a PlantUML renderer is available, render to check; if not, state that rendering was not verified.
