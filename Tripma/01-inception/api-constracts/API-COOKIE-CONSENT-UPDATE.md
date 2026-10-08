---
artifact_type: api-contract
status: Frozen
api_id: API-COOKIE-CONSENT-UPDATE
related_uc_id: UC-15
---

# API-COOKIE-CONSENT-UPDATE: Update Cookie Consent

## General Information

### API ID

API-COOKIE-CONSENT-UPDATE

### API Name

Update Cookie Consent

### Related Use Case IDs

UC-15

### Method

PUT

### Path

/api/privacy/cookie-consent

### Description

Stores the effective cookie-consent state for the current Tripma browser.

### Authentication

Public

### Authorization

None

## Request Header(s)

### headers.Content-Type

Type: string; Format: MIME type; Required: Yes; Nullable: No

Trigger: Every PUT request to this endpoint.

Description: Media type of the request body.

Example: "application/json"

Note: Identifies the media type of the submitted request body.

### headers.Accept

Type: string; Format: MIME type; Required: No; Nullable: No

Trigger: When the client supplies the Accept header.

Description: Requested response media type.

Example: "application/json"

Note: Identifies the requested response media type.

## Path Parameter(s)

None

## Query Parameter(s)

None

## Request Body

### analytics

Type: boolean; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Analytics-cookie consent flag.

Example: false

### personalization

Type: boolean; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Personalization-cookie consent flag.

Example: false

### marketing

Type: boolean; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Marketing-cookie consent flag.

Example: false

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

Example: {"necessary": true, "analytics": false, "personalization": false, "marketing": false, "status": "REJECTED_OPTIONAL", "policyVersion": "2026-10", "decidedAt": "2026-10-07T09:00:00Z", "expiresAt": "2027-04-05T09:00:00Z"}

### data.necessary

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Necessary-cookie consent flag.

Example: true

### data.analytics

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Analytics-cookie consent flag.

Example: false

### data.personalization

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Personalization-cookie consent flag.

Example: false

### data.marketing

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Marketing-cookie consent flag.

Example: false

### data.status

Type: string; Format: enum; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Public consent state.

Example: "REJECTED_OPTIONAL"

### data.policyVersion

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Consent policy version string.

Example: "2026-10"

### data.decidedAt

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Decided at timestamp in the declared ISO 8601 format.

Example: "2026-10-07T09:00:00Z"

### data.expiresAt

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Expires at timestamp in the declared ISO 8601 format.

Example: "2027-04-05T09:00:00Z"

## Success Response Header(s)

### headers.Set-Cookie

Type: string; Format: HTTP Set-Cookie; Required: Yes; Nullable: No

Trigger: Returned with the successful HTTP response.

Description: Cookie setting returned by the endpoint.

Example: "tripma_consent=opaque-consent-value; Path=/; SameSite=Lax"

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

This local API stores the consent selection required by UC-15 in a first-party cookie.
