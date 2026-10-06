---
artifact_type: api-contract
status: Draft
api_id: API-TRANSACTION-CREATE
related_uc_id: UC-04
---

# API-TRANSACTION-CREATE: Create Transaction

## General Information

### API ID

`API-TRANSACTION-CREATE`

### API Name

Create Transaction

### Related Use Case IDs

`UC-04`

### Method

`POST`

### Path

`/api/v1/transactions`

### Description

Create a revenue or expense transaction and update the account balance atomically.

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

None.

## Query Parameter(s)

None.

## Request Body

### accountId

Type: integer
Required: Yes
Nullable: No
Validation: JSON integer; query and path values use complete decimal text.
Trigger: Request containing this field.
Description: Account identifier.
Example: `3`

### transactionDate

Type: string
Format: date
Required: Yes
Nullable: No
Validation: Valid calendar date in YYYY-MM-DD representation.
Trigger: Request containing this field.
Description: 
Example: `2025-11-01`

### type

Type: string
Required: Yes
Nullable: No
Allowed values: Revenue; Expense
Validation: Member of the declared public enum.
Trigger: Request containing this field.
Description: 
Example: `Expense`

### itemDescription

Type: string
Required: Yes
Nullable: No
Validation: Matches the declared JSON type.
Trigger: Request containing this field.
Description: 
Example: `Movie Ticket`

### category_id

Type: integer
Required: No
Nullable: Yes
Validation: JSON integer; query and path values use complete decimal text.
Trigger: Request containing this field.
Description: Optional transaction category; maps to Transactions.category_id.
Example: `3`

### shopName

Type: string
Required: Yes
Nullable: No
Validation: Matches the declared JSON type.
Trigger: Request containing this field.
Description: 
Example: `Cinema`

### amount

Type: number
Format: decimal
Required: Yes
Nullable: No
Validation: JSON number; query and path values use complete decimal text.
Trigger: Request containing this field.
Description: 
Example: `150000`

### paymentMethod

Type: string
Required: Yes
Nullable: No
Validation: Matches the declared JSON type.
Trigger: Request containing this field.
Description: 
Example: `Credit Card`

### status

Type: string
Required: No
Nullable: No
Default: Complete
Allowed values: Complete; Pending; Failed
Validation: Member of the declared public enum.
Trigger: Request containing this field.
Description: 
Example: `Complete`

### expected_version

Type: integer
Required: Yes
Nullable: No
Validation: JSON integer; query and path values use complete decimal text.
Trigger: Request containing this field.
Description: Resource version supplied by the client.
Example: `1`

## Success Response — HTTP 201

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

### data.transactionId

Type: integer
Required: Yes
Nullable: No
Validation: JSON integer.
Trigger: Response containing this field.
Description: Created transaction identifier.
Example: `8`

### data.accountId

Type: integer
Required: Yes
Nullable: No
Validation: JSON integer.
Trigger: Response containing this field.
Description: Related account identifier.
Example: `3`

### data.transactionDate

Type: string
Format: date-time
Required: Yes
Nullable: No
Validation: RFC 3339 date-time representation.
Trigger: Response containing this field.
Description: Stored transaction date.
Example: `example`

### data.type

Type: string
Required: Yes
Nullable: No
Allowed values: Revenue; Expense
Validation: Member of the declared public enum.
Trigger: Response containing this field.
Description: Stored transaction type.
Example: `Expense`

### data.itemDescription

Type: string
Required: Yes
Nullable: No
Validation: JSON string.
Trigger: Response containing this field.
Description: Stored description.
Example: `Movie Ticket`

### data.shopName

Type: string
Required: Yes
Nullable: No
Validation: JSON string.
Trigger: Response containing this field.
Description: Stored merchant name from Transactions.shop_name.
Example: `Cinema`

### data.amount

Type: number
Required: Yes
Nullable: No
Validation: JSON number.
Trigger: Response containing this field.
Description: Stored amount.
Example: `150000`

### data.paymentMethod

Type: string
Required: Yes
Nullable: No
Validation: JSON string.
Trigger: Response containing this field.
Description: Stored payment method from Transactions.payment_method.
Example: `Credit Card`

### data.status

Type: string
Required: Yes
Nullable: No
Allowed values: Complete; Pending; Failed
Validation: Member of the declared public enum.
Trigger: Response containing this field.
Description: Stored status.
Example: `Complete`

### data.receiptId

Type: string
Required: Yes
Nullable: Yes
Validation: JSON string.
Trigger: Response containing this field.
Description: Receipt identifier.
Example: `null`

### data.createdAt

Type: string
Format: date-time
Required: Yes
Nullable: No
Validation: RFC 3339 date-time representation.
Trigger: Response containing this field.
Description: Creation timestamp.
Example: `2026-09-30T03:00:00Z`

### data.category_id

Type: integer
Required: Yes
Nullable: Yes
Validation: JSON integer.
Trigger: Response containing this field.
Description: Stored optional category identifier.
Example: `3`

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

[Common wire contract](common-contract.md). Source: [API contract starting at row 155](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=439687549&range=A155:B171). These are reviewed contracts; compatibility changes are recorded in the package review. Child fields under a nullable object apply when that object is present.
