---
artifact_type: api-contract
status: Draft
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

Type: string; Format: MIME type
Required: No
Nullable: No

## Path Parameter(s)

None

## Query Parameter(s)

None

## Request Body

None

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

### data.necessary

Type: boolean
Required: Yes
Nullable: No

### data.analytics

Type: boolean
Required: Yes
Nullable: No

### data.personalization

Type: boolean
Required: Yes
Nullable: No

### data.marketing

Type: boolean
Required: Yes
Nullable: No

### data.status

Type: string; Format: enum
Required: Yes
Nullable: No

### data.policyVersion

Type: string
Required: Yes
Nullable: No

### data.decidedAt

Type: string; Format: ISO 8601
Required: No
Nullable: Yes

### data.expiresAt

Type: string; Format: ISO 8601
Required: No
Nullable: Yes

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

This local API reads the first-party consent cookie required by UC-15.
