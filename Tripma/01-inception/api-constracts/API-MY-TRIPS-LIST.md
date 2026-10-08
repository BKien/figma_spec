---
artifact_type: api-contract
status: Frozen
api_id: API-MY-TRIPS-LIST
related_uc_ids: ["UC-12", "UC-14"]
---

# API-MY-TRIPS-LIST: List My Trips

## General Information

### API ID

API-MY-TRIPS-LIST

### API Name

List My Trips

### Related Use Case IDs

UC-12, UC-14

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

Type: string; Format: MIME type; Required: No; Nullable: No

Trigger: When the client supplies the Accept header.

Description: Requested response media type.

Example: "application/json"

Note: Identifies the requested response media type.

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

Example: {"upcomingTrips": [{"bookingId": "6ca91d4e-4bc3-515b-86f9-8930c7b1a1e3", "bookingStatus": "CONFIRMED", "timingStatus": "UPCOMING", "departingFlight": {"flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "fromCity": "San Francisco", "toCity": "Tokyo", "airlineName": "Example Air", "duration": "11h 30m", "stopsNumber": 0, "fromToTime": "09:00 - 20:30", "date": "2026-10-10T09:00:00Z", "arrivalAt": "2026-10-10T20:30:00Z"}, "journeyEndAt": "2026-10-10T20:30:00Z", "passengerCount": 1, "total": 300, "currency": "USD", "bookedAt": "2026-10-07T09:00:00Z"}], "completedTrips": [{"bookingId": "1b626472-801a-5908-b1a2-088ecd59d1aa", "bookingStatus": "CONFIRMED", "timingStatus": "COMPLETED", "departingFlight": {"flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "fromCity": "San Francisco", "toCity": "Tokyo", "airlineName": "Example Air", "duration": "11h 30m", "stopsNumber": 0, "fromToTime": "09:00 - 20:30", "date": "2026-09-10T09:00:00Z", "arrivalAt": "2026-09-10T20:30:00Z"}, "journeyEndAt": "2026-09-10T20:30:00Z", "passengerCount": 1, "total": 300, "currency": "USD", "bookedAt": "2026-09-01T09:00:00Z"}], "cancelledTrips": [{"bookingId": "265655f7-5768-57e5-bd14-d10fb19d75ce", "bookingStatus": "CANCELLED", "timingStatus": "CANCELLED", "departingFlight": {"flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "fromCity": "San Francisco", "toCity": "Tokyo", "airlineName": "Example Air", "duration": "11h 30m", "stopsNumber": 0, "fromToTime": "09:00 - 20:30", "date": "2026-10-10T09:00:00Z", "arrivalAt": "2026-10-10T20:30:00Z"}, "journeyEndAt": "2026-10-10T20:30:00Z", "passengerCount": 1, "total": 300, "currency": "USD", "bookedAt": "2026-10-07T09:00:00Z"}]}

### data.upcomingTrips

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Upcoming trip representations.

Example: [{"bookingId": "6ca91d4e-4bc3-515b-86f9-8930c7b1a1e3", "bookingStatus": "CONFIRMED", "timingStatus": "UPCOMING", "departingFlight": {"flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "fromCity": "San Francisco", "toCity": "Tokyo", "airlineName": "Example Air", "duration": "11h 30m", "stopsNumber": 0, "fromToTime": "09:00 - 20:30", "date": "2026-10-10T09:00:00Z", "arrivalAt": "2026-10-10T20:30:00Z"}, "journeyEndAt": "2026-10-10T20:30:00Z", "passengerCount": 1, "total": 300, "currency": "USD", "bookedAt": "2026-10-07T09:00:00Z"}]

### data.completedTrips

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Completed trip representations.

Example: [{"bookingId": "1b626472-801a-5908-b1a2-088ecd59d1aa", "bookingStatus": "CONFIRMED", "timingStatus": "COMPLETED", "departingFlight": {"flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "fromCity": "San Francisco", "toCity": "Tokyo", "airlineName": "Example Air", "duration": "11h 30m", "stopsNumber": 0, "fromToTime": "09:00 - 20:30", "date": "2026-09-10T09:00:00Z", "arrivalAt": "2026-09-10T20:30:00Z"}, "journeyEndAt": "2026-09-10T20:30:00Z", "passengerCount": 1, "total": 300, "currency": "USD", "bookedAt": "2026-09-01T09:00:00Z"}]

### data.cancelledTrips

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Cancelled trip representations.

Example: [{"bookingId": "265655f7-5768-57e5-bd14-d10fb19d75ce", "bookingStatus": "CANCELLED", "timingStatus": "CANCELLED", "departingFlight": {"flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "fromCity": "San Francisco", "toCity": "Tokyo", "airlineName": "Example Air", "duration": "11h 30m", "stopsNumber": 0, "fromToTime": "09:00 - 20:30", "date": "2026-10-10T09:00:00Z", "arrivalAt": "2026-10-10T20:30:00Z"}, "journeyEndAt": "2026-10-10T20:30:00Z", "passengerCount": 1, "total": 300, "currency": "USD", "bookedAt": "2026-10-07T09:00:00Z"}]

### data.upcomingTrips[] / data.completedTrips[] / data.cancelledTrips[]

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Upcoming trip representations.

Example: {"bookingId": "6ca91d4e-4bc3-515b-86f9-8930c7b1a1e3", "bookingStatus": "CONFIRMED", "timingStatus": "UPCOMING", "departingFlight": {"flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "fromCity": "San Francisco", "toCity": "Tokyo", "airlineName": "Example Air", "duration": "11h 30m", "stopsNumber": 0, "fromToTime": "09:00 - 20:30", "date": "2026-10-10T09:00:00Z", "arrivalAt": "2026-10-10T20:30:00Z"}, "journeyEndAt": "2026-10-10T20:30:00Z", "passengerCount": 1, "total": 300, "currency": "USD", "bookedAt": "2026-10-07T09:00:00Z"}

### data.*Trips[].bookingId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.*Trips[] object or array item is present and non-null.

Description: Booking identifier.

Example: "6ca91d4e-4bc3-515b-86f9-8930c7b1a1e3"

### data.*Trips[].bookingStatus

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.*Trips[] object or array item is present and non-null.

Description: Public booking state.

Example: "CONFIRMED"

Allowed values: CONFIRMED, CANCELLED

### data.*Trips[].timingStatus

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.*Trips[] object or array item is present and non-null.

Description: Public trip timing classification.

Example: "UPCOMING"

Allowed values: UPCOMING, COMPLETED, CANCELLED

### data.*Trips[].departingFlight

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.*Trips[] object or array item is present and non-null.

Description: Outbound flight representation.

Example: {"flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "fromCity": "San Francisco", "toCity": "Tokyo", "airlineName": "Example Air", "duration": "11h 30m", "stopsNumber": 0, "fromToTime": "09:00 - 20:30", "date": "2026-10-10T09:00:00Z", "arrivalAt": "2026-10-10T20:30:00Z"}

### data.*Trips[].returningFlight

Type: object; Required: No; Nullable: Yes

Trigger: Included in the HTTP 200 success response when the containing data.*Trips[] object or array item is present and non-null and this optional property is returned.

Description: Return flight representation.

Example: {"flightId": "9862aa86-635a-5236-88c8-ac4e5b22147e", "fromCity": "Tokyo", "toCity": "San Francisco", "airlineName": "Example Air", "duration": "11h 30m", "stopsNumber": 0, "fromToTime": "09:00 - 20:30", "date": "2026-10-17T09:00:00Z", "arrivalAt": "2026-10-17T20:30:00Z"}

### data.*Trips[].departingFlight.flightId / data.*Trips[].returningFlight.flightId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.*Trips[].departingFlight object or array item is present and non-null.

Description: Flight identifier.

Example: "955efaff-2d21-5d86-a015-541efa3d7bb5"

### data.*Trips[].departingFlight.fromCity / data.*Trips[].returningFlight.fromCity

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.*Trips[].departingFlight object or array item is present and non-null.

Description: Departure city label.

Example: "San Francisco"

### data.*Trips[].departingFlight.toCity / data.*Trips[].returningFlight.toCity

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.*Trips[].departingFlight object or array item is present and non-null.

Description: Arrival city label.

Example: "Tokyo"

### data.*Trips[].departingFlight.airlineName / data.*Trips[].returningFlight.airlineName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.*Trips[].departingFlight object or array item is present and non-null.

Description: Airline display name.

Example: "Example Air"

### data.*Trips[].departingFlight.duration / data.*Trips[].returningFlight.duration

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.*Trips[].departingFlight object or array item is present and non-null.

Description: Flight duration display text.

Example: "11h 30m"

### data.*Trips[].departingFlight.stopsNumber / data.*Trips[].returningFlight.stopsNumber

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.*Trips[].departingFlight object or array item is present and non-null.

Description: Reported number of flight stops.

Example: 0

### data.*Trips[].departingFlight.fromToTime / data.*Trips[].returningFlight.fromToTime

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.*Trips[].departingFlight object or array item is present and non-null.

Description: Departure and arrival time display text.

Example: "09:00 - 20:30"

### data.*Trips[].departingFlight.date / data.*Trips[].returningFlight.date

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.*Trips[].departingFlight object or array item is present and non-null.

Description: Flight departure date-time in the declared ISO 8601 format.

Example: "2026-10-10T09:00:00Z"

### data.*Trips[].departingFlight.arrivalAt / data.*Trips[].returningFlight.arrivalAt

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.*Trips[].departingFlight object or array item is present and non-null.

Description: Arrival at timestamp in the declared ISO 8601 format.

Example: "2026-10-10T20:30:00Z"

### data.*Trips[].journeyEndAt

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.*Trips[] object or array item is present and non-null.

Description: Journey end at timestamp in the declared ISO 8601 format.

Example: "2026-10-10T20:30:00Z"

### data.*Trips[].passengerCount

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.*Trips[] object or array item is present and non-null.

Description: Reported passenger count.

Example: 1

### data.*Trips[].total

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.*Trips[] object or array item is present and non-null.

Description: Reported total amount.

Example: 300

### data.*Trips[].currency

Type: string; Format: ISO 4217 currency code; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.*Trips[] object or array item is present and non-null.

Description: ISO 4217 currency code for monetary values.

Example: "USD"

### data.*Trips[].bookedAt

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.*Trips[] object or array item is present and non-null.

Description: Booked at timestamp in the declared ISO 8601 format.

Example: "2026-10-07T09:00:00Z"

## Error Response — HTTP 401

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 401 error response.

Description: Public error outcome summary.

Example: "Authentication was not accepted."

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

This contract returns the authenticated user's trip collection required by UC-12.
