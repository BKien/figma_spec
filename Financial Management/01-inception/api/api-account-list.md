---
artifact_type: api-contract
status: Draft
api_id: API-ACCOUNT-LIST
related_uc_ids: ["UC-04", "UC-05"]
---

# API-ACCOUNT-LIST: List User Accounts

## General Information

### API ID

`API-ACCOUNT-LIST`

### API Name

List User Accounts

### Related Use Case IDs

`UC-04`, `UC-05`

### Method

`GET`

### Path

`/api/v1/accounts`

### Description

Return all bank accounts owned by the authenticated user.

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

## Path Parameter(s)

None.

## Query Parameter(s)

None.

## Request Body

None.

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

### data.user_id

Type: integer
Required: Yes
Nullable: No
Validation: JSON integer.
Trigger: Response containing this field.
Description: Authenticated user identifier.
Example: `1`

### data.accounts

Type: array<object>
Required: Yes
Nullable: No
Validation: JSON array<object>.
Trigger: Response containing this field.
Description: Array of accounts. May be empty.
Example: `[]`

### data.accounts[].id

Type: integer
Required: Yes
Nullable: No
Validation: JSON integer.
Trigger: Response containing this field.
Description: Account identifier.
Example: `3`

### data.accounts[].bank_name

Type: string
Required: Yes
Nullable: No
Validation: JSON string.
Trigger: Response containing this field.
Description: Bank or financial institution name.
Example: `Vietcombank`

### data.accounts[].account_type

Type: string
Required: Yes
Nullable: No
Allowed values: Checking; Credit Card; Savings; Investment; Loan
Validation: Member of the declared public enum.
Trigger: Response containing this field.
Description: Account type.
Example: `Checking`

### data.accounts[].branch_name

Type: string
Required: Yes
Nullable: Yes
Validation: JSON string.
Trigger: Response containing this field.
Description: Branch name.
Example: `Hanoi Branch`

### data.accounts[].account_number_last_4

Type: string
Required: Yes
Nullable: No
Validation: JSON string.
Trigger: Response containing this field.
Description: Last four digits of the account number.
Example: `0123`

### data.accounts[].balance

Type: number
Required: Yes
Nullable: No
Validation: JSON number.
Trigger: Response containing this field.
Description: Current account balance.
Example: `4500000`

### data.accounts[].version

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

[Common wire contract](common-contract.md). Source: [API contract starting at row 39](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=439687549&range=A39:B55). These are reviewed contracts; compatibility changes are recorded in the package review. Child fields under a nullable object apply when that object is present.
