---
artifact_type: api-contract
status: Frozen
api_id: API-ADMIN-USER-LIST
related_uc_id: UC-19
---

# API-ADMIN-USER-LIST: List Admin Users

## General Information

### API ID

API-ADMIN-USER-LIST

### API Name

List Admin Users

### Related Use Case IDs

- UC-19

### Method

GET

### Path

/api/v1/admin/users

### Description

Accepts the displayed list admin users interaction and returns its public result.

### Authentication

Bearer access token.

### Authorization

Administration role.

## Request Header(s)

### headers.Authorization

Type: string; Format: bearer token; Required: Yes; Nullable: No

Trigger: Every GET request to this endpoint.

Description: Carries the bearer access token.

Example: Bearer eyJ...

Note: Uses the HTTP Bearer authentication scheme.

Validation: Must use the Bearer <access-token> header syntax.

## Path Parameter(s)

None.

## Query Parameter(s)

None.

## Request Body

None.

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

### data.users

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: data users supplied on the wire.

Example: []

Validation: Must be encoded as a JSON array.

### data.nextCursor

Type: string; Required: No; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null and this optional property is returned.

Description: data nextCursor supplied on the wire.

Example: cur_123

Validation: Must be encoded as a JSON string.

### data.users[].id

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.users[] object or array item is present and non-null.

Description: data users[] id supplied on the wire.

Example: acc_123

Validation: Must be encoded as a JSON string.

### data.users[].displayName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.users[] object or array item is present and non-null.

Description: data users[] displayName supplied on the wire.

Example: Alex Morgan

Validation: Must be encoded as a JSON string.

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

## Notes

The common response envelope and pagination conventions are defined in [common-contract.md](common-contract.md). Business behavior is specified only in [UC-19](../uc/uc-19-manage-users.md).
