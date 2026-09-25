# UC-14: View and Manage Browsing History

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

View Browsing History and Control Recording

Description:

- Allows an authenticated customer to revisit previously viewed products, search/filter their history, load older entries, and enable or disable future recording.
- Connects successful product-detail viewing in UC-05 with the account Browsing History page.
- Recording scope, retention, grouping, filtering, pagination, and API contracts below are project decisions. Figma establishes the inspected desktop controls and dated product groups.
- This UC does not track guests, collect external browser history, recommend products, record cart actions, or implement individual/bulk history deletion.

Primary Actor:

Signed-in Customer with an active, verified account.

Preconditions:

- UC-02 supplies the authenticated account and session; UC-05 supplies successful product-detail views and shared product identity.
- `/account/browsing-history` supports direct navigation and reload within the existing account shell.
- UC-04's product-card contract, USD-cent monetary units, and shared response envelopes apply.

Postconditions:

- Success: The customer sees their matching saved product-view entries and may revisit a product through its existing detail route.
- Recording success: An eligible product view creates or updates the current day's entry for that product/account.
- Preference success: The persisted enabled value controls subsequent recording. Disabling preserves existing retained entries; enabling does not backfill views that occurred while disabled.
- Failure: A failed history operation does not prevent public product browsing or modify cart, wishlist, comparison, inventory, profile, or orders.

Main Flow:

1. A signed-in customer successfully opens a published product through UC-05.
2. After rendering the successful product detail, the frontend submits a separate history-record request for its product ID. The product GET itself remains read-only.
3. The backend resolves the current account and recording preference. When enabled, it creates or updates the product's entry for the current UTC date.
4. The customer selects Browsing History in the account sidebar, opening `/account/browsing-history`.
5. The frontend reads the first history page and displays the persisted recording switch, search/date controls, and product cards grouped by view date.
6. The customer may submit a search term, choose a date, load more matching entries, or open a product card.
7. The customer may change the recording switch. The frontend confirms the preference through the server before displaying the new persisted state.

Alternative Flow:

A.1 — First use, empty history, or no matches

- A new account has recording enabled and an empty history. Display `You have no browsing history yet.` with `Browse products` linking to `/shop`.
- A filter with zero matches displays `No browsing history matches your filters.` with an action to clear filters. Do not treat it as a missing account or service failure.
- Disabled recording with an empty history displays `Browsing history is off. Turn it on to save future product views.`

A.2 — Repeated views and grouping

- Store at most one entry per account, product ID, and UTC calendar date. A repeated successful view on the same date updates lastViewedAt and moves that entry to the newest position within the date group.
- The same product viewed on a later date appears in that date's group as well. Variant changes within the same loaded product do not create another record request; history is product-level, not configuration-level.
- Record once per successful product-route visit, including a deliberate reload or navigation back to that product. Re-renders, image changes, tab changes, prefetches, and opening history itself are not product visits.

A.3 — Recording off

- The switch controls only future recording. Existing entries remain searchable/viewable until normal expiry or capacity removal.
- The server checks the persisted preference when processing a record request. A view processed while disabled returns recorded=false and creates no entry. A record already completed before disabling remains present.
- A later enable does not retrospectively record earlier visits. No hidden queue of guest/offline/disabled views is replayed.

A.4 — Search, date, and older entries

- Search matches the saved product-name snapshot using a case-insensitive literal substring; it is not fuzzy matching, a regex, or a catalog-wide search.
- The date filter selects exactly one UTC calendar date. Search and date conditions combine with AND.
- Submit search on Enter or the search control; a date selection applies immediately. Changing either filter resets pagination to page 1. Clearing both restores all retained history.
- LOAD MORE appends the next page, merging adjacent entries into existing date headings. It does not duplicate the same date heading merely because a group spans pages.

A.5 — Revisit a product

- A published card opens `/products/:slug` using the current slug and UC-05's default configuration. History does not restore a past selected variant or quantity.
- A successful revisit may update today's history under A.2. Browser Back reloads page 1 for the prior filters; it need not restore previously appended pages.

A.6 — Retention and capacity

- Retain today and the preceding 29 UTC calendar dates, capped at 200 product/day entries per account. Remove expired entries and, when over capacity, the oldest lastViewedAt entries first, with ascending entry ID as the tie-breaker.
- Reads do not extend retention. Sign-out, session expiry, and password changes do not delete retained history or reset the preference. Another authenticated session for the same account reads the same history.
- Guest browsing does not become account history after sign-in. History is independent of browser-scoped cart/wishlist/comparison ownership.

Exception Flow:

E.1 — Recording request fails

- A failed optional history write does not replace a successful UC-05 product page with an error or prevent purchase-related actions.
- Do not retry it automatically or queue it for another login. A later deliberate product visit may record normally.

E.2 — Authentication expired

- History endpoints return HTTP 401 UNAUTHENTICATED when the current session/account is ineligible.
- On the account history page, clear personal history and return to `/sign-in`. On the public product page, stop account-history recording and clear expired account state while leaving the product readable.

E.3 — Product removed or unavailable

- A new record requires an available public product detail under UC-05; otherwise return HTTP 404 PRODUCT_NOT_FOUND without recording.
- Retained entries for removed/unpublished products remain visible as unavailable with their last-known name/image and no current price or rating. Disable the product link; do not replace it with another product.
- Temporary catalog failure is a service error, not evidence that every product was removed.

E.4 — History changed between pages

- Load-more requests carry the revision from page 1. If recorded views, expiry, capacity removal, or preference changes advanced the history revision, return HTTP 409 HISTORY_CHANGED.
- Display `Your browsing history changed. Reload to see the latest entries.` Stop appending until the customer reloads page 1 with the same filters. Do not mix inconsistent pages.

E.5 — Preference result or service state unknown

- If a switch request has no usable response, keep its state marked unresolved and disable further toggles until a history read confirms the saved enabled value.
- A failed page read offers retry, not a fabricated empty list. A failed Load more retains already loaded entries with a page-level retry action.
- Missing/invalid response data shows `Unable to load browsing history. Please try again.` No guessed saved preference is shown as confirmed.

UI Integration:

- Source: `33_Dasboard_Browsing History`, node `478:12199`, desktop 1921 × 3632.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=478-12199
- Live frame metadata and design contexts/rendered screenshots of heading `478:14666`, filters `478:15664`, dated product group `478:13344`, and Load more `478:18242` were inspected on 2026-09-19. The full frame exceeded the tool context size; these focused reads establish the relevant controls. No complete frozen dataset, mobile design, or unseen feedback state is claimed.

| Observed element | Integration |
| --- | --- |
| Browsing History heading | Account history page |
| Turn Browsing History on/off switch | Persisted recording preference |
| Search in browsing history | q filter |
| DD/MM/YYYY date field | Single-date filter; API uses YYYY-MM-DD |
| Dated bordered groups | UTC view-date grouping |
| Product image/title, stars/count, price, badge | Shared product-card content with current catalog values |
| LOAD MORE | Append the next matching page |

- Reuse Clicon shell/sidebar, Public Sans, orange switch/actions, blue prices, light borders, and four-card desktop rows.
- Enable the existing Browsing History sidebar item at `/account/browsing-history`. Reuse already implemented account/shop destinations; do not enable unrelated Order History or payment-card routes here.
- Add a concise `Dates shown in UTC` label so date filtering/grouping does not imply the device's local calendar. The displayed DD/MM/YYYY date is converted explicitly to the API date format.
- Source product-name/image mismatches and historical example dates are sample content, not data rules. Use coherent product records; show unavailable cards and neutral missing-image placeholders as project supplements.
- No per-card remove icon or Clear history control is inferred. The inspected switch pauses recording; it is not a deletion action.
- Card links navigate to product details. No unobserved quick-add, hover purchase, or review-submission interaction is introduced by this UC.

API Endpoint:

| Method and path | Purpose |
| --- | --- |
| `GET /api/v1/account/browsing-history` | Read preference and a filtered history page |
| `PUT /api/v1/account/browsing-history/preference` | Set recording enabled or disabled |
| `POST /api/v1/account/browsing-history/views` | Record one successful product-route visit |

Request Body:

GET has no body; accepted query parameters:

| Parameter | Contract |
| --- | --- |
| q | Optional trimmed string, at most 100 Unicode code points; empty means no name filter |
| date | Optional valid YYYY-MM-DD calendar date; empty/malformed is invalid; outside retention returns no matches |
| page | Positive decimal integer, default 1; page size fixed at 20 |
| revision | Nonnegative decimal integer, required for page > 1; omitted for page 1 |

- Reject unknown/repeated query keys and body data on GET. A page beyond matching results returns an empty page with hasMore=false when its revision is valid.
- Page 1 accepts no revision parameter. Filters used for Load more must equal those of the loaded page sequence.

Preference PUT:

```json
{"enabled": false}
```

Record POST:

```json
{"productId": "c168f6e8-a7e4-4efc-b278-2f96da050e8f"}
```

- Exactly the shown required fields; enabled is a JSON boolean and productId is a UUID. Reject extra fields/query parameters. Do not accept account ID, client timestamps, variant ID, or product display data.
- The server resolves the account and view time. Preference operations set an explicit value rather than toggle an unknown state; for competing changes, the last successfully processed request determines enabled.

Successful Response:

History GET — HTTP 200:

```json
{
  "success": true,
  "message": "Browsing history retrieved.",
  "data": {
    "enabled": true,
    "revision": 4,
    "timeZone": "UTC",
    "page": 1,
    "pageSize": 20,
    "totalItems": 1,
    "hasMore": false,
    "entries": [{
      "id": "64a16373-c30e-4b41-8738-ab580d6ea875",
      "viewDate": "2026-09-19",
      "lastViewedAt": "2026-09-19T10:00:00.000Z",
      "productId": "c168f6e8-a7e4-4efc-b278-2f96da050e8f",
      "savedName": "Apple MacBook Pro 14-inch",
      "savedImageUrl": "/images/products/macbook-pro-14-front.png",
      "product": {
        "id": "c168f6e8-a7e4-4efc-b278-2f96da050e8f",
        "slug": "macbook-pro-14",
        "name": "Apple MacBook Pro 14-inch",
        "imageUrl": "/images/products/macbook-pro-14-front.png",
        "price": 169900,
        "compareAtPrice": 199900,
        "currency": "USD",
        "ratingAverage": 4.7,
        "reviewCount": 21671,
        "badge": null
      }
    }]
  }
}
```

- All keys are required. entries has at most 20 records, ordered by lastViewedAt descending, then id descending. id is an entry UUID; productId is shared catalog identity.
- viewDate is the UTC date of lastViewedAt. lastViewedAt is a server-generated ISO 8601 UTC timestamp. The same product/date retains its entry ID when viewed again.
- savedName is the product-name snapshot at its latest recorded view that day; savedImageUrl is that view's effective product-summary image or null. Search uses savedName even if the catalog name subsequently changes.
- product is the current UC-04 card summary with its exact existing field semantics, or null when the product is no longer publicly available under UC-05. Its prices/image use the current default variant, not a past variant selection. If null, show only retained name/image and an Unavailable label.
- totalItems counts all matching retained entries before pagination, not unique products across dates. hasMore is true exactly when page × pageSize < totalItems.
- revision starts at 0. Each successful recorded view and each actual preference change advances it by one. An expiry/capacity cleanup that changes the entry set also advances it; a repeated unchanged preference or skipped disabled view does not. Cleanup associated with a view may be included in that view's one revision advance.
- Apply expiry cleanup before checking a pagination revision. Return entries/count/revision from a consistent history state. Catalog display updates alone do not change history membership revision.

Preference PUT — HTTP 200:

```json
{
  "success": true,
  "message": "Browsing history preference saved.",
  "data": {"enabled": false, "revision": 5}
}
```

Record POST — HTTP 200:

```json
{
  "success": true,
  "message": "Product view processed.",
  "data": {"recorded": true}
}
```

- recorded is false when recording is disabled. For an authenticated, well-shaped request, check enabled before catalog lookup; disabled mode needs no catalog lookup or entry write.
- No record response means the frontend must not claim that the view was saved. Background recording does not require a user-facing success toast.

Error Response:

Use the shared envelope with no data; timestamp is server-generated UTC and path is the actual endpoint pathname, excluding query parameters.

```json
{
  "success": false,
  "statusCode": 409,
  "code": "HISTORY_CHANGED",
  "message": "Your browsing history changed. Reload to see the latest entries.",
  "timestamp": "2026-09-19T10:00:00.000Z",
  "path": "/api/v1/account/browsing-history"
}
```

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | `Please correct the highlighted fields.` |
| 401 | UNAUTHENTICATED | `You must sign in to continue.` |
| 404 | PRODUCT_NOT_FOUND | `This product is not available.` |
| 409 | HISTORY_CHANGED | `Your browsing history changed. Reload to see the latest entries.` |
| 503 | CATALOG_UNAVAILABLE | `The product catalog is temporarily unavailable. Please try again later.` |
| 503 | HISTORY_UNAVAILABLE | `Browsing history is temporarily unavailable. Please try again later.` |
| 500 | INTERNAL_ERROR | `Unable to complete your request. Please try again later.` |

- Optional errors is limited to VALIDATION_ERROR and maps request fields/query names to nonempty string arrays. Body-level errors may omit it.
- No history yet is HTTP 200 with enabled preference, revision, and empty entries. Missing authentication is not an empty history.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement the three authenticated endpoints in NestJS using the existing account and catalog identity.

- Maintain the account recording preference and product/day entries with their latest view time and retained display snapshot. Do not attach account history to browser-cart identity or import guest activity.
- Record only the supplied product for the current authenticated account, using server time and current preference. Preserve the one-entry-per-product/day rule under concurrent visits.
- Apply the declared calendar retention, capacity, ordering, and revision rules. Preference off prevents new recording without deleting retained entries.
- Search the saved name and filter the saved UTC date before pagination. Project current catalog summaries afterward; unavailable entries remain in the matching history with product=null.
- Return consistent counts/pages and reject changed revisions on Load more. Missing optional images are not catalog outages; failure to resolve required catalog data is a service error.
- Keep product GET, cart, profile, wishlist, comparison, and order behavior unchanged. Recording is a separate optional operation after a successful detail render.

### Frontend UI Context

Build `BrowsingHistoryPage` at `/account/browsing-history` in React, TypeScript, and Tailwind CSS.

- Implement the inspected switch, search field, single-date input, dated product grids, and LOAD MORE button within the shared account shell.
- Use date headings derived from UTC viewDate and merge a date group across appended pages. Keep at most four cards per desktop row, with wrapping for additional entries.
- Render current product cards using existing UC-04 components; unavailable entries use their retained identity and disabled navigation.
- Hide LOAD MORE when hasMore=false; keep it disabled during its request. Give the switch an accessible enabled/disabled label and unresolved/pending state.
- Provide distinct empty-history, no-match, recording-off, and service-failure feedback. These are project supplements, not verified alternate frames.

### Frontend Logic and API Context

- On entry, resolve the session and load page 1. Maintain filters, loaded entries, revision, enabled preference, pending states, and feedback.
- Preserve q/date in the browser URL; refresh reconstructs filters and loads page 1. Appended page count/revision remains local rather than restoring a stale page sequence after reload.
- Filter changes cancel/obsolete earlier reads, clear the loaded sequence, and fetch page 1. Load more uses the same filters and current sequence revision; only a successful response appends.
- Preference success updates enabled, then reloads page 1 because its revision may have changed. A failed follow-up read is a refresh failure, not a failed preference save.
- On UC-05, submit one record request after a successful eligible product-route render when the customer is authenticated. Do not send requests for mere configuration changes or framework re-renders, and do not replay requests after an account switch.
- History-record failure is nonblocking for product display. Session expiry stops recording, while public product viewing remains available.

### Validation and Error-Handling Context

- Validate UUID/body types, filter lengths/date syntax, positive page values, and pagination revision. The server owns account resolution, enabled state, timestamp, and retention.
- Distinguish date filters with no matches from invalid dates and service failure. Never parse ambiguous DD/MM/YYYY text as a different calendar convention.
- A stale pagination revision requires a new page-1 sequence. Do not silently append results that may duplicate or skip entries after a concurrent view update.
- No HTTP response displays `Unable to connect. Please check your connection and try again.` Optional background recording can fail silently without claiming success; user-initiated page/switch failures receive visible feedback.
- Reconcile an uncertain switch through a read before another preference decision. Do not invert a locally guessed state or automatically replay history writes.
- Do not infer product purchases, selected configurations, price history, or review submissions from browsing entries. This UC stores only the declared account product-view history.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
