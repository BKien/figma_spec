---
artifact_type: api-contract
status: Draft
api_id: API-AUTH-SIGNUP
related_uc_id: UC-07
---

# API-AUTH-SIGNUP: Sign Up

## General Information

### API ID

API-AUTH-SIGNUP

### API Name

Sign Up

### Related Use Case IDs

UC-07

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

Type: string; Format: MIME type
Required: Yes
Nullable: No
Default: application/json
Allowed values: application/json

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

### agreeTerms

Type: boolean
Required: Yes
Nullable: No

### receiveDealAlerts

Type: boolean
Required: Yes
Nullable: No
Default: false

## Success Response — HTTP 201

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

### data.id

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.email

Type: string; Format: email
Required: Yes
Nullable: No

### data.username

Type: string
Required: Yes
Nullable: No

### data.receiveDealAlerts

Type: boolean
Required: Yes
Nullable: No

### data.createdAt

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

## Error Response — HTTP 409

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

This contract creates an account for UC-07. It may be invoked from the navbar registration entry or from the account-creation option referenced by UC-05.
