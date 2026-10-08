---
artifact_type: api-contract
status: Frozen
api_id: API-PREFERENCES-UPDATE
related_uc_ids: ["UC-12", "UC-13", "UC-14", "UC-15"]
---

# API-PREFERENCES-UPDATE: Update Session Preferences

## General Information

### API ID

API-PREFERENCES-UPDATE

### API Name

Update Session Preferences

### Related Use Case IDs

- UC-12
- UC-13
- UC-14
- UC-15

### Method

PATCH

### Path

/api/v1/sessions/{sessionId}/participants/{participantId}/preferences

### Description

Returns the media and view preference representation.

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

Example: command-22-01

Note: Transmit the command reference as a single header value.

## Path Parameter(s)

### path.sessionId

Type: string; Required: Yes; Nullable: No

Trigger: Every request using the sessionId path segment.

Description: UUID identifier.

Example: 11111111-1111-4111-8111-111111111111

### path.participantId

Type: string; Required: Yes; Nullable: No

Trigger: Every request using the participantId path segment.

Description: UUID identifier.

Example: 11111111-1111-4111-8111-111111111111

## Query Parameter(s)

None.

## Request Body

### microphoneDeviceId

Type: string; Required: No; Nullable: Yes

Trigger: When the client includes this property in the request body.

Description: microphoneDeviceId value.

Example: "microphone-device-01"

Validation: Must be null or a JSON string.

### cameraDeviceId

Type: string; Required: No; Nullable: Yes

Trigger: When the client includes this property in the request body.

Description: cameraDeviceId value.

Example: "camera-device-01"

Validation: Must be null or a JSON string.

### speakerDeviceId

Type: string; Required: No; Nullable: Yes

Trigger: When the client includes this property in the request body.

Description: speakerDeviceId value.

Example: "speaker-device-01"

Validation: Must be null or a JSON string.

### virtualBackgroundId

Type: string; Required: No; Nullable: Yes

Trigger: When the client includes this property in the request body.

Description: virtualBackgroundId value.

Example: "background-01"

Validation: Must be null or a JSON string.

### layout

Type: string; Required: No; Nullable: No

Trigger: When the client includes this property in the request body.

Description: layout value.

Example: "EQUAL_PROMINENCE"

Allowed values: EQUAL_PROMINENCE, SIDEBAR, PRESENTER

Validation: Must be a JSON string. String values must belong to the declared enum.

### focusedParticipantId

Type: string; Required: No; Nullable: Yes

Trigger: When the client includes this property in the request body.

Description: focusedParticipantId value.

Example: "11111111-1111-4111-8111-111111111111"

Validation: Must be null or a JSON string.

### sidePanel

Type: string; Required: No; Nullable: Yes

Trigger: When the client includes this property in the request body.

Description: sidePanel value.

Example: "CHAT"

Allowed values: CHAT, PARTICIPANTS, SETTINGS

Validation: Must be null or a JSON string. String values must belong to the declared enum.

### pictureInPicture

Type: boolean; Required: No; Nullable: No

Trigger: When the client includes this property in the request body.

Description: pictureInPicture value.

Example: false

Validation: Must be a JSON boolean.

## Success Response — HTTP 200

Inherits the success envelope and named object definitions in [Common Contract](common-contract.md).

### data.media

Type: object (MediaPreference); Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Representation defined in the common contract.

Example: {"participantId": "11111111-1111-4111-8111-111111111111", "microphoneDeviceId": "microphone-device-01", "cameraDeviceId": "camera-device-01", "speakerDeviceId": "speaker-device-01", "virtualBackgroundId": "11111111-1111-4111-8111-111111111111", "updatedAt": "2026-09-22T09:00:00Z"}

### data.view

Type: object (ViewPreference); Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Representation defined in the common contract.

Example: {"participantId": "11111111-1111-4111-8111-111111111111", "layout": "EQUAL_PROMINENCE", "focusedParticipantId": "11111111-1111-4111-8111-111111111111", "sidePanel": "CHAT", "pictureInPicture": false, "updatedAt": "2026-09-22T09:00:00Z"}

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

This endpoint inherits [Common Contract](common-contract.md).
