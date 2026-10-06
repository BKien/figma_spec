---
artifact_type: api-contract
status: Draft
api_id: API-TRANSACTION-LIST
related_uc_ids: ["UC-03", "UC-17"]
---

# API-TRANSACTION-LIST: List Transactions

## General Information

### API ID

`API-TRANSACTION-LIST`

### API Name

List Transactions

### Related Use Case IDs

`UC-03`, `UC-17`

### Method

`GET`

### Path

`/api/v1/transactions`

### Description

Return the authenticated user's transactions with filtering and pagination.

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

### query.type

Type: string
Required: No
Nullable: No
Default: All
Allowed values: All; Revenue; Expense
Validation: Member of the declared public enum.
Trigger: Request containing this field.
Description: Transaction type filter.
Example: `All`

### query.limit

Type: integer
Required: No
Nullable: No
Default: 10
Validation: JSON integer; query and path values use complete decimal text.
Trigger: Request containing this field.
Description: Maximum number of returned records.
Example: `10`

### query.offset

Type: integer
Required: No
Nullable: No
Default: 0
Validation: JSON integer; query and path values use complete decimal text.
Trigger: Request containing this field.
Description: Zero-based pagination offset.
Example: `0`

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

Type: array<object>
Required: Yes
Nullable: No
Validation: JSON array<object>.
Trigger: Response containing this field.
Description: Transaction array. May be empty.
Example: `[]`

### data[].transaction_id

Type: integer
Required: Yes
Nullable: No
Validation: JSON integer.
Trigger: Response containing this field.
Description: Transactions.transaction_id.
Example: `8`

### data[].account_id

Type: integer
Required: Yes
Nullable: No
Validation: JSON integer.
Trigger: Response containing this field.
Description: Account identifier.
Example: `3`

### data[].transaction_date

Type: string
Format: date
Required: Yes
Nullable: No
Validation: Valid calendar date in YYYY-MM-DD representation.
Trigger: Response containing this field.
Description: Transactions.transaction_date.
Example: `2025-11-01`

### data[].type

Type: string
Required: Yes
Nullable: No
Allowed values: Revenue; Expense
Validation: Member of the declared public enum.
Trigger: Response containing this field.
Description: Transaction type.
Example: `Expense`

### data[].item_description

Type: string
Required: Yes
Nullable: No
Validation: JSON string.
Trigger: Response containing this field.
Description: Transactions.item_description.
Example: `Movie Ticket`

### data[].shop_name

Type: string
Required: Yes
Nullable: No
Validation: JSON string.
Trigger: Response containing this field.
Description: Transactions.shop_name.
Example: `Cinema`

### data[].amount

Type: number
Required: Yes
Nullable: No
Validation: JSON number.
Trigger: Response containing this field.
Description: Transactions.amount.
Example: `150000`

### data[].payment_method

Type: string
Required: Yes
Nullable: No
Validation: JSON string.
Trigger: Response containing this field.
Description: Transactions.payment_method.
Example: `Credit Card`

### data[].status

Type: string
Required: Yes
Nullable: No
Allowed values: Complete; Pending; Failed
Validation: Member of the declared public enum.
Trigger: Response containing this field.
Description: Transaction status.
Example: `Complete`

### total

Type: integer
Required: Yes
Nullable: No
Validation: JSON integer.
Trigger: Response containing this field.
Description: Integer count associated with the response.
Example: `25`

### hasMore

Type: boolean
Required: Yes
Nullable: No
Validation: JSON boolean.
Trigger: Response containing this field.
Description: Boolean page continuation indicator.
Example: `true`

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

[Common wire contract](common-contract.md). Source: [API contract starting at row 136](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=439687549&range=A136:B152). These are reviewed contracts; compatibility changes are recorded in the package review. Child fields under a nullable object apply when that object is present.
