# API-BOOKING-UPDATE — Change a Booking

## API ID

`API-BOOKING-UPDATE`

## API Name

Change a Booking

## Related Use Case IDs

- `UC-10`

## Method

`PATCH`

## Path

`/api/v1/bookings/{bookingId}`

## Description

Accepts the displayed change a booking interaction and returns its public result.

## Authentication

Bearer access token.

## Authorization

Authenticated customer.

## Request Headers

### `Authorization`

- Type: string
- Format: bearer token
- Required: Yes
- Nullable: No
- Validation: Must use the `Bearer <access-token>` header syntax.
- Description: Carries the bearer access token.
- Example: `Bearer eyJ...`

### `Content-Type`

- Type: string
- Format: MIME type
- Required: Yes
- Nullable: No
- Allowed values: application/json
- Validation: Must identify the `application/json` media type.
- Description: Declares the request media type.
- Example: `application/json`


## Path Parameters

### `bookingId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as one URL path segment.
- Description: bookingId supplied on the wire.
- Example: `bkg_123`


## Query Parameters

None.

## Request Body

### `slotId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: slotId supplied on the wire.
- Example: `slot_456`

### `partySize`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON integer.
- Description: partySize supplied on the wire.
- Example: `3`

### `version`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON integer.
- Description: version supplied on the wire.
- Example: `2`


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

### `data.bookingId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data bookingId supplied on the wire.
- Example: `bkg_123`

### `data.status`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data status supplied on the wire.
- Example: `CONFIRMED`

### `data.version`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON integer.
- Description: data version supplied on the wire.
- Example: `3`




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

## Error Response — HTTP 401

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
- Example: `AUTHENTICATION_REQUIRED`

- Trigger: Rejected authentication context.

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

## Error Response — HTTP 409

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
- Example: `OPERATION_CONFLICT`

- Trigger: Operation conflict response.

## Notes

The common response envelope and pagination conventions are defined in [common-contract.md](common-contract.md). Business behavior is specified only in [UC-10](../uc/uc-10-change-booking.md).
