# API-UC-16-01 — POST /api/v1/contact-submissions

## API ID

`API-UC-16-01`

## API Name

Submit a Contact Message — POST /api/v1/contact-submissions

## Related Use Case IDs

- `UC-16`

## Method

`POST`

## Path

`/api/v1/contact-submissions`

## Description

Provides the wire operation referenced by the supplied Submit a Contact Message specification.

## Authentication

Authentication context is supplied when required by the preserved source contract.

## Authorization

The service evaluates the submitted operation context.

## Request Headers

### `Content-Type`

- Type: string
- Format: MIME type
- Required: Yes
- Nullable: No
- Allowed values: application/json
- Validation: Must identify the `application/json` media type.
- Description: Declares the request representation.
- Example: `application/json`

## Path Parameters

None.

## Query Parameters

None.

## Request Body

### `payload`

- Type: object
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON object.
- Description: Carries the operation-specific request fields defined by the preserved source contract.
- Example: `{}`

## Success Response — HTTP 201

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

Detailed endpoint fields, status codes, examples, and public outcomes are preserved in [the supplied source](../source/dh-dental-uc-16-submit-contact-message.md). Business behavior is specified by [UC-16](../uc/uc-16-submit-contact-message.md).
