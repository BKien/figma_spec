---
artifact_type: api-contract
status: Draft
api_id: API-MY-TRIPS-LIST
related_uc_id: UC-12
---

# API-MY-TRIPS-LIST: List My Trips

## General Information

### API ID

API-MY-TRIPS-LIST

### API Name

List My Trips

### Related Use Case IDs

UC-12

### Method

GET

### Path

/api/users/me/bookings

### Description

Provides the Tripma trip-summary collection associated with the current account.

### Authentication

Required session

### Authorization

Governed by UC-12.

## Request Header(s)

### headers.Accept

Type: string; Format: MIME type
Required: No
Nullable: No
Default: application/json
Allowed values: application/json

## Path Parameter(s)

None

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

### data.upcomingTrips

Type: array
Required: Yes
Nullable: No

### data.completedTrips

Type: array
Required: Yes
Nullable: No

### data.cancelledTrips

Type: array
Required: Yes
Nullable: No

### data.upcomingTrips[] / data.completedTrips[] / data.cancelledTrips[]

Type: object
Required: Yes
Nullable: No

### data.*Trips[].bookingId

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.*Trips[].bookingStatus

Type: string; Format: enum
Required: Yes
Nullable: No
Allowed values: CONFIRMED, CANCELLED

### data.*Trips[].timingStatus

Type: string; Format: enum
Required: Yes
Nullable: No
Allowed values: UPCOMING, COMPLETED, CANCELLED

### data.*Trips[].departingFlight

Type: object
Required: Yes
Nullable: No

### data.*Trips[].returningFlight

Type: object
Required: No
Nullable: Yes

### data.*Trips[].departingFlight.flightId / data.*Trips[].returningFlight.flightId

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.*Trips[].departingFlight.fromCity / data.*Trips[].returningFlight.fromCity

Type: string
Required: Yes
Nullable: No

### data.*Trips[].departingFlight.toCity / data.*Trips[].returningFlight.toCity

Type: string
Required: Yes
Nullable: No

### data.*Trips[].departingFlight.airlineName / data.*Trips[].returningFlight.airlineName

Type: string
Required: Yes
Nullable: No

### data.*Trips[].departingFlight.duration / data.*Trips[].returningFlight.duration

Type: string
Required: Yes
Nullable: No

### data.*Trips[].departingFlight.stopsNumber / data.*Trips[].returningFlight.stopsNumber

Type: integer
Required: Yes
Nullable: No

### data.*Trips[].departingFlight.fromToTime / data.*Trips[].returningFlight.fromToTime

Type: string
Required: Yes
Nullable: No

### data.*Trips[].departingFlight.date / data.*Trips[].returningFlight.date

Type: string; Format: ISO 8601
Required: Yes
Nullable: No

### data.*Trips[].departingFlight.arrivalAt / data.*Trips[].returningFlight.arrivalAt

Type: string; Format: ISO 8601
Required: Yes
Nullable: No

### data.*Trips[].journeyEndAt

Type: string; Format: ISO 8601
Required: Yes
Nullable: No

### data.*Trips[].passengerCount

Type: integer
Required: Yes
Nullable: No

### data.*Trips[].total

Type: number
Required: Yes
Nullable: No

### data.*Trips[].currency

Type: string; Format: ISO 4217 currency code
Required: Yes
Nullable: No

### data.*Trips[].bookedAt

Type: string; Format: ISO 8601
Required: Yes
Nullable: No

## Error Response — HTTP 401

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

This contract returns the authenticated user's trip collection required by UC-12.
