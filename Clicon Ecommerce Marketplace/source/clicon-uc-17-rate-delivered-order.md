# UC-17: Rate a Delivered Order

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Rate a Delivered Order

Description:

- Lets the authenticated owner leave one rating and feedback about a delivered order from UC-16's Leave a Rating modal.
- This is an order/service review: the inspected modal has no product selector. It does not alter product ratingAverage/reviewCount in UC-04/UC-05/UC-10, and it does not enable UC-05's product-review tab.
- Eligibility, single-review behavior, contracts, and visibility are project decisions. Editing/deleting reviews and public product reviews are outside this UC.

Primary Actor:

Signed-in Customer whose account owns the delivered order under UC-15.

Preconditions:

- UC-16 detail routes and UC-15 account association are implemented; UC-08 fulfillment is DELIVERED.
- An original-browser guest receipt alone is insufficient. Guest orders are not claimed through matching email or later sign-in.
- UC-02 session, shared envelopes, and existing order IDs apply.

Postconditions:

- Success: Exactly one review is saved for the order and visible to its account owner. Order/payment/fulfillment and product aggregate ratings are unchanged.
- Failure: No new review is published by a rejected request. An uncertain response is reconciled through the current order-review endpoint.
- Publish means saving the order feedback in this experiment; no public feed, email, or moderation workflow is promised.

Main Flow:

1. UC-16 requests the order-review state for the current account-owned order without blocking receipt rendering.
2. When eligible, the customer selects Leave a Rating; the modal opens with an unselected rating and empty feedback.
3. The customer chooses an integer star rating from 1 to 5, enters feedback, and selects PUBLISH REVIEW.
4. The frontend submits the request once; the backend checks current ownership, delivered state, and whether a review exists.
5. On confirmed success, close the modal, show `Review submitted.`, and change the action to View your review.
6. Reopening displays the saved rating/feedback read-only; it does not offer another submission.

Alternative Flow:

A.1 — Not delivered or guest

- For an accessible account order not yet delivered, return canSubmit=false, reason=NOT_DELIVERED. Show `You can review this order after delivery.`
- A guest receipt does not request another account's review data. Leave a Rating is disabled with `Reviews require an order linked to your signed-in account.`

A.2 — Existing review and repeated submission

- GET returns the existing review with reason=ALREADY_REVIEWED. Same normalized rating/feedback submitted again returns HTTP 200 with that review; it creates no duplicate. First creation returns 201.
- Different content for an already reviewed order returns 409 REVIEW_ALREADY_EXISTS. Load the saved review rather than silently editing it.

A.3 — Close the modal

- Escape, outside click, or the supplementary close control closes/discards the local draft when not submitting. Restore focus to the opener. During submission disable repeated submit/close until a result or uncertain-result state is established.

Exception Flow:

E.1 — Authentication, ownership, or eligibility changed

- 401 clears account/review state and returns to Sign In. Unknown/unowned order gives generic 404 ORDER_NOT_FOUND. An undelivered order on submission gives 409 ORDER_NOT_DELIVERED.
- Do not infer ownership from receipt email or fabricate delivered status to permit review.

E.2 — Invalid values

- 400 VALIDATION_ERROR maps errors to rating/feedback; preserve the correctable draft. The frontend cannot use its displayed eligibility in place of the server's current check.

E.3 — Unknown outcome

- Disable further submissions, keep the receipt visible, and read the same review resource. If a review exists, show it as the saved result; if none exists, permit a deliberate retry. Failed reconciliation offers retry-read only; no automatic POST loop.

UI Integration:

- Modal source: `30_Dasboard_Order Detail_Leave a Rating`, node `510:15928`; parent receipt `478:12692`.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=510-15928
- Live design context and screenshot inspected on 2026-09-19. Preserve centered white dialog, overlay, Rating dropdown, Feedback textarea, and orange PUBLISH REVIEW.
- Correct the source's erroneous Billing Address dialog heading to `Leave a Rating`. No initial five-star choice is silently submitted: show `Select a rating` until chosen.
- Close control, focus behavior, eligibility/loading/error states, and read-only review display are project supplements. No frozen dataset or mobile dialog is claimed.
- Rating refers to the whole order. Do not add a hidden selected product or fan one review out across purchased products.

API Endpoint:

`GET /api/v1/account/orders/:orderId/review`

`POST /api/v1/account/orders/:orderId/review`

Request Body:

GET: no body/query. orderId is a UUID. POST accepts exactly:
```json
{
  "rating": 5,
  "feedback": "The order arrived as expected."
}
```
- rating is a JSON integer 1–5; feedback is trimmed text, 1–2000 Unicode code points. Reject unknown keys, body on GET, or any query parameters.
- The session supplies ownership. No productId, accountId, delivered flag, timestamp, or display name is accepted.

Successful Response:

```json
{
  "success": true,
  "message": "Order review retrieved.",
  "data": {
    "canSubmit": true,
    "reason": null,
    "review": null
  }
}
```
- GET HTTP 200: canSubmit boolean; reason is null, NOT_DELIVERED, or ALREADY_REVIEWED. Existing review takes precedence and requires canSubmit=false. Otherwise delivered means canSubmit=true/reason=null; undelivered means false/NOT_DELIVERED.
- review is null or the exact review object below.

```json
{
  "success": true,
  "message": "Review submitted.",
  "data": {
    "review": {
      "id": "bc8eb6ee-dbe7-4d1b-8663-c4dca33180d1",
      "rating": 5,
      "feedback": "The order arrived as expected.",
      "createdAt": "2026-09-19T11:00:00.000Z"
    }
  }
}
```
- POST HTTP 201 first creation or 200 identical repeat. Review keys required: id UUID, rating integer, feedback normalized string, createdAt server ISO UTC. POST always returns the persisted object; repeat does not change its timestamp.
- State and creation checks are coherent under concurrent requests. There is one review per order, including when two tabs submit.

Error Response:

Use the shared error envelope: success=false, statusCode matching HTTP status, code, message, server-generated ISO 8601 UTC timestamp, and actual request pathname without query string. Omit data. Optional errors is only for VALIDATION_ERROR and maps input paths to nonempty arrays of strings. All shown success keys are required; examples illustrate contracts rather than fixed data.

```json
{
  "success": false,
  "statusCode": 409,
  "code": "ORDER_NOT_DELIVERED",
  "message": "You can review this order after delivery.",
  "timestamp": "2026-09-19T10:00:00.000Z",
  "path": "/api/v1/account/orders/b5cf395b-fc08-4c2d-9132-bb01924ba70b/review"
}
```

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | You must sign in to continue. |
| 404 | ORDER_NOT_FOUND | This order is not available. |
| 409 | ORDER_NOT_DELIVERED | You can review this order after delivery. |
| 409 | REVIEW_ALREADY_EXISTS | This order already has a review. |
| 503 | REVIEW_UNAVAILABLE | Order reviews are temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

## Project-Specific Implementation Context

### Backend Implementation Context

Implement review state/create in NestJS with UC-15 ownership and UC-08 fulfillment. Persist one order review and expose it only through its eligible account scope. Resolve repeat creation before rejecting different content; never create duplicate feedback or update product stars. No staff moderation UI, public review endpoint, or guest-claim service is added.

### Frontend UI Context

Implement the modal in React/TypeScript/Tailwind and integrate the existing UC-16 action. Provide labelled rating choices, feedback errors, keyboard/focus behavior, a pending state, and a read-only existing-review view. Do not block the receipt when review state cannot load.

### Frontend Logic and API Context

Load eligibility for the current order/account, clear obsolete modal state on navigation, and guard double submissions. After success replace eligibility with the saved review. A 409 existing-review conflict triggers GET; uncertain network results use the same reconciliation. Account changes clear prior private feedback.

### Validation and Error-Handling Context

Validate numeric rating and trimmed feedback. Enforce ownership and delivery at creation, not only during GET. Network/malformed-response recovery must not claim submission without evidence. No automatic repost, product-aggregate update, payment change, or inventory mutation follows a review.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
