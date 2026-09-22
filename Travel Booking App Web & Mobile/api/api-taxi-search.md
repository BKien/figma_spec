# API-TAXI-SEARCH — Search Taxis

## API ID

`API-TAXI-SEARCH`

## API Name

Taxi Search

## Related Use Case IDs

- `UC-09`
- `UC-10`
- `UC-11`

## Method

`GET`

## Path

`/api/v1/taxis/search`

## Description

Returns a paginated collection of taxi offers for submitted search criteria.

## Authentication

Public

## Authorization

None

## Request Headers

None.

## Path Parameters

None.

## Query Parameters

### `pickupId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a query-string value.
- Description: Opaque pickup-location identifier.
- Example: `loc_airport`

### `dropoffId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a query-string value.
- Description: Opaque drop-off-location identifier.
- Example: `loc_city_center`

### `pickupAt`

- Type: string
- Format: ISO 8601 date-time
- Required: Yes
- Nullable: No
- Validation: Must use the declared date-time syntax.
- Description: Requested pickup time.
- Example: `2026-10-10T08:30:00+07:00`

### `dropoffAt`

- Type: string
- Format: ISO 8601 date-time
- Required: Yes
- Nullable: No
- Validation: Must use the declared date-time syntax.
- Description: Requested drop-off time.
- Example: `2026-10-10T09:30:00+07:00`

### `passengers`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must use integer syntax.
- Description: Requested passenger count.
- Example: `2`

### `minPrice`

- Type: number
- Required: No
- Nullable: No
- Validation: Must use JSON-compatible decimal syntax when supplied.
- Description: Client-supplied lower price filter.
- Example: `10.00`

### `maxPrice`

- Type: number
- Required: No
- Nullable: No
- Validation: Must use JSON-compatible decimal syntax when supplied.
- Description: Client-supplied upper price filter.
- Example: `80.00`

### `sort`

- Type: string
- Format: enum
- Required: No
- Default: `RECOMMENDED`
- Nullable: No
- Allowed values: `RECOMMENDED`, `PRICE`, `DISTANCE`
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

### `vehicleTypes`

- Type: string array
- Required: No
- Nullable: No
- Serialization: repeated query parameter
- Validation: Every supplied value must use query-string syntax.
- Description: Vehicle-type filters.

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
- Example: `Taxi offers retrieved.`

### `data.items[]`

- Type: object array
- Required: Yes
- Nullable: No
- Fields: `offerId` (string), `vehicleType` (string), `seats` (integer), `distanceKm` (number), `total` (money object).
- Description: Taxi offers in the current page.

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
