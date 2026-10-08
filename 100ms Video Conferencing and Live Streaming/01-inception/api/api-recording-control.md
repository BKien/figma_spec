---
artifact_type: api-contract
status: Frozen
api_id: API-RECORDING-CONTROL
related_uc_id: UC-16
---

# API-RECORDING-CONTROL: Control Session Recording

## General Information

### API ID

API-RECORDING-CONTROL

### API Name

Control Session Recording

### Related Use Case IDs

- UC-16

### Method

POST

### Path

/api/v1/sessions/{sessionId}/recording/commands

### Description

Returns the recording representation.

### Authentication

Bearer session access token, using the registered or guest form described in the common contract.

### Authorization

Required.

## Request Header(s)

### headers.Authorization

Type: string; Format: Bearer token; Required: Yes; Nullable: No

Trigger: Every POST request to this endpoint.

Description: Bearer session access token.

Example: Bearer <session-access-token>

Note: Uses the HTTP Bearer authentication scheme.

### headers.Content-Type

Type: string; Format: HTTP media type; Required: Yes; Nullable: No

Trigger: Every POST request to this endpoint.

Description: HTTP media-type header.

Example: application/json

Note: Identifies the media type of the submitted request body.

Allowed values: application/json

### headers.Idempotency-Key

Type: string; Format: Opaque HTTP header value; Required: Yes; Nullable: No

Trigger: Every POST request to this endpoint.

Description: Opaque HTTP command token.

Example: command-22-01

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

### action

Type: string; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: action value.

Example: START

Allowed values: START, STOP

Validation: Must be a JSON string. String values must belong to the declared enum.

### expectedVersion

Type: integer; Required: No; Nullable: Yes

Trigger: When the client includes this property in the request body.

Description: expectedVersion value.

Example: 1

Validation: Must be null or a JSON integer.

## Success Response — HTTP 200

Inherits the success envelope and named object definitions in [Common Contract](common-contract.md).

### data.recording

Type: object (Recording); Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Representation defined in the common contract.

Example: {"createdAt": "2026-09-22T09:00:00Z", "recordingId": "11111111-1111-4111-8111-111111111111", "sessionId": "11111111-1111-4111-8111-111111111111", "startedByParticipantId": "11111111-1111-4111-8111-111111111111", "status": "STARTING", "version": 1, "startedAt": null, "stoppedAt": null}

### data.sessionVersion

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: sessionVersion value.

Example: 1

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

This endpoint inherits [Common Contract](common-contract.md). Subsequent representations are available from the session-state endpoint.
