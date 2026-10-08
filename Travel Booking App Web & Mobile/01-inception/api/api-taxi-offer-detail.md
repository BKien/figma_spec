---
artifact_type: api-contract
status: Frozen
api_id: API-TAXI-OFFER-DETAIL
related_uc_id: UC-12
---

# API-TAXI-OFFER-DETAIL: Taxi Rental Offer Detail

## General Information

### API ID

API-TAXI-OFFER-DETAIL

### API Name

Taxi Rental Offer Detail

### Related Use Case IDs

- UC-12

### Method

GET

### Path

/api/v1/taxi-offers/{offerId}

### Description

Returns the selected vehicle, assigned driver, rental period, allowance, price, and payment options.

### Authentication

Optional bearer access token.

### Authorization

Public.

## Request Header(s)

### headers.Authorization

Type: string; Format: bearer token; Required: No; Nullable: No

Trigger: When the client supplies the Authorization header.

Description: Carries an optional access token.

Example: Bearer eyJhbGciOiJIUzI1NiIs...

Note: Uses the HTTP Bearer authentication scheme.

Validation: Must use the Bearer <access-token> syntax.

## Path Parameter(s)

### path.offerId

Type: string; Format: opaque identifier; Required: Yes; Nullable: No

Trigger: Every request using the offerId path segment.

Description: Selected Taxi offer identifier.

Example: to_01JABCDEF

Validation: Must be encoded as a JSON string.

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

Validation: Must be encoded as the declared JSON type.

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Human-readable operation outcome summary.

Example: Taxi rental offer retrieved.

Validation: Must be encoded as a JSON string.

### data.offer

Type: object; Required: Yes; Nullable: No
- Fields: id (string), location (object), pickupAt (ISO 8601 date-time string), dropoffAt (ISO 8601 date-time string), passengers (integer), distanceFromCenterKm (number), mileageAllowanceKm (number), deposit (money object), rating (number), total (money object), paymentMode (string).

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Rental facts displayed in the detail and checkout summary.

Example: {"id": "offer_01JABCDEF", "location": {"name": "Kyoto", "countryCode": "JP"}, "pickupAt": "2026-10-10T09:00:00Z", "dropoffAt": "2026-10-10T20:30:00Z", "passengers": 1, "distanceFromCenterKm": 2.5, "mileageAllowanceKm": 150, "deposit": {"amount": 300.0, "currency": "LKR"}, "rating": 5, "total": {"amount": 300.0, "currency": "LKR"}, "paymentMode": "PAY_DRIVER"}

### data.driver

Type: object; Required: Yes; Nullable: No
- Fields: id (string), fullName (string), phone (string), imageUrl (URI string).

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Assigned driver card displayed by the Figma Taxi checkout.

Example: {"id": "driver_01JABCDEF", "fullName": "Alex Morgan", "phone": "+14155550123", "imageUrl": "https://example.com/images/travel.jpg"}

### data.vehicle

Type: object; Required: Yes; Nullable: No
- Fields: id (string), displayName (string), registrationNumber (string), category (string), transmission (string), electricType (string), seatCapacity (integer), largeBagCapacity (integer), smallBagCapacity (integer), imageUrl (URI string).

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Selected vehicle details.

Example: {"id": "vehicle_01JABCDEF", "displayName": "Example Sedan", "registrationNumber": "EXAMPLE-123", "category": "MEDIUM", "transmission": "AUTOMATIC", "electricType": "HYBRID", "seatCapacity": 4, "largeBagCapacity": 2, "smallBagCapacity": 2, "imageUrl": "https://example.com/images/travel.jpg"}

## Error Response — HTTP 400

- Code: VALIDATION_ERROR
Trigger: The path value cannot be decoded using the declared wire syntax.
Description: Protocol-level request error.
- Example message: The request could not be completed.

## Error Response — HTTP 401

- Code: UNAUTHORIZED
Trigger: The endpoint does not accept the supplied optional authentication context.
Description: Authentication error.
- Example message: The request could not be completed.

## Error Response — HTTP 404

- Code: NOT_FOUND
Trigger: The requested offer cannot be returned.
Description: Public not-found response.
- Example message: The request could not be completed.

## Error Response — HTTP 409

- Code: OFFER_CONFLICT
Trigger: The requested detail conflicts with the current offer state.
Description: Public offer conflict.
- Example message: The request could not be completed.

## Error Response — HTTP 503

- Code: SERVICE_UNAVAILABLE
Trigger: The endpoint is temporarily unable to return the offer.
Description: Temporary detail failure.
- Example message: The request could not be completed.

## Notes

Response envelopes and money values follow the [common API contract](common-contract.md). Driver phone and vehicle registration are included because both are visibly presented in the supplied mobile Figma checkout.
