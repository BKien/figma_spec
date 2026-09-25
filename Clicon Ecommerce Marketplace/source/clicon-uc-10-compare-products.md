# UC-10: Compare Products

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Compare Products

Description:

- Allows a visitor or customer to save up to three selected product configurations for side-by-side comparison of customer feedback, price, seller, brand, model, stock status, size, and weight.
- Connects UC-05's Add to Compare control, shared Compare navigation, UC-06's cart operation, and UC-09's wishlist actions.
- Variant identity, capacity, persistence, missing-data rules, and API contracts are project decisions. Figma establishes the inspected desktop comparison table and controls.
- This UC does not recommend a winner, normalize incomparable measurements, create reviews, manage sellers, reserve stock, or create an order.

Primary Actor:

Visitor or signed-in Customer using the same browser context.

Preconditions:

- UC-04/UC-05 provide catalog identity, published variants, selected configuration, prices, availability, rating summaries, and product-detail routes.
- UC-06 and UC-09 provide their existing cart and wishlist APIs.
- `/compare` supports direct navigation and reload. No login session is required.
- Shared API envelopes and integer USD-cent monetary units apply.

Postconditions:

- Success: The requested configuration is included or removed, and the comparison table reflects confirmed server membership with coherent current catalog values.
- Failure: A rejected membership operation leaves the saved comparison unchanged; the frontend does not report an unconfirmed addition/removal as successful.
- Cart/wishlist actions affect only their owning resource. Removing a comparison column does not remove cart or wishlist entries.
- Comparison does not change inventory, prices, ratings, payment, or orders.

Main Flow:

1. The visitor selects a valid configuration on UC-05 and selects `Add to Compare`.
2. The frontend requests `PUT /api/v1/comparison/items/:variantId`.
3. The backend ensures that the selected variant is included once, subject to the three-configuration limit, and returns confirmed membership.
4. The frontend displays `Added to comparison.` and offers `View comparison` linking to `/compare`.
5. The visitor opens `/compare` through that link or shared Compare navigation.
6. The frontend loads `GET /api/v1/comparison` and renders the selected configuration columns against the shared row labels.
7. The visitor reads the comparison, opens a configuration's details, adds one available unit to the cart, changes wishlist membership, or removes a column.
8. Removing a column sends DELETE for that variant. Confirmed success removes only that column; remaining columns retain their relative order.

Alternative Flow:

A.1 — Empty or partial selection

- An empty selection displays `No products to compare.` and `Browse products` linking to `/shop`.
- One configuration remains viewable with `Add another product to compare.` Two configurations can be compared without requiring a third.
- Render the label column and actual selected columns; do not invent empty product records or duplicate an existing product to fill the frame.

A.2 — Duplicate configuration or full comparison

- Repeated PUT for an already included variant succeeds without duplication or reordering, including when all three slots are occupied.
- Different configurations of the same product are permitted and consume separate slots. Show their option values beneath the product name.
- A fourth distinct configuration returns HTTP 409 `COMPARISON_LIMIT_REACHED`. Keep all current selections; require the visitor to remove one deliberately before adding another.

A.3 — Different categories and missing attributes

- Cross-category comparison is permitted, as illustrated by the source frame. Fixed comparison rows remain in the same order across columns.
- Unknown/not-applicable seller, model, size, or weight displays an em dash. Do not infer a phone-sized display for a keyboard or manufacture missing dimensions from sample text.
- The table presents supplied values without claiming that unlike measurements are equivalent. No unit conversion, best-value highlighting, or automatic ranking is introduced.

A.4 — Add to cart or wishlist

- For an IN_STOCK configuration, read UC-06's cart and add quantity 1 with its current expectedRevision. Use the returned cart count and offer `/cart`; keep the comparison selection unchanged.
- The heart reflects membership of that exact variant in UC-09. PUT saves it and DELETE removes it using the existing wishlist contracts. A published out-of-stock variant can still be wishlisted under UC-09.
- Load wishlist membership before enabling hearts. Wishlist failure does not prevent viewing comparison data or removing comparison columns.
- For UNAVAILABLE entries, disable product navigation, cart, and wishlist controls in this table. Removal from comparison remains available; existing wishlist membership can still be managed through `/wishlist`.

A.5 — Persistence and independent membership

- The browser comparison persists for seven days after each successful PUT/DELETE, including duplicate adds and absent removals. Reads do not extend expiry.
- Sign-in/out, account-session expiry, cart checkout, and wishlist changes do not replace or clear it. Other browsers have separate selections; no account merging or cross-device synchronization is included.
- Expiry or loss of browser identification starts an empty comparison. Capacity and membership are independent of cart/wishlist capacity.
- Single-entry operations preserve unrelated entries. Concurrent operations on one variant resolve to the last successfully processed desired state; the three-entry limit still holds under competing additions.

Exception Flow:

E.1 — Unavailable configuration

- A new addition requires a published product and variant; otherwise return HTTP 404 `VARIANT_NOT_FOUND`. Published out-of-stock variants may be added.
- A previously selected variant that becomes unavailable remains as an UNAVAILABLE column with last-known identity/options/image. Disable its actionable catalog links and keep its remove control.
- Duplicate PUT still confirms an existing selection even if its variant later became unavailable. DELETE succeeds for absent variants and does not require catalog access.

E.2 — Price or stock changes

- Reads use current published catalog prices and availability. These values are snapshots, not a reservation or a guarantee that cart addition will succeed.
- Cart addition reuses UC-06's current stock, quantity, capacity, and revision checks. Show a rejection without silently substituting a variant or reducing quantity.

E.3 — Dependency or service failure

- Catalog failure returns CATALOG_UNAVAILABLE; comparison-store failure returns COMPARISON_UNAVAILABLE. Neither is represented as an empty comparison or universal out-of-stock status.
- Wishlist/cart errors retain their owning endpoint's contract. A successful comparison load must not be discarded merely because another resource cannot be loaded.

E.4 — Uncertain mutation result

- When a mutation has no usable response, show feedback and read the affected resource before allowing another mutation on it.
- Comparison uncertainty is reconciled with GET comparison; wishlist uncertainty with GET wishlist; cart uncertainty follows UC-06's GET cart reconciliation. Never automatically replay an additive cart request.
- If reconciliation fails, keep the affected controls disabled with a retry action. Do not announce success from a locally removed column or toggled heart alone.

UI Integration:

- Source: `11_Compare`, node `493:14714`.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=493-14714
- Live design context and its rendered screenshot were inspected on 2026-09-18. This establishes the desktop table and controls, not a frozen dataset, responsive layouts, persistence behavior, or unseen error/empty states.

| Observed element | Integration |
| --- | --- |
| Three product columns, each with circled X | Up to three selected variants and individual removal |
| Product image and name | Current published identity, or retained unavailable identity |
| ADD TO CARD and cart icon | Add one unit through UC-06 |
| Heart beside the cart action | Exact-variant wishlist save/remove through UC-09 |
| Customer feedback | Product-level ratingAverage and reviewCount |
| Price | Selected-variant unit price |
| Sold by / Brand / Model | Catalog seller, brand, and selected-variant model |
| Stock status | IN STOCK / OUT OF STOCK / supplementary UNAVAILABLE |
| Size / Weight | Selected-variant size and weight display values |
| Header/footer Compare navigation | Open `/compare` |

- Reuse the Clicon shell, Public Sans, bordered comparison grid, alternating pale-gray rows, orange actions (#FA8232), blue prices (#2DA5F3), and green/red stock labels. Preserve source label `ADD TO CARD` consistently with previous UCs.
- Row order follows the rendered frame: Customer feedback, Price, Sold by, Brand, Model, Stock status, Size, Weight. Use semantic row/column headers so values remain associated with the correct configuration.
- The source contains inconsistent sample names, images, specifications, and extremely large feedback counts. Populate coherent catalog records; do not infer business data from those examples.
- The source grays the out-of-stock column's heart as well as its cart action. This project's heart remains enabled for a published out-of-stock variant, consistent with UC-09. The cart action stays disabled.
- Show selected configuration options beneath titles as a project supplement. Empty/partial selection hints, saved-heart states, and loading/error feedback are also supplements.
- On UC-05, show `Remove from Compare` when the selected variant is included. Cards without explicit variant selection go to product details before adding, rather than silently selecting a configuration.
- No sort, bulk-clear, differences-only filter, additional product-picker modal, or comparison count badge is introduced. Responsive presentation is an implementation adaptation, not a verified mobile frame.

API Endpoint:

| Method and path | Purpose |
| --- | --- |
| `GET /api/v1/comparison` | Read selected variants and comparison attributes |
| `PUT /api/v1/comparison/items/:variantId` | Ensure the exact configuration is included |
| `DELETE /api/v1/comparison/items/:variantId` | Ensure it is absent |

Cart and wishlist actions reuse UC-06/UC-09 endpoints unchanged.

Request Body:

- Comparison endpoints have no body or query parameters; reject supplied bodies/query parameters. PUT/DELETE require a UUID variantId path parameter.
- Resolve the list through the browser context. Do not accept an account ID, list ID, client price, stock status, or attribute values as comparison inputs.
- Cart addition uses UC-06's body with the selected variantId, quantity 1, and latest expectedRevision. Wishlist PUT/DELETE uses that same variantId with no body, as defined by UC-09.

Successful Response:

Comparison read — HTTP 200:

```json
{
  "success": true,
  "message": "Comparison retrieved.",
  "data": {
    "comparison": {
      "itemCount": 1,
      "items": [{
        "variantId": "5c69ff67-1c39-41e3-982f-51ec2016da71",
        "productId": "c168f6e8-a7e4-4efc-b278-2f96da050e8f",
        "slug": "macbook-pro-14",
        "name": "Apple MacBook Pro 14-inch",
        "options": {"color": "Space Gray", "size": "14-inch", "memory": "16GB", "storage": "512GB SSD"},
        "imageUrl": "/images/products/macbook-pro-14-front.png",
        "currency": "USD",
        "price": 169900,
        "status": "IN_STOCK",
        "ratingAverage": 4.7,
        "reviewCount": 21671,
        "sellerName": "Clicon",
        "brandName": "Apple",
        "model": null,
        "size": "14-inch",
        "weight": null
      }]
    }
  }
}
```

- All shown keys are required. Examples illustrate the contract; actual catalog records supply the values. itemCount equals items.length, from 0 to 3. Each variant is unique.
- Items use first-added order, oldest first. Duplicate additions preserve position; remove then re-add places a configuration at the end.
- UUIDs, slug, options, and image selection reuse UC-05. Each option is a nonempty string or null; imageUrl is a string or null. An unavailable entry retains last-known identity, options, and image for recognition/removal.
- status is IN_STOCK, OUT_OF_STOCK, or UNAVAILABLE. Missing/unpublished product or variant takes precedence as UNAVAILABLE; otherwise use UC-05's availability.
- For published variants, price is current nonnegative integer USD cents; ratingAverage is 0–5 or null if reviewCount is zero; reviewCount is a nonnegative integer. Ratings describe the product across variants, consistently with UC-04/UC-05.
- sellerName is a nonempty catalog seller display string or null, never inferred from brandName. brandName is the product's catalog brand name. model, size, and weight are nonempty display strings or null.
- size equals the selected variant's options.size when present; otherwise null. model and weight use optional structured catalog comparison attributes. Weight includes its supplied unit; do not parse arbitrary product-name text or silently convert units. If the same attributes appear in UC-05 specifications, their values must agree.
- UNAVAILABLE entries have null price, ratingAverage, reviewCount, sellerName, brandName, model, size, and weight. Show an em dash for unknown values instead of stale attributes presented as current.
- Published products with zero reviews show `No reviews yet.` Missing optional attributes do not fail the entire comparison. Catalog-service failure is a service error, not an unavailable-product conclusion.

Add — HTTP 200:

```json
{
  "success": true,
  "message": "Added to comparison.",
  "data": {
    "variantId": "5c69ff67-1c39-41e3-982f-51ec2016da71",
    "included": true,
    "itemCount": 1
  }
}
```

Remove — HTTP 200:

```json
{
  "success": true,
  "message": "Removed from comparison.",
  "data": {
    "variantId": "5c69ff67-1c39-41e3-982f-51ec2016da71",
    "included": false,
    "itemCount": 0
  }
}
```

- Mutation responses confirm membership and persisted count at completion, without requiring a catalog read for every other column. Duplicate additions and absent removals use the same respective successful contracts.
- Cart/wishlist responses remain their existing contracts. Comparison itemCount counts configurations; cart itemCount sums quantities; do not interchange them.

Error Response:

Use the shared envelope, with no data field. timestamp is server-generated ISO 8601 UTC; path is the actual endpoint pathname without its query string.

```json
{
  "success": false,
  "statusCode": 409,
  "code": "COMPARISON_LIMIT_REACHED",
  "message": "You can compare at most 3 product configurations. Remove one before adding another.",
  "timestamp": "2026-09-18T10:00:00.000Z",
  "path": "/api/v1/comparison/items/5c69ff67-1c39-41e3-982f-51ec2016da71"
}
```

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | `Please correct the highlighted fields.` |
| 404 | VARIANT_NOT_FOUND | `This product configuration is not available.` |
| 409 | COMPARISON_LIMIT_REACHED | `You can compare at most 3 product configurations. Remove one before adding another.` |
| 503 | CATALOG_UNAVAILABLE | `The product catalog is temporarily unavailable. Please try again later.` |
| 503 | COMPARISON_UNAVAILABLE | `Product comparison is temporarily unavailable. Please try again later.` |
| 500 | INTERNAL_ERROR | `Unable to complete your request. Please try again later.` |

- Optional errors is limited to VALIDATION_ERROR and maps field names such as variantId to nonempty message arrays. Body-level errors may omit it.
- Missing comparison identity returns an empty list. DELETE of an absent variant succeeds. Cart/wishlist errors keep their original codes, messages, and endpoint paths.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement the comparison endpoints in NestJS using existing catalog identity, browser context, and API envelopes.

- Store ordered variant membership, expiry, and last-known display identity. Keep comparison independent of account sessions, carts, wishlists, and orders.
- Preserve explicit include/remove behavior, uniqueness, and the three-entry maximum under concurrent additions. Single-entry mutations cannot overwrite unrelated selections.
- New additions validate publication; duplicate includes and absent removals do not require catalog access. Empty GET can succeed without catalog retrieval.
- Project current prices, product ratings/brand, selected-variant size, and optional seller/model/weight fields. Add those optional catalog attributes without changing UC-05's existing response shape or inventing a seller-management subsystem.
- Missing optional fields remain null. Missing/unpublished variants remain removable with retained identity. Catalog failure returns a service error rather than manufactured column values.
- Do not implement duplicate cart/wishlist logic. Their APIs remain responsible for their own stock, capacity, persistence, and mutation rules.

### Frontend UI Context

Build `ComparePage` at `/compare` in React, TypeScript, and Tailwind CSS using the inspected desktop frame.

- Render a row-label column and one column per saved configuration, with shared row alignment, alternating backgrounds, observed images/actions, and current data.
- Label remove, cart, and wishlist controls with the relevant product/configuration. Use text in addition to stock color and expose saved-heart state accessibly.
- Preserve the readable matrix when values wrap; do not mix rows across columns. Unknown attributes use an em dash; no-rating feedback is distinct from unavailable rating data.
- Wire product links to `/products/:slug?variant=<variantId>`. Disable catalog actions for unavailable entries while retaining remove.
- Keep empty/partial hints and service recovery within the shared shell. Do not introduce additional comparison features or claim unobserved mobile designs.

### Frontend Logic and API Context

- Load comparison membership/data on route entry and for UC-05's selected-variant comparison control. Load wishlist membership independently for the comparison hearts.
- Disable each resource's mutation controls until its membership is known. A wishlist-loading failure does not disable comparison removal or otherwise valid cart actions.
- Capture variantId when an action is clicked. A delayed response must not change the indicator for another newly selected configuration.
- Confirm comparison PUT/DELETE before updating membership, then refresh the complete table. Serialize comparison mutations in the current view and ignore obsolete load responses.
- After a confirmed mutation followed by a failed refresh, distinguish `saved change, refresh failed` from a rejected mutation; retain the confirmed membership and offer refresh.
- Add to cart only after reading the latest cart revision, using quantity 1. Wishlist actions reuse UC-09. Neither operation removes or reorders comparison columns.
- Refresh comparison when reopening the page to observe external changes. No polling, automatic cross-tab sync, or ranking calculation is required.

### Validation and Error-Handling Context

- Validate UUIDs and request shape on the server; distinguish publication eligibility for new additions from stock eligibility for cart actions.
- Never automatically evict a column when full, silently substitute a variant, fabricate missing attributes, or present failed catalog reads as empty/unavailable selections.
- For no HTTP response, display `Unable to connect. Please check your connection and try again.` Reconcile uncertain mutations through the correct resource before further actions on it.
- A malformed comparison response displays `Unable to load product comparison. Please try again.` Keep previously confirmed data visibly stale rather than presenting fabricated current prices.
- Image failure uses a neutral placeholder while retaining identity and allowed actions. Missing model/weight is normal optional data, not a network failure.
- Cart failures follow UC-06's recovery without automatic additive retries. Wishlist failures follow UC-09 without changing comparison membership.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
