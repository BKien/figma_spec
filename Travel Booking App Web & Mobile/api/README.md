# API Contract Specifications

This directory contains the English API contracts related to the 18 documented use cases. Evidence strength and unresolved visual gaps are recorded in [`../coverage-report.md`](../coverage-report.md).

Each endpoint contract uses a sequential layout. A label is followed by its value or field definitions; endpoint files do not use property tables, UML, OCL, or domain-policy definitions.

## Catalogue

- [API-AUTH-REGISTER — Register an Account](api-auth-register.md)
- [API-AUTH-LOGIN — Log In](api-auth-login.md)
- [API-HOME-SUMMARY — Get Home Summary](api-home-summary.md)
- [API-LOCATION-SUGGEST — Suggest Locations](api-location-suggest.md)
- [API-STAY-SEARCH — Search Stays](api-stay-search.md)
- [API-STAY-DETAIL — Get Stay Details](api-stay-detail.md)
- [API-STAY-QUOTE — Quote a Stay Booking](api-stay-quote.md)
- [API-STAY-BOOKING-CREATE — Create a Stay Booking](api-stay-booking-create.md)
- [API-TAXI-SEARCH — Search Taxi Rentals](api-taxi-search.md)
- [API-TAXI-OFFER-DETAIL — Get Taxi Rental Offer Details](api-taxi-offer-detail.md)
- [API-TAXI-QUOTE — Quote a Taxi Rental](api-taxi-quote.md)
- [API-TAXI-BOOKING-CREATE — Create a Taxi Rental Booking](api-taxi-booking-create.md)
- [API-FLIGHT-SEARCH — Search Flights](api-flight-search.md)
- [API-BUDGET-TRIP-LIST — List Budget Trips](api-budget-trip-list.md)
- [API-BUDGET-TRIP-DETAIL — Get Budget Trip Details](api-budget-trip-detail.md)
- [API-REVIEW-LIST — List Reviews](api-review-list.md)
- [Common API Contract](common-contract.md)

The persistence model is defined in [`../schema.dbml`](../schema.dbml). Canonical domain vocabulary is defined in [`../CONTEXT.md`](../CONTEXT.md).
