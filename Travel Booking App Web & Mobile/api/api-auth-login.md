# API-AUTH-LOGIN — Log In

## API ID

`API-AUTH-LOGIN`

## API Name

User Login

## Related Use Case IDs

- `UC-02`

## Method

`POST`

## Path

`/api/v1/auth/login`

## Description

Authenticates a submitted credential set and returns an access-token response.

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
- Trigger: Every request containing the login body.
- Description: Declares the request body media type.
- Example: `application/json`

## Path Parameters

None.

## Query Parameters

None.

## Request Body

### `email`

- Type: string
- Format: email
- Required: Yes
- Nullable: No
- Validation: Must use email-address syntax.
- Trigger: Login request.
- Description: Email submitted as part of the credential set.
- Example: `alex@example.com`

### `password`

- Type: string
- Format: password
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Trigger: Login request.
- Description: Password submitted as part of the credential set.
- Example: `Str0ng!Pass`

## Success Response — HTTP 200

### `success`

- Type: boolean
- Required: Yes
- Nullable: No
- Trigger: The authentication request succeeds.
- Description: Indicates successful completion.
- Example: `true`

### `message`

- Type: string
- Required: Yes
- Nullable: No
- Trigger: The authentication request succeeds.
- Description: Human-readable success message.
- Example: `Login successful.`

### `data.accessToken`

- Type: string
- Required: Yes
- Nullable: No
- Trigger: The authentication request succeeds.
- Description: Access token for authenticated API calls.
- Example: `eyJhbGciOiJIUzI1NiIs...`

### `data.expiresAt`

- Type: string
- Format: ISO 8601 date-time
- Required: Yes
- Nullable: No
- Trigger: The authentication request succeeds.
- Description: Access-token expiration timestamp.
- Example: `2026-09-19T10:30:00Z`

### `data.user.id`

- Type: string
- Required: Yes
- Nullable: No
- Description: Authenticated user identifier.
- Example: `usr_01JABCDEF`

### `data.user.fullName`

- Type: string
- Required: Yes
- Nullable: No
- Description: Authenticated user's display name.
- Example: `Alex Morgan`

### `data.user.email`

- Type: string
- Format: email
- Required: Yes
- Nullable: No
- Description: Authenticated user's email address.
- Example: `alex@example.com`

## Error Response — HTTP 400

- Code: `VALIDATION_ERROR`
- Trigger: The request cannot be decoded or does not match the declared wire schema.
- Description: Protocol-level request error.
- Example message: `The request payload is invalid.`

## Error Response — HTTP 401

- Code: `INVALID_CREDENTIALS`
- Trigger: The authentication request is not accepted.
- Description: Public authentication failure.
- Example message: `The submitted credentials could not be accepted.`

## Error Response — HTTP 500

- Code: `INTERNAL_ERROR`
- Trigger: An unexpected server error prevents authentication.
- Description: Unexpected authentication-service failure.
- Example message: `Internal Server Error`

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md).

Response envelopes follow the common API contract.
