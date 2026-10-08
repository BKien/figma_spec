---
artifact_type: api-contract
status: Frozen
api_id: API-REVIEW-LIST
related_uc_ids: ["UC-03", "UC-18"]
---

# API-REVIEW-LIST: Review List

## General Information

### API ID

API-REVIEW-LIST

### API Name

Review List

### Related Use Case IDs

- UC-03
- UC-18

### Method

GET

### Path

/api/v1/reviews

### Description

Returns a paginated review collection.

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

Example: Reviews retrieved.

### data.items[]

Type: object array; Required: Yes; Nullable: No
- Fields: id (string), authorName (string), rating (integer), comment (string), publishedAt (ISO 8601 date-time string), verifiedBooking (boolean).

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Reviews in the current page.

Example: [{"id": "booking_01JABCDEF", "authorName": "A***", "rating": 5, "comment": "A comfortable stay.", "publishedAt": "2026-10-07T09:00:00Z", "verifiedBooking": true}]

### data.total

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Reported collection size.

Example: 42

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

Example: true

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
Trigger: An unexpected server error prevents reviews from being returned.
Description: Unexpected review-service failure.
- Example message: Internal Server Error

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md).

Pagination fields follow the common API contract.
