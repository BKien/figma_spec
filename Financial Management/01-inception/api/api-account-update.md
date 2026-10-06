---
artifact_type: api-contract
status: Draft
api_id: API-ACCOUNT-UPDATE
related_uc_id: UC-08
---

# API-ACCOUNT-UPDATE: Update Bank Account

## General Information

### API ID

`API-ACCOUNT-UPDATE`

### API Name

Update Bank Account

### Related Use Case IDs

`UC-08`

### Method

`PUT`

### Path

`/api/v1/accounts/{id}`

### Description

Update an account owned by the authenticated user.

### Authentication

Bearer JWT in the Authorization header.

### Authorization

Authenticated request context.

## Request Header(s)

### Authorization

Type: string
Required: Yes
Nullable: No
Validation: Matches the declared JSON type.
Trigger: Request containing this field.
Description: Bearer authentication header.
Example: `Bearer <access-token>`

### Content-Type

Type: string
Required: Yes
Nullable: No
Allowed values: application/json
Validation: Member of the declared public enum.
Trigger: Request containing this field.
Description: Body media type.
Example: `application/json`

## Path Parameter(s)

### path.id

Type: integer
Required: Yes
Nullable: No
Validation: JSON integer; query and path values use complete decimal text.
Trigger: Request containing this field.
Description: Account identifier.
Example: `3`

## Query Parameter(s)

None.

## Request Body

### bank_name

Type: string
Required: Yes
Nullable: No
Validation: Matches the declared JSON type.
Trigger: Request containing this field.
Description: Updated bank name.
Example: `Vietcombank`

### account_type

Type: string
Required: Yes
Nullable: No
Allowed values: Checking; Credit Card; Savings; Investment; Loan
Validation: Member of the declared public enum.
Trigger: Request containing this field.
Description: Updated account type.
Example: `Checking`

### branch_name

Type: string
Required: No
Nullable: Yes
Validation: Matches the declared JSON type.
Trigger: Request containing this field.
Description: Updated branch name.
Example: `Hanoi Branch`

### account_number_full

Type: string
Required: Yes
Nullable: No
Validation: Matches the declared JSON type.
Trigger: Request containing this field.
Description: Updated full account number.
Example: `9704221234567890123`

### balance

Type: number
Format: decimal
Required: Yes
Nullable: No
Validation: JSON number; query and path values use complete decimal text.
Trigger: Request containing this field.
Description: Updated balance.
Example: `4500000`

### expected_version

Type: integer
Required: Yes
Nullable: No
Validation: JSON integer; query and path values use complete decimal text.
Trigger: Request containing this field.
Description: Resource version supplied by the client.
Example: `1`

## Success Response — HTTP 200

### success

Type: boolean
Required: Yes
Nullable: No
Validation: JSON boolean.
Trigger: Response containing this field.
Description: Response outcome flag.
Example: `true`

### message

Type: string
Required: Yes
Nullable: No
Validation: JSON string.
Trigger: Response containing this field.
Description: Human-readable response message.
Example: `Operation completed`

### data

Type: object
Required: Yes
Nullable: No
Validation: JSON object.
Trigger: Response containing this field.
Description: Operation payload.
Example: `{}`

### data.id

Type: integer
Required: Yes
Nullable: No
Validation: JSON integer.
Trigger: Response containing this field.
Description: Updated account identifier.
Example: `3`

### data.user_id

Type: integer
Required: Yes
Nullable: No
Validation: JSON integer.
Trigger: Response containing this field.
Description: User identifier.
Example: `1`

### data.bank_name

Type: string
Required: Yes
Nullable: No
Validation: JSON string.
Trigger: Response containing this field.
Description: Updated bank name.
Example: `Vietcombank`

### data.account_type

Type: string
Required: Yes
Nullable: No
Allowed values: Checking; Credit Card; Savings; Investment; Loan
Validation: Member of the declared public enum.
Trigger: Response containing this field.
Description: Updated account type.
Example: `Checking`

### data.branch_name

Type: string
Required: Yes
Nullable: Yes
Validation: JSON string.
Trigger: Response containing this field.
Description: Updated branch name.
Example: `Hanoi Branch`

### data.account_number_last_4

Type: string
Required: Yes
Nullable: No
Validation: JSON string.
Trigger: Response containing this field.
Description: Updated final four digits.
Example: `0123`

### data.balance

Type: number
Required: Yes
Nullable: No
Validation: JSON number.
Trigger: Response containing this field.
Description: Updated balance.
Example: `4500000`

### data.version

Type: integer
Required: Yes
Nullable: No
Validation: JSON integer.
Trigger: Response containing this field.
Description: Resource version.
Example: `1`

## Error Response — HTTP 400

Public outcome: Malformed wire input or rejected operation.

### success

Type: boolean
Required: Yes
Nullable: No
Validation: JSON boolean.
Trigger: Response containing this field.
Description: Error outcome flag.
Example: `false`

### message

Type: string
Required: Yes
Nullable: No
Validation: JSON string.
Trigger: Response containing this field.
Description: Human-readable error message.
Example: `Request could not be completed`

### error

Type: object
Required: Yes
Nullable: No
Validation: JSON object.
Trigger: Response containing this field.
Description: Error payload.
Example: `{}`

### error.code

Type: string
Required: Yes
Nullable: No
Allowed values: MALFORMED_REQUEST
Validation: Member of the declared public enum.
Trigger: Response containing this field.
Description: Public error code.
Example: `MALFORMED_REQUEST`

## Error Response — HTTP 401

Public outcome: Rejected authentication context.

### success

Type: boolean
Required: Yes
Nullable: No
Validation: JSON boolean.
Trigger: Response containing this field.
Description: Error outcome flag.
Example: `false`

### message

Type: string
Required: Yes
Nullable: No
Validation: JSON string.
Trigger: Response containing this field.
Description: Human-readable error message.
Example: `Request could not be completed`

### error

Type: object
Required: Yes
Nullable: No
Validation: JSON object.
Trigger: Response containing this field.
Description: Error payload.
Example: `{}`

### error.code

Type: string
Required: Yes
Nullable: No
Allowed values: UNAUTHENTICATED
Validation: Member of the declared public enum.
Trigger: Response containing this field.
Description: Public error code.
Example: `UNAUTHENTICATED`

## Error Response — HTTP 404

Public outcome: Unavailable resource response.

### success

Type: boolean
Required: Yes
Nullable: No
Validation: JSON boolean.
Trigger: Response containing this field.
Description: Error outcome flag.
Example: `false`

### message

Type: string
Required: Yes
Nullable: No
Validation: JSON string.
Trigger: Response containing this field.
Description: Human-readable error message.
Example: `Request could not be completed`

### error

Type: object
Required: Yes
Nullable: No
Validation: JSON object.
Trigger: Response containing this field.
Description: Error payload.
Example: `{}`

### error.code

Type: string
Required: Yes
Nullable: No
Allowed values: NOT_FOUND
Validation: Member of the declared public enum.
Trigger: Response containing this field.
Description: Public error code.
Example: `NOT_FOUND`

## Error Response — HTTP 409

Public outcome: Operation conflict.

### success

Type: boolean
Required: Yes
Nullable: No
Validation: JSON boolean.
Trigger: Response containing this field.
Description: Error outcome flag.
Example: `false`

### message

Type: string
Required: Yes
Nullable: No
Validation: JSON string.
Trigger: Response containing this field.
Description: Human-readable error message.
Example: `Request could not be completed`

### error

Type: object
Required: Yes
Nullable: No
Validation: JSON object.
Trigger: Response containing this field.
Description: Error payload.
Example: `{}`

### error.code

Type: string
Required: Yes
Nullable: No
Allowed values: OPERATION_CONFLICT
Validation: Member of the declared public enum.
Trigger: Response containing this field.
Description: Public error code.
Example: `OPERATION_CONFLICT`

## Error Response — HTTP 500

Public outcome: Temporary service failure.

### success

Type: boolean
Required: Yes
Nullable: No
Validation: JSON boolean.
Trigger: Response containing this field.
Description: Error outcome flag.
Example: `false`

### message

Type: string
Required: Yes
Nullable: No
Validation: JSON string.
Trigger: Response containing this field.
Description: Human-readable error message.
Example: `Request could not be completed`

### error

Type: object
Required: Yes
Nullable: No
Validation: JSON object.
Trigger: Response containing this field.
Description: Error payload.
Example: `{}`

### error.code

Type: string
Required: Yes
Nullable: No
Allowed values: INTERNAL_ERROR
Validation: Member of the declared public enum.
Trigger: Response containing this field.
Description: Public error code.
Example: `INTERNAL_ERROR`

## Notes

[Common wire contract](common-contract.md). Source: [API contract starting at row 95](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=439687549&range=A95:B111). These are reviewed contracts; compatibility changes are recorded in the package review. Child fields under a nullable object apply when that object is present.
