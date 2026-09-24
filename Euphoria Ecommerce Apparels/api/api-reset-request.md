# API-RESET-REQUEST — Request reset email

## API ID

`API-RESET-REQUEST`

## API Name

Request reset email.

## Related Use Case IDs

- `UC-09` — [specification](../uc/uc-09-request-password-reset.md)
- `UC-10` — [specification](../uc/uc-10-resend-password-reset-email.md)

## Method

`POST`

## Path

`/v1/password-reset-requests`

## Description

Request reset email for the web client. Request and response objects are defined in [common wire definitions](common-contract.md).

## Authentication

None.

## Authorization

Public operation.

## Request Headers

### `Accept`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: HTTP media type syntax; allowed value application/json.
- Description: Response media type.
- Example: `"application/json"`.

### `Content-Type`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: HTTP media type syntax; allowed value application/json.
- Description: Request media type.
- Example: `"application/json"`.

## Path Parameters

None.

## Query Parameters

None.

## Request Body

### `body`

- Type: ResetEmail.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: JSON object; full ResetEmail field definitions are in common-contract.md.
- Example: `{"email": "alex@example.com"}`.

```json
{
  "email": "alex@example.com"
}
```

## Success Response — HTTP 202

Content-Type: application/json.

### `data`

- Type: Accepted.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Accepted object; all nested fields are defined in common-contract.md.
- Example: `{"accepted": true}`.

### `requestId`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Opaque response correlation identifier.
- Example: `"req_01"`.

```json
{
  "data": {
    "accepted": true
  },
  "requestId": "req_01"
}
```

## Error Response — HTTP 400

- Trigger: Malformed wire input.

Content-Type: application/json.

### `error`

- Type: object.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Error object with code and message.
- Example: `{"code": "MALFORMED_REQUEST", "message": "Malformed wire input."}`.

### `error.code`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Membership in the public enum stated in the description.
- Description: Public enum: MALFORMED_REQUEST.
- Example: `"MALFORMED_REQUEST"`.

### `error.message`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Display message.
- Example: `"Malformed wire input."`.

### `requestId`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Opaque response correlation identifier.
- Example: `"req_01"`.

## Error Response — HTTP 429

- Trigger: Request temporarily limited.

Content-Type: application/json.

### `error`

- Type: object.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Error object with code and message.
- Example: `{"code": "REQUEST_LIMITED", "message": "Request temporarily limited."}`.

### `error.code`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Membership in the public enum stated in the description.
- Description: Public enum: REQUEST_LIMITED.
- Example: `"REQUEST_LIMITED"`.

### `error.message`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Display message.
- Example: `"Request temporarily limited."`.

### `requestId`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Opaque response correlation identifier.
- Example: `"req_01"`.

## Error Response — HTTP 503

- Trigger: Temporary service failure.

Content-Type: application/json.

### `error`

- Type: object.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Error object with code and message.
- Example: `{"code": "SERVICE_UNAVAILABLE", "message": "Temporary service failure."}`.

### `error.code`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Membership in the public enum stated in the description.
- Description: Public enum: SERVICE_UNAVAILABLE.
- Example: `"SERVICE_UNAVAILABLE"`.

### `error.message`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Display message.
- Example: `"Temporary service failure."`.

### `requestId`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Opaque response correlation identifier.
- Example: `"req_01"`.

## Notes

This is a proposed contract, not a discovered endpoint. Field definitions in [common wire definitions](common-contract.md) are part of this contract. There are no pagination parameters in this version. All declared errors use the stated JSON envelope.
