# UC-09: Manage Wishlist

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Manage Wishlist

Description:

- Allows a visitor or customer to save selected product configurations, view their current prices and stock status, remove saved configurations, and add an available saved configuration to the shopping cart.
- Connects UC-05's Add to Wishlist action, the shared Wishlist navigation, and UC-06's existing cart API.
- Variant-level identity, browser persistence, limits, API contracts, and interaction behavior below are project decisions. Figma establishes the inspected desktop list and visible actions.
- This UC does not create orders, reserve inventory, send stock/price notifications, share wishlists, or synchronize lists across accounts/devices.

Primary Actor:

Visitor or signed-in Customer using the same browser context.

Preconditions:

- UC-05 provides published products, selected variant IDs, option values, prices, images, and availability.
- UC-06 provides cart read/add operations and the existing `/cart` route. `/shop` and `/products/:slug` are available from UC-04/UC-05.
- `/wishlist` supports direct navigation and reload. Login is not required.
- Shared API envelopes and integer USD-cent monetary units apply.

Postconditions:

- Success: The requested variant is saved or removed, and the visible list reflects the confirmed server state. Each variant appears at most once.
- Cart success: UC-06 adds one unit of the selected saved variant and returns its updated cart. The wishlist entry remains saved.
- Failure: A rejected wishlist mutation leaves stored membership unchanged. A failed cart action does not remove its wishlist entry.
- Saving/removing a wishlist entry does not change inventory, cart contents, payment, or orders.

Main Flow:

1. On UC-05, the visitor selects a valid published product configuration and selects `Add to Wishlist`.
2. The frontend requests `PUT /api/v1/wishlist/items/:variantId` for that selected variant.
3. The backend ensures that the variant is present once in the current browser wishlist and returns its saved state and membership count.
4. The frontend displays `Saved to wishlist.` and updates that configuration's saved indicator.
5. The visitor opens `/wishlist` through the shared header heart icon or footer Wishlist link.
6. The frontend requests `GET /api/v1/wishlist` and renders the returned products, selected options, current prices, stock status, and actions.
7. The visitor may open a product's saved configuration, add one available unit to the cart, or remove an entry.
8. Removing an entry sends DELETE for that variant; only confirmed success removes it from the visible list. There is no separate Update Wishlist action.

Alternative Flow:

A.1 — Save a duplicate or another configuration

- Repeating PUT for an already saved variant succeeds without adding a duplicate or changing its list position.
- Different variants of the same product are separate entries. Show their option values so they can be distinguished.
- A published out-of-stock variant can be saved. An invalid option combination cannot be saved because it has no selected variant ID.

A.2 — Empty wishlist

- A browser without a wishlist receives an empty list with itemCount 0. Display `Your wishlist is empty.` and `Browse products` linking to `/shop`.
- Removing the final entry produces the same empty state; a failed load must not be rendered as an empty list.

A.3 — Add a saved variant to the cart

- For an IN_STOCK line, first read the current cart using UC-06, then submit its `POST /api/v1/cart/items` with this variantId, quantity 1, and the returned expectedRevision.
- UC-06 determines whether the resulting cart quantity is permitted. Wishlist stock status alone does not establish available capacity for another cart unit.
- Confirm success only from the cart response; update the shared cart count and offer `View cart` linking to `/cart`.
- Keep the wishlist entry, including after a successful order. This is Add to Cart, not Move to Cart.

A.4 — Open product details

- A published saved variant links to `/products/:slug?variant=<variantId>` using its current slug. Never open a different default variant silently.
- On the detail page, changing configuration changes which variant's saved state is displayed. Removing one configuration does not remove other configurations of the same product.

A.5 — Persistence and concurrent actions

- The browser wishlist persists for seven days after a successful PUT or DELETE, including an accepted duplicate save or already-absent removal. Reads do not extend this period.
- Expiry returns an empty wishlist. Sign-in, sign-out, account-session expiry, cart expiry, and checkout completion do not transfer or clear it. Clearing its browser identification data or using another browser starts a separate list.
- Operations affect one variant at a time. Saving/removing different variants must not replace the entire list or erase unrelated entries. For competing operations on the same variant, the last successfully processed operation determines membership.

Exception Flow:

E.1 — Saved variant becomes unavailable

- An unavailable saved product/variant remains listed as UNAVAILABLE, with its last-known name, options, and image. Its price is unknown, its product link and cart action are disabled, and removal remains available.
- A published out-of-stock variant remains viewable with its current price, an OUT OF STOCK label, and disabled cart action.
- Do not replace unavailable variants, automatically remove entries, or invent a current price.

E.2 — Save unavailable variant or exceed capacity

- Saving a variant not already in the list requires a currently published product and variant; otherwise return HTTP 404 `VARIANT_NOT_FOUND`.
- A wishlist holds at most 50 distinct variants, including unavailable saved entries. A new entry exceeding this count returns HTTP 409 `WISHLIST_LIMIT_REACHED`.
- Ensuring an already saved entry succeeds even if the list is full or the variant subsequently becomes unavailable. No duplicate is inserted.

E.3 — Removal already completed

- Removing an absent variant succeeds with saved false. Removing unavailable products does not require a working catalog lookup.
- Other entries and the cart remain unchanged.

E.4 — Cart rejection

- UC-06's CART_CHANGED, QUANTITY_UNAVAILABLE, CART_LIMIT_REACHED, VARIANT_NOT_FOUND, and service errors retain their existing envelopes and meanings.
- Show feedback beside the cart action and refresh the relevant cart/wishlist data. Do not silently reduce quantity, delete the saved entry, or automatically repeat an additive cart request.
- If the cart mutation outcome is unknown, follow UC-06's reconciliation through a cart read before allowing another add.

E.5 — Wishlist service or network failure

- Explicit mutation rejection leaves the displayed membership unchanged and shows feedback. A missing/unusable mutation response leaves its outcome uncertain.
- Re-read the wishlist to reconcile uncertain membership before another action on it. Do not claim success from a locally toggled heart alone.
- If reconciliation fails, show a retry action and keep membership controls disabled until the state can be loaded. No error is converted into a fabricated empty list.

UI Integration:

- Source: `12_Wishlist`, node `418:11632`.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=418-11632
- Live design context and its rendered screenshot were inspected on 2026-09-18. This establishes the desktop Wishlist frame; it does not establish a frozen dataset, responsive frames, persistence behavior, or unseen error/empty states.

| Observed element | Integration |
| --- | --- |
| Wishlist title and breadcrumb | `/wishlist` route within the shared shell |
| PRODUCTS column; image and title | Saved variant's product identity and selected configuration |
| PRICE; optional crossed-out price | Current unit price and comparison price |
| STOCK STATUS | IN STOCK, OUT OF STOCK, or supplementary UNAVAILABLE state |
| Orange ADD TO CARD action with cart icon | Add exactly one saved variant unit through UC-06 |
| Gray ADD TO CARD on out-of-stock row | Disabled cart action |
| Circled X on each row | Immediate remove request, confirmed by server |
| Header heart and footer Wishlist | Navigate to `/wishlist` |

- Preserve the table layout, shared Clicon header/footer, Public Sans, orange actions (#FA8232), green stock text (#2DB224), red out-of-stock text (#EE5858), gray disabled action (#ADB7BC), and light borders (#E4E7E9).
- Retain the source's `ADD TO CARD` label for consistency with UC-05/UC-06. It invokes the shopping cart operation, not payment-card collection.
- Display configuration values beneath product names as a project supplement. Source sample images/names/prices are illustrative; use coherent catalog records instead of reproducing their mismatched identities.
- Show a neutral image placeholder when necessary. UNAVAILABLE prices display an em dash with explanatory text, never a fabricated $0.00.
- Connect UC-05's Add to Wishlist control. When already saved, show `Remove from Wishlist`; changing the selected configuration recomputes this state. These saved/pending states are project supplements.
- UC-04 cards without an explicit complete variant selection navigate to product details before saving; do not silently choose a variant. No wishlist quantity selector, bulk removal, sorting, or pagination is introduced.
- Empty, pending, unavailable, and error feedback are project supplements styled consistently with the source. Do not add a wishlist count badge that is not shown in this frame; itemCount supports state consistency and the empty state.

API Endpoint:

| Method and path | Purpose |
| --- | --- |
| `GET /api/v1/wishlist` | Read all saved entries with current catalog display data |
| `PUT /api/v1/wishlist/items/:variantId` | Ensure one selected variant is saved |
| `DELETE /api/v1/wishlist/items/:variantId` | Ensure the selected variant is absent |

Cart integration reuses UC-06's `GET /api/v1/cart` and `POST /api/v1/cart/items` unchanged; no new wishlist-to-cart endpoint is introduced.

Request Body:

- Wishlist endpoints have no request body or query parameters; reject supplied bodies and unknown query parameters. PUT/DELETE require a UUID variantId in the path.
- The browser context identifies the wishlist. No account ID, list ID, price, stock value, or product ID is accepted as an ownership/identity override.
- PUT means saved=true and DELETE means saved=false; there is no ambiguous toggle request.

Cart addition uses the existing UC-06 body:

```json
{
  "variantId": "5c69ff67-1c39-41e3-982f-51ec2016da71",
  "quantity": 1,
  "expectedRevision": 2
}
```

Successful Response:

Wishlist read — HTTP 200:

```json
{
  "success": true,
  "message": "Wishlist retrieved.",
  "data": {
    "wishlist": {
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
        "compareAtPrice": 199900,
        "status": "IN_STOCK"
      }]
    }
  }
}
```

- All shown keys are required. IDs are UUIDs; example records and image paths must be supplied by actual catalog data.
- itemCount equals items.length, from 0 to 50; variants are unique. Items are ordered by first save, oldest first. Repeated save preserves position; removing and later saving creates a new position at the end.
- options uses UC-05's color/size/memory/storage keys, each a nonempty string or null. imageUrl is the first effective variant/product image under UC-05's fallback rule, or null.
- status is IN_STOCK, OUT_OF_STOCK, or UNAVAILABLE. Missing/unpublished product or variant takes precedence as UNAVAILABLE; otherwise UC-05's availability determines the stock label.
- Published variants have current nonnegative integer USD-cent price and a compareAtPrice that is null or greater than price. Prices are snapshots, not a future cart-price guarantee.
- UNAVAILABLE entries retain last-known productId, slug, name, options, and imageUrl for display/removal; price and compareAtPrice are null. The retained slug is not an enabled navigation destination.
- Catalog failure is not proof of unavailability. Return a service error instead of relabeling every item unavailable. Empty lists can be returned without catalog access.

Wishlist save — HTTP 200:

```json
{
  "success": true,
  "message": "Saved to wishlist.",
  "data": {
    "variantId": "5c69ff67-1c39-41e3-982f-51ec2016da71",
    "saved": true,
    "itemCount": 1
  }
}
```

Wishlist removal — HTTP 200:

```json
{
  "success": true,
  "message": "Removed from wishlist.",
  "data": {
    "variantId": "5c69ff67-1c39-41e3-982f-51ec2016da71",
    "saved": false,
    "itemCount": 0
  }
}
```

- Mutation responses confirm membership only, so removal/duplicate-save do not depend on retrieving catalog display data for every entry. itemCount is the persisted list size at completion.
- Successful cart addition returns the complete `data.cart` schema and `Added to cart.` message already defined by UC-06, including its updated revision and persisted itemCount. Wishlist itemCount and cart itemCount have different meanings and must not be interchanged.

Error Response:

Use the shared envelope. Errors omit data; timestamp is generated in UTC; path is the actual endpoint pathname without query parameters.

```json
{
  "success": false,
  "statusCode": 409,
  "code": "WISHLIST_LIMIT_REACHED",
  "message": "Your wishlist can contain at most 50 product configurations.",
  "timestamp": "2026-09-18T10:00:00.000Z",
  "path": "/api/v1/wishlist/items/5c69ff67-1c39-41e3-982f-51ec2016da71"
}
```

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | `Please correct the highlighted fields.` |
| 404 | VARIANT_NOT_FOUND | `This product configuration is not available.` |
| 409 | WISHLIST_LIMIT_REACHED | `Your wishlist can contain at most 50 product configurations.` |
| 503 | CATALOG_UNAVAILABLE | `The product catalog is temporarily unavailable. Please try again later.` |
| 503 | WISHLIST_UNAVAILABLE | `Your wishlist is temporarily unavailable. Please try again later.` |
| 500 | INTERNAL_ERROR | `Unable to complete your request. Please try again later.` |

- Optional errors appears only for VALIDATION_ERROR and maps field names, such as variantId, to nonempty arrays of strings; body-level validation may omit it.
- A missing wishlist is a successful empty list, not a login error. Unknown/absent variants on DELETE are successful absence confirmation, not VARIANT_NOT_FOUND.
- UC-06 errors from cart requests retain their cart endpoint path and contract; do not relabel a cart error as wishlist-save failure.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement the three wishlist endpoints in NestJS, reusing the project's browser context, catalog identity, and response envelopes.

- Persist browser-scoped membership, first-save order, expiry, and last-known display identity for retained unavailable entries. Keep wishlist lifetime separate from cart and account-session lifetimes.
- Resolve exact variants rather than merging all configurations of a product. Permit published out-of-stock configurations to be saved.
- Enforce duplicate-free membership and the 50-entry limit under concurrent saves. Single-entry mutations preserve unrelated variants; PUT/DELETE expose explicit desired states.
- Ensure duplicate saves and absent removals return the documented successful state. They do not require catalog retrieval. New saves validate publication before adding the entry.
- Resolve current display prices/availability on GET; retain unavailable entries as documented. A read does not extend wishlist expiry or mutate cart/inventory.
- Cart addition is the existing UC-06 business operation. Do not implement a second cart store, bypass its quantity/revision rules, or automatically remove saved entries after cart/order success.

### Frontend UI Context

Build `WishlistPage` at `/wishlist` in React, TypeScript, and Tailwind CSS from the inspected frame.

- Render Products, Price, Stock Status, and Actions columns with variant-aware data. Show crossed-out prices only when compareAtPrice is present.
- Preserve the observed disabled out-of-stock cart action. Unavailable entries remain removable while product navigation/cart actions are disabled.
- Provide accessible product/configuration names for remove and add-to-cart buttons. Stock feedback uses text as well as color.
- Connect shared heart/footer navigation and UC-05's selected-variant save/remove control. Do not pretend the selected variant is unsaved while its membership load has failed or is still pending.
- Show empty, loading, and retry states; these are project supplements, not additional verified Figma frames. No mobile layout is asserted from the inspected desktop frame.

### Frontend Logic and API Context

- Load the wishlist on route entry and when initializing UC-05's save control. Use returned variant IDs for membership, not product names or current cart contents.
- Disable membership actions until the initial lookup succeeds. On detail variant changes, derive the new variant's saved state from the loaded list; no valid selection means no enabled save action.
- PUT/DELETE applies to the variant captured when clicked. Do not let a delayed response mark a different, newly selected variant as saved/removed.
- Wait for mutation confirmation before changing displayed membership. Disable overlapping membership mutations in the current view, then refresh the list to reconcile its complete state. A refresh failure after confirmed mutation is reported as a refresh problem, not as a rejected mutation.
- Refresh on page re-entry to observe changes from another tab; no live cross-tab synchronization is required. Ignore responses older than the most recently started applicable load/mutation.
- For Add to Cart, obtain the current cart revision and submit quantity 1 to UC-06. Disable overlapping cart additions and use the returned cart count. Wishlist membership remains unchanged.
- After uncertain outcomes, reconcile the affected resource: GET wishlist for membership and GET cart for cart additions. Do not automatically resend additive cart requests.

### Validation and Error-Handling Context

- Validate UUID path parameters and absence of unsupported body/query inputs. Current catalog publication determines whether a new entry may be saved; stock availability determines the separate cart action.
- Distinguish OUT_OF_STOCK, UNAVAILABLE, catalog outage, full wishlist, and full/changed cart. A stock label cannot guarantee that an addition will fit the existing cart quantity limit.
- Never silently replace variants, clamp cart quantities, clear the wishlist on checkout, or treat a failed read as confirmed empty state.
- No HTTP response shows `Unable to connect. Please check your connection and try again.` If it followed a mutation, reconcile state before further membership changes or additive cart actions.
- Malformed read data shows `Unable to load your wishlist. Please try again.` Preserve valid previously confirmed state as stale; do not fabricate prices, stock labels, or success feedback.
- Image failure uses a neutral placeholder while preserving readable identity, status, and permitted actions. Removal must remain possible for unavailable entries and does not require purchasing eligibility.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
