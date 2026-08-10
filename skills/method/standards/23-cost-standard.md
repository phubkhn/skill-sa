# Standard 23 — Cost Model

**Artifact:** `01-analysis/cost-model.md`
**Purpose:** an architecture nobody has costed is an architecture nobody has approved. Cost is a quality attribute with a currency attached, and it is decided by the same choices as latency and availability.

## Required content

| Section | Content |
|---|---|
| Cost drivers | the handful of variables that actually move the number — request volume, data volume, retention, instance hours, egress, licences, operating headcount |
| Build cost | one-off effort and spend to deliver: engineering effort per work package, one-off licences, migration, dual-run |
| Run cost | recurring monthly cost per component group, at expected and at peak load |
| Unit economics | cost per unit of business value — per request, per order, per tenant, per GB retained |
| Cost at scale | the run cost at the 12-month and 36-month volume projections from the data design |
| Comparison | run cost of each option in `solution-options.md`, and of "do nothing" |
| Cost of the quality attributes | what the availability target, the retention period and the latency target each cost — separately |
| Optimisation levers | what can be turned down later, how much it saves, and what it costs in quality |
| Assumptions & confidence | every number labelled measured / quoted / estimated, with the source |
| Cost controls | budgets, alerts, tagging/allocation, and who owns the bill |

## Run cost table

| Component group | Resource | Unit | Qty at expected | Qty at peak | Unit cost | Monthly (expected) | Monthly (peak) | Source |
|---|---|---|---|---|---|---|---|---|

## Cost of quality table

The point of this table is to let a stakeholder buy a lower number knowingly.

| Driver | Current target | Monthly cost attributable | Cost at one notch lower | What is lost |
|---|---|---|---|---|
| Availability | 99.95% | | 99.9% → | longer recovery, no hot standby |
| Retention | 7 years | | 2 years → | no historical analytics |
| Latency | p99 300 ms | | p99 800 ms → | fewer instances, no cache tier |

## Rules

1. **Cost is estimated against the design, not the vendor price list.** Start from the capacity table in the resilience design; if there is no capacity table, there is no cost model — say so instead of guessing.
2. **Every number carries its source and its confidence.** `measured` (from an existing system), `quoted` (from a vendor or a public price), `estimated` (derived) — and estimates state the formula.
3. **Run cost dominates build cost** for anything that lives more than a year. Present both, but rank options by run cost at the 36-month volume.
4. **Cost the quality attributes separately.** "The system costs X" is not actionable; "the availability target costs 40% of X" is.
5. **Include the unglamorous lines:** egress, inter-zone traffic, log and metric ingestion, backup storage, non-production environments, and the people who operate it. These are where cost models are wrong.
6. **Non-production is a real cost.** State how many environments and their sizing relative to production.
7. **Name the bill owner.** A cost model with no owning budget is an estimate, not a control.
8. **Re-cost on any change to the capacity table, the retention period, or the availability target.** Those three move the number more than anything else.
9. **Currency and time base stated once**, at the top. Mixed monthly/annual figures in one table is the most common error here.

## Anti-patterns

- A cost model built from list prices with no capacity numbers behind it
- Run cost quoted at expected load only, with no peak figure
- Optimisation levers listed with savings but not with what they cost in quality
- Build cost presented as the headline for a system that will run for five years

## Checklist

Self-assess against this list before reporting the artifact done. Report pass/fail **per item** — never a silent pass. A failed item becomes an OPEN item with an owner; it is not deleted to make the list pass.

- [ ] Cost drivers identified and traced to the capacity table
- [ ] Build cost and run cost presented separately
- [ ] Run cost given at both expected and peak load
- [ ] Run cost projected at 12 and 36 months using the data design's growth numbers
- [ ] Unit economics stated in a business unit, not a technical one
- [ ] Every option in `solution-options.md` costed, including "do nothing"
- [ ] Availability, retention and latency targets costed individually
- [ ] Egress, telemetry ingestion, backups and non-production environments included
- [ ] Operating effort (people) included
- [ ] Every number labelled measured / quoted / estimated, with its source
- [ ] Currency and time base stated once and used consistently
- [ ] Optimisation levers state both the saving and the quality cost
- [ ] Budget owner named; cost alerts and allocation tagging defined
- [ ] Material cost risks pushed to the risk register
