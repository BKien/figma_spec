# API-UC-10-03 — DELETE /api/v1/comparison/items/:variantId

## API ID

`API-UC-10-03`

## API Name

Compare Products — DELETE /api/v1/comparison/items/:variantId

## Related Use Case IDs

- `UC-10`

## Method

`DELETE`

## Path

`/api/v1/comparison/items/:variantId`

## Description

Provides the wire operation referenced by the supplied Compare Products specification.

## Authentication

Authentication context is supplied when required by the preserved source contract.

## Authorization

The service evaluates the submitted operation context.

## Request Headers

None.

## Path Parameters

### `variantId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as an opaque path string.
- Description: Identifies the requested path resource on the wire.
- Example: `example-variantId`

## Query Parameters

None.

## Request Body

None.

## Success Response — HTTP 200

### `success`

- Type: boolean
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON boolean.
- Description: Indicates a successful protocol outcome.
- Example: `true`

### `data`

- Type: object
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON object.
- Description: Contains the operation-specific response fields defined by the preserved source contract.
- Example: `{}`

## Error Response — HTTP 400

### `error`

- Type: object
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON object.
- Description: Contains the public protocol error.
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
- Description: Human-readable public error summary.
- Example: `The request could not be processed.`

- Trigger: Malformed wire input.

## Notes

Detailed endpoint fields, status codes, examples, and public outcomes are preserved in [the supplied source](../source/clicon-uc-10-compare-products.md). Business behavior is specified by [UC-10](../uc/uc-10-compare-products.md).
