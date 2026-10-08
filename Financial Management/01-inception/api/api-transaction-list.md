---
artifact_type: api-contract
status: Frozen
api_id: API-TRANSACTION-LIST
related_uc_ids: ["UC-03", "UC-17"]
---

# API-TRANSACTION-LIST: List Transactions

## General Information

### API ID

API-TRANSACTION-LIST

### API Name

List Transactions

### Related Use Case IDs

UC-03, UC-17

### Method

GET

### Path

/api/v1/transactions

### Description

Return the authenticated user's transactions with filtering and pagination.

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

None.

## Query Parameter(s)

### query.type

Type: string; Required: No; Nullable: No

Trigger: Request containing this field.

Description: Transaction type filter.

Example: All

Default: All

Allowed values: All; Revenue; Expense

Validation: Member of the declared public enum.

### query.limit

Type: integer; Required: No; Nullable: No

Trigger: Request containing this field.

Description: Maximum number of returned records.

Example: 10

Default: 10

Validation: JSON integer; query and path values use complete decimal text.

### query.offset

Type: integer; Required: No; Nullable: No

Trigger: Request containing this field.

Description: Zero-based pagination offset.

Example: 0

Default: 0

Validation: JSON integer; query and path values use complete decimal text.

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

Type: array<object>; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Transaction array. May be empty.

Example: []

Validation: JSON array<object>.

### data[].transaction_id

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Transactions.transaction_id.

Example: 8

Validation: JSON integer.

### data[].account_id

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Account identifier.

Example: 3

Validation: JSON integer.

### data[].transaction_date

Type: string; Format: date; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Transactions.transaction_date.

Example: 2025-11-01

Validation: Valid calendar date in YYYY-MM-DD representation.

### data[].type

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Transaction type.

Example: Expense

Allowed values: Revenue; Expense

Validation: Member of the declared public enum.

### data[].item_description

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Transactions.item_description.

Example: Movie Ticket

Validation: JSON string.

### data[].shop_name

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Transactions.shop_name.

Example: Cinema

Validation: JSON string.

### data[].amount

Type: number; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Transactions.amount.

Example: 150000

Validation: JSON number.

### data[].payment_method

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Transactions.payment_method.

Example: Credit Card

Validation: JSON string.

### data[].status

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Transaction status.

Example: Complete

Allowed values: Complete; Pending; Failed

Validation: Member of the declared public enum.

### total

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Integer count associated with the response.

Example: 25

Validation: JSON integer.

### hasMore

Type: boolean; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Boolean page continuation indicator.

Example: true

Validation: JSON boolean.

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

[Common wire contract](common-contract.md). Source: [API contract starting at row 136](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=439687549&range=A136:B152). These are reviewed contracts; compatibility changes are recorded in the package review. Child fields under a nullable object apply when that object is present.
