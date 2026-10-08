---
artifact_type: api-contract
status: Frozen
api_id: API-EXPENSE-BREAKDOWN
related_uc_id: UC-11
---

# API-EXPENSE-BREAKDOWN: Get Expense Breakdown by Category

## General Information

### API ID

API-EXPENSE-BREAKDOWN

### API Name

Get Expense Breakdown by Category

### Related Use Case IDs

UC-11

### Method

GET

### Path

/api/v1/expenses/breakdown

### Description

Return the authenticated user's expense breakdown by category for a selected month.

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

### query.month

Type: string; Format: YYYY-MM; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: Month selected by the user.

Example: 2025-11

Validation: Calendar month in YYYY-MM representation.

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

Description: Expense breakdown results for the selected month.

Example: []

Validation: JSON array<object>.

### data[].category

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Category label for the group.

Example: Entertainment

Validation: JSON string.

### data[].total

Type: number; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Total expense amount for the category group.

Example: 1500000

Validation: JSON number.

### data[].changePercent

Type: number; Required: Yes; Nullable: Yes

Trigger: Response containing this field.

Description: Percentage change compared with the previous month.

Example: 25.5

Validation: JSON number.

### data[].subCategories

Type: array<object>; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Underlying transaction details for the category group.

Example: []

Validation: JSON array<object>.

### data[].subCategories[].item_description

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Transaction description.

Example: Movie Ticket

Validation: JSON string.

### data[].subCategories[].amount

Type: number; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Transaction amount.

Example: 150000

Validation: JSON number.

### data[].subCategories[].date

Type: string; Format: date; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Transaction date.

Example: 2025-11-01

Validation: Valid calendar date in YYYY-MM-DD representation.

### data[].category_id

Type: integer; Required: Yes; Nullable: Yes

Trigger: Response containing this field.

Description: Category group identifier.

Example: 3

Validation: JSON integer.

### data[].subCategories[].transaction_id

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Transaction identifier.

Example: 8

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

[Common wire contract](common-contract.md). Source: [API contract starting at row 222](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=439687549&range=A222:B238). These are reviewed contracts; compatibility changes are recorded in the package review. Child fields under a nullable object apply when that object is present.
