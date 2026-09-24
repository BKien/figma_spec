# API-CATALOG — Read product listing

## API ID

`API-CATALOG`

## API Name

Read product listing.

## Related Use Case IDs

- `UC-01` — [specification](../uc/uc-01-explore-storefront.md)
- `UC-02` — [specification](../uc/uc-02-browse-products.md)
- `UC-03` — [specification](../uc/uc-03-filter-products.md)
- `UC-04` — [specification](../uc/uc-04-sort-products.md)

## Method

`GET`

## Path

`/v1/products`

## Description

Read product listing for the web client. Request and response objects are defined in [common wire definitions](common-contract.md).

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

None.

## Query Parameters

### `categoryId`

- Type: string.
- Required: No.
- Nullable: Yes.
- Default: None.
- Validation: JSON type only.
- Description: Category selection value.
- Example: `null`.

### `colors`

- Type: string[].
- Required: No.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Repeated query parameter, for example colors=black&colors=blue.
- Example: `[]`.

### `sizes`

- Type: string[].
- Required: No.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Repeated query parameter, for example sizes=M&sizes=L.
- Example: `[]`.

### `styles`

- Type: string[].
- Required: No.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Repeated query parameter, for example styles=Casual.
- Example: `[]`.

### `minAmount`

- Type: string.
- Required: No.
- Nullable: No.
- Default: None.
- Validation: Decimal string syntax: ^-?[0-9]+(?:\.[0-9]+)?$.
- Description: Decimal text value.
- Example: `"0.00"`.

### `maxAmount`

- Type: string.
- Required: No.
- Nullable: Yes.
- Default: None.
- Validation: Decimal string syntax: ^-?[0-9]+(?:\.[0-9]+)?$.
- Description: Decimal text value or omitted.
- Example: `null`.

### `sort`

- Type: string.
- Required: No.
- Nullable: No.
- Default: None.
- Validation: Membership in the public enum stated in the description.
- Description: Public enum: NEW, RECOMMENDED.
- Example: `"RECOMMENDED"`.

## Request Body

None.

## Success Response — HTTP 200

Content-Type: application/json.

### `data`

- Type: CatalogResult.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: CatalogResult object; all nested fields are defined in common-contract.md.
- Example: `{"items": [{"id": "prd_01", "title": "Printed shirt", "brand": "Euphoria", "imageUrl": "https://example.com/shirt.jpg", "price": {"amount": "29.00", "currency": "USD"}}], "categories": [], "colors": [], "sizes": [], "styles": [], "total": 1}`.

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
    "items": [
      {
        "id": "prd_01",
        "title": "Printed shirt",
        "brand": "Euphoria",
        "imageUrl": "https://example.com/shirt.jpg",
        "price": {
          "amount": "29.00",
          "currency": "USD"
        }
      }
    ],
    "categories": [],
    "colors": [],
    "sizes": [],
    "styles": [],
    "total": 1
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
