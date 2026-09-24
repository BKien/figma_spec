# API-STAY-BOOKING-CREATE — Create a Stay Booking

## API ID

`API-STAY-BOOKING-CREATE`

## API Name

Stay Booking Creation

## Related Use Case IDs

- `UC-08`

## Method

`POST`

## Path

`/api/v1/stay-bookings`

## Description

Accepts checkout data and returns a stay-booking response.

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

### `Idempotency-Key`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as an HTTP header value.
- Description: Client-generated operation key.
- Example: `book-stay-7ec67a2d`

## Path Parameters

None.

## Query Parameters

None.

## Request Body

### `quoteId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Opaque quote identifier.
- Example: `sq_01JABCDEF`

### `guest.firstName`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Guest first name.
- Example: `Alex`

### `guest.lastName`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Guest last name.
- Example: `Morgan`

### `guest.homeAddress`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Home address entered at checkout.
- Example: `14 Lake Road, Colombo`

### `guest.bookingFor`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `MAIN_GUEST`, `SOMEONE_ELSE`
- Validation: Must be one of the public enum values.
- Description: Displayed booking-party choice.
- Example: `MAIN_GUEST`

### `guest.workTravel`

- Type: boolean
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON boolean.
- Description: Displayed work-travel choice.
- Example: `false`

### `guest.email`

- Type: string
- Format: email
- Required: Yes
- Nullable: No
- Validation: Must use email-address syntax.
- Description: Guest email address.
- Example: `alex@example.com`

### `guest.phone`

- Type: string
- Format: telephone number
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Guest phone number.
- Example: `+12025550123`

### `guest.countryCode`

- Type: string
- Format: country code
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Guest country code.
- Example: `US`

### `paymentToken`

- Type: string
- Format: payment-provider token
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Opaque payment reference supplied by the payment client.
- Example: `pay_tok_01JABCDEF`

### `savePaymentMethod`

- Type: boolean
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON boolean.
- Description: Save-card checkbox selection.
- Example: `false`

## Success Response — HTTP 201

### `success`

- Type: boolean
- Required: Yes
- Nullable: No
- Example: `true`

### `message`

- Type: string
- Required: Yes
- Nullable: No
- Example: `Stay booking created.`

### `data.id`

- Type: string
- Required: Yes
- Nullable: No
- Description: Booking identifier.

### `data.status`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `PENDING`, `CONFIRMED`, `FAILED`, `CANCELLED`
- Description: Booking status returned by the service.

### `data.total`

- Type: money object
- Required: Yes
- Nullable: No
- Description: Booking total.

### `data.createdAt`

- Type: string
- Format: ISO 8601 date-time
- Required: Yes
- Nullable: No
- Description: Booking creation timestamp.

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
- Example: `Stay booking returned.`

### `data.id`

- Type: string
- Required: Yes
- Nullable: No
- Description: Booking identifier.

### `data.status`

- Type: string
- Required: Yes
- Nullable: No
- Allowed values: `PENDING`, `CONFIRMED`, `FAILED`, `CANCELLED`
- Description: Booking status returned by the service.

### `data.total`

- Type: money object
- Required: Yes
- Nullable: No
- Description: Booking total.

### `data.createdAt`

- Type: string
- Format: ISO 8601 date-time
- Required: Yes
- Nullable: No
- Description: Booking creation timestamp.

## Error Response — HTTP 400

- Code: `VALIDATION_ERROR`
- Trigger: The request cannot be decoded or does not match the declared wire schema.
- Description: Protocol-level request error.
- Example message: `The request payload is invalid.`

## Error Response — HTTP 401

- Code: `UNAUTHORIZED`
- Trigger: The endpoint does not accept the supplied authentication context.
- Description: Authentication error.
- Example message: `Authentication is required.`

## Error Response — HTTP 404

- Code: `NOT_FOUND`
- Trigger: A referenced checkout resource cannot be returned.
- Description: Public not-found response.
- Example message: `The requested resource was not found.`

## Error Response — HTTP 409

- Code: `CHECKOUT_CONFLICT`
- Trigger: The request conflicts with the current checkout state.
- Description: Public checkout conflict.
- Example message: `The booking request could not be completed.`

## Error Response — HTTP 422

- Code: `UNPROCESSABLE_REQUEST`
- Trigger: The syntactically valid request cannot be completed by a required processor.
- Description: Public processing failure.
- Example message: `The booking request could not be processed.`

## Error Response — HTTP 503

- Code: `SERVICE_UNAVAILABLE`
- Trigger: The operation cannot currently return a definitive response.
- Description: Temporary booking-service failure.
- Example message: `The request could not be completed.`

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md).

The card fields visible in Figma belong to a payment-provider control; this API receives only its opaque token. No card number, expiry value, or CVV is accepted or stored. HTTP 201 and HTTP 200 use the same response schema.
