# API-UC-18-02 — POST /api/v1/instructor/courses/:courseId/enrollments

## API ID

`API-UC-18-02`

## API Name

Publish a Course and Assign Learners — POST /api/v1/instructor/courses/:courseId/enrollments

## Related Use Case IDs

- `UC-18`

## Method

`POST`

## Path

`/api/v1/instructor/courses/:courseId/enrollments`

## Description

Provides the wire operation referenced by the supplied Publish a Course and Assign Learners specification.

## Authentication

Authentication context is supplied when required by the preserved source contract.

## Authorization

The service evaluates the submitted operation context.

## Request Headers

### `Content-Type`

- Type: string
- Format: MIME type
- Required: Yes
- Nullable: No
- Allowed values: application/json
- Validation: Must identify the `application/json` media type.
- Description: Declares the request representation.
- Example: `application/json`

## Path Parameters

### `courseId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as an opaque path string.
- Description: Identifies the requested path resource on the wire.
- Example: `example-courseId`

## Query Parameters

None.

## Request Body

### `payload`

- Type: object
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON object.
- Description: Carries the operation-specific request fields defined by the preserved source contract.
- Example: `{}`

## Success Response — HTTP 201

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

Detailed endpoint fields, status codes, examples, and public outcomes are preserved in [the supplied source](../source/edtech-uc-18-publish-and-assign-course.md). Business behavior is specified by [UC-18](../uc/uc-18-publish-and-assign-course.md).
