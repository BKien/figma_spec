---
artifact_type: api-contract
status: Frozen
api_id: API-RESET-REQUEST
related_uc_ids: ["UC-09", "UC-10"]
---

# API-RESET-REQUEST: Request reset email.

## General Information

### API ID

API-RESET-REQUEST

### API Name

Request reset email.

### Related Use Case IDs

- UC-09 — [specification](../uc/uc-09-request-password-reset.md)
- UC-10 — [specification](../uc/uc-10-resend-password-reset-email.md)

### Method

POST

### Path

/v1/password-reset-requests

### Description

Request reset email for the web client. Request and response objects are defined in [common wire definitions](common-contract.md).

### Authentication

None.

### Authorization

Public operation.

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

## Path Parameter(s)

None.

## Query Parameter(s)

None.

## Request Body

### body

Type: ResetEmail.; Required: Yes.; Nullable: No.

Trigger: Every request body sent to this endpoint.

Description: JSON object; full ResetEmail field definitions are in common-contract.md.

Example: {"email": "alex@example.com"}.

~~~json
{
  "email": "alex@example.com"
}
~~~

Default: None.

Validation: Object or array shape defined in common-contract.md.

## Success Response — HTTP 202

Content-Type: application/json.

### data

Type: Accepted.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 202 success response.

Description: Accepted object; all nested fields are defined in common-contract.md.

Example: {"accepted": true}.

Default: None.

Validation: Object or array shape defined in common-contract.md.

### requestId

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 202 success response.

Description: Opaque response correlation identifier.

Example: "req_01".

~~~json
{
  "data": {
    "accepted": true
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

## Error Response — HTTP 429

Trigger: Request temporarily limited.

Content-Type: application/json.

### error

Type: object.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 429 error response.

Description: Error object with code and message.

Example: {"code": "REQUEST_LIMITED", "message": "Request temporarily limited."}.

Note: Field of the JSON error response.

Default: None.

Validation: JSON type only.

### error.code

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 429 error response when the containing error object or array item is present and non-null.

Description: Public enum: REQUEST_LIMITED.

Example: "REQUEST_LIMITED".

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Default: None.

Validation: Membership in the public enum stated in the description.

### error.message

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 429 error response when the containing error object or array item is present and non-null.

Description: Display message.

Example: "Request temporarily limited.".

Note: Field of the JSON error response; nested requiredness applies when its containing object or array item is present.

Default: None.

Validation: JSON type only.

### requestId

Type: string.; Required: Yes.; Nullable: No.

Trigger: Included in the HTTP 429 error response.

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
