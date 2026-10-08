---
artifact_type: api-contract
status: Frozen
api_id: API-ACCOUNT-REGISTER
related_uc_id: UC-01
---

# API-ACCOUNT-REGISTER: Register an Account

## General Information

### API ID

API-ACCOUNT-REGISTER

### API Name

Register an Account

### Related Use Case IDs

- UC-01

### Method

POST

### Path

/api/v1/accounts

### Description

Accepts the displayed register an account interaction and returns its public result.

### Authentication

None.

### Authorization

Public endpoint.

## Request Header(s)

### headers.Content-Type

Type: string; Format: MIME type; Required: Yes; Nullable: No

Trigger: Every POST request to this endpoint.

Description: Declares the request media type.

Example: application/json

Note: Identifies the media type of the submitted request body.

Allowed values: application/json

Validation: Must identify the application/json media type.

## Path Parameter(s)

None.

## Query Parameter(s)

None.

## Request Body

### email

Type: string; Format: email; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: email supplied on the wire.

Example: alex@example.com

Validation: Must use email-address syntax.

### password

Type: string; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: password supplied on the wire.

Example: ExamplePassphrase1!

Validation: Must be encoded as a JSON string.

### displayName

Type: string; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: displayName supplied on the wire.

Example: Alex Morgan

Validation: Must be encoded as a JSON string.

### agreementAccepted

Type: boolean; Required: Yes; Nullable: No

Trigger: Every request body sent to this endpoint.

Description: agreementAccepted supplied on the wire.

Example: true

Validation: Must be encoded as a JSON boolean.

## Success Response — HTTP 201

### success

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response.

Description: success supplied on the wire.

Example: true

Validation: Must be encoded as a JSON boolean.

### data

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response.

Description: data supplied on the wire.

Example: {}

Validation: Must be encoded as a JSON object.

### data.accountId

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: data accountId supplied on the wire.

Example: acc_123

Validation: Must be encoded as a JSON string.

### data.verificationRequired

Type: boolean; Required: Yes; Nullable: No

Trigger: Included in the HTTP 201 success response when the containing data object or array item is present and non-null.

Description: data verificationRequired supplied on the wire.

Example: true

Validation: Must be encoded as a JSON boolean.

## Error Response — HTTP 400

### error

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 400 error response.

Description: error supplied on the wire.

Example: {}

Note: Field of the JSON error response.

Validation: Must be encoded as a JSON object.

### error.code

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 400 error response when the containing error object or array item is present and non-null.

Description: Stable public error identifier.

Example: MALFORMED_REQUEST

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Validation: Must be encoded as a JSON string.

### error.message

Type: string; Required: Yes; Nullable: No

Trigger: Malformed wire input.

Description: Human-readable error summary.

Example: The request could not be processed.

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Validation: Must be encoded as a JSON string.

## Error Response — HTTP 503

### error

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 503 error response.

Description: error supplied on the wire.

Example: {}

Note: Field of the JSON error response.

Validation: Must be encoded as a JSON object.

### error.code

Type: string; Required: Yes; Nullable: No

Trigger: Included in the HTTP 503 error response when the containing error object or array item is present and non-null.

Description: Stable public error identifier.

Example: SERVICE_UNAVAILABLE

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Validation: Must be encoded as a JSON string.

### error.message

Type: string; Required: Yes; Nullable: No

Trigger: Temporary service failure.

Description: Human-readable error summary.

Example: Please try again later.

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Validation: Must be encoded as a JSON string.

## Error Response — HTTP 409

### error

Type: object; Required: Yes; Nullable: No

Trigger: Included in the HTTP 409 error response.

Description: error supplied on the wire.

Example: {}

Note: Field of the JSON error response.

Validation: Must be encoded as a JSON object.

### error.code

Type: string; Required: Yes; Nullable: No

Trigger: Operation conflict response.

Description: Stable public error identifier.

Example: OPERATION_CONFLICT

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Validation: Must be encoded as a JSON string.

## Notes

The common response envelope and pagination conventions are defined in [common-contract.md](common-contract.md). Business behavior is specified only in [UC-01](../uc/uc-01-register-account.md).
