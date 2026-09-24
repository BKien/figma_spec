# API-TAXI-OFFER-DETAIL — Get Taxi Rental Offer Details

## API ID

`API-TAXI-OFFER-DETAIL`

## API Name

Taxi Rental Offer Detail

## Related Use Case IDs

- `UC-12`

## Method

`GET`

## Path

`/api/v1/taxi-offers/{offerId}`

## Description

Returns the selected vehicle, assigned driver, rental period, allowance, price, and payment options.

## Authentication

Optional bearer access token.

## Authorization

Public.

## Request Headers

### `Authorization`

- Type: string
- Format: bearer token
- Required: No
- Nullable: No
- Validation: Must use the `Bearer <access-token>` syntax.
- Description: Carries an optional access token.
- Example: `Bearer eyJhbGciOiJIUzI1NiIs...`

## Path Parameters

### `offerId`

- Type: string
- Format: opaque identifier
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Selected Taxi offer identifier.
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
- Validation: Must be encoded as the declared JSON type.
- Example: `true`

### `message`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Example: `Taxi rental offer retrieved.`

### `data.offer`

- Type: object
- Required: Yes
- Nullable: No
- Fields: `id` (string), `location` (object), `pickupAt` (ISO 8601 date-time string), `dropoffAt` (ISO 8601 date-time string), `passengers` (integer), `distanceFromCenterKm` (number), `mileageAllowanceKm` (number), `deposit` (money object), `rating` (number), `total` (money object), `paymentMode` (string).
- Description: Rental facts displayed in the detail and checkout summary.

### `data.driver`

- Type: object
- Required: Yes
- Nullable: No
- Fields: `id` (string), `fullName` (string), `phone` (string), `imageUrl` (URI string).
- Description: Assigned driver card displayed by the Figma Taxi checkout.

### `data.vehicle`

- Type: object
- Required: Yes
- Nullable: No
- Fields: `id` (string), `displayName` (string), `registrationNumber` (string), `category` (string), `transmission` (string), `electricType` (string), `seatCapacity` (integer), `largeBagCapacity` (integer), `smallBagCapacity` (integer), `imageUrl` (URI string).
- Description: Selected vehicle details.

## Error Response — HTTP 400

- Code: `VALIDATION_ERROR`
- Trigger: The path value cannot be decoded using the declared wire syntax.
- Description: Protocol-level request error.
- Example message: `The request could not be completed.`

## Error Response — HTTP 401

- Code: `UNAUTHORIZED`
- Trigger: The endpoint does not accept the supplied optional authentication context.
- Description: Authentication error.
- Example message: `The request could not be completed.`

## Error Response — HTTP 404

- Code: `NOT_FOUND`
- Trigger: The requested offer cannot be returned.
- Description: Public not-found response.
- Example message: `The request could not be completed.`

## Error Response — HTTP 409

- Code: `OFFER_CONFLICT`
- Trigger: The requested detail conflicts with the current offer state.
- Description: Public offer conflict.
- Example message: `The request could not be completed.`

## Error Response — HTTP 503

- Code: `SERVICE_UNAVAILABLE`
- Trigger: The endpoint is temporarily unable to return the offer.
- Description: Temporary detail failure.
- Example message: `The request could not be completed.`

## Notes

Response envelopes and money values follow the [common API contract](common-contract.md). Driver phone and vehicle registration are included because both are visibly presented in the supplied mobile Figma checkout.
