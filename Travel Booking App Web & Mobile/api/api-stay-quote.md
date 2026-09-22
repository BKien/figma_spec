# API-STAY-QUOTE — Quote a Stay Booking

## API ID

`API-STAY-QUOTE`

## API Name

Stay Booking Quote

## Related Use Case IDs

- `UC-08`

## Method

`POST`

## Path

`/api/v1/stay-bookings/quotes`

## Description

Accepts a stay-offer reference and returns a quote response for checkout.

## Authentication

Bearer access token

## Authorization

Authenticated user

## Request Headers

### `Authorization`

- Type: string
- Format: bearer token
- Required: Yes
- Nullable: No
- Validation: Must use the `Bearer <access-token>` syntax.
- Description: Carries the access token.
- Example: `Bearer eyJhbGciOiJIUzI1NiIs...`

### `Content-Type`

- Type: string
- Format: MIME type
- Required: Yes
- Nullable: No
- Allowed value: `application/json`
- Validation: Must identify a JSON request body.
- Description: Declares the request body media type.
- Example: `application/json`

## Path Parameters

None.

## Query Parameters

None.

## Request Body

### `offerId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Opaque stay-offer identifier.
- Example: `so_01JABCDEF`

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
- Example: `Stay quote created.`

### `data.quoteId`

- Type: string
- Required: Yes
- Nullable: No
- Description: Quote identifier.

### `data.offerId`

- Type: string
- Required: Yes
- Nullable: No
- Description: Referenced stay-offer identifier.

### `data.available`

- Type: boolean
- Required: Yes
- Nullable: No
- Description: Availability indicator returned with the quote.

### `data.total`

- Type: money object
- Required: Yes
- Nullable: No
- Description: Quoted total.

### `data.expiresAt`

- Type: string
- Format: ISO 8601 date-time
- Required: Yes
- Nullable: No
- Description: Quote expiration timestamp.

## Error Response — HTTP 400

- Code: `VALIDATION_ERROR`
- Trigger: The request cannot be decoded or does not match the declared wire schema.
- Description: Protocol-level request error.
- Example message: `The request could not be completed.`

## Error Response — HTTP 401

- Code: `UNAUTHORIZED`
- Trigger: The endpoint does not accept the supplied authentication context.
- Description: Authentication error.
- Example message: `Authentication is required.`

## Error Response — HTTP 404

- Code: `NOT_FOUND`
- Trigger: The referenced checkout resource cannot be returned.
- Description: Public not-found response.
- Example message: `The requested resource was not found.`

## Error Response — HTTP 409

- Code: `CHECKOUT_CONFLICT`
- Trigger: The quote request conflicts with the current checkout state.
- Description: Public checkout conflict.
- Example message: `The quote request could not be completed.`

## Error Response — HTTP 502

- Code: `UPSTREAM_ERROR`
- Trigger: An upstream dependency returns an unusable result.
- Description: Upstream quote failure.
- Example message: `An upstream service returned an invalid response.`

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md).

The contract does not disclose how the service evaluates or constructs a quote.
