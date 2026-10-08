---
artifact_type: api-contract
status: Frozen
api_id: API-STAY-BOOKING-CREATE
related_uc_id: UC-08
---

# API-STAY-BOOKING-CREATE: Stay Booking Creation

## General Information

### API ID

API-STAY-BOOKING-CREATE

### API Name

Stay Booking Creation

### Related Use Case IDs

- UC-08

### Method

POST

### Path

/api/v1/stay-bookings

### Description

Accepts checkout data and returns a stay-booking response.

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

### headers.Idempotency-Key

Type: string; Format: Opaque HTTP header value; Required: Yes; Nullable: No

Trigger: Every POST request to this endpoint.

Description: Client-generated operation key.

Example: book-stay-7ec67a2d

Note: Transmit the command reference as a single header value.

Validation: Must be encoded as an HTTP header value.

## Path Parameter(s)

None.

## Query Parameter(s)

None.

## Request Body

### quoteId

Type: string; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Opaque quote identifier.

Example: sq_01JABCDEF

Validation: Must be encoded as a JSON string.

### guest.firstName

Type: string; Required: Yes; Nullable: No

Trigger: When the containing guest object or array item is supplied in the request body.

Description: Guest first name.

Example: Alex

Validation: Must be encoded as a JSON string.

### guest.lastName

Type: string; Required: Yes; Nullable: No

Trigger: When the containing guest object or array item is supplied in the request body.

Description: Guest last name.

Example: Morgan

Validation: Must be encoded as a JSON string.

### guest.homeAddress

Type: string; Required: Yes; Nullable: No

Trigger: When the containing guest object or array item is supplied in the request body.

Description: Home address entered at checkout.

Example: 14 Lake Road, Colombo

Validation: Must be encoded as a JSON string.

### guest.bookingFor

Type: string; Required: Yes; Nullable: No

Trigger: When the containing guest object or array item is supplied in the request body.

Description: Displayed booking-party choice.

Example: MAIN_GUEST

Allowed values: MAIN_GUEST, SOMEONE_ELSE

Validation: Must be one of the public enum values.

### guest.workTravel

Type: boolean; Required: Yes; Nullable: No

Trigger: When the containing guest object or array item is supplied in the request body.

Description: Displayed work-travel choice.

Example: false

Validation: Must be encoded as a JSON boolean.

### guest.email

Type: string; Format: email; Required: Yes; Nullable: No

Trigger: When the containing guest object or array item is supplied in the request body.

Description: Guest email address.

Example: alex@example.com

Validation: Must use email-address syntax.

### guest.phone

Type: string; Format: telephone number; Required: Yes; Nullable: No

Trigger: When the containing guest object or array item is supplied in the request body.

Description: Guest phone number.

Example: +12025550123

Validation: Must be encoded as a JSON string.

### guest.countryCode

Type: string; Format: country code; Required: Yes; Nullable: No

Trigger: When the containing guest object or array item is supplied in the request body.

Description: Guest country code.

Example: US

Validation: Must be encoded as a JSON string.

### paymentToken

Type: string; Format: payment-provider token; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Opaque payment reference supplied by the payment client.

Example: pay_tok_01JABCDEF

Validation: Must be encoded as a JSON string.

### savePaymentMethod

Type: boolean; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Save-card checkbox selection.

Example: false

Validation: Must be encoded as a JSON boolean.

## Success Response — HTTP 201

### success

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response.

Description: Indicates whether the HTTP operation completed successfully.

Example: true

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response.

Description: Human-readable operation outcome summary.

Example: Stay booking created.

### data.id

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Booking identifier.

Example: "stay_01JABCDEF"

### data.status

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Booking status returned by the service.

Example: "PENDING"

Allowed values: PENDING, CONFIRMED, FAILED, CANCELLED

### data.total

Type: money object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Booking total.

Example: {"amount": 300.0, "currency": "USD"}

### data.createdAt

Type: string; Format: ISO 8601 date-time; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Booking creation timestamp.

Example: "2026-10-07T09:00:00Z"

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

Example: Stay booking returned.

### data.id

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Booking identifier.

Example: "stay_01JABCDEF"

### data.status

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Booking status returned by the service.

Example: "PENDING"

Allowed values: PENDING, CONFIRMED, FAILED, CANCELLED

### data.total

Type: money object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Booking total.

Example: {"amount": 300.0, "currency": "USD"}

### data.createdAt

Type: string; Format: ISO 8601 date-time; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Booking creation timestamp.

Example: "2026-10-07T09:00:00Z"

## Error Response — HTTP 400

- Code: VALIDATION_ERROR
Trigger: The request cannot be decoded or does not match the declared wire schema.
Description: Protocol-level request error.
- Example message: The request payload is invalid.

## Error Response — HTTP 401

- Code: UNAUTHORIZED
Trigger: The endpoint does not accept the supplied authentication context.
Description: Authentication error.
- Example message: Authentication is required.

## Error Response — HTTP 404

- Code: NOT_FOUND
Trigger: A referenced checkout resource cannot be returned.
Description: Public not-found response.
- Example message: The requested resource was not found.

## Error Response — HTTP 409

- Code: CHECKOUT_CONFLICT
Trigger: The request conflicts with the current checkout state.
Description: Public checkout conflict.
- Example message: The booking request could not be completed.

## Error Response — HTTP 422

- Code: UNPROCESSABLE_REQUEST
Trigger: The syntactically valid request cannot be completed by a required processor.
Description: Public processing failure.
- Example message: The booking request could not be processed.

## Error Response — HTTP 503

- Code: SERVICE_UNAVAILABLE
Trigger: The operation cannot currently return a definitive response.
Description: Temporary booking-service failure.
- Example message: The request could not be completed.

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md).

The card fields visible in Figma belong to a payment-provider control; this API receives only its opaque token. No card number, expiry value, or CVV is accepted or stored. HTTP 201 and HTTP 200 use the same response schema.
