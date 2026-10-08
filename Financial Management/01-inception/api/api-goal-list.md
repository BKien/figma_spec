---
artifact_type: api-contract
status: Frozen
api_id: API-GOAL-LIST
related_uc_ids: ["UC-13", "UC-15"]
---

# API-GOAL-LIST: List Financial Goals

## General Information

### API ID

API-GOAL-LIST

### API Name

List Financial Goals

### Related Use Case IDs

UC-13, UC-15

### Method

GET

### Path

/api/v1/goals

### Description

Return financial-goal data for the authenticated user's Goals view.

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

### data.savingGoal

Type: object; Required: Yes; Nullable: Yes

Trigger: Response containing this field.

Description: Saving-goal data when available.

Example: null

Validation: JSON object.

### data.savingGoal.goal_id

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Saving goal identifier.

Example: 2

Validation: JSON integer.

### data.savingGoal.goal_type

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Saving goal type.

Example: Saving

Allowed values: Saving

Validation: Member of the declared public enum.

### data.savingGoal.target_amount

Type: number; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Saving target amount.

Example: 10000000

Validation: JSON number.

### data.savingGoal.target_achieved

Type: number; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Calculated achieved amount for the saving goal.

Example: 3500000

Validation: JSON number.

### data.savingGoal.start_date

Type: string; Format: date; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Saving goal start date.

Example: 2025-11-01

Validation: Valid calendar date in YYYY-MM-DD representation.

### data.savingGoal.end_date

Type: string; Format: date; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Saving goal end date.

Example: 2025-11-30

Validation: Valid calendar date in YYYY-MM-DD representation.

### data.expenseGoals

Type: array<object>; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Expense-goal items returned for the Goals view.

Example: []

Validation: JSON array<object>.

### data.expenseGoals[].goal_id

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Expense goal identifier.

Example: 5

Validation: JSON integer.

### data.expenseGoals[].category

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Category label for the expense goal.

Example: Food

Validation: JSON string.

### data.expenseGoals[].target_amount

Type: number; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Expense-goal target amount.

Example: 3000000

Validation: JSON number.

### data.expenseGoals[].current_expense

Type: number; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Calculated expense amount for the expense goal.

Example: 1200000

Validation: JSON number.

### data.savingGoal.version

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Goal version.

Example: 1

Validation: JSON integer.

### data.expenseGoals[].version

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Goal version.

Example: 1

Validation: JSON integer.

### data.expenseGoals[].goal_type

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Goal goal type.

Example: Expense_Limit

Validation: JSON string.

### data.expenseGoals[].start_date

Type: string; Format: date; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Goal start date.

Example: 2026-10-01

Validation: Valid calendar date in YYYY-MM-DD representation.

### data.expenseGoals[].end_date

Type: string; Format: date; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Goal end date.

Example: 2026-10-31

Validation: Valid calendar date in YYYY-MM-DD representation.

### data.expenseGoals[].category_id

Type: integer; Required: Yes; Nullable: Yes

Trigger: Response containing this field.

Description: Category identifier.

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

[Common wire contract](common-contract.md). Source: [API contract starting at row 258](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=439687549&range=A258:B274). These are reviewed contracts; compatibility changes are recorded in the package review. Child fields under a nullable object apply when that object is present.
