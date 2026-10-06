---
artifact_type: api-contract
status: Draft
api_id: API-PASSENGER-INFO-PREPARE
related_uc_id: UC-03
---

# API-PASSENGER-INFO-PREPARE: Prepare Passenger Information

## General Information

### API ID

API-PASSENGER-INFO-PREPARE

### API Name

Prepare Passenger Information

### Related Use Case IDs

UC-03

### Method

POST

### Path

/api/passenger-information/prepare

### Description

Prepares passenger, emergency-contact, and baggage information for the current Tripma booking workflow.

### Authentication

Public

### Authorization

None

## Request Header(s)

### headers.Content-Type

Type: string; Format: MIME type; Required: Yes; Nullable: No
Allowed values: application/json

### headers.Accept

Type: string; Format: MIME type; Required: No; Nullable: No
Default: application/json
Allowed values: application/json

## Query Parameter(s)

None

## Request Body

### selectionContextKey

Type: string
Required: Yes
Nullable: No

### type

Type: boolean
Required: Yes
Nullable: No

### adults

Type: integer
Required: Yes
Nullable: No

### minors

Type: integer
Required: Yes
Nullable: No

### departingFlightId

Type: string; Format: UUID
Required: Yes
Nullable: No

### returningFlightId

Type: string; Format: UUID
Required: No
Nullable: No

### primaryPassengerRef

Type: string
Required: Yes
Nullable: No

### passengers

Type: array
Required: Yes
Nullable: No

### passengers[].passengerRef

Type: string
Required: Yes
Nullable: No

### passengers[].passengerType

Type: string; Format: enum
Required: Yes
Nullable: No
Allowed values: ADULT, MINOR

### passengers[].firstName

Type: string
Required: Yes
Nullable: No

### passengers[].middleName

Type: string
Required: No
Nullable: No

### passengers[].lastName

Type: string
Required: Yes
Nullable: No

### passengers[].suffix

Type: string
Required: No
Nullable: No

### passengers[].dateOfBirth

Type: string; Format: date
Required: Yes
Nullable: No

### passengers[].email

Type: string; Format: email
Required: No
Nullable: No

### passengers[].phone

Type: string; Format: telephone
Required: No
Nullable: No

### passengers[].redressNumber

Type: string
Required: No
Nullable: No

### passengers[].knownTravelerNumber

Type: string
Required: No
Nullable: No

### baggage

Type: array
Required: Yes
Nullable: No

### baggage[].passengerRef

Type: string
Required: Yes
Nullable: No

### baggage[].departingCheckedBags

Type: integer
Required: Yes
Nullable: No

### baggage[].returningCheckedBags

Type: integer
Required: No
Nullable: No

### emergencyContact

Type: object
Required: Yes
Nullable: No

### emergencyContact.usePrimaryPassenger

Type: boolean
Required: Yes
Nullable: No

### emergencyContact.firstName

Type: string
Required: No
Nullable: No

### emergencyContact.lastName

Type: string
Required: No
Nullable: No

### emergencyContact.email

Type: string; Format: email
Required: No
Nullable: No

### emergencyContact.phone

Type: string; Format: telephone
Required: No
Nullable: No

## Success Response — HTTP 200

### passengerContextKey

Type: string
Required: Yes
Nullable: No

### selectionContextKey

Type: string
Required: Yes
Nullable: No

### primaryPassengerRef

Type: string
Required: Yes
Nullable: No

### preparedAt

Type: string; Format: ISO 8601
Required: Yes
Nullable: No

### passengers

Type: array
Required: Yes
Nullable: No

### passengers[].passengerRef

Type: string
Required: Yes
Nullable: No

### passengers[].passengerType

Type: string; Format: enum
Required: Yes
Nullable: No
Allowed values: ADULT, MINOR

### passengers[].firstName

Type: string
Required: Yes
Nullable: No

### passengers[].middleName

Type: string
Required: No
Nullable: No

### passengers[].lastName

Type: string
Required: Yes
Nullable: No

### passengers[].suffix

Type: string
Required: No
Nullable: No

### passengers[].dateOfBirth

Type: string; Format: date
Required: Yes
Nullable: No

### passengers[].email

Type: string; Format: email
Required: No
Nullable: No

### passengers[].phone

Type: string; Format: telephone
Required: No
Nullable: No

### passengers[].redressNumber

Type: string
Required: No
Nullable: No

### passengers[].knownTravelerNumber

Type: string
Required: No
Nullable: No

### baggage

Type: array
Required: Yes
Nullable: No

### baggage[].passengerRef

Type: string
Required: Yes
Nullable: No

### baggage[].departingCheckedBags

Type: integer
Required: Yes
Nullable: No

### baggage[].returningCheckedBags

Type: integer
Required: No
Nullable: No

### emergencyContact

Type: object
Required: Yes
Nullable: No

### emergencyContact.usePrimaryPassenger

Type: boolean
Required: Yes
Nullable: No

### emergencyContact.firstName

Type: string
Required: Yes
Nullable: No

### emergencyContact.lastName

Type: string
Required: Yes
Nullable: No

### emergencyContact.email

Type: string; Format: email
Required: Yes
Nullable: No

### emergencyContact.phone

Type: string; Format: telephone
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

Note: The response should use the standard error envelope if configured in the global exception filter.

## Error Response — HTTP 500

### message

Type: string
Required: Yes
Nullable: No

Note: The response should use the standard error envelope if configured in the global exception filter.
