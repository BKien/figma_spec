# API-SLOT-LIST — Check Table Availability

## API ID

`API-SLOT-LIST`

## API Name

Check Table Availability

## Related Use Case IDs

- `UC-07`

## Method

`GET`

## Path

`/api/v1/restaurants/{restaurantId}/slots`

## Description

Accepts the displayed check table availability interaction and returns its public result.

## Authentication

None.

## Authorization

Public endpoint.

## Request Headers

None.

## Path Parameters

### `restaurantId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as one URL path segment.
- Description: restaurantId supplied on the wire.
- Example: `rst_123`


## Query Parameters

### `date`

- Type: string
- Format: date
- Required: Yes
- Nullable: No
- Validation: Must use ISO 8601 calendar-date syntax.
- Description: date supplied on the wire.
- Example: `2026-10-02`

### `partySize`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must use decimal integer query syntax.
- Description: partySize supplied on the wire.
- Example: `2`


## Request Body

None.

## Success Response — HTTP 200

### `success`

- Type: boolean
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON boolean.
- Description: success supplied on the wire.
- Example: `true`

### `data`

- Type: object
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON object.
- Description: data supplied on the wire.
- Example: `{}`

### `data.slots`

- Type: array
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON array.
- Description: data slots supplied on the wire.
- Example: `[]`

### `data.date`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data date supplied on the wire.
- Example: `2026-10-02`

### `data.slots[].id`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data slots[] id supplied on the wire.
- Example: `slot_123`

### `data.slots[].startsAt`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data slots[] startsAt supplied on the wire.
- Example: `2026-10-02T19:00:00Z`

### `data.slots[].remainingSeats`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON integer.
- Description: data slots[] remainingSeats supplied on the wire.
- Example: `4`




## Error Response — HTTP 400

### `error`

- Type: object
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON object.
- Description: error supplied on the wire.
- Example: `{}`

### `error.code`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Stable public error identifier.
- Example: `MALFORMED_REQUEST`

### `error.message`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Human-readable error summary.
- Example: `The request could not be processed.`

- Trigger: Malformed wire input.

## Error Response — HTTP 503

### `error`

- Type: object
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON object.
- Description: error supplied on the wire.
- Example: `{}`

### `error.code`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Stable public error identifier.
- Example: `SERVICE_UNAVAILABLE`

### `error.message`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Human-readable error summary.
- Example: `Please try again later.`

- Trigger: Temporary service failure.

## Error Response — HTTP 404

### `error`

- Type: object
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON object.
- Description: error supplied on the wire.
- Example: `{}`

### `error.code`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Stable public error identifier.
- Example: `RESOURCE_UNAVAILABLE`

- Trigger: Unavailable resource response.

## Notes

The common response envelope and pagination conventions are defined in [common-contract.md](common-contract.md). Business behavior is specified only in [UC-07](../uc/uc-07-check-availability.md).
