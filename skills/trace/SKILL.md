---
name: trace
description: Build and query the end-to-end traceability index: what one decision touched, orphan artifacts, stale artifacts, and driver coverage. Use when the user asks why a design element exists, what a change affected, or what is now out of date.
---

# SA — Build and query the end-to-end traceability index

| | |
|---|---|
| Journey step | 16 — Trace |
| Produces | _logs/.trace-index.md (regenerated), report to stdout |
| Gate | none |
| Standards | `../method/standards/17-traceability-and-change.md` |

**Method contract:** read `../method/SKILL.md` and `../method/standards/01-workflow-protocol.md` before acting. All nine execution phases (P1–P9) are defined there and are mandatory.

---

Arguments: $ARGUMENTS — one of:
- `<scope>` — rebuild the trace index for a scope (default)
- `<TR-scope-NNN>` — show everything one decision touched
- `--orphans` — artifacts with no trace-id, or trace-ids with no origin
- `--stale` — artifacts whose upstream changed after they were last written
- `--coverage` — drivers with no artifact, and artifacts with no driver

Steps:

1. Read `sa-config.yaml` for `docs-root` and `trace-prefix`.
2. Scan every artifact header block and `_logs/.design-log` for trace ids, change types, cr-refs, versions, and dates.
3. **Rebuild `_logs/.trace-index.md`** — one row per trace-id: origin, type, date, artifacts touched (path + version), status. Sort by trace-id.
4. **`<TR-...>` mode:** run `grep -rn "<TR-...>" <docs-root>` and present the results grouped by journey step, in dependency order, so the reader sees the decision propagate from driver to handoff.
5. **`--orphans`:** report (a) artifacts with no trace-id in their header, (b) trace-ids appearing in artifacts but never in an origin record. Both are traceability defects; state which artifact and what to add.
6. **`--stale`:** using the staleness table in Standard 17, compare each artifact's last-write date/version against its upstreams'. Report every artifact whose upstream moved after it did, with the command that refreshes it. **Do not regenerate anything** — staleness is the SA's call.
7. **`--coverage`:** cross-reference `00-context/architecture-drivers.md` against all artifacts. Report drivers addressed nowhere (a design gap) and design elements addressing no driver (possible over-engineering).

This command never writes to any artifact other than `_logs/.trace-index.md`.
