---
artifact_type: api-contract
status: Frozen
api_id: API-BOOKING-CONFIRMATION-GET
related_uc_ids: ["UC-06", "UC-12", "UC-14"]
---

# API-BOOKING-CONFIRMATION-GET: Get Booking Confirmation

## General Information

### API ID

API-BOOKING-CONFIRMATION-GET

### API Name

Get Booking Confirmation

### Related Use Case IDs

UC-06, UC-12, UC-14

### Method

GET

### Path

/api/bookings/{bookingId}/confirmation

### Description

Provides the Tripma confirmation view associated with a submitted booking reference.

### Authentication

Optional session

### Authorization

Governed by UC-06.

## Request Header(s)

### headers.Accept

Type: string; Format: MIME type; Required: No; Nullable: No

Trigger: When the client supplies the Accept header.

Description: Requested response media type.

Example: "application/json"

Note: Identifies the requested response media type.

Default: application/json

Allowed values: application/json

### headers.X-Confirmation-Code

Type: string; Format: Opaque HTTP header value; Required: No; Nullable: No

Trigger: When the client supplies the X-Confirmation-Code header.

Description: Booking confirmation access code carried by the HTTP header.

Example: "TRP7K2"

Note: Transmit the confirmation code as a single header value.

## Path Parameter(s)

### path.bookingId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Every request using the bookingId path segment.

Description: Booking identifier.

Example: "6ca91d4e-4bc3-515b-86f9-8930c7b1a1e3"

## Query Parameter(s)

None

## Request Body

None

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

Example: "Request completed successfully."

### data

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Endpoint-specific response payload.

Example: {"bookingId": "6ca91d4e-4bc3-515b-86f9-8930c7b1a1e3", "confirmationCode": "TRP7K2", "status": "CONFIRMED", "createdAt": "2026-10-07T09:00:00Z", "departingFlight": {"flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "fromCity": "San Francisco", "toCity": "Tokyo", "airlineName": "Example Air", "duration": "11h 30m", "stopsNumber": 0, "fromToTime": "09:00 - 20:30", "date": "2026-10-10T09:00:00Z", "arrivalAt": "2026-10-10T20:30:00Z", "subtotalPrice": 250, "taxesAndFees": 25, "currency": "USD"}, "passengers": [{"passengerId": "a40c745b-93fd-5e05-9707-9f703b184285", "firstName": "Alex", "lastName": "Morgan"}], "seatAssignments": [{"passengerId": "a40c745b-93fd-5e05-9707-9f703b184285", "flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "seatNumber": "12A", "seatClass": "ECONOMY"}], "baggage": [{"passengerId": "a40c745b-93fd-5e05-9707-9f703b184285", "flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "checkedBags": 1}], "payment": {"paymentMethod": "CREDIT_CARD", "status": "COMPLETED"}, "priceBreakdown": {"flightSubtotal": 250, "taxesAndFees": 25, "baggageFees": 15, "upgradeFees": 10, "total": 300, "currency": "USD"}}

### data.bookingId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Booking identifier.

Example: "6ca91d4e-4bc3-515b-86f9-8930c7b1a1e3"

### data.confirmationCode

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Booking confirmation access code.

Example: "TRP7K2"

### data.status

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Public booking state.

Example: "CONFIRMED"

Allowed values: CONFIRMED

### data.createdAt

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Created at timestamp in the declared ISO 8601 format.

Example: "2026-10-07T09:00:00Z"

### data.departingFlight

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Outbound flight representation.

Example: {"flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "fromCity": "San Francisco", "toCity": "Tokyo", "airlineName": "Example Air", "duration": "11h 30m", "stopsNumber": 0, "fromToTime": "09:00 - 20:30", "date": "2026-10-10T09:00:00Z", "arrivalAt": "2026-10-10T20:30:00Z", "subtotalPrice": 250, "taxesAndFees": 25, "currency": "USD"}

### data.departingFlight.flightId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.departingFlight object or array item is present and non-null.

Description: Flight identifier.

Example: "955efaff-2d21-5d86-a015-541efa3d7bb5"

### data.departingFlight.fromCity

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.departingFlight object or array item is present and non-null.

Description: Departure city label.

Example: "San Francisco"

### data.departingFlight.toCity

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.departingFlight object or array item is present and non-null.

Description: Arrival city label.

Example: "Tokyo"

### data.departingFlight.airlineName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.departingFlight object or array item is present and non-null.

Description: Airline display name.

Example: "Example Air"

### data.departingFlight.duration

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.departingFlight object or array item is present and non-null.

Description: Flight duration display text.

Example: "11h 30m"

### data.departingFlight.stopsNumber

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.departingFlight object or array item is present and non-null.

Description: Reported number of flight stops.

Example: 0

### data.departingFlight.fromToTime

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.departingFlight object or array item is present and non-null.

Description: Departure and arrival time display text.

Example: "09:00 - 20:30"

### data.departingFlight.date

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.departingFlight object or array item is present and non-null.

Description: Flight departure date-time in the declared ISO 8601 format.

Example: "2026-10-10T09:00:00Z"

### data.departingFlight.arrivalAt

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.departingFlight object or array item is present and non-null.

Description: Arrival at timestamp in the declared ISO 8601 format.

Example: "2026-10-10T20:30:00Z"

### data.departingFlight.subtotalPrice

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.departingFlight object or array item is present and non-null.

Description: Reported flight subtotal in the response currency.

Example: 250

### data.departingFlight.taxesAndFees

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.departingFlight object or array item is present and non-null.

Description: Reported taxes and fees in the response currency.

Example: 25

### data.departingFlight.currency

Type: string; Format: ISO 4217 currency code; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.departingFlight object or array item is present and non-null.

Description: ISO 4217 currency code for monetary values.

Example: "USD"

### data.returningFlight

Type: object; Required: No; Nullable: Yes

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null and this optional property is returned.

Description: Return flight representation.

Example: {"flightId": "9862aa86-635a-5236-88c8-ac4e5b22147e", "fromCity": "Tokyo", "toCity": "San Francisco", "airlineName": "Example Air", "duration": "11h 30m", "stopsNumber": 0, "fromToTime": "09:00 - 20:30", "date": "2026-10-17T09:00:00Z", "arrivalAt": "2026-10-17T20:30:00Z", "subtotalPrice": 250, "taxesAndFees": 25, "currency": "USD"}

### data.returningFlight.flightId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.returningFlight object or array item is present and non-null.

Description: Flight identifier.

Example: "9862aa86-635a-5236-88c8-ac4e5b22147e"

### data.returningFlight.fromCity

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.returningFlight object or array item is present and non-null.

Description: Departure city label.

Example: "Tokyo"

### data.returningFlight.toCity

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.returningFlight object or array item is present and non-null.

Description: Arrival city label.

Example: "San Francisco"

### data.returningFlight.airlineName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.returningFlight object or array item is present and non-null.

Description: Airline display name.

Example: "Example Air"

### data.returningFlight.duration

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.returningFlight object or array item is present and non-null.

Description: Flight duration display text.

Example: "11h 30m"

### data.returningFlight.stopsNumber

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.returningFlight object or array item is present and non-null.

Description: Reported number of flight stops.

Example: 0

### data.returningFlight.fromToTime

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.returningFlight object or array item is present and non-null.

Description: Departure and arrival time display text.

Example: "09:00 - 20:30"

### data.returningFlight.date

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.returningFlight object or array item is present and non-null.

Description: Flight departure date-time in the declared ISO 8601 format.

Example: "2026-10-17T09:00:00Z"

### data.returningFlight.arrivalAt

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.returningFlight object or array item is present and non-null.

Description: Arrival at timestamp in the declared ISO 8601 format.

Example: "2026-10-17T20:30:00Z"

### data.returningFlight.subtotalPrice

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.returningFlight object or array item is present and non-null.

Description: Reported flight subtotal in the response currency.

Example: 250

### data.returningFlight.taxesAndFees

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.returningFlight object or array item is present and non-null.

Description: Reported taxes and fees in the response currency.

Example: 25

### data.returningFlight.currency

Type: string; Format: ISO 4217 currency code; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.returningFlight object or array item is present and non-null.

Description: ISO 4217 currency code for monetary values.

Example: "USD"

### data.passengers

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Passenger representations.

Example: [{"passengerId": "a40c745b-93fd-5e05-9707-9f703b184285", "firstName": "Alex", "lastName": "Morgan"}]

### data.passengers[].passengerId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.passengers[] object or array item is present and non-null.

Description: Passenger identifier.

Example: "a40c745b-93fd-5e05-9707-9f703b184285"

### data.passengers[].firstName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.passengers[] object or array item is present and non-null.

Description: Given name.

Example: "Alex"

### data.passengers[].lastName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.passengers[] object or array item is present and non-null.

Description: Family name.

Example: "Morgan"

### data.seatAssignments

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Passenger seat assignment representations.

Example: [{"passengerId": "a40c745b-93fd-5e05-9707-9f703b184285", "flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "seatNumber": "12A", "seatClass": "ECONOMY"}]

### data.seatAssignments[].passengerId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.seatAssignments[] object or array item is present and non-null.

Description: Passenger identifier.

Example: "a40c745b-93fd-5e05-9707-9f703b184285"

### data.seatAssignments[].flightId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.seatAssignments[] object or array item is present and non-null.

Description: Flight identifier.

Example: "955efaff-2d21-5d86-a015-541efa3d7bb5"

### data.seatAssignments[].seatNumber

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.seatAssignments[] object or array item is present and non-null.

Description: Seat label.

Example: "12A"

### data.seatAssignments[].seatClass

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.seatAssignments[] object or array item is present and non-null.

Description: Public cabin-class value.

Example: "ECONOMY"

Allowed values: ECONOMY, BUSINESS

### data.baggage

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Passenger baggage representations.

Example: [{"passengerId": "a40c745b-93fd-5e05-9707-9f703b184285", "flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "checkedBags": 1}]

### data.baggage[].passengerId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.baggage[] object or array item is present and non-null.

Description: Passenger identifier.

Example: "a40c745b-93fd-5e05-9707-9f703b184285"

### data.baggage[].flightId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.baggage[] object or array item is present and non-null.

Description: Flight identifier.

Example: "955efaff-2d21-5d86-a015-541efa3d7bb5"

### data.baggage[].checkedBags

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.baggage[] object or array item is present and non-null.

Description: Reported checked bag count.

Example: 1

### data.payment

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Payment representation.

Example: {"paymentMethod": "CREDIT_CARD", "status": "COMPLETED"}

### data.payment.paymentMethod

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.payment object or array item is present and non-null.

Description: Public payment method value.

Example: "CREDIT_CARD"

Allowed values: CREDIT_CARD, GOOGLE_PAY, APPLE_PAY, PAYPAL, CRYPTO

### data.payment.status

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.payment object or array item is present and non-null.

Description: Public payment state.

Example: "COMPLETED"

Allowed values: COMPLETED

### data.payment.nameOnCard

Type: string; Required: No; Nullable: Yes

Trigger: Included in the HTTP 200 success response when the containing data.payment object or array item is present and non-null and this optional property is returned.

Description: Cardholder display name.

Example: "Alex Morgan"

### data.payment.cardLastFour

Type: string; Required: No; Nullable: Yes

Trigger: Included in the HTTP 200 success response when the containing data.payment object or array item is present and non-null and this optional property is returned.

Description: Last four digits displayed for the payment card.

Example: "4242"

### data.payment.expireDate

Type: string; Format: date; Required: No; Nullable: Yes

Trigger: Included in the HTTP 200 success response when the containing data.payment object or array item is present and non-null and this optional property is returned.

Description: Payment-card expiry date in the declared wire format.

Example: "2030-12-01"

### data.priceBreakdown

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Itemized monetary response amounts.

Example: {"flightSubtotal": 250, "taxesAndFees": 25, "baggageFees": 15, "upgradeFees": 10, "total": 300, "currency": "USD"}

### data.priceBreakdown.flightSubtotal

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.priceBreakdown object or array item is present and non-null.

Description: Reported flight subtotal.

Example: 250

### data.priceBreakdown.taxesAndFees

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.priceBreakdown object or array item is present and non-null.

Description: Reported taxes and fees in the response currency.

Example: 25

### data.priceBreakdown.baggageFees

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.priceBreakdown object or array item is present and non-null.

Description: Reported baggage fees.

Example: 15

### data.priceBreakdown.upgradeFees

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.priceBreakdown object or array item is present and non-null.

Description: Reported cabin or seat upgrade fees.

Example: 10

### data.priceBreakdown.total

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.priceBreakdown object or array item is present and non-null.

Description: Reported total amount.

Example: 300

### data.priceBreakdown.currency

Type: string; Format: ISO 4217 currency code; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.priceBreakdown object or array item is present and non-null.

Description: ISO 4217 currency code for monetary values.

Example: "USD"

## Error Response — HTTP 403

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 403 error response.

Description: Public error outcome summary.

Example: "Access to this operation was not accepted."

Note: Field of the JSON error response.

## Error Response — HTTP 404

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 404 error response.

Description: Public error outcome summary.

Example: "The requested resource was not found."

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

This contract supplies booking-confirmation data to the booking-success page (/successbooking) for UC-06.
