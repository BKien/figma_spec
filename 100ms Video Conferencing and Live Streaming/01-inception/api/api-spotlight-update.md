---
artifact_type: api-contract
status: Frozen
api_id: API-SPOTLIGHT-UPDATE
related_uc_id: UC-15
---

# API-SPOTLIGHT-UPDATE: Update Session Spotlight

## General Information

### API ID

API-SPOTLIGHT-UPDATE

### API Name

Update Session Spotlight

### Related Use Case IDs

- UC-15

### Method

PATCH

### Path

/api/v1/sessions/{sessionId}/spotlight

### Description

Returns the session representation after setting or clearing the tile spotlighted for everyone.

### Authentication

Bearer session access token, using the registered or guest form described in the common contract.

### Authorization

Required.

## Request Header(s)

### headers.Authorization

Type: string; Format: Bearer token; Required: Yes; Nullable: No

Trigger: Every PATCH request to this endpoint.

Description: Bearer session access token.

Example: Bearer <session-access-token>

Note: Uses the HTTP Bearer authentication scheme.

### headers.Content-Type

Type: string; Format: HTTP media type; Required: Yes; Nullable: No

Trigger: Every PATCH request to this endpoint.

Description: HTTP media-type header.

Example: application/json

Note: Identifies the media type of the submitted request body.

Allowed values: application/json

### headers.Idempotency-Key

Type: string; Format: Opaque HTTP header value; Required: Yes; Nullable: No

Trigger: Every PATCH request to this endpoint.

Description: Opaque HTTP command token.

Example: command-15-01

Note: Transmit the command reference as a single header value.

## Path Parameter(s)

### path.sessionId

Type: string; Required: Yes; Nullable: No

Trigger: Every request using the sessionId path segment.

Description: UUID identifier.

Example: 11111111-1111-4111-8111-111111111111

## Query Parameter(s)

None.

## Request Body

### targetParticipantId

Type: string; Required: Yes; Nullable: Yes

Trigger: Every request body sent to this endpoint.

Description: Participant identifier to spotlight, or null to clear the shared spotlight.

Example: "11111111-1111-4111-8111-111111111111"

Validation: Must be null or a JSON string.

### expectedVersion

Type: integer; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: Session version observed by the client.

Example: 1

Validation: Must be a JSON integer.

## Success Response — HTTP 200

Inherits the success envelope and named object definitions in [Common Contract](common-contract.md).

### data.session

Type: object (SessionSummary); Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Representation defined in the common contract.

Example: {"sessionId": "11111111-1111-4111-8111-111111111111", "kind": "LIVE_STREAM", "status": "LIVE", "version": 1, "hostParticipantId": "11111111-1111-4111-8111-111111111111", "spotlightedParticipantId": "11111111-1111-4111-8111-111111111111", "endedAt": null}

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

## Error Response — HTTP 409

- Code: OPERATION_CONFLICT
Trigger: The operation conflicts with the current resource response.
Description: Uses the common error envelope.
- Example message: The request could not be completed.

## Error Response — HTTP 422

- Code: COMMAND_REJECTED
Trigger: The submitted command is rejected.
Description: Uses the common error envelope.
- Example message: The request could not be completed.

## Error Response — HTTP 503

- Code: SERVICE_UNAVAILABLE
Trigger: A required service is temporarily unavailable.
Description: Uses the common error envelope.
- Example message: The request could not be completed.

## Notes

This endpoint inherits [Common Contract](common-contract.md). Personal pinning remains part of API-PREFERENCES-UPDATE.
