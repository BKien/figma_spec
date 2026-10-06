---
artifact_type: api-contract
status: Draft
api_id: API-GOAL-LIST
related_uc_ids: ["UC-13", "UC-15"]
---

# API-GOAL-LIST: List Financial Goals

## General Information

### API ID

`API-GOAL-LIST`

### API Name

List Financial Goals

### Related Use Case IDs

`UC-13`, `UC-15`

### Method

`GET`

### Path

`/api/v1/goals`

### Description

Return financial-goal data for the authenticated user's Goals view.

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

### data.savingGoal

Type: object
Required: Yes
Nullable: Yes
Validation: JSON object.
Trigger: Response containing this field.
Description: Saving-goal data when available.
Example: `null`

### data.savingGoal.goal_id

Type: integer
Required: Yes
Nullable: No
Validation: JSON integer.
Trigger: Response containing this field.
Description: Saving goal identifier.
Example: `2`

### data.savingGoal.goal_type

Type: string
Required: Yes
Nullable: No
Allowed values: Saving
Validation: Member of the declared public enum.
Trigger: Response containing this field.
Description: Saving goal type.
Example: `Saving`

### data.savingGoal.target_amount

Type: number
Required: Yes
Nullable: No
Validation: JSON number.
Trigger: Response containing this field.
Description: Saving target amount.
Example: `10000000`

### data.savingGoal.target_achieved

Type: number
Required: Yes
Nullable: No
Validation: JSON number.
Trigger: Response containing this field.
Description: Calculated achieved amount for the saving goal.
Example: `3500000`

### data.savingGoal.start_date

Type: string
Format: date
Required: Yes
Nullable: No
Validation: Valid calendar date in YYYY-MM-DD representation.
Trigger: Response containing this field.
Description: Saving goal start date.
Example: `2025-11-01`

### data.savingGoal.end_date

Type: string
Format: date
Required: Yes
Nullable: No
Validation: Valid calendar date in YYYY-MM-DD representation.
Trigger: Response containing this field.
Description: Saving goal end date.
Example: `2025-11-30`

### data.expenseGoals

Type: array<object>
Required: Yes
Nullable: No
Validation: JSON array<object>.
Trigger: Response containing this field.
Description: Expense-goal items returned for the Goals view.
Example: `[]`

### data.expenseGoals[].goal_id

Type: integer
Required: Yes
Nullable: No
Validation: JSON integer.
Trigger: Response containing this field.
Description: Expense goal identifier.
Example: `5`

### data.expenseGoals[].category

Type: string
Required: Yes
Nullable: No
Validation: JSON string.
Trigger: Response containing this field.
Description: Category label for the expense goal.
Example: `Food`

### data.expenseGoals[].target_amount

Type: number
Required: Yes
Nullable: No
Validation: JSON number.
Trigger: Response containing this field.
Description: Expense-goal target amount.
Example: `3000000`

### data.expenseGoals[].current_expense

Type: number
Required: Yes
Nullable: No
Validation: JSON number.
Trigger: Response containing this field.
Description: Calculated expense amount for the expense goal.
Example: `1200000`

### data.savingGoal.version

Type: integer
Required: Yes
Nullable: No
Validation: JSON integer.
Trigger: Response containing this field.
Description: Goal version.
Example: `1`

### data.expenseGoals[].version

Type: integer
Required: Yes
Nullable: No
Validation: JSON integer.
Trigger: Response containing this field.
Description: Goal version.
Example: `1`

### data.expenseGoals[].goal_type

Type: string
Required: Yes
Nullable: No
Validation: JSON string.
Trigger: Response containing this field.
Description: Goal goal type.
Example: `Expense_Limit`

### data.expenseGoals[].start_date

Type: string
Format: date
Required: Yes
Nullable: No
Validation: Valid calendar date in YYYY-MM-DD representation.
Trigger: Response containing this field.
Description: Goal start date.
Example: `2026-10-01`

### data.expenseGoals[].end_date

Type: string
Format: date
Required: Yes
Nullable: No
Validation: Valid calendar date in YYYY-MM-DD representation.
Trigger: Response containing this field.
Description: Goal end date.
Example: `2026-10-31`

### data.expenseGoals[].category_id

Type: integer
Required: Yes
Nullable: Yes
Validation: JSON integer.
Trigger: Response containing this field.
Description: Category identifier.
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

[Common wire contract](common-contract.md). Source: [API contract starting at row 258](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=439687549&range=A258:B274). These are reviewed contracts; compatibility changes are recorded in the package review. Child fields under a nullable object apply when that object is present.
