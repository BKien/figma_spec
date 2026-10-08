---
artifact_type: api-contract
status: Frozen
api_id: API-AUTH-REGISTER
related_uc_id: UC-01
---

# API-AUTH-REGISTER: User Registration

## General Information

### API ID

API-AUTH-REGISTER

### API Name

User Registration

### Related Use Case IDs

- UC-01

### Method

POST

### Path

/api/v1/auth/register

### Description

Accepts account-registration data and returns an authenticated session response.

### Authentication

Public

### Authorization

None

## Request Header(s)

### headers.Content-Type

Type: string; Format: MIME type; Required: Yes; Nullable: No

Trigger: Every registration request.

Description: Declares the request body media type.

Example: application/json

Note: Identifies the media type of the submitted request body.

Allowed value: application/json

Validation: Must identify a JSON request body.

## Path Parameter(s)

None.

## Query Parameter(s)

None.

## Request Body

### fullName

Type: string; Required: Yes; Nullable: No

Trigger: Registration request.

Description: Display name submitted for the account.

Example: Alex Morgan

Validation: Must be encoded as a JSON string.

### email

Type: string; Format: email; Required: Yes; Nullable: No

Trigger: Registration request.

Description: Email submitted for the account.

Example: alex@example.com

Validation: Must use email-address syntax.

### password

Type: string; Format: password; Required: Yes; Nullable: No

Trigger: Registration request.

Description: Password submitted for registration.

Example: Str0ng!Pass

Validation: Must be encoded as a JSON string.

### confirmPassword

Type: string; Format: password; Required: Yes; Nullable: No

Trigger: Registration request.

Description: Confirmation value submitted with the password.

Example: Str0ng!Pass

Validation: Must be encoded as a JSON string.

## Success Response — HTTP 201

### success

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response.

Description: Indicates successful completion.

Example: true

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response.

Description: Human-readable success message.

Example: Registration successful.

### data.accessToken

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Access token for authenticated API calls.

Example: eyJhbGciOiJIUzI1NiIs...

### data.expiresAt

Type: string; Format: ISO 8601 date-time; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Access-token expiration timestamp.

Example: 2026-09-19T10:30:00Z

### data.user.id

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.user object or array item is present and non-null.

Description: Created user identifier.

Example: usr_01JABCDEF

### data.user.fullName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.user object or array item is present and non-null.

Description: Created user's display name.

Example: Alex Morgan

### data.user.email

Type: string; Format: email; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data.user object or array item is present and non-null.

Description: Created user's email address.

Example: alex@example.com

## Error Response — HTTP 400

- Code: VALIDATION_ERROR
Trigger: The request cannot be decoded or does not match the declared wire schema.
Description: Protocol-level request error.
- Example message: The request payload is invalid.

## Error Response — HTTP 409

- Code: CONFLICT
Trigger: The registration request conflicts with the current account state.
Description: Public registration conflict.
- Example message: The registration request could not be completed.

## Error Response — HTTP 422

- Code: UNPROCESSABLE_REQUEST
Trigger: The syntactically valid request cannot be completed.
Description: Public processing failure.
- Example message: The request could not be completed.

## Error Response — HTTP 500

- Code: INTERNAL_ERROR
Trigger: An unexpected server error prevents registration.
Description: Unexpected registration-service failure.
- Example message: Internal Server Error

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md).

The response exposes only public user fields.
