---
artifact_type: api-contract
status: Frozen
api_id: API-SEATS-LIST
related_uc_id: UC-04
---

# API-SEATS-LIST: Get Available Seats

## General Information

### API ID

API-SEATS-LIST

### API Name

Get Available Seats

### Related Use Case IDs

UC-04

### Method

GET

### Path

/api/seats/{flightId}

### Description

Provides Tripma seat data for a submitted flight reference.

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

### path.flightId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Every request using the flightId path segment.

Description: Flight identifier.

Example: "955efaff-2d21-5d86-a015-541efa3d7bb5"

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

Example: {"flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "currency": "USD", "businessSeats": [{"id": "26927cf9-0f95-5ff4-b634-80783a645c42", "flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "seatNumber": "2A", "seatClass": "BUSINESS", "available": true, "price": 300, "currency": "USD"}], "economySeats": [{"id": "d3b42501-3620-5a0e-9e20-1ce5b58fdca1", "flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "seatNumber": "12A", "seatClass": "ECONOMY", "available": true, "price": 300, "currency": "USD"}]}

### data.flightId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Flight identifier.

Example: "955efaff-2d21-5d86-a015-541efa3d7bb5"

### data.currency

Type: string; Format: ISO 4217 currency code; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: ISO 4217 currency code for monetary values.

Example: "USD"

### data.businessSeats

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Business cabin seat representations.

Example: [{"id": "26927cf9-0f95-5ff4-b634-80783a645c42", "flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "seatNumber": "2A", "seatClass": "BUSINESS", "available": true, "price": 300, "currency": "USD"}]

### data.businessSeats[].id

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.businessSeats[] object or array item is present and non-null.

Description: Identifier of the represented resource.

Example: "26927cf9-0f95-5ff4-b634-80783a645c42"

### data.businessSeats[].flightId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.businessSeats[] object or array item is present and non-null.

Description: Flight identifier.

Example: "955efaff-2d21-5d86-a015-541efa3d7bb5"

### data.businessSeats[].seatNumber

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.businessSeats[] object or array item is present and non-null.

Description: Seat label.

Example: "2A"

### data.businessSeats[].seatClass

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.businessSeats[] object or array item is present and non-null.

Description: Public cabin-class value.

Example: "BUSINESS"

Allowed values: ECONOMY, BUSINESS

### data.businessSeats[].available

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.businessSeats[] object or array item is present and non-null.

Description: Reported availability flag.

Example: true

### data.businessSeats[].price

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.businessSeats[] object or array item is present and non-null.

Description: Reported price in the response currency.

Example: 300

### data.businessSeats[].currency

Type: string; Format: ISO 4217 currency code; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.businessSeats[] object or array item is present and non-null.

Description: ISO 4217 currency code for monetary values.

Example: "USD"

### data.economySeats

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Economy cabin seat representations.

Example: [{"id": "d3b42501-3620-5a0e-9e20-1ce5b58fdca1", "flightId": "955efaff-2d21-5d86-a015-541efa3d7bb5", "seatNumber": "12A", "seatClass": "ECONOMY", "available": true, "price": 300, "currency": "USD"}]

### data.economySeats[].id

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.economySeats[] object or array item is present and non-null.

Description: Identifier of the represented resource.

Example: "d3b42501-3620-5a0e-9e20-1ce5b58fdca1"

### data.economySeats[].flightId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.economySeats[] object or array item is present and non-null.

Description: Flight identifier.

Example: "955efaff-2d21-5d86-a015-541efa3d7bb5"

### data.economySeats[].seatNumber

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.economySeats[] object or array item is present and non-null.

Description: Seat label.

Example: "12A"

### data.economySeats[].seatClass

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.economySeats[] object or array item is present and non-null.

Description: Public cabin-class value.

Example: "ECONOMY"

Allowed values: ECONOMY, BUSINESS

### data.economySeats[].available

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.economySeats[] object or array item is present and non-null.

Description: Reported availability flag.

Example: true

### data.economySeats[].price

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.economySeats[] object or array item is present and non-null.

Description: Reported price in the response currency.

Example: 300

### data.economySeats[].currency

Type: string; Format: ISO 4217 currency code; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.economySeats[] object or array item is present and non-null.

Description: ISO 4217 currency code for monetary values.

Example: "USD"

## Error Response — HTTP 400

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 400 error response.

Description: Public error outcome summary.

Example: "The request does not match the declared wire schema."

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

Note: Error responses should use the standard error envelope if configured in the global exception filter.
