---
artifact_type: api-contract
status: Frozen
api_id: API-PAYMENT-METHOD-SAVE
related_uc_ids: ["UC-05", "UC-13"]
---

# API-PAYMENT-METHOD-SAVE: Save Payment Method

## General Information

### API ID

API-PAYMENT-METHOD-SAVE

### API Name

Save Payment Method

### Related Use Case IDs

UC-05, UC-13

### Method

POST

### Path

/api/users/me/payment-methods

### Description

Creates an account-owned saved payment method from a completed Tripma booking payment.

### Authentication

Required session

### Authorization

Governed by UC-13.

## Request Header(s)

### headers.Content-Type

Type: string; Format: MIME type; Required: Yes; Nullable: No

Trigger: Every POST request to this endpoint.

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

None

## Query Parameter(s)

None

## Request Body

### bookingId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Booking identifier.

Example: "6ca91d4e-4bc3-515b-86f9-8930c7b1a1e3"

### makeDefault

Type: boolean; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Client flag requesting the default payment-method setting.

Example: true

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

Example: {"id": "e5030dbf-bdae-5b07-9772-17fc79301ee1", "paymentMethod": "CREDIT_CARD", "displayName": "Alex Morgan", "cardLastFour": "4242", "expireDate": "2030-12-01", "isDefault": true, "createdAt": "2026-10-07T09:00:00Z"}

### data.id

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Identifier of the represented resource.

Example: "e5030dbf-bdae-5b07-9772-17fc79301ee1"

### data.paymentMethod

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Public payment method value.

Example: "CREDIT_CARD"

### data.displayName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Public display label.

Example: "Alex Morgan"

### data.cardLastFour

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Last four digits displayed for the payment card.

Example: "4242"

### data.expireDate

Type: string; Format: ISO 8601 date; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Payment-card expiry date in the declared wire format.

Example: "2030-12-01"

### data.isDefault

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Reported default payment-method flag.

Example: true

### data.createdAt

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Created at timestamp in the declared ISO 8601 format.

Example: "2026-10-07T09:00:00Z"

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

## Error Response — HTTP 401

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 401 error response.

Description: Public error outcome summary.

Example: "Authentication was not accepted."

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

This contract saves a reusable payment-method reference after the successful booking payment described by UC-13.
