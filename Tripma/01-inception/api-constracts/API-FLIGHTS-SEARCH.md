---
artifact_type: api-contract
status: Draft
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
Default: application/json
Allowed values: application/json

## Query Parameter(s)

### query.fromCity
Type: string; Required: Yes; Nullable: No

### query.toCity
Type: string; Required: Yes; Nullable: No

### query.startDate
Type: string; Format: date; Required: Yes; Nullable: No

### query.endDate
Type: string; Format: date; Required: No; Nullable: No

### query.type
Type: boolean; Required: Yes; Nullable: No

### query.adults
Type: integer; Required: Yes; Nullable: No

### query.minors
Type: integer; Required: Yes; Nullable: No

## Request Body

None

## Success Response — HTTP 200

### currency
Type: string; Format: ISO 4217 currency code
Required: Yes
Nullable: No

### departingFlights
Type: array
Required: Yes
Nullable: No

### departingFlights[].flightId
Type: string; Format: UUID
Required: Yes
Nullable: No

### departingFlights[].fromCity
Type: string
Required: Yes
Nullable: No

### departingFlights[].toCity
Type: string
Required: Yes
Nullable: No

### departingFlights[].type
Type: boolean
Required: Yes
Nullable: No

### departingFlights[].imagePath
Type: string
Required: Yes
Nullable: No

### departingFlights[].subtotalPrice
Type: number
Required: Yes
Nullable: No

### departingFlights[].taxesAndFees
Type: number
Required: Yes
Nullable: No

### departingFlights[].airlineName
Type: string
Required: Yes
Nullable: No

### departingFlights[].duration
Type: string
Required: Yes
Nullable: No

### departingFlights[].fromToTime
Type: string
Required: Yes
Nullable: No

### departingFlights[].date
Type: string; Format: ISO 8601
Required: Yes
Nullable: No

### departingFlights[].arrivalAt
Type: string; Format: ISO 8601
Required: Yes
Nullable: No

### departingFlights[].availableSeats
Type: integer
Required: Yes
Nullable: No

### departingFlights[].availableSeatClasses
Type: array
Required: Yes
Nullable: No
Allowed values: ECONOMY, BUSINESS

### departingFlights[].stopsNumber
Type: integer
Required: Yes
Nullable: No

### departingFlights[].stopsInfo
Type: string
Required: Yes
Nullable: Yes

### arrivingFlights
Type: array
Required: Yes
Nullable: No

### arrivingFlights[].flightId
Type: string; Format: UUID
Required: Yes
Nullable: No

### arrivingFlights[].fromCity
Type: string
Required: Yes
Nullable: No

### arrivingFlights[].toCity
Type: string
Required: Yes
Nullable: No

### arrivingFlights[].type
Type: boolean
Required: Yes
Nullable: No

### arrivingFlights[].imagePath
Type: string
Required: Yes
Nullable: No

### arrivingFlights[].subtotalPrice
Type: number
Required: Yes
Nullable: No

### arrivingFlights[].taxesAndFees
Type: number
Required: Yes
Nullable: No

### arrivingFlights[].airlineName
Type: string
Required: Yes
Nullable: No

### arrivingFlights[].duration
Type: string
Required: Yes
Nullable: No

### arrivingFlights[].fromToTime
Type: string
Required: Yes
Nullable: No

### arrivingFlights[].date
Type: string; Format: ISO 8601
Required: Yes
Nullable: No

### arrivingFlights[].arrivalAt
Type: string; Format: ISO 8601
Required: Yes
Nullable: No

### arrivingFlights[].availableSeats
Type: integer
Required: Yes
Nullable: No

### arrivingFlights[].availableSeatClasses
Type: array
Required: Yes
Nullable: No
Allowed values: ECONOMY, BUSINESS

### arrivingFlights[].stopsNumber
Type: integer
Required: Yes
Nullable: No

### arrivingFlights[].stopsInfo
Type: string
Required: Yes
Nullable: Yes

### priceGrid
Type: array
Required: Yes
Nullable: No

### priceGrid[].departingDate
Type: string; Format: date
Required: Yes
Nullable: No

### priceGrid[].returningDate
Type: string; Format: date
Required: No
Nullable: No

### priceGrid[].minPrice
Type: number
Required: Yes
Nullable: No

### priceHistory
Type: array
Required: Yes
Nullable: No

### priceHistory[].recordedDate
Type: string; Format: date
Required: Yes
Nullable: No

### priceHistory[].averagePrice
Type: number
Required: Yes
Nullable: No

### priceRating
Type: object
Required: No
Nullable: No

### priceRating.averagePrice
Type: number
Required: Yes
Nullable: No

### priceRating.projectedPrice
Type: number
Required: Yes
Nullable: No

### priceRating.projectedChangePercent
Type: number
Required: Yes
Nullable: No

### priceRating.recommendation
Type: string; Format: enum
Required: Yes
Nullable: No
Allowed values: BUY_SOON, WAIT

## Error Response — HTTP 400

### message

Type: string | string[]
Required: Yes
Nullable: No
Note: The response should use standard error envelopes if configured in the global exception filter.

## Error Response — HTTP 500

### message

Type: string
Required: Yes
Nullable: No
Note: The response should use standard error envelopes if configured in the global exception filter.
