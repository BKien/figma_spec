---
artifact_type: api-contract
status: Frozen
api_id: API-CATALOG
related_uc_ids: ["UC-01", "UC-02", "UC-03", "UC-04"]
---

# API-CATALOG: Read product listing.

## General Information

### API ID

API-CATALOG

### API Name

Read product listing.

### Related Use Case IDs

- UC-01 — [specification](../uc/uc-01-explore-storefront.md)
- UC-02 — [specification](../uc/uc-02-browse-products.md)
- UC-03 — [specification](../uc/uc-03-filter-products.md)
- UC-04 — [specification](../uc/uc-04-sort-products.md)

### Method

GET

### Path

/v1/products

### Description

Read product listing for the web client. Request and response objects are defined in [common wire definitions](common-contract.md).

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

None.

## Query Parameter(s)

### query.categoryId

Type: string.; Required: No.; Nullable: Yes.

Trigger: When the client supplies the categoryId query parameter.

Description: Category selection value.

Example: null.

Default: None.

Validation: JSON type only.

### query.colors

Type: string[].; Required: No.; Nullable: No.

Trigger: When the client supplies the colors query parameter.

Description: Repeated query parameter, for example colors=black&colors=blue.

Example: [].

Default: None.

Validation: JSON type only.

### query.sizes

Type: string[].; Required: No.; Nullable: No.

Trigger: When the client supplies the sizes query parameter.

Description: Repeated query parameter, for example sizes=M&sizes=L.

Example: [].

Default: None.

Validation: JSON type only.

### query.styles

Type: string[].; Required: No.; Nullable: No.

Trigger: When the client supplies the styles query parameter.

Description: Repeated query parameter, for example styles=Casual.

Example: [].

Default: None.

Validation: JSON type only.

### query.minAmount

Type: string.; Required: No.; Nullable: No.

Trigger: When the client supplies the minAmount query parameter.

Description: Decimal text value.

Example: "0.00".

Default: None.

Validation: Decimal string syntax: ^-?[0-9]+(?:\.[0-9]+)?$.

### query.maxAmount

Type: string.; Required: No.; Nullable: Yes.

Trigger: When the client supplies the maxAmount query parameter.

Description: Decimal text value or omitted.

Example: null.

Default: None.

Validation: Decimal string syntax: ^-?[0-9]+(?:\.[0-9]+)?$.

### query.sort

Type: string.; Required: No.; Nullable: No.

Trigger: When the client supplies the sort query parameter.

Description: Public enum: NEW, RECOMMENDED.

Example: "RECOMMENDED".

Default: None.

Validation: Membership in the public enum stated in the description.

## Request Body

None.

## Success Response — HTTP 200

Content-Type: application/json.

### data

Type: CatalogResult.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 200 success response.

Description: CatalogResult object; all nested fields are defined in common-contract.md.

Example: {"items": [{"id": "prd_01", "title": "Printed shirt", "brand": "Euphoria", "imageUrl": "https://example.com/shirt.jpg", "price": {"amount": "29.00", "currency": "USD"}}], "categories": [], "colors": [], "sizes": [], "styles": [], "total": 1}.

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
