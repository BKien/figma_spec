---
artifact_type: api-contract
status: Frozen
api_id: API-BOOKING-CREATE
related_uc_ids: ["UC-05", "UC-13"]
---

# API-BOOKING-CREATE: Create Booking

## General Information

### API ID

API-BOOKING-CREATE

### API Name

Create Booking

### Related Use Case IDs

UC-05, UC-13

### Method

POST

### Path

/api/booking

### Description

Processes a submitted Tripma checkout and returns its booking outcome.

### Authentication

Optional session

### Authorization

The current session is used when the checkout is associated with an authenticated Tripma user.

## Request Header(s)

### headers.Content-Type

Type: string; Format: MIME type; Required: Yes; Nullable: No

Trigger: Every POST request to this endpoint.

Description: Media type of the request body.

Example: "application/json"

Note: Identifies the media type of the submitted request body.

Default: application/json

Allowed values: application/json

### headers.Accept

Type: string; Format: MIME type; Required: No; Nullable: No

Trigger: When the client supplies the Accept header.

Description: Requested response media type.

Example: "application/json"

Note: Identifies the requested response media type.

Default: application/json

Allowed values: application/json

### headers.Idempotency-Key

Type: string; Format: Opaque HTTP header value; Required: Yes; Nullable: No

Trigger: Every POST request to this endpoint.

Description: Opaque command reference carried by the HTTP header.

Example: "command-example-01"

Note: Transmit the command reference as a single header value.

## Path Parameter(s)

None

## Query Parameter(s)

None

## Request Body

### seatSelectionContextKey

Type: string; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Opaque reference to the submitted seat-selection context.

Example: "seat-selection-example-01"

### payment

Type: object; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Payment representation.

Example: {"paymentMethod": "CREDIT_CARD", "nameOnCard": "Alex Morgan", "cardNumber": "4242424242424242", "securityCode": "123", "expireDate": "2030-12-01"}

### payment.paymentMethod

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: When the containing payment object or array item is supplied in the request body.

Description: Public payment method value.

Example: "CREDIT_CARD"

Allowed values: CREDIT_CARD, GOOGLE_PAY, APPLE_PAY, PAYPAL, CRYPTO

### payment.nameOnCard

Type: string; Required: No; Nullable: Yes

Trigger: When the client includes this optional property in the containing payment object or array item.

Description: Cardholder display name.

Example: "Alex Morgan"

### payment.cardNumber

Type: string; Required: No; Nullable: Yes

Trigger: When the client includes this optional property in the containing payment object or array item.

Description: Card number submitted through this declared payment field.

Example: "4242424242424242"

### payment.securityCode

Type: string; Required: No; Nullable: Yes

Trigger: When the client includes this optional property in the containing payment object or array item.

Description: Card security code submitted through this declared payment field.

Example: "123"

### payment.expireDate

Type: string; Format: date; Required: No; Nullable: Yes

Trigger: When the client includes this optional property in the containing payment object or array item.

Description: Payment-card expiry date in the declared wire format.

Example: "2030-12-01"

### payment.providerToken

Type: string; Format: opaque token; Required: No; Nullable: Yes

Trigger: When the client includes this optional property in the containing payment object or array item.

Description: Opaque payment-provider token.

Example: "provider-token-example-01"

### billingAddress

Type: object; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Submitted billing address.

Example: {"sameAsPrimaryPassenger": true}

### billingAddress.sameAsPrimaryPassenger

Type: boolean; Required: Yes; Nullable: No

Trigger: When the containing billingAddress object or array item is supplied in the request body.

Description: Client flag selecting the primary passenger address.

Example: true

### billingAddress.addressLine1

Type: string; Required: No; Nullable: Yes

Trigger: When the client includes this optional property in the containing billingAddress object or array item.

Description: First street address line.

Example: "123 Example Street"

### billingAddress.addressLine2

Type: string; Required: No; Nullable: Yes

Trigger: When the client includes this optional property in the containing billingAddress object or array item.

Description: Additional street address line.

Example: "Apartment 4"

### billingAddress.city

Type: string; Required: No; Nullable: Yes

Trigger: When the client includes this optional property in the containing billingAddress object or array item.

Description: City display label.

Example: "San Francisco"

### billingAddress.region

Type: string; Required: No; Nullable: Yes

Trigger: When the client includes this optional property in the containing billingAddress object or array item.

Description: Region or state label.

Example: "California"

### billingAddress.postalCode

Type: string; Required: No; Nullable: Yes

Trigger: When the client includes this optional property in the containing billingAddress object or array item.

Description: Postal code.

Example: "94103"

### billingAddress.country

Type: string; Required: No; Nullable: Yes

Trigger: When the client includes this optional property in the containing billingAddress object or array item.

Description: Country label.

Example: "United States"

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

Example: "Request completed successfully."

### data

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response.

Description: Endpoint-specific response payload.

Example: {"bookingId": "6ca91d4e-4bc3-515b-86f9-8930c7b1a1e3", "confirmationCode": "TRP7K2", "status": "CONFIRMED", "paymentMethod": "CREDIT_CARD", "paymentStatus": "COMPLETED", "departingFlight": {"flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "fromCity": "San Francisco", "toCity": "Tokyo", "airlineName": "Example Air", "date": "2026-10-10T09:00:00Z", "arrivalAt": "2026-10-10T20:30:00Z"}, "passengers": [{"passengerRef": "passenger_01", "firstName": "Alex", "lastName": "Morgan"}], "seatAssignments": [{"passengerRef": "passenger_01", "flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "seatNumber": "12A", "seatClass": "ECONOMY"}], "flightSubtotal": 250, "taxesAndFees": 25, "baggageFees": 15, "upgradeFees": 10, "total": 300, "currency": "USD", "createdAt": "2026-10-07T09:00:00Z"}

### data.bookingId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Booking identifier.

Example: "6ca91d4e-4bc3-515b-86f9-8930c7b1a1e3"

### data.confirmationCode

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Booking confirmation access code.

Example: "TRP7K2"

### data.status

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Public booking state.

Example: "CONFIRMED"

Allowed values: CONFIRMED

### data.userId

Type: string; Format: UUID; Required: No; Nullable: Yes

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null and this optional property is returned.

Description: User identifier.

Example: "50b4d91a-7924-59fe-8d7a-8d6f2f4ca0d4"

### data.paymentMethod

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Public payment method value.

Example: "CREDIT_CARD"

Allowed values: CREDIT_CARD, GOOGLE_PAY, APPLE_PAY, PAYPAL, CRYPTO

### data.paymentStatus

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Public payment state.

Example: "COMPLETED"

Allowed values: PENDING, AUTHORIZED, DECLINED, COMPLETED, FAILED

### data.paymentAccountDisplay

Type: string; Required: No; Nullable: Yes

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null and this optional property is returned.

Description: Payment account display summary.

Example: "Visa ending in 4242"

### data.departingFlight

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Outbound flight representation.

Example: {"flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "fromCity": "San Francisco", "toCity": "Tokyo", "airlineName": "Example Air", "date": "2026-10-10T09:00:00Z", "arrivalAt": "2026-10-10T20:30:00Z"}

### data.departingFlight.flightId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.departingFlight object or array item is present and non-null.

Description: Flight identifier.

Example: "955efaff-2d21-5d86-a015-541efa3d7bb5"

### data.departingFlight.fromCity

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.departingFlight object or array item is present and non-null.

Description: Departure city label.

Example: "San Francisco"

### data.departingFlight.toCity

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.departingFlight object or array item is present and non-null.

Description: Arrival city label.

Example: "Tokyo"

### data.departingFlight.airlineName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.departingFlight object or array item is present and non-null.

Description: Airline display name.

Example: "Example Air"

### data.departingFlight.date

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.departingFlight object or array item is present and non-null.

Description: Flight departure date-time in the declared ISO 8601 format.

Example: "2026-10-10T09:00:00Z"

### data.departingFlight.arrivalAt

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.departingFlight object or array item is present and non-null.

Description: Arrival at timestamp in the declared ISO 8601 format.

Example: "2026-10-10T20:30:00Z"

### data.returningFlight

Type: object; Required: No; Nullable: Yes

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null and this optional property is returned.

Description: Return flight representation.

Example: {"flightId": "9862aa86-635a-5236-88c8-ac4e5b22147e", "fromCity": "Tokyo", "toCity": "San Francisco", "airlineName": "Example Air", "date": "2026-10-17T09:00:00Z", "arrivalAt": "2026-10-17T20:30:00Z"}

### data.returningFlight.flightId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.returningFlight object or array item is present and non-null.

Description: Flight identifier.

Example: "9862aa86-635a-5236-88c8-ac4e5b22147e"

### data.returningFlight.fromCity

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.returningFlight object or array item is present and non-null.

Description: Departure city label.

Example: "Tokyo"

### data.returningFlight.toCity

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.returningFlight object or array item is present and non-null.

Description: Arrival city label.

Example: "San Francisco"

### data.returningFlight.airlineName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.returningFlight object or array item is present and non-null.

Description: Airline display name.

Example: "Example Air"

### data.returningFlight.date

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.returningFlight object or array item is present and non-null.

Description: Flight departure date-time in the declared ISO 8601 format.

Example: "2026-10-17T09:00:00Z"

### data.returningFlight.arrivalAt

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.returningFlight object or array item is present and non-null.

Description: Arrival at timestamp in the declared ISO 8601 format.

Example: "2026-10-17T20:30:00Z"

### data.passengers

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Passenger representations.

Example: [{"passengerRef": "passenger_01", "firstName": "Alex", "lastName": "Morgan"}]

### data.passengers[].passengerRef

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.passengers[] object or array item is present and non-null.

Description: Client passenger reference.

Example: "passenger_01"

### data.passengers[].firstName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.passengers[] object or array item is present and non-null.

Description: Given name.

Example: "Alex"

### data.passengers[].lastName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.passengers[] object or array item is present and non-null.

Description: Family name.

Example: "Morgan"

### data.seatAssignments

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Passenger seat assignment representations.

Example: [{"passengerRef": "passenger_01", "flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "seatNumber": "12A", "seatClass": "ECONOMY"}]

### data.seatAssignments[].passengerRef

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.seatAssignments[] object or array item is present and non-null.

Description: Client passenger reference.

Example: "passenger_01"

### data.seatAssignments[].flightId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.seatAssignments[] object or array item is present and non-null.

Description: Flight identifier.

Example: "955efaff-2d21-5d86-a015-541efa3d7bb5"

### data.seatAssignments[].seatNumber

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.seatAssignments[] object or array item is present and non-null.

Description: Seat label.

Example: "12A"

### data.seatAssignments[].seatClass

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.seatAssignments[] object or array item is present and non-null.

Description: Public cabin-class value.

Example: "ECONOMY"

Allowed values: ECONOMY, BUSINESS

### data.flightSubtotal

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Reported flight subtotal.

Example: 250

### data.taxesAndFees

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Reported taxes and fees in the response currency.

Example: 25

### data.baggageFees

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Reported baggage fees.

Example: 15

### data.upgradeFees

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Reported cabin or seat upgrade fees.

Example: 10

### data.total

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Reported total amount.

Example: 300

### data.currency

Type: string; Format: ISO 4217 currency code; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: ISO 4217 currency code for monetary values.

Example: "USD"

### data.createdAt

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Created at timestamp in the declared ISO 8601 format.

Example: "2026-10-07T09:00:00Z"

## Error Response — HTTP 400

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 400 error response.

Description: Public error outcome summary.

Example: "The request does not match the declared wire schema."

Note: Field of the JSON error response.

### issues

Type: array; Required: No; Nullable: No

Trigger: Included in the HTTP 400 error response when this optional field is returned.

Description: Optional array of protocol-level field issues.

Example: [{"field": "request", "code": "INVALID_FORMAT"}]

Note: Field of the JSON error response.

### issues[].field

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 400 error response when the containing issues[] object or array item is present and non-null.

Description: Request field path associated with this issue.

Example: "request"

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

### issues[].code

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 400 error response when the containing issues[] object or array item is present and non-null.

Description: Public machine-readable outcome or issue code.

Example: "INVALID_FORMAT"

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

## Error Response — HTTP 402

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 402 error response.

Description: Public error outcome summary.

Example: "Request completed successfully."

Note: Field of the JSON error response.

## Error Response — HTTP 409

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 409 error response.

Description: Public error outcome summary.

Example: "The request conflicts with the current operation."

Note: Field of the JSON error response.

## Error Response — HTTP 500

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 500 error response.

Description: Public error outcome summary.

Example: "An unexpected server error occurred."

Note: Field of the JSON error response.

### retryable

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 500 error response.

Description: Indicates whether the public response suggests retrying the request.

Example: false

Note: Field of the JSON error response.

## Notes

This contract consumes the flight, passenger and seat-selection context prepared by UC-02, UC-03 and UC-04. Account registration and saving a reusable payment method remain separate operations.
