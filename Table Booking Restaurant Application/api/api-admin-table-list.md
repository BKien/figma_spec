# API-ADMIN-TABLE-LIST — View Table Layout

## API ID

`API-ADMIN-TABLE-LIST`

## API Name

View Table Layout

## Related Use Case IDs

- `UC-17`

## Method

`GET`

## Path

`/api/v1/admin/restaurants/{restaurantId}/tables`

## Description

Accepts the displayed view table layout interaction and returns its public result.

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

### `restaurantId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as one URL path segment.
- Description: restaurantId supplied on the wire.
- Example: `rst_123`


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

### `data.tables`

- Type: array
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON array.
- Description: data tables supplied on the wire.
- Example: `[]`

### `data.restaurantId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data restaurantId supplied on the wire.
- Example: `rst_123`

### `data.tables[].id`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data tables[] id supplied on the wire.
- Example: `tbl_123`

### `data.tables[].label`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data tables[] label supplied on the wire.
- Example: `T1`

### `data.tables[].capacity`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON integer.
- Description: data tables[] capacity supplied on the wire.
- Example: `4`

### `data.tables[].layoutX`

- Type: number
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON number.
- Description: data tables[] layoutX supplied on the wire.
- Example: `120`

### `data.tables[].layoutY`

- Type: number
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON number.
- Description: data tables[] layoutY supplied on the wire.
- Example: `80`




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

The common response envelope and pagination conventions are defined in [common-contract.md](common-contract.md). Business behavior is specified only in [UC-17](../uc/uc-17-view-table-layout.md).
