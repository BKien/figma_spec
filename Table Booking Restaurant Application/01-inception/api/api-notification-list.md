---
artifact_type: api-contract
status: Frozen
api_id: API-NOTIFICATION-LIST
related_uc_id: UC-12
---

# API-NOTIFICATION-LIST: View Notifications

## General Information

### API ID

API-NOTIFICATION-LIST

### API Name

View Notifications

### Related Use Case IDs

- UC-12

### Method

GET

### Path

/api/v1/me/notifications

### Description

Accepts the displayed view notifications interaction and returns its public result.

### Authentication

Bearer access token.

### Authorization

Authenticated customer.

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

### data.notifications

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: data notifications supplied on the wire.

Example: []

Validation: Must be encoded as a JSON array.

### data.nextCursor

Type: string; Required: No; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null and this optional property is returned.

Description: data nextCursor supplied on the wire.

Example: cur_123

Validation: Must be encoded as a JSON string.

### data.notifications[].id

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.notifications[] object or array item is present and non-null.

Description: data notifications[] id supplied on the wire.

Example: ntf_123

Validation: Must be encoded as a JSON string.

### data.notifications[].title

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.notifications[] object or array item is present and non-null.

Description: data notifications[] title supplied on the wire.

Example: Booking confirmed

Validation: Must be encoded as a JSON string.

### data.notifications[].body

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.notifications[] object or array item is present and non-null.

Description: data notifications[] body supplied on the wire.

Example: Your table is booked.

Validation: Must be encoded as a JSON string.

### data.notifications[].createdAt

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.notifications[] object or array item is present and non-null.

Description: data notifications[] createdAt supplied on the wire.

Example: 2026-09-24T10:00:00Z

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

## Notes

The common response envelope and pagination conventions are defined in [common-contract.md](common-contract.md). Business behavior is specified only in [UC-12](../uc/uc-12-view-notifications.md).
