# Specification Consistency Review

Audit date: 2026-09-22.

Scope: all 18 use cases, 16 API contracts, the common API contract, shared UML vocabulary, assumptions, source manifest and persistence model in this package. This is a local-document audit; no live Figma inspection was possible from the retained source identifiers.

## Corrections

| Finding | Correction | Main artifacts |
| --- | --- | --- |
| Login OCL and API used different public rejection codes. | Aligned the OCL outcome with INVALID_CREDENTIALS; completed accepted/rejected session effects. | UC-02, API-AUTH-LOGIN |
| Hash creation was treated as deterministic equality, and read-only rules compared only object membership. | Verify salted password hashes; use structural state comparison for read-only operations; distinguish transient tokens from persisted hashes. | UC-01, UC-02, shared model |
| Consumed or expired quotes made booking retries fail their own precondition. | Separate new-booking acceptance from identical replay; bind server-derived fingerprints and return the existing booking without new payment or allocation effects. | UC-08, UC-13 |
| Quote APIs lacked corresponding quote-operation rules, and booking guest data had no persistence postcondition. | Added quote ownership/version/terms/nonreservation rules and explicit persisted guest mappings. | UC-08, UC-13, shared model |
| Taxi allocation only counted bookings for one offer, allowing overlapping bookings through other offers. | Check overlapping intervals sharing either driver or vehicle; represent active resource claims and PostgreSQL exclusion constraints. | UC-13, schema.dbml, persistence-constraints.sql |
| PAY_DRIVER required a payment-reference object despite nullable persistence and no provider payment. | Use a null payment reference for PAY_DRIVER; constrain initial ONLINE states separately. | UC-13, shared model |
| Refinement always required offset zero, contradicting pagination; optional API filters were mandatory numeric comparisons in OCL. | Reset traversal only for changed refinements, guard absent filters, and specify snapshot ID/version, currency and exact page slices. | UC-05, UC-06, UC-10, UC-11, UC-15; search APIs |
| Snapshot pages used a moving clock and live provider observations without a stable continuation contract. | Bind page observations to captured time and a validity window; expose continuation metadata and conflict responses. | UC-05, UC-10, shared model, search APIs |
| Taxi vehicle filters were described but absent from the contract. | Added vehicleTypes transport and domain fields and conjunctive filtering. | UC-11, API-TAXI-SEARCH |
| Stay detail modeled a current offer without an API request/response field. | Added optional offerId and nullable currentOffer; scoped the review aggregate to the selected stay. | UC-07, API-STAY-DETAIL |
| Public taxi detail could not supply authenticated contact behavior and rejected an already booked offer. | Added optional authentication, display-field mapping and access through an owned confirmed booking. | UC-12, API-TAXI-OFFER-DETAIL |
| Round-trip search ignored return dates and mixed a destination stay with flight connections. | Split outbound/inbound journeys, bind both local dates and endpoints, and calculate connections/duration within each journey. | UC-14, API-FLIGHT-SEARCH, flight_segments |
| The quickest-flight sorting expression had an unmatched parenthesis. | Balanced the expression and checked all OCL delimiters. | UC-15 |
| Editorial price evidence could be future-dated or compared across currencies. | Require nonfuture recent evidence in the displayed currency; add supporting persistence. | UC-03, UC-16, UC-17 |
| Shared/local UML declared incompatible operation results and property types. | Centralized canonical members and signatures; retained local diagrams as views of that model. | All UC UML sections, shared-domain-model.md |
| Several OCL concepts were absent from persistence. | Added snapshot observations, quote/booking fingerprints, price evidence, moderation/booking links, publication fields, flight journey direction and active taxi allocations. | schema.dbml |
| Some response fields, public enum values and error outcomes were unspecified. | Added missing response projections, nested-field conventions, booking response variants and neutral 409/422 outcomes. | API contracts, common-contract.md |

## Business Rule Coverage

The package previously had 108 BR blocks. It now has 153, a net addition of 45. All 12 use cases that previously had fewer than seven rules now meet the requested minimum. Existing use cases with more than seven rules retain their necessary coverage.

| Use case | Before | After |
| --- | ---: | ---: |
| UC-01 | 7 | 8 |
| UC-02 | 4 | 7 |
| UC-03 | 5 | 8 |
| UC-04 | 6 | 7 |
| UC-05 | 5 | 7 |
| UC-06 | 6 | 8 |
| UC-07 | 6 | 7 |
| UC-08 | 7 | 15 |
| UC-09 | 7 | 9 |
| UC-10 | 5 | 7 |
| UC-11 | 6 | 8 |
| UC-12 | 5 | 7 |
| UC-13 | 8 | 15 |
| UC-14 | 7 | 9 |
| UC-15 | 6 | 8 |
| UC-16 | 6 | 7 |
| UC-17 | 5 | 7 |
| UC-18 | 7 | 9 |

## Policy Isolation

Triggers, preconditions, postconditions, Basic Flows, Alternative Flows and Exception Flows were reviewed separately from the OCL blocks. They contain observable interactions and outcomes without BR IDs, rule names or duplicated policy predicates. Booking recovery now describes a request retry supported by the existing API instead of referring to an unspecified status-recovery interaction. No standalone flight-detail or flight-booking use case was added.

New or corrected product-policy assumptions are inventoried in [ASSUMPTIONS.md](ASSUMPTIONS.md). The [shared model](uc/shared-domain-model.md) defines their domain vocabulary and primitive-helper semantics.

## Validation

- Package validator: 18 UC files, 16 sequential API files, 136 coded conditions/branch flows, 185 numbered activities and 153 uniquely identified OCL rules.
- [Additional static checker](scripts/validate_audit.py): minimum BR counts, sequential IDs, balanced OCL delimiters, qualified-name resolution, direct property paths, repeated rule bodies, policy references and local Markdown links.
- DBML compilation to PostgreSQL SQL.
- Repository validator: both specification packages passed; edits were confined to the Travel Booking package.
- PostgreSQL parser validation of the six statements in [persistence-constraints.sql](persistence-constraints.sql). This supplement is applied after DBML compilation; it was not executed against a database.

The checks do not constitute a complete OCL type check or a proof of every policy. Primitive helpers need implementation and product confirmation. Missing Figma URL, file key and node IDs remain recorded in [FIGMA.md](FIGMA.md) and [coverage-report.md](coverage-report.md); frame-level design traceability cannot be independently verified from the current package.

## Re-run

From the repository root:

```powershell
python '.\Travel Booking App Web & Mobile\scripts\validate_audit.py'
powershell -NoProfile -ExecutionPolicy Bypass -File '.\skills\figma-to-ocl-specs\scripts\validate_specs.ps1' -Root '.\Travel Booking App Web & Mobile'
powershell -NoProfile -ExecutionPolicy Bypass -File '.\skills\figma-to-ocl-specs\scripts\validate_repository.ps1' -Root '.'
```
