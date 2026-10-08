---
artifact_type: api-contract
status: Frozen
api_id: API-SAVINGS-SUMMARY
related_uc_id: UC-16
---

# API-SAVINGS-SUMMARY: Get Savings Summary

## General Information

### API ID

API-SAVINGS-SUMMARY

### API Name

Get Savings Summary

### Related Use Case IDs

UC-16

### Method

GET

### Path

/api/v1/savings/summary

### Description

Return monthly net savings for a selected year and the preceding year.

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

### query.year

Type: integer; Format: YYYY; Required: No; Nullable: No

Trigger: Request containing this field.

Description: Optional target year resolved by the controller.

Example: 2026

Validation: Exactly four decimal digits representing an integer year.

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

### data.summary

Type: object; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Nested response object.

Example: {}

Validation: JSON object.

### data.user_id

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Authenticated user identifier.

Example: 1

Validation: JSON integer.

### data.year

Type: integer; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Resolved target year.

Example: 2025

Validation: JSON integer.

### data.summary.this_year

Type: array<object>; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Twelve monthly savings values for the selected year.

Example: []

Validation: JSON array<object>.

### data.summary.this_year[].month

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Two-digit month number.

Example: 01

Validation: JSON string.

### data.summary.this_year[].amount

Type: number; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Revenue minus expense for the month.

Example: 1500000

Validation: JSON number.

### data.summary.last_year

Type: array<object>; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Twelve monthly savings values for the previous year.

Example: []

Validation: JSON array<object>.

### data.summary.last_year[].month

Type: string; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Two-digit month number.

Example: 01

Validation: JSON string.

### data.summary.last_year[].amount

Type: number; Required: Yes; Nullable: No

Trigger: Response containing this field.

Description: Revenue minus expense for the month.

Example: 1200000

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

[Common wire contract](common-contract.md). Source: [API contract starting at row 311](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=439687549&range=A311:B327). These are reviewed contracts; compatibility changes are recorded in the package review. Child fields under a nullable object apply when that object is present.
