---
artifact_type: api-contract
status: Frozen
api_id: API-PRODUCT
related_uc_ids: ["UC-05", "UC-14", "UC-15"]
---

# API-PRODUCT: Read product detail.

## General Information

### API ID

API-PRODUCT

### API Name

Read product detail.

### Related Use Case IDs

- UC-05 — [specification](../uc/uc-05-view-product-details.md)
- UC-14 — [specification](../uc/uc-14-view-wishlist.md)
- UC-15 — [specification](../uc/uc-15-view-recently-viewed-products.md)

### Method

GET

### Path

/v1/products/{productId}

### Description

Read product detail for the web client. Request and response objects are defined in [common wire definitions](common-contract.md).

### Authentication

None.

### Authorization

Public operation.

## Request Header(s)

### headers.Accept

Type: string.; Format: HTTP media type; Required: Yes.; Nullable: No.

Trigger: Every GET request to this endpoint.

Description: Response media type.

Example: "application/json".

Note: Identifies the requested response media type.

Default: None.

Validation: HTTP media type syntax; allowed value application/json.

## Path Parameter(s)

### path.productId

Type: string.; Required: Yes.; Nullable: No.

Trigger: Every request using the productId path segment.

Description: Opaque product identifier.

Example: "prd_01".

Default: None.

Validation: JSON type only.

## Query Parameter(s)

None.

## Request Body

None.

## Success Response — HTTP 200

Content-Type: application/json.

### data

Type: ProductDetail.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 200 success response.

Description: ProductDetail object; all nested fields are defined in common-contract.md.

Example: {"product": {"id": "prd_01", "title": "Printed shirt", "brand": "Euphoria", "imageUrl": "https://example.com/shirt.jpg", "price": {"amount": "29.00", "currency": "USD"}}, "description": "Printed cotton shirt.", "images": [], "rating": 3.5, "commentCount": 120, "questionCount": 4, "attributes": [], "variants": [{"id": "var_01", "size": "M", "color": "Black", "price": {"amount": "29.00", "currency": "USD"}, "purchasable": true}], "similarProducts": []}.

Default: None.

Validation: Object or array shape defined in common-contract.md.

### requestId

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 200 success response.

Description: Opaque response correlation identifier.

Example: "req_01".

~~~json
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
~~~

Default: None.

Validation: JSON type only.

## Error Response — HTTP 400

Trigger: Malformed wire input.

Content-Type: application/json.

### error

Type: object.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 400 error response.

Description: Error object with code and message.

Example: {"code": "MALFORMED_REQUEST", "message": "Malformed wire input."}.

Note: Field of the JSON error response.

Default: None.

Validation: JSON type only.

### error.code

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 400 error response when the containing error object or array item is present and non-null.

Description: Public enum: MALFORMED_REQUEST.

Example: "MALFORMED_REQUEST".

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Default: None.

Validation: Membership in the public enum stated in the description.

### error.message

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 400 error response when the containing error object or array item is present and non-null.

Description: Display message.

Example: "Malformed wire input.".

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Default: None.

Validation: JSON type only.

### requestId

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 400 error response.

Description: Opaque response correlation identifier.

Example: "req_01".

Note: Field of the JSON error response.

Default: None.

Validation: JSON type only.

## Error Response — HTTP 404

Trigger: Unavailable resource response.

Content-Type: application/json.

### error

Type: object.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 404 error response.

Description: Error object with code and message.

Example: {"code": "RESOURCE_UNAVAILABLE", "message": "Unavailable resource response."}.

Note: Field of the JSON error response.

Default: None.

Validation: JSON type only.

### error.code

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 404 error response when the containing error object or array item is present and non-null.

Description: Public enum: RESOURCE_UNAVAILABLE.

Example: "RESOURCE_UNAVAILABLE".

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Default: None.

Validation: Membership in the public enum stated in the description.

### error.message

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 404 error response when the containing error object or array item is present and non-null.

Description: Display message.

Example: "Unavailable resource response.".

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Default: None.

Validation: JSON type only.

### requestId

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 404 error response.

Description: Opaque response correlation identifier.

Example: "req_01".

Note: Field of the JSON error response.

Default: None.

Validation: JSON type only.

## Error Response — HTTP 503

Trigger: Temporary service failure.

Content-Type: application/json.

### error

Type: object.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 503 error response.

Description: Error object with code and message.

Example: {"code": "SERVICE_UNAVAILABLE", "message": "Temporary service failure."}.

Note: Field of the JSON error response.

Default: None.

Validation: JSON type only.

### error.code

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 503 error response when the containing error object or array item is present and non-null.

Description: Public enum: SERVICE_UNAVAILABLE.

Example: "SERVICE_UNAVAILABLE".

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Default: None.

Validation: Membership in the public enum stated in the description.

### error.message

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 503 error response when the containing error object or array item is present and non-null.

Description: Display message.

Example: "Temporary service failure.".

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Default: None.

Validation: JSON type only.

### requestId

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 503 error response.

Description: Opaque response correlation identifier.

Example: "req_01".

Note: Field of the JSON error response.

Default: None.

Validation: JSON type only.

## Notes

This is a proposed contract, not a discovered endpoint. Field definitions in [common wire definitions](common-contract.md) are part of this contract. There are no pagination parameters in this version. All declared errors use the stated JSON envelope.
