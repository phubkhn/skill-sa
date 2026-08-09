# Flow — <flow-name>

<!-- header block. Accompanies 04-flows/<flow-name>.puml -->

**Trigger:**
**Participants:** <must match HLD element names exactly>
**Drivers exercised:**
**Preconditions:**
**Terminal states:** success / failure / partial / timed-out

## Steps
| # | Actor | Action | Data | Sync/Async | Timeout | Retry | Idempotent | Failure behaviour | Emits |
|---|---|---|---|---|---|---|---|---|---|

## Consistency points
| Point | Durable? | Consistency | Window | Visible effect during window |
|---|---|---|---|---|

## Failure paths covered
| Failure | Covered? | Behaviour | Compensation |
|---|---|---|---|
| Dependency timeout | | | |
| Dependency error | | | |
| Dependency unavailable | | | |
| Partial success | | | |
| Duplicate / replayed request | | | |
| Concurrent conflicting request | | | |
| Invalid input | | | |
| Authorisation denied | | | |
| Resource exhausted | | | |
| Message lost | | | |
| Message out of order | | | |
| Poison message | | | |

## Timeout budget check
| Call chain | Caller timeout | Sum of callee budget | Nests correctly? |
|---|---|---|---|
