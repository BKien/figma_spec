# API-BUDGET-TRIP-LIST — List Budget Trips

## API ID

`API-BUDGET-TRIP-LIST`

## API Name

Budget Trip List

## Related Use Case IDs

- `UC-16`

## Method

`GET`

## Path

`/api/v1/budget-trips`

## Description

Returns a paginated collection of budget-trip summaries.

## Authentication

Public

## Authorization

None

## Request Headers

None.

## Path Parameters

None.

## Query Parameters

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
- Example: `Budget trips retrieved.`

### `data.items[]`

- Type: object array
- Required: Yes
- Nullable: No
- Fields: `id` (string), `title` (string), `destinationName` (string), `imageUrl` (URI string), `startingPrice` (money object).
- Description: Budget-trip summaries in the current page.

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
- Trigger: An unexpected server error prevents trips from being returned.
- Description: Unexpected trip-service failure.
- Example message: `Internal Server Error`

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md).

Pagination fields follow the common API contract.
