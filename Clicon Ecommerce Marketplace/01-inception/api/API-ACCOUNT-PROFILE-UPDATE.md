---
artifact_type: api-contract
status: Frozen
api_id: API-ACCOUNT-PROFILE-UPDATE
related_uc_id: UC-11
---

# API-ACCOUNT-PROFILE-UPDATE: Manage Account Profile — PUT /api/v1/account/profile

## General Information

### API ID

API-ACCOUNT-PROFILE-UPDATE

### API Name

Manage Account Profile — PUT /api/v1/account/profile

### Related Use Case IDs

- UC-11

### Method

PUT

### Path

/api/v1/account/profile

### Description

Provides the wire operation referenced by the supplied Manage Account Profile specification.

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

None.

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

Detailed endpoint fields, status codes, examples, and public outcomes are preserved in [the supplied source](../../source/clicon-uc-11-manage-account-profile.md). Business behavior is specified by [UC-11](../uc/uc-11-manage-account-profile.md).
