# High-level Design

Create the fewest views needed for a shared understanding of the system boundary, responsibilities, relationships, and deployment.

## View selection

- Context: people, system boundary, and external systems.
- Container: deployable or independently operated responsibilities. Default view.
- Component: only when one container's internals are architecture-significant.
- Deployment: only when region, network, scaling, tenancy, or failure domains matter.

## Required content

Every element has a stable name, one clear responsibility, and an owner. Every relationship has direction, purpose, protocol or mechanism, sync/async nature, and relevant failure behaviour. Show relevant trust boundaries and owned data.

Check cycles, excessive fan-out, chattiness, shared-store coupling, god components, orphans, and elements with no driver. A diagram must agree with accepted ADRs.

## Checklist

- [ ] Scope and audience are clear
- [ ] Every element has responsibility and owner
- [ ] Every relationship is labelled and directional
- [ ] External systems and trust boundaries are shown where relevant
- [ ] Data ownership is not ambiguous
- [ ] Coupling concerns were checked
- [ ] Diagram agrees with accepted decisions
- [ ] No unnecessary view or element was added
