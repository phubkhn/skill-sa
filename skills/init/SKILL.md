---
name: init
description: Scaffold the Solution Architect workspace: create sa-config.yaml and the docs/architecture directory tree. Use when starting architecture work in a repository for the first time, or when the user asks to set up / bootstrap / initialise SA docs.
---

# SA — Scaffold the SA workspace and configuration

| | |
|---|---|
| Journey step | 0 — Init |
| Gate | none |
| Standards | `../method/standards/19-naming-and-structure.md`, `../method/standards/00-sa-journey.md` |

**Method contract:** read `../method/SKILL.md` and `../method/standards/01-workflow-protocol.md` before acting. All nine execution phases (P1–P9) are defined there and are mandatory.

---

Bootstrap this repository for the SA journey.

Arguments: $ARGUMENTS — optional scope/initiative slug (kebab-case)

Steps:

1. Check whether `sa-config.yaml` exists at repo root. If it does, print it and ask whether to reconfigure — do not overwrite silently.

2. Ask (one round, batched) for:
   - scope/initiative slug — used in trace ids
   - docs root (default `docs/architecture`)
   - diagram tool (default PlantUML)
   - sync contract format (default OpenAPI 3.1) and async format (default AsyncAPI 2.6)
   - which optional steps are in play: data, security, observability, resilience (default: all on)

3. Write `sa-config.yaml`:

```yaml
scope: <slug>
docs-root: docs/architecture
diagram: plantuml
contracts:
  sync: openapi-3.1
  async: asyncapi-2.6
steps-enabled: [intake, drivers, impact, adr, hld, flow, lld, interface, data, security, observability, resilience, risk, review, handoff]
gates: {G1: true, G2: true, G3: true, G4: true}
trace-prefix: TR
```

4. Create the directory tree from `../method/standards/19-naming-and-structure.md`, with a `.gitkeep` in each empty directory. Create empty `_logs/.design-log` and `_logs/.trace-index.md` (with header row).

5. Create `docs/architecture/README.md` — a one-page map: what each directory holds, which command produces it, which standard governs it.

6. Report the tree created and tell the user: `Next: /sa:intake <scope>`.

Do not create any content artifacts here — only structure.
