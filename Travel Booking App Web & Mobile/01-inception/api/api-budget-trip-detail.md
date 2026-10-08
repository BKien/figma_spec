---
artifact_type: api-contract
status: Frozen
api_id: API-BUDGET-TRIP-DETAIL
related_uc_id: UC-17
---

# API-BUDGET-TRIP-DETAIL: Budget Trip Details

## General Information

### API ID

API-BUDGET-TRIP-DETAIL

### API Name

Budget Trip Details

### Related Use Case IDs

- UC-17

### Method

GET

### Path

/api/v1/budget-trips/{tripId}

### Description

Returns destination, description, attraction, media, and price data for one budget trip.

### Authentication

Public

### Authorization

None

## Request Header(s)

None.

## Path Parameter(s)

### path.tripId

Type: string; Required: Yes; Nullable: No

Trigger: Every request using the tripId path segment.

Description: Opaque budget-trip identifier.

Example: trip_01JABCDEF

Validation: Must be encoded as one path segment.

## Query Parameter(s)

None.

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

Example: Budget trip details retrieved.

### data.id

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Budget-trip identifier.

Example: "trip_01JABCDEF"

### data.title

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Display title.

Example: "A weekend in Kyoto"

### data.description

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Descriptive content.

Example: "A comfortable stay near the city center."

### data.destination

Type: object; Required: Yes; Nullable: No
- Fields: id (string), name (string), countryCode (string).

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Destination data returned for display.

Example: {"id": "destination_01JABCDEF", "name": "Kyoto", "countryCode": "JP"}

### data.attractions

Type: string array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Attraction labels.

Example: ["Historic district"]

### data.imageUrls

Type: URI string array; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Media URLs.

Example: ["https://example.com/images/travel.jpg"]

### data.startingPrice

Type: money object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Display starting price.

Example: {"amount": 300.0, "currency": "USD"}

## Error Response — HTTP 404

- Code: BUDGET_TRIP_NOT_FOUND
Trigger: The requested budget trip cannot be returned.
Description: Public not-found response.
- Example message: The requested budget trip was not found.

## Error Response — HTTP 500

- Code: INTERNAL_ERROR
Trigger: An unexpected server error prevents details from being returned.
Description: Unexpected trip-service failure.
- Example message: Internal Server Error

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md).

The response contains display-ready data only.
