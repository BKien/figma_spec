# Figma Alignment and Consistency Review

## Scope

The package was re-audited on 2026-09-24 against the supplied Figma Community resource and the creator-linked public prototype video. The review covered all 18 use cases, 16 API contracts, shared UML vocabulary, OCL rules, DBML persistence, source traceability, and cross-file references.

Direct canvas enumeration was unavailable because Figma required authentication. The source manifest records the public resource, the desktop and mobile prototype keys visible in the video, and the node IDs available from prototype URLs.

## Corrected Figma Mismatches

| Finding | Correction | Affected artifacts |
| --- | --- | --- |
| Taxi search was modeled as a point-to-point transfer with separate pickup and destination locations. | Modeled the observed Taxi experience as a vehicle-and-driver rental at one location between pick-up and drop-off times. | UC-09–UC-13, Taxi APIs, shared model, DBML |
| Taxi result filtering used price, distance, and generic vehicle types. | Added the displayed car categories, pick-up-deposit bands, Fully Electric/Hybrid filters, and the observed `Our top picks` ordering. Unobserved sort values were omitted. | UC-11, API-TAXI-SEARCH |
| Result cards lacked several visible vehicle facts. | Added vehicle name, category, transmission, electric type, seat and bag capacities, distance from centre, mileage allowance, deposit, rating, and rental price. | UC-10–UC-12, Taxi APIs, shared model, DBML |
| Driver details and vehicle registration were treated as masked or available only after a confirmed booking. | Matched the mobile prototype, which displays the assigned driver's name, phone and registration details before confirmation. | UC-12, API-TAXI-OFFER-DETAIL |
| Checkout omitted visible contact and trip-purpose controls. | Added home address, booking-for selection, work-travel selection, and save-card choice to stay and Taxi checkout contracts and persistence. | UC-08, UC-13, booking APIs, shared model, DBML |
| Card fields could be interpreted as raw server input. | Defined them as a payment-provider control; APIs accept only opaque payment tokens and persistence stores provider references rather than card number, expiry or CVV. | Booking APIs, shared model, DBML |
| The home specification omitted the visible `Your Next Trip` notification. | Added an optional upcoming-trip projection to the home use case and API. | UC-03, API-HOME-SUMMARY, shared model |
| The source manifest did not retain the supplied Figma identity. | Recorded the Community URL, resource ID, prototype keys, audit date, evidence boundary, and five observed prototype node IDs. | FIGMA.md |

## Coverage Decisions

- UC-01 through UC-07 and UC-09 through UC-18 have sufficient public prototype evidence for their stated interaction boundaries.
- UC-08 remains `Partial`: the checkout, payment controls and `Book now` action are visible, but the post-submit presentation is not demonstrated. Its contract keeps the returned presentation generic and records the gap.
- Flight-offer detail and flight booking remain outside supported scope.
- Saved items, bookings/itinerary management, Help Centre, and budget-trip share/translation remain candidates because only entry points or actions are visible; no complete outcome is demonstrated.
- Notification is represented inside UC-03 because it is a home-page state rather than a separate actor goal.

## Business Rule Coverage

The package contains 156 OCL Business Rules. Every use case contains at least seven independent BR blocks. Trigger, precondition, postcondition, Basic Flow, Alternative Flow and Exception Flow sections contain no BR identifiers or duplicated policy predicates.

| Use case | BR count |
| --- | ---: |
| UC-01 | 8 |
| UC-02 | 7 |
| UC-03 | 9 |
| UC-04 | 7 |
| UC-05 | 7 |
| UC-06 | 8 |
| UC-07 | 7 |
| UC-08 | 16 |
| UC-09 | 9 |
| UC-10 | 7 |
| UC-11 | 9 |
| UC-12 | 7 |
| UC-13 | 15 |
| UC-14 | 9 |
| UC-15 | 8 |
| UC-16 | 7 |
| UC-17 | 7 |
| UC-18 | 9 |

## Validation

- Package structure and traceability validator: 18 UC files, 16 sequential API files, 139 coded conditions and branch flows, 189 numbered flow activities, and 156 unique OCL rules.
- Additional audit checker: rule count and sequencing, OCL delimiter balance, qualified-name and direct-property resolution, duplicate rule bodies, policy isolation, fences, and local links passed.
- `schema.dbml` compiled successfully to PostgreSQL SQL with `@dbml/cli`.
- `git diff --check` passed.

The static checks are not a complete OCL theorem proof. Hidden provider behavior, timeout values, credential policies, concurrency behavior and other nonvisual product decisions remain explicitly marked as assumptions.

## Re-run

From the repository root:

```powershell
python '.\Travel Booking App Web & Mobile\scripts\validate_audit.py'
pwsh -NoProfile -File 'C:\Users\User\.codex\skills\figma-to-ocl-specs\scripts\validate_specs.ps1' -Root '.\Travel Booking App Web & Mobile' -SkipDbmlCompile
npx --yes --package @dbml/cli dbml2sql '.\Travel Booking App Web & Mobile\schema.dbml' --postgres -o "$env:TEMP\travel-booking-schema.sql"
```
