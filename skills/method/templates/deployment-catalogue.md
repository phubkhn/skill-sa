# Deployment Catalogue — <environment> — <scope>

<!-- Accompanies 03-hld/deployment-<environment>.puml. Standard 22. -->
<!-- Header block — copy from standards/01-workflow-protocol.md, phase P8 -->

**Environment:** <production | staging | …>
**Differs from production by:** <state it, or "n/a — this is production">

## 1. Nodes

| Node | Type | Hosts (containers) | Region / zone | Instances (min–max) | Scaling trigger | Failure domain | Owner |
|---|---|---|---|---|---|---|---|
| | cluster \| vm \| serverless \| managed service \| device | | | | | | |

<!-- Every container from the L2 view appears on exactly one node group.
     A container on no node is not deployed — that is a finding. -->

## 2. Network paths

| From | To | Protocol | Port class | Encryption | Crosses public network | Latency budget | Notes |
|---|---|---|---|---|---|---|---|
| | | | | | yes/no | | |

<!-- "Internal network" is not encryption. -->

## 3. Ingress and egress

| Direction | Path | Mechanism | Authentication | Notes |
|---|---|---|---|---|
| in | | load balancer \| gateway \| CDN | | |
| out | | NAT \| proxy \| partner link | | |

## 4. Boundaries

<!-- Network, trust and administrative boundaries are rarely the same lines. -->

| Boundary | Kind | Encloses | Crossing control |
|---|---|---|---|
| | network \| trust \| administrative | | |

## 5. Shared infrastructure

| Resource | Shared with | Coupling this creates | Contention risk |
|---|---|---|---|
| | | | |

## 6. Failure domains

| Domain | What is lost if it fails | Surviving capability | Recovery path |
|---|---|---|---|
| | | | |

<!-- Must agree with the zone/region loss rows in 08-crosscutting/resilience-design.md -->

## 7. Environment parity

| Aspect | Production | This environment | What the gap hides |
|---|---|---|---|
| | | | |
