# Use Case Specifications

This directory contains the English-language specifications for the 18 use cases supported by the retained UI evidence.

## Catalogue

Each use case is stored in its own Markdown file and follows the naming convention `uc-<sequence>-<slug>.md`.

| Use Case | File |
| --- | --- |
| UC-01 | [Register an Account](uc-01-register-an-account.md) |
| UC-02 | [Log In](uc-02-log-in.md) |
| UC-03 | [View the Home Page](uc-03-view-the-home-page.md) |
| UC-04 | [Search for Stays](uc-04-search-for-stays.md) |
| UC-05 | [View Stay Results](uc-05-view-stay-results.md) |
| UC-06 | [Filter and Sort Stay Results](uc-06-filter-and-sort-stay-results.md) |
| UC-07 | [View Stay Details](uc-07-view-stay-details.md) |
| UC-08 | [Book a Stay](uc-08-book-a-stay.md) |
| UC-09 | [Search for Taxis](uc-09-search-for-taxis.md) |
| UC-10 | [View Taxi Results](uc-10-view-taxi-results.md) |
| UC-11 | [Filter and Sort Taxi Results](uc-11-filter-and-sort-taxi-results.md) |
| UC-12 | [View Taxi and Driver Details](uc-12-view-taxi-and-driver-details.md) |
| UC-13 | [Book a Taxi](uc-13-book-a-taxi.md) |
| UC-14 | [Search for Flights](uc-14-search-for-flights.md) |
| UC-15 | [View, Filter, and Sort Flight Results](uc-15-view-filter-and-sort-flight-results.md) |
| UC-16 | [Browse Budget Trips](uc-16-browse-budget-trips.md) |
| UC-17 | [View Budget Trip Details](uc-17-view-budget-trip-details.md) |
| UC-18 | [View Traveller Reviews](uc-18-view-traveller-reviews.md) |
| Shared | [Shared Domain Model](shared-domain-model.md) |

## Conventions

- All content is written in English.
- Every use case contains at least seven distinct Business Rules.
- Every Business Rule is an independent OCL block with an identifier such as `BR-UC-04-01`.
- The UML model defines the classifiers, attributes, associations, enumerations, and operations referenced by the OCL constraints.
- Trigger and condition items use the namespaces `TRG`, `PRE`, and `POST`, followed by the use-case number and a two-digit local sequence.
- Each use case has exactly one Basic Flow. Its activities are an ordered list starting at `1` and carry no individual identifiers.
- Each Alternative Flow and Exception Flow has its own `AF-UC-NN-XX` or `EF-UC-NN-XX` heading. The activities under each flow are an ordered list starting at `1`.
- Each flow is specific to the actor goal and describes only observable actor, client, and system interactions.
- Preconditions, postconditions, and flows are policy-neutral, self-contained, and free of rule citations or internal decision rationale.
- Business Rules express domain policy, cross-record consistency, privacy, concurrency, idempotency, deterministic ordering, and state effects. Elementary field-shape validation belongs in the related API contract.
- A rule marked `Source: Assumption` is listed in [`../ASSUMPTIONS.md`](../ASSUMPTIONS.md) when it introduces a product decision not established by the retained UI evidence.
- API references resolve to the contracts in `../api`.
- Persistence concepts resolve to [`../schema.dbml`](../schema.dbml), and canonical terminology resolves to [`../CONTEXT.md`](../CONTEXT.md).

Audit results and validation limits are recorded in [the consistency report](../consistency-review.md).
