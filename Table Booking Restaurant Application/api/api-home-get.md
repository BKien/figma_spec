# API-HOME-GET — Browse the Restaurant Home Page

## API ID

`API-HOME-GET`

## API Name

Browse the Restaurant Home Page

## Related Use Case IDs

- `UC-03`

## Method

`GET`

## Path

`/api/v1/home`

## Description

Accepts the displayed browse the restaurant home page interaction and returns its public result.

## Authentication

None.

## Authorization

Public endpoint.

## Request Headers

None.

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

### `data.restaurants`

- Type: array
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON array.
- Description: data restaurants supplied on the wire.
- Example: `[]`

### `data.featuredCount`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON integer.
- Description: data featuredCount supplied on the wire.
- Example: `4`

### `data.restaurants[].id`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data restaurants[] id supplied on the wire.
- Example: `rst_123`

### `data.restaurants[].name`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data restaurants[] name supplied on the wire.
- Example: `Villagio Restaurant and Bar`

### `data.restaurants[].heroImageUrl`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data restaurants[] heroImageUrl supplied on the wire.
- Example: `https://example.com/hero.jpg`




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

## Notes

The common response envelope and pagination conventions are defined in [common-contract.md](common-contract.md). Business behavior is specified only in [UC-03](../uc/uc-03-browse-home.md).
