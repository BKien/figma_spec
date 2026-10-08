---
artifact_type: api-contract
status: Frozen
api_id: API-HOME-SUMMARY
related_uc_id: UC-03
---

# API-HOME-SUMMARY: Home Summary

## General Information

### API ID

API-HOME-SUMMARY

### API Name

Home Summary

### Related Use Case IDs

- UC-03

### Method

GET

### Path

/api/v1/home

### Description

Returns the content collections required to render the home page.

### Authentication

Optional bearer access token

### Authorization

Public

## Request Header(s)

### headers.Authorization

Type: string; Format: bearer token; Required: No; Nullable: No

Trigger: Optional authenticated navigation context.

Description: Carries an optional access token.

Example: Bearer eyJhbGciOiJIUzI1NiIs...

Note: Uses the HTTP Bearer authentication scheme.

Validation: When supplied, must use the Bearer <access-token> syntax.

## Path Parameter(s)

None.

## Query Parameter(s)

None.

## Request Body

None.

## Success Response — HTTP 200

### success

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Indicates whether the HTTP operation completed successfully.

Example: true

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Human-readable operation outcome summary.

Example: Home summary retrieved.

### data.services

Type: string array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Service labels presented by the home page.

Example: ["Stays", "Taxis", "Flights"]

### data.destinations[]

Type: object array; Required: Yes; Nullable: No
- Fields: id (string), title (string), imageUrl (URI string), startingPrice (money object).

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Destination cards displayed on the home page.

Example: [{"id": "destination_01JABCDEF", "title": "A weekend in Kyoto", "imageUrl": "https://example.com/images/travel.jpg", "startingPrice": {"amount": 300.0, "currency": "USD"}}]

### data.reviews[]

Type: object array; Required: Yes; Nullable: No
- Fields: id (string), authorName (string), rating (integer), comment (string).

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Review cards displayed on the home page.

Example: [{"id": "booking_01JABCDEF", "authorName": "A***", "rating": 5, "comment": "A comfortable stay."}]

### data.viewer

Type: object; Required: Yes; Nullable: No
- Fields: authenticated (boolean), displayName (nullable string).

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Navigation display context.

Example: {"authenticated": true, "displayName": "Alex Morgan"}

### data.sectionStates

Type: object; Required: Yes; Nullable: No
- Fields: destinations (string), reviews (string).
- Allowed values for each field: READY, EMPTY, UNAVAILABLE.

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Content-section outcomes.

Example: {"destinations": "READY", "reviews": "READY"}

### data.upcomingTrip

Type: object; Required: Yes; Nullable: Yes
- Fields: bookingId (string), destinationName (string), stayName (string), tripDate (ISO 8601 date string), daysRemaining (integer).

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Upcoming-trip notification card for an authenticated traveller; null when no card is returned.

Example: {"bookingId": "booking_example_01", "destinationName": "Kyoto", "stayName": "Example Riverside Hotel", "tripDate": "2026-10-10", "daysRemaining": 3}

## Error Response — HTTP 401

- Code: UNAUTHORIZED
Trigger: The endpoint does not accept the supplied authentication context.
Description: Public authentication failure.
- Example message: The request could not be completed.

## Error Response — HTTP 500

- Code: INTERNAL_ERROR
Trigger: An unexpected server error prevents the response from being produced.
Description: Unexpected home-content failure.
- Example message: Internal Server Error

## Error Response — HTTP 503

- Code: SERVICE_UNAVAILABLE
Trigger: The endpoint is temporarily unable to return the home summary.
Description: Temporary service failure.
- Example message: The service is temporarily unavailable.

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md).

The optional token does not change the wire shape of the response.
