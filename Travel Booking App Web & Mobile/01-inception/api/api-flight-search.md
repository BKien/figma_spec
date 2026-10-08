---
artifact_type: api-contract
status: Frozen
api_id: API-FLIGHT-SEARCH
related_uc_ids: ["UC-14", "UC-15"]
---

# API-FLIGHT-SEARCH: Flight Search

## General Information

### API ID

API-FLIGHT-SEARCH

### API Name

Flight Search

### Related Use Case IDs

- UC-14
- UC-15

### Method

GET

### Path

/api/v1/flights/search

### Description

Returns a paginated collection of flight offers for submitted search criteria.

### Authentication

Public

### Authorization

None

## Request Header(s)

None.

## Path Parameter(s)

None.

## Query Parameter(s)

### query.originId

Type: string; Required: Yes; Nullable: No

Trigger: Every request includes the originId query parameter.

Description: Opaque origin identifier.

Example: airport_sgn

Validation: Must be encoded as a query-string value.

### query.destinationId

Type: string; Required: Yes; Nullable: No

Trigger: Every request includes the destinationId query parameter.

Description: Opaque destination identifier.

Example: airport_hnd

Validation: Must be encoded as a query-string value.

### query.departOn

Type: string; Format: date (YYYY-MM-DD); Required: Yes; Nullable: No

Trigger: Every request includes the departOn query parameter.

Description: Requested departure date.

Example: 2026-10-10

Validation: Must use the declared date syntax.

### query.returnOn

Type: string; Format: date (YYYY-MM-DD); Required: No; Nullable: No

Trigger: When the client supplies the returnOn query parameter.

Description: Requested return date.

Example: 2026-10-17

Validation: Must use the declared date syntax when supplied.

### query.passengers

Type: integer; Required: Yes; Nullable: No

Trigger: Every request includes the passengers query parameter.

Description: Requested passenger count.

Example: 1

Validation: Must use integer syntax.

### query.minPrice

Type: number; Required: No; Nullable: No

Trigger: When the client supplies the minPrice query parameter.

Description: Client-supplied lower price filter.

Example: 100.00

Validation: Must use JSON-compatible decimal syntax when supplied.

### query.maxPrice

Type: number; Required: No; Nullable: No

Trigger: When the client supplies the maxPrice query parameter.

Description: Client-supplied upper price filter.

Example: 1000.00

Validation: Must use JSON-compatible decimal syntax when supplied.

### query.maxDurationMinutes

Type: integer; Required: No; Nullable: No

Trigger: When the client supplies the maxDurationMinutes query parameter.

Description: Client-supplied duration filter in minutes.

Example: 720

Validation: Must use integer syntax when supplied.

### query.providerIds

Type: string array
- Serialization: repeated query parameter; Required: No; Nullable: No

Trigger: When the client supplies the providerIds query parameter.

Description: Client-supplied provider filters.

Example: providerIds=provider_a&providerIds=provider_b

Validation: Every supplied value must use query-string syntax.

### query.sort

Type: string; Format: enum; Required: No; Nullable: No

Trigger: When the client supplies the sort query parameter.

Description: Requested result ordering.

Example: BEST

Default: BEST

Allowed values: CHEAPEST, BEST, QUICKEST

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

Example: Flight offers retrieved.

### data.items[]

Type: object array; Required: Yes; Nullable: No
- Fields: offerId (string), providerId (string), outboundSegments (object array), inboundSegments (object array), durationMinutes (integer), total (money object), expiresAt (ISO 8601 date-time string).
- Segment fields (both arrays): originCode (string), destinationCode (string), departureAt (ISO 8601 date-time string), arrivalAt (ISO 8601 date-time string), carrierCode (string).

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Flight offers in the current page.

Example: [{"offerId": "offer_01JABCDEF", "providerId": "provider_a", "outboundSegments": [{"originCode": "SGN", "destinationCode": "HND", "departureAt": "2026-10-10T09:00:00Z", "arrivalAt": "2026-10-10T14:30:00Z", "carrierCode": "EX"}], "inboundSegments": [{"originCode": "HND", "destinationCode": "SGN", "departureAt": "2026-10-17T09:00:00Z", "arrivalAt": "2026-10-17T14:30:00Z", "carrierCode": "EX"}], "durationMinutes": 660, "total": {"amount": 300.0, "currency": "USD"}, "expiresAt": "2026-10-10T20:30:00Z"}]

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

### data.partial

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Indicates a partial search response.

Example: false

### data.providerErrors[]

Type: object array; Required: Yes; Nullable: No
- Fields: providerId (string), code (string).

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Provider-level public outcomes.

Example: [{"providerId": "provider_a", "code": "UPSTREAM_UNAVAILABLE"}]

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

## Error Response — HTTP 429

- Code: RATE_LIMITED
Trigger: The service temporarily rejects additional requests from the client.
Description: Public request-throttling response.
- Example message: Too many requests.

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

The current scope does not define flight-offer detail or booking endpoints. Cross-field evaluation and result-ranking logic are outside this wire contract.
