---
artifact_type: api-contract
status: Draft
api_id: API-AUTH-SIGNIN
related_uc_id: UC-08
---

# API-AUTH-SIGNIN: Sign In

## General Information

### API ID

API-AUTH-SIGNIN

### API Name

Sign In

### Related Use Case IDs

UC-08

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

Type: string; Format: MIME type
Required: Yes
Nullable: No
Default: application/x-www-form-urlencoded
Allowed values: application/x-www-form-urlencoded, application/json

### headers.Accept

Type: string; Format: MIME type
Required: No
Nullable: No
Default: application/json
Allowed values: application/json

## Path Parameter(s)

None

## Query Parameter(s)

None

## Request Body

### email

Type: string; Format: email
Required: Yes
Nullable: No

### password

Type: string; Format: password
Required: Yes
Nullable: No

### callbackUrl

Type: string; Format: URI
Required: No
Nullable: No

### csrfToken

Type: string
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

### data.user

Type: object
Required: Yes
Nullable: No

### data.user.id

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.user.email

Type: string; Format: email
Required: Yes
Nullable: No

### data.user.username

Type: string
Required: Yes
Nullable: No

### data.session

Type: object
Required: Yes
Nullable: No

### data.session.expiresAt

Type: string; Format: ISO 8601
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

## Error Response — HTTP 401

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

This contract handles email-and-password authentication and establishes the session required by UC-08.
