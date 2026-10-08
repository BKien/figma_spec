---
artifact_type: api-contract
status: Frozen
api_id: API-GOAL-CREATE
related_uc_id: UC-14
---

# API-GOAL-CREATE: Create Financial Goal

## General Information

### API ID

API-GOAL-CREATE

### API Name

Create Financial Goal

### Related Use Case IDs

UC-14

### Method

POST

### Path

/api/v1/goals

### Description

Create financial-goal data for the authenticated user's Goals workflow.

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

### goal_type

Type: string; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: Goal type supplied by the client.

Example: Saving

Allowed values: Saving; Expense_Limit

Validation: Member of the declared public enum.

### category_id

Type: integer; Required: No; Nullable: Yes

Trigger: Request containing this field.

Description: Optional category identifier supplied with the goal request.

Example: 3

Validation: JSON integer; query and path values use complete decimal text.

### start_date

Type: string; Format: YYYY-MM-DD; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: Goal start date supplied by the client.

Example: 2025-11-01

Validation: Valid calendar date in YYYY-MM-DD representation.

### end_date

Type: string; Format: YYYY-MM-DD; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: Goal end date supplied by the client.

Example: 2025-11-30

Validation: Valid calendar date in YYYY-MM-DD representation.

### target_amount

Type: number; Format: decimal; Required: Yes; Nullable: No

Trigger: Request containing this field.

Description: Goal target amount supplied by the client.

Example: 10000000

Validation: JSON number; query and path values use complete decimal text.

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

### data.goal_id

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Identifier returned for the created goal.

Example: 5

Validation: JSON integer.

### data.version

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Goal version.

Example: 0

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

[Common wire contract](common-contract.md). Source: [API contract starting at row 274](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=439687549&range=A274:B290). These are reviewed contracts; compatibility changes are recorded in the package review. Child fields under a nullable object apply when that object is present.
