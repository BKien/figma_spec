---
artifact_type: api-contract
status: Frozen
api_id: API-SLOT-LIST
related_uc_id: UC-07
---

# API-SLOT-LIST: Check Table Availability

## General Information

### API ID

API-SLOT-LIST

### API Name

Check Table Availability

### Related Use Case IDs

- UC-07

### Method

GET

### Path

/api/v1/restaurants/{restaurantId}/slots

### Description

Accepts the displayed check table availability interaction and returns its public result.

### Authentication

None.

### Authorization

Public endpoint.

## Request Header(s)

None.

## Path Parameter(s)

### path.restaurantId

Type: string; Required: Yes; Nullable: No

Trigger: Every request using the restaurantId path segment.

Description: restaurantId supplied on the wire.

Example: rst_123

Validation: Must be encoded as one URL path segment.

## Query Parameter(s)

### query.date

Type: string; Format: date; Required: Yes; Nullable: No

Trigger: Every request includes the date query parameter.

Description: date supplied on the wire.

Example: 2026-10-02

Validation: Must use ISO 8601 calendar-date syntax.

### query.partySize

Type: integer; Required: Yes; Nullable: No

Trigger: Every request includes the partySize query parameter.

Description: partySize supplied on the wire.

Example: 2

Validation: Must use decimal integer query syntax.

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

### data.slots

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: data slots supplied on the wire.

Example: []

Validation: Must be encoded as a JSON array.

### data.date

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: data date supplied on the wire.

Example: 2026-10-02

Validation: Must be encoded as a JSON string.

### data.slots[].id

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.slots[] object or array item is present and non-null.

Description: data slots[] id supplied on the wire.

Example: slot_123

Validation: Must be encoded as a JSON string.

### data.slots[].startsAt

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.slots[] object or array item is present and non-null.

Description: data slots[] startsAt supplied on the wire.

Example: 2026-10-02T19:00:00Z

Validation: Must be encoded as a JSON string.

### data.slots[].remainingSeats

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.slots[] object or array item is present and non-null.

Description: data slots[] remainingSeats supplied on the wire.

Example: 4

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

## Notes

The common response envelope and pagination conventions are defined in [common-contract.md](common-contract.md). Business behavior is specified only in [UC-07](../uc/uc-07-check-availability.md).
