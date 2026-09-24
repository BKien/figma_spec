# API-TAXI-SEARCH — Search Taxi Rentals

## API ID

`API-TAXI-SEARCH`

## API Name

Taxi Rental Search

## Related Use Case IDs

- `UC-09`
- `UC-10`
- `UC-11`

## Method

`GET`

## Path

`/api/v1/taxi-offers`

## Description

Returns vehicle-and-driver rental offers for one location and rental period.

## Authentication

None.

## Authorization

Public.

## Request Headers

None.

## Path Parameters

None.

## Query Parameters

### `locationId`

- Type: string
- Format: opaque identifier
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Selected rental location.
- Example: `loc_kurunegala`
### `pickupAt`

- Type: string
- Format: ISO 8601 date-time
- Required: Yes
- Nullable: No
- Validation: Must use ISO 8601 date-time syntax with an offset.
- Description: Selected pick-up date and time.
- Example: `2026-06-26T08:00:00+05:30`
### `dropoffAt`

- Type: string
- Format: ISO 8601 date-time
- Required: Yes
- Nullable: No
- Validation: Must use ISO 8601 date-time syntax with an offset.
- Description: Selected drop-off date and time.
- Example: `2026-06-27T08:00:00+05:30`
### `passengers`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Selected passenger count.
- Example: `2`
### `vehicleCategories`

- Type: string array
- Required: No
- Nullable: No
- Allowed values: `SMALL`, `MEDIUM`, `LARGE`, `ESTATE`
- Validation: Must be encoded as a JSON array of strings.
- Description: Selected car-category filters.
- Example: `["SMALL", "ESTATE"]`
### `depositBands`

- Type: string array
- Required: No
- Nullable: No
- Allowed values: `LKR_200_500`, `LKR_500_1000`, `LKR_1000_1200`, `LKR_1200_1500`
- Validation: Must be encoded as a JSON array of strings.
- Description: Selected pick-up-deposit bands shown by the interface.
- Example: `["LKR_200_500"]`
### `electricTypes`

- Type: string array
- Required: No
- Nullable: No
- Allowed values: `FULLY_ELECTRIC`, `HYBRID`
- Validation: Must be encoded as a JSON array of strings.
- Description: Selected electric-car filters.
- Example: `["HYBRID"]`
### `minPrice`

- Type: number
- Required: No
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Optional lower price filter.
- Example: `200`
### `maxPrice`

- Type: number
- Required: No
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Optional upper price filter.
- Example: `1500`
### `sort`

- Type: string
- Required: No
- Nullable: No
- Default: `TOP_PICKS`
- Allowed values: `TOP_PICKS`
- Validation: Must be encoded as a JSON string.
- Description: Selected result ordering.
- Example: `TOP_PICKS`
### `limit`

- Type: integer
- Required: No
- Nullable: No
- Default: `20`
- Validation: Must be encoded as the declared JSON type.
- Description: Requested page size.
- Example: `20`
### `offset`

- Type: integer
- Required: No
- Nullable: No
- Default: `0`
- Validation: Must be encoded as the declared JSON type.
- Description: Requested result offset.
- Example: `0`
### `searchContextId`

- Type: string
- Format: opaque identifier
- Required: No
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Existing result context used for pagination or refinement.
- Example: `ts_01JABCDEF`
### `snapshotVersion`

- Type: integer
- Required: No
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Existing result-context version.
- Example: `1`
### `currency`

- Type: string
- Required: No
- Nullable: No
- Default: `LKR`
- Allowed values: ISO 4217 currency code
- Validation: Must be encoded as a JSON string.
- Description: Requested comparison currency.
- Example: `LKR`

## Request Body

None.

## Success Response — HTTP 200

### `success`

- Type: boolean
- Required: Yes
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Indicates a successful response.
- Example: `true`

### `message`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Human-readable result summary.
- Example: `Taxi rental offers retrieved.`

### `data.items[]`

- Type: object array
- Required: Yes
- Nullable: No
- Fields: `offerId` (string), `vehicleName` (string), `vehicleCategory` (string), `seats` (integer), `transmission` (string), `largeBagCapacity` (integer), `smallBagCapacity` (integer), `electricType` (string), `distanceFromCenterKm` (number), `mileageAllowanceKm` (number), `deposit` (money object), `rating` (number), `total` (money object).
- Description: Vehicle cards displayed by the Taxi results page.

### `data.total`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Total matching offers.
- Example: `68`

### `data.limit`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Applied page size.
- Example: `20`

### `data.offset`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Applied result offset.
- Example: `0`

### `data.hasMore`

- Type: boolean
- Required: Yes
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Indicates whether another page is available.
- Example: `true`

### `data.searchContextId`

- Type: string
- Format: opaque identifier
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Returned result-context identifier.
- Example: `ts_01JABCDEF`

### `data.snapshotVersion`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Returned result-context version.
- Example: `1`

### `data.validUntil`

- Type: string
- Format: ISO 8601 date-time
- Required: Yes
- Nullable: No
- Validation: Must use ISO 8601 date-time syntax with an offset.
- Description: Result-context expiry time.
- Example: `2026-06-25T12:15:00+05:30`

## Error Response — HTTP 400

- Code: `VALIDATION_ERROR`
- Trigger: The request cannot be decoded or does not match the declared wire schema.
- Description: Protocol-level request error.
- Example message: `The request could not be completed.`

## Error Response — HTTP 409

- Code: `SEARCH_CONTEXT_CONFLICT`
- Trigger: The supplied result context cannot be used for this request.
- Description: Public result-context conflict.
- Example message: `The request could not be completed.`

## Error Response — HTTP 422

- Code: `UNPROCESSABLE_REQUEST`
- Trigger: The syntactically valid request cannot be processed.
- Description: Public processing outcome.
- Example message: `The request could not be completed.`

## Error Response — HTTP 502

- Code: `UPSTREAM_ERROR`
- Trigger: A required provider does not return a usable response.
- Description: Provider failure.
- Example message: `The request could not be completed.`

## Error Response — HTTP 503

- Code: `SERVICE_UNAVAILABLE`
- Trigger: The endpoint is temporarily unable to return results.
- Description: Temporary search failure.
- Example message: `The request could not be completed.`

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md). The service name remains `Taxi` because that is the Figma navigation label; the wire data represents a vehicle and driver rented at one location between the supplied times.
