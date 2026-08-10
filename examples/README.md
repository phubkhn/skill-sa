# Worked example — `express-lane`

A deliberately small, complete pass through the journey at **`standard` profile**. Every artifact is real but abbreviated: enough to show the shape, the level of specificity, and how one artifact feeds the next. Read it when a template alone does not make clear what "done" looks like.

The domain is intentionally dull — a hypothetical order-taking system adding an expedited path. Nothing here is domain knowledge you need; the point is the method.

## What to notice

1. **Numbers, everywhere.** `architecture-drivers.md` has no adjective standing alone. This is the single biggest difference between a design that gets built and one that gets rewritten.
2. **The out-of-scope list is longer than the in-scope list.** That is normal and it is what G1 checks.
3. **The ADR rejects a real option**, and the rejected option is one a reasonable person would have chosen.
4. **The impact analysis contains `None (verified)` rows.** Absence from the table would have been evidence that nobody looked.
5. **The flow's failure paths outnumber its happy path steps.**
6. **Ownership is decided in the data design and back-propagated to the LLD** — the two-pass rule in action.
7. **The review finds real problems.** A review that finds nothing was not a review.

## Files

| File | Step | Shows |
|---|---|---|
| `sa-config.yaml` | 0 | profile and gate configuration |
| `00-context/sa-intent.md` | 1 | problem stated without solution language |
| `00-context/architecture-drivers.md` | 2 | six-part scenarios with measures |
| `01-analysis/impact-analysis.md` | 3 | blast-radius walk and verified-no-impact rows |
| `02-decisions/ADR-0001-async-order-intake.md` | 4 | two genuine options, negative consequences, compliance mechanism |
| `03-hld/container-orders.puml` | 5 | container view, with sync/async visually distinct |
| `03-hld/container-orders-catalogue.md` | 5 | element + relationship catalogues, budget allocation, coupling checks |
| `04-flows/client-submit-express-order.puml` | 6 | failure paths, timeouts, idempotency |
| `05-lld/order-intake.yaml` | 7 | responsibilities mapped to operations |
| `09-review/design-review-2026-03-14.md` | 15 | findings with evidence and a mechanical verdict |

Steps not shown (interfaces, security, resilience, observability, cost, risk, handoff, trace) follow the same pattern; their templates are self-explanatory once these are read.

## How this example was produced

By running the skills in order and answering their questions. It was not hand-written to look good — which is why the review report is not clean.
