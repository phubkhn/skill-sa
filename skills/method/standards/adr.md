# Architecture Decisions

Use an ADR for one consequential, contested, cross-cutting, or expensive-to-reverse choice. Do not use ADRs for routine implementation details.

## Required content

- decision question and status
- context, constraints, and measurable deciding drivers
- at least two credible options, presented fairly
- one-sentence decision
- positive and negative consequences
- reversibility and reconsideration trigger
- compliance check

Include keeping the current design when credible. A vendor or new technology decision must state operational burden and exit path. Split independent choices so they can be superseded separately.

Use `Proposed` until authorised deciders agree. When superseding, link both ADRs and preserve the old record.

## Checklist

- [ ] One decision only
- [ ] At least two credible options
- [ ] Drivers and constraints make the comparison understandable
- [ ] Decision is explicit
- [ ] Negative consequences are stated
- [ ] Reversibility and reconsideration trigger are stated
- [ ] Compliance is checkable
- [ ] Status reflects actual agreement
