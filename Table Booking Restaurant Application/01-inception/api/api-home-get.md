---
artifact_type: api-contract
status: Frozen
api_id: API-HOME-GET
related_uc_id: UC-03
---

# API-HOME-GET: Browse the Restaurant Home Page

## General Information

### API ID

API-HOME-GET

### API Name

Browse the Restaurant Home Page

### Related Use Case IDs

- UC-03

### Method

GET

### Path

/api/v1/home

### Description

Accepts the displayed browse the restaurant home page interaction and returns its public result.

### Authentication

None.

### Authorization

Public endpoint.

## Request Header(s)

None.

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

### data.restaurants

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: data restaurants supplied on the wire.

Example: []

Validation: Must be encoded as a JSON array.

### data.featuredCount

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: data featuredCount supplied on the wire.

Example: 4

Validation: Must be encoded as a JSON integer.

### data.restaurants[].id

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.restaurants[] object or array item is present and non-null.

Description: data restaurants[] id supplied on the wire.

Example: rst_123

Validation: Must be encoded as a JSON string.

### data.restaurants[].name

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.restaurants[] object or array item is present and non-null.

Description: data restaurants[] name supplied on the wire.

Example: Villagio Restaurant and Bar

Validation: Must be encoded as a JSON string.

### data.restaurants[].heroImageUrl

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.restaurants[] object or array item is present and non-null.

Description: data restaurants[] heroImageUrl supplied on the wire.

Example: https://example.com/hero.jpg

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

## Notes

The common response envelope and pagination conventions are defined in [common-contract.md](common-contract.md). Business behavior is specified only in [UC-03](../uc/uc-03-browse-home.md).
