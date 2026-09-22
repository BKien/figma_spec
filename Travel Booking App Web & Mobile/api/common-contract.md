# Common API Contract

## Base Path

`/api/v1`

## Media Type

`application/json`

## Authentication Header

Protected endpoints receive credentials through `Authorization: Bearer <access-token>`.

## Date and Time Representation

Date values use `YYYY-MM-DD`. Date-time values use ISO 8601 with an explicit UTC offset.

## Money Representation

Money objects expose:

- `amount`
  - Type: number
  - Required: Yes
  - Nullable: No
  - Description: Monetary amount returned by the endpoint.
  - Example: `125.50`
- `currency`
  - Type: string
  - Format: ISO 4217 currency code
  - Required: Yes
  - Nullable: No
  - Description: Currency associated with the amount.
  - Example: `USD`

## Pagination Representation

Paginated responses expose:

- `items`: array containing the resources for the current page.
- `total`: integer containing the reported collection size.
- `limit`: integer echoing the applied page size.
- `offset`: integer echoing the applied starting position.
- `hasMore`: boolean indicating whether another page can be requested.

## Success Envelope

- `success`
  - Type: boolean
  - Required: Yes
  - Nullable: No
  - Description: Indicates that the HTTP operation completed successfully.
  - Example: `true`
- `message`
  - Type: string
  - Required: Yes
  - Nullable: No
  - Description: Human-readable outcome summary.
  - Example: `Request completed successfully.`
- `data`
  - Type: object, array, or null as declared by the endpoint
  - Required: Yes
  - Description: Endpoint-specific response payload.

## Error Envelope

- `success`
  - Type: boolean
  - Required: Yes
  - Nullable: No
  - Example: `false`
- `message`
  - Type: string or string array
  - Required: Yes
  - Nullable: No
  - Description: Public error description.
- `code`
  - Type: string
  - Required: Yes
  - Nullable: No
  - Description: Stable machine-readable error category.
- `details`
  - Type: string array
  - Required: No
  - Nullable: No
  - Description: Optional protocol-level error details.

## Standard Error Categories

### HTTP 400 — `VALIDATION_ERROR`

The submitted HTTP payload cannot be decoded or does not match the declared wire schema.

### HTTP 401 — `UNAUTHORIZED`

The endpoint did not accept the supplied authentication context.

### HTTP 403 — `FORBIDDEN`

The authenticated request is not permitted to access the endpoint result.

### HTTP 404 — `NOT_FOUND`

The requested resource cannot be returned.

### HTTP 409 — `CONFLICT`

The request conflicts with the current resource or operation state.

### HTTP 422 — `UNPROCESSABLE_REQUEST`

The syntactically valid request could not be completed.

### HTTP 429 — `RATE_LIMITED`

The service temporarily rejects additional requests from the client.

### HTTP 500 — `INTERNAL_ERROR`

An unexpected server error occurred.

### HTTP 502 — `UPSTREAM_ERROR`

An upstream dependency returned an unusable result.

### HTTP 503 — `SERVICE_UNAVAILABLE`

The endpoint is temporarily unavailable.

## Nested Objects and Arrays

Every member listed under `Fields` or `Segment fields` is required and non-null unless explicitly marked nullable or optional. An object array may be empty; each element follows its listed object fields. A nullable object is either JSON null or an object containing its declared fields. A money object follows Money Representation above. URI strings use URI syntax. Dotted field names describe object nesting, not literal JSON keys. The `guest` parent in booking requests is a required non-null object.

## Opaque Identifiers

All resource identifiers are opaque strings. Examples with prefixes illustrate the wire representation and do not declare a database column type.

## Optional Query Values

Optional query values are omitted when absent; a literal `null` is not a date, number, or integer. Repeated array parameters use one query occurrence per element. An omitted array parameter is represented by an empty array in the decoded request. The sort and currency defaults are declared in each search endpoint.
