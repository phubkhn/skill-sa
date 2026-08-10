# Architecture — <scope>

Design artifacts for this repository. Produced and maintained by the `sa` skill set.

**Profile:** <light | standard | full> — see `21-tailoring.md`. Directories the profile does not require will be empty; that is intentional, not a gap.

## Map

| Directory | Holds | Produced by | Standard |
|---|---|---|---|
| `00-context/` | intent, drivers, stakeholders, principles | `sa:intake`, `sa:drivers` | 02, 03 |
| `01-analysis/` | impact analysis, solution options, cost model, risk register | `sa:impact`, `sa:options`, `sa:cost`, `sa:risk` | 04, 25, 23, 14 |
| `02-decisions/` | ADRs and their index | `sa:adr` | 05 |
| `03-hld/` | C4 context / container / component + deployment views | `sa:hld` | 06, 18, 22 |
| `04-flows/` | runtime sequence diagrams + narratives | `sa:flow` | 07, 18 |
| `05-lld/` | per-component internal design | `sa:lld` | 08 |
| `06-interfaces/` | OpenAPI, AsyncAPI, shared schemas | `sa:interface` | 09 |
| `07-data/` | data model, data design, migration plan | `sa:data` | 10, 18 |
| `08-crosscutting/` | security, resilience, observability designs | `sa:security`, `sa:resilience`, `sa:observability` | 11, 13, 12 |
| `09-review/` | design review reports | `sa:review` | 15, 20 |
| `10-handoff/` | implementation handoff packages | `sa:handoff` | 16, 24 |
| `_logs/` | design log and trace index | every skill / `sa:trace` | 01, 17 |

## How to read this

Start with `00-context/sa-intent.md` — the problem. Then `00-context/architecture-drivers.md` — what makes a solution good. Then `02-decisions/adr-index.md` — what was chosen and why. The diagrams make sense only after those three.

## Conventions

- Diagrams are PlantUML text, so they diff and review like code. No binary diagram files.
- Every artifact carries a header with a trace-id linking it to the change that caused it.
- Only `Accepted` artifacts may be cited by downstream work. `Draft` means not yet agreed.
- `Superseded` artifacts stay in place with a pointer to their successor. Nothing is deleted.

## Working on this

Run `sa:trace <scope> --stale` before trusting anything: it reports artifacts whose upstream has moved since they were written. Staleness is not corrected automatically — that is the architect's call.
