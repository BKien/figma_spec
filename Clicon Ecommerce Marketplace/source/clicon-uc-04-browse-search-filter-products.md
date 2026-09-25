# UC-04: Browse, Search and Filter Products

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Browse, Search and Filter Products

Description:

- Allows a visitor or customer to find products by browsing the catalog, entering a search phrase, combining filters, choosing a sort order, and navigating result pages.
- These actions form one goal: obtaining a relevant product list. Viewing full product details, adding to cart, managing a wishlist, comparing products, and checkout belong to separate use cases.
- Filter combination rules, search matching, sort options beyond the visible selection, URL behavior, and API contracts below are project decisions. The referenced Figma frame supplies the desktop controls and layout.

Primary Actor:

Visitor or signed-in Customer.

Preconditions:

- The application exposes the public `/shop` route, including direct navigation and reload.
- The catalog has published-product records and category, brand, and tag reference data. An empty catalog remains a valid state.
- Both public API endpoints use the shared Clicon success/error envelopes. No account or existing session is required.

Postconditions:

- Success: The current product page, matching-result count, applied filters, sort order, and pagination reflect the accepted request. The URL represents the applied state and can be reopened.
- Failure: No catalog, account, cart, or wishlist data changes. The page shows an actionable error rather than incorrectly displaying a successful empty result.

Main Flow:

1. The visitor opens `/shop`, optionally with supported query parameters.
2. The frontend loads available filter options and requests products for the URL state. With no query, use no filters, Most Popular sorting, and page 1.
3. The system displays the filter sidebar, local search box, Sort by dropdown, Active Filters, result count, product grid, and pagination.
4. The visitor submits a search phrase and/or changes category, price, brand, or tag selections.
5. The frontend validates the proposed state, applies it, resets page to 1, and requests the matching products.
6. The backend applies the documented matching and filter rules, orders the result, and returns one page plus pagination metadata.
7. The frontend displays returned products and the total number of matches, updates filter chips and the URL, and keeps controls synchronized.
8. The visitor may change sort order or navigate a result page. A sort change resets page to 1; a page change preserves all search/filter/sort criteria.
9. The visitor can remove an applied-filter chip to broaden the results without clearing unrelated criteria.

Alternative Flow:

A.1 — Search from the shared header

- Submitting the header search navigates to `/shop?q=<encoded phrase>` with other filters cleared, default sorting, and page 1. Local Shop search preserves existing filters.
- An empty or whitespace-only phrase removes the search constraint and browses the remaining criteria.

A.2 — Combine and remove filters

- Select at most one category. Multiple brands match any selected brand; multiple tags match any selected tag. Different filter groups are combined with AND.
- The category chip's remove action clears the category. Each brand/tag chip clears only that item. Removing the price chip clears both price bounds. Removing the search chip clears the applied phrase.
- All filter/search changes reset page to 1. The frontend derives chips from applied state, not from example text in Figma.

A.3 — Price presets and custom range

- The slider, Min price/Max price inputs, and preset choices represent the same price range. Selecting a preset updates the other controls.
- Custom edits replace the preset selection; they do not add a second price constraint. Empty bounds mean unbounded; All Price clears both bounds.
- Apply numeric input on Enter or when focus leaves the price-input group, provided both current values are valid. Apply the slider when the user finishes dragging or commits a keyboard adjustment.

A.4 — Restore navigation state

- Browser Back/Forward, direct URL entry, and reload restore the query and fetch the corresponding result. Draft text that was never submitted is not treated as an applied search.

A.5 — Rating chip from a shared URL

- Figma shows a `5 Star Rating` chip but no rating selector in the inspected sidebar. Support optional `rating=5` in a shared URL, display that removable chip, and match products whose unrounded average rating is exactly 5 with at least one review.
- No new rating selector is added to this screen. This URL behavior is a project interpretation of the observed chip, not confirmed prototype behavior.

Exception Flow:

E.1 — Invalid query or price range

- Invalid price input or minimum greater than maximum displays feedback near the range controls and is not applied.
- Invalid API query parameters return HTTP 400 `VALIDATION_ERROR` with field-keyed messages. Unknown category/brand/tag slugs are validation errors, not empty-result matches.
- For an invalid direct URL, show the error with `Reset filters`, which restores `/shop`. Do not silently apply a different subset of the invalid request.

E.2 — No matching products

- Return HTTP 200 with an empty `items` array and zero result count. Retain the applied filters and show `No products match your search. Try changing your filters.`
- Hide pagination when there are no results. Provide `Reset filters` to remove search/filters and restore default sort/page. This feedback/action is a project UI supplement.

E.3 — Page no longer exists

- If a valid requested page exceeds the last available page, return the last page and its actual page number. If there are no matches, return page 1 with totalPages 0.
- The frontend replaces the URL page with the returned page without issuing a redundant request. This handles a catalog that changes between requests.

E.4 — Product or filter-options service failure

- Return HTTP 503 `CATALOG_UNAVAILABLE` for known catalog-service unavailability and HTTP 500 `INTERNAL_ERROR` for unexpected failures.
- A failed filter-options load shows a retry state before interactive browsing; do not fabricate options. A failed product query preserves the requested controls and shows retry feedback in the results area.
- Previously displayed products may remain only if clearly labelled as previous results; do not present their count as the count of the failed new query.

E.5 — Overlapping requests

- When the visitor changes criteria quickly, only the response associated with the latest applied state can update the grid/count/URL. An older response must not overwrite the latest selection.

UI Integration:

- Main source: `07_Shop Page`, node `391:4117`, desktop frame 1920 × 3084.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=391-4117
- Metadata for the main frame and design context/screenshots for the following subnodes were inspected live on 2026-09-18. A complete immutable design release, mobile layout, open dropdown variants, and loading/error variants are not claimed by this UC.

| Observed region | Exact node | Integration |
| --- | --- | --- |
| Filter sidebar | `394:7680` | Category radios, price slider/inputs/presets, brand checkboxes, selectable tags |
| Search and Sort by | `391:6927` | Search for anything...; visible selection Most Popular |
| Active Filters and Results | `394:7723` | Removable chips and dynamic matching-result count |
| Representative product card | `394:7726` | Image, rating stars/count, title, price, badge |
| Pagination | `478:11898` | Previous/next arrows and numbered pages |

- Desktop content width is 1320 px: sidebar 312 px, gap 24 px, results area 984 px. The grid has four columns of 234 px cards with 16 px gaps; the reference shows 24 cards per page.
- Preserve Public Sans, orange active controls (`#FA8232`), blue product prices (`#2DA5F3`), gray borders (`#E4E7E9`), and the light-gray Active Filters background (`#F2F4F5`). Reuse the existing Clicon header/footer and breadcrumb structure.
- The visible selected filters, `65,867` result count, six page buttons, and product text are design examples, not application defaults or fixed catalog values. Render actual data. The sampled card's image/title are inconsistent; seed data must associate each image with its real product rather than copy the mismatch.
- Sidebar category labels include Electronics Devices, Computer & Laptop, Computer Accessories, SmartPhone, Headphone, Mobile Accessories, Gaming Console, Camera & Photo, TV & Homes Appliances, Watchs & Accessories, GPS & Navigation, and Warable Technology. Preserve source wording in the visual reference; bind selections to catalog slugs.
- Popular Brands and Popular Tag are data-backed option lists. The selected Graphics Card tag and checked brands shown in the design do not force initial selections.
- The closed sort dropdown verifies Most Popular only. The additional Price: Low to High, Price: High to Low, and Newest options are project additions.
- Banner Add to Cart, banner View Details, and product-detail/card navigation are owned by separate use cases. In an isolated UC-04 build, retain their visual placement where present but leave action controls disabled with a scope explanation; do not navigate to an absent route or report a cart update. Existing implemented integrations may retain their own behavior.
- Empty, loading, invalid-query, retry, and disabled-boundary pagination states are project supplements. This UC defines desktop behavior and does not claim an unseen responsive design.

API Endpoint:

| Operation | Endpoint |
| --- | --- |
| Load catalog filter options | `GET /api/v1/catalog/filters` |
| Query published products | `GET /api/v1/products` |

Request Body:

Neither GET endpoint has a request body. The filter-options endpoint accepts no query parameters. Product query parameters are:

| Parameter | Format | Default / behavior |
| --- | --- | --- |
| `q` | String, at most 100 Unicode code points after trimming | Omitted or blank means no text constraint |
| `category` | One catalog category slug | Omitted means all categories |
| `brand` | Repeated query parameter, up to 20 distinct brand slugs | Omitted means all brands |
| `tag` | Repeated query parameter, up to 20 distinct tag slugs | Omitted means all tags |
| `minPrice` | Nonnegative integer in USD cents | Omitted means no lower bound |
| `maxPrice` | Nonnegative integer in USD cents | Omitted means no upper bound |
| `rating` | Literal integer `5` only | Omitted means no rating constraint |
| `sort` | `popular`, `price_asc`, `price_desc`, `newest` | `popular` |
| `page` | Integer from 1 through 1000000 | 1 |

- Page size is fixed at 24; there is no `pageSize` request parameter or page-size selector.
- Price bounds must be safe integers no greater than 100000000 cents; minimum must not exceed maximum. Visible inputs are USD amounts with at most two decimal places and map to integer cents. One blank bound is allowed.
- Unknown parameter names, empty option slugs, malformed numbers, and repeated scalar parameters are invalid. Duplicate brand/tag entries are collapsed before applying their distinct-count limits. Brand/tag order does not affect matching.
- Search trims surrounding whitespace and matches the complete phrase, case-insensitively, as a substring of product name or SKU. No fuzzy matching, query-language syntax, or relevance ranking is defined.
- Category matching uses the selected catalog category directly; hierarchical descendant behavior is not introduced.
- Custom price bounds are inclusive. Preserve the displayed preset labels with these exact mappings:

| Visible preset | Query mapping in cents |
| --- | --- |
| All Price | Omit both bounds |
| Under $20 | `maxPrice=1999` |
| $25 to $100 | `minPrice=2500&maxPrice=10000` |
| $100 to $300 | `minPrice=10000&maxPrice=30000` |
| $300 to $500 | `minPrice=30000&maxPrice=50000` |
| $500 to $1,000 | `minPrice=50000&maxPrice=100000` |
| $1,000 to $10,000 | `minPrice=100000&maxPrice=1000000` |

- The preset gaps/overlapping endpoints reflect the source labels; presets are alternatives, not disjoint catalog partitions. Custom inputs cover other ranges.
- Most Popular orders by the catalog's numeric `popularityScore` descending; price orders by current selling price; Newest orders by `publishedAt` descending. Ties use product ID ascending. How popularity is assigned is outside this browsing UC; use consistent catalog values, not random ordering.
- The URL for `/shop` uses the same query names and representations as the product API. Display currency is USD for this UC; currency conversion is outside scope.

Example request:

```text
GET /api/v1/products?q=wireless&category=headphone&brand=tozo&minPrice=2500&maxPrice=10000&sort=price_asc&page=1
```

Successful Response:

Filter options — HTTP 200. The example represents a small catalog; arrays contain all available options in the actual dataset, in display order.

```json
{
  "success": true,
  "message": "Catalog filters retrieved.",
  "data": {
    "currency": "USD",
    "categories": [{"slug": "headphone", "name": "Headphone"}],
    "brands": [{"slug": "tozo", "name": "TOZO"}],
    "tags": [{"slug": "wireless", "name": "Wireless"}],
    "priceRange": {"min": 2500, "max": 15000}
  }
}
```

- `priceRange` gives current minimum/maximum published selling prices in cents; it is null when there are no published products. It supplies slider bounds, not validation limits for typed/query prices.
- Filter options are independent of the current query; do not remove selected options just because their combination has zero matches. An option deleted from the catalog subsequently becomes an invalid slug.
- Custom prices outside the available catalog range remain valid within the request contract. Keep their entered values; constrain the slider's displayed handles to its available range without silently rewriting the query. Disable the slider when the range is null or has equal endpoints.

Product results — HTTP 200:

```json
{
  "success": true,
  "message": "Products retrieved.",
  "data": {
    "items": [
      {
        "id": "f109a7be-4cf3-4a2a-9694-6cce4b049e31",
        "slug": "tozo-t6-wireless-earbuds",
        "name": "TOZO T6 True Wireless Earbuds",
        "imageUrl": "/images/products/tozo-t6.png",
        "price": 7000,
        "compareAtPrice": 9000,
        "currency": "USD",
        "ratingAverage": 4.6,
        "reviewCount": 738,
        "badge": "HOT"
      }
    ],
    "pagination": {
      "page": 1,
      "pageSize": 24,
      "totalItems": 1,
      "totalPages": 1
    }
  }
}
```

- Every listed item field is present. IDs are UUID strings; slugs identify products. Image URLs refer to actual supplied catalog assets; the example path is not proof an image file already exists.
- `price` and optional-value `compareAtPrice` use integer cents; `compareAtPrice` is null unless it exceeds the current price. `badge` is null or a catalog-provided display string. These values do not imply a discount-calculation or promotion-management feature.
- `ratingAverage` is a number from 0 to 5, or null when `reviewCount` is 0. `reviewCount` is a nonnegative integer. Rating rendering may use partial stars; filtering uses the stored unrounded average.
- `totalItems` counts all matches before pagination. `totalPages = ceil(totalItems / 24)`; `items` has at most 24 elements. No matches returns `items: []`, `page: 1`, `pageSize: 24`, `totalItems: 0`, `totalPages: 0` with the same success envelope.
- Internal SKU, publication state, category/brand/tag relations, publication time, and popularity score support matching/ordering but need not be returned in this card-summary response.

Error Response:

Use the shared error envelope, without `data`. Generate `timestamp` in UTC and set `path` to the endpoint pathname without the query string.

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-18T10:00:00.000Z",
  "path": "/api/v1/products",
  "errors": {
    "maxPrice": ["Maximum price must be greater than or equal to minimum price."]
  }
}
```

```json
{
  "success": false,
  "statusCode": 503,
  "code": "CATALOG_UNAVAILABLE",
  "message": "The product catalog is temporarily unavailable. Please try again later.",
  "timestamp": "2026-09-18T10:00:00.000Z",
  "path": "/api/v1/products"
}
```

| HTTP | Endpoint | Code | Exact message |
| --- | --- | --- | --- |
| 400 | Both | `VALIDATION_ERROR` | `Please correct the highlighted fields.` |
| 503 | Both | `CATALOG_UNAVAILABLE` | `The product catalog is temporarily unavailable. Please try again later.` |
| 500 | Both | `INTERNAL_ERROR` | `Unable to complete your request. Please try again later.` |

- Field-level `errors` is present only for validation and uses the query parameter names. No-result searches are successful responses, not 404 errors.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement the two public GET endpoints in NestJS using the shared response contract.

- Define catalog records with publication status, identity, name/SKU, image, selling/comparison prices, category, brand, tags, rating summary, badge, publishedAt, and popularityScore sufficient for the declared behavior. Reuse an existing project catalog model if one is present.
- Expose only published products in this browsing flow. Out-of-stock published products can still be listed; purchasing eligibility belongs to the cart/checkout use cases.
- Return actual reference options and coherent product data. Product names, images, prices, and result counts must describe the same catalog records.
- Apply the declared search/filter groups together, followed by sorting and pagination. Return count and items for the same logical query. Resolve out-of-range pages using E.3.
- Keep defaults, preset mappings, currency units, and slug validation consistent between both endpoints and the frontend.
- Browsing requires no sign-in and performs no account, inventory, order, cart, or wishlist mutation.

### Frontend UI Context

Build `ShopPage` at `/shop` in React, TypeScript, and Tailwind CSS using the inspected Figma regions.

- Reuse the shared header/footer; render the sidebar, search/sort toolbar, applied filters, result count, product grid, and pagination in the captured desktop arrangement.
- Use radio behavior for category/presets, checkboxes for brands, toggle behavior for tags, and two synchronized price handles/inputs. Selected states and chips reflect applied values.
- Show product images, full accessible names with visually truncated titles where needed, price, optional comparison price, rating/count, and optional badge.
- Display up to six consecutive page buttons around the current page, shifting the window at boundaries; use the source's circular styling. Previous/next are disabled at their boundaries. Hide pagination for zero matches and allow a single page indicator for one page.
- Loading, empty, invalid-query, unavailable-image, and service-error states use the existing visual language. A missing image uses a neutral product-image placeholder with alternative text and leaves other card data readable.
- Do not add a rating selector, cart implementation, quick-view modal, or full product-detail screen to this UC.

### Frontend Logic and API Context

- Maintain separate draft input values and applied query state. Applied state comprises q, category, brand/tag selections, price bounds, optional rating=5, sort, and page.
- At page entry, interpret supported URL parameters, fetch filter options, and load results for the valid state. Unsupported/malformed URLs follow E.1.
- Submit local search on Enter or its search icon. Category, brand, tag, and sort changes apply on selection; price changes follow A.3. Reset page on every search/filter/sort change.
- After applying state, update the URL and fetch the product endpoint. Repeated brand/tag parameters are serialized consistently; omitted values retain documented defaults. History navigation restores state without adding a new history entry.
- Only the latest query response updates the result display. Parse `data.items` and `data.pagination`, not unwrapped root fields. Normalize an out-of-range page from the returned metadata using history replacement.
- Removing a chip updates its corresponding control as well as the query. Reset filters clears search, category, brands, tags, price, rating, and returns sort/page to defaults.
- On service failure, retain intended criteria for manual retry. Do not replace a failed request with a fake empty array and zero count.

### Validation and Error-Handling Context

- Validate typed currency amounts before converting to cents; do not round an input with more than two decimal places into a different filter. Display an inline correction message.
- Keep server validation authoritative for slugs, ranges, defaults, and query shape. Map price/search errors to their controls and errors without visible controls to the form/result area.
- Distinguish loading, successful empty results, invalid queries, and service failure. Disable pagination while its next result is pending; filters remain editable so the visitor can change intent.
- Announce the updated result count and provide accessible names for chip removal, slider handles, search submission, and page controls.
- For no HTTP response, show `Unable to connect. Please check your connection and try again.` with a manual retry action.
- An unexpected response shape shows `Unable to load products. Please try again.` and does not replace the page with fabricated success data.
- Keep optional out-of-scope actions visibly unavailable until their owning use cases are integrated; never report a successful mutation from this read-only flow.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
