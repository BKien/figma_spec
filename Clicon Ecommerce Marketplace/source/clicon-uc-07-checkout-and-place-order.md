# UC-07: Checkout and Place Order

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Checkout and Place Order

Description:

- Allows a visitor or customer to provide billing/delivery information, review a checkout quote, and place a Cash on Delivery order from the saved UC-06 cart.
- Includes the checkout form, order creation, and reloadable order-confirmation screen. Continues UC-06 without requiring account registration or login.
- Payment availability, delivery coverage, quote lifetime, pricing, order rules, and API contracts are project decisions. The inspected Figma frames establish desktop layout and visible controls.
- Online payment, coupons, order history/details, tracking, cancellation, email notifications, and saved address management are separate use cases or integrations. Cash on Delivery placement does not imply that payment has been collected.

Primary Actor:

Visitor or signed-in Customer with a browser cart.

Preconditions:

- UC-06 provides a saved, nonempty cart whose lines are currently eligible for checkout. Unsaved cart edits must be saved before proceeding.
- UC-04/UC-05 provide the shared catalog, variant identities, USD-cent prices, and current availability. Inventory contains a quantity available for each purchasable variant.
- Browser routes `/checkout` and `/checkout/success/:quoteId` support direct navigation and reload.
- The shared response envelope applies. Browser cart identity remains independent of the UC-02 account session; signing in does not merge carts or change checkout ownership.

Postconditions:

- Success: Exactly one order is associated with the accepted quote; its item, address, and price snapshots are saved. Order status is `PLACED`; payment status is `UNPAID`; payment method is `CASH_ON_DELIVERY`.
- Success: Available inventory is reduced by the ordered quantities, the purchased cart is emptied, and its revision advances by one. The header count becomes 0 after cart refresh.
- Failure: A rejected placement creates no order, deducts no inventory, and clears no cart items. A transport failure may leave the result unknown; the frontend resolves the original quote's result before attempting further placement.
- Viewing the form or obtaining a quote creates no order, reserves no stock, and collects no payment.

Main Flow:

1. The visitor selects UC-06's `PROCEED TO CHECKOUT` for a saved cart. The frontend refreshes that cart and navigates to `/checkout` only when it remains eligible.
2. The checkout page obtains delivery options and the current cart. It displays Billing Information, Payment Option, Additional Information, and Order Summary.
3. The visitor enters first/last name, optional company, address, country, region/state, city, postal code, email, and phone number.
4. By default, the billing address is also the delivery address. The visitor may select `Ship into different address` and enter the separate recipient/address fields.
5. Cash on Delivery is selected. The visitor may enter optional order notes.
6. Once the complete form is valid, the frontend requests a quote using the current cart revision and entered form values. The backend validates the form, cart, availability, and delivery coverage, then returns current line prices and totals.
7. The visitor reviews the returned quote and selects `PLACE ORDER`. Form edits invalidate the displayed quote and require a new quote before placement.
8. The backend checks the quote, unchanged cart, current prices, delivery policy, and sufficient inventory. It places the order, deducts inventory, and empties the purchased cart as one business outcome.
9. The API returns the persisted order confirmation. The frontend navigates to `/checkout/success/:quoteId`, loads its confirmation, and refreshes the header cart count.
10. The confirmation screen displays successful placement, the order number, and the amount due on delivery. It does not report payment success.

Alternative Flow:

A.1 — Guest checkout

- The visitor uses the same browser cart and supplies contact information without logging in. Checkout does not create an account or verify an email address.
- Order confirmation is available only in the originating browser context. An order number or quote ID alone does not grant another browser access.
- Signing in during the flow does not replace the cart or attach a guest order to a different identity. Account history association is outside this UC.

A.2 — Separate delivery address

- When selected, show an additional address group with first name, last name, optional company, street address, country, region/state, city, and postal code.
- Billing email/phone remain the order contact details. A second contact email/phone is not introduced.
- When deselected, send `shippingAddress: null`; the backend copies the billing address into the order's delivery snapshot. Hidden draft values are not submitted.

A.3 — Return to cart

- The breadcrumb's Shopping Card link returns to `/cart`. Checkout does not silently save cart changes.
- Form values remain in component state during the current page visit; navigating away/reloading may discard them. A placed order remains retrievable through its confirmation route.

A.4 — Repeat a placement request

- The same quote can create at most one order. A repeat placement for an already placed quote returns HTTP 200 with that existing order, even though the cart is now empty or the quote's original validity time has passed.
- A first successful placement returns HTTP 201. Both outcomes use the same successful payload and message.
- Reusing another quote for the consumed cart fails the cart-revision check; it cannot create a second order from the same saved cart version.

Exception Flow:

E.1 — Empty, expired, or ineligible cart

- Direct entry with an empty/expired cart displays `Your cart is empty.` and a link to `/shop`.
- Unavailable or insufficient-quantity lines block quoting/placement. Show feedback and `Review cart` linking to `/cart`; do not silently remove lines or reduce quantities.

E.2 — Invalid input or unsupported address/payment

- Invalid field shapes/values return HTTP 400 `VALIDATION_ERROR` with field feedback where applicable.
- Well-formed addresses outside the experiment's supported delivery locations return HTTP 422 `DELIVERY_UNAVAILABLE`.
- A recognized online payment method returns HTTP 422 `PAYMENT_METHOD_UNAVAILABLE`. Unknown payment-method strings are validation errors.
- Preserve entered form values and allow correction. No order is created.

E.3 — Cart or quote changed

- A cart revision different from the quote's saved revision returns HTTP 409 `CART_CHANGED`. Reload the cart and require a new quote; preserve form values while the page remains open.
- An unplaced quote expires fifteen minutes after creation. Placement at or after its expiry returns HTTP 409 `QUOTE_EXPIRED`; obtaining a replacement does not place an order.
- If any quoted unit price or delivery-pricing policy changes, return HTTP 409 `QUOTE_CHANGED`. Obtain and display a new quote and require another deliberate `PLACE ORDER` click. Never automatically accept a changed total.
- Prices/totals cannot be trusted merely because cart revision still matches: UC-06 revisions track item mutations, not price changes.

E.4 — Stock changes before placement

- Removed/unpublished variants return HTTP 404 `VARIANT_NOT_FOUND`. Insufficient stock or a reduced quantity limit returns HTTP 409 `QUANTITY_UNAVAILABLE`.
- Stock must be sufficient for the entire order. Concurrent purchases cannot result in negative available inventory or partial orders.
- Retain the cart on rejection and direct the visitor to review it. A quote is not a stock reservation.

E.5 — Placement response is lost

- Display `We could not confirm your order. Checking its status.` Keep the original quote ID and disable creation of a replacement quote/order while the result is unresolved.
- Load the original quote through the read endpoint. If PLACED, show its existing confirmation. If READY, allow a deliberate retry using the same quote ID; a concurrent completion still returns the same order. If EXPIRED, allow a fresh quote only after the read confirms that no order is associated with it.
- A failed status read leaves the result unknown. Display a retry-status action; do not show success, clear the cart locally, or automatically submit a new order.

E.6 — Confirmation unavailable

- An unknown quote, or one belonging to another browser context, returns HTTP 404 `CHECKOUT_NOT_FOUND`.
- A READY or EXPIRED quote on the success route displays `This checkout has not placed an order.` and `Return to checkout`; it must not show a success checkmark.
- Service errors show retry feedback. A frontend route alone is not proof of placement.

UI Integration:

- Checkout source: `14_Check-out`, node `493:15194`.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=493-15194
- Confirmation source: `15_Check-out_Success`, node `510:16556`.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=510-16556
- Live design context and rendered screenshots of both frames were inspected on 2026-09-18. This does not claim a frozen dataset, responsive design, error states, or a captured expanded delivery-address panel.

| Observed element | Integration |
| --- | --- |
| Billing Information; User name / first and last name | `billingAddress.firstName` and `lastName` |
| Company Name (Optional), Address | `company`, `addressLine` |
| Country, Region/State, City, Zip Code | Dependent selectors and postal-code input |
| Email, Phone Number | `contact.email`, `contact.phone` |
| Ship into different address checkbox | `shipToDifferentAddress` and conditional `shippingAddress` |
| Cash on Delivery / Venmo / Paypal / Amazon Pay / Debit/Credit Card | COD enabled; other displayed methods disabled with a scope explanation |
| Name on Card / Card Number / Expire Date / CVC | Card-specific group hidden under selected COD; card collection is not implemented |
| Order Notes (Optional) | `orderNotes` |
| Order Summery, product lines, price breakdown | Quote-backed summary; use corrected visible heading `Order Summary` |
| PLACE ORDER | Submit the reviewed quote |
| Success checkmark and heading | Only after confirmed PLACED state |
| Go to Dashboard / View Order | Existing account shell / future order-details integration as described below |

- Reuse the shared Clicon header/footer, breadcrumbs, Public Sans, orange primary actions (#FA8232), blue prices (#2DA5F3), and light borders (#E4E7E9). Preserve the form/summary desktop columns and centered confirmation composition.
- The source selects a card payment and displays card inputs. This experiment selects the visible COD option instead; disable online-payment choices with `Online payment is not available yet.` Do not collect card data or simulate a paid response.
- The expanded delivery form reuses the billing-address field arrangement as a project supplement. Loading, invalid-input, expired-quote, and uncertain-result states are also supplements.
- Replace the source's sample amounts with calculated values. Before a quote exists, show saved cart merchandise totals and `Pending quote` for final totals; never present those amounts as a confirmed order total.
- Shipping is a flat 500 USD cents per order, discount is 0, and experimental tax is 0. These are fixed experiment fixtures, not real shipping/tax rules. Label the zero tax `Tax (experiment)`.
- Correct the success heading to `Your order has been placed successfully.` Replace filler text with order number and `Amount due on delivery: <total>.` The number/amount are project additions, not observed source fields.
- `Go to Dashboard` links to the existing `/account/dashboard` shell for a signed-in user. For guests, label the same secondary action `Continue shopping` and link to `/shop`.
- `View Order` remains disabled with `Order details are not available yet.` until its owning UC provides a real route. Do not create an unimplemented destination or count a new order-details feature in UC-07.

API Endpoint:

| Method and path | Purpose |
| --- | --- |
| `GET /api/v1/checkout/options` | Obtain supported address/payment options and experiment pricing |
| `POST /api/v1/checkout/quotes` | Validate the form and create a reviewable quote |
| `GET /api/v1/checkout/quotes/:quoteId` | Resolve READY, EXPIRED, or PLACED state and any order confirmation |
| `POST /api/v1/orders` | Place the order represented by the supplied quote |

Request Body:

GET endpoints have no body or query parameters. `quoteId` is a UUID.

Quote request:

```json
{
  "expectedCartRevision": 2,
  "contact": {"email": "customer@example.com", "phone": "+14155550123"},
  "billingAddress": {
    "firstName": "Alex",
    "lastName": "Nguyen",
    "company": null,
    "addressLine": "123 Example Street",
    "countryCode": "US",
    "regionCode": "CA",
    "cityCode": "SAN_FRANCISCO",
    "postalCode": "94105"
  },
  "shipToDifferentAddress": false,
  "shippingAddress": null,
  "paymentMethod": "CASH_ON_DELIVERY",
  "orderNotes": null
}
```

Placement request:

```json
{"quoteId": "12dd9374-7eac-4d29-99bc-ad42cff8b791"}
```

- All shown keys are required; reject unknown fields/query parameters. Do not accept cart items, account/cart IDs, prices, totals, or payment status in either request. The server resolves the browser cart and quoted form.
- `expectedCartRevision` is a nonnegative JSON integer. `shipToDifferentAddress` is a JSON boolean.
- Address objects always use the eight displayed keys. First/last name: trimmed, 1–100 characters each; company: null or trimmed 1–100 characters; addressLine: trimmed 1–200 characters.
- Country/region/city codes are strings of 1–40 uppercase letters or underscores. Their relationships and membership must match the options endpoint. Postal code is exactly five ASCII digits for the supported US fixture.
- Email: trim/lowercase, valid email format, maximum 254 characters, consistent with the project's identity normalization. This is an order contact, not proof of account ownership. Phone: a plus sign followed by 8–15 digits, first digit nonzero.
- `shippingAddress` must be a complete address object when the checkbox is true, and null otherwise. Both submitted addresses must belong to supported fixture locations.
- `orderNotes` is null or trimmed text of 1–500 characters. Blank optional company/notes inputs are submitted as null. String-length limits count Unicode code points.
- Recognized payment enums are CASH_ON_DELIVERY, VENMO, PAYPAL, AMAZON_PAY, and CARD; only CASH_ON_DELIVERY can produce a quote in this UC.

Successful Response:

All fields shown in the following contracts are required. UUIDs, product records, and times are examples, not fixed production data.

Options — HTTP 200:

```json
{
  "success": true,
  "message": "Checkout options retrieved.",
  "data": {
    "countries": [{
      "code": "US", "name": "United States",
      "regions": [{
        "code": "CA", "name": "California",
        "cities": [
          {"code": "SAN_FRANCISCO", "name": "San Francisco"},
          {"code": "LOS_ANGELES", "name": "Los Angeles"}
        ]
      }]
    }],
    "paymentMethods": [
      {"code": "CASH_ON_DELIVERY", "enabled": true},
      {"code": "VENMO", "enabled": false},
      {"code": "PAYPAL", "enabled": false},
      {"code": "AMAZON_PAY", "enabled": false},
      {"code": "CARD", "enabled": false}
    ],
    "pricing": {"currency": "USD", "shipping": 500, "discount": 0, "tax": 0}
  }
}
```

- The two California cities above are the complete experiment delivery fixture, not a claim of worldwide service. Selectors use this hierarchy; changing a parent clears incompatible descendants. No external location service is required.

Quote creation — HTTP 201, message `Checkout quote created.`; quote read — HTTP 200, message `Checkout retrieved.`. Both return the following `data` schema:

```json
{
  "success": true,
  "message": "Checkout quote created.",
  "data": {
    "checkout": {
      "quoteId": "12dd9374-7eac-4d29-99bc-ad42cff8b791",
      "status": "READY",
      "cartRevision": 2,
      "expiresAt": "2026-09-18T10:15:00.000Z",
      "currency": "USD",
      "items": [{
        "productId": "c168f6e8-a7e4-4efc-b278-2f96da050e8f",
        "variantId": "5c69ff67-1c39-41e3-982f-51ec2016da71",
        "name": "Apple MacBook Pro 14-inch",
        "options": {"color": "Space Gray", "size": "14-inch", "memory": "16GB", "storage": "512GB SSD"},
        "imageUrl": "/images/products/macbook-pro-14-front.png",
        "quantity": 2,
        "unitPrice": 169900,
        "lineTotal": 339800
      }],
      "totals": {"subtotal": 339800, "discount": 0, "shipping": 500, "tax": 0, "total": 340300},
      "order": null
    }
  }
}
```

- `items` is a nonempty ordered snapshot of UC-06's saved cart. IDs/options/image selection reuse UC-05/UC-06; imageUrl may be null, and each option is a nonempty string or null. Quantities are integers 1–99 and satisfy availability when quoted.
- Amounts are nonnegative integer USD cents. lineTotal = unitPrice × quantity; subtotal = sum(lineTotal); total = subtotal − discount + shipping + tax.
- `status` is READY, EXPIRED, or PLACED. READY means unplaced and within its time window; it does not guarantee that stock/prices/cart are still unchanged. EXPIRED means unplaced and at/past expiresAt. PLACED takes precedence over expiry.
- Quote reads return the original item/total snapshot, never silently reprice it. Creating a fresh quote is required after input or pricing changes. Reads do not extend validity.
- `order` is null for READY/EXPIRED, and the order object below for PLACED. Contact/address/notes are captured with the quote for placement but are not echoed by this response.

Placement — HTTP 201 for creation, HTTP 200 for an existing result:

```json
{
  "success": true,
  "message": "Order placed successfully.",
  "data": {
    "order": {
      "id": "b5cf395b-fc08-4c2d-9132-bb01924ba70b",
      "orderNumber": "CL-00001234",
      "quoteId": "12dd9374-7eac-4d29-99bc-ad42cff8b791",
      "status": "PLACED",
      "paymentMethod": "CASH_ON_DELIVERY",
      "paymentStatus": "UNPAID",
      "currency": "USD",
      "total": 340300,
      "placedAt": "2026-09-18T10:03:00.000Z"
    }
  }
}
```

- `id` and quoteId are UUIDs; orderNumber is a unique nonempty display string. The displayed `CL-00001234` format is illustrative. Times are server-generated ISO 8601 UTC.
- The placed order retains its own contact, billing/delivery address, notes, item, and price snapshots even after catalog/cart changes. This minimal confirmation response is not the future order-details API.
- Quote/result lookup remains available in the originating browser context for at least seven days after quote creation, independently of cart clearing and account-session expiry. Losing that browser context removes access through this UC; it does not delete an order or authorize recreation.

Error Response:

Use the centralized envelope with no `data`. `timestamp` is generated in UTC; `path` is the actual endpoint pathname without a query string.

```json
{
  "success": false,
  "statusCode": 409,
  "code": "QUOTE_CHANGED",
  "message": "Checkout prices have changed. Review a new quote before placing your order.",
  "timestamp": "2026-09-18T10:02:00.000Z",
  "path": "/api/v1/orders"
}
```

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-18T10:00:00.000Z",
  "path": "/api/v1/checkout/quotes",
  "errors": {"billingAddress.postalCode": ["Postal code must contain exactly five digits."]}
}
```

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | `Please correct the highlighted fields.` |
| 404 | CHECKOUT_NOT_FOUND | `This checkout is not available.` |
| 404 | VARIANT_NOT_FOUND | `This product configuration is not available.` |
| 409 | CART_EMPTY | `Your cart is empty.` |
| 409 | CART_CHANGED | `Your cart changed. Review it before trying again.` |
| 409 | QUANTITY_UNAVAILABLE | `The requested quantity is not available. Review your cart.` |
| 409 | QUOTE_EXPIRED | `Your checkout quote has expired. Review a new quote before placing your order.` |
| 409 | QUOTE_CHANGED | `Checkout prices have changed. Review a new quote before placing your order.` |
| 422 | DELIVERY_UNAVAILABLE | `This address is outside the supported delivery area.` |
| 422 | PAYMENT_METHOD_UNAVAILABLE | `This payment method is not available.` |
| 503 | CATALOG_UNAVAILABLE | `The product catalog is temporarily unavailable. Please try again later.` |
| 503 | CART_UNAVAILABLE | `Your cart is temporarily unavailable. Please try again later.` |
| 503 | CHECKOUT_UNAVAILABLE | `Checkout is temporarily unavailable. Please try again later.` |
| 500 | INTERNAL_ERROR | `Unable to complete your request. Please try again later.` |

- Optional `errors` appears only for VALIDATION_ERROR, mapping request field paths to nonempty arrays of message strings. Body-level errors may omit it.
- On placement, resolve an accessible quote and return any existing order before checking expiry, cart revision, or current stock. For an unplaced quote, check expiry, cart revision, nonempty cart, variant availability/quantity, and quote pricing before creation. No business rejection partially changes the order/cart/inventory outcome.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement checkout options, quote creation/read, and order placement in NestJS using the existing catalog, browser cart, and response envelopes.

- Store quotes with their originating browser/cart context, cart revision, submitted form snapshot, item/pricing snapshot, creation/expiry times, and any resulting order identity.
- Distinguish the concrete originating cart from its revision: a newly created cart with a repeated numeric revision must not satisfy a quote for an expired/replaced cart.
- Use the declared delivery and pricing fixtures. Copy billing to delivery when separate shipping is false. Store the effective delivery address with the order, not a reference to mutable form state.
- A quote captures the complete form. Changing contact, address, payment, or notes requires a new quote; order placement accepts only quoteId.
- Preserve the one-order-per-quote and one-consumption-per-cart-version outcomes under repeated/concurrent requests. Order creation, inventory deduction, and cart clearing must either all succeed or all remain unchanged.
- Deduct actual variant inventory on successful placement and expose resulting availability through UC-05/UC-06. Clear the consumed cart, increment revision once, and refresh its seven-day persistence period as a successful cart mutation.
- Subsequent repeats return the saved order without another inventory deduction or cart clearing. In particular, do not clear products added after the original order was placed.
- Keep confirmation lookup independent of account-session duration and empty-cart lifecycle for the declared availability period. This UC does not create account history, send email, invoke a payment provider, or claim that cash has been collected.

### Frontend UI Context

Build `CheckoutPage` and `CheckoutSuccessPage` in React, TypeScript, and Tailwind CSS from the inspected frames.

- Connect UC-06's eligible, saved-cart action to `/checkout`. Register the confirmation route within this UC so placement cannot finish at a missing page.
- Preserve billing fields, dependent address selectors, payment option row, notes field, summary column, and confirmation composition. Show selected product options in summary lines where needed to distinguish variants.
- Select COD; disable other payment methods with their explanation and hide card-only inputs. Do not render a pretend card-processing interaction.
- Expand the separate delivery form only when requested. Provide labels, inline field errors, loading indicators, and clear focus on the first invalid field.
- Display the payable total only from a valid reviewed quote. After any form change, label the old summary `Updating quote` or `Quote required` and disable placement until the current form has a successful quote.
- Only a PLACED response displays the success checkmark. Dashboard/continue-shopping and future View Order controls follow the explicit route boundaries above.

### Frontend Logic and API Context

- On checkout entry, read the saved cart and checkout options. Empty/ineligible carts receive their documented recovery state, not an active placement form.
- Keep contact, billing address, separate-delivery toggle/address, notes, quote, loading/error state, and placement state. Initialize blank form fields; do not infer personal contact data from Figma examples.
- Request a quote when a complete valid form settles after a field change, allowing one second without further edits. Invalid or incomplete form state has no usable quote. Ignore a quote response for an older form/cart snapshot.
- Placement is enabled only for a READY quote matching the current form and cart snapshot, while no request is pending. Server time/expiry checks remain authoritative even if the browser countdown differs.
- Send only quoteId on placement. Retain that ID and the unresolved-placement marker across reload in the same browser until its result is reconciled; a reloaded page checks that result before starting another checkout.
- After confirmed placement, navigate to the success route and refresh the cart count from UC-06. Reopening success reads the quote; it never posts another order merely because the page mounted.
- For expired/changed quotes, preserve form values, fetch a new quote, show the updated summary, and require a new explicit placement click. For a changed/ineligible cart, send the visitor to review the cart as needed.
- Do not replace an unresolved placement with a fresh quote. Follow E.5 using the original quote read/retry behavior.

### Validation and Error-Handling Context

- Validate field presence/types/lengths, address hierarchy, postal code, email/phone, and conditional delivery-address requirements. Disabled browser choices do not replace server validation of supported methods and locations.
- Check current cart identity/revision, publication, quantity limits, stock, prices, and delivery-pricing policy again at placement. Browser totals are display values, not order inputs.
- Treat placement's business success as an indivisible order/inventory/cart outcome; do not acknowledge a partial order or silently modify purchased quantities.
- Explicit validation/business rejection leaves the form editable and does not announce success. A timeout, unreadable response, or server response that does not establish a definite result is reconciled through the original quote before another placement decision.
- Options/quote-read network failure shows `Unable to connect. Please check your connection and try again.` Preserve the last known state as stale, with placement disabled until recovery.
- A malformed quote/confirmation response displays `Unable to load checkout information. Please try again.` It must not produce a zero total, fabricated order number, or success screen.
- Missing product images use a neutral placeholder while retaining readable names, quantities, and prices. Unavailable confirmation offers a path to `/shop`; it never instructs the visitor to recreate an order whose outcome is unknown.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
