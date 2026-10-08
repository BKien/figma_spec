---
artifact_type: api-contract
status: Frozen
api_id: API-TAXI-SEARCH
related_uc_ids: ["UC-09", "UC-10", "UC-11"]
---

# API-TAXI-SEARCH: Taxi Rental Search

## General Information

### API ID

API-TAXI-SEARCH

### API Name

Taxi Rental Search

### Related Use Case IDs

- UC-09
- UC-10
- UC-11

### Method

GET

### Path

/api/v1/taxi-offers

### Description

Returns vehicle-and-driver rental offers for one location and rental period.

### Authentication

None.

### Authorization

Public.

## Request Header(s)

None.

## Path Parameter(s)

None.

## Query Parameter(s)

### query.locationId

Type: string; Format: opaque identifier; Required: Yes; Nullable: No

Trigger: Every request includes the locationId query parameter.

Description: Selected rental location.

Example: loc_kurunegala

Validation: Must be encoded as a JSON string.

### query.pickupAt

Type: string; Format: ISO 8601 date-time; Required: Yes; Nullable: No

Trigger: Every request includes the pickupAt query parameter.

Description: Selected pick-up date and time.

Example: 2026-06-26T08:00:00+05:30

Validation: Must use ISO 8601 date-time syntax with an offset.

### query.dropoffAt

Type: string; Format: ISO 8601 date-time; Required: Yes; Nullable: No

Trigger: Every request includes the dropoffAt query parameter.

Description: Selected drop-off date and time.

Example: 2026-06-27T08:00:00+05:30

Validation: Must use ISO 8601 date-time syntax with an offset.

### query.passengers

Type: integer; Required: Yes; Nullable: No

Trigger: Every request includes the passengers query parameter.

Description: Selected passenger count.

Example: 2

Validation: Must be encoded as the declared JSON type.

### query.vehicleCategories

Type: string array; Required: No; Nullable: No

Trigger: When the client supplies the vehicleCategories query parameter.

Description: Selected car-category filters.

Example: ["SMALL", "ESTATE"]

Allowed values: SMALL, MEDIUM, LARGE, ESTATE

Validation: Must be encoded as a JSON array of strings.

### query.depositBands

Type: string array; Required: No; Nullable: No

Trigger: When the client supplies the depositBands query parameter.

Description: Selected pick-up-deposit bands shown by the interface.

Example: ["LKR_200_500"]

Allowed values: LKR_200_500, LKR_500_1000, LKR_1000_1200, LKR_1200_1500

Validation: Must be encoded as a JSON array of strings.

### query.electricTypes

Type: string array; Required: No; Nullable: No

Trigger: When the client supplies the electricTypes query parameter.

Description: Selected electric-car filters.

Example: ["HYBRID"]

Allowed values: FULLY_ELECTRIC, HYBRID

Validation: Must be encoded as a JSON array of strings.

### query.minPrice

Type: number; Required: No; Nullable: No

Trigger: When the client supplies the minPrice query parameter.

Description: Optional lower price filter.

Example: 200

Validation: Must be encoded as the declared JSON type.

### query.maxPrice

Type: number; Required: No; Nullable: No

Trigger: When the client supplies the maxPrice query parameter.

Description: Optional upper price filter.

Example: 1500

Validation: Must be encoded as the declared JSON type.

### query.sort

Type: string; Required: No; Nullable: No

Trigger: When the client supplies the sort query parameter.

Description: Selected result ordering.

Example: TOP_PICKS

Default: TOP_PICKS

Allowed values: TOP_PICKS

Validation: Must be encoded as a JSON string.

### query.limit

Type: integer; Required: No; Nullable: No

Trigger: When the client supplies the limit query parameter.

Description: Requested page size.

Example: 20

Default: 20

Validation: Must be encoded as the declared JSON type.

### query.offset

Type: integer; Required: No; Nullable: No

Trigger: When the client supplies the offset query parameter.

Description: Requested result offset.

Example: 0

Default: 0

Validation: Must be encoded as the declared JSON type.

### query.searchContextId

Type: string; Format: opaque identifier; Required: No; Nullable: No

Trigger: When the client supplies the searchContextId query parameter.

Description: Existing result context used for pagination or refinement.

Example: ts_01JABCDEF

Validation: Must be encoded as a JSON string.

### query.snapshotVersion

Type: integer; Required: No; Nullable: No

Trigger: When the client supplies the snapshotVersion query parameter.

Description: Existing result-context version.

Example: 1

Validation: Must be encoded as the declared JSON type.

### query.currency

Type: string; Required: No; Nullable: No

Trigger: When the client supplies the currency query parameter.

Description: Requested comparison currency.

Example: LKR

Default: LKR

Allowed values: ISO 4217 currency code

Validation: Must be encoded as a JSON string.

## Request Body

None.

## Success Response — HTTP 200

### success

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Indicates a successful response.

Example: true

Validation: Must be encoded as the declared JSON type.

### message

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response.

Description: Human-readable result summary.

Example: Taxi rental offers retrieved.

Validation: Must be encoded as a JSON string.

### data.items[]

Type: object array; Required: Yes; Nullable: No
- Fields: offerId (string), vehicleName (string), vehicleCategory (string), seats (integer), transmission (string), largeBagCapacity (integer), smallBagCapacity (integer), electricType (string), distanceFromCenterKm (number), mileageAllowanceKm (number), deposit (money object), rating (number), total (money object).

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Vehicle cards displayed by the Taxi results page.

Example: [{"offerId": "offer_01JABCDEF", "vehicleName": "Example Sedan", "vehicleCategory": "MEDIUM", "seats": 4, "transmission": "AUTOMATIC", "largeBagCapacity": 2, "smallBagCapacity": 2, "electricType": "HYBRID", "distanceFromCenterKm": 2.5, "mileageAllowanceKm": 150, "deposit": {"amount": 300.0, "currency": "LKR"}, "rating": 5, "total": {"amount": 300.0, "currency": "LKR"}}]

### data.total

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Total matching offers.

Example: 68

Validation: Must be encoded as the declared JSON type.

### data.limit

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Applied page size.

Example: 20

Validation: Must be encoded as the declared JSON type.

### data.offset

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Applied result offset.

Example: 0

Validation: Must be encoded as the declared JSON type.

### data.hasMore

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Indicates whether another page is available.

Example: true

Validation: Must be encoded as the declared JSON type.

### data.searchContextId

Type: string; Format: opaque identifier; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Returned result-context identifier.

Example: ts_01JABCDEF

Validation: Must be encoded as a JSON string.

### data.snapshotVersion

Type: integer; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Returned result-context version.

Example: 1

Validation: Must be encoded as the declared JSON type.

### data.validUntil

Type: string; Format: ISO 8601 date-time; Required: Yes; Nullable: No

Trigger: Included in the HTTP 200 success response when the containing data object or array item is present and non-null.

Description: Result-context expiry time.

Example: 2026-06-25T12:15:00+05:30

Validation: Must use ISO 8601 date-time syntax with an offset.

## Error Response — HTTP 400

- Code: VALIDATION_ERROR
Trigger: The request cannot be decoded or does not match the declared wire schema.
Description: Protocol-level request error.
- Example message: The request could not be completed.

## Error Response — HTTP 409

- Code: SEARCH_CONTEXT_CONFLICT
Trigger: The supplied result context cannot be used for this request.
Description: Public result-context conflict.
- Example message: The request could not be completed.

## Error Response — HTTP 422

- Code: UNPROCESSABLE_REQUEST
Trigger: The syntactically valid request cannot be processed.
Description: Public processing outcome.
- Example message: The request could not be completed.

## Error Response — HTTP 502

- Code: UPSTREAM_ERROR
Trigger: A required provider does not return a usable response.
Description: Provider failure.
- Example message: The request could not be completed.

## Error Response — HTTP 503

- Code: SERVICE_UNAVAILABLE
Trigger: The endpoint is temporarily unable to return results.
Description: Temporary search failure.
- Example message: The request could not be completed.

## Notes

Response envelopes, money values, and nested-field conventions follow the [common API contract](common-contract.md). The service name remains Taxi because that is the Figma navigation label; the wire data represents a vehicle and driver rented at one location between the supplied times.
