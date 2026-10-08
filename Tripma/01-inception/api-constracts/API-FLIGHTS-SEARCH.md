---
artifact_type: api-contract
status: Frozen
api_id: API-FLIGHTS-SEARCH
related_uc_id: UC-01
---

# API-FLIGHTS-SEARCH: Search Flights

## General Information

### API ID

API-FLIGHTS-SEARCH

### API Name

Search Flights

### Related Use Case IDs

UC-01

### Method

GET

### Path

/api/flights

### Description

Provides Tripma flight-search data for a submitted travel-search request.

### Authentication

Public

### Authorization

None

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

None.

## Query Parameter(s)

### query.fromCity

Type: string; Required: Yes; Nullable: No

Trigger: Every request includes the fromCity query parameter.

Description: Departure city label.

Example: "San Francisco"

### query.toCity

Type: string; Required: Yes; Nullable: No

Trigger: Every request includes the toCity query parameter.

Description: Arrival city label.

Example: "Tokyo"

### query.startDate

Type: string; Format: date; Required: Yes; Nullable: No

Trigger: Every request includes the startDate query parameter.

Description: Submitted outbound travel date.

Example: "2026-10-10"

### query.endDate

Type: string; Format: date; Required: No; Nullable: No

Trigger: When the client supplies the endDate query parameter.

Description: Submitted return travel date.

Example: "2026-10-17"

### query.type

Type: boolean; Required: Yes; Nullable: No

Trigger: Every request includes the type query parameter.

Description: Trip-type flag: true denotes round-trip and false denotes one-way.

Example: true

### query.adults

Type: integer; Required: Yes; Nullable: No

Trigger: Every request includes the adults query parameter.

Description: Submitted adult passenger count.

Example: 1

### query.minors

Type: integer; Required: Yes; Nullable: No

Trigger: Every request includes the minors query parameter.

Description: Submitted minor passenger count.

Example: 0

## Request Body

None

## Success Response — HTTP 200

### currency

Type: string; Format: ISO 4217 currency code; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: ISO 4217 currency code for monetary values.

Example: "USD"

### departingFlights

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Outbound flight results.

Example: [{"flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "fromCity": "San Francisco", "toCity": "Tokyo", "type": true, "imagePath": "https://example.com/images/travel.jpg", "subtotalPrice": 250, "taxesAndFees": 25, "airlineName": "Example Air", "duration": "11h 30m", "fromToTime": "09:00 - 20:30", "date": "2026-10-10T09:00:00Z", "arrivalAt": "2026-10-10T20:30:00Z", "availableSeats": 24, "availableSeatClasses": ["ECONOMY"], "stopsNumber": 0, "stopsInfo": "Nonstop"}]

### departingFlights[].flightId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing departingFlights[] object or array item is present and non-null.

Description: Flight identifier.

Example: "955efaff-2d21-5d86-a015-541efa3d7bb5"

### departingFlights[].fromCity

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing departingFlights[] object or array item is present and non-null.

Description: Departure city label.

Example: "San Francisco"

### departingFlights[].toCity

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing departingFlights[] object or array item is present and non-null.

Description: Arrival city label.

Example: "Tokyo"

### departingFlights[].type

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing departingFlights[] object or array item is present and non-null.

Description: Trip-type flag: true denotes round-trip and false denotes one-way.

Example: true

### departingFlights[].imagePath

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing departingFlights[] object or array item is present and non-null.

Description: Image URI or path.

Example: "https://example.com/images/travel.jpg"

### departingFlights[].subtotalPrice

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing departingFlights[] object or array item is present and non-null.

Description: Reported flight subtotal in the response currency.

Example: 250

### departingFlights[].taxesAndFees

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing departingFlights[] object or array item is present and non-null.

Description: Reported taxes and fees in the response currency.

Example: 25

### departingFlights[].airlineName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing departingFlights[] object or array item is present and non-null.

Description: Airline display name.

Example: "Example Air"

### departingFlights[].duration

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing departingFlights[] object or array item is present and non-null.

Description: Flight duration display text.

Example: "11h 30m"

### departingFlights[].fromToTime

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing departingFlights[] object or array item is present and non-null.

Description: Departure and arrival time display text.

Example: "09:00 - 20:30"

### departingFlights[].date

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing departingFlights[] object or array item is present and non-null.

Description: Flight departure date-time in the declared ISO 8601 format.

Example: "2026-10-10T09:00:00Z"

### departingFlights[].arrivalAt

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing departingFlights[] object or array item is present and non-null.

Description: Arrival at timestamp in the declared ISO 8601 format.

Example: "2026-10-10T20:30:00Z"

### departingFlights[].availableSeats

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing departingFlights[] object or array item is present and non-null.

Description: Reported available seat count.

Example: 24

### departingFlights[].availableSeatClasses

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing departingFlights[] object or array item is present and non-null.

Description: Reported public cabin-class values.

Example: ["ECONOMY"]

Allowed values: ECONOMY, BUSINESS

### departingFlights[].stopsNumber

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing departingFlights[] object or array item is present and non-null.

Description: Reported number of flight stops.

Example: 0

### departingFlights[].stopsInfo

Type: string; Required: Yes; Nullable: Yes

Trigger: Included in the HTTP 200 success response when the containing departingFlights[] object or array item is present and non-null.

Description: Flight stop display summary.

Example: "Nonstop"

### arrivingFlights

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Return flight results.

Example: [{"flightId": "9862aa86-635a-5236-88c8-ac4e5b22147e", "fromCity": "Tokyo", "toCity": "San Francisco", "type": true, "imagePath": "https://example.com/images/travel.jpg", "subtotalPrice": 250, "taxesAndFees": 25, "airlineName": "Example Air", "duration": "11h 30m", "fromToTime": "09:00 - 20:30", "date": "2026-10-17T09:00:00Z", "arrivalAt": "2026-10-17T20:30:00Z", "availableSeats": 24, "availableSeatClasses": ["ECONOMY"], "stopsNumber": 0, "stopsInfo": "Nonstop"}]

### arrivingFlights[].flightId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing arrivingFlights[] object or array item is present and non-null.

Description: Flight identifier.

Example: "9862aa86-635a-5236-88c8-ac4e5b22147e"

### arrivingFlights[].fromCity

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing arrivingFlights[] object or array item is present and non-null.

Description: Departure city label.

Example: "Tokyo"

### arrivingFlights[].toCity

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing arrivingFlights[] object or array item is present and non-null.

Description: Arrival city label.

Example: "San Francisco"

### arrivingFlights[].type

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing arrivingFlights[] object or array item is present and non-null.

Description: Trip-type flag: true denotes round-trip and false denotes one-way.

Example: true

### arrivingFlights[].imagePath

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing arrivingFlights[] object or array item is present and non-null.

Description: Image URI or path.

Example: "https://example.com/images/travel.jpg"

### arrivingFlights[].subtotalPrice

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing arrivingFlights[] object or array item is present and non-null.

Description: Reported flight subtotal in the response currency.

Example: 250

### arrivingFlights[].taxesAndFees

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing arrivingFlights[] object or array item is present and non-null.

Description: Reported taxes and fees in the response currency.

Example: 25

### arrivingFlights[].airlineName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing arrivingFlights[] object or array item is present and non-null.

Description: Airline display name.

Example: "Example Air"

### arrivingFlights[].duration

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing arrivingFlights[] object or array item is present and non-null.

Description: Flight duration display text.

Example: "11h 30m"

### arrivingFlights[].fromToTime

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing arrivingFlights[] object or array item is present and non-null.

Description: Departure and arrival time display text.

Example: "09:00 - 20:30"

### arrivingFlights[].date

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing arrivingFlights[] object or array item is present and non-null.

Description: Flight departure date-time in the declared ISO 8601 format.

Example: "2026-10-17T09:00:00Z"

### arrivingFlights[].arrivalAt

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing arrivingFlights[] object or array item is present and non-null.

Description: Arrival at timestamp in the declared ISO 8601 format.

Example: "2026-10-17T20:30:00Z"

### arrivingFlights[].availableSeats

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing arrivingFlights[] object or array item is present and non-null.

Description: Reported available seat count.

Example: 24

### arrivingFlights[].availableSeatClasses

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing arrivingFlights[] object or array item is present and non-null.

Description: Reported public cabin-class values.

Example: ["ECONOMY"]

Allowed values: ECONOMY, BUSINESS

### arrivingFlights[].stopsNumber

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing arrivingFlights[] object or array item is present and non-null.

Description: Reported number of flight stops.

Example: 0

### arrivingFlights[].stopsInfo

Type: string; Required: Yes; Nullable: Yes

Trigger: Included in the HTTP 200 success response when the containing arrivingFlights[] object or array item is present and non-null.

Description: Flight stop display summary.

Example: "Nonstop"

### priceGrid

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Price points for travel-date combinations.

Example: [{"departingDate": "2026-10-10", "minPrice": 280}]

### priceGrid[].departingDate

Type: string; Format: date; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing priceGrid[] object or array item is present and non-null.

Description: Outbound date for this price point.

Example: "2026-10-10"

### priceGrid[].returningDate

Type: string; Format: date; Required: No; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing priceGrid[] object or array item is present and non-null and this optional property is returned.

Description: Return date for this price point.

Example: "2026-10-17"

### priceGrid[].minPrice

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing priceGrid[] object or array item is present and non-null.

Description: Reported lowest amount for this price point.

Example: 280

### priceHistory

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Historical price point representations.

Example: [{"recordedDate": "2026-10-10", "averagePrice": 320}]

### priceHistory[].recordedDate

Type: string; Format: date; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing priceHistory[] object or array item is present and non-null.

Description: Date represented by this historical price point.

Example: "2026-10-10"

### priceHistory[].averagePrice

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing priceHistory[] object or array item is present and non-null.

Description: Reported average price.

Example: 320

### priceRating

Type: object; Required: No; Nullable: No

Trigger: Included in the HTTP 200 success response when this optional field is returned.

Description: Public price trend summary.

Example: {"averagePrice": 320, "projectedPrice": 300, "projectedChangePercent": -6.25, "recommendation": "BUY_SOON"}

### priceRating.averagePrice

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing priceRating object or array item is present and non-null.

Description: Reported average price.

Example: 320

### priceRating.projectedPrice

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing priceRating object or array item is present and non-null.

Description: Reported projected price.

Example: 300

### priceRating.projectedChangePercent

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing priceRating object or array item is present and non-null.

Description: Reported projected percentage change.

Example: -6.25

### priceRating.recommendation

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing priceRating object or array item is present and non-null.

Description: Public recommendation value.

Example: "BUY_SOON"

Allowed values: BUY_SOON, WAIT

## Error Response — HTTP 400

### message

Type: string | string[]; Required: Yes; Nullable: No

Trigger: Included in the HTTP 400 error response.

Description: Public error outcome summary.

Example: "The request does not match the declared wire schema."

Note: The response should use standard error envelopes if configured in the global exception filter.

## Error Response — HTTP 500

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 500 error response.

Description: Public error outcome summary.

Example: "An unexpected server error occurred."

Note: The response should use standard error envelopes if configured in the global exception filter.
