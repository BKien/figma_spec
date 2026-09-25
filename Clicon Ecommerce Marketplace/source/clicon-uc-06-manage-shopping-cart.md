# UC-06: Manage Shopping Cart

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Manage Shopping Cart

Description:

- Allows a visitor or customer to add a selected product configuration to a shopping cart, inspect its contents, change quantities, and remove items before checkout.
- Continues UC-05 through its selected variant and quantity. Includes the cart page and shared header cart count.
- Cart persistence, staged editing, pricing rules, and API contracts below are project decisions. Figma establishes the inspected desktop controls and layout, not their backend behavior.
- Coupon application, shipping/tax quotation, checkout, Buy Now, and the homepage cart popup belong to separate integrations. This UC does not reserve stock or create an order.

Primary Actor:

Visitor or signed-in Customer using the same browser.

Preconditions:

- UC-04 exposes `/shop`; UC-05 exposes `/products/:slug` and published product variants with prices, availability, and `maxQuantity`.
- The application exposes `/cart` with direct navigation and reload support.
- The shared success/error envelope applies. Monetary amounts use integer USD cents, consistent with UC-04 and UC-05.
- Login is not required. For this experiment, the cart belongs to the browser context, independently of the eight-hour account session. It is not an account-synchronized cart.

Postconditions:

- Success: The server stores the accepted item quantities; the cart page and header count reflect the returned cart. Each product variant appears at most once.
- Failure: A rejected mutation leaves stored item quantities unchanged. The frontend shows the relevant error and does not report a successful add/update.
- Reading or editing the cart does not reserve or decrement inventory, apply a coupon, take payment, or place an order.

Main Flow:

1. On UC-05, the visitor selects a valid in-stock variant and a permitted quantity.
2. The frontend obtains the current cart and its revision, then submits the selected variant and quantity using `POST /api/v1/cart/items`.
3. The backend checks the cart revision and current catalog availability. For an existing variant, the requested quantity is added to its stored quantity; otherwise, a new line is added.
4. The backend returns HTTP 200 with the complete updated cart. The frontend displays `Added to cart.`, updates the header count, and offers `View cart` linking to `/cart`.
5. The visitor opens `/cart`; the frontend loads `GET /api/v1/cart` and renders its items and current price summary.
6. The visitor changes quantities using minus/plus or selects a line's remove icon. These changes form a local draft; they are not yet persisted.
7. The visitor selects `UPDATE CART`. The frontend sends the complete desired set of remaining lines and their quantities using `PUT /api/v1/cart`.
8. The backend validates the complete update and saves it as one business operation. No subset of a rejected update is saved.
9. The frontend replaces its stored snapshot and draft with the returned cart, updates totals and the header count, and displays `Cart updated.`

Alternative Flow:

A.1 — Open an empty cart

- A browser without a cart receives an empty cart with revision 0. An existing cart with no lines retains its current revision.
- Display `Your cart is empty.` and `RETURN TO SHOP` linking to `/shop`. The header count is 0; checkout is disabled.

A.2 — Add a variant already in the cart

- Merge by `variantId`, not product name or product ID. Different variants of the same product remain separate lines.
- The resulting quantity must be within the current `maxQuantity`. Do not silently reduce the requested amount to fit stock.

A.3 — Remove items

- Selecting the remove icon removes that line from the local draft. Display `Unsaved cart changes.` until `UPDATE CART` succeeds.
- If all lines are removed from the draft, keep the update action available with `Save changes to empty your cart.` The stored cart and header count remain unchanged until saving succeeds.
- Navigating away or reloading discards unsaved edits. Returning loads the stored cart; no background save is implied.

A.4 — Continue shopping

- `RETURN TO SHOP` navigates to `/shop`. Clicking an available item's image/title opens `/products/:slug?variant=<variantId>`.
- Unsaved cart edits are discarded on either navigation. Display this behavior alongside the unsaved-changes notice.

A.5 — Revisit the cart

- Successful mutations keep the browser cart available for seven days from that mutation. Reads do not extend this period. After expiry, a read returns a new empty cart with revision 0.
- Sign-in, sign-out, or account-session expiry does not transfer, merge, or clear this browser cart. A different browser starts with a separate cart. Clearing browser cart-identification data loses access to the previous cart.
- These are experiment scope decisions; account synchronization and guest-to-account merging are not part of this UC.

Exception Flow:

E.1 — Quantity or cart limit exceeded

- Adding or saving a quantity that exceeds current availability returns HTTP 409 `QUANTITY_UNAVAILABLE`.
- A cart permits at most 50 distinct variants. An addition exceeding that count returns HTTP 409 `CART_LIMIT_REACHED`.
- Show the error, reload the current cart, and require the visitor to choose and submit new quantities. Do not silently accept a smaller quantity or a partial update.

E.2 — Product or variant no longer available

- Adding an unknown, removed, or unpublished variant/product returns HTTP 404 `VARIANT_NOT_FOUND`.
- A previously saved line remains visible when its product/variant becomes unavailable. Mark it `UNAVAILABLE`, disable its product link and quantity controls, and allow removal.
- An out-of-stock published variant is marked `OUT_OF_STOCK`; a saved quantity above the new positive limit is marked `QUANTITY_EXCEEDED`. Keep these lines visible and block checkout until corrected or removed.
- Saving a draft that retains an unavailable line returns `VARIANT_NOT_FOUND`; retaining an out-of-stock or excessive-quantity line returns `QUANTITY_UNAVAILABLE`. Removing such lines is permitted.

E.3 — Cart changed elsewhere or expired

- If `expectedRevision` differs from the current cart revision, return HTTP 409 `CART_CHANGED` without saving the request.
- Reload the cart, discard the stale draft, and display `Your cart changed. Review it before trying again.` Never automatically replay a failed addition or overwrite the newer cart.

E.4 — Price changed

- Cart reads and mutations use current catalog prices, not prices supplied by the browser or copied from the Figma samples.
- When a known displayed price changes after refresh/save, show `Some prices have changed. Review your cart.` Render the new returned values.
- Cart prices are estimates at the time of the response; checkout must obtain its own current quote. A cart revision tracks saved item changes, not a price guarantee.

E.5 — Service failure or uncertain mutation outcome

- A service error shows the documented feedback. An explicit rejected request does not change stored item quantities.
- If a mutation receives no usable response, its outcome may be unknown. Show `We could not confirm the cart change. Reload your cart before trying again.` Disable further mutations until a cart read succeeds; do not automatically resend the mutation.
- Failed reads show a retry action; do not present a service failure as an empty cart.

UI Integration:

- Source: `13_Shopping Card`, node `493:14954`, desktop frame 1920 × 1504.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=493-14954
- Live design context and its rendered screenshot were inspected on 2026-09-18. This establishes the desktop cart layout and visible controls; it does not establish a frozen dataset, mobile layout, empty/error states, or prototype behavior.

| Observed element | Integration |
| --- | --- |
| Shopping Card table; Products / Price / Quantity / Sub-Total | Cart lines, current unit prices, editable quantities, and calculated line totals |
| Circled remove icon | Remove a line from the local draft |
| Minus / quantity / plus | Edit a line's local quantity |
| RETURN TO SHOP | Navigate to `/shop` |
| UPDATE CART | Persist the complete draft |
| Card Totals; Sub-total / Shipping / Discount / Tax / Total | Current merchandise subtotal and explicitly provisional summary |
| PROCEED TO CHECKOUT | Checkout integration point; disabled until its owning UC is integrated |
| Coupon Code panel and APPLY COUPON | Coupon integration point; disabled until its owning UC is integrated |
| Shared header cart icon and badge | Open `/cart`; show total persisted item quantity |

- Reuse the shared header/footer and breadcrumb. Preserve the desktop table/summary columns, Public Sans typography, orange primary action (`#FA8232`), blue secondary actions (`#2DA5F3`), light borders (`#E4E7E9`), and dark body text (`#191C1F`).
- Preserve source labels `Shopping Card` and `Card Totals`. The source coupon input says `Email address`; use the meaningful placeholder `Coupon code`, while leaving coupon controls disabled with `Coupon application is not available yet.`
- The source shows a $250 item with quantity 03 but a $250 line subtotal. Do not reproduce that mismatch: unit price × quantity determines each line subtotal.
- Coupon discount is zero in this UC. Shipping and tax are not quoted: display `Calculated at checkout` for both, and label the total `Estimated total`. Never copy the sample Free shipping, $24 discount, or $61.99 tax into live calculations.
- Show selected configuration values beneath each product name so different variants remain distinguishable. Use the variant's first effective image under UC-05's image-fallback rule; use a neutral placeholder if no usable image exists.
- Empty, unsaved, loading, unavailable-line, and error feedback are project supplements styled consistently with this frame. Do not claim they are separately verified Figma states.
- In an isolated UC-06 implementation, checkout remains disabled with `Checkout is not available yet.` Do not navigate to an absent checkout route. Once its owning UC is integrated, connect the button to that defined route only for a saved, eligible cart.
- Connect UC-05's `ADD TO CARD` action to this UC. Keep `BUY NOW` separately scoped. UC-04 cards without an explicit complete variant selection continue to product details rather than choosing a configuration silently. The shared cart icon links directly to `/cart`; the homepage popup is not implemented here.

API Endpoint:

| Method and path | Operation |
| --- | --- |
| `GET /api/v1/cart` | Read the current browser cart with current catalog pricing |
| `POST /api/v1/cart/items` | Add a quantity of one selected variant |
| `PUT /api/v1/cart` | Save quantities/removals as a complete replacement of current lines |

Request Body:

`GET`: no body or query parameters.

`POST`:

```json
{
  "variantId": "5c69ff67-1c39-41e3-982f-51ec2016da71",
  "quantity": 1,
  "expectedRevision": 0
}
```

`PUT`:

```json
{
  "expectedRevision": 1,
  "items": [
    {
      "variantId": "5c69ff67-1c39-41e3-982f-51ec2016da71",
      "quantity": 2
    }
  ]
}
```

- All shown keys are required. Reject unknown fields and query parameters. Requests use the browser cart context; neither an account ID nor a cart ID is accepted in the body/query.
- `variantId` is a UUID. `quantity` is a JSON integer from 1 to 99, further constrained by current catalog `maxQuantity`. Numeric strings, fractions, null, and zero are invalid; removal is expressed by omission from the PUT list.
- `expectedRevision` is a nonnegative JSON integer obtained from the most recent cart response.
- PUT `items` is an array of 0–50 unique variant IDs already present in the current cart. It cannot introduce a new variant; additions use POST. Duplicate IDs or a new ID in this list are validation errors.
- An empty PUT list removes all lines. PUT quantity is the desired final quantity; POST quantity is an increment.
- The backend rejects a revision mismatch before interpreting the requested list against the cart. After shape validation, availability/quantity errors are resolved without saving any subset of the request.

Successful Response:

All three operations return HTTP 200 using the same payload schema. Messages are `Cart retrieved.`, `Added to cart.`, and `Cart updated.` respectively.

```json
{
  "success": true,
  "message": "Cart updated.",
  "data": {
    "cart": {
      "revision": 2,
      "currency": "USD",
      "items": [
        {
          "variantId": "5c69ff67-1c39-41e3-982f-51ec2016da71",
          "productId": "c168f6e8-a7e4-4efc-b278-2f96da050e8f",
          "slug": "macbook-pro-14",
          "name": "Apple MacBook Pro 14-inch",
          "options": {"color": "Space Gray", "size": "14-inch", "memory": "16GB", "storage": "512GB SSD"},
          "imageUrl": "/images/products/macbook-pro-14-front.png",
          "quantity": 2,
          "maxQuantity": 5,
          "status": "AVAILABLE",
          "unitPrice": 169900,
          "compareAtPrice": 199900,
          "lineTotal": 339800
        }
      ],
      "itemCount": 2,
      "totals": {
        "subtotal": 339800,
        "discount": 0,
        "shipping": null,
        "tax": null,
        "estimatedTotal": 339800,
        "isFinal": false
      },
      "eligibleForCheckout": true
    }
  }
}
```

- All shown keys are required. Example records/paths are illustrative and must be backed by actual catalog data. Item order is first-added order; changing a quantity does not reorder lines.
- `revision` starts at 0 and increases by one for each successful POST or PUT, including an accepted unchanged PUT. Failed mutations and reads do not advance it. An expired browser cart starts again at 0; stale nonzero revisions are rejected.
- `itemCount` is the sum of saved quantities, including currently unavailable lines. It is not the count of distinct variants.
- Product/variant IDs, options, and image selection reuse UC-05. Each option value is a nonempty string or null. `imageUrl` is a string or null. Retain last-known display identity/options/image for unavailable saved lines; never substitute another product.
- `status` is exactly `AVAILABLE`, `OUT_OF_STOCK`, `QUANTITY_EXCEEDED`, or `UNAVAILABLE`. Missing/unpublished product or variant takes precedence as UNAVAILABLE; otherwise maxQuantity 0 means OUT_OF_STOCK; otherwise saved quantity above maxQuantity means QUANTITY_EXCEEDED; all other lines are AVAILABLE.
- `maxQuantity` uses UC-05's current limit, 0–99; it is 0 for UNAVAILABLE lines. A saved quantity remains 1–99 even when current stock falls below it.
- For published variants, `unitPrice` is current nonnegative integer USD cents; `compareAtPrice` is null or greater than unitPrice; `lineTotal = unitPrice × quantity`. An unavailable line has null unitPrice, compareAtPrice, and lineTotal.
- `subtotal` is the sum of lineTotal, or null if any lineTotal is null. An empty cart has subtotal 0. `discount` is 0; `shipping` and `tax` are null; `estimatedTotal` equals subtotal and may be null; `isFinal` is false.
- `eligibleForCheckout` is true only for a nonempty cart whose every line is AVAILABLE. It describes item eligibility, not whether the checkout feature has been implemented or whether stock has been reserved.

Error Response:

Use the shared envelope. Errors omit `data`; `timestamp` is server-generated ISO 8601 UTC, and `path` is the actual endpoint pathname without its query string.

```json
{
  "success": false,
  "statusCode": 409,
  "code": "CART_CHANGED",
  "message": "Your cart changed. Review it before trying again.",
  "timestamp": "2026-09-18T10:00:00.000Z",
  "path": "/api/v1/cart"
}
```

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-18T10:00:00.000Z",
  "path": "/api/v1/cart",
  "errors": {
    "items.0.quantity": ["Quantity must be an integer from 1 to 99."]
  }
}
```

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | `VALIDATION_ERROR` | `Please correct the highlighted fields.` |
| 404 | `VARIANT_NOT_FOUND` | `This product configuration is not available.` |
| 409 | `QUANTITY_UNAVAILABLE` | `The requested quantity is not available. Review your cart.` |
| 409 | `CART_LIMIT_REACHED` | `Your cart can contain at most 50 product configurations.` |
| 409 | `CART_CHANGED` | `Your cart changed. Review it before trying again.` |
| 503 | `CATALOG_UNAVAILABLE` | `The product catalog is temporarily unavailable. Please try again later.` |
| 503 | `CART_UNAVAILABLE` | `Your cart is temporarily unavailable. Please try again later.` |
| 500 | `INTERNAL_ERROR` | `Unable to complete your request. Please try again later.` |

- `errors` is optional and only used for VALIDATION_ERROR. It maps request field paths such as `quantity`, `expectedRevision`, `items`, or `items.0.quantity` to nonempty arrays of strings. Body-level validation may omit it.
- Missing cart identity means an empty browser cart, not an authentication error. Catalog-service failure must not be converted into missing-product status or zero totals.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement the three cart endpoints in NestJS with the shared envelope and UC-04/UC-05 catalog identities.

- Persist the browser cart's revision, expiry, ordered variant quantities, and last-known display identity for retained unavailable lines. Resolve its browser context independently of account login; do not return an authentication token or require an account ID for cart operations.
- Apply the declared seven-day persistence rule and browser scope. Do not introduce account merging or change UC-02's session duration.
- POST merges only the same variant. PUT replaces current line quantities/removals, requires the matching revision, and permits no partial update. Preserve the declared behavior when competing requests arrive.
- Validate the resulting quantities against current published variants and maxQuantity. Removed lines do not need to remain purchasable for their removal to succeed.
- Resolve current catalog prices for responses and compute totals in integer cents. Do not accept client-supplied prices, discounts, totals, or availability.
- An empty cart can be returned without a catalog lookup. Failure to resolve required catalog data is a service error, not evidence that every saved variant was removed.
- Keep unavailable saved lines removable. Cart activity does not mutate inventory or create orders. Do not implement coupons, tax/shipping calculation, or payment in these endpoints.

### Frontend UI Context

Build `CartPage` at `/cart` in React, TypeScript, and Tailwind CSS using the inspected desktop frame.

- Render the source's item table, quantity controls, remove controls, return/update actions, summary, and coupon area. Use API-backed names, selected options, images, and monetary values.
- Preserve the desktop visual hierarchy and style. Additional empty/error/unsaved states follow the declared project behavior; no separate mobile design is asserted.
- Provide accessible names for remove and quantity buttons using the product/configuration. Show textual availability feedback and disabled-action explanations.
- For an available line, minus stops at 1 and plus stops at maxQuantity. For QUANTITY_EXCEEDED, allow minus to reduce the quantity toward the current limit; keep plus disabled until permitted. OUT_OF_STOCK and UNAVAILABLE quantities are not editable, but their lines remain removable.
- A missing image uses a placeholder without hiding the name or remove action. Null amounts display an em dash with an availability explanation, never $0.00.
- Coupon and checkout integration controls remain visibly scoped until their owning UCs exist. The return-to-shop and product-detail destinations are already defined by UC-04/UC-05.

### Frontend Logic and API Context

- Maintain a server cart snapshot and a separate draft of its remaining variant IDs and quantities. Mark the page dirty whenever the draft differs from the snapshot.
- GET initializes both snapshot and draft. Header count always follows persisted itemCount. On the product page, load the cart revision before allowing an add request; do not treat a failed load as an empty cart.
- POST sends the selected variant, quantity increment, and latest revision. Prevent overlapping mutations from the current view; show success only after a usable successful response.
- Quantity/remove controls update the draft. While dirty, calculate provisional line/subtotal displays using the loaded unit prices and label the summary `Unsaved changes`; these are not server-confirmed prices or quantities.
- UPDATE CART is enabled only for a changed draft with valid remaining quantities and no request in progress. An empty draft is valid. PUT sends the complete desired list with the snapshot revision.
- Successful mutation replaces both snapshot and draft with the returned cart. Clear dirty state and update the header count. No separate locally guessed success total is retained.
- Checkout stays disabled while loading, dirty, in error, ineligible, or not integrated. Refresh from GET before handing a clean cart to an integrated checkout; checkout independently revalidates its own quote.
- After a business conflict, reload the cart and explain that unsaved edits were discarded. Ignore older responses after navigation or a newer load; do not overwrite a current page with stale cart data.

### Validation and Error-Handling Context

- Validate request shape, UUIDs, integer quantities/revisions, list size, and duplicate variants. Enforce catalog availability and resulting quantities on the server, including when browser controls appeared to permit the action.
- Distinguish empty cart, unavailable line, out-of-stock line, insufficient quantity, stale revision, and service failure. A stale revision is not a generic invalid-input error.
- Never silently clamp a submitted quantity, delete an unavailable saved item, or substitute another variant. Require a deliberate corrected update/removal.
- Map validation messages to their request fields; show general business errors near the cart/add action. Service errors offer a manual reload instead of a fabricated empty state.
- For a read without a network response, show `Unable to connect. Please check your connection and try again.` A failed or malformed mutation response follows the uncertain-outcome recovery in E.5.
- Do not automatically retry additive POST requests. After uncertain mutation outcomes, a successful GET is required before any further mutation; the visitor reviews the stored result before deciding what to do next.
- Preserve editable drafts on explicit validation/service rejection, but replace them after the documented conflict reload or an uncertain-outcome reconciliation. Do not announce successful persistence until confirmed.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
