---
artifact_type: api-contract
status: Frozen
api_id: API-UNIQUE-PLACES-LIST
related_uc_id: UC-11
---

# API-UNIQUE-PLACES-LIST: List Unique Places

## General Information

### API ID

API-UNIQUE-PLACES-LIST

### API Name

List Unique Places

### Related Use Case IDs

UC-11

### Method

GET

### Path

/api/unique-places

### Description

Provides the Tripma unique-place collection.

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

Default: application/json

Allowed values: application/json

## Path Parameter(s)

None

## Query Parameter(s)

None

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

Type: array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Endpoint-specific response payload.

Example: [{"id": "e5030dbf-bdae-5b07-9772-17fc79301ee1", "placeName": "Kyoto", "city": "Kyoto", "imagePath": "https://example.com/images/travel.jpg", "price": 300, "currency": "USD", "description": "A comfortable stay near the city center.", "motivation": "Explore local culture and memorable landmarks."}]

### data[].id

Type: string; Format: UUID; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data[] object or array item is present and non-null.

Description: Identifier of the represented resource.

Example: "e5030dbf-bdae-5b07-9772-17fc79301ee1"

### data[].placeName

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data[] object or array item is present and non-null.

Description: Destination or place display name.

Example: "Kyoto"

### data[].city

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data[] object or array item is present and non-null.

Description: City display label.

Example: "Kyoto"

### data[].imagePath

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data[] object or array item is present and non-null.

Description: Image URI or path.

Example: "https://example.com/images/travel.jpg"

### data[].price

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data[] object or array item is present and non-null.

Description: Reported price in the response currency.

Example: 300

### data[].currency

Type: string; Format: ISO 4217 currency code; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data[] object or array item is present and non-null.

Description: ISO 4217 currency code for monetary values.

Example: "USD"

### data[].description

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data[] object or array item is present and non-null.

Description: Display description text.

Example: "A comfortable stay near the city center."

### data[].motivation

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data[] object or array item is present and non-null.

Description: Destination promotional display text.

Example: "Explore local culture and memorable landmarks."

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

This contract returns the active unique-place collection required by UC-11.
