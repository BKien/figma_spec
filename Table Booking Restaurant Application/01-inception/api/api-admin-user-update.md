---
artifact_type: api-contract
status: Frozen
api_id: API-ADMIN-USER-UPDATE
related_uc_id: UC-19
---

# API-ADMIN-USER-UPDATE: Manage Users

## General Information

### API ID

API-ADMIN-USER-UPDATE

### API Name

Manage Users

### Related Use Case IDs

- UC-19

### Method

PATCH

### Path

/api/v1/admin/users/{accountId}

### Description

Accepts the displayed manage users interaction and returns its public result.

### Authentication

Bearer access token.

### Authorization

Administration role.

## Request Header(s)

### headers.Authorization

Type: string; Format: bearer token; Required: Yes; Nullable: No

Trigger: Every PATCH request to this endpoint.

Description: Carries the bearer access token.

Example: Bearer eyJ...

Note: Uses the HTTP Bearer authentication scheme.

Validation: Must use the Bearer <access-token> header syntax.

### headers.Content-Type

Type: string; Format: MIME type; Required: Yes; Nullable: No

Trigger: Every PATCH request to this endpoint.

Description: Declares the request media type.

Example: application/json

Note: Identifies the media type of the submitted request body.

Allowed values: application/json

Validation: Must identify the application/json media type.

## Path Parameter(s)

### path.accountId

Type: string; Required: Yes; Nullable: No

Trigger: Every request using the accountId path segment.

Description: accountId supplied on the wire.

Example: acc_123

Validation: Must be encoded as one URL path segment.

## Query Parameter(s)

None.

## Request Body

### displayName

Type: string; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: displayName supplied on the wire.

Example: Alex Morgan

Validation: Must be encoded as a JSON string.

### status

Type: string; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: status supplied on the wire.

Example: ACTIVE

Allowed values: ACTIVE, SUSPENDED

Validation: Must be one of the public enum values.

### version

Type: integer; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: version supplied on the wire.

Example: 2

Validation: Must be encoded as a JSON integer.

## Success Response — HTTP 200

### success

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: success supplied on the wire.

Example: true

Validation: Must be encoded as a JSON boolean.

### data

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: data supplied on the wire.

Example: {}

Validation: Must be encoded as a JSON object.

### data.accountId

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: data accountId supplied on the wire.

Example: acc_123

Validation: Must be encoded as a JSON string.

### data.version

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: data version supplied on the wire.

Example: 3

Validation: Must be encoded as a JSON integer.

## Error Response — HTTP 400

### error

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 400 error response.

Description: error supplied on the wire.

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

Description: Human-readable error summary.

Example: The request could not be processed.

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Validation: Must be encoded as a JSON string.

## Error Response — HTTP 503

### error

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 503 error response.

Description: error supplied on the wire.

Example: {}

Note: Field of the JSON error response.

Validation: Must be encoded as a JSON object.

### error.code

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 503 error response when the containing error object or array item is present and non-null.

Description: Stable public error identifier.

Example: SERVICE_UNAVAILABLE

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Validation: Must be encoded as a JSON string.

### error.message

Type: string; Required: Yes; Nullable: No

Trigger: Temporary service failure.

Description: Human-readable error summary.

Example: Please try again later.

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Validation: Must be encoded as a JSON string.

## Error Response — HTTP 401

### error

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 401 error response.

Description: error supplied on the wire.

Example: {}

Note: Field of the JSON error response.

Validation: Must be encoded as a JSON object.

### error.code

Type: string; Required: Yes; Nullable: No

Trigger: Rejected authentication context.

Description: Stable public error identifier.

Example: AUTHENTICATION_REQUIRED

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Validation: Must be encoded as a JSON string.

## Error Response — HTTP 403

### error

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 403 error response.

Description: error supplied on the wire.

Example: {}

Note: Field of the JSON error response.

Validation: Must be encoded as a JSON object.

### error.code

Type: string; Required: Yes; Nullable: No

Trigger: Access denied response.

Description: Stable public error identifier.

Example: ACCESS_DENIED

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Validation: Must be encoded as a JSON string.

## Error Response — HTTP 404

### error

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 404 error response.

Description: error supplied on the wire.

Example: {}

Note: Field of the JSON error response.

Validation: Must be encoded as a JSON object.

### error.code

Type: string; Required: Yes; Nullable: No

Trigger: Unavailable resource response.

Description: Stable public error identifier.

Example: RESOURCE_UNAVAILABLE

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Validation: Must be encoded as a JSON string.

## Error Response — HTTP 409

### error

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 409 error response.

Description: error supplied on the wire.

Example: {}

Note: Field of the JSON error response.

Validation: Must be encoded as a JSON object.

### error.code

Type: string; Required: Yes; Nullable: No

Trigger: Operation conflict response.

Description: Stable public error identifier.

Example: OPERATION_CONFLICT

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Validation: Must be encoded as a JSON string.

## Notes

The common response envelope and pagination conventions are defined in [common-contract.md](common-contract.md). Business behavior is specified only in [UC-19](../uc/uc-19-manage-users.md).
