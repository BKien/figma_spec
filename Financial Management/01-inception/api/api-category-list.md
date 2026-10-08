---
artifact_type: api-contract
status: Frozen
api_id: API-CATEGORY-LIST
related_uc_ids: ["UC-04", "UC-14", "UC-18"]
---

# API-CATEGORY-LIST: List Categories

## General Information

### API ID

API-CATEGORY-LIST

### API Name

List Categories

### Related Use Case IDs

UC-04, UC-14, UC-18

### Method

GET

### Path

/api/categories

### Description

Return all available transaction and goal categories.

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

Description: Category array. May be empty.

Example: []

Validation: JSON array<object>.

### data[].category_id

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Category identifier.

Example: 3

Validation: JSON integer.

### data[].category_name

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Category name.

Example: Entertainment

Validation: JSON string.

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

[Common wire contract](common-contract.md). Source: [API contract starting at row 173](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=439687549&range=A173:B189). These are reviewed contracts; compatibility changes are recorded in the package review. Child fields under a nullable object apply when that object is present.
