---
artifact_type: api-contract
status: Draft
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

Type: string; Format: MIME type
Required: Yes
Nullable: No

### headers.Accept

Type: string; Format: MIME type
Required: No
Nullable: No

## Path Parameter(s)

None

## Query Parameter(s)

None

## Request Body

### analytics

Type: boolean
Required: Yes
Nullable: No

### personalization

Type: boolean
Required: Yes
Nullable: No

### marketing

Type: boolean
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
Required: Yes
Nullable: No

### data.expiresAt

Type: string; Format: ISO 8601
Required: Yes
Nullable: No

## Success Response Header(s)

### headers.Set-Cookie

Type: string; Format: HTTP Set-Cookie
Required: Yes
Nullable: No

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

This local API stores the consent selection required by UC-15 in a first-party cookie.
