---
artifact_type: api-contract
status: Draft
api_id: API-FLIGHT-DEALS-LIST
related_uc_id: UC-10
---

# API-FLIGHT-DEALS-LIST: List Flight Deals

## General Information

### API ID

API-FLIGHT-DEALS-LIST

### API Name

List Flight Deals

### Related Use Case IDs

UC-10

### Method

GET

### Path

/api/flight-deals

### Description

Provides the Tripma flight-deal collection.

### Authentication

Public

### Authorization

None

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

Type: array
Required: Yes
Nullable: No

### data[].id

Type: string; Format: UUID
Required: Yes
Nullable: No

### data[].placeName

Type: string
Required: Yes
Nullable: No

### data[].city

Type: string
Required: Yes
Nullable: No

### data[].imagePath

Type: string
Required: Yes
Nullable: No

### data[].price

Type: number
Required: Yes
Nullable: No

### data[].currency

Type: string; Format: ISO 4217 currency code
Required: Yes
Nullable: No

### data[].description

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

This contract returns the active flight-deal collection required by UC-10.
