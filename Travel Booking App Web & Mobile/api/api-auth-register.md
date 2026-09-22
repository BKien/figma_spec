# API-AUTH-REGISTER — Register an Account

## API ID

`API-AUTH-REGISTER`

## API Name

User Registration

## Related Use Case IDs

- `UC-01`

## Method

`POST`

## Path

`/api/v1/auth/register`

## Description

Accepts account-registration data and returns an authenticated session response.

## Authentication

Public

## Authorization

None

## Request Headers

### `Content-Type`

- Type: string
- Format: MIME type
- Required: Yes
- Nullable: No
- Allowed value: `application/json`
- Validation: Must identify a JSON request body.
- Trigger: Every registration request.
- Description: Declares the request body media type.
- Example: `application/json`

## Path Parameters

None.

## Query Parameters

None.

## Request Body

### `fullName`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Trigger: Registration request.
- Description: Display name submitted for the account.
- Example: `Alex Morgan`

### `email`

- Type: string
- Format: email
- Required: Yes
- Nullable: No
- Validation: Must use email-address syntax.
- Trigger: Registration request.
- Description: Email submitted for the account.
- Example: `alex@example.com`

### `password`

- Type: string
- Format: password
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Trigger: Registration request.
- Description: Password submitted for registration.
- Example: `Str0ng!Pass`

### `confirmPassword`

- Type: string
- Format: password
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Trigger: Registration request.
- Description: Confirmation value submitted with the password.
- Example: `Str0ng!Pass`

## Success Response — HTTP 201

### `success`

- Type: boolean
- Required: Yes
- Nullable: No
- Description: Indicates successful completion.
- Example: `true`

### `message`

- Type: string
- Required: Yes
- Nullable: No
- Description: Human-readable success message.
- Example: `Registration successful.`

### `data.accessToken`

- Type: string
- Required: Yes
- Nullable: No
- Description: Access token for authenticated API calls.
- Example: `eyJhbGciOiJIUzI1NiIs...`

### `data.expiresAt`

- Type: string
- Format: ISO 8601 date-time
- Required: Yes
- Nullable: No
- Description: Access-token expiration timestamp.
- Example: `2026-09-19T10:30:00Z`

### `data.user.id`

- Type: string
- Required: Yes
- Nullable: No
- Description: Created user identifier.
- Example: `usr_01JABCDEF`

### `data.user.fullName`

- Type: string
- Required: Yes
- Nullable: No
- Description: Created user's display name.
- Example: `Alex Morgan`

### `data.user.email`

- Type: string
- Format: email
- Required: Yes
- Nullable: No
- Description: Created user's email address.
- Example: `alex@example.com`

## Error Response — HTTP 400

- Code: `VALIDATION_ERROR`
- Trigger: The request cannot be decoded or does not match the declared wire schema.
- Description: Protocol-level request error.
- Example message: `The request payload is invalid.`

## Error Response — HTTP 409

- Code: `CONFLICT`
- Trigger: The registration request conflicts with the current account state.
- Description: Public registration conflict.
- Example message: `The registration request could not be completed.`

## Error Response — HTTP 422

- Code: `UNPROCESSABLE_REQUEST`
- Trigger: The syntactically valid request cannot be completed.
- Description: Public processing failure.
- Example message: `The request could not be completed.`

## Error Response — HTTP 500

- Code: `INTERNAL_ERROR`
- Trigger: An unexpected server error prevents registration.
- Description: Unexpected registration-service failure.
- Example message: `Internal Server Error`

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md).

The response exposes only public user fields.
