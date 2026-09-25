# API-ADMIN-REPORT-GET — View Reports

## API ID

`API-ADMIN-REPORT-GET`

## API Name

View Reports

## Related Use Case IDs

- `UC-20`

## Method

`GET`

## Path

`/api/v1/admin/reports`

## Description

Accepts the displayed view reports interaction and returns its public result.

## Authentication

Bearer access token.

## Authorization

Administration role.

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

### `restaurantId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as one URL query value.
- Description: restaurantId supplied on the wire.
- Example: `rst_123`

### `from`

- Type: string
- Format: date
- Required: Yes
- Nullable: No
- Validation: Must use ISO 8601 calendar-date syntax.
- Description: from supplied on the wire.
- Example: `2026-09-01`

### `to`

- Type: string
- Format: date
- Required: Yes
- Nullable: No
- Validation: Must use ISO 8601 calendar-date syntax.
- Description: to supplied on the wire.
- Example: `2026-09-30`


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

### `data.bookingCount`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON integer.
- Description: data bookingCount supplied on the wire.
- Example: `42`

### `data.cancelledCount`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON integer.
- Description: data cancelledCount supplied on the wire.
- Example: `3`

### `data.series`

- Type: array
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON array.
- Description: data series supplied on the wire.
- Example: `[]`

### `data.series[].date`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data series[] date supplied on the wire.
- Example: `2026-09-01`

### `data.series[].bookingCount`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON integer.
- Description: data series[] bookingCount supplied on the wire.
- Example: `5`




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

## Error Response — HTTP 403

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
- Example: `ACCESS_DENIED`

- Trigger: Access denied response.

## Notes

The common response envelope and pagination conventions are defined in [common-contract.md](common-contract.md). Business behavior is specified only in [UC-20](../uc/uc-20-view-reports.md).
