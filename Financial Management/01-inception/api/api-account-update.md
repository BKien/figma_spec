---
artifact_type: api-contract
status: Frozen
api_id: API-ACCOUNT-UPDATE
related_uc_id: UC-08
---

# API-ACCOUNT-UPDATE: Update Bank Account

## General Information

### API ID

API-ACCOUNT-UPDATE

### API Name

Update Bank Account

### Related Use Case IDs

UC-08

### Method

PUT

### Path

/api/v1/accounts/{id}

### Description

Update an account owned by the authenticated user.

### Authentication

Bearer JWT in the Authorization header.

### Authorization

Authenticated request context.

## Request Header(s)

### headers.Authorization

Type: string; Format: Bearer token; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: Bearer authentication header.

Example: Bearer <access-token>

Note: Uses the HTTP Bearer authentication scheme.

Validation: Matches the declared JSON type.

### headers.Content-Type

Type: string; Format: HTTP media type; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: Body media type.

Example: application/json

Note: Identifies the media type of the submitted request body.

Allowed values: application/json

Validation: Member of the declared public enum.

## Path Parameter(s)

### path.id

Type: integer; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: Account identifier.

Example: 3

Validation: JSON integer; query and path values use complete decimal text.

## Query Parameter(s)

None.

## Request Body

### bank_name

Type: string; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: Updated bank name.

Example: Vietcombank

Validation: Matches the declared JSON type.

### account_type

Type: string; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: Updated account type.

Example: Checking

Allowed values: Checking; Credit Card; Savings; Investment; Loan

Validation: Member of the declared public enum.

### branch_name

Type: string; Required: No; Nullable: Yes

Trigger: Request containing this field.

Description: Updated branch name.

Example: Hanoi Branch

Validation: Matches the declared JSON type.

### account_number_full

Type: string; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: Updated full account number.

Example: 9704221234567890123

Validation: Matches the declared JSON type.

### balance

Type: number; Format: decimal; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: Updated balance.

Example: 4500000

Validation: JSON number; query and path values use complete decimal text.

### expected_version

Type: integer; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: Resource version supplied by the client.

Example: 1

Validation: JSON integer; query and path values use complete decimal text.

## Success Response — HTTP 200

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

### data.id

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Updated account identifier.

Example: 3

Validation: JSON integer.

### data.user_id

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: User identifier.

Example: 1

Validation: JSON integer.

### data.bank_name

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Updated bank name.

Example: Vietcombank

Validation: JSON string.

### data.account_type

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Updated account type.

Example: Checking

Allowed values: Checking; Credit Card; Savings; Investment; Loan

Validation: Member of the declared public enum.

### data.branch_name

Type: string; Required: Yes; Nullable: Yes

Trigger: Response containing this field.

Description: Updated branch name.

Example: Hanoi Branch

Validation: JSON string.

### data.account_number_last_4

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Updated final four digits.

Example: 0123

Validation: JSON string.

### data.balance

Type: number; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Updated balance.

Example: 4500000

Validation: JSON number.

### data.version

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Resource version.

Example: 1

Validation: JSON integer.

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

## Error Response — HTTP 401

Public outcome: Rejected authentication context.

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

Example: UNAUTHENTICATED

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Allowed values: UNAUTHENTICATED

Validation: Member of the declared public enum.

## Error Response — HTTP 404

Public outcome: Unavailable resource response.

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

Example: NOT_FOUND

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Allowed values: NOT_FOUND

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

[Common wire contract](common-contract.md). Source: [API contract starting at row 95](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=439687549&range=A95:B111). These are reviewed contracts; compatibility changes are recorded in the package review. Child fields under a nullable object apply when that object is present.
