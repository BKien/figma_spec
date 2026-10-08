---
artifact_type: api-contract
status: Frozen
api_id: API-TAXI-BOOKING-CREATE
related_uc_id: UC-13
---

# API-TAXI-BOOKING-CREATE: Taxi Rental Booking Creation

## General Information

### API ID

API-TAXI-BOOKING-CREATE

### API Name

Taxi Rental Booking Creation

### Related Use Case IDs

- UC-13

### Method

POST

### Path

/api/v1/taxi-bookings

### Description

Accepts the Taxi reservation form and returns the driver-follow-up booking outcome.

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

### headers.Idempotency-Key

Type: string; Format: Opaque HTTP header value; Required: Yes; Nullable: No

Trigger: Every POST request to this endpoint.

Description: Client-generated operation key.

Example: book-taxi-7ec67a2d

Note: Transmit the command reference as a single header value.

Validation: Must be encoded as a JSON string.

## Path Parameter(s)

None.

## Query Parameter(s)

None.

## Request Body

### quoteId

Type: string; Format: opaque identifier; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Checkout quote identifier.

Example: tq_01JABCDEF

Validation: Must be encoded as a JSON string.

### guest.firstName

Type: string; Required: Yes; Nullable: No

Trigger: When the containing guest object or array item is supplied in the request body.

Description: First name entered at checkout.

Example: Alex

Validation: Must be encoded as a JSON string.

### guest.lastName

Type: string; Required: Yes; Nullable: No

Trigger: When the containing guest object or array item is supplied in the request body.

Description: Last name entered at checkout.

Example: Morgan

Validation: Must be encoded as a JSON string.

### guest.homeAddress

Type: string; Required: Yes; Nullable: No

Trigger: When the containing guest object or array item is supplied in the request body.

Description: Home address entered at checkout.

Example: 14 Lake Road, Colombo

Validation: Must be encoded as a JSON string.

### guest.email

Type: string; Format: email; Required: Yes; Nullable: No

Trigger: When the containing guest object or array item is supplied in the request body.

Description: Confirmation email address.

Example: alex@example.com

Validation: Must use email-address syntax.

### guest.countryCode

Type: string; Required: Yes; Nullable: No

Trigger: When the containing guest object or array item is supplied in the request body.

Description: Country or region code selected at checkout.

Example: LK

Validation: Must be encoded as a JSON string.

### guest.phone

Type: string; Required: Yes; Nullable: No

Trigger: When the containing guest object or array item is supplied in the request body.

Description: Telephone number entered at checkout.

Example: +94771234567

Validation: Must be encoded as a JSON string.

### guest.bookingFor

Type: string; Required: Yes; Nullable: No

Trigger: When the containing guest object or array item is supplied in the request body.

Description: Displayed booking-party choice.

Example: MAIN_GUEST

Allowed values: MAIN_GUEST, SOMEONE_ELSE

Validation: Must be encoded as a JSON string.

### guest.workTravel

Type: boolean; Required: Yes; Nullable: No

Trigger: When the containing guest object or array item is supplied in the request body.

Description: Displayed work-travel choice.

Example: false

Validation: Must be encoded as the declared JSON type.

### paymentToken

Type: string; Format: opaque identifier; Required: No; Nullable: No

Trigger: When the client includes this property in the request body.

Description: Payment-provider token produced by the embedded card control.

Example: pay_tok_01JABCDEF

Validation: Must be encoded as a JSON string.

### savePaymentMethod

Type: boolean; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Save-card checkbox selection.

Example: false

Validation: Must be encoded as the declared JSON type.

## Success Response — HTTP 201

### success

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response.

Description: Indicates whether the HTTP operation completed successfully.

Example: true

Validation: Must be encoded as the declared JSON type.

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response.

Description: Human-readable operation outcome summary.

Example: Reservation confirmed. Your driver will reach out.

Validation: Must be encoded as a JSON string.

### data.id

Type: string; Format: opaque identifier; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Booking identifier.

Example: tb_01JABCDEF

Validation: Must be encoded as a JSON string.

### data.status

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Returned booking status.

Example: CONFIRMED

Allowed values: PENDING, CONFIRMED, FAILED, CANCELLED

Validation: Must be encoded as a JSON string.

### data.total

Type: money object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Booked rental price.

Example: {"amount": 300.0, "currency": "LKR"}

Validation: Must be encoded as the declared JSON type.

### data.paymentMode

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Applied payment mode.

Example: PAY_DRIVER

Allowed values: ONLINE, PAY_DRIVER

Validation: Must be encoded as a JSON string.

### data.driverContactAvailable

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Indicates whether the response includes driver follow-up data.

Example: true

Validation: Must be encoded as the declared JSON type.

### data.smsNotificationScheduled

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Indicates whether the displayed SMS continuation was scheduled.

Example: true

Validation: Must be encoded as the declared JSON type.

### data.createdAt

Type: string; Format: ISO 8601 date-time; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Booking creation timestamp.

Example: 2026-06-25T12:00:00+05:30

Validation: Must use ISO 8601 date-time syntax with an offset.

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

Example: Reservation returned.

Validation: Must be encoded as a JSON string.

### data.id

Type: string; Format: opaque identifier; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Existing booking identifier.

Example: tb_01JABCDEF

Validation: Must be encoded as a JSON string.

### data.status

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Returned booking status.

Example: CONFIRMED

Allowed values: PENDING, CONFIRMED, FAILED, CANCELLED

Validation: Must be encoded as a JSON string.

### data.total

Type: money object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Booked rental price.

Example: {"amount": 300.0, "currency": "LKR"}

Validation: Must be encoded as the declared JSON type.

### data.paymentMode

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Applied payment mode.

Example: PAY_DRIVER

Allowed values: ONLINE, PAY_DRIVER

Validation: Must be encoded as a JSON string.

### data.driverContactAvailable

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Indicates whether driver follow-up data is available.

Example: true

Validation: Must be encoded as the declared JSON type.

### data.smsNotificationScheduled

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Indicates whether the displayed SMS continuation was scheduled.

Example: true

Validation: Must be encoded as the declared JSON type.

### data.createdAt

Type: string; Format: ISO 8601 date-time; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Booking creation timestamp.

Example: 2026-06-25T12:00:00+05:30

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
Trigger: A referenced checkout resource cannot be returned.
Description: Public not-found response.
- Example message: The request could not be completed.

## Error Response — HTTP 409

- Code: CHECKOUT_CONFLICT
Trigger: The request conflicts with the current checkout state.
Description: Public checkout conflict.
- Example message: The request could not be completed.

## Error Response — HTTP 422

- Code: UNPROCESSABLE_REQUEST
Trigger: The syntactically valid request cannot be completed by a required processor.
Description: Public processing failure.
- Example message: The request could not be completed.

## Error Response — HTTP 503

- Code: SERVICE_UNAVAILABLE
Trigger: The operation cannot currently return a definitive response.
Description: Temporary booking failure.
- Example message: The request could not be completed.

## Notes

Response envelopes and money values follow the [common API contract](common-contract.md). The card fields visible in Figma belong to a payment-provider control; this API receives only its opaque token. No card number, expiry value, or CVV is accepted or stored. HTTP 201 and HTTP 200 represent new creation and an existing idempotent outcome.
