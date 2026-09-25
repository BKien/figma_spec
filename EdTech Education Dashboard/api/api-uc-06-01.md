# API-UC-06-01 — GET /api/v1/student/my-courses

## API ID

`API-UC-06-01`

## API Name

View Assigned Courses and Module Progress — GET /api/v1/student/my-courses

## Related Use Case IDs

- `UC-06`

## Method

`GET`

## Path

`/api/v1/student/my-courses`

## Description

Provides the wire operation referenced by the supplied View Assigned Courses and Module Progress specification.

## Authentication

Authentication context is supplied when required by the preserved source contract.

## Authorization

The service evaluates the submitted operation context.

## Request Headers

None.

## Path Parameters

None.

## Query Parameters

None.

## Request Body

None.

## Success Response — HTTP 200

### `success`

- Type: boolean
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON boolean.
- Description: Indicates a successful protocol outcome.
- Example: `true`

### `data`

- Type: object
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON object.
- Description: Contains the operation-specific response fields defined by the preserved source contract.
- Example: `{}`

## Error Response — HTTP 400

### `error`

- Type: object
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON object.
- Description: Contains the public protocol error.
- Example: `{}`

### `error.code`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Stable public error identifier.
- Example: `MALFORMED_REQUEST`

### `error.message`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Human-readable public error summary.
- Example: `The request could not be processed.`

- Trigger: Malformed wire input.

## Notes

Detailed endpoint fields, status codes, examples, and public outcomes are preserved in [the supplied source](../source/edtech-uc-06-view-my-courses.md). Business behavior is specified by [UC-06](../uc/uc-06-view-my-courses.md).
