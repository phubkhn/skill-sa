# HLD Catalogue — <view> — <scope>

<!-- Accompanies every .puml in 03-hld/ -->

## Elements
| Element | Type | Responsibility | Owns (data) | Technology | Drivers addressed |
|---|---|---|---|---|---|

## Relationships
| From | To | Protocol | Sync/Async | Purpose | Failure behaviour |
|---|---|---|---|---|---|

## Coupling checks
| Check | Result | Detail |
|---|---|---|
| Sync fan-out ≤ 3 | | |
| Round trips per user action ≤ 5 | | |
| No shared data store | | |
| No container-level cycles | | |
| No god component | | |
| No orphan elements | | |

## Elements not traced to a driver
| Element | Justification or action |
|---|---|
