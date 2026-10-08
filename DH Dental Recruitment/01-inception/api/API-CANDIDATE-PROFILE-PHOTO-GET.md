---
artifact_type: api-contract
status: Frozen
api_id: API-CANDIDATE-PROFILE-PHOTO-GET
related_uc_id: UC-19
---

# API-CANDIDATE-PROFILE-PHOTO-GET: View a Public Candidate Profile — GET /api/v1/candidate-profiles/:profileId/photo

## General Information

### API ID

API-CANDIDATE-PROFILE-PHOTO-GET

### API Name

View a Public Candidate Profile — GET /api/v1/candidate-profiles/:profileId/photo

### Related Use Case IDs

- UC-19

### Method

GET

### Path

/api/v1/candidate-profiles/:profileId/photo

### Description

Provides the wire operation referenced by the supplied View a Public Candidate Profile specification.

### Authentication

Authentication context is supplied when required by the preserved source contract.

### Authorization

The service evaluates the submitted operation context.

## Request Header(s)

None.

## Path Parameter(s)

### path.profileId

Type: string; Required: Yes; Nullable: No

Trigger: Every request using the profileId path segment.

Description: Identifies the requested path resource on the wire.

Example: example-profileId

Validation: Must be encoded as an opaque path string.

## Query Parameter(s)

None.

## Request Body

None.

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

Detailed endpoint fields, status codes, examples, and public outcomes are preserved in [the supplied source](../../source/dh-dental-uc-19-view-public-profile.md). Business behavior is specified by [UC-19](../uc/uc-19-view-public-profile.md).
