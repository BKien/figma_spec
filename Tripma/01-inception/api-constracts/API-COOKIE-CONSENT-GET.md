---
artifact_type: api-contract
status: Frozen
api_id: API-COOKIE-CONSENT-GET
related_uc_id: UC-15
---

# API-COOKIE-CONSENT-GET: Get Cookie Consent

## General Information

### API ID

API-COOKIE-CONSENT-GET

### API Name

Get Cookie Consent

### Related Use Case IDs

UC-15

### Method

GET

### Path

/api/privacy/cookie-consent

### Description

Provides the effective cookie-consent state for the current Tripma browser.

### Authentication

Public

### Authorization

None

## Request Header(s)

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

None

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

Example: {"necessary": true, "analytics": false, "personalization": false, "marketing": false, "status": "REJECTED_OPTIONAL", "policyVersion": "2026-10"}

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

Type: string; Format: ISO 8601; Required: No; Nullable: Yes

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null and this optional property is returned.

Description: Decided at timestamp in the declared ISO 8601 format.

Example: "2026-10-07T09:00:00Z"

### data.expiresAt

Type: string; Format: ISO 8601; Required: No; Nullable: Yes

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null and this optional property is returned.

Description: Expires at timestamp in the declared ISO 8601 format.

Example: "2027-04-05T09:00:00Z"

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

This local API reads the first-party consent cookie required by UC-15.
