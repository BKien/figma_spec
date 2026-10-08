---
artifact_type: api-contract
status: Frozen
api_id: API-ADMIN-TABLE-LIST
related_uc_id: UC-17
---

# API-ADMIN-TABLE-LIST: View Table Layout

## General Information

### API ID

API-ADMIN-TABLE-LIST

### API Name

View Table Layout

### Related Use Case IDs

- UC-17

### Method

GET

### Path

/api/v1/admin/restaurants/{restaurantId}/tables

### Description

Accepts the displayed view table layout interaction and returns its public result.

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

### path.restaurantId

Type: string; Required: Yes; Nullable: No

Trigger: Every request using the restaurantId path segment.

Description: restaurantId supplied on the wire.

Example: rst_123

Validation: Must be encoded as one URL path segment.

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

### data.tables

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: data tables supplied on the wire.

Example: []

Validation: Must be encoded as a JSON array.

### data.restaurantId

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: data restaurantId supplied on the wire.

Example: rst_123

Validation: Must be encoded as a JSON string.

### data.tables[].id

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.tables[] object or array item is present and non-null.

Description: data tables[] id supplied on the wire.

Example: tbl_123

Validation: Must be encoded as a JSON string.

### data.tables[].label

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.tables[] object or array item is present and non-null.

Description: data tables[] label supplied on the wire.

Example: T1

Validation: Must be encoded as a JSON string.

### data.tables[].capacity

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.tables[] object or array item is present and non-null.

Description: data tables[] capacity supplied on the wire.

Example: 4

Validation: Must be encoded as a JSON integer.

### data.tables[].layoutX

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.tables[] object or array item is present and non-null.

Description: data tables[] layoutX supplied on the wire.

Example: 120

Validation: Must be encoded as a JSON number.

### data.tables[].layoutY

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.tables[] object or array item is present and non-null.

Description: data tables[] layoutY supplied on the wire.

Example: 80

Validation: Must be encoded as a JSON number.

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

The common response envelope and pagination conventions are defined in [common-contract.md](common-contract.md). Business behavior is specified only in [UC-17](../uc/uc-17-view-table-layout.md).
