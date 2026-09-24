# API-ADDRESS-CREATE — Add address

## API ID

`API-ADDRESS-CREATE`

## API Name

Add address.

## Related Use Case IDs

- `UC-13` — [specification](../uc/uc-13-add-address.md)

## Method

`POST`

## Path

`/v1/me/addresses`

## Description

Add address for the web client. Request and response objects are defined in [common wire definitions](common-contract.md).

## Authentication

Cookie named euphoria_session.

## Authorization

Access outcomes are represented by HTTP 401 and HTTP 403.

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

### `Cookie`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: HTTP Cookie header encoding.
- Description: HTTP cookie encoding; euphoria_session carries an opaque value.
- Example: `"euphoria_session=opaque-session-value"`.

### `X-CSRF-Token`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Opaque request header value.
- Example: `"opaque-csrf-value"`.

## Path Parameters

None.

## Query Parameters

None.

## Request Body

### `body`

- Type: NewAddress.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: JSON object; full NewAddress field definitions are in common-contract.md.
- Example: `{"details": {"firstName": "Alex", "lastName": "Lee", "country": "US", "company": null, "street": "10 Sample Street", "unit": null, "city": "Sample City", "state": "CA", "postalCode": "90001", "phone": "+12025550123", "instructions": null}, "defaultShipping": false, "defaultBilling": false, "expectedVersion": 1}`.

```json
{
  "details": {
    "firstName": "Alex",
    "lastName": "Lee",
    "country": "US",
    "company": null,
    "street": "10 Sample Street",
    "unit": null,
    "city": "Sample City",
    "state": "CA",
    "postalCode": "90001",
    "phone": "+12025550123",
    "instructions": null
  },
  "defaultShipping": false,
  "defaultBilling": false,
  "expectedVersion": 1
}
```

## Success Response — HTTP 200

Content-Type: application/json.

### `data`

- Type: AddressBook.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: AddressBook object; all nested fields are defined in common-contract.md.
- Example: `{"version": 1, "items": [{"id": "addr_01", "details": {"firstName": "Alex", "lastName": "Lee", "country": "US", "company": null, "street": "10 Sample Street", "unit": null, "city": "Sample City", "state": "CA", "postalCode": "90001", "phone": "+12025550123", "instructions": null}, "defaultShipping": false, "defaultBilling": false}]}`.

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
    "version": 1,
    "items": [
      {
        "id": "addr_01",
        "details": {
          "firstName": "Alex",
          "lastName": "Lee",
          "country": "US",
          "company": null,
          "street": "10 Sample Street",
          "unit": null,
          "city": "Sample City",
          "state": "CA",
          "postalCode": "90001",
          "phone": "+12025550123",
          "instructions": null
        },
        "defaultShipping": false,
        "defaultBilling": false
      }
    ]
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

## Error Response — HTTP 401

- Trigger: Rejected authentication context.

Content-Type: application/json.

### `error`

- Type: object.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Error object with code and message.
- Example: `{"code": "AUTHENTICATION_REJECTED", "message": "Rejected authentication context."}`.

### `error.code`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Membership in the public enum stated in the description.
- Description: Public enum: AUTHENTICATION_REJECTED.
- Example: `"AUTHENTICATION_REJECTED"`.

### `error.message`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Display message.
- Example: `"Rejected authentication context."`.

### `requestId`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Opaque response correlation identifier.
- Example: `"req_01"`.

## Error Response — HTTP 403

- Trigger: Rejected access context.

Content-Type: application/json.

### `error`

- Type: object.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Error object with code and message.
- Example: `{"code": "ACCESS_REJECTED", "message": "Rejected access context."}`.

### `error.code`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Membership in the public enum stated in the description.
- Description: Public enum: ACCESS_REJECTED.
- Example: `"ACCESS_REJECTED"`.

### `error.message`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Display message.
- Example: `"Rejected access context."`.

### `requestId`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Opaque response correlation identifier.
- Example: `"req_01"`.

## Error Response — HTTP 409

- Trigger: Operation conflict.

Content-Type: application/json.

### `error`

- Type: object.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Error object with code and message.
- Example: `{"code": "OPERATION_CONFLICT", "message": "Operation conflict."}`.

### `error.code`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Membership in the public enum stated in the description.
- Description: Public enum: OPERATION_CONFLICT.
- Example: `"OPERATION_CONFLICT"`.

### `error.message`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Display message.
- Example: `"Operation conflict."`.

### `requestId`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Opaque response correlation identifier.
- Example: `"req_01"`.

## Error Response — HTTP 422

- Trigger: Operation rejected.

Content-Type: application/json.

### `error`

- Type: object.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Error object with code and message.
- Example: `{"code": "REQUEST_REJECTED", "message": "Operation rejected."}`.

### `error.code`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Membership in the public enum stated in the description.
- Description: Public enum: REQUEST_REJECTED.
- Example: `"REQUEST_REJECTED"`.

### `error.message`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Display message.
- Example: `"Operation rejected."`.

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
