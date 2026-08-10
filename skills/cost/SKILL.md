---
name: cost
description: Build the architecture cost model — build cost, run cost at expected and peak load, unit economics, the cost of each quality target, and optimisation levers. Use when the user asks what a design costs, asks for a TCO or run-rate estimate, or asks which quality targets are driving the bill.
allowed-tools: Read, Grep, Glob
---

# SA — Model the build and run cost of the design

| | |
|---|---|
| Journey step | 13 — Cost |
| Produces | 01-analysis/cost-model.md |
| Inputs | 08-crosscutting/resilience-design.md (capacity table), 03-hld/*, 07-data/data-design.md, 00-context/architecture-drivers.md, 01-analysis/solution-options.md |
| Gate | none |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/23-cost-standard.md` |

**Method contract:** read `../method/SKILL.md`, `../method/standards/01-workflow-protocol.md` and `../method/standards/26-operating-guardrails.md` before acting. All nine execution phases (P1–P9) are mandatory, as is the write boundary at P7.

**Checklist:** the `## Checklist` section of `../method/standards/23-cost-standard.md` — self-assess item by item in P9.

---

Follow `../method/standards/01-workflow-protocol.md` P1–P9.

**P3:** read the resilience design's **capacity table** (this is the basis of the whole model — instances, per-instance capacity, headroom), the deployment view (node types, regions, cross-zone traffic), the data design (volume, growth, retention), the drivers (the availability, latency and retention targets being paid for), and the options paper if one exists.

**If there is no capacity table, stop.** Say that the cost model has no basis and that `sa:resilience` must run first. Do not substitute vendor list prices for capacity analysis — a cost model built that way is confident and wrong.

**Method:**

1. **Identify the cost drivers** — the handful of variables that actually move the number. Everything else is noise; do not model it.
2. **Build cost:** engineering effort per work package, one-off licences, migration and dual-run, data transfer for the initial load.
3. **Run cost** per component group, at **expected and at peak** load, from the capacity table. Include the lines that are usually forgotten: egress, inter-zone traffic, telemetry ingestion and retention, backup storage, non-production environments, and operating headcount.
4. **Project to 12 and 36 months** using the growth numbers from the data design. Rank options and decisions by the 36-month figure, not the first month.
5. **Unit economics:** cost per request, per order, per tenant, or per GB retained — whichever unit the business already uses.
6. **Cost the quality targets individually.** For availability, retention and latency: what the current target costs, what one notch lower would cost, and what is lost. This is the table stakeholders actually act on.
7. **Optimisation levers:** what can be turned down later, the saving, and the quality cost of doing so.
8. **Label every number** measured / quoted / estimated, with its source; estimates state their formula. State currency and time base once, at the top.
9. **Name the budget owner** and define cost alerts and allocation tagging.
10. Emit material cost uncertainties as **candidate risks** for the register.

**P6 Change Summary must include** the cost drivers, the expected-vs-peak monthly totals, and the confidence label distribution — before writing.

**P8:** `../method/templates/cost-model.md`.

**P9:** report the 36-month run cost, the three largest line items, the cost attributable to the availability and retention targets, and every figure still labelled `estimated`, then `Next: sa:risk <scope>`.
