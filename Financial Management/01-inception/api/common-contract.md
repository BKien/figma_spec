# Common Wire Contract

## Representation

All endpoint documents describe HTTPS JSON requests and responses. `Content-Type` is `application/json` for bodies. Bearer authentication uses `Authorization: Bearer <access-token>`. The `Credit Card` public enum maps to local UML `AccountType::Credit_Card`; all other public enum values retain the spelling shown in each contract.

Integer identifiers use JSON integer values in bodies/responses and complete base-10 integer text in path parameters. Query integer values must match complete decimal text; savings `year` uses four decimal digits. Values such as `2025abc`, fractional integer text, and malformed date/month text receive HTTP 400. Unknown JSON body properties receive HTTP 400. JSON `number` money values use finite decimal notation; decimal values are decoded without binary floating point conversion. Domain precision and bounds are specified in use cases.

Calendar dates use YYYY-MM-DD; calendar months use YYYY-MM; timestamps use RFC 3339 UTC representations. Optional nullable fields may be omitted or explicitly null; absent optional non-null fields use their documented default. Optional `branch_name` omission maps to null in both create and replacement update. Child properties under nullable objects apply only when the object is non-null. Arrays contain the element shape specified by their `[]` field definitions.

## Success Shapes

Every successful operation returns `success` (boolean), `message` (string) and `data` (object or array as specified by the endpoint). Transaction-list `total` (integer) and `hasMore` (boolean) are additional envelope properties. Payload property names retain supplied source spelling, including the source's mixture of snake_case and camelCase. Legacy bare success objects are wrapped in `data`; `account` and `updated_goal` wrappers are flattened into that payload. This is a deliberate compatibility change.

## Error Shape

Every listed error returns `success: false`, a string `message`, and `error: { code: string }`. There is no success `data` payload in an error response. Error codes and public HTTP outcomes are enumerated in each endpoint. Error messages are examples, not stable decision identifiers.

## Version Fields

`expected_version` is a required integer in transaction-create, account-update and goal-update bodies. Account delete carries required `If-Match` with a quoted integer version, such as `"1"`. Account detail returns an `ETag` header with the same quoted version representation. Account projections and goal projections expose `version` integers. Version conflict is represented by HTTP 409 `OPERATION_CONFLICT`.

## Session Representation

Auth responses return `data.accessToken` and `data.user` with `id`, `fullName` and `email`. Requests after authentication use the bearer token header. No refresh, logout, password recovery, OAuth or persistent-session endpoint is supplied in this package.

## Contract Boundary

Transport definitions do not restate domain predicates. The individual use cases contain business policy, and the package review explains changes to the supplied contracts. No backend implementation or compatibility migration has been executed.
