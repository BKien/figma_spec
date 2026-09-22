# API-HOME-SUMMARY — Get Home Summary

## API ID

`API-HOME-SUMMARY`

## API Name

Home Summary

## Related Use Case IDs

- `UC-03`

## Method

`GET`

## Path

`/api/v1/home`

## Description

Returns the content collections required to render the home page.

## Authentication

Optional bearer access token

## Authorization

Public

## Request Headers

### `Authorization`

- Type: string
- Format: bearer token
- Required: No
- Nullable: No
- Validation: When supplied, must use the `Bearer <access-token>` syntax.
- Trigger: Optional authenticated navigation context.
- Description: Carries an optional access token.
- Example: `Bearer eyJhbGciOiJIUzI1NiIs...`

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
- Example: `true`

### `message`

- Type: string
- Required: Yes
- Nullable: No
- Example: `Home summary retrieved.`

### `data.services`

- Type: string array
- Required: Yes
- Nullable: No
- Description: Service labels presented by the home page.
- Example: `["Stays", "Taxis", "Flights"]`

### `data.destinations[]`

- Type: object array
- Required: Yes
- Nullable: No
- Fields: `id` (string), `title` (string), `imageUrl` (URI string), `startingPrice` (money object).
- Description: Destination cards displayed on the home page.

### `data.reviews[]`

- Type: object array
- Required: Yes
- Nullable: No
- Fields: `id` (string), `authorName` (string), `rating` (integer), `comment` (string).
- Description: Review cards displayed on the home page.

### `data.viewer`

- Type: object
- Required: Yes
- Nullable: No
- Fields: `authenticated` (boolean), `displayName` (nullable string).
- Description: Navigation display context.

### `data.sectionStates`

- Type: object
- Required: Yes
- Nullable: No
- Fields: `destinations` (string), `reviews` (string).
- Allowed values for each field: `READY`, `EMPTY`, `UNAVAILABLE`.
- Description: Content-section outcomes.

## Error Response — HTTP 401

- Code: `UNAUTHORIZED`
- Trigger: The endpoint does not accept the supplied authentication context.
- Description: Public authentication failure.
- Example message: `The request could not be completed.`

## Error Response — HTTP 500

- Code: `INTERNAL_ERROR`
- Trigger: An unexpected server error prevents the response from being produced.
- Description: Unexpected home-content failure.
- Example message: `Internal Server Error`

## Error Response — HTTP 503

- Code: `SERVICE_UNAVAILABLE`
- Trigger: The endpoint is temporarily unable to return the home summary.
- Description: Temporary service failure.
- Example message: `The service is temporarily unavailable.`

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md).

The optional token does not change the wire shape of the response.
