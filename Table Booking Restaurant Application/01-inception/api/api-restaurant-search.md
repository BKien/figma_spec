---
artifact_type: api-contract
status: Frozen
api_id: API-RESTAURANT-SEARCH
related_uc_id: UC-04
---

# API-RESTAURANT-SEARCH: Search Restaurants

## General Information

### API ID

API-RESTAURANT-SEARCH

### API Name

Search Restaurants

### Related Use Case IDs

- UC-04

### Method

GET

### Path

/api/v1/restaurants

### Description

Accepts the displayed search restaurants interaction and returns its public result.

### Authentication

None.

### Authorization

Public endpoint.

## Request Header(s)

None.

## Path Parameter(s)

None.

## Query Parameter(s)

### query.location

Type: string; Required: Yes; Nullable: No

Trigger: Every request includes the location query parameter.

Description: location supplied on the wire.

Example: Miami

Validation: Must be encoded as one URL query value.

### query.cuisine

Type: string; Required: Yes; Nullable: No

Trigger: Every request includes the cuisine query parameter.

Description: cuisine supplied on the wire.

Example: Italian

Validation: Must be encoded as one URL query value.

### query.meal

Type: string; Required: Yes; Nullable: No

Trigger: Every request includes the meal query parameter.

Description: meal supplied on the wire.

Example: dinner

Validation: Must be encoded as one URL query value.

### query.date

Type: string; Format: date; Required: Yes; Nullable: No

Trigger: Every request includes the date query parameter.

Description: date supplied on the wire.

Example: 2026-10-02

Validation: Must use ISO 8601 calendar-date syntax.

### query.time

Type: string; Format: time; Required: Yes; Nullable: No

Trigger: Every request includes the time query parameter.

Description: time supplied on the wire.

Example: 19:00

Validation: Must use 24-hour HH:mm time syntax.

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

### data.restaurants

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: data restaurants supplied on the wire.

Example: []

Validation: Must be encoded as a JSON array.

### data.nextCursor

Type: string; Required: No; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null and this optional property is returned.

Description: data nextCursor supplied on the wire.

Example: cur_123

Validation: Must be encoded as a JSON string.

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

### data.restaurants[].city

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.restaurants[] object or array item is present and non-null.

Description: data restaurants[] city supplied on the wire.

Example: Miami

Validation: Must be encoded as a JSON string.

### data.restaurants[].cuisine

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.restaurants[] object or array item is present and non-null.

Description: data restaurants[] cuisine supplied on the wire.

Example: Italian

Validation: Must be encoded as a JSON string.

### data.restaurants[].rating

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.restaurants[] object or array item is present and non-null.

Description: data restaurants[] rating supplied on the wire.

Example: 4.5

Validation: Must be encoded as a JSON number.

### data.restaurants[].availabilityLabel

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.restaurants[] object or array item is present and non-null.

Description: data restaurants[] availabilityLabel supplied on the wire.

Example: 11:15 AM

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

The common response envelope and pagination conventions are defined in [common-contract.md](common-contract.md). Business behavior is specified only in [UC-04](../uc/uc-04-search-restaurants.md).
