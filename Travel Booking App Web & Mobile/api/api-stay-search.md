# API-STAY-SEARCH — Search Stays

## API ID

`API-STAY-SEARCH`

## API Name

Stay Search

## Related Use Case IDs

- `UC-04`
- `UC-05`
- `UC-06`

## Method

`GET`

## Path

`/api/v1/stays/search`

## Description

Returns a paginated collection of stay offers for submitted search criteria.

## Authentication

Public

## Authorization

None

## Request Headers

None.

## Path Parameters

None.

## Query Parameters

### `destinationId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a query-string value.
- Description: Opaque destination identifier.
- Example: `loc_paris`

### `checkIn`

- Type: string
- Format: date (`YYYY-MM-DD`)
- Required: Yes
- Nullable: No
- Validation: Must use the declared date syntax.
- Description: Requested check-in date.
- Example: `2026-10-10`

### `checkOut`

- Type: string
- Format: date (`YYYY-MM-DD`)
- Required: Yes
- Nullable: No
- Validation: Must use the declared date syntax.
- Description: Requested check-out date.
- Example: `2026-10-14`

### `rooms`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must use integer syntax.
- Description: Requested room count.
- Example: `1`

### `adults`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must use integer syntax.
- Description: Requested adult guest count.
- Example: `2`

### `minPrice`

- Type: number
- Required: No
- Nullable: No
- Validation: Must use JSON-compatible decimal syntax when supplied.
- Description: Client-supplied lower price filter.
- Example: `50.00`

### `maxPrice`

- Type: number
- Required: No
- Nullable: No
- Validation: Must use JSON-compatible decimal syntax when supplied.
- Description: Client-supplied upper price filter.
- Example: `250.00`

### `minRating`

- Type: number
- Required: No
- Nullable: No
- Validation: Must use JSON-compatible decimal syntax when supplied.
- Description: Client-supplied rating filter.
- Example: `4.0`

### `sort`

- Type: string
- Format: enum
- Required: No
- Default: `RECOMMENDED`
- Nullable: No
- Allowed values: `RECOMMENDED`, `PRICE`, `RATING`
- Validation: Must match one public enum value when supplied.
- Description: Requested result ordering.
- Example: `RECOMMENDED`

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
- Example: `Stay offers retrieved.`

### `data.items[]`

- Type: object array
- Required: Yes
- Nullable: No
- Fields: `offerId` (string), `stayId` (string), `stayName` (string), `rating` (number), `availableRooms` (integer), `total` (money object).
- Description: Stay offers in the current page.

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

All identifiers are opaque client values. Cross-field evaluation is outside this wire contract.
