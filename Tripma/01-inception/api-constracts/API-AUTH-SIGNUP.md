---
artifact_type: api-contract
status: Frozen
api_id: API-AUTH-SIGNUP
related_uc_ids: ["UC-05", "UC-07"]
---

# API-AUTH-SIGNUP: Sign Up

## General Information

### API ID

API-AUTH-SIGNUP

### API Name

Sign Up

### Related Use Case IDs

UC-05, UC-07

### Method

POST

### Path

/api/auth/signup

### Description

Processes a submitted Tripma email-and-password account request and returns its outcome.

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

## Path Parameter(s)

None

## Query Parameter(s)

None

## Request Body

### email

Type: string; Format: email; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Email address.

Example: "alex@example.com"

### password

Type: string; Format: password; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Submitted account password.

Example: "ExamplePassword42!"

### agreeTerms

Type: boolean; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Submitted terms acceptance flag.

Example: true

### receiveDealAlerts

Type: boolean; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Deal-alert subscription flag.

Example: false

Default: false

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

Example: {"id": "e5030dbf-bdae-5b07-9772-17fc79301ee1", "email": "alex@example.com", "username": "alexmorgan", "receiveDealAlerts": false, "createdAt": "2026-10-07T09:00:00Z"}

### data.id

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Identifier of the represented resource.

Example: "e5030dbf-bdae-5b07-9772-17fc79301ee1"

### data.email

Type: string; Format: email; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Email address.

Example: "alex@example.com"

### data.username

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Account display username.

Example: "alexmorgan"

### data.receiveDealAlerts

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Deal-alert subscription flag.

Example: false

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

Example: [{"field": "email", "code": "INVALID_FORMAT"}]

Note: Field of the JSON error response.

### issues[].field

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 400 error response when the containing issues[] object or array item is present and non-null.

Description: Request field path associated with this issue.

Example: "email"

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

### issues[].code

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 400 error response when the containing issues[] object or array item is present and non-null.

Description: Public machine-readable outcome or issue code.

Example: "INVALID_FORMAT"

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

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

This contract creates an account for UC-07. It may be invoked from the navbar registration entry or from the account-creation option referenced by UC-05.
