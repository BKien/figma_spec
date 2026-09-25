# API-ACCOUNT-REGISTER — Register an Account

## API ID

`API-ACCOUNT-REGISTER`

## API Name

Register an Account

## Related Use Case IDs

- `UC-01`

## Method

`POST`

## Path

`/api/v1/accounts`

## Description

Accepts the displayed register an account interaction and returns its public result.

## Authentication

None.

## Authorization

Public endpoint.

## Request Headers

### `Content-Type`

- Type: string
- Format: MIME type
- Required: Yes
- Nullable: No
- Allowed values: application/json
- Validation: Must identify the `application/json` media type.
- Description: Declares the request media type.
- Example: `application/json`


## Path Parameters

None.

## Query Parameters

None.

## Request Body

### `email`

- Type: string
- Format: email
- Required: Yes
- Nullable: No
- Validation: Must use email-address syntax.
- Description: email supplied on the wire.
- Example: `alex@example.com`

### `password`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: password supplied on the wire.
- Example: `ExamplePassphrase1!`

### `displayName`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: displayName supplied on the wire.
- Example: `Alex Morgan`

### `agreementAccepted`

- Type: boolean
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON boolean.
- Description: agreementAccepted supplied on the wire.
- Example: `true`


## Success Response — HTTP 201

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

### `data.accountId`

- Type: string
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON string.
- Description: data accountId supplied on the wire.
- Example: `acc_123`

### `data.verificationRequired`

- Type: boolean
- Required: Yes
- Nullable: No
- Validation: Must be encoded as a JSON boolean.
- Description: data verificationRequired supplied on the wire.
- Example: `true`




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

## Error Response — HTTP 409

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
- Example: `OPERATION_CONFLICT`

- Trigger: Operation conflict response.

## Notes

The common response envelope and pagination conventions are defined in [common-contract.md](common-contract.md). Business behavior is specified only in [UC-01](../uc/uc-01-register-account.md).
