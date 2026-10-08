---
artifact_type: api-contract
status: Frozen
api_id: API-ORDER-CREATE
related_uc_id: UC-08
---

# API-ORDER-CREATE: Submit cash-on-delivery order.

## General Information

### API ID

API-ORDER-CREATE

### API Name

Submit cash-on-delivery order.

### Related Use Case IDs

- UC-08 — [specification](../uc/uc-08-place-cash-on-delivery-order.md)

### Method

POST

### Path

/v1/me/orders

### Description

Submit cash-on-delivery order for the web client. Request and response objects are defined in [common wire definitions](common-contract.md).

### Authentication

Cookie named euphoria_session.

### Authorization

Access outcomes are represented by HTTP 401 and HTTP 403.

## Request Header(s)

### headers.Accept

Type: string.; Format: HTTP media type; Required: Yes.; Nullable: No.

Trigger: Every POST request to this endpoint.

Description: Response media type.

Example: "application/json".

Note: Identifies the requested response media type.

Default: None.

Validation: HTTP media type syntax; allowed value application/json.

### headers.Content-Type

Type: string.; Format: HTTP media type; Required: Yes.; Nullable: No.

Trigger: Every POST request to this endpoint.

Description: Request media type.

Example: "application/json".

Note: Identifies the media type of the submitted request body.

Default: None.

Validation: HTTP media type syntax; allowed value application/json.

### headers.Cookie

Type: string.; Format: HTTP Cookie; Required: Yes.; Nullable: No.

Trigger: Every POST request to this endpoint.

Description: HTTP cookie encoding; euphoria_session carries an opaque value.

Example: "euphoria_session=opaque-session-value".

Note: Carries semicolon-separated HTTP cookie pairs.

Default: None.

Validation: HTTP Cookie header encoding.

### headers.X-CSRF-Token

Type: string.; Format: Opaque HTTP header value; Required: Yes.; Nullable: No.

Trigger: Every POST request to this endpoint.

Description: Opaque request header value.

Example: "opaque-csrf-value".

Note: Transmit the opaque token as a single header value.

Default: None.

Validation: JSON type only.

### headers.Idempotency-Key

Type: string.; Format: Opaque HTTP header value; Required: Yes.; Nullable: No.

Trigger: Every POST request to this endpoint.

Description: Opaque request key.

Example: "request_01".

Note: Transmit the command reference as a single header value.

Default: None.

Validation: JSON type only.

## Path Parameter(s)

None.

## Query Parameter(s)

None.

## Request Body

### body

Type: CheckoutSubmission.; Required: Yes.; Nullable: No.

Trigger: Every request body sent to this endpoint.

Description: JSON object; full CheckoutSubmission field definitions are in common-contract.md.

Example: {"checkout": {"cartVersion": 1, "billing": {"firstName": "Alex", "lastName": "Lee", "country": "US", "company": null, "street": "10 Sample Street", "unit": null, "city": "Sample City", "state": "CA", "postalCode": "90001", "phone": "+12025550123", "instructions": null}, "shipping": null, "sameAsBilling": true}, "displayedTotal": {"amount": "34.00", "currency": "USD"}, "paymentMethod": "COD"}.

~~~json
{
  "checkout": {
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
  },
  "displayedTotal": {
    "amount": "34.00",
    "currency": "USD"
  },
  "paymentMethod": "COD"
}
~~~

Default: None.

Validation: Object or array shape defined in common-contract.md.

## Success Response — HTTP 200

Content-Type: application/json.

### data

Type: Confirmation.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 200 success response.

Description: Confirmation object; all nested fields are defined in common-contract.md.

Example: {"orderId": "ord_01", "message": "Your Order is Confirmed"}.

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
    "orderId": "ord_01",
    "message": "Your Order is Confirmed"
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

## Error Response — HTTP 409

Trigger: Operation conflict.

Content-Type: application/json.

### error

Type: object.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 409 error response.

Description: Error object with code and message.

Example: {"code": "OPERATION_CONFLICT", "message": "Operation conflict."}.

Note: Field of the JSON error response.

Default: None.

Validation: JSON type only.

### error.code

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 409 error response when the containing error object or array item is present and non-null.

Description: Public enum: OPERATION_CONFLICT.

Example: "OPERATION_CONFLICT".

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Default: None.

Validation: Membership in the public enum stated in the description.

### error.message

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 409 error response when the containing error object or array item is present and non-null.

Description: Display message.

Example: "Operation conflict.".

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Default: None.

Validation: JSON type only.

### requestId

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 409 error response.

Description: Opaque response correlation identifier.

Example: "req_01".

Note: Field of the JSON error response.

Default: None.

Validation: JSON type only.

## Error Response — HTTP 422

Trigger: Operation rejected.

Content-Type: application/json.

### error

Type: object.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 422 error response.

Description: Error object with code and message.

Example: {"code": "REQUEST_REJECTED", "message": "Operation rejected."}.

Note: Field of the JSON error response.

Default: None.

Validation: JSON type only.

### error.code

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 422 error response when the containing error object or array item is present and non-null.

Description: Public enum: REQUEST_REJECTED.

Example: "REQUEST_REJECTED".

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Default: None.

Validation: Membership in the public enum stated in the description.

### error.message

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 422 error response when the containing error object or array item is present and non-null.

Description: Display message.

Example: "Operation rejected.".

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Default: None.

Validation: JSON type only.

### requestId

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 422 error response.

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
