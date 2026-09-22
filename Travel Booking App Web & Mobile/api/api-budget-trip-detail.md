# API-BUDGET-TRIP-DETAIL — Get Budget Trip Details

## API ID

`API-BUDGET-TRIP-DETAIL`

## API Name

Budget Trip Details

## Related Use Case IDs

- `UC-17`

## Method

`GET`

## Path

`/api/v1/budget-trips/{tripId}`

## Description

Returns destination, description, attraction, media, and price data for one budget trip.

## Authentication

Public

## Authorization

None

## Request Headers

None.

## Path Parameters

### `tripId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as one path segment.
- Description: Opaque budget-trip identifier.
- Example: `trip_01JABCDEF`

## Query Parameters

None.

## Request Body

None.

## Success Response — HTTP 200

### `success`

- Type: boolean
- Required: Yes
- Nullable: No
- Example: `true`

### `message`

- Type: string
- Required: Yes
- Nullable: No
- Example: `Budget trip details retrieved.`

### `data.id`

- Type: string
- Required: Yes
- Nullable: No
- Description: Budget-trip identifier.

### `data.title`

- Type: string
- Required: Yes
- Nullable: No
- Description: Display title.

### `data.description`

- Type: string
- Required: Yes
- Nullable: No
- Description: Descriptive content.

### `data.destination`

- Type: object
- Required: Yes
- Nullable: No
- Fields: `id` (string), `name` (string), `countryCode` (string).
- Description: Destination data returned for display.

### `data.attractions`

- Type: string array
- Required: Yes
- Nullable: No
- Description: Attraction labels.

### `data.imageUrls`

- Type: URI string array
- Required: Yes
- Nullable: No
- Description: Media URLs.

### `data.startingPrice`

- Type: money object
- Required: Yes
- Nullable: No
- Description: Display starting price.

## Error Response — HTTP 404

- Code: `BUDGET_TRIP_NOT_FOUND`
- Trigger: The requested budget trip cannot be returned.
- Description: Public not-found response.
- Example message: `The requested budget trip was not found.`

## Error Response — HTTP 500

- Code: `INTERNAL_ERROR`
- Trigger: An unexpected server error prevents details from being returned.
- Description: Unexpected trip-service failure.
- Example message: `Internal Server Error`

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md).

The response contains display-ready data only.
