---
artifact_type: api-contract
status: Draft
api_id: API-BOOKING-CONFIRMATION-GET
related_uc_id: UC-06
---

# API-BOOKING-CONFIRMATION-GET: Get Booking Confirmation

## General Information

### API ID

API-BOOKING-CONFIRMATION-GET

### API Name

Get Booking Confirmation

### Related Use Case IDs

UC-06

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

Type: string; Format: MIME type
Required: No
Nullable: No
Default: application/json
Allowed values: application/json

### headers.X-Confirmation-Code

Type: string
Required: No
Nullable: No

## Path Parameter(s)

### path.bookingId

Type: string; Format: UUID
Required: Yes
Nullable: No

## Query Parameter(s)

None

## Request Body

None

## Success Response — HTTP 200

### success

Type: boolean
Required: Yes
Nullable: No

### message

Type: string
Required: Yes
Nullable: No

### data

Type: object
Required: Yes
Nullable: No

### data.bookingId

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.confirmationCode

Type: string
Required: Yes
Nullable: No

### data.status

Type: string; Format: enum
Required: Yes
Nullable: No
Allowed values: CONFIRMED

### data.createdAt

Type: string; Format: ISO 8601
Required: Yes
Nullable: No

### data.departingFlight

Type: object
Required: Yes
Nullable: No

### data.departingFlight.flightId

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.departingFlight.fromCity

Type: string
Required: Yes
Nullable: No

### data.departingFlight.toCity

Type: string
Required: Yes
Nullable: No

### data.departingFlight.airlineName

Type: string
Required: Yes
Nullable: No

### data.departingFlight.duration

Type: string
Required: Yes
Nullable: No

### data.departingFlight.stopsNumber

Type: integer
Required: Yes
Nullable: No

### data.departingFlight.fromToTime

Type: string
Required: Yes
Nullable: No

### data.departingFlight.date

Type: string; Format: ISO 8601
Required: Yes
Nullable: No

### data.departingFlight.arrivalAt

Type: string; Format: ISO 8601
Required: Yes
Nullable: No

### data.departingFlight.subtotalPrice

Type: number
Required: Yes
Nullable: No

### data.departingFlight.taxesAndFees

Type: number
Required: Yes
Nullable: No

### data.departingFlight.currency

Type: string; Format: ISO 4217 currency code
Required: Yes
Nullable: No

### data.returningFlight

Type: object
Required: No
Nullable: Yes

### data.returningFlight.flightId

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.returningFlight.fromCity

Type: string
Required: Yes
Nullable: No

### data.returningFlight.toCity

Type: string
Required: Yes
Nullable: No

### data.returningFlight.airlineName

Type: string
Required: Yes
Nullable: No

### data.returningFlight.duration

Type: string
Required: Yes
Nullable: No

### data.returningFlight.stopsNumber

Type: integer
Required: Yes
Nullable: No

### data.returningFlight.fromToTime

Type: string
Required: Yes
Nullable: No

### data.returningFlight.date

Type: string; Format: ISO 8601
Required: Yes
Nullable: No

### data.returningFlight.arrivalAt

Type: string; Format: ISO 8601
Required: Yes
Nullable: No

### data.returningFlight.subtotalPrice

Type: number
Required: Yes
Nullable: No

### data.returningFlight.taxesAndFees

Type: number
Required: Yes
Nullable: No

### data.returningFlight.currency

Type: string; Format: ISO 4217 currency code
Required: Yes
Nullable: No

### data.passengers

Type: array
Required: Yes
Nullable: No

### data.passengers[].passengerId

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.passengers[].firstName

Type: string
Required: Yes
Nullable: No

### data.passengers[].lastName

Type: string
Required: Yes
Nullable: No

### data.seatAssignments

Type: array
Required: Yes
Nullable: No

### data.seatAssignments[].passengerId

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.seatAssignments[].flightId

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.seatAssignments[].seatNumber

Type: string
Required: Yes
Nullable: No

### data.seatAssignments[].seatClass

Type: string; Format: enum
Required: Yes
Nullable: No
Allowed values: ECONOMY, BUSINESS

### data.baggage

Type: array
Required: Yes
Nullable: No

### data.baggage[].passengerId

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.baggage[].flightId

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.baggage[].checkedBags

Type: integer
Required: Yes
Nullable: No

### data.payment

Type: object
Required: Yes
Nullable: No

### data.payment.paymentMethod

Type: string; Format: enum
Required: Yes
Nullable: No
Allowed values: CREDIT_CARD, GOOGLE_PAY, APPLE_PAY, PAYPAL, CRYPTO

### data.payment.status

Type: string; Format: enum
Required: Yes
Nullable: No
Allowed values: COMPLETED

### data.payment.nameOnCard

Type: string
Required: No
Nullable: Yes

### data.payment.cardLastFour

Type: string
Required: No
Nullable: Yes

### data.payment.expireDate

Type: string; Format: date
Required: No
Nullable: Yes

### data.priceBreakdown

Type: object
Required: Yes
Nullable: No

### data.priceBreakdown.flightSubtotal

Type: number
Required: Yes
Nullable: No

### data.priceBreakdown.taxesAndFees

Type: number
Required: Yes
Nullable: No

### data.priceBreakdown.baggageFees

Type: number
Required: Yes
Nullable: No

### data.priceBreakdown.upgradeFees

Type: number
Required: Yes
Nullable: No

### data.priceBreakdown.total

Type: number
Required: Yes
Nullable: No

### data.priceBreakdown.currency

Type: string; Format: ISO 4217 currency code
Required: Yes
Nullable: No

## Error Response — HTTP 403

### message

Type: string
Required: Yes
Nullable: No

## Error Response — HTTP 404

### message

Type: string
Required: Yes
Nullable: No

## Error Response — HTTP 500

### message

Type: string
Required: Yes
Nullable: No

### retryable

Type: boolean
Required: Yes
Nullable: No

## Notes

This contract supplies booking-confirmation data to the booking-success page (`/successbooking`) for UC-06.
