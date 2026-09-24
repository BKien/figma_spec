# API-TAXI-BOOKING-CREATE — Create a Taxi Rental Booking

## API ID

`API-TAXI-BOOKING-CREATE`

## API Name

Taxi Rental Booking Creation

## Related Use Case IDs

- `UC-13`

## Method

`POST`

## Path

`/api/v1/taxi-bookings`

## Description

Accepts the Taxi reservation form and returns the driver-follow-up booking outcome.

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

### `Idempotency-Key`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Client-generated operation key.
- Example: `book-taxi-7ec67a2d`

## Path Parameters

None.

## Query Parameters

None.

## Request Body

### `quoteId`

- Type: string
- Format: opaque identifier
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Checkout quote identifier.
- Example: `tq_01JABCDEF`
### `guest.firstName`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: First name entered at checkout.
- Example: `Alex`
### `guest.lastName`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Last name entered at checkout.
- Example: `Morgan`
### `guest.homeAddress`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Home address entered at checkout.
- Example: `14 Lake Road, Colombo`
### `guest.email`

- Type: string
- Format: email
- Required: Yes
- Nullable: No
- Validation: Must use email-address syntax.
- Description: Confirmation email address.
- Example: `alex@example.com`
### `guest.countryCode`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Country or region code selected at checkout.
- Example: `LK`
### `guest.phone`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Telephone number entered at checkout.
- Example: `+94771234567`
### `guest.bookingFor`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `MAIN_GUEST`, `SOMEONE_ELSE`
- Validation: Must be encoded as a JSON string.
- Description: Displayed booking-party choice.
- Example: `MAIN_GUEST`
### `guest.workTravel`

- Type: boolean
- Required: Yes
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Displayed work-travel choice.
- Example: `false`
### `paymentToken`

- Type: string
- Format: opaque identifier
- Required: No
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Payment-provider token produced by the embedded card control.
- Example: `pay_tok_01JABCDEF`
### `savePaymentMethod`

- Type: boolean
- Required: Yes
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Save-card checkbox selection.
- Example: `false`

## Success Response — HTTP 201

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
- Example: `Reservation confirmed. Your driver will reach out.`

### `data.id`

- Type: string
- Format: opaque identifier
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Booking identifier.
- Example: `tb_01JABCDEF`

### `data.status`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `PENDING`, `CONFIRMED`, `FAILED`, `CANCELLED`
- Validation: Must be encoded as a JSON string.
- Description: Returned booking status.
- Example: `CONFIRMED`

### `data.total`

- Type: money object
- Required: Yes
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Booked rental price.

### `data.paymentMode`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `ONLINE`, `PAY_DRIVER`
- Validation: Must be encoded as a JSON string.
- Description: Applied payment mode.
- Example: `PAY_DRIVER`

### `data.driverContactAvailable`

- Type: boolean
- Required: Yes
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Indicates whether the response includes driver follow-up data.
- Example: `true`

### `data.smsNotificationScheduled`

- Type: boolean
- Required: Yes
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Indicates whether the displayed SMS continuation was scheduled.
- Example: `true`

### `data.createdAt`

- Type: string
- Format: ISO 8601 date-time
- Required: Yes
- Nullable: No
- Validation: Must use ISO 8601 date-time syntax with an offset.
- Description: Booking creation timestamp.
- Example: `2026-06-25T12:00:00+05:30`

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
- Example: `Reservation returned.`

### `data.id`

- Type: string
- Format: opaque identifier
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Existing booking identifier.
- Example: `tb_01JABCDEF`

### `data.status`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `PENDING`, `CONFIRMED`, `FAILED`, `CANCELLED`
- Validation: Must be encoded as a JSON string.
- Description: Returned booking status.
- Example: `CONFIRMED`

### `data.total`

- Type: money object
- Required: Yes
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Booked rental price.

### `data.paymentMode`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `ONLINE`, `PAY_DRIVER`
- Validation: Must be encoded as a JSON string.
- Description: Applied payment mode.
- Example: `PAY_DRIVER`

### `data.driverContactAvailable`

- Type: boolean
- Required: Yes
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Indicates whether driver follow-up data is available.
- Example: `true`

### `data.smsNotificationScheduled`

- Type: boolean
- Required: Yes
- Nullable: No
- Validation: Must be encoded as the declared JSON type.
- Description: Indicates whether the displayed SMS continuation was scheduled.
- Example: `true`

### `data.createdAt`

- Type: string
- Format: ISO 8601 date-time
- Required: Yes
- Nullable: No
- Validation: Must use ISO 8601 date-time syntax with an offset.
- Description: Booking creation timestamp.
- Example: `2026-06-25T12:00:00+05:30`

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
- Trigger: A referenced checkout resource cannot be returned.
- Description: Public not-found response.
- Example message: `The request could not be completed.`

## Error Response — HTTP 409

- Code: `CHECKOUT_CONFLICT`
- Trigger: The request conflicts with the current checkout state.
- Description: Public checkout conflict.
- Example message: `The request could not be completed.`

## Error Response — HTTP 422

- Code: `UNPROCESSABLE_REQUEST`
- Trigger: The syntactically valid request cannot be completed by a required processor.
- Description: Public processing failure.
- Example message: `The request could not be completed.`

## Error Response — HTTP 503

- Code: `SERVICE_UNAVAILABLE`
- Trigger: The operation cannot currently return a definitive response.
- Description: Temporary booking failure.
- Example message: `The request could not be completed.`

## Notes

Response envelopes and money values follow the [common API contract](common-contract.md). The card fields visible in Figma belong to a payment-provider control; this API receives only its opaque token. No card number, expiry value, or CVV is accepted or stored. HTTP 201 and HTTP 200 represent new creation and an existing idempotent outcome.
