# API-NOTIFICATION-LIST — View Notifications

## API ID

`API-NOTIFICATION-LIST`

## API Name

View Notifications

## Related Use Case IDs

- `UC-12`

## Method

`GET`

## Path

`/api/v1/me/notifications`

## Description

Accepts the displayed view notifications interaction and returns its public result.

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

### `data.notifications`

- Type: array
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON array.
- Description: data notifications supplied on the wire.
- Example: `[]`

### `data.nextCursor`

- Type: string
- Required: No
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data nextCursor supplied on the wire.
- Example: `cur_123`

### `data.notifications[].id`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data notifications[] id supplied on the wire.
- Example: `ntf_123`

### `data.notifications[].title`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data notifications[] title supplied on the wire.
- Example: `Booking confirmed`

### `data.notifications[].body`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data notifications[] body supplied on the wire.
- Example: `Your table is booked.`

### `data.notifications[].createdAt`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data notifications[] createdAt supplied on the wire.
- Example: `2026-09-24T10:00:00Z`




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

The common response envelope and pagination conventions are defined in [common-contract.md](common-contract.md). Business behavior is specified only in [UC-12](../uc/uc-12-view-notifications.md).
