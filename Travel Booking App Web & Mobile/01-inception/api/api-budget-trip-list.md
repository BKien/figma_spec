---
artifact_type: api-contract
status: Frozen
api_id: API-BUDGET-TRIP-LIST
related_uc_id: UC-16
---

# API-BUDGET-TRIP-LIST: Budget Trip List

## General Information

### API ID

API-BUDGET-TRIP-LIST

### API Name

Budget Trip List

### Related Use Case IDs

- UC-16

### Method

GET

### Path

/api/v1/budget-trips

### Description

Returns a paginated collection of budget-trip summaries.

### Authentication

Public

### Authorization

None

## Request Header(s)

None.

## Path Parameter(s)

None.

## Query Parameter(s)

### query.limit

Type: integer; Required: No; Nullable: No

Trigger: When the client supplies the limit query parameter.

Description: Requested page size.

Example: 20

Default: 20

Validation: Must use integer syntax when supplied.

### query.offset

Type: integer; Required: No; Nullable: No

Trigger: When the client supplies the offset query parameter.

Description: Requested starting position.

Example: 0

Default: 0

Validation: Must use integer syntax when supplied.

## Request Body

None.

## Success Response — HTTP 200

### success

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Indicates whether the HTTP operation completed successfully.

Example: true

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Human-readable operation outcome summary.

Example: Budget trips retrieved.

### data.items[]

Type: object array; Required: Yes; Nullable: No
- Fields: id (string), title (string), destinationName (string), imageUrl (URI string), startingPrice (money object).

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Budget-trip summaries in the current page.

Example: [{"id": "trip_01JABCDEF", "title": "A weekend in Kyoto", "destinationName": "Kyoto", "imageUrl": "https://example.com/images/travel.jpg", "startingPrice": {"amount": 300.0, "currency": "USD"}}]

### data.total

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Reported collection size.

Example: 1

### data.limit

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Applied page size.

Example: 20

### data.offset

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Applied starting position.

Example: 0

### data.hasMore

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Indicates whether another page can be requested.

Example: false

## Error Response — HTTP 400

- Code: VALIDATION_ERROR
Trigger: A query parameter cannot be decoded or does not match the declared wire type.
Description: Protocol-level query error.
- Example message: The query parameters are invalid.

## Error Response — HTTP 422

- Code: UNPROCESSABLE_REQUEST
Trigger: The syntactically valid request cannot be completed.
Description: Public processing failure.
- Example message: The request could not be completed.

## Error Response — HTTP 500

- Code: INTERNAL_ERROR
Trigger: An unexpected server error prevents trips from being returned.
Description: Unexpected trip-service failure.
- Example message: Internal Server Error

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md).

Pagination fields follow the common API contract.
