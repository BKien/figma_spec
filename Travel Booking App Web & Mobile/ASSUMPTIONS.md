# Assumptions Requiring Product Confirmation

This audit uses the retained local UI evidence. There is no live Figma URL, file key or node inventory in the package. The working policies below are assumptions, not confirmed product requirements. They remain explicit so product decisions can replace them without copying policy into triggers, conditions or interaction flows.

## Use-case policy inventory

| Use case | Working assumptions | Rule scope |
| --- | --- | --- |
| [UC-01](uc/uc-01-register-an-account.md) | Canonical identity, credential policy, confirmation, one newly created user, salted password verification, a transient session token with a persisted hash, and usable name/email. | BR-UC-01-01 through BR-UC-01-08 |
| [UC-02](uc/uc-02-log-in.md) | One active credential match, a uniform INVALID_CREDENTIALS outcome, a fresh accepted session, no session on rejection, immutable identities, and token hashing. | BR-UC-02-01 through BR-UC-02-07 |
| [UC-03](uc/uc-03-view-the-home-page.md) | Published editorial destinations, moderated reviews, stable tie-breaks, supported service entries, read-only content, privacy-safe review projections, same-currency price evidence, and an authenticated upcoming-trip projection. | BR-UC-03-01 through BR-UC-03-09 |
| [UC-04](uc/uc-04-search-for-stays.md) | A searchable destination; 1–30 nights in its local calendar; 1–8 rooms and 1–4 adults per room; matching, deduplicated inventory; no reservation during search; one comparison currency. | BR-UC-04-01 through BR-UC-04-07 |
| [UC-05](uc/uc-05-view-stay-results.md) | Exact slices of an immutable stay-search observation, coherent pagination, snapshot-time liveness, distinct IDs, stable order and currency consistency. | BR-UC-05-01 through BR-UC-05-07 |
| [UC-06](uc/uc-06-filter-and-sort-stay-results.md) | Conjunctive optional stay filters, coherent numeric bounds, stable sorting, a fresh traversal when refinements change, and ID/version-bound continuation. | BR-UC-06-01 through BR-UC-06-08 |
| [UC-07](uc/uc-07-view-stay-details.md) | An active selected stay, canonical amenities, gap-free media order, approved reviews scoped to that stay, an optional selected live offer, and no persisted changes during retrieval. | BR-UC-07-01 through BR-UC-07-07 |
| [UC-08](uc/uc-08-book-a-stay.md) | An authenticated quote owner, server-derived request fingerprint, replay safety, quoted commercial terms, atomic consumption, payment authorization, provider reservation, Figma checkout fields, tokenized card handling and optional saved-provider reference. | BR-UC-08-01 through BR-UC-08-16 |
| [UC-09](uc/uc-09-search-for-taxis.md) | An active rental location, pick-up 2–4320 hours ahead, a party of 1–16, positive rental duration, live free resources, deduplication and one comparison currency. | BR-UC-09-01 through BR-UC-09-09 |
| [UC-10](uc/uc-10-view-taxi-results.md) | Exact slices of an immutable Taxi rental search observation, coherent pagination, snapshot liveness, distinct IDs, stable order and coherent card facts. | BR-UC-10-01 through BR-UC-10-07 |
| [UC-11](uc/uc-11-filter-and-sort-taxi-results.md) | Conjunctive car-category, deposit, electric-type and optional price filters; stable top-picks ordering, coherent bounds and snapshot continuation. | BR-UC-11-01 through BR-UC-11-09 |
| [UC-12](uc/uc-12-view-taxi-and-driver-details.md) | A live offer or owned booking, correct assigned resources, Figma-visible driver phone and registration, read-only retrieval, one rental location, positive period and coherent commercial facts. | BR-UC-12-01 through BR-UC-12-07 |
| [UC-13](uc/uc-13-book-a-taxi.md) | Quote ownership, payment mode, fingerprinting, replay safety, overlap exclusion, quoted terms, Figma checkout fields, optional saved-provider reference and quote nonallocation. PAY_DRIVER has no payment-reference row. | BR-UC-13-01 through BR-UC-13-15 |
| [UC-14](uc/uc-14-search-for-flights.md) | Active air-travel endpoints, distinct route endpoints, positive party size, origin-local travel dates, separate outbound/inbound journeys, transfer windows of 45–1440 minutes within each journey, live party-sized offers, deduplication and total travel duration excluding the stay at the destination. | BR-UC-14-01 through BR-UC-14-09 |
| [UC-15](uc/uc-15-view-filter-and-sort-flight-results.md) | Conjunctive optional flight filters, unique commercial results, deterministic sort tie-breaks, coherent numeric/pagination bounds and ID/version-bound continuation. | BR-UC-15-01 through BR-UC-15-08 |
| [UC-16](uc/uc-16-browse-budget-trips.md) | Published editorial trips, one card per destination, same-currency nonfuture price evidence no older than 24 hours, deterministic editorial ordering, coherent pagination and read-only retrieval. | BR-UC-16-01 through BR-UC-16-07 |
| [UC-17](uc/uc-17-view-budget-trip-details.md) | A published selected trip, destination-scoped published attractions, stable attraction order, same-currency recent price evidence, readable content and distinct ordered media. | BR-UC-17-01 through BR-UC-17-07 |
| [UC-18](uc/uc-18-view-traveller-reviews.md) | Approved published reviews, verified badges backed by completed travel, public author/content projections, deterministic recent ordering, coherent pagination, read-only retrieval and integer ratings from 1 to 5. | BR-UC-18-01 through BR-UC-18-09 |

UC-01 confirmation equality retains its original Figma provenance. All other policy predicates use Assumption provenance. The retained frame names establish interaction scope, not hidden validation or persistence behavior.

## Cross-contract decisions

- Search currency defaults to USD for stays and flights and LKR for Taxi rentals; sort defaults to RECOMMENDED for stays, TOP_PICKS for Taxi rentals and BEST for flights. Omitted scalar filters have no bound and omitted list filters are empty. Snapshots expire no later than any included offer observation. Search IDs and versions are supplied together.
- An expired, consumed or subsequently changed quote does not block an identical replay of an existing booking. A reused operation key with a different fingerprint is rejected. No replay creates an additional booking, reservation, allocation or authorization.
- Quote issuance revalidates the current provider offer and captures its version/terms. It does not reserve inventory or charge payment. New stay bookings require a provider reservation reference. Provider reservation/authorization actions use an idempotent provider key and reconciliation after uncertain outcomes.
- Taxi rental allocations use half-open intervals. Adjacent rental periods can share a resource; overlapping active rentals cannot. Resource claims must be created and released in the same database transaction as booking changes. The supplemental PostgreSQL exclusion constraints represent concurrency enforcement.
- Opaque API IDs encode database UUIDs. Public response objects are projections, not serialized persistence entities. Optional internal domain values map absent wire fields to null. Raw session/payment credentials never enter persistent rows or read-state snapshots.
- Editorial and review pagination uses a live collection at request time; it does not promise a retained snapshot across requests. Travel-offer result pages use explicit snapshots.
- Errors after valid wire decoding use public 409/422 outcomes as declared by the endpoint; API error triggers do not reproduce the underlying policy. A processor rejection creates no booking. Provider lifecycle transitions outside the represented UI scope are not additional use cases.

## Evidence limitation

The Figma-source limitation is tracked in [FIGMA.md](FIGMA.md) and [coverage-report.md](coverage-report.md). No missing flight detail or flight checkout screens have been added to the supported scope.
