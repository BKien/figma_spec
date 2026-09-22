# API-FLIGHT-SEARCH — Search Flights

## API ID

`API-FLIGHT-SEARCH`

## API Name

Flight Search

## Related Use Case IDs

- `UC-14`
- `UC-15`

## Method

`GET`

## Path

`/api/v1/flights/search`

## Description

Returns a paginated collection of flight offers for submitted search criteria.

## Authentication

Public

## Authorization

None

## Request Headers

None.

## Path Parameters

None.

## Query Parameters

### `originId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a query-string value.
- Description: Opaque origin identifier.
- Example: `airport_sgn`

### `destinationId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a query-string value.
- Description: Opaque destination identifier.
- Example: `airport_hnd`

### `departOn`

- Type: string
- Format: date (`YYYY-MM-DD`)
- Required: Yes
- Nullable: No
- Validation: Must use the declared date syntax.
- Description: Requested departure date.
- Example: `2026-10-10`

### `returnOn`

- Type: string
- Format: date (`YYYY-MM-DD`)
- Required: No
- Nullable: No
- Validation: Must use the declared date syntax when supplied.
- Description: Requested return date.
- Example: `2026-10-17`

### `passengers`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must use integer syntax.
- Description: Requested passenger count.
- Example: `1`

### `minPrice`

- Type: number
- Required: No
- Nullable: No
- Validation: Must use JSON-compatible decimal syntax when supplied.
- Description: Client-supplied lower price filter.
- Example: `100.00`

### `maxPrice`

- Type: number
- Required: No
- Nullable: No
- Validation: Must use JSON-compatible decimal syntax when supplied.
- Description: Client-supplied upper price filter.
- Example: `1000.00`

### `maxDurationMinutes`

- Type: integer
- Required: No
- Nullable: No
- Validation: Must use integer syntax when supplied.
- Description: Client-supplied duration filter in minutes.
- Example: `720`

### `providerIds`

- Type: string array
- Serialization: repeated query parameter
- Required: No
- Nullable: No
- Validation: Every supplied value must use query-string syntax.
- Description: Client-supplied provider filters.
- Example: `providerIds=provider_a&providerIds=provider_b`

### `sort`

- Type: string
- Format: enum
- Required: No
- Default: `BEST`
- Nullable: No
- Allowed values: `CHEAPEST`, `BEST`, `QUICKEST`
- Validation: Must match one public enum value when supplied.
- Description: Requested result ordering.
- Example: `BEST`

### `limit`

- Type: integer
- Required: No
- Nullable: No
- Default: `20`
- Validation: Must use integer syntax when supplied.
- Description: Requested page size.
- Example: `20`

### `offset`

- Type: integer
- Required: No
- Nullable: No
- Default: `0`
- Validation: Must use integer syntax when supplied.
- Description: Requested starting position.
- Example: `0`

### `searchContextId`

- Type: string
- Required: No
- Nullable: No
- Validation: Must be encoded as a query-string value.
- Description: Opaque search-context reference.

### `snapshotVersion`

- Type: integer
- Required: No
- Nullable: No
- Validation: Must use integer syntax when supplied.
- Description: Search snapshot version.

### `currency`

- Type: string
- Required: No
- Nullable: No
- Format: ISO 4217 currency code
- Default: `USD`
- Validation: Must use three uppercase ASCII letters.
- Description: Currency code for monetary fields.

## Request Body

None.

## Success Response — HTTP 200

### `success`

- Type: boolean
- Required: Yes
- Nullable: No
- Example: `true`

### `message`

- Type: string
- Required: Yes
- Nullable: No
- Example: `Flight offers retrieved.`

### `data.items[]`

- Type: object array
- Required: Yes
- Nullable: No
- Fields: `offerId` (string), `providerId` (string), `outboundSegments` (object array), `inboundSegments` (object array), `durationMinutes` (integer), `total` (money object), `expiresAt` (ISO 8601 date-time string).
- Segment fields (both arrays): `originCode` (string), `destinationCode` (string), `departureAt` (ISO 8601 date-time string), `arrivalAt` (ISO 8601 date-time string), `carrierCode` (string).
- Description: Flight offers in the current page.

### `data.total`

- Type: integer
- Required: Yes
- Nullable: No
- Description: Reported collection size.

### `data.limit`

- Type: integer
- Required: Yes
- Nullable: No
- Description: Applied page size.

### `data.offset`

- Type: integer
- Required: Yes
- Nullable: No
- Description: Applied starting position.

### `data.hasMore`

- Type: boolean
- Required: Yes
- Nullable: No
- Description: Indicates whether another page can be requested.

### `data.searchContextId`

- Type: string
- Required: Yes
- Nullable: No
- Description: Search-context identifier.

### `data.snapshotVersion`

- Type: integer
- Required: Yes
- Nullable: No
- Description: Search snapshot version.

### `data.validUntil`

- Type: string
- Required: Yes
- Nullable: No
- Format: ISO 8601 date-time
- Description: Snapshot timestamp.

### `data.partial`

- Type: boolean
- Required: Yes
- Nullable: No
- Description: Indicates a partial search response.

### `data.providerErrors[]`

- Type: object array
- Required: Yes
- Nullable: No
- Fields: `providerId` (string), `code` (string).
- Description: Provider-level public outcomes.

## Error Response — HTTP 400

- Code: `VALIDATION_ERROR`
- Trigger: A query parameter cannot be decoded or does not match the declared wire type.
- Description: Protocol-level query error.
- Example message: `The query parameters are invalid.`

## Error Response — HTTP 409

- Code: `SEARCH_CONTEXT_CONFLICT`
- Trigger: The request conflicts with the current search context.
- Description: Public search-context conflict.
- Example message: `The request could not be completed.`

## Error Response — HTTP 422

- Code: `UNPROCESSABLE_REQUEST`
- Trigger: The syntactically valid request cannot be completed.
- Description: Public processing failure.
- Example message: `The request could not be completed.`

## Error Response — HTTP 429

- Code: `RATE_LIMITED`
- Trigger: The service temporarily rejects additional requests from the client.
- Description: Public request-throttling response.
- Example message: `Too many requests.`

## Error Response — HTTP 502

- Code: `UPSTREAM_ERROR`
- Trigger: An upstream dependency returns an unusable result.
- Description: Upstream search failure.
- Example message: `An upstream service returned an invalid response.`

## Error Response — HTTP 503

- Code: `SERVICE_UNAVAILABLE`
- Trigger: The endpoint is temporarily unable to return search results.
- Description: Temporary service failure.
- Example message: `The service is temporarily unavailable.`

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md).

The current scope does not define flight-offer detail or booking endpoints. Cross-field evaluation and result-ranking logic are outside this wire contract.
