---
artifact_type: api-contract
status: Frozen
api_id: API-TAXI-QUOTE
related_uc_id: UC-13
---

# API-TAXI-QUOTE: Taxi Rental Quote

## General Information

### API ID

API-TAXI-QUOTE

### API Name

Taxi Rental Quote

### Related Use Case IDs

- UC-13

### Method

POST

### Path

/api/v1/taxi-quotes

### Description

Revalidates a selected Taxi rental offer and returns the checkout summary.

### Authentication

Bearer access token.

### Authorization

Authenticated user.

## Request Header(s)

### headers.Authorization

Type: string; Format: bearer token; Required: Yes; Nullable: No

Trigger: Every POST request to this endpoint.

Description: Carries the access token.

Example: Bearer eyJhbGciOiJIUzI1NiIs...

Note: Uses the HTTP Bearer authentication scheme.

Validation: Must use the Bearer <access-token> syntax.

### headers.Content-Type

Type: string; Format: MIME type; Required: Yes; Nullable: No

Trigger: Every POST request to this endpoint.

Description: Declares the request body media type.

Example: application/json

Note: Identifies the media type of the submitted request body.

Allowed values: application/json

Validation: Must be encoded as a JSON string.

## Path Parameter(s)

None.

## Query Parameter(s)

None.

## Request Body

### offerId

Type: string; Format: opaque identifier; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Selected Taxi rental offer.

Example: to_01JABCDEF

Validation: Must be encoded as a JSON string.

## Success Response — HTTP 200

### success

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Indicates whether the HTTP operation completed successfully.

Example: true

Validation: Must be encoded as the declared JSON type.

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Human-readable operation outcome summary.

Example: Taxi rental quote created.

Validation: Must be encoded as a JSON string.

### data.quoteId

Type: string; Format: opaque identifier; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Checkout quote identifier.

Example: tq_01JABCDEF

Validation: Must be encoded as a JSON string.

### data.offerId

Type: string; Format: opaque identifier; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Quoted offer identifier.

Example: to_01JABCDEF

Validation: Must be encoded as a JSON string.

### data.available

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Availability outcome returned by the service.

Example: true

Validation: Must be encoded as the declared JSON type.

### data.total

Type: money object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Quoted rental price.

Example: {"amount": 300.0, "currency": "LKR"}

Validation: Must be encoded as the declared JSON type.

### data.deposit

Type: money object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Pick-up deposit displayed by checkout.

Example: {"amount": 300.0, "currency": "LKR"}

Validation: Must be encoded as the declared JSON type.

### data.paymentMode

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Payment option returned for checkout.

Example: PAY_DRIVER

Allowed values: ONLINE, PAY_DRIVER

Validation: Must be encoded as a JSON string.

### data.expiresAt

Type: string; Format: ISO 8601 date-time; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Quote expiry time.

Example: 2026-06-25T12:15:00+05:30

Validation: Must use ISO 8601 date-time syntax with an offset.

## Error Response — HTTP 400

- Code: VALIDATION_ERROR
Trigger: The request cannot be decoded or does not match the declared wire schema.
Description: Protocol-level request error.
- Example message: The request could not be completed.

## Error Response — HTTP 401

- Code: UNAUTHORIZED
Trigger: The endpoint does not accept the supplied authentication context.
Description: Authentication error.
- Example message: The request could not be completed.

## Error Response — HTTP 404

- Code: NOT_FOUND
Trigger: The selected offer cannot be returned.
Description: Public not-found response.
- Example message: The request could not be completed.

## Error Response — HTTP 409

- Code: QUOTE_CONFLICT
Trigger: The request conflicts with the current offer state.
Description: Public quote conflict.
- Example message: The request could not be completed.

## Error Response — HTTP 502

- Code: UPSTREAM_ERROR
Trigger: A required provider does not return a usable response.
Description: Provider failure.
- Example message: The request could not be completed.

## Error Response — HTTP 503

- Code: SERVICE_UNAVAILABLE
Trigger: The endpoint is temporarily unable to return a quote.
Description: Temporary quote failure.
- Example message: The request could not be completed.

## Notes

Response envelopes and money values follow the [common API contract](common-contract.md).
