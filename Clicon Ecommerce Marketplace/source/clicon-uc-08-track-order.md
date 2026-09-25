# UC-08: Track Order

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Track Order

Description:

- Allows a visitor or customer to look up a previously placed order using its displayed order number and checkout billing email, then view fulfillment progress and recorded activity.
- Continues UC-07 using the persisted order and its original browser context. Includes the tracking form and read-only tracking result.
- Lookup eligibility, fulfillment states, API contracts, and recovery behavior below are project decisions. Figma establishes the inspected desktop form, summary, progress indicator, and activity list.
- This UC does not change an order, collect payment, contact a carrier, generate shipment events, send email, or implement order history, cancellation, returns, or full order details.

Primary Actor:

Visitor or signed-in Customer in the browser context that placed the order.

Preconditions:

- UC-07 has persisted an order with its order number, placedAt, contact email, purchased item snapshots, total, and originating browser context.
- `/track-order` and `/track-order/details` are registered routes with direct navigation/reload support.
- Login is not required. As in UC-07, account login and a supplied identifier alone do not establish access to another browser's order.
- Shared success/error envelopes and integer USD-cent monetary units apply.

Postconditions:

- Success: The visitor sees the matching order's saved amount, purchased item count, placement time, fulfillment stage, available delivery estimate, and recorded events.
- Failure: No matching order details are displayed; the user receives the documented validation, lookup, or service feedback.
- Lookup and refresh do not modify cart contents, inventory, fulfillment, payment status, or order status.

Main Flow:

1. The visitor selects `Track Order` in the shared header/footer and opens `/track-order`.
2. The form asks for Order ID and Billing Email. Order ID means the display `orderNumber` from UC-07, not its internal UUID or quote ID.
3. The visitor enters the order number and the contact email used at checkout, then selects `TRACK ORDER`.
4. The frontend validates the fields and submits `POST /api/v1/orders/track`.
5. The backend resolves the order within the originating browser context and matches the normalized billing email to the order's saved contact email.
6. The backend returns the order summary and coherent fulfillment snapshot using HTTP 200 and the shared success envelope.
7. The frontend displays `/track-order/details` with the order summary, progress indicator, arrival information, and newest-first activity list.
8. The visitor may refresh the result or return to the lookup form to track another order.

Alternative Flow:

A.1 — Newly placed order

- An order created through UC-07 begins with fulfillmentStatus `ORDER_PLACED` and a placement event at the order's placedAt timestamp.
- Until fulfillment information is supplied, expectedDeliveryDate is null and there are no packaging, transit, or delivery events. Display `Estimated arrival is not available yet.`
- Do not advance stages based on elapsed time or copy the Figma sample history into a real order.

A.2 — Refresh progress

- A project-supplied `Refresh tracking` action repeats the lookup using the current in-memory form values.
- The result reflects the latest stored fulfillment snapshot. There is no automatic polling or carrier integration in this UC.
- During refresh, retain the visible snapshot with `Refreshing tracking...`. A failed refresh labels it `Could not refresh. Showing the previous result.` rather than implying it is current.

A.3 — Return to the form or reload

- `Track another order` returns to `/track-order`, clears the previous result, and allows new input.
- Lookup values and results are held only for the current page session in memory. Direct navigation or a full reload of `/track-order/details` without that state returns to the lookup form with `Enter your order number and billing email to view tracking.`
- The URL contains neither the billing email nor order identifiers. Browser Back restores the form when in-memory state exists; it does not create an order or mutate tracking.

A.4 — Delivery completed or estimate missing

- DELIVERED displays all four milestones completed and `Delivered on <deliveredAt>` instead of a future expected-arrival message.
- For an undelivered order, a non-null estimate is displayed as an estimate, not a guarantee. If its date has passed, display `The estimated arrival date has passed. Check the latest tracking activity.`
- Missing estimates do not make an otherwise available order a lookup failure.

Exception Flow:

E.1 — Invalid input

- Missing, malformed, or overlength input returns HTTP 400 `VALIDATION_ERROR`. Show field feedback without submitting another lookup until corrected.

E.2 — No accessible matching order

- Unknown order number, mismatched billing email, missing originating browser context, and a different browser's order all return HTTP 404 `ORDER_NOT_FOUND` with the same message.
- Clear any previous result for a newly submitted lookup. Do not identify which input matched or expose a different order as a fallback.
- Clearing browser identification data or switching browser may prevent lookup under this experiment's access model. Offer `/shop` and allow the user to correct the lookup fields; do not promise cross-device recovery.

E.3 — Order data unavailable

- A temporary order/tracking service failure returns HTTP 503 `TRACKING_UNAVAILABLE`. An unexpected failure returns HTTP 500 `INTERNAL_ERROR`.
- Show a manual retry. A failure is not an empty activity list or proof that the order was not placed.

E.4 — Inconsistent fulfillment data

- A current stage that contradicts completed milestones, an invalid chronology, or a missing required placement event is invalid source data.
- Return HTTP 503 `TRACKING_UNAVAILABLE` rather than displaying contradictory progress or inventing missing events.
- The frontend also rejects malformed response data with `Unable to load tracking information. Please try again.`

UI Integration:

- Lookup frame: `09_Track Order`, node `418:10475`, desktop 1920 × 1264; inspected content node `418:11087`.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=418-10475
- Result frame: `10_Track Order_Details`, node `418:11361`, desktop 1920 × 1704; inspected content node `493:14233`.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=418-11361
- Live page metadata and design context/rendered screenshots of both content nodes were inspected on 2026-09-18. This establishes the desktop content; it does not establish a frozen dataset, responsive layouts, or unseen loading/error states.

| Observed element | Integration |
| --- | --- |
| Track Order title and introduction | Lookup form heading and corrected instructions |
| Order ID input; ID... placeholder | `orderNumber` from UC-07 |
| Billing Email; Email address placeholder | `billingEmail` matched to saved checkout contact |
| Information hint beneath Order ID | Explain where to find the checkout order number |
| TRACK ORDER button | Submit the lookup |
| Highlighted order summary | Order number, saved quantity count, placement time, and order total |
| Order expected arrival | Available estimate or documented fallback |
| Order Placed / Packaging / On The Road / Delivered | Four fulfillment milestones |
| Order Activity list | Recorded events, newest first, with date/time and corresponding icon |

- Reuse the shared Clicon shell, breadcrumbs, Public Sans, orange action/progress (#FA8232), blue amount (#2DA5F3), light borders (#E4E7E9), pale-yellow summary (#FDFAE7), and green completed-state accents (#2DB224).
- Preserve the two-column lookup inputs and centered tracking card. `Refresh tracking`, `Track another order`, and error/loading feedback are project supplements, not observed source controls.
- Replace the source's claim that an email was sent with `Enter the order number shown on your checkout confirmation and the email used at checkout.` UC-07 does not send confirmation email.
- Use the source label Order ID but clarify `Use the order number from your confirmation, for example CL-00001234.` Do not impose that example's format on every stored order number.
- The source shows Packaging progress alongside a delivered event, and includes an invalid time of 2:61 PM. Render coherent stored data and valid timestamps rather than those sample mismatches.
- Display `itemCount` as `N items`, meaning the sum of ordered quantities, not distinct products. Total is the saved final UC-07 order total, including checkout shipping; do not reprice from the current catalog.
- In the four-step indicator, earlier stages are complete, the current nonterminal stage is active, and later stages are pending. DELIVERED makes all stages complete. Expose text labels as well as colors/icons.
- UC-07's `View Order` remains owned by the future full order-details UC. This tracking implementation does not silently replace that action. The implemented shared `Track Order` links provide access to `/track-order`.

API Endpoint:

`POST /api/v1/orders/track`

This is a read-only lookup despite using POST; submitting it creates no order or tracking event.

Request Body:

```json
{
  "orderNumber": "CL-00001234",
  "billingEmail": "customer@example.com"
}
```

- Both keys are required strings. Reject unknown fields and all query parameters.
- orderNumber: trim surrounding whitespace, require 1–100 Unicode code points, reject control characters, then compare exactly with the stored display order number. Case is preserved; do not infer an internal UUID or remove an entered prefix.
- billingEmail: trim surrounding whitespace, lowercase, require valid email format and maximum 254 characters. Compare with the contact email snapshot from checkout, not a current account email.
- No account ID, cart ID, quote ID, order UUID, or fulfillment status is accepted as lookup input. Browser context is resolved through the existing project integration.
- Order writers must keep display order numbers within this input contract. This refines UC-07's nonempty display-string contract without requiring its illustrative CL prefix.

Successful Response:

HTTP 200:

```json
{
  "success": true,
  "message": "Order tracking retrieved.",
  "data": {
    "tracking": {
      "orderNumber": "CL-00001234",
      "orderStatus": "PLACED",
      "placedAt": "2026-09-18T10:03:00.000Z",
      "itemCount": 2,
      "currency": "USD",
      "total": 340300,
      "fulfillmentStatus": "PACKAGING",
      "expectedDeliveryDate": "2026-09-22",
      "deliveryTimeZone": "America/Los_Angeles",
      "deliveredAt": null,
      "events": [
        {
          "id": "39a414e5-b445-49fb-aedc-d39d0d163268",
          "sequence": 2,
          "stage": "PACKAGING",
          "occurredAt": "2026-09-18T11:00:00.000Z",
          "message": "Your order is being prepared for shipment."
        },
        {
          "id": "c9de7d57-8c69-4f16-8071-549871331ac0",
          "sequence": 1,
          "stage": "ORDER_PLACED",
          "occurredAt": "2026-09-18T10:03:00.000Z",
          "message": "Your order has been placed."
        }
      ]
    }
  }
}
```

- All shown keys are required. Examples illustrate the schema; fulfillment values must come from coherent stored data.
- orderStatus stays `PLACED` for the UC-07 order lifecycle covered here. fulfillmentStatus is a separate enum: ORDER_PLACED, PACKAGING, ON_THE_ROAD, DELIVERED. Tracking does not redefine UC-07's order status or infer a payment-status change from delivery.
- itemCount is a positive integer equal to the sum of quantities in the immutable purchased-item snapshot. total is the saved nonnegative integer USD-cent total; it is unrelated to the current cart, which may be empty or contain new items.
- placedAt and event occurredAt are ISO 8601 UTC timestamps. expectedDeliveryDate is a valid YYYY-MM-DD date or null; it is a delivery-local calendar date, not midnight UTC.
- deliveryTimeZone is `America/Los_Angeles` for UC-07's California fixture. Display event/placement timestamps in this zone and label the timezone. Determine whether an estimate has passed using the same zone.
- deliveredAt is null except for DELIVERED, when it equals the first recorded DELIVERED event time. Do not derive it from the estimated date.
- events is a nonempty array, ordered by descending sequence. Each event has a unique UUID id, a positive integer sequence unique within the order, one of the four stage values, a valid occurredAt, and a nonempty plain-text message of at most 500 Unicode code points.
- The earliest event has sequence 1, stage ORDER_PLACED, and occurredAt equal to placedAt. Later sequences have nondecreasing times. Stages advance through the declared order without skipping or moving backward; multiple events may describe the same stage. The highest-sequence event's stage equals fulfillmentStatus.
- Activity messages come from the fulfillment record, not from a fabricated carrier feed. The API returns the complete recorded list for this experiment; there is no omitted-page or implicit pagination contract.
- Response scope is tracking summary only. Billing email, contact details, addresses, internal order/cart identifiers, and item-level purchase details are not part of this response.

Error Response:

Use the shared envelope; errors contain no `data`. timestamp is server-generated ISO 8601 UTC; path is `/api/v1/orders/track`.

```json
{
  "success": false,
  "statusCode": 404,
  "code": "ORDER_NOT_FOUND",
  "message": "No matching order is available. Check your order number and billing email in the browser used at checkout.",
  "timestamp": "2026-09-18T12:00:00.000Z",
  "path": "/api/v1/orders/track"
}
```

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-18T12:00:00.000Z",
  "path": "/api/v1/orders/track",
  "errors": {"billingEmail": ["Enter a valid billing email address."]}
}
```

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | `Please correct the highlighted fields.` |
| 404 | ORDER_NOT_FOUND | `No matching order is available. Check your order number and billing email in the browser used at checkout.` |
| 503 | TRACKING_UNAVAILABLE | `Order tracking is temporarily unavailable. Please try again later.` |
| 500 | INTERNAL_ERROR | `Unable to complete your request. Please try again later.` |

- Optional errors appears only for VALIDATION_ERROR and maps request field names to nonempty arrays of messages. Body-level validation may omit it.
- No-match conditions use the same status/code/message. A service failure or corrupt fulfillment record must not be disguised as a no-match response.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement the tracking lookup in NestJS using UC-07's persisted order and originating browser context.

- Reuse orderNumber, contact email snapshot, placedAt, purchased quantities, and final order total. Do not look up these values from a mutable account profile, current product price, or current cart.
- Make each newly placed UC-07 order trackable with an ORDER_PLACED fulfillment record and placement event. Previously created experiment orders without fulfillment data require a one-time initialization from their persisted placement record, not fabrication on each lookup.
- Maintain fulfillmentStatus, optional delivery estimate, deliveredAt, and ordered activity records separately from the order/payment state. The lookup reads them without mutation.
- Fulfillment beyond placement is supplied by coherent experiment seed data or a future fulfillment integration. This UC creates no public status-update API, administrative page, carrier connection, or timer that automatically delivers orders.
- Preserve access to tracking in the originating browser context for at least the seven-day period defined by UC-07, independently of cart clearing and account-session expiry. Do not require the cart to still contain purchased items.
- Match both the accessible order and normalized checkout email before returning its limited summary. Do not broaden this UC into cross-browser recovery or account order history.
- Return a coherent summary/event snapshot. Invalid fulfillment chronology or stage disagreement follows TRACKING_UNAVAILABLE rather than constructing a plausible but unsupported timeline.

### Frontend UI Context

Build `TrackOrderPage` and `TrackOrderDetailsPage` in React, TypeScript, and Tailwind CSS using the inspected content and shared shell.

- Connect existing header/footer Track Order links to `/track-order`. Register `/track-order/details` with the declared state-free recovery behavior.
- Implement the two labeled inputs, information hint, orange submit action, pale-yellow summary, four milestones, and vertically stacked activity rows.
- Use the observed milestone icons and activity styling, with actual stage-driven progress. Do not use a static progress image that permanently depicts Packaging for every order.
- Correct source text that claims a confirmation email was sent. Keep order-number guidance consistent with UC-07's on-screen confirmation.
- Render messages as text. Format USD cents and dates consistently; keep the expected date separate from timestamp conversion. Explain missing estimates and stale refresh results visibly.
- Loading, inline validation, no-match feedback, refresh, and track-another actions are project supplements. Responsive layouts remain implementation adaptations, not verified mobile frames.

### Frontend Logic and API Context

- State contains orderNumber, billingEmail, current tracking result, submitted lookup values, loading/refresh status, and feedback. Keep the form input values separate from the lookup associated with a displayed result.
- Submit only after local field validation; read `data.tracking` after a successful response. Navigate to the result route only when a valid result exists.
- For a different submitted lookup, clear the previous result before displaying its loading/error state. For refresh of the same lookup, retain and label the previous snapshot until replacement succeeds.
- Ignore responses for obsolete lookups or unmounted pages. An earlier response must not replace the result of a later submission.
- Derive completed/current/pending milestones from fulfillmentStatus; render events in returned descending-sequence order. Do not change milestones based solely on their expected delivery date.
- A full reload without lookup state returns to the form. Do not put billing email into route parameters or query strings, and do not automatically place/recreate an order as a lookup recovery action.

### Validation and Error-Handling Context

- Apply the exact order-number and email contracts on both frontend and backend. Use the server result for lookup eligibility; a logged-in account does not bypass the originating-browser requirement.
- Preserve form values after explicit validation/no-match feedback so they can be corrected. Do not reveal which field matched an inaccessible order.
- Check response types, monetary units, stage membership, and required timestamps before displaying a result. Null delivery estimates are supported; missing required data is not.
- Distinguish no-match, unavailable service, invalid fulfillment data, and failed refresh. Do not replace a network/service failure with empty activity or a delivered state.
- For no HTTP response, show `Unable to connect. Please check your connection and try again.` Retry is a read-only lookup; it must not alter fulfillment or order data.
- Tracking cannot clear the cart, decrement inventory again, mark COD paid, or activate cancellation/refund behavior. Those actions are outside this read-only UC.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
