---
artifact_type: api-contract
status: Frozen
api_id: API-STAY-DETAIL
related_uc_id: UC-07
---

# API-STAY-DETAIL: Stay Details

## General Information

### API ID

API-STAY-DETAIL

### API Name

Stay Details

### Related Use Case IDs

- UC-07

### Method

GET

### Path

/api/v1/stays/{stayId}

### Description

Returns descriptive, location, amenity, media, rating, and contact data for one stay.

### Authentication

Public

### Authorization

None

## Request Header(s)

None.

## Path Parameter(s)

### path.stayId

Type: string; Required: Yes; Nullable: No

Trigger: Every request using the stayId path segment.

Description: Opaque stay identifier.

Example: stay_01JABCDEF

Validation: Must be encoded as one path segment.

## Query Parameter(s)

### query.offerId

Type: string; Required: No; Nullable: No

Trigger: When the client supplies the offerId query parameter.

Description: Selected stay-offer reference.

Example: "offer_01JABCDEF"

Validation: Must be encoded as a query-string value.

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

Example: Stay details retrieved.

### data.id

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Stay identifier.

Example: "stay_01JABCDEF"

### data.name

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Display name.

Example: "Example Riverside Hotel"

### data.description

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Descriptive content.

Example: "A comfortable stay near the city center."

### data.rating

Type: number; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Display rating.

Example: 5

### data.reviewCount

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Display review count.

Example: 25

### data.amenities

Type: string array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Amenity labels.

Example: ["Wi-Fi"]

### data.imageUrls

Type: URI string array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Media URLs.

Example: ["https://example.com/images/travel.jpg"]

### data.location

Type: object; Required: Yes; Nullable: No
- Fields: name (string), address (string), latitude (nullable number), longitude (nullable number), countryCode (string).

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Display location.

Example: {"name": "Example Riverside Hotel", "address": "123 Example Street, Kyoto", "latitude": 35.0116, "longitude": 135.7681, "countryCode": "JP"}

### data.contact

Type: object; Required: Yes; Nullable: No
- Fields: phone (nullable string), email (nullable email string).

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Public contact data returned by the endpoint.

Example: {"phone": "+14155550123", "email": "alex@example.com"}

### data.currentOffer

Type: object; Required: Yes; Nullable: Yes
- Fields when non-null: offerId (string), total (money object), expiresAt (ISO 8601 date-time string).

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Offer presentation included with the detail.

Example: {"offerId": "offer_01JABCDEF", "total": {"amount": 300.0, "currency": "USD"}, "expiresAt": "2026-10-10T20:30:00Z"}

## Error Response — HTTP 404

- Code: STAY_NOT_FOUND
Trigger: The requested stay cannot be returned.
Description: Public not-found response.
- Example message: The requested stay was not found.

## Error Response — HTTP 500

- Code: INTERNAL_ERROR
Trigger: An unexpected server error prevents details from being returned.
Description: Unexpected stay-service failure.
- Example message: Internal Server Error

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md).

The response contains display-ready data only.
