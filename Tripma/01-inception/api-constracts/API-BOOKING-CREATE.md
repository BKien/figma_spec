---
artifact_type: api-contract
status: Draft
api_id: API-BOOKING-CREATE
related_uc_id: UC-05
---

# API-BOOKING-CREATE: Create Booking

## General Information

### API ID

API-BOOKING-CREATE

### API Name

Create Booking

### Related Use Case IDs

UC-05

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

Type: string; Format: MIME type
Required: Yes
Nullable: No
Default: application/json
Allowed values: application/json

### headers.Accept

Type: string; Format: MIME type
Required: No
Nullable: No
Default: application/json
Allowed values: application/json

### headers.Idempotency-Key

Type: string
Required: Yes
Nullable: No

## Path Parameter(s)

None

## Query Parameter(s)

None

## Request Body

### seatSelectionContextKey

Type: string
Required: Yes
Nullable: No

### payment

Type: object
Required: Yes
Nullable: No

### payment.paymentMethod

Type: string; Format: enum
Required: Yes
Nullable: No
Allowed values: CREDIT_CARD, GOOGLE_PAY, APPLE_PAY, PAYPAL, CRYPTO

### payment.nameOnCard

Type: string
Required: No
Nullable: Yes

### payment.cardNumber

Type: string
Required: No
Nullable: Yes

### payment.securityCode

Type: string
Required: No
Nullable: Yes

### payment.expireDate

Type: string; Format: date
Required: No
Nullable: Yes

### payment.providerToken

Type: string; Format: opaque token
Required: No
Nullable: Yes

### billingAddress

Type: object
Required: Yes
Nullable: No

### billingAddress.sameAsPrimaryPassenger

Type: boolean
Required: Yes
Nullable: No

### billingAddress.addressLine1

Type: string
Required: No
Nullable: Yes

### billingAddress.addressLine2

Type: string
Required: No
Nullable: Yes

### billingAddress.city

Type: string
Required: No
Nullable: Yes

### billingAddress.region

Type: string
Required: No
Nullable: Yes

### billingAddress.postalCode

Type: string
Required: No
Nullable: Yes

### billingAddress.country

Type: string
Required: No
Nullable: Yes

## Success Response — HTTP 201

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

### data.userId

Type: string; Format: UUID
Required: No
Nullable: Yes

### data.paymentMethod

Type: string; Format: enum
Required: Yes
Nullable: No
Allowed values: CREDIT_CARD, GOOGLE_PAY, APPLE_PAY, PAYPAL, CRYPTO

### data.paymentStatus

Type: string; Format: enum
Required: Yes
Nullable: No
Allowed values: PENDING, AUTHORIZED, DECLINED, COMPLETED, FAILED

### data.paymentAccountDisplay

Type: string
Required: No
Nullable: Yes

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

### data.departingFlight.date

Type: string; Format: ISO 8601
Required: Yes
Nullable: No

### data.departingFlight.arrivalAt

Type: string; Format: ISO 8601
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

### data.returningFlight.date

Type: string; Format: ISO 8601
Required: Yes
Nullable: No

### data.returningFlight.arrivalAt

Type: string; Format: ISO 8601
Required: Yes
Nullable: No

### data.passengers

Type: array
Required: Yes
Nullable: No

### data.passengers[].passengerRef

Type: string
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

### data.seatAssignments[].passengerRef

Type: string
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

### data.flightSubtotal

Type: number
Required: Yes
Nullable: No

### data.taxesAndFees

Type: number
Required: Yes
Nullable: No

### data.baggageFees

Type: number
Required: Yes
Nullable: No

### data.upgradeFees

Type: number
Required: Yes
Nullable: No

### data.total

Type: number
Required: Yes
Nullable: No

### data.currency

Type: string; Format: ISO 4217 currency code
Required: Yes
Nullable: No

### data.createdAt

Type: string; Format: ISO 8601
Required: Yes
Nullable: No

## Error Response — HTTP 400

### message

Type: string
Required: Yes
Nullable: No

### issues

Type: array
Required: No
Nullable: No

### issues[].field

Type: string
Required: Yes
Nullable: No

### issues[].code

Type: string
Required: Yes
Nullable: No

## Error Response — HTTP 402

### message

Type: string
Required: Yes
Nullable: No

## Error Response — HTTP 409

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

This contract consumes the flight, passenger and seat-selection context prepared by UC-02, UC-03 and UC-04. Account registration and saving a reusable payment method remain separate operations.
