# API-ORDER-DETAIL — Read order detail

## API ID

`API-ORDER-DETAIL`

## API Name

Read order detail.

## Related Use Case IDs

- `UC-16` — [specification](../uc/uc-16-view-order-history.md)
- `UC-18` — [specification](../uc/uc-18-view-order-detail.md)

## Method

`GET`

## Path

`/v1/me/orders/{orderId}`

## Description

Read order detail for the web client. Request and response objects are defined in [common wire definitions](common-contract.md).

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

### `Cookie`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: HTTP Cookie header encoding.
- Description: HTTP cookie encoding; euphoria_session carries an opaque value.
- Example: `"euphoria_session=opaque-session-value"`.

## Path Parameters

### `orderId`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Opaque order identifier.
- Example: `"ord_01"`.

## Query Parameters

None.

## Request Body

None.

## Success Response — HTTP 200

Content-Type: application/json.

### `data`

- Type: OrderDetail.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: OrderDetail object; all nested fields are defined in common-contract.md.
- Example: `{"order": {"id": "ord_01", "number": "EU-1001", "placedAt": "2026-09-24T02:00:00Z", "status": "PLACED", "paymentMethod": "COD", "estimatedDelivery": null, "total": {"amount": "34.00", "currency": "USD"}, "items": [{"id": "cl_01", "variantId": "var_01", "title": "Printed shirt", "imageUrl": "https://example.com/shirt.jpg", "color": "Black", "size": "M", "quantity": 1, "unitPrice": {"amount": "29.00", "currency": "USD"}, "lineTotal": {"amount": "29.00", "currency": "USD"}}]}, "events": [{"status": "PLACED", "occurredAt": "2026-09-24T02:00:00Z", "message": "Order received."}]}`.

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
    "order": {
      "id": "ord_01",
      "number": "EU-1001",
      "placedAt": "2026-09-24T02:00:00Z",
      "status": "PLACED",
      "paymentMethod": "COD",
      "estimatedDelivery": null,
      "total": {
        "amount": "34.00",
        "currency": "USD"
      },
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
      ]
    },
    "events": [
      {
        "status": "PLACED",
        "occurredAt": "2026-09-24T02:00:00Z",
        "message": "Order received."
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

## Error Response — HTTP 404

- Trigger: Unavailable resource response.

Content-Type: application/json.

### `error`

- Type: object.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Error object with code and message.
- Example: `{"code": "RESOURCE_UNAVAILABLE", "message": "Unavailable resource response."}`.

### `error.code`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Membership in the public enum stated in the description.
- Description: Public enum: RESOURCE_UNAVAILABLE.
- Example: `"RESOURCE_UNAVAILABLE"`.

### `error.message`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Display message.
- Example: `"Unavailable resource response."`.

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
