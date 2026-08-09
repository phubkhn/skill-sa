# Resilience, Capacity & Operability — <scope>

<!-- Header block — copy from standards/01-workflow-protocol.md, phase P8 -->

## 1. Availability targets
| Capability | Target | Measured as | RTO | RPO | Source |
|---|---|---|---|---|---|

## 2. Dependency map
| Dependency | Criticality (hard/soft/optional) | Their availability | Ceiling imposed | Meets target? |
|---|---|---|---|---|

## 3. Failure mode analysis
| ID | Failure | Trigger | Blast radius | Detection | Automatic response | Manual response | User-visible effect | Residual risk |
|---|---|---|---|---|---|---|---|---|

## 4. Degradation modes
| Dependency down | System still does | System stops doing | User sees | Recovery on restore |
|---|---|---|---|---|

## 5. Tactics
| Call / path | Timeout | Retry policy | Backoff+jitter | Cap | Circuit breaker | Bulkhead | Idempotent |
|---|---|---|---|---|---|---|---|

**Timeout budget nesting**
| Chain | Caller timeout | Sum of callee budget | Nests? |
|---|---|---|---|

## 6. Capacity
| Component | Unit of work | Expected | Peak | Per-instance capacity | Instances | Headroom | Scaling trigger | Ceiling | Source (measured/extrapolated/assumed) |
|---|---|---|---|---|---|---|---|---|---|

## 7. Recovery
| Scenario | Procedure | Tested? | Duration | Data loss window |
|---|---|---|---|---|

## 8. Operability
| Item | Approach |
|---|---|
| Deployment strategy | |
| Rollback | |
| Feature flags | |
| Safe config change | |
| Runbooks required | |

## 9. Verification plan
| Test | Type | Cadence | Pass criteria | Owner |
|---|---|---|---|---|
