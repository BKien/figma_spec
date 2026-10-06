---
artifact_type: api-contract
status: Draft
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

Type: string; Format: MIME type
Required: No
Nullable: No

## Path Parameter(s)

None

## Query Parameter(s)

### cursor

Type: string
Required: No
Nullable: No

### limit

Type: integer
Required: No
Nullable: No

## Request Body

None

## Success Response — HTTP 200

### success

Type: boolean
Required: Yes
Nullable: No

### message

Type: string
Required: Yes
Nullable: No

### data

Type: object
Required: Yes
Nullable: No

### data.items

Type: array
Required: Yes
Nullable: No

### data.items[]

Type: object
Required: Yes
Nullable: No

### data.items[].reviewId

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.items[].reviewerDisplayName

Type: string
Required: Yes
Nullable: No

### data.items[].reviewerImagePath

Type: string
Required: Yes
Nullable: No

### data.items[].rating

Type: integer
Required: Yes
Nullable: No

### data.items[].content

Type: string
Required: Yes
Nullable: No

### data.items[].reviewedAt

Type: string; Format: ISO 8601
Required: Yes
Nullable: No

### data.nextCursor

Type: string
Required: No
Nullable: Yes

## Error Response — HTTP 400

### message

Type: string
Required: Yes
Nullable: No

## Error Response — HTTP 500

### message

Type: string
Required: Yes
Nullable: No

### retryable

Type: boolean
Required: Yes
Nullable: No

## Notes

This contract returns the paginated public customer-review collection required by UC-16.
