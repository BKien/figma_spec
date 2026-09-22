# API-LOCATION-SUGGEST — Suggest Locations

## API ID

`API-LOCATION-SUGGEST`

## API Name

Location Suggestions

## Related Use Case IDs

- `UC-04`
- `UC-09`

## Method

`GET`

## Path

`/api/v1/locations/suggestions`

## Description

Returns location suggestions for travel search inputs.

## Authentication

Public

## Authorization

None

## Request Headers

None.

## Path Parameters

None.

## Query Parameters

### `query`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a query-string value.
- Trigger: Location suggestion request.
- Description: User-entered location text.
- Example: `Paris`

### `limit`

- Type: integer
- Required: No
- Nullable: No
- Default: `10`
- Validation: Must use integer syntax when supplied.
- Trigger: Location suggestion request.
- Description: Requested result-page size.
- Example: `10`

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
- Example: `Location suggestions retrieved.`

### `data[]`

- Type: object array
- Required: Yes
- Nullable: No
- Fields: `id` (string), `name` (string), `countryCode` (string).
- Description: Suggested locations.
- Example: `[{"id":"loc_paris","name":"Paris","countryCode":"FR"}]`

## Error Response — HTTP 400

- Code: `VALIDATION_ERROR`
- Trigger: A query parameter cannot be decoded or does not match the declared wire type.
- Description: Protocol-level query error.
- Example message: `The query parameters are invalid.`

## Error Response — HTTP 422

- Code: `UNPROCESSABLE_REQUEST`
- Trigger: The syntactically valid request cannot be completed.
- Description: Public processing failure.
- Example message: `The request could not be completed.`

## Error Response — HTTP 500

- Code: `INTERNAL_ERROR`
- Trigger: An unexpected server error prevents suggestions from being returned.
- Description: Unexpected lookup failure.
- Example message: `Internal Server Error`

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md).

Location identifiers are opaque client values.
