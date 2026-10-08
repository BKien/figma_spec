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

UC-01

### Method

POST

### Path

/api/auth/register

### Description

Create a new user account and issue a JWT token.

### Authentication

Public.

### Authorization

None.

## Request Header(s)

### headers.Content-Type

Type: string; Format: HTTP media type; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: Body media type.

Example: application/json

Note: Identifies the media type of the submitted request body.

Allowed values: application/json

Validation: Member of the declared public enum.

## Path Parameter(s)

None.

## Query Parameter(s)

None.

## Request Body

### fullName

Type: string; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: User's full name.

Example: John Doe

Validation: Matches the declared JSON type.

### email

Type: string; Format: email; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: Unique email address.

Example: user@example.com

Validation: Email-address syntax.

### password

Type: string; Format: password; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: New password.

Example: P@ssw0rd!

Validation: Matches the declared JSON type.

### confirmPassword

Type: string; Format: password; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: Password confirmation.

Example: P@ssw0rd!

Validation: Matches the declared JSON type.

## Success Response — HTTP 201

### success

Type: boolean; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Response outcome flag.

Example: true

Validation: JSON boolean.

### message

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Human-readable response message.

Example: Operation completed

Validation: JSON string.

### data

Type: object; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Operation payload.

Example: {}

Validation: JSON object.

### data.user

Type: object; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Nested response object.

Example: {}

Validation: JSON object.

### data.accessToken

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: JWT access token issued for the created user.

Example: eyJhbGciOiJIUzI1NiIs...

Validation: JSON string.

### data.user.id

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Created user identifier.

Example: 1

Validation: JSON integer.

### data.user.fullName

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Normalized full name of the created user.

Example: John Doe

Validation: JSON string.

### data.user.email

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Normalized email address of the created user.

Example: user@example.com

Validation: JSON string.

## Error Response — HTTP 400

Public outcome: Malformed wire input or rejected operation.

### success

Type: boolean; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Error outcome flag.

Example: false

Note: Field of the JSON error response.

Validation: JSON boolean.

### message

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Human-readable error message.

Example: Request could not be completed

Note: Field of the JSON error response.

Validation: JSON string.

### error

Type: object; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Error payload.

Example: {}

Note: Field of the JSON error response.

Validation: JSON object.

### error.code

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Public error code.

Example: MALFORMED_REQUEST

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Allowed values: MALFORMED_REQUEST

Validation: Member of the declared public enum.

## Error Response — HTTP 409

Public outcome: Operation conflict.

### success

Type: boolean; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Error outcome flag.

Example: false

Note: Field of the JSON error response.

Validation: JSON boolean.

### message

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Human-readable error message.

Example: Request could not be completed

Note: Field of the JSON error response.

Validation: JSON string.

### error

Type: object; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Error payload.

Example: {}

Note: Field of the JSON error response.

Validation: JSON object.

### error.code

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Public error code.

Example: OPERATION_CONFLICT

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Allowed values: OPERATION_CONFLICT

Validation: Member of the declared public enum.

## Error Response — HTTP 500

Public outcome: Temporary service failure.

### success

Type: boolean; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Error outcome flag.

Example: false

Note: Field of the JSON error response.

Validation: JSON boolean.

### message

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Human-readable error message.

Example: Request could not be completed

Note: Field of the JSON error response.

Validation: JSON string.

### error

Type: object; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Error payload.

Example: {}

Note: Field of the JSON error response.

Validation: JSON object.

### error.code

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Public error code.

Example: INTERNAL_ERROR

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Allowed values: INTERNAL_ERROR

Validation: Member of the declared public enum.

## Notes

[Common wire contract](common-contract.md). Source: [API contract starting at row 21](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=439687549&range=A21:B37). These are reviewed contracts; compatibility changes are recorded in the package review. Child fields under a nullable object apply when that object is present.
