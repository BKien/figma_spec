# API-PRODUCT — Read product detail

## API ID

`API-PRODUCT`

## API Name

Read product detail.

## Related Use Case IDs

- `UC-05` — [specification](../uc/uc-05-view-product-details.md)
- `UC-14` — [specification](../uc/uc-14-view-wishlist.md)
- `UC-15` — [specification](../uc/uc-15-view-recently-viewed-products.md)

## Method

`GET`

## Path

`/v1/products/{productId}`

## Description

Read product detail for the web client. Request and response objects are defined in [common wire definitions](common-contract.md).

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

## Path Parameters

### `productId`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Opaque product identifier.
- Example: `"prd_01"`.

## Query Parameters

None.

## Request Body

None.

## Success Response — HTTP 200

Content-Type: application/json.

### `data`

- Type: ProductDetail.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: ProductDetail object; all nested fields are defined in common-contract.md.
- Example: `{"product": {"id": "prd_01", "title": "Printed shirt", "brand": "Euphoria", "imageUrl": "https://example.com/shirt.jpg", "price": {"amount": "29.00", "currency": "USD"}}, "description": "Printed cotton shirt.", "images": [], "rating": 3.5, "commentCount": 120, "questionCount": 4, "attributes": [], "variants": [{"id": "var_01", "size": "M", "color": "Black", "price": {"amount": "29.00", "currency": "USD"}, "purchasable": true}], "similarProducts": []}`.

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
    "product": {
      "id": "prd_01",
      "title": "Printed shirt",
      "brand": "Euphoria",
      "imageUrl": "https://example.com/shirt.jpg",
      "price": {
        "amount": "29.00",
        "currency": "USD"
      }
    },
    "description": "Printed cotton shirt.",
    "images": [],
    "rating": 3.5,
    "commentCount": 120,
    "questionCount": 4,
    "attributes": [],
    "variants": [
      {
        "id": "var_01",
        "size": "M",
        "color": "Black",
        "price": {
          "amount": "29.00",
          "currency": "USD"
        },
        "purchasable": true
      }
    ],
    "similarProducts": []
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
