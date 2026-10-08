---
artifact_type: api-contract
status: Frozen
api_id: API-CHAT-MESSAGE-LIST
related_uc_id: UC-09
---

# API-CHAT-MESSAGE-LIST: Read Session Chat

## General Information

### API ID

API-CHAT-MESSAGE-LIST

### API Name

Read Session Chat

### Related Use Case IDs

- UC-09

### Method

GET

### Path

/api/v1/sessions/{sessionId}/chat/messages

### Description

Returns a page of chat messages and a continuation token.

### Authentication

Bearer session access token, using the registered or guest form described in the common contract.

### Authorization

Required.

## Request Header(s)

### headers.Authorization

Type: string; Format: Bearer token; Required: Yes; Nullable: No

Trigger: Every GET request to this endpoint.

Description: Bearer session access token.

Example: Bearer <session-access-token>

Note: Uses the HTTP Bearer authentication scheme.

### headers.Accept

Type: string; Format: HTTP media type; Required: Yes; Nullable: No

Trigger: Every GET request to this endpoint.

Description: HTTP media-type header.

Example: application/json

Note: Identifies the requested response media type.

Allowed values: application/json

## Path Parameter(s)

### path.sessionId

Type: string; Required: Yes; Nullable: No

Trigger: Every request using the sessionId path segment.

Description: UUID identifier.

Example: 11111111-1111-4111-8111-111111111111

## Query Parameter(s)

### query.cursor

Type: string; Required: No; Nullable: No

Trigger: When the client supplies the cursor query parameter.

Description: URI-encoded opaque continuation token.

Example: cursor-reference

Validation: Must be a JSON string.

### query.pageSize

Type: integer; Required: No; Nullable: No

Trigger: When the client supplies the pageSize query parameter.

Description: pageSize value.

Example: 50

Default: 50

Validation: Must be a JSON integer.

## Request Body

None.

## Success Response — HTTP 200

Inherits the success envelope and named object definitions in [Common Contract](common-contract.md).

### data.items

Type: array (Message); Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Array of representations defined in the common contract.

Example: []

### data.nextCursor

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Opaque continuation token, including for an empty page.

Example: "opaque-page-cursor-02"

## Error Response — HTTP 400

- Code: INVALID_REQUEST
Trigger: The request cannot be decoded or does not match the declared wire schema.
Description: Uses the common error envelope.
- Example message: The request could not be completed.

## Error Response — HTTP 401

- Code: AUTHENTICATION_REJECTED
Trigger: The authentication context is rejected.
Description: Uses the common error envelope.
- Example message: The request could not be completed.

## Error Response — HTTP 403

- Code: ACCESS_REJECTED
Trigger: The operation is rejected for the supplied access context.
Description: Uses the common error envelope.
- Example message: The request could not be completed.

## Error Response — HTTP 404

- Code: RESOURCE_UNAVAILABLE
Trigger: The requested resource is unavailable.
Description: Uses the common error envelope.
- Example message: The request could not be completed.

## Error Response — HTTP 503

- Code: SERVICE_UNAVAILABLE
Trigger: A required service is temporarily unavailable.
Description: Uses the common error envelope.
- Example message: The request could not be completed.

## Notes

This endpoint inherits [Common Contract](common-contract.md).
