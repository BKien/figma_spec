---
artifact_type: api-contract
status: Frozen
api_id: API-ADMIN-BOOKING-LIST
related_uc_id: UC-15
---

# API-ADMIN-BOOKING-LIST: View Admin Bookings

## General Information

### API ID

API-ADMIN-BOOKING-LIST

### API Name

View Admin Bookings

### Related Use Case IDs

- UC-15

### Method

GET

### Path

/api/v1/admin/bookings

### Description

Accepts the displayed view admin bookings interaction and returns its public result.

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

### query.restaurantId

Type: string; Required: Yes; Nullable: No

Trigger: Every request includes the restaurantId query parameter.

Description: restaurantId supplied on the wire.

Example: rst_123

Validation: Must be encoded as one URL query value.

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

### data.bookings

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: data bookings supplied on the wire.

Example: []

Validation: Must be encoded as a JSON array.

### data.nextCursor

Type: string; Required: No; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null and this optional property is returned.

Description: data nextCursor supplied on the wire.

Example: cur_123

Validation: Must be encoded as a JSON string.

### data.bookings[].id

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.bookings[] object or array item is present and non-null.

Description: data bookings[] id supplied on the wire.

Example: bkg_123

Validation: Must be encoded as a JSON string.

### data.bookings[].status

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.bookings[] object or array item is present and non-null.

Description: data bookings[] status supplied on the wire.

Example: CONFIRMED

Validation: Must be encoded as a JSON string.

### data.bookings[].restaurantId

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.bookings[] object or array item is present and non-null.

Description: data bookings[] restaurantId supplied on the wire.

Example: rst_123

Validation: Must be encoded as a JSON string.

### data.bookings[].startsAt

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.bookings[] object or array item is present and non-null.

Description: data bookings[] startsAt supplied on the wire.

Example: 2026-10-02T19:00:00Z

Validation: Must be encoded as a JSON string.

### data.bookings[].partySize

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.bookings[] object or array item is present and non-null.

Description: data bookings[] partySize supplied on the wire.

Example: 2

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

## Notes

The common response envelope and pagination conventions are defined in [common-contract.md](common-contract.md). Business behavior is specified only in [UC-15](../uc/uc-15-view-admin-bookings.md).
