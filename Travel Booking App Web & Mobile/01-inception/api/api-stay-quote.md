---
artifact_type: api-contract
status: Frozen
api_id: API-STAY-QUOTE
related_uc_id: UC-08
---

# API-STAY-QUOTE: Stay Booking Quote

## General Information

### API ID

API-STAY-QUOTE

### API Name

Stay Booking Quote

### Related Use Case IDs

- UC-08

### Method

POST

### Path

/api/v1/stay-bookings/quotes

### Description

Accepts a stay-offer reference and returns a quote response for checkout.

### Authentication

Bearer access token

### Authorization

Authenticated user

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

Allowed value: application/json

Validation: Must identify a JSON request body.

## Path Parameter(s)

None.

## Query Parameter(s)

None.

## Request Body

### offerId

Type: string; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Opaque stay-offer identifier.

Example: so_01JABCDEF

Validation: Must be encoded as a JSON string.

## Success Response — HTTP 200

### success

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Indicates whether the HTTP operation completed successfully.

Example: true

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Human-readable operation outcome summary.

Example: Stay quote created.

### data.quoteId

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Quote identifier.

Example: "quote_01JABCDEF"

### data.offerId

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Referenced stay-offer identifier.

Example: "offer_01JABCDEF"

### data.available

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Availability indicator returned with the quote.

Example: true

### data.total

Type: money object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Quoted total.

Example: {"amount": 300.0, "currency": "USD"}

### data.expiresAt

Type: string; Format: ISO 8601 date-time; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Quote expiration timestamp.

Example: "2026-10-10T20:30:00Z"

## Error Response — HTTP 400

- Code: VALIDATION_ERROR
Trigger: The request cannot be decoded or does not match the declared wire schema.
Description: Protocol-level request error.
- Example message: The request could not be completed.

## Error Response — HTTP 401

- Code: UNAUTHORIZED
Trigger: The endpoint does not accept the supplied authentication context.
Description: Authentication error.
- Example message: Authentication is required.

## Error Response — HTTP 404

- Code: NOT_FOUND
Trigger: The referenced checkout resource cannot be returned.
Description: Public not-found response.
- Example message: The requested resource was not found.

## Error Response — HTTP 409

- Code: CHECKOUT_CONFLICT
Trigger: The quote request conflicts with the current checkout state.
Description: Public checkout conflict.
- Example message: The quote request could not be completed.

## Error Response — HTTP 502

- Code: UPSTREAM_ERROR
Trigger: An upstream dependency returns an unusable result.
Description: Upstream quote failure.
- Example message: An upstream service returned an invalid response.

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md).

The contract does not disclose how the service evaluates or constructs a quote.
