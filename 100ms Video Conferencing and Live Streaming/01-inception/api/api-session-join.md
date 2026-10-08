---
artifact_type: api-contract
status: Frozen
api_id: API-SESSION-JOIN
related_uc_ids: ["UC-02", "UC-12", "UC-13"]
---

# API-SESSION-JOIN: Join a Session

## General Information

### API ID

API-SESSION-JOIN

### API Name

Join a Session

### Related Use Case IDs

- UC-02
- UC-12
- UC-13

### Method

POST

### Path

/api/v1/sessions/{sessionId}/participants

### Description

Submits preview identity, media selections, and draft preferences.

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

### displayName

Type: string; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: displayName value.

Example: Alex Morgan

Validation: Must be a JSON string.

### microphoneEnabled

Type: boolean; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: microphoneEnabled value.

Example: false

Validation: Must be a JSON boolean.

### cameraEnabled

Type: boolean; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: cameraEnabled value.

Example: false

Validation: Must be a JSON boolean.

### microphoneDeviceId

Type: string; Required: No; Nullable: Yes

Trigger: When the client includes this property in the request body.

Description: microphoneDeviceId value.

Example: device-reference

Validation: Must be null or a JSON string.

### cameraDeviceId

Type: string; Required: No; Nullable: Yes

Trigger: When the client includes this property in the request body.

Description: cameraDeviceId value.

Example: device-reference

Validation: Must be null or a JSON string.

### speakerDeviceId

Type: string; Required: No; Nullable: Yes

Trigger: When the client includes this property in the request body.

Description: speakerDeviceId value.

Example: device-reference

Validation: Must be null or a JSON string.

### virtualBackgroundId

Type: string; Required: No; Nullable: Yes

Trigger: When the client includes this property in the request body.

Description: UUID identifier.

Example: 11111111-1111-4111-8111-111111111111

Validation: Must be null or a JSON string.

## Success Response — HTTP 201

Inherits the success envelope and named object definitions in [Common Contract](common-contract.md).

### data.participant

Type: object (Participant); Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Representation defined in the common contract.

Example: {"participantId": "11111111-1111-4111-8111-111111111111", "sessionId": "11111111-1111-4111-8111-111111111111", "displayName": "Alex Morgan", "role": "HOST", "status": "JOINED", "microphoneEnabled": false, "cameraEnabled": false, "version": 1, "joinedAt": "2026-09-22T09:00:00Z", "leftAt": null}

### data.session

Type: object (SessionSummary); Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Representation defined in the common contract.

Example: {"sessionId": "11111111-1111-4111-8111-111111111111", "kind": "LIVE_STREAM", "status": "LIVE", "version": 1, "hostParticipantId": "11111111-1111-4111-8111-111111111111", "spotlightedParticipantId": null, "endedAt": null}

### data.stream

Type: object (Stream); Required: Yes; Nullable: Yes

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Representation defined in the common contract.

Example: {"streamId": "11111111-1111-4111-8111-111111111111", "sessionId": "11111111-1111-4111-8111-111111111111", "status": "READY", "version": 1, "startedAt": null, "endedAt": null}

### data.media

Type: object (MediaPreference); Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Representation defined in the common contract.

Example: {"participantId": "11111111-1111-4111-8111-111111111111", "microphoneDeviceId": null, "cameraDeviceId": null, "speakerDeviceId": null, "virtualBackgroundId": null, "updatedAt": "2026-09-22T09:00:00Z"}

### data.view

Type: object (ViewPreference); Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: Representation defined in the common contract.

Example: {"participantId": "11111111-1111-4111-8111-111111111111", "layout": "EQUAL_PROMINENCE", "focusedParticipantId": null, "sidePanel": null, "pictureInPicture": false, "updatedAt": "2026-09-22T09:00:00Z"}

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

This endpoint inherits [Common Contract](common-contract.md).
