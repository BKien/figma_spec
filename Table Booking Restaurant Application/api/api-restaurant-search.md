# API-RESTAURANT-SEARCH — Search Restaurants

## API ID

`API-RESTAURANT-SEARCH`

## API Name

Search Restaurants

## Related Use Case IDs

- `UC-04`

## Method

`GET`

## Path

`/api/v1/restaurants`

## Description

Accepts the displayed search restaurants interaction and returns its public result.

## Authentication

None.

## Authorization

Public endpoint.

## Request Headers

None.

## Path Parameters

None.

## Query Parameters

### `location`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as one URL query value.
- Description: location supplied on the wire.
- Example: `Miami`

### `cuisine`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as one URL query value.
- Description: cuisine supplied on the wire.
- Example: `Italian`

### `meal`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as one URL query value.
- Description: meal supplied on the wire.
- Example: `dinner`

### `date`

- Type: string
- Format: date
- Required: Yes
- Nullable: No
- Validation: Must use ISO 8601 calendar-date syntax.
- Description: date supplied on the wire.
- Example: `2026-10-02`

### `time`

- Type: string
- Format: time
- Required: Yes
- Nullable: No
- Validation: Must use 24-hour HH:mm time syntax.
- Description: time supplied on the wire.
- Example: `19:00`

### `partySize`

- Type: integer
- Required: Yes
- Nullable: No
- Validation: Must use decimal integer query syntax.
- Description: partySize supplied on the wire.
- Example: `2`


## Request Body

None.

## Success Response — HTTP 200

### `success`

- Type: boolean
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON boolean.
- Description: success supplied on the wire.
- Example: `true`

### `data`

- Type: object
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON object.
- Description: data supplied on the wire.
- Example: `{}`

### `data.restaurants`

- Type: array
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON array.
- Description: data restaurants supplied on the wire.
- Example: `[]`

### `data.nextCursor`

- Type: string
- Required: No
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data nextCursor supplied on the wire.
- Example: `cur_123`

### `data.restaurants[].id`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data restaurants[] id supplied on the wire.
- Example: `rst_123`

### `data.restaurants[].name`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data restaurants[] name supplied on the wire.
- Example: `Villagio Restaurant and Bar`

### `data.restaurants[].city`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data restaurants[] city supplied on the wire.
- Example: `Miami`

### `data.restaurants[].cuisine`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data restaurants[] cuisine supplied on the wire.
- Example: `Italian`

### `data.restaurants[].rating`

- Type: number
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON number.
- Description: data restaurants[] rating supplied on the wire.
- Example: `4.5`

### `data.restaurants[].availabilityLabel`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data restaurants[] availabilityLabel supplied on the wire.
- Example: `11:15 AM`




## Error Response — HTTP 400

### `error`

- Type: object
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON object.
- Description: error supplied on the wire.
- Example: `{}`

### `error.code`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Stable public error identifier.
- Example: `MALFORMED_REQUEST`

### `error.message`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Human-readable error summary.
- Example: `The request could not be processed.`

- Trigger: Malformed wire input.

## Error Response — HTTP 503

### `error`

- Type: object
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON object.
- Description: error supplied on the wire.
- Example: `{}`

### `error.code`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Stable public error identifier.
- Example: `SERVICE_UNAVAILABLE`

### `error.message`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: Human-readable error summary.
- Example: `Please try again later.`

- Trigger: Temporary service failure.

## Notes

The common response envelope and pagination conventions are defined in [common-contract.md](common-contract.md). Business behavior is specified only in [UC-04](../uc/uc-04-search-restaurants.md).
