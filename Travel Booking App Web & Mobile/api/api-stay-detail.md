# API-STAY-DETAIL — Get Stay Details

## API ID

`API-STAY-DETAIL`

## API Name

Stay Details

## Related Use Case IDs

- `UC-07`

## Method

`GET`

## Path

`/api/v1/stays/{stayId}`

## Description

Returns descriptive, location, amenity, media, rating, and contact data for one stay.

## Authentication

Public

## Authorization

None

## Request Headers

None.

## Path Parameters

### `stayId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as one path segment.
- Description: Opaque stay identifier.
- Example: `stay_01JABCDEF`

## Query Parameters

### `offerId`

- Type: string
- Required: No
- Nullable: No
- Validation: Must be encoded as a query-string value.
- Description: Selected stay-offer reference.

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
- Example: `Stay details retrieved.`

### `data.id`

- Type: string
- Required: Yes
- Nullable: No
- Description: Stay identifier.

### `data.name`

- Type: string
- Required: Yes
- Nullable: No
- Description: Display name.

### `data.description`

- Type: string
- Required: Yes
- Nullable: No
- Description: Descriptive content.

### `data.rating`

- Type: number
- Required: Yes
- Nullable: No
- Description: Display rating.

### `data.reviewCount`

- Type: integer
- Required: Yes
- Nullable: No
- Description: Display review count.

### `data.amenities`

- Type: string array
- Required: Yes
- Nullable: No
- Description: Amenity labels.

### `data.imageUrls`

- Type: URI string array
- Required: Yes
- Nullable: No
- Description: Media URLs.

### `data.location`

- Type: object
- Required: Yes
- Nullable: No
- Fields: `name` (string), `address` (string), `latitude` (nullable number), `longitude` (nullable number), `countryCode` (string).
- Description: Display location.

### `data.contact`

- Type: object
- Required: Yes
- Nullable: No
- Fields: `phone` (nullable string), `email` (nullable email string).
- Description: Public contact data returned by the endpoint.

### `data.currentOffer`

- Type: object
- Required: Yes
- Nullable: Yes
- Fields when non-null: `offerId` (string), `total` (money object), `expiresAt` (ISO 8601 date-time string).
- Description: Offer presentation included with the detail.

## Error Response — HTTP 404

- Code: `STAY_NOT_FOUND`
- Trigger: The requested stay cannot be returned.
- Description: Public not-found response.
- Example message: `The requested stay was not found.`

## Error Response — HTTP 500

- Code: `INTERNAL_ERROR`
- Trigger: An unexpected server error prevents details from being returned.
- Description: Unexpected stay-service failure.
- Example message: `Internal Server Error`

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md).

The response contains display-ready data only.
