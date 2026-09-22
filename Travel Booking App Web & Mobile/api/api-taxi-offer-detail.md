# API-TAXI-OFFER-DETAIL — Get Taxi Offer Details

## API ID

`API-TAXI-OFFER-DETAIL`

## API Name

Taxi Offer Details

## Related Use Case IDs

- `UC-12`

## Method

`GET`

## Path

`/api/v1/taxi-offers/{offerId}`

## Description

Returns trip, price, capacity, driver, and vehicle data for one taxi offer.

## Authentication

Optional bearer access token

## Authorization

None

## Request Headers

### `Authorization`

- Type: string
- Required: No
- Nullable: No
- Format: bearer token
- Validation: Must use the `Bearer <access-token>` syntax when supplied.
- Description: Optional access token.

## Path Parameters

### `offerId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as one path segment.
- Description: Opaque taxi-offer identifier.
- Example: `to_01JABCDEF`

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
- Example: `Taxi offer details retrieved.`

### `data.id`

- Type: string
- Required: Yes
- Nullable: No
- Description: Taxi-offer identifier.

### `data.pickupAt`

- Type: string
- Format: ISO 8601 date-time
- Required: Yes
- Nullable: No
- Description: Pickup timestamp.

### `data.dropoffAt`

- Type: string
- Format: ISO 8601 date-time
- Required: Yes
- Nullable: No
- Description: Drop-off timestamp.

### `data.seats`

- Type: integer
- Required: Yes
- Nullable: No
- Description: Seat count represented by the offer.

### `data.total`

- Type: money object
- Required: Yes
- Nullable: No
- Description: Offer total.

### `data.driver`

- Type: object
- Required: Yes
- Nullable: No
- Fields: `id` (string), `fullName` (string), `phone` (string), `imageUrl` (nullable URI string).
- Description: Driver data returned for display.

### `data.vehicle`

- Type: object
- Required: Yes
- Nullable: No
- Fields: `id` (string), `registrationNumber` (string), `vehicleType` (string), `seatCapacity` (integer).
- Description: Vehicle data returned for display.

## Error Response — HTTP 401

- Code: `UNAUTHORIZED`
- Trigger: The endpoint does not accept the supplied authentication context.
- Description: Public authentication failure.
- Example message: `The request could not be completed.`

## Error Response — HTTP 404

- Code: `TAXI_OFFER_NOT_FOUND`
- Trigger: The requested taxi offer cannot be returned.
- Description: Public not-found response.
- Example message: `The requested taxi offer was not found.`

## Error Response — HTTP 409

- Code: `OFFER_CONFLICT`
- Trigger: The request conflicts with the current offer state.
- Description: Public offer conflict.
- Example message: `The taxi offer cannot be returned in its current state.`

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md).

Contact values are represented exactly as returned by this public response contract.
