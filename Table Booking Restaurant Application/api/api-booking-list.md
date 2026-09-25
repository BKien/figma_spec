# API-BOOKING-LIST — View Booking History

## API ID

`API-BOOKING-LIST`

## API Name

View Booking History

## Related Use Case IDs

- `UC-09`

## Method

`GET`

## Path

`/api/v1/me/bookings`

## Description

Accepts the displayed view booking history interaction and returns its public result.

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


## Path Parameters

None.

## Query Parameters

None.

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

### `data.bookings`

- Type: array
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON array.
- Description: data bookings supplied on the wire.
- Example: `[]`

### `data.nextCursor`

- Type: string
- Required: No
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data nextCursor supplied on the wire.
- Example: `cur_123`

### `data.bookings[].id`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data bookings[] id supplied on the wire.
- Example: `bkg_123`

### `data.bookings[].status`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data bookings[] status supplied on the wire.
- Example: `CONFIRMED`

### `data.bookings[].restaurantName`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data bookings[] restaurantName supplied on the wire.
- Example: `Villagio Restaurant and Bar`

### `data.bookings[].startsAt`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data bookings[] startsAt supplied on the wire.
- Example: `2026-10-02T19:00:00Z`

### `data.bookings[].partySize`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON integer.
- Description: data bookings[] partySize supplied on the wire.
- Example: `2`




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

## Notes

The common response envelope and pagination conventions are defined in [common-contract.md](common-contract.md). Business behavior is specified only in [UC-09](../uc/uc-09-view-bookings.md).
