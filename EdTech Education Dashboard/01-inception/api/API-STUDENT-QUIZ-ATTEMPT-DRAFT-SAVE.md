---
artifact_type: api-contract
status: Frozen
api_id: API-STUDENT-QUIZ-ATTEMPT-DRAFT-SAVE
related_uc_id: UC-09
---

# API-STUDENT-QUIZ-ATTEMPT-DRAFT-SAVE: Take a Course Quiz and View the Result — PUT /api/v1/student/courses/:courseId/units/:unitId/quiz/attempts/:attemptId/draft

## General Information

### API ID

API-STUDENT-QUIZ-ATTEMPT-DRAFT-SAVE

### API Name

Take a Course Quiz and View the Result — PUT /api/v1/student/courses/:courseId/units/:unitId/quiz/attempts/:attemptId/draft

### Related Use Case IDs

- UC-09

### Method

PUT

### Path

/api/v1/student/courses/:courseId/units/:unitId/quiz/attempts/:attemptId/draft

### Description

Provides the wire operation referenced by the supplied Take a Course Quiz and View the Result specification.

### Authentication

Authentication context is supplied when required by the preserved source contract.

### Authorization

The service evaluates the submitted operation context.

## Request Header(s)

### headers.Content-Type

Type: string; Format: MIME type; Required: Yes; Nullable: No

Trigger: Every PUT request to this endpoint.

Description: Declares the request representation.

Example: application/json

Note: Identifies the media type of the submitted request body.

Allowed values: application/json

Validation: Must identify the application/json media type.

## Path Parameter(s)

### path.courseId

Type: string; Required: Yes; Nullable: No

Trigger: Every request using the courseId path segment.

Description: Identifies the requested path resource on the wire.

Example: example-courseId

Validation: Must be encoded as an opaque path string.

### path.unitId

Type: string; Required: Yes; Nullable: No

Trigger: Every request using the unitId path segment.

Description: Identifies the requested path resource on the wire.

Example: example-unitId

Validation: Must be encoded as an opaque path string.

### path.attemptId

Type: string; Required: Yes; Nullable: No

Trigger: Every request using the attemptId path segment.

Description: Identifies the requested path resource on the wire.

Example: example-attemptId

Validation: Must be encoded as an opaque path string.

## Query Parameter(s)

None.

## Request Body

### payload

Type: object; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Carries the operation-specific request fields defined by the preserved source contract.

Example: {}

Validation: Must be encoded as a JSON object.

## Success Response — HTTP 200

### success

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Indicates a successful protocol outcome.

Example: true

Validation: Must be encoded as a JSON boolean.

### data

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Contains the operation-specific response fields defined by the preserved source contract.

Example: {}

Validation: Must be encoded as a JSON object.

## Error Response — HTTP 400

### error

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 400 error response.

Description: Contains the public protocol error.

Example: {}

Note: Field of the JSON error response.

Validation: Must be encoded as a JSON object.

### error.code

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 400 error response when the containing error object or array item is present and non-null.

Description: Stable public error identifier.

Example: MALFORMED_REQUEST

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Validation: Must be encoded as a JSON string.

### error.message

Type: string; Required: Yes; Nullable: No

Trigger: Malformed wire input.

Description: Human-readable public error summary.

Example: The request could not be processed.

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Validation: Must be encoded as a JSON string.

## Notes

Detailed endpoint fields, status codes, examples, and public outcomes are preserved in [the supplied source](../../source/edtech-uc-09-take-course-quiz.md). Business behavior is specified by [UC-09](../uc/uc-09-take-course-quiz.md).
