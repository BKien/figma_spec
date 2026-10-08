---
artifact_type: api-contract
status: Frozen
api_id: API-TRANSACTION-CREATE
related_uc_id: UC-04
---

# API-TRANSACTION-CREATE: Create Transaction

## General Information

### API ID

API-TRANSACTION-CREATE

### API Name

Create Transaction

### Related Use Case IDs

UC-04

### Method

POST

### Path

/api/v1/transactions

### Description

Create a revenue or expense transaction and update the account balance atomically.

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

None.

## Query Parameter(s)

None.

## Request Body

### accountId

Type: integer; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: Account identifier.

Example: 3

Validation: JSON integer; query and path values use complete decimal text.

### transactionDate

Type: string; Format: date; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: 

Example: 2025-11-01

Validation: Valid calendar date in YYYY-MM-DD representation.

### type

Type: string; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: 

Example: Expense

Allowed values: Revenue; Expense

Validation: Member of the declared public enum.

### itemDescription

Type: string; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: 

Example: Movie Ticket

Validation: Matches the declared JSON type.

### category_id

Type: integer; Required: No; Nullable: Yes

Trigger: Request containing this field.

Description: Optional transaction category; maps to Transactions.category_id.

Example: 3

Validation: JSON integer; query and path values use complete decimal text.

### shopName

Type: string; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: 

Example: Cinema

Validation: Matches the declared JSON type.

### amount

Type: number; Format: decimal; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: 

Example: 150000

Validation: JSON number; query and path values use complete decimal text.

### paymentMethod

Type: string; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: 

Example: Credit Card

Validation: Matches the declared JSON type.

### status

Type: string; Required: No; Nullable: No

Trigger: Request containing this field.

Description: 

Example: Complete

Default: Complete

Allowed values: Complete; Pending; Failed

Validation: Member of the declared public enum.

### expected_version

Type: integer; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: Resource version supplied by the client.

Example: 1

Validation: JSON integer; query and path values use complete decimal text.

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

### data.transactionId

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Created transaction identifier.

Example: 8

Validation: JSON integer.

### data.accountId

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Related account identifier.

Example: 3

Validation: JSON integer.

### data.transactionDate

Type: string; Format: date-time; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Stored transaction date.

Example: example

Validation: RFC 3339 date-time representation.

### data.type

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Stored transaction type.

Example: Expense

Allowed values: Revenue; Expense

Validation: Member of the declared public enum.

### data.itemDescription

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Stored description.

Example: Movie Ticket

Validation: JSON string.

### data.shopName

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Stored merchant name from Transactions.shop_name.

Example: Cinema

Validation: JSON string.

### data.amount

Type: number; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Stored amount.

Example: 150000

Validation: JSON number.

### data.paymentMethod

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Stored payment method from Transactions.payment_method.

Example: Credit Card

Validation: JSON string.

### data.status

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Stored status.

Example: Complete

Allowed values: Complete; Pending; Failed

Validation: Member of the declared public enum.

### data.receiptId

Type: string; Required: Yes; Nullable: Yes

Trigger: Response containing this field.

Description: Receipt identifier.

Example: null

Validation: JSON string.

### data.createdAt

Type: string; Format: date-time; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Creation timestamp.

Example: 2026-09-30T03:00:00Z

Validation: RFC 3339 date-time representation.

### data.category_id

Type: integer; Required: Yes; Nullable: Yes

Trigger: Response containing this field.

Description: Stored optional category identifier.

Example: 3

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

[Common wire contract](common-contract.md). Source: [API contract starting at row 155](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=439687549&range=A155:B171). These are reviewed contracts; compatibility changes are recorded in the package review. Child fields under a nullable object apply when that object is present.
