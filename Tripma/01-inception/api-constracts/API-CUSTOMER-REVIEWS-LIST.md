---
artifact_type: api-contract
status: Frozen
api_id: API-CUSTOMER-REVIEWS-LIST
related_uc_id: UC-16
---

# API-CUSTOMER-REVIEWS-LIST: List Customer Reviews

## General Information

### API ID

API-CUSTOMER-REVIEWS-LIST

### API Name

List Customer Reviews

### Related Use Case IDs

UC-16

### Method

GET

### Path

/api/comments

### Description

Provides the public Tripma customer-review collection.

### Authentication

Public

### Authorization

None

## Request Header(s)

### headers.Accept

Type: string; Format: MIME type; Required: No; Nullable: No

Trigger: When the client supplies the Accept header.

Description: Requested response media type.

Example: "application/json"

Note: Identifies the requested response media type.

## Path Parameter(s)

None

## Query Parameter(s)

### query.cursor

Type: string; Required: No; Nullable: No

Trigger: When the client supplies the cursor query parameter.

Description: Opaque pagination cursor.

Example: "opaque-page-cursor-01"

### query.limit

Type: integer; Required: No; Nullable: No

Trigger: When the client supplies the limit query parameter.

Description: Requested page size.

Example: 20

## Request Body

None

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

Example: "Request completed successfully."

### data

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Endpoint-specific response payload.

Example: {"items": [{"reviewId": "eb5716b4-e22c-57c8-8a27-8c3dd6ff79ed", "reviewerDisplayName": "Alex Morgan", "reviewerImagePath": "https://example.com/images/reviewer.jpg", "rating": 5, "content": "A comfortable trip with helpful staff.", "reviewedAt": "2026-10-07T09:00:00Z"}]}

### data.items

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Resource representations returned in this page.

Example: [{"reviewId": "eb5716b4-e22c-57c8-8a27-8c3dd6ff79ed", "reviewerDisplayName": "Alex Morgan", "reviewerImagePath": "https://example.com/images/reviewer.jpg", "rating": 5, "content": "A comfortable trip with helpful staff.", "reviewedAt": "2026-10-07T09:00:00Z"}]

### data.items[]

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Resource representations returned in this page.

Example: {"reviewId": "eb5716b4-e22c-57c8-8a27-8c3dd6ff79ed", "reviewerDisplayName": "Alex Morgan", "reviewerImagePath": "https://example.com/images/reviewer.jpg", "rating": 5, "content": "A comfortable trip with helpful staff.", "reviewedAt": "2026-10-07T09:00:00Z"}

### data.items[].reviewId

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.items[] object or array item is present and non-null.

Description: Review identifier.

Example: "eb5716b4-e22c-57c8-8a27-8c3dd6ff79ed"

### data.items[].reviewerDisplayName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.items[] object or array item is present and non-null.

Description: Reviewer display name.

Example: "Alex Morgan"

### data.items[].reviewerImagePath

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.items[] object or array item is present and non-null.

Description: Reviewer image URI or path.

Example: "https://example.com/images/reviewer.jpg"

### data.items[].rating

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.items[] object or array item is present and non-null.

Description: Reported numeric rating.

Example: 5

### data.items[].content

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.items[] object or array item is present and non-null.

Description: Review text.

Example: "A comfortable trip with helpful staff."

### data.items[].reviewedAt

Type: string; Format: ISO 8601; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data.items[] object or array item is present and non-null.

Description: Reviewed at timestamp in the declared ISO 8601 format.

Example: "2026-10-07T09:00:00Z"

### data.nextCursor

Type: string; Required: No; Nullable: Yes

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null and this optional property is returned.

Description: Opaque cursor for a subsequent page, or null when the response declares no cursor.

Example: "opaque-page-cursor-02"

## Error Response — HTTP 400

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 400 error response.

Description: Public error outcome summary.

Example: "The request does not match the declared wire schema."

Note: Field of the JSON error response.

## Error Response — HTTP 500

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 500 error response.

Description: Public error outcome summary.

Example: "An unexpected server error occurred."

Note: Field of the JSON error response.

### retryable

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 500 error response.

Description: Indicates whether the public response suggests retrying the request.

Example: false

Note: Field of the JSON error response.

## Notes

This contract returns the paginated public customer-review collection required by UC-16.
