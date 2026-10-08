---
artifact_type: api-contract
status: Frozen
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

Trigger: Every POST request to this endpoint.

Description: Media type of the request body.

Example: "application/json"

Note: Identifies the media type of the submitted request body.

Allowed values: application/json

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

None

## Request Body

### selectionContextKey

Type: string; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Opaque flight-selection context reference.

Example: "flight-selection-example-01"

### type

Type: boolean; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Trip-type flag: true denotes round-trip and false denotes one-way.

Example: true

### adults

Type: integer; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Submitted adult passenger count.

Example: 1

### minors

Type: integer; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Submitted minor passenger count.

Example: 0

### departingFlightId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Departing flight identifier.

Example: "e5030dbf-bdae-5b07-9772-17fc79301ee1"

### returningFlightId

Type: string; Format: UUID; Required: No; Nullable: No

Trigger: When the client includes this property in the request body.

Description: Returning flight identifier.

Example: "9862aa86-635a-5236-88c8-ac4e5b22147e"

### primaryPassengerRef

Type: string; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Client reference identifying the primary passenger.

Example: "passenger_01"

### passengers

Type: array; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Passenger representations.

Example: [{"passengerRef": "passenger_01", "passengerType": "ADULT", "firstName": "Alex", "lastName": "Morgan", "dateOfBirth": "1990-01-15"}]

### passengers[].passengerRef

Type: string; Required: Yes; Nullable: No

Trigger: When the containing passengers[] object or array item is supplied in the request body.

Description: Client passenger reference.

Example: "passenger_01"

### passengers[].passengerType

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: When the containing passengers[] object or array item is supplied in the request body.

Description: Public passenger category.

Example: "ADULT"

Allowed values: ADULT, MINOR

### passengers[].firstName

Type: string; Required: Yes; Nullable: No

Trigger: When the containing passengers[] object or array item is supplied in the request body.

Description: Given name.

Example: "Alex"

### passengers[].middleName

Type: string; Required: No; Nullable: No

Trigger: When the client includes this optional property in the containing passengers[] object or array item.

Description: Middle name.

Example: "Taylor"

### passengers[].lastName

Type: string; Required: Yes; Nullable: No

Trigger: When the containing passengers[] object or array item is supplied in the request body.

Description: Family name.

Example: "Morgan"

### passengers[].suffix

Type: string; Required: No; Nullable: No

Trigger: When the client includes this optional property in the containing passengers[] object or array item.

Description: Name suffix.

Example: "Jr."

### passengers[].dateOfBirth

Type: string; Format: date; Required: Yes; Nullable: No

Trigger: When the containing passengers[] object or array item is supplied in the request body.

Description: Passenger birth date.

Example: "1990-01-15"

### passengers[].email

Type: string; Format: email; Required: No; Nullable: No

Trigger: When the client includes this optional property in the containing passengers[] object or array item.

Description: Email address.

Example: "alex@example.com"

### passengers[].phone

Type: string; Format: telephone; Required: No; Nullable: No

Trigger: When the client includes this optional property in the containing passengers[] object or array item.

Description: Telephone contact string.

Example: "+14155550123"

### passengers[].redressNumber

Type: string; Required: No; Nullable: No

Trigger: When the client includes this optional property in the containing passengers[] object or array item.

Description: Submitted passenger redress reference.

Example: "1234567"

### passengers[].knownTravelerNumber

Type: string; Required: No; Nullable: No

Trigger: When the client includes this optional property in the containing passengers[] object or array item.

Description: Submitted known-traveler reference.

Example: "123456789"

### baggage

Type: array; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Passenger baggage representations.

Example: [{"passengerRef": "passenger_01", "departingCheckedBags": 1}]

### baggage[].passengerRef

Type: string; Required: Yes; Nullable: No

Trigger: When the containing baggage[] object or array item is supplied in the request body.

Description: Client passenger reference.

Example: "passenger_01"

### baggage[].departingCheckedBags

Type: integer; Required: Yes; Nullable: No

Trigger: When the containing baggage[] object or array item is supplied in the request body.

Description: Submitted outbound checked bag count.

Example: 1

### baggage[].returningCheckedBags

Type: integer; Required: No; Nullable: No

Trigger: When the client includes this optional property in the containing baggage[] object or array item.

Description: Submitted return checked bag count.

Example: 1

### emergencyContact

Type: object; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Emergency contact representation.

Example: {"usePrimaryPassenger": true}

### emergencyContact.usePrimaryPassenger

Type: boolean; Required: Yes; Nullable: No

Trigger: When the containing emergencyContact object or array item is supplied in the request body.

Description: Client flag selecting the primary passenger contact.

Example: true

### emergencyContact.firstName

Type: string; Required: No; Nullable: No

Trigger: When the client includes this optional property in the containing emergencyContact object or array item.

Description: Given name.

Example: "Alex"

### emergencyContact.lastName

Type: string; Required: No; Nullable: No

Trigger: When the client includes this optional property in the containing emergencyContact object or array item.

Description: Family name.

Example: "Morgan"

### emergencyContact.email

Type: string; Format: email; Required: No; Nullable: No

Trigger: When the client includes this optional property in the containing emergencyContact object or array item.

Description: Email address.

Example: "alex@example.com"

### emergencyContact.phone

Type: string; Format: telephone; Required: No; Nullable: No

Trigger: When the client includes this optional property in the containing emergencyContact object or array item.

Description: Telephone contact string.

Example: "+14155550123"

## Success Response — HTTP 200

### passengerContextKey

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Opaque passenger-information context reference.

Example: "passenger-context-example-01"

### selectionContextKey

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Opaque flight-selection context reference.

Example: "flight-selection-example-01"

### primaryPassengerRef

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Client reference identifying the primary passenger.

Example: "passenger_01"

### preparedAt

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Prepared at timestamp in the declared ISO 8601 format.

Example: "2026-10-07T09:00:00Z"

### passengers

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Passenger representations.

Example: [{"passengerRef": "passenger_01", "passengerType": "ADULT", "firstName": "Alex", "lastName": "Morgan", "dateOfBirth": "1990-01-15"}]

### passengers[].passengerRef

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing passengers[] object or array item is present and non-null.

Description: Client passenger reference.

Example: "passenger_01"

### passengers[].passengerType

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing passengers[] object or array item is present and non-null.

Description: Public passenger category.

Example: "ADULT"

Allowed values: ADULT, MINOR

### passengers[].firstName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing passengers[] object or array item is present and non-null.

Description: Given name.

Example: "Alex"

### passengers[].middleName

Type: string; Required: No; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing passengers[] object or array item is present and non-null and this optional property is returned.

Description: Middle name.

Example: "Taylor"

### passengers[].lastName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing passengers[] object or array item is present and non-null.

Description: Family name.

Example: "Morgan"

### passengers[].suffix

Type: string; Required: No; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing passengers[] object or array item is present and non-null and this optional property is returned.

Description: Name suffix.

Example: "Jr."

### passengers[].dateOfBirth

Type: string; Format: date; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing passengers[] object or array item is present and non-null.

Description: Passenger birth date.

Example: "1990-01-15"

### passengers[].email

Type: string; Format: email; Required: No; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing passengers[] object or array item is present and non-null and this optional property is returned.

Description: Email address.

Example: "alex@example.com"

### passengers[].phone

Type: string; Format: telephone; Required: No; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing passengers[] object or array item is present and non-null and this optional property is returned.

Description: Telephone contact string.

Example: "+14155550123"

### passengers[].redressNumber

Type: string; Required: No; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing passengers[] object or array item is present and non-null and this optional property is returned.

Description: Submitted passenger redress reference.

Example: "1234567"

### passengers[].knownTravelerNumber

Type: string; Required: No; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing passengers[] object or array item is present and non-null and this optional property is returned.

Description: Submitted known-traveler reference.

Example: "123456789"

### baggage

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Passenger baggage representations.

Example: [{"passengerRef": "passenger_01", "departingCheckedBags": 1}]

### baggage[].passengerRef

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing baggage[] object or array item is present and non-null.

Description: Client passenger reference.

Example: "passenger_01"

### baggage[].departingCheckedBags

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing baggage[] object or array item is present and non-null.

Description: Submitted outbound checked bag count.

Example: 1

### baggage[].returningCheckedBags

Type: integer; Required: No; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing baggage[] object or array item is present and non-null and this optional property is returned.

Description: Submitted return checked bag count.

Example: 1

### emergencyContact

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Emergency contact representation.

Example: {"usePrimaryPassenger": true, "firstName": "Alex", "lastName": "Morgan", "email": "alex@example.com", "phone": "+14155550123"}

### emergencyContact.usePrimaryPassenger

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing emergencyContact object or array item is present and non-null.

Description: Client flag selecting the primary passenger contact.

Example: true

### emergencyContact.firstName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing emergencyContact object or array item is present and non-null.

Description: Given name.

Example: "Alex"

### emergencyContact.lastName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing emergencyContact object or array item is present and non-null.

Description: Family name.

Example: "Morgan"

### emergencyContact.email

Type: string; Format: email; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing emergencyContact object or array item is present and non-null.

Description: Email address.

Example: "alex@example.com"

### emergencyContact.phone

Type: string; Format: telephone; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing emergencyContact object or array item is present and non-null.

Description: Telephone contact string.

Example: "+14155550123"

## Error Response — HTTP 400

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 400 error response.

Description: Public error outcome summary.

Example: "The request does not match the declared wire schema."

Note: Field of the JSON error response.

### issues

Type: array; Required: No; Nullable: No

Trigger: Included in the HTTP 400 error response when this optional field is returned.

Description: Optional array of protocol-level field issues.

Example: [{"field": "request", "code": "INVALID_FORMAT"}]

Note: Field of the JSON error response.

### issues[].field

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 400 error response when the containing issues[] object or array item is present and non-null.

Description: Request field path associated with this issue.

Example: "request"

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

### issues[].code

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 400 error response when the containing issues[] object or array item is present and non-null.

Description: Public machine-readable outcome or issue code.

Example: "INVALID_FORMAT"

Note: The response should use the standard error envelope if configured in the global exception filter.

## Error Response — HTTP 500

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 500 error response.

Description: Public error outcome summary.

Example: "An unexpected server error occurred."

Note: The response should use the standard error envelope if configured in the global exception filter.
