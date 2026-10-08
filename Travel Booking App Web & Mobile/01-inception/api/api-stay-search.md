---
artifact_type: api-contract
status: Frozen
api_id: API-STAY-SEARCH
related_uc_ids: ["UC-04", "UC-05", "UC-06"]
---

# API-STAY-SEARCH: Stay Search

## General Information

### API ID

API-STAY-SEARCH

### API Name

Stay Search

### Related Use Case IDs

- UC-04
- UC-05
- UC-06

### Method

GET

### Path

/api/v1/stays/search

### Description

Returns a paginated collection of stay offers for submitted search criteria.

### Authentication

Public

### Authorization

None

## Request Header(s)

None.

## Path Parameter(s)

None.

## Query Parameter(s)

### query.destinationId

Type: string; Required: Yes; Nullable: No

Trigger: Every request includes the destinationId query parameter.

Description: Opaque destination identifier.

Example: loc_paris

Validation: Must be encoded as a query-string value.

### query.checkIn

Type: string; Format: date (YYYY-MM-DD); Required: Yes; Nullable: No

Trigger: Every request includes the checkIn query parameter.

Description: Requested check-in date.

Example: 2026-10-10

Validation: Must use the declared date syntax.

### query.checkOut

Type: string; Format: date (YYYY-MM-DD); Required: Yes; Nullable: No

Trigger: Every request includes the checkOut query parameter.

Description: Requested check-out date.

Example: 2026-10-14

Validation: Must use the declared date syntax.

### query.rooms

Type: integer; Required: Yes; Nullable: No

Trigger: Every request includes the rooms query parameter.

Description: Requested room count.

Example: 1

Validation: Must use integer syntax.

### query.adults

Type: integer; Required: Yes; Nullable: No

Trigger: Every request includes the adults query parameter.

Description: Requested adult guest count.

Example: 2

Validation: Must use integer syntax.

### query.minPrice

Type: number; Required: No; Nullable: No

Trigger: When the client supplies the minPrice query parameter.

Description: Client-supplied lower price filter.

Example: 50.00

Validation: Must use JSON-compatible decimal syntax when supplied.

### query.maxPrice

Type: number; Required: No; Nullable: No

Trigger: When the client supplies the maxPrice query parameter.

Description: Client-supplied upper price filter.

Example: 250.00

Validation: Must use JSON-compatible decimal syntax when supplied.

### query.minRating

Type: number; Required: No; Nullable: No

Trigger: When the client supplies the minRating query parameter.

Description: Client-supplied rating filter.

Example: 4.0

Validation: Must use JSON-compatible decimal syntax when supplied.

### query.sort

Type: string; Format: enum; Required: No; Nullable: No

Trigger: When the client supplies the sort query parameter.

Description: Requested result ordering.

Example: RECOMMENDED

Default: RECOMMENDED

Allowed values: RECOMMENDED, PRICE, RATING

Validation: Must match one public enum value when supplied.

### query.limit

Type: integer; Required: No; Nullable: No

Trigger: When the client supplies the limit query parameter.

Description: Requested page size.

Example: 20

Default: 20

Validation: Must use integer syntax when supplied.

### query.offset

Type: integer; Required: No; Nullable: No

Trigger: When the client supplies the offset query parameter.

Description: Requested starting position.

Example: 0

Default: 0

Validation: Must use integer syntax when supplied.

### query.searchContextId

Type: string; Required: No; Nullable: No

Trigger: When the client supplies the searchContextId query parameter.

Description: Opaque search-context reference.

Example: "search-context-example-01"

Validation: Must be encoded as a query-string value.

### query.snapshotVersion

Type: integer; Required: No; Nullable: No

Trigger: When the client supplies the snapshotVersion query parameter.

Description: Search snapshot version.

Example: 1

Validation: Must use integer syntax when supplied.

### query.currency

Type: string; Format: ISO 4217 currency code; Required: No; Nullable: No

Trigger: When the client supplies the currency query parameter.

Description: Currency code for monetary fields.

Example: "USD"

Default: USD

Validation: Must use three uppercase ASCII letters.

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

Example: Stay offers retrieved.

### data.items[]

Type: object array; Required: Yes; Nullable: No
- Fields: offerId (string), stayId (string), stayName (string), rating (number), availableRooms (integer), total (money object).

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Stay offers in the current page.

Example: [{"offerId": "offer_01JABCDEF", "stayId": "stay_example_01", "stayName": "Example Riverside Hotel", "rating": 5, "availableRooms": 4, "total": {"amount": 300.0, "currency": "USD"}}]

### data.total

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Reported collection size.

Example: 1

### data.limit

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Applied page size.

Example: 20

### data.offset

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Applied starting position.

Example: 0

### data.hasMore

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Indicates whether another page can be requested.

Example: false

### data.searchContextId

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Search-context identifier.

Example: "search-context-example-01"

### data.snapshotVersion

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Search snapshot version.

Example: 1

### data.validUntil

Type: string; Format: ISO 8601 date-time; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Snapshot timestamp.

Example: "2026-10-10T20:30:00Z"

## Error Response — HTTP 400

- Code: VALIDATION_ERROR
Trigger: A query parameter cannot be decoded or does not match the declared wire type.
Description: Protocol-level query error.
- Example message: The query parameters are invalid.

## Error Response — HTTP 409

- Code: SEARCH_CONTEXT_CONFLICT
Trigger: The request conflicts with the current search context.
Description: Public search-context conflict.
- Example message: The request could not be completed.

## Error Response — HTTP 422

- Code: UNPROCESSABLE_REQUEST
Trigger: The syntactically valid request cannot be completed.
Description: Public processing failure.
- Example message: The request could not be completed.

## Error Response — HTTP 502

- Code: UPSTREAM_ERROR
Trigger: An upstream dependency returns an unusable result.
Description: Upstream search failure.
- Example message: An upstream service returned an invalid response.

## Error Response — HTTP 503

- Code: SERVICE_UNAVAILABLE
Trigger: The endpoint is temporarily unable to return search results.
Description: Temporary service failure.
- Example message: The service is temporarily unavailable.

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md).

All identifiers are opaque client values. Cross-field evaluation is outside this wire contract.
