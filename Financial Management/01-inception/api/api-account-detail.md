---
artifact_type: api-contract
status: Frozen
api_id: API-ACCOUNT-DETAIL
related_uc_ids: ["UC-07", "UC-08"]
---

# API-ACCOUNT-DETAIL: Get Account Details

## General Information

### API ID

API-ACCOUNT-DETAIL

### API Name

Get Account Details

### Related Use Case IDs

UC-07, UC-08

### Method

GET

### Path

/api/v1/accounts/{id}

### Description

Return one owned account and its five most recent transactions.

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

None.

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

Description: Account identifier.

Example: 3

Validation: JSON integer.

### data.bank_name

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Bank name.

Example: Vietcombank

Validation: JSON string.

### data.account_type

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Account type.

Example: Checking

Allowed values: Checking; Credit Card; Savings; Investment; Loan

Validation: Member of the declared public enum.

### data.branch_name

Type: string; Required: Yes; Nullable: Yes

Trigger: Response containing this field.

Description: Branch name.

Example: Hanoi Branch

Validation: JSON string.

### data.account_number_full

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Full account number.

Example: 9704221234567890123

Validation: JSON string.

### data.balance

Type: number; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Current balance.

Example: 4500000

Validation: JSON number.

### data.recent_transactions

Type: array<object>; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Recent transaction array.

Example: []

Validation: JSON array<object>.

### data.recent_transactions[].date

Type: string; Format: date; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Transaction date.

Example: 2025-11-01

Validation: Valid calendar date in YYYY-MM-DD representation.

### data.recent_transactions[].amount

Type: number; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Signed transaction amount.

Example: -150000

Validation: JSON number.

### data.recent_transactions[].description

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Transaction description.

Example: Movie Ticket

Validation: JSON string.

### data.recent_transactions[].status

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Transaction status.

Example: Complete

Allowed values: Complete; Pending; Failed

Validation: Member of the declared public enum.

### data.recent_transactions[].receipt_id

Type: string; Required: Yes; Nullable: Yes

Trigger: Response containing this field.

Description: Receipt identifier.

Example: null

Validation: JSON string.

### data.recent_transactions[].type

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Transaction type.

Example: Expense

Allowed values: Revenue; Expense

Validation: Member of the declared public enum.

### data.recent_transactions[].transaction_id

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Transaction identifier.

Example: 8

Validation: JSON integer.

### data.version

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Resource version.

Example: 1

Response header: ETag, type string, required, non-null; example "1".

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

[Common wire contract](common-contract.md). Source: [API contract starting at row 74](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=439687549&range=A74:B90). These are reviewed contracts; compatibility changes are recorded in the package review. Child fields under a nullable object apply when that object is present.
