---
artifact_type: api-contract
status: Draft
api_id: API-BOOKING-CANCEL
related_uc_id: UC-14
---

# API-BOOKING-CANCEL: Cancel Booking

## General Information

### API ID

API-BOOKING-CANCEL

### API Name

Cancel Booking

### Related Use Case IDs

UC-14

### Method

POST

### Path

/api/bookings/{bookingId}/cancellations

### Description

Creates a cancellation for an eligible accessible Tripma booking.

### Authentication

Optional session

### Authorization

Governed by UC-14.

## Request Header(s)

### headers.Content-Type

Type: string; Format: MIME type
Required: No
Nullable: No

### headers.Accept

Type: string; Format: MIME type
Required: No
Nullable: No

### headers.Idempotency-Key

Type: string
Required: Yes
Nullable: No

## Path Parameter(s)

### bookingId

Type: string; Format: UUID
Required: Yes
Nullable: No

## Query Parameter(s)

None

## Request Body

### confirmationCode

Type: string
Required: No
Nullable: No

## Success Response — HTTP 201

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

### data.cancellationId

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.bookingId

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.bookingStatus

Type: string; Format: enum
Required: Yes
Nullable: No

### data.cancellationFee

Type: number
Required: Yes
Nullable: No

### data.refundAmount

Type: number
Required: Yes
Nullable: No

### data.currency

Type: string; Format: ISO 4217 currency code
Required: Yes
Nullable: No

### data.refundStatus

Type: string; Format: enum
Required: Yes
Nullable: No

### data.cancelledAt

Type: string; Format: ISO 8601
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

## Error Response — HTTP 409

### message

Type: string
Required: Yes
Nullable: No

## Error Response — HTTP 422

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

This contract performs booking cancellation for UC-14 and preserves the cancelled booking as historical data.
