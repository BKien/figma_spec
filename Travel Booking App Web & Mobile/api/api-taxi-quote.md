# API-TAXI-QUOTE — Quote a Taxi Rental

## API ID

`API-TAXI-QUOTE`

## API Name

Taxi Rental Quote

## Related Use Case IDs

- `UC-13`

## Method

`POST`

## Path

`/api/v1/taxi-quotes`

## Description

Revalidates a selected Taxi rental offer and returns the checkout summary.

## Authentication

Bearer access token.

## Authorization

Authenticated user.

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
- Allowed values: `application/json`
- Validation: Must be encoded as a JSON string.
- Description: Declares the request body media type.
- Example: `application/json`

## Path Parameters

None.

## Query Parameters

None.

## Request Body

### `offerId`

- Type: string
- Format: opaque identifier
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Selected Taxi rental offer.
- Example: `to_01JABCDEF`

## Success Response — HTTP 200

### `success`

- Type: boolean
- Required: Yes
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Example: `true`

### `message`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Example: `Taxi rental quote created.`

### `data.quoteId`

- Type: string
- Format: opaque identifier
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Checkout quote identifier.
- Example: `tq_01JABCDEF`

### `data.offerId`

- Type: string
- Format: opaque identifier
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Quoted offer identifier.
- Example: `to_01JABCDEF`

### `data.available`

- Type: boolean
- Required: Yes
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Availability outcome returned by the service.
- Example: `true`

### `data.total`

- Type: money object
- Required: Yes
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Quoted rental price.

### `data.deposit`

- Type: money object
- Required: Yes
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Pick-up deposit displayed by checkout.

### `data.paymentMode`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `ONLINE`, `PAY_DRIVER`
- Validation: Must be encoded as a JSON string.
- Description: Payment option returned for checkout.
- Example: `PAY_DRIVER`

### `data.expiresAt`

- Type: string
- Format: ISO 8601 date-time
- Required: Yes
- Nullable: No
- Validation: Must use ISO 8601 date-time syntax with an offset.
- Description: Quote expiry time.
- Example: `2026-06-25T12:15:00+05:30`

## Error Response — HTTP 400

- Code: `VALIDATION_ERROR`
- Trigger: The request cannot be decoded or does not match the declared wire schema.
- Description: Protocol-level request error.
- Example message: `The request could not be completed.`

## Error Response — HTTP 401

- Code: `UNAUTHORIZED`
- Trigger: The endpoint does not accept the supplied authentication context.
- Description: Authentication error.
- Example message: `The request could not be completed.`

## Error Response — HTTP 404

- Code: `NOT_FOUND`
- Trigger: The selected offer cannot be returned.
- Description: Public not-found response.
- Example message: `The request could not be completed.`

## Error Response — HTTP 409

- Code: `QUOTE_CONFLICT`
- Trigger: The request conflicts with the current offer state.
- Description: Public quote conflict.
- Example message: `The request could not be completed.`

## Error Response — HTTP 502

- Code: `UPSTREAM_ERROR`
- Trigger: A required provider does not return a usable response.
- Description: Provider failure.
- Example message: `The request could not be completed.`

## Error Response — HTTP 503

- Code: `SERVICE_UNAVAILABLE`
- Trigger: The endpoint is temporarily unable to return a quote.
- Description: Temporary quote failure.
- Example message: `The request could not be completed.`

## Notes

Response envelopes and money values follow the [common API contract](common-contract.md).
