---
artifact_type: api-contract
status: Frozen
api_id: API-BILL-LIST
related_uc_id: UC-12
---

# API-BILL-LIST: List Upcoming Bills

## General Information

### API ID

API-BILL-LIST

### API Name

List Upcoming Bills

### Related Use Case IDs

UC-12

### Method

GET

### Path

/api/v1/bills

### Description

Return bill data for the authenticated user's Upcoming Bills view.

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

Type: array<object>; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Bill items returned for the Upcoming Bills view.

Example: []

Validation: JSON array<object>.

### data[].billId

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Bill identifier.

Example: 7

Validation: JSON integer.

### data[].userId

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: User identifier.

Example: 1

Validation: JSON integer.

### data[].itemDescription

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Bill description.

Example: Netflix

Validation: JSON string.

### data[].logoUrl

Type: string; Required: Yes; Nullable: Yes

Trigger: Response containing this field.

Description: Optional bill logo URL.

Example: https://example.com/netflix.png

Validation: JSON string.

### data[].dueDate

Type: string; Format: date; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Bill due date.

Example: 2025-11-15

Validation: Valid calendar date in YYYY-MM-DD representation.

### data[].lastChargeDate

Type: string; Format: date; Required: Yes; Nullable: Yes

Trigger: Response containing this field.

Description: Most recent charge date when available.

Example: 2025-10-15

Validation: Valid calendar date in YYYY-MM-DD representation.

### data[].amount

Type: number; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Bill amount.

Example: 260000

Validation: JSON number.

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

[Common wire contract](common-contract.md). Source: [API contract starting at row 242](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=439687549&range=A242:B258). These are reviewed contracts; compatibility changes are recorded in the package review. Child fields under a nullable object apply when that object is present.
