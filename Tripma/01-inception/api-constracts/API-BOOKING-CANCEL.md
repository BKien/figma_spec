---
artifact_type: api-contract
status: Frozen
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

Type: string; Format: MIME type; Required: No; Nullable: No

Trigger: When the client supplies the Content-Type header.

Description: Media type of the request body.

Example: "application/json"

Note: Identifies the media type of the submitted request body.

### headers.Accept

Type: string; Format: MIME type; Required: No; Nullable: No

Trigger: When the client supplies the Accept header.

Description: Requested response media type.

Example: "application/json"

Note: Identifies the requested response media type.

### headers.Idempotency-Key

Type: string; Format: Opaque HTTP header value; Required: Yes; Nullable: No

Trigger: Every POST request to this endpoint.

Description: Opaque command reference carried by the HTTP header.

Example: "command-example-01"

Note: Transmit the command reference as a single header value.

## Path Parameter(s)

### path.bookingId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Every request using the bookingId path segment.

Description: Booking identifier.

Example: "6ca91d4e-4bc3-515b-86f9-8930c7b1a1e3"

## Query Parameter(s)

None

## Request Body

### confirmationCode

Type: string; Required: No; Nullable: No

Trigger: When the client includes this property in the request body.

Description: Booking confirmation access code.

Example: "TRP7K2"

## Success Response — HTTP 201

### success

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response.

Description: Indicates whether the HTTP operation completed successfully.

Example: true

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response.

Description: Human-readable operation outcome summary.

Example: "Request completed successfully."

### data

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response.

Description: Endpoint-specific response payload.

Example: {"cancellationId": "603f4b95-9c30-5710-b26b-894b0b99afca", "bookingId": "6ca91d4e-4bc3-515b-86f9-8930c7b1a1e3", "bookingStatus": "CANCELLED", "cancellationFee": 25, "refundAmount": 275, "currency": "USD", "refundStatus": "COMPLETED", "cancelledAt": "2026-10-07T09:00:00Z"}

### data.cancellationId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Cancellation identifier.

Example: "603f4b95-9c30-5710-b26b-894b0b99afca"

### data.bookingId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Booking identifier.

Example: "6ca91d4e-4bc3-515b-86f9-8930c7b1a1e3"

### data.bookingStatus

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Public booking state.

Example: "CANCELLED"

### data.cancellationFee

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Reported cancellation fee in the response currency.

Example: 25

### data.refundAmount

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Reported refund amount in the response currency.

Example: 275

### data.currency

Type: string; Format: ISO 4217 currency code; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: ISO 4217 currency code for monetary values.

Example: "USD"

### data.refundStatus

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Public refund state.

Example: "COMPLETED"

### data.cancelledAt

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Cancelled at timestamp in the declared ISO 8601 format.

Example: "2026-10-07T09:00:00Z"

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

## Error Response — HTTP 409

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 409 error response.

Description: Public error outcome summary.

Example: "The request conflicts with the current operation."

Note: Field of the JSON error response.

## Error Response — HTTP 422

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 422 error response.

Description: Public error outcome summary.

Example: "The request could not be processed."

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

This contract performs booking cancellation for UC-14 and preserves the cancelled booking as historical data.
