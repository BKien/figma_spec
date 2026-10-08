---
artifact_type: api-contract
status: Frozen
api_id: API-AUTH-SIGNIN
related_uc_ids: ["UC-05", "UC-08"]
---

# API-AUTH-SIGNIN: Sign In

## General Information

### API ID

API-AUTH-SIGNIN

### API Name

Sign In

### Related Use Case IDs

UC-05, UC-08

### Method

POST

### Path

/api/auth/signin

### Description

Handles a submitted Tripma email-and-password sign-in request and returns its authentication outcome.

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

Default: application/x-www-form-urlencoded

Allowed values: application/x-www-form-urlencoded, application/json

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

### callbackUrl

Type: string; Format: URI; Required: No; Nullable: No

Trigger: When the client includes this property in the request body.

Description: Client callback URI.

Example: "https://example.com/account"

### csrfToken

Type: string; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Opaque CSRF token submitted by the client.

Example: "csrf-example-01"

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

Example: {"user": {"id": "e5030dbf-bdae-5b07-9772-17fc79301ee1", "email": "alex@example.com", "username": "alexmorgan"}, "session": {"expiresAt": "2026-10-10T20:30:00Z"}}

### data.user

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Public user representation.

Example: {"id": "e5030dbf-bdae-5b07-9772-17fc79301ee1", "email": "alex@example.com", "username": "alexmorgan"}

### data.user.id

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.user object or array item is present and non-null.

Description: Identifier of the represented resource.

Example: "e5030dbf-bdae-5b07-9772-17fc79301ee1"

### data.user.email

Type: string; Format: email; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.user object or array item is present and non-null.

Description: Email address.

Example: "alex@example.com"

### data.user.username

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.user object or array item is present and non-null.

Description: Account display username.

Example: "alexmorgan"

### data.session

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Session representation.

Example: {"expiresAt": "2026-10-10T20:30:00Z"}

### data.session.expiresAt

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.session object or array item is present and non-null.

Description: Expires at timestamp in the declared ISO 8601 format.

Example: "2026-10-10T20:30:00Z"

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

## Error Response — HTTP 401

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 401 error response.

Description: Public error outcome summary.

Example: "Authentication was not accepted."

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

This contract handles email-and-password authentication and establishes the session required by UC-08.
