---
artifact_type: api-contract
status: Frozen
api_id: API-SESSION-STATE
related_uc_ids: ["UC-02", "UC-03", "UC-04", "UC-05", "UC-06", "UC-07", "UC-08", "UC-10", "UC-11", "UC-12", "UC-13", "UC-14", "UC-15", "UC-16", "UC-17", "UC-18"]
---

# API-SESSION-STATE: Read Session State

## General Information

### API ID

API-SESSION-STATE

### API Name

Read Session State

### Related Use Case IDs

- UC-02
- UC-03
- UC-04
- UC-05
- UC-06
- UC-07
- UC-08
- UC-10
- UC-11
- UC-12
- UC-13
- UC-14
- UC-15
- UC-16
- UC-17
- UC-18

### Method

GET

### Path

/api/v1/sessions/{sessionId}/state

### Description

Returns the current session and caller representations, stage requests, and a page of reaction events.

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

### query.reactionCursor

Type: string; Required: No; Nullable: No

Trigger: When the client supplies the reactionCursor query parameter.

Description: URI-encoded opaque reaction continuation token.

Example: "opaque-reaction-cursor-01"

Validation: Must be a JSON string.

## Request Body

None.

## Success Response — HTTP 200

Inherits the success envelope and named object definitions in [Common Contract](common-contract.md).

### data.session

Type: object (SessionSummary); Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Representation defined in the common contract.

Example: {"sessionId": "11111111-1111-4111-8111-111111111111", "kind": "LIVE_STREAM", "status": "LIVE", "version": 1, "hostParticipantId": "11111111-1111-4111-8111-111111111111", "spotlightedParticipantId": null, "endedAt": null}

### data.selfParticipant

Type: object (Participant); Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Representation defined in the common contract.

Example: {"participantId": "11111111-1111-4111-8111-111111111111", "sessionId": "11111111-1111-4111-8111-111111111111", "displayName": "Alex Morgan", "role": "HOST", "status": "JOINED", "microphoneEnabled": false, "cameraEnabled": false, "version": 1, "joinedAt": "2026-09-22T09:00:00Z", "leftAt": null}

### data.stream

Type: object (Stream); Required: Yes; Nullable: Yes

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Representation defined in the common contract.

Example: {"streamId": "11111111-1111-4111-8111-111111111111", "sessionId": "11111111-1111-4111-8111-111111111111", "status": "READY", "version": 1, "startedAt": null, "endedAt": null}

### data.recording

Type: object (Recording); Required: Yes; Nullable: Yes

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Representation defined in the common contract.

Example: {"createdAt": "2026-09-22T09:00:00Z", "recordingId": "11111111-1111-4111-8111-111111111111", "sessionId": "11111111-1111-4111-8111-111111111111", "startedByParticipantId": "11111111-1111-4111-8111-111111111111", "status": "IDLE", "version": 1, "startedAt": null, "stoppedAt": null}

### data.share

Type: object (Share); Required: Yes; Nullable: Yes

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Representation defined in the common contract.

Example: {"shareId": "11111111-1111-4111-8111-111111111111", "sessionId": "11111111-1111-4111-8111-111111111111", "ownerParticipantId": "11111111-1111-4111-8111-111111111111", "kind": "SCREEN", "status": "ACTIVE", "sourceReference": "source-opaque-reference", "version": 1, "startedAt": "2026-09-22T09:00:00Z", "stoppedAt": null}

### data.media

Type: object (MediaPreference); Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Representation defined in the common contract.

Example: {"participantId": "11111111-1111-4111-8111-111111111111", "microphoneDeviceId": null, "cameraDeviceId": null, "speakerDeviceId": null, "virtualBackgroundId": null, "updatedAt": "2026-09-22T09:00:00Z"}

### data.view

Type: object (ViewPreference); Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Representation defined in the common contract.

Example: {"participantId": "11111111-1111-4111-8111-111111111111", "layout": "EQUAL_PROMINENCE", "focusedParticipantId": null, "sidePanel": null, "pictureInPicture": false, "updatedAt": "2026-09-22T09:00:00Z"}

### data.stageRequests

Type: array (StageRequest); Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Array of representations defined in the common contract.

Example: []

### data.reactions

Type: array (Reaction); Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Array of representations defined in the common contract.

Example: []

### data.nextReactionCursor

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Opaque continuation token, including for an empty event page.

Example: "opaque-reaction-cursor-02"

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

This endpoint inherits [Common Contract](common-contract.md). The client can repeat this request to refresh its representation. Chat and participant collections have separate list endpoints.
