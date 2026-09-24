# API-CHECKOUT-PREVIEW — Read checkout summary

## API ID

`API-CHECKOUT-PREVIEW`

## API Name

Read checkout summary.

## Related Use Case IDs

- `UC-07` — [specification](../uc/uc-07-review-checkout.md)
- `UC-08` — [specification](../uc/uc-08-place-cash-on-delivery-order.md)

## Method

`POST`

## Path

`/v1/me/checkout/preview`

## Description

Read checkout summary for the web client. Request and response objects are defined in [common wire definitions](common-contract.md).

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

- Type: CheckoutRequest.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: JSON object; full CheckoutRequest field definitions are in common-contract.md.
- Example: `{"cartVersion": 1, "billing": {"firstName": "Alex", "lastName": "Lee", "country": "US", "company": null, "street": "10 Sample Street", "unit": null, "city": "Sample City", "state": "CA", "postalCode": "90001", "phone": "+12025550123", "instructions": null}, "shipping": null, "sameAsBilling": true}`.

```json
{
  "cartVersion": 1,
  "billing": {
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
  "shipping": null,
  "sameAsBilling": true
}
```

## Success Response — HTTP 200

Content-Type: application/json.

### `data`

- Type: CheckoutPreview.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: CheckoutPreview object; all nested fields are defined in common-contract.md.
- Example: `{"cartVersion": 1, "items": [{"id": "cl_01", "variantId": "var_01", "title": "Printed shirt", "imageUrl": "https://example.com/shirt.jpg", "color": "Black", "size": "M", "quantity": 1, "unitPrice": {"amount": "29.00", "currency": "USD"}, "lineTotal": {"amount": "29.00", "currency": "USD"}}], "subtotal": {"amount": "29.00", "currency": "USD"}, "discount": {"amount": "0.00", "currency": "USD"}, "shipping": {"amount": "5.00", "currency": "USD"}, "total": {"amount": "34.00", "currency": "USD"}, "estimatedDelivery": null}`.

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
    "cartVersion": 1,
    "items": [
      {
        "id": "cl_01",
        "variantId": "var_01",
        "title": "Printed shirt",
        "imageUrl": "https://example.com/shirt.jpg",
        "color": "Black",
        "size": "M",
        "quantity": 1,
        "unitPrice": {
          "amount": "29.00",
          "currency": "USD"
        },
        "lineTotal": {
          "amount": "29.00",
          "currency": "USD"
        }
      }
    ],
    "subtotal": {
      "amount": "29.00",
      "currency": "USD"
    },
    "discount": {
      "amount": "0.00",
      "currency": "USD"
    },
    "shipping": {
      "amount": "5.00",
      "currency": "USD"
    },
    "total": {
      "amount": "34.00",
      "currency": "USD"
    },
    "estimatedDelivery": null
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
