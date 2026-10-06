---
artifact_type: api-contract
status: Draft
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
Default: application/json
Allowed values: application/json

## Path Parameter(s)

### path.flightId

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

### data.flightId

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.currency

Type: string; Format: ISO 4217 currency code
Required: Yes
Nullable: No

### data.businessSeats

Type: array
Required: Yes
Nullable: No

### data.businessSeats[].id

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.businessSeats[].flightId

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.businessSeats[].seatNumber

Type: string
Required: Yes
Nullable: No

### data.businessSeats[].seatClass

Type: string; Format: enum
Required: Yes
Nullable: No
Allowed values: ECONOMY, BUSINESS

### data.businessSeats[].available

Type: boolean
Required: Yes
Nullable: No

### data.businessSeats[].price

Type: number
Required: Yes
Nullable: No

### data.businessSeats[].currency

Type: string; Format: ISO 4217 currency code
Required: Yes
Nullable: No

### data.economySeats

Type: array
Required: Yes
Nullable: No

### data.economySeats[].id

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.economySeats[].flightId

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.economySeats[].seatNumber

Type: string
Required: Yes
Nullable: No

### data.economySeats[].seatClass

Type: string; Format: enum
Required: Yes
Nullable: No
Allowed values: ECONOMY, BUSINESS

### data.economySeats[].available

Type: boolean
Required: Yes
Nullable: No

### data.economySeats[].price

Type: number
Required: Yes
Nullable: No

### data.economySeats[].currency

Type: string; Format: ISO 4217 currency code
Required: Yes
Nullable: No

## Error Response — HTTP 400

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

Note: Error responses should use the standard error envelope if configured in the global exception filter.
