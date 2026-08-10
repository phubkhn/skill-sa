# Standard 22 — Deployment & Infrastructure View

**Artifact:** `03-hld/deployment-<environment>.puml` + the node catalogue
**Purpose:** the container view says *what the parts are*; the deployment view says *where they run and what carries the traffic between them*. Availability, latency, cost and blast radius are all decided here, and none of them are visible in C4 L1–L3.

Produced by `sa:hld` when the deployment view is required (Standard 21) or requested explicitly.

## Required content

| Section | Content |
|---|---|
| Environments | which environments exist, and which of them this view describes; how they differ from production |
| Nodes | every execution and storage location: cluster, VM, serverless runtime, managed service, device, on-prem host |
| Placement | which container from the L2 view runs on which node, and how many instances |
| Topology | region(s), availability zone(s), and what is replicated across which of them |
| Network paths | every link between nodes: protocol, port class, encryption, whether it crosses a public network |
| Boundaries | network boundaries, trust boundaries, and administrative boundaries — they are rarely the same lines |
| Ingress & egress | how traffic enters (load balancer, gateway, CDN) and every route out (NAT, proxy, partner link) |
| Shared infrastructure | anything not exclusively owned by this system, and who else uses it |
| Scaling | scaling unit and mechanism per node group; minimum and maximum instance count |
| Failure domains | what fails together — a node group, a zone, a region, a shared dependency |
| Environment parity | where non-production deliberately differs from production, and what that hides |

## Node catalogue

Ships with every deployment diagram.

| Node | Type | Hosts (containers) | Region / zone | Instances (min–max) | Scaling trigger | Failure domain | Owner |
|---|---|---|---|---|---|---|---|

## Network path catalogue

| From | To | Protocol | Port class | Encryption | Crosses public network | Latency budget | Notes |
|---|---|---|---|---|---|---|---|

## Rules

1. **The deployment view is drawn from the container view.** Every container appears on exactly one node group, or the mismatch is a finding. A container that appears nowhere is not deployed.
2. **Name the failure domain of every node.** "Multi-AZ" is a claim, not a design — say which nodes span which zones and what happens when one is lost.
3. **Co-location is a decision.** Two containers on the same node share a failure domain and a resource pool. If that is intended, say why; if it is an accident, separate them.
4. **Every network hop has a latency budget** consistent with the end-to-end budget in the drivers (Standard 03, NFR budget allocation). Hops whose sum exceeds the target are a finding, not a rounding error.
5. **Every cross-boundary link states its encryption.** "Internal network" is not encryption.
6. **Shared infrastructure names its other tenants.** A shared cluster, database instance, or gateway is a coupling that does not appear anywhere else in the design.
7. **Environment parity gaps are written down.** The gap between production and the environment you tested in is where the incident comes from.
8. **Physical detail stops at the design boundary.** Node types, counts, and topology belong here; instance SKUs, subnet CIDRs and IaC module names do not, unless a driver forces them.

## Diagram conventions

Follows Standard 18, with these additions:

- Use PlantUML deployment nodes (`node`, `database`, `cloud`) — not container-view boxes.
- One diagram per environment. Do not overlay production and staging.
- Zone and region boundaries are drawn as nested nodes, never as colour alone.
- Public network segments are visually distinct from private ones, with a legend.

## Checklist

Self-assess against this list before reporting the artifact done. Report pass/fail **per item** — never a silent pass. A failed item becomes an OPEN item with an owner; it is not deleted to make the list pass.

- [ ] Environment named, and its differences from production stated
- [ ] Every container from the L2 view placed on exactly one node group
- [ ] Node catalogue complete: type, region/zone, instance range, scaling trigger, owner
- [ ] Failure domain named per node group
- [ ] Deliberate co-locations justified; accidental ones separated
- [ ] Every network path has protocol, encryption, and public/private classification
- [ ] Latency budget per hop, summing within the end-to-end driver target
- [ ] Ingress and every egress route shown
- [ ] Shared infrastructure identified with its other tenants
- [ ] Trust, network and administrative boundaries drawn separately where they differ
- [ ] Environment parity gaps stated
- [ ] Consistent with the resilience design's zone/region loss failure modes
- [ ] `@startuml/@enduml` balanced; no undeclared or duplicate aliases
