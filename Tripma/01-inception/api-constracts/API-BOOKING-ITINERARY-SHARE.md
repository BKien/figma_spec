---
artifact_type: api-contract
status: Draft
api_id: API-BOOKING-ITINERARY-SHARE
related_uc_id: UC-09
---

# API-BOOKING-ITINERARY-SHARE: Share Booking Itinerary

## General Information

### API ID

API-BOOKING-ITINERARY-SHARE

### API Name

Share Booking Itinerary

### Related Use Case IDs

UC-09

### Method

POST

### Path

/api/bookings/{bookingId}/share

### Description

Processes a Tripma itinerary-sharing request for a referenced booking.

### Authentication

Optional session

### Authorization

Governed by UC-09.

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

### headers.X-Confirmation-Code

Type: string
Required: No
Nullable: No

## Path Parameter(s)

### path.bookingId

Type: string; Format: UUID
Required: Yes
Nullable: No

## Query Parameter(s)

None

## Request Body

### recipientEmails

Type: array
Required: Yes
Nullable: No

### recipientEmails[]

Type: string; Format: email
Required: Yes
Nullable: No

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

### data.bookingId

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.deliveries

Type: array
Required: Yes
Nullable: No

### data.deliveries[].shareId

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.deliveries[].recipientEmail

Type: string; Format: email
Required: Yes
Nullable: No

### data.deliveries[].deliveryStatus

Type: string; Format: enum
Required: Yes
Nullable: No
Allowed values: SENT, FAILED

### data.deliveries[].sentAt

Type: string; Format: ISO 8601
Required: No
Nullable: Yes

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

## Error Response — HTTP 403

### message

Type: string
Required: Yes
Nullable: No

## Error Response — HTTP 404

### message

Type: string
Required: Yes
Nullable: No

## Error Response — HTTP 502

### message

Type: string
Required: Yes
Nullable: No

### data

Type: object
Required: No
Nullable: No

### data.bookingId

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.deliveries

Type: array
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

This contract sends the itinerary of an accessible booking to the recipient specified in UC-09.
