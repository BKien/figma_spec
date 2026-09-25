# UC-15: View Account Order History

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

View Account Order History

Description:

- Allows an authenticated customer to view a paginated summary of orders explicitly associated with their account, including order number, fulfillment summary, placement date, final total, and purchased quantity.
- Includes the account-order association needed to populate this page from future UC-07 checkouts. That association is an explicit integration extension; it was not previously implemented or implied by UC-07's browser-owned confirmation contract.
- Ownership, status mapping, pagination, and API contracts are project decisions. Figma establishes the inspected desktop table, sidebar, and pagination controls.
- Full order details, cancellation, refunds, payment collection, order search, and order-history import are outside this UC. View Details remains an integration point for its owning UC.

Primary Actor:

Signed-in Customer with an active, verified account.

Preconditions:

- UC-02 provides an authenticated browser session. `/account/orders` supports direct navigation and reload.
- UC-07 persists order snapshots; UC-08 defines fulfillmentStatus separately from the order's PLACED status.
- New checkout quotes/orders follow the account association extension below. Existing orders without an explicit account association remain unassociated.
- The shared success/error envelope and integer USD-cent monetary units apply.

Postconditions:

- Success: The customer sees only orders explicitly associated with their current account, sorted newest first, with accurate totals and quantities from saved order snapshots.
- Failure: No other account's order data is displayed. Authentication/service failure is not represented as a successful empty history.
- Reading history changes no order, inventory, cart, payment, profile, or fulfillment state.

Main Flow:

1. The customer selects Order History in the account sidebar or the new Order History link in the existing dashboard shell.
2. The frontend resolves the current session, then requests page 1 from `GET /api/v1/account/orders`.
3. The backend derives the account from the session and selects only orders whose saved account association matches it.
4. The API returns HTTP 200 with the requested order summaries and pagination metadata.
5. The frontend displays Order ID, Status, Date, Total, and Action columns using the returned records.
6. The customer selects a numbered page or previous/next control; the frontend replaces the table with that page's result.
7. The customer may return to the dashboard or another implemented account/shop destination. Full View Details navigation becomes available only when its owning UC is integrated.

Alternative Flow:

A.1 — No account orders

- Return HTTP 200 with an empty items array and totalItems/totalPages equal to 0.
- Display `You have no orders linked to this account yet.` with `Browse products` linking to `/shop`.
- Guest orders and old orders lacking an explicit account association are not inferred from matching contact email, profile name, saved address, or current browser contents.

A.2 — Account association for new checkout orders

- When UC-07 creates a new quote, record the current authenticated account ID internally, or null when checkout is genuinely unauthenticated. Never accept this identity from the request body.
- Before first placement of an account-bound quote, the same account must still have a valid active/verified session. A guest-bound quote is placed only while the checkout remains unauthenticated.
- If the quote was account-bound but its session has expired/ended, reject placement with 401 UNAUTHENTICATED; the customer may sign in and review checkout again. Do not silently convert it to a guest order.
- If a different valid account is now signed in, or a guest-bound quote now has an authenticated account, return 409 CHECKOUT_ACCOUNT_CHANGED. Preserve the form, resolve the current session, obtain a new quote, and require another explicit PLACE ORDER click.
- At successful first placement, copy the quote's account association to the order as part of the existing order/inventory/cart outcome. Guest orders keep null association.
- If session status cannot be determined because its service failed, fail the quote/placement with CHECKOUT_UNAVAILABLE; do not assume a guest or another account.

A.3 — Existing orders and repeated placement

- An already placed quote returns the existing order according to UC-07's original-browser eligibility and repeat-response behavior before checking the current login association. A retry never reassigns ownership, creates a second order, or clears a newer cart.
- Guest orders are not claimed later by signing in. Existing experiment orders without recorded ownership remain absent from account history; do not backfill ownership through email matching.
- Account history can be read from another browser after signing into the same account. This does not relax UC-07's original-browser confirmation lookup or UC-08's browser-plus-email tracking contract.
- Browser cart/wishlist/comparison remain browser-scoped. Attaching an order to an account does not migrate these collections.

A.4 — Fulfillment summary

- ORDER_PLACED, PACKAGING, and ON_THE_ROAD map to display status IN_PROGRESS; DELIVERED maps to COMPLETED.
- These are history presentation states, not replacements for UC-07's orderStatus PLACED. COMPLETED means delivered for this table; it does not mean a Cash on Delivery payment was recorded as paid.
- Existing UC-08 placement/fulfillment records are the source of truth. The history endpoint does not advance fulfillment or infer delivery from an expected date.

A.5 — Live pagination

- Each page is a current read, not a frozen export. New orders can shift records between numbered pages; reloading page 1 shows the latest order list.
- The backend uses a deterministic order within each response. The frontend replaces pages rather than appending them into a supposedly complete historical snapshot.
- An out-of-range positive page returns an empty items array and current counts. Show `This page has no orders.` with `Go to first page`; do not label the entire account history empty if totalItems is positive.

Exception Flow:

E.1 — Missing or expired authentication

- Return HTTP 401 UNAUTHENTICATED. Clear displayed account-order data and navigate to `/sign-in`.
- Do not substitute guest orders, cache belonging to another account, or a public tracking result for the protected list.

E.2 — Invalid page request

- Unknown/repeated query parameters, malformed page values, or a supplied GET body return HTTP 400 VALIDATION_ERROR.
- Show feedback with an action to open `/account/orders` without the invalid query. Do not issue an arbitrary corrected query silently.

E.3 — Order service unavailable

- Temporary data-service failure returns HTTP 503 ORDER_HISTORY_UNAVAILABLE; unexpected failure returns HTTP 500 INTERNAL_ERROR.
- Show a retry for the current page. A failed request for another page must not display the previous page under the new page number as if it were current.

E.4 — Inconsistent source order data

- Missing required snapshots, invalid item counts/totals, or fulfillment values outside the supported lifecycle return ORDER_HISTORY_UNAVAILABLE.
- Do not fabricate a completed/canceled row or calculate missing totals from current product prices. Optional details not included in this list do not require catalog access.

UI Integration:

- Source: `28_Dasboard_Order History`, node `478:10910`, desktop 1920 × 1698.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=478-10910
- Live design context and rendered screenshot were inspected on 2026-09-19. This establishes the desktop list and controls; it does not establish a frozen dataset, mobile layout, or alternate loading/error states.

| Observed element | Integration |
| --- | --- |
| Order History title and active sidebar item | `/account/orders` |
| Order ID | Saved display orderNumber, not the internal UUID |
| Status | IN PROGRESS or COMPLETED from the declared fulfillment mapping |
| Date | Saved placedAt, displayed in the declared timezone |
| Total with product count | Final saved total and sum of purchased quantities |
| View Details and arrow | Disabled integration action until the order-details UC supplies its route |
| Numbered circles and previous/next arrows | Page navigation with actual totalPages |

- Reuse the shared Clicon shell/sidebar, Public Sans, light table borders/header background, orange active navigation/pagination, orange IN PROGRESS, green COMPLETED, and blue action styling.
- The source includes CANCELED samples, but the established UC-07/UC-08 lifecycle has no cancellation operation. Do not add a cancellation workflow or seed fictitious canceled orders just to reproduce those sample rows. Supporting canceled orders requires a later explicit lifecycle extension.
- The source repeats order numbers and has nonchronological sample dates. Populate unique order identities and the declared sort order instead.
- Label the quantity text `N items`, meaning summed purchased quantities. Preserve saved amounts even if catalog prices or products change.
- Use `America/Los_Angeles` for placement-date display, consistent with the California experiment and UC-08. Include a small timezone label; API timestamps remain UTC.
- A detached single-order sample appears beneath the main table in the source. It has no defined separate action/data role and is omitted from this desktop list implementation; do not treat it as another real order or infer a complete mobile layout from it.
- Empty, loading, out-of-range, and error states are project supplements. View Details is visible but disabled with `Order details are not available yet.` No absent route is registered as a working destination.
- Enable Order History in implemented account sidebars and add a link to the existing dashboard shell. This does not implement full dashboard statistics or change UC-07's disabled View Order control yet.

API Endpoint:

`GET /api/v1/account/orders`

Checkout integration extends internal quote/order association and first-placement eligibility as specified in A.2/A.3. Existing UC-07 request and successful response shapes are unchanged; no ownership-assignment endpoint is introduced.

Request Body:

No body. Accepted query:

| Parameter | Contract |
| --- | --- |
| page | Optional decimal integer from 1 to 1000000, default 1; fixed page size 12 |

- Reject zero, signs, fractions, whitespace, repeated page, unknown query parameters, or a GET body. Canonical browser URL is `/account/orders?page=<page>`; omit page for page 1.
- The session selects the account. Do not accept email, accountId, browser cart ID, order status, or client-provided ownership filters.

Successful Response:

HTTP 200:

```json
{
  "success": true,
  "message": "Order history retrieved.",
  "data": {
    "items": [{
      "id": "b5cf395b-fc08-4c2d-9132-bb01924ba70b",
      "orderNumber": "CL-00001234",
      "orderStatus": "PLACED",
      "fulfillmentStatus": "ORDER_PLACED",
      "displayStatus": "IN_PROGRESS",
      "placedAt": "2026-09-19T10:03:00.000Z",
      "currency": "USD",
      "total": 340300,
      "itemCount": 2
    }],
    "page": 1,
    "pageSize": 12,
    "totalItems": 1,
    "totalPages": 1,
    "displayTimeZone": "America/Los_Angeles"
  }
}
```

- All keys are required. id is the order UUID; orderNumber is its unique saved display number. Example values are illustrative and use UC-07-compatible monetary units.
- items contains at most 12 account-associated orders, sorted by placedAt descending and id descending for equal timestamps. Count and page selection use the same account scope and consistent database view for that response.
- orderStatus is PLACED for the supported lifecycle. fulfillmentStatus is ORDER_PLACED, PACKAGING, ON_THE_ROAD, or DELIVERED. displayStatus is IN_PROGRESS or COMPLETED according to A.4.
- placedAt is ISO 8601 UTC. currency is USD; total is a nonnegative integer number of cents from the persisted final order total, including its original shipping/discount/tax.
- itemCount is a positive integer sum of saved line quantities. It is not the count of distinct variants, current cart count, or remaining inventory.
- totalItems is the number of associated orders; totalPages = ceil(totalItems / 12), including 0 when empty. Page beyond totalPages has empty items without changing the requested page number.
- No contact email, address, payment credentials, quote ID, or account identity is exposed by this summary response. An order number is not an authorization grant for another endpoint.

Error Response:

Use the shared envelope without data. timestamp is server-generated UTC; path is the request pathname without query parameters.

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-19T10:00:00.000Z",
  "path": "/api/v1/account/orders",
  "errors": {"page": ["Page must be an integer from 1 to 1000000."]}
}
```

| HTTP | Endpoint scope | Code | Exact message |
| --- | --- | --- | --- |
| 400 | History | VALIDATION_ERROR | `Please correct the highlighted fields.` |
| 401 | History or new account-bound placement | UNAUTHENTICATED | `You must sign in to continue.` |
| 503 | History | ORDER_HISTORY_UNAVAILABLE | `Order history is temporarily unavailable. Please try again later.` |
| 500 | History | INTERNAL_ERROR | `Unable to complete your request. Please try again later.` |
| 409 | UC-07 first placement | CHECKOUT_ACCOUNT_CHANGED | `Your checkout account changed. Review a new quote before placing your order.` |
| 503 | UC-07 quote/placement identity resolution | CHECKOUT_UNAVAILABLE | `Checkout is temporarily unavailable. Please try again later.` |

- Optional errors appears only for VALIDATION_ERROR and maps query field names to nonempty message arrays. Body-level errors may omit it.
- Checkout errors use their actual `/api/v1/orders` or `/api/v1/checkout/quotes` path and the same required timestamp/statusCode/code/message envelope. They do not clear the cart or create a partial order.
- CHECKOUT_ACCOUNT_CHANGED is an added UC-07 integration error for this combined baseline, not a claim that the earlier UC-07 already defined it.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement the authenticated account-order list in NestJS and the explicit forward-only checkout association extension.

- Add nullable internal account ownership to quotes/orders. Bind a new quote to the resolved current account or confirmed guest state, and preserve that binding through first placement as defined above.
- Derive ownership from trusted authenticated context; neither matching contact email nor a client-supplied account ID assigns an order.
- Copy ownership as part of UC-07's all-or-nothing order creation outcome. Repeated placement returns the existing result without reassignment; existing guest/unassociated orders remain unassociated.
- Query only the current account's orders. Preserve immutable amounts/quantities and obtain fulfillment from UC-08's existing source. No catalog-price lookup or carrier request is needed to render history.
- Keep account-history ownership independent of original-browser confirmation/tracking eligibility. No guest-order claim, account merge, migration by email, or payment-state update is implemented here.
- Provide a consistent count/page result with deterministic sorting. This endpoint is read-only and does not extend session expiry.

### Frontend UI Context

Build `OrderHistoryPage` at `/account/orders` in React, TypeScript, and Tailwind CSS from the inspected table.

- Enable Order History navigation in the existing account shell/sidebar. Retain implemented Dashboard, Tracking, Cart, Wishlist, Compare, Browsing History, and Settings routes.
- Render the five observed columns and numbered pagination. Show actual totalPages, not the source's fixed six pages. Show all pages when there are at most seven; otherwise show first/last, current and adjacent pages, with noninteractive ellipses for gaps.
- Disable previous/next at boundaries and while loading. Hide pagination for zero/one page. Mark active page accessibly.
- Use distinct in-progress/completed labels and colors. Do not show paid/canceled/refunded status from unsupported assumptions.
- Keep View Details disabled with its scope explanation until the order-detail feature exists. No simulated detail screen or row action is introduced.

### Frontend Logic and API Context

- Resolve the session, parse the browser page query, and request that page. Preserve page in the URL so reload/back/forward reproduce the requested page.
- State includes account identity, page, rows, counts, loading, and feedback. A page/account change invalidates prior pending responses; only the current request can populate the table.
- Replace rows on each successful page load. Failed navigation displays a page-specific error rather than mislabeling previous rows as the new page.
- On 401, clear personal data and navigate to Sign In. On a valid empty result distinguish no account orders from an out-of-range page.
- In checkout, display `This order will be linked to your signed-in account.` for account-bound quotes and `Guest order` for guest-bound quotes based on the resolved session used for quoting. These are project supplements, not Figma-derived ownership rules.
- If identity changes while reviewing checkout, invalidate the local quote and request a fresh one; the backend checks again at placement. During an unresolved placement outcome, reconcile the existing quote first under UC-07 before starting a new quote or account-binding decision.
- Account-bound placement 401 requires sign-in/review; CHECKOUT_ACCOUNT_CHANGED requires a fresh quote and explicit new placement click. Never automatically resubmit an order after either response.

### Validation and Error-Handling Context

- Validate query shape and pagination range; resolve account ownership on every list request. Display-order numbers and contact emails do not replace session-based account association.
- Do not conflate history displayStatus with orderStatus, fulfillmentStatus, or payment status. A delivered COD order is not assumed paid.
- Preserve unassociated orders as such; an empty account list must not trigger automatic guest-order import or a duplicate purchase.
- A network failure shows `Unable to connect. Please check your connection and try again.` Malformed list data shows `Unable to load order history. Please try again.` Neither displays fabricated rows or a successful empty history.
- Missing required order snapshots or inconsistent fulfillment data follows the documented service-error path, not catalog-based reconstruction.
- Failure of the association eligibility checks must leave UC-07's order/inventory/cart outcome unchanged. Existing successful retries remain governed by the original order's immutable association.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
