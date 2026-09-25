# API-UC-10-04 — GET /api/v1/job-seeker/introduction-video/media/:videoId

## API ID

`API-UC-10-04`

## API Name

Record and Manage an Introduction Video — GET /api/v1/job-seeker/introduction-video/media/:videoId

## Related Use Case IDs

- `UC-10`

## Method

`GET`

## Path

`/api/v1/job-seeker/introduction-video/media/:videoId`

## Description

Provides the wire operation referenced by the supplied Record and Manage an Introduction Video specification.

## Authentication

Authentication context is supplied when required by the preserved source contract.

## Authorization

The service evaluates the submitted operation context.

## Request Headers

None.

## Path Parameters

### `videoId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as an opaque path string.
- Description: Identifies the requested path resource on the wire.
- Example: `example-videoId`

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

Detailed endpoint fields, status codes, examples, and public outcomes are preserved in [the supplied source](../source/dh-dental-uc-10-manage-introduction-video.md). Business behavior is specified by [UC-10](../uc/uc-10-manage-introduction-video.md).
