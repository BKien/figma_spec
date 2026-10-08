---
artifact_type: api-contract
status: Frozen
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

Type: string; Format: MIME type; Required: Yes; Nullable: No

Trigger: Every POST request to this endpoint.

Description: Media type of the request body.

Example: "application/json"

Note: Identifies the media type of the submitted request body.

Default: application/json

Allowed values: application/json

### headers.Accept

Type: string; Format: MIME type; Required: No; Nullable: No

Trigger: When the client supplies the Accept header.

Description: Requested response media type.

Example: "application/json"

Note: Identifies the requested response media type.

Default: application/json

Allowed values: application/json

### headers.X-Confirmation-Code

Type: string; Format: Opaque HTTP header value; Required: No; Nullable: No

Trigger: When the client supplies the X-Confirmation-Code header.

Description: Booking confirmation access code carried by the HTTP header.

Example: "TRP7K2"

Note: Transmit the confirmation code as a single header value.

## Path Parameter(s)

### path.bookingId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Every request using the bookingId path segment.

Description: Booking identifier.

Example: "6ca91d4e-4bc3-515b-86f9-8930c7b1a1e3"

## Query Parameter(s)

None

## Request Body

### recipientEmails

Type: array; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Recipient email address array.

Example: ["friend@example.com"]

### recipientEmails[]

Type: string; Format: email; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Recipient email address array.

Example: "friend@example.com"

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

Example: {"bookingId": "6ca91d4e-4bc3-515b-86f9-8930c7b1a1e3", "deliveries": [{"shareId": "0513ca65-6209-512d-9aad-f2ef88167fa1", "recipientEmail": "friend@example.com", "deliveryStatus": "SENT"}]}

### data.bookingId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Booking identifier.

Example: "6ca91d4e-4bc3-515b-86f9-8930c7b1a1e3"

### data.deliveries

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Itinerary delivery outcome representations.

Example: [{"shareId": "0513ca65-6209-512d-9aad-f2ef88167fa1", "recipientEmail": "friend@example.com", "deliveryStatus": "SENT"}]

### data.deliveries[].shareId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.deliveries[] object or array item is present and non-null.

Description: Share identifier.

Example: "0513ca65-6209-512d-9aad-f2ef88167fa1"

### data.deliveries[].recipientEmail

Type: string; Format: email; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.deliveries[] object or array item is present and non-null.

Description: Recipient email address.

Example: "friend@example.com"

### data.deliveries[].deliveryStatus

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.deliveries[] object or array item is present and non-null.

Description: Public itinerary delivery state.

Example: "SENT"

Allowed values: SENT, FAILED

### data.deliveries[].sentAt

Type: string; Format: ISO 8601; Required: No; Nullable: Yes

Trigger: Included in the HTTP 200 success response when the containing data.deliveries[] object or array item is present and non-null and this optional property is returned.

Description: Sent at timestamp in the declared ISO 8601 format.

Example: "2026-10-10T09:00:00Z"

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

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

## Error Response — HTTP 403

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 403 error response.

Description: Public error outcome summary.

Example: "Access to this operation was not accepted."

Note: Field of the JSON error response.

## Error Response — HTTP 404

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 404 error response.

Description: Public error outcome summary.

Example: "The requested resource was not found."

Note: Field of the JSON error response.

## Error Response — HTTP 502

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 502 error response.

Description: Public error outcome summary.

Example: "An upstream service returned an unusable response."

Note: Field of the JSON error response.

### data

Type: object; Required: No; Nullable: No

Trigger: Included in the HTTP 502 error response when this optional field is returned.

Description: Endpoint-specific response payload.

Example: {"bookingId": "6ca91d4e-4bc3-515b-86f9-8930c7b1a1e3", "deliveries": [{"shareId": "0513ca65-6209-512d-9aad-f2ef88167fa1", "recipientEmail": "friend@example.com", "deliveryStatus": "FAILED"}]}

Note: Field of the JSON error response.

### data.bookingId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 502 error response when the containing data object or array item is present and non-null.

Description: Booking identifier.

Example: "6ca91d4e-4bc3-515b-86f9-8930c7b1a1e3"

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

### data.deliveries

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 502 error response when the containing data object or array item is present and non-null.

Description: Itinerary delivery outcome representations.

Example: [{"shareId": "0513ca65-6209-512d-9aad-f2ef88167fa1", "recipientEmail": "friend@example.com", "deliveryStatus": "FAILED"}]

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

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

This contract sends the itinerary of an accessible booking to the recipient specified in UC-09.
