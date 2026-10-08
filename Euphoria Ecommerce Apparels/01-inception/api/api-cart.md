---
artifact_type: api-contract
status: Frozen
api_id: API-CART
related_uc_ids: ["UC-06", "UC-07", "UC-08"]
---

# API-CART: Read cart.

## General Information

### API ID

API-CART

### API Name

Read cart.

### Related Use Case IDs

- UC-06 — [specification](../uc/uc-06-review-cart.md)
- UC-07 — [specification](../uc/uc-07-review-checkout.md)
- UC-08 — [specification](../uc/uc-08-place-cash-on-delivery-order.md)

### Method

GET

### Path

/v1/me/cart

### Description

Read cart for the web client. Request and response objects are defined in [common wire definitions](common-contract.md).

### Authentication

Cookie named euphoria_session.

### Authorization

Access outcomes are represented by HTTP 401 and HTTP 403.

## Request Header(s)

### headers.Accept

Type: string.; Format: HTTP media type; Required: Yes.; Nullable: No.

Trigger: Every GET request to this endpoint.

Description: Response media type.

Example: "application/json".

Note: Identifies the requested response media type.

Default: None.

Validation: HTTP media type syntax; allowed value application/json.

### headers.Cookie

Type: string.; Format: HTTP Cookie; Required: Yes.; Nullable: No.

Trigger: Every GET request to this endpoint.

Description: HTTP cookie encoding; euphoria_session carries an opaque value.

Example: "euphoria_session=opaque-session-value".

Note: Carries semicolon-separated HTTP cookie pairs.

Default: None.

Validation: HTTP Cookie header encoding.

## Path Parameter(s)

None.

## Query Parameter(s)

None.

## Request Body

None.

## Success Response — HTTP 200

Content-Type: application/json.

### data

Type: Cart.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 200 success response.

Description: Cart object; all nested fields are defined in common-contract.md.

Example: {"id": "cart_01", "version": 1, "items": [{"id": "cl_01", "variantId": "var_01", "title": "Printed shirt", "imageUrl": "https://example.com/shirt.jpg", "color": "Black", "size": "M", "quantity": 1, "unitPrice": {"amount": "29.00", "currency": "USD"}, "lineTotal": {"amount": "29.00", "currency": "USD"}}], "subtotal": {"amount": "29.00", "currency": "USD"}, "shippingEstimate": {"amount": "5.00", "currency": "USD"}, "totalEstimate": {"amount": "34.00", "currency": "USD"}}.

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
    "id": "cart_01",
    "version": 1,
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
    "shippingEstimate": {
      "amount": "5.00",
      "currency": "USD"
    },
    "totalEstimate": {
      "amount": "34.00",
      "currency": "USD"
    }
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

## Error Response — HTTP 401

Trigger: Rejected authentication context.

Content-Type: application/json.

### error

Type: object.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 401 error response.

Description: Error object with code and message.

Example: {"code": "AUTHENTICATION_REJECTED", "message": "Rejected authentication context."}.

Note: Field of the JSON error response.

Default: None.

Validation: JSON type only.

### error.code

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 401 error response when the containing error object or array item is present and non-null.

Description: Public enum: AUTHENTICATION_REJECTED.

Example: "AUTHENTICATION_REJECTED".

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Default: None.

Validation: Membership in the public enum stated in the description.

### error.message

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 401 error response when the containing error object or array item is present and non-null.

Description: Display message.

Example: "Rejected authentication context.".

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Default: None.

Validation: JSON type only.

### requestId

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 401 error response.

Description: Opaque response correlation identifier.

Example: "req_01".

Note: Field of the JSON error response.

Default: None.

Validation: JSON type only.

## Error Response — HTTP 403

Trigger: Rejected access context.

Content-Type: application/json.

### error

Type: object.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 403 error response.

Description: Error object with code and message.

Example: {"code": "ACCESS_REJECTED", "message": "Rejected access context."}.

Note: Field of the JSON error response.

Default: None.

Validation: JSON type only.

### error.code

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 403 error response when the containing error object or array item is present and non-null.

Description: Public enum: ACCESS_REJECTED.

Example: "ACCESS_REJECTED".

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Default: None.

Validation: Membership in the public enum stated in the description.

### error.message

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 403 error response when the containing error object or array item is present and non-null.

Description: Display message.

Example: "Rejected access context.".

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Default: None.

Validation: JSON type only.

### requestId

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 403 error response.

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
