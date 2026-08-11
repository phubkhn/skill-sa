# Runtime Flow

Model scenarios where order, failure, consistency, or timing changes the architecture. One diagram covers one trigger and its terminal outcomes.

## Required content

- trigger, preconditions, and participants
- numbered happy path
- applicable failure and timeout paths
- bounded retry and backoff behaviour
- idempotency for non-safe or replayed operations
- durability and consistency points
- compensation or reconciliation where needed
- success, failure, partial, and timed-out outcomes as applicable
- signals needed to detect important failures

Participant names match the HLD. Caller timeouts must accommodate callee timeouts and bounded retries. Never retry a non-idempotent operation without a deduplication mechanism.

## Checklist

- [ ] One architecture-significant scenario
- [ ] Participants match the HLD or are explicitly proposed
- [ ] Happy path and applicable failure paths are present
- [ ] Timeouts and retries are safe and bounded
- [ ] Idempotency is explicit
- [ ] Consistency and durability points are visible
- [ ] Recovery or reconciliation is defined
- [ ] Terminal outcomes and detection signals are clear
