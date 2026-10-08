---
artifact_type: api-contract
status: Frozen
api_id: API-MENU-LIST
related_uc_id: UC-06
---

# API-MENU-LIST: View a Restaurant Menu

## General Information

### API ID

API-MENU-LIST

### API Name

View a Restaurant Menu

### Related Use Case IDs

- UC-06

### Method

GET

### Path

/api/v1/restaurants/{restaurantId}/menu

### Description

Accepts the displayed view a restaurant menu interaction and returns its public result.

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

### data.items

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: data items supplied on the wire.

Example: []

Validation: Must be encoded as a JSON array.

### data.restaurantId

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: data restaurantId supplied on the wire.

Example: rst_123

Validation: Must be encoded as a JSON string.

### data.items[].id

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.items[] object or array item is present and non-null.

Description: data items[] id supplied on the wire.

Example: itm_123

Validation: Must be encoded as a JSON string.

### data.items[].name

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.items[] object or array item is present and non-null.

Description: data items[] name supplied on the wire.

Example: Pasta

Validation: Must be encoded as a JSON string.

### data.items[].sectionName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.items[] object or array item is present and non-null.

Description: data items[] sectionName supplied on the wire.

Example: Mains

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

The common response envelope and pagination conventions are defined in [common-contract.md](common-contract.md). Business behavior is specified only in [UC-06](../uc/uc-06-view-menu.md).
