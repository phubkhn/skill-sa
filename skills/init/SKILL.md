---
name: init
description: Scaffold the Solution Architect workspace: create sa-config.yaml and the docs/architecture directory tree. Use when starting architecture work in a repository for the first time, or when the user asks to set up / bootstrap / initialise SA docs. Not for generating CLAUDE.md or initialising a codebase — this only creates architecture documentation structure.
allowed-tools: Read, Grep, Glob
---

# SA — Scaffold the SA workspace and configuration

| | |
|---|---|
| Journey step | 0 — Init |
| Gate | none |
| Produces | `sa-config.yaml`, the `<docs-root>` tree, `_logs/.design-log`, `_logs/.trace-index.md`, `<docs-root>/README.md` |
| Standards | `../method/standards/19-naming-and-structure.md`, `../method/standards/00-sa-journey.md`, `../method/standards/21-tailoring.md` |

**Method contract:** read `../method/SKILL.md`, `../method/standards/01-workflow-protocol.md` and `../method/standards/26-operating-guardrails.md` before acting. This skill is the one exception to the write boundary: it may create the directory tree and empty logs before confirmation, because structure is reversible and contains no content. It still writes no artifact content.

---

Bootstrap this repository for the SA journey.

Arguments: $ARGUMENTS — optional scope/initiative slug (kebab-case)

Steps:

1. Check whether `sa-config.yaml` exists at repo root. If it does, print it and ask whether to reconfigure — do not overwrite silently.

2. Ask (one round, batched) for:
   - scope/initiative slug — used in trace ids
   - **profile** — `light` | `standard` | `full`. Present the selection table from `../method/standards/21-tailoring.md` and let the user choose; default `standard`. This decides which of the later steps are required at all, so it is the most consequential answer here.
   - **language** for artifact prose — default `en`. Identifiers stay English regardless.
   - docs root (default `docs/architecture`)
   - diagram tool (default PlantUML)
   - sync contract format (default OpenAPI 3.1) and async format (default AsyncAPI 2.6)
   - which optional steps are in play (default: everything the chosen profile requires)

3. Write `sa-config.yaml` at the repository root:

```yaml
scope: <slug>
profile: standard              # light | standard | full — see standard 21
language: en                   # artifact prose; identifiers stay English kebab-case
docs-root: docs/architecture
diagram: plantuml
contracts:
  sync: openapi-3.1
  async: asyncapi-2.6
steps-enabled: [intake, drivers, impact, options, adr, hld, flow, lld, interface,
                data, security, resilience, observability, cost, risk, review, handoff]
gates: {G1: true, G2: true, G3: true, G4: true}
trace-prefix: TR
```

Set `gates` from the profile table in Standard 21 (`light` → G1 only; `standard` → G1, G2, G4; `full` → all four), and trim `steps-enabled` to what the profile requires. Tell the user which steps the profile dropped and that they can still be run manually.

Use `../method/templates/sa-config.yaml` as the skeleton.

4. Create the directory tree from `../method/standards/19-naming-and-structure.md`, relative to `docs-root`, with a `.gitkeep` in each empty directory. Create `_logs/.design-log` from `../method/templates/design-log.yaml`, `_logs/.trace-index.md` from `../method/templates/trace-index.md`, and `_logs/.failure-log` from `../method/templates/failure-log.yaml`.

5. Create `<docs-root>/README.md` from `../method/templates/docs-readme.md` — a one-page map: what each directory holds, which skill produces it, which standard governs it.

6. Report the tree created, the profile chosen and what it excludes, then: `Next: sa:intake <scope>`.

Do not create any content artifacts here — only structure.
