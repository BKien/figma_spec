# UC-05: View Product Details

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

View Product Details

Description:

- Allows a visitor or customer to inspect a published product, browse its images, select an available product configuration, and read product information before deciding whether to purchase.
- Continues UC-04 through product-card navigation. Includes read-only image/configuration selection, information tabs, related-product navigation, and copying the product link.
- Adding to cart, Buy Now, wishlist, comparison, reading/submitting individual reviews, and external social sharing belong to separate use cases. Their visible controls remain integration points, not simulated successful actions.
- Variant behavior, API contracts, quantity limits, and content for tabs not shown open in Figma are project decisions. The inspected frame establishes the visible desktop layout and controls.

Primary Actor:

Visitor or signed-in Customer.

Preconditions:

- The application exposes `/products/:slug` with direct navigation and reload support. UC-04 provides a catalog slug for each product card.
- The catalog contains product details and at least one published variant for each product considered available for public detail viewing. A single-configuration product still has one variant.
- Currency and summary values are consistent with UC-04; the shared success/error envelope applies. No login session is required.

Postconditions:

- Success: The page shows the requested product and selected variant's coherent images, SKU, configuration, price, and availability. The selected valid variant can be reopened using the URL.
- Failure: An invalid, removed, or unavailable product/configuration produces the documented recovery state; another product is not silently substituted.
- Viewing, selecting variants, changing local quantity, and copying a link do not change inventory, create a cart item, reserve stock, submit an order, or write a review.

Main Flow:

1. The visitor selects a product image/title in UC-04 or opens `/products/:slug` directly, optionally with `variant=<variantId>`.
2. The frontend requests `GET /api/v1/products/:slug`, forwarding the optional variant query.
3. The backend resolves the published product, its published variants, and the selected variant. Without a variant query, use `defaultVariantId`.
4. The API returns HTTP 200 with the product detail payload using the shared success envelope.
5. The frontend displays the image gallery, title, rating summary, SKU, brand, category, selected price, comparison price when present, availability, and configuration controls. Description is initially active.
6. The visitor may choose thumbnails or use gallery arrows to inspect images of the selected configuration.
7. The visitor may change Color, Size, Memory, or Storage. When the resulting complete selection matches a published variant, the frontend updates the selected variant, its dependent content, and the URL.
8. The visitor can switch between Description, Additional information, and Specification to inspect supplied content.
9. The visitor may open another product from the related-product sections or return to the previous Shop result through browser navigation.

Alternative Flow:

A.1 — Single-configuration product

- Select the only published variant. Hide an option group when it has no applicable value; show a single available value as selected when it exists. Do not invent laptop-specific fields for unrelated product categories.

A.2 — Select a configuration

- Option values are derived from the returned variants. Each combination of applicable color, size, memory, and storage identifies at most one variant.
- Preserve the visitor's other selections when one option changes. If the combination exists, switch to that variant; otherwise follow E.3 rather than silently changing another option.
- A valid selection updates SKU, price, comparison price, availability, maxQuantity, variant specifications, and gallery. Reset the displayed gallery to its first image and quantity to 1 when purchasable, or 0 when out of stock.
- Product-level name, brand, category, description, and aggregate rating remain unchanged. Show selected configuration values separately so the page does not contradict them.

A.3 — Change gallery image

- A thumbnail selects its corresponding image and receives the active border. Previous/next selects the adjacent image without wrapping and keeps the selected thumbnail visible.
- Disable an arrow at its respective boundary. If there is only one image, hide gallery arrows; if none are available, follow E.5.

A.4 — Adjust quantity locally

- The quantity control starts at 1 for an in-stock variant and permits integers from 1 to `maxQuantity`. Minus/plus changes by one; reaching a boundary disables that direction.
- Out-of-stock variants remain viewable; quantity is 0 and both controls are disabled. Quantity changes alone make no API mutation and are not stored as a cart.

A.5 — Copy a product link

- The copy icon copies the absolute application URL `/products/:slug?variant=<selectedVariantId>`. It does not include local quantity or prior Shop filters.
- Display `Product link copied.` only after successful copying. On clipboard failure, show the link for manual selection with `Copy this product link manually.`
- External social-network icons remain outside this UC; no external post is sent.

A.6 — Open related products or return to Shop

- Cards in Related Product, Product Accessories, the brand-product section, and Featured Products navigate to the selected product's `/products/:slug` route. These sections use catalog-provided associations; a recommendation algorithm is not specified.
- The Shop breadcrumb goes to `/shop`; category navigation goes to `/shop?category=<categorySlug>`. Browser Back restores UC-04's query/page from its URL.

Exception Flow:

E.1 — Product not found

- Unknown, removed, or unpublished products return HTTP 404 `PRODUCT_NOT_FOUND`.
- Show `This product is not available.` and a `Back to shop` link to `/shop`. Do not display old product content under the failed product URL.

E.2 — Invalid or unavailable variant in a direct URL

- A malformed variant ID returns HTTP 400 `VALIDATION_ERROR`; a well-formed ID that is not a published variant of this product returns HTTP 404 `VARIANT_NOT_FOUND`.
- Display feedback with `View default configuration`, which removes the variant query and explicitly loads the product default. Do not silently replace the requested variant.

E.3 — Unavailable option combination

- If current option values do not match a returned variant, display `This configuration is not available. Choose another option.`
- Keep the option controls editable. Show no stale variant-specific price, SKU, stock label, or purchase quantity as though it belongs to that combination. Disable copy and purchase-related actions until a valid configuration is selected.
- Remove the variant query while selection is incomplete; the product URL then reopens its documented default. Product-level information remains readable, and gallery may show product-level images. No unsuccessful selection changes inventory.

E.4 — Detail service failure or overlapping requests

- Known catalog-service unavailability returns HTTP 503 `CATALOG_UNAVAILABLE`; unexpected failure returns HTTP 500 `INTERNAL_ERROR`.
- Display a retry action for the current URL. Only the latest product request can update the screen; an earlier response must not overwrite a newly opened product.

E.5 — Missing images or optional content

- Use a neutral image placeholder with meaningful alternative text if no usable image is available. Other product information remains readable.
- An empty content section shows `No additional information available.` or `No specifications available.` as appropriate. Products with no reviews show `No reviews yet.` in the rating summary.
- Empty recommendation groups may be omitted; do not fill them with unrelated fabricated products.

UI Integration:

- Source: `08_Product Detail`, node `394:8951`, desktop frame 1920 × 2434.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=394-8951
- Live design context and its rendered screenshot were inspected on 2026-09-18. The source includes a gallery, configuration controls, Description content, other tab labels, action controls, and four product-link groups. A complete frozen dataset, responsive states, and unseen open-tab contents are not claimed here.

| Observed element | Integration |
| --- | --- |
| Main image, thumbnails, orange gallery arrows | Selected variant gallery, with product images as fallback |
| Star rating and User feedback count | Product-level `ratingAverage` and `reviewCount` |
| Product title; Sku, Availability, Brand, Category | Product/selected-variant fields |
| Current price, crossed-out price, percentage badge | Selected-variant selling/comparison prices and derived discount |
| Color swatches | `options.color` values with accessible names |
| Size / Memory / Storage dropdowns | Matching option values from published variants |
| Minus / quantity / plus | Local quantity selection |
| ADD TO CARD; BUY NOW | Preserve source labels/placement; actions owned by cart/purchase UCs |
| Add to Wishlist / Add to Compare | Separate UC integration points |
| Share product copy icon | Copy the current valid configuration URL |
| Description / Additional information / Specification / Review | Three information panels; Review reserved for its separate UC |
| Related Product / Product Accessories / Apple Product / Featured Products | Catalog-associated product links; brand heading follows actual brand |

- Reuse the shared Clicon header/footer and breadcrumbs. Preserve the two-column gallery/details region, Public Sans typography, orange actions (`#FA8232`), blue prices (`#2DA5F3`), light borders (`#E4E7E9`), and information-panel styling.
- The source title mentions a 13-inch/8GB/256GB configuration while selected controls show other values; its displayed discount is also inconsistent with its prices. Populate coherent catalog data instead of reproducing these sample-data mismatches. Correct `1TV SSD Storage` to the actual catalog value rather than treating the typo as a business rule.
- Discount display is a project rule: when `compareAtPrice > price`, display the whole-number percentage `floor(100 * (compareAtPrice - price) / compareAtPrice)`; omit the percentage if it rounds down to zero. No comparison price means no crossed-out price or percentage badge.
- Description includes text, Feature statements, and Shipping Information. These are catalog informational content, not a calculated checkout quote or evidence of implemented payment/warranty services.
- Additional information and Specification use simple label/value rows styled consistently with Description. Their panel layout is a project supplement because those tabs were not captured open. Review is visible but disabled with a scope explanation until the review UC is integrated; the summary is still displayed.
- In an isolated UC-05 build, cart, Buy Now, wishlist, comparison, and external social controls remain visible but disabled with scope explanations. Once their owning UCs exist, connect the selected product/variant/quantity to them; do not fake successful actions here.
- Payment logos and the source's checkout-assurance text are visual content, not an implementation specification for payment handling. No new success screen, zoom modal, review form, or mobile layout is inferred.

API Endpoint:

`GET /api/v1/products/:slug`

Request Body:

No request body. This public endpoint accepts:

| Input | Contract |
| --- | --- |
| `slug` path parameter | Lowercase alphanumeric words separated by single hyphens; 1–160 characters; must identify a published product |
| `variant` optional query parameter | UUID of a published variant belonging to that product; omitted selects `defaultVariantId` |

- Reject unknown query parameters, repeated `variant`, or an empty/malformed variant ID with `VALIDATION_ERROR`.
- Browser route `/products/:slug` uses the same optional query. Image, tab, and quantity changes do not add API query parameters.

```text
GET /api/v1/products/macbook-pro-14?variant=5c69ff67-1c39-41e3-982f-51ec2016da71
```

Successful Response:

HTTP 200:

```json
{
  "success": true,
  "message": "Product details retrieved.",
  "data": {
    "product": {
      "id": "c168f6e8-a7e4-4efc-b278-2f96da050e8f",
      "slug": "macbook-pro-14",
      "name": "Apple MacBook Pro 14-inch",
      "brand": {"slug": "apple", "name": "Apple"},
      "category": {"slug": "computer-laptop", "name": "Computer & Laptop"},
      "currency": "USD",
      "ratingAverage": 4.7,
      "reviewCount": 21671,
      "images": [
        {"id": "front", "url": "/images/products/macbook-pro-14-front.png", "alt": "MacBook Pro viewed from the front"},
        {"id": "side", "url": "/images/products/macbook-pro-14-side.png", "alt": "MacBook Pro viewed from the side"}
      ],
      "description": ["A notebook for everyday and creative work."],
      "features": ["One-year warranty"],
      "shippingInformation": [{"label": "Courier", "value": "Estimated delivery in 2–4 days"}],
      "additionalInformation": [{"label": "Package contents", "value": "Notebook and power adapter"}],
      "defaultVariantId": "5c69ff67-1c39-41e3-982f-51ec2016da71",
      "variants": [
        {
          "id": "5c69ff67-1c39-41e3-982f-51ec2016da71",
          "sku": "MBP14-SG-16-512",
          "options": {"color": "Space Gray", "size": "14-inch", "memory": "16GB", "storage": "512GB SSD"},
          "colorHex": "#8E9295",
          "price": 169900,
          "compareAtPrice": 199900,
          "availability": "IN_STOCK",
          "maxQuantity": 5,
          "images": [],
          "specifications": [
            {"label": "Display", "value": "14-inch"},
            {"label": "Memory", "value": "16GB"},
            {"label": "Storage", "value": "512GB SSD"}
          ]
        },
        {
          "id": "27dc9eaf-3cea-42e5-993e-ce962da09a45",
          "sku": "MBP14-SV-16-512",
          "options": {"color": "Silver", "size": "14-inch", "memory": "16GB", "storage": "512GB SSD"},
          "colorHex": "#DADDDD",
          "price": 169900,
          "compareAtPrice": null,
          "availability": "OUT_OF_STOCK",
          "maxQuantity": 0,
          "images": [],
          "specifications": [
            {"label": "Display", "value": "14-inch"},
            {"label": "Memory", "value": "16GB"},
            {"label": "Storage", "value": "512GB SSD"}
          ]
        }
      ]
    },
    "selectedVariantId": "5c69ff67-1c39-41e3-982f-51ec2016da71",
    "recommendations": {
      "related": [],
      "accessories": [],
      "brandProducts": [],
      "featured": []
    }
  }
}
```

- Example names, values, UUIDs, and image paths illustrate the contract; implementation supplies actual coherent catalog records and assets.
- All shown keys are required. Product and variant IDs are UUIDs. Arrays preserve display order; product variants are nonempty and `defaultVariantId`/`selectedVariantId` each identify one returned variant.
- `options` always has color, size, memory, and storage keys. Each value is a nonempty display string or null when that dimension does not apply. `colorHex` is a six-digit hexadecimal color or null; a null swatch color uses a labelled neutral swatch. Option labels and the set of combinations come from actual product data.
- Prices are nonnegative integer USD cents, matching UC-04. `compareAtPrice` is null or greater than price. Product-level currency applies to all its variants.
- `availability` is `IN_STOCK` or `OUT_OF_STOCK`. `maxQuantity` is the current permitted quantity for that variant, 1–99 when in stock and 0 otherwise. This is a display snapshot, not a stock reservation or a promise that a future cart request will succeed.
- `ratingAverage` is 0–5 or null when reviewCount is zero. Ratings summarize the product across variants, consistently with UC-04.
- Product and variant `images` use the same `{id, url, alt}` schema. Nonempty variant images replace the product gallery; an empty variant image array uses the product gallery. IDs are unique within each gallery.
- Description/features are arrays of text strings. Shipping information, additional information, and variant specifications are arrays of `{label, value}` strings. Empty arrays mean unavailable optional content, not a service error.
- Each recommendation group contains zero to three published products other than the current product, in configured order. Every item uses the exact UC-04 card-summary schema: `id`, `slug`, `name`, `imageUrl`, `price`, `compareAtPrice`, `currency`, `ratingAverage`, `reviewCount`, `badge`. Do not add a new incompatible card contract.
- UC-04's product summary uses the product's default variant selling/comparison prices and first effective gallery image. Detail loaded without `variant` must show those same prices for the same catalog state. Product name/slug/rating identity remains shared. This integration rule does not change UC-04's response shape.

Error Response:

Use the shared envelope; errors contain no `data`. `timestamp` is generated in UTC and `path` contains the actual endpoint pathname without its query string.

```json
{
  "success": false,
  "statusCode": 404,
  "code": "PRODUCT_NOT_FOUND",
  "message": "This product is not available.",
  "timestamp": "2026-09-18T10:00:00.000Z",
  "path": "/api/v1/products/macbook-pro-14"
}
```

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-18T10:00:00.000Z",
  "path": "/api/v1/products/macbook-pro-14",
  "errors": {
    "variant": ["Variant must be a valid UUID."]
  }
}
```

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | `VALIDATION_ERROR` | `Please correct the highlighted fields.` |
| 404 | `PRODUCT_NOT_FOUND` | `This product is not available.` |
| 404 | `VARIANT_NOT_FOUND` | `This product configuration is not available.` |
| 503 | `CATALOG_UNAVAILABLE` | `The product catalog is temporarily unavailable. Please try again later.` |
| 500 | `INTERNAL_ERROR` | `Unable to complete your request. Please try again later.` |

- `errors` is optional, appears only for validation, and maps `slug` or query-field names to nonempty message arrays. An out-of-stock published variant is a successful detail response, not a 404.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement the public detail endpoint in NestJS using the existing UC-04 catalog identity and shared API envelope.

- Extend/reuse the catalog with ordered images, descriptive content, variants, default-variant identity, variant stock/quantity availability, specifications, and configured product associations.
- Return only published product/variant detail. A product with no published variants is unavailable through this endpoint. A default ID referring to a missing variant is invalid catalog data; do not invent a variant in the response.
- Resolve the optional variant within the requested product and return the documented error when it does not belong. Use the default only when the parameter is absent.
- Preserve UC-04 summary/detail agreement through the default-variant projection described above. Do not create a separate product identity or incompatible monetary units for the detail page.
- Resolve recommendation groups from configured associations, omitting unpublished/missing targets. Missing optional recommendation groups do not prevent viewing the primary product; failure of the primary detail source is a service error.
- Serve this use case without inventory mutation, cart creation, order placement, or review submission. Purchase and review service behavior is not implemented by this endpoint.

### Frontend UI Context

Build `ProductDetailPage` at `/products/:slug` in React, TypeScript, and Tailwind CSS using the inspected Figma frame.

- Connect UC-04 image/title links and configured promotional View Details links to this route once UC-05 is integrated. Do not alter UC-04's filtering or summary response contract.
- Build the gallery and information columns, option controls, quantity selector, tabs, informational Feature/Shipping content, and product-link groups in the observed desktop arrangement.
- Use Description as the initial tab. Additional information and Specification show their declared label/value data; keep Review scoped as described in UI Integration.
- Derive option groups and product content from API data, not the sample MacBook strings. Announce selected colors by name rather than color alone; label every dropdown and gallery control.
- Preserve disabled integration actions until their owning UCs exist. Displaying an assurance badge or payment logo must not trigger any payment behavior.

### Frontend Logic and API Context

- State includes product data, selected option values, selectedVariantId or no valid selection, active image, active information tab, local quantity, loading, and error/copy feedback.
- On route entry or product-slug change, fetch the detail endpoint with the optional variant ID. Read `data.product`, `data.selectedVariantId`, and `data.recommendations`.
- On successful load, initialize option values from the selected variant, first effective image, Description tab, and the permitted starting quantity. Remove old product content while loading a different product.
- Resolve configuration changes against the returned variant list. A valid change updates dependent fields locally and writes `variant` to the browser URL without an unnecessary fetch of identical detail data. Refresh/direct navigation still validates that ID through the endpoint.
- Invalid combinations follow E.3; do not retain the preceding variant's actionable selection. Handle browser history changes by restoring a matching loaded variant or reloading the requested product when necessary.
- Derive discount and monetary formatting from the declared values. Do not change the unit price because local quantity changed.
- Recommendation links stay within the same implemented detail route. Reset image/quantity/tab state when the product changes. Browser Back uses the recorded UC-04 URL rather than constructing new default filters.
- Copy only a valid selected-variant URL and report clipboard success/failure accurately. No other sharing integration is introduced.

### Validation and Error-Handling Context

- Validate route/query shape before applying a selection; server membership and publication checks determine whether a requested variant is available.
- Keep unavailable product, unavailable variant, out-of-stock variant, invalid option combination, missing optional content, and service failure as distinct UI states.
- Quantity cannot exceed maxQuantity or become fractional/negative. Disable its controls when the variant is unavailable or out of stock; reaching a valid boundary is not a server error.
- Use the default-configuration recovery action only when explicitly selected by the visitor. Missing-product feedback always offers `/shop` as a reachable destination.
- For no HTTP response, display `Unable to connect. Please check your connection and try again.` and allow a manual retry of the current URL.
- Unexpected/malformed detail data displays `Unable to load product details. Please try again.`; do not show a fabricated price or falsely mark the product in stock.
- If image loading fails, retain readable information and show the placeholder. If copying fails, provide the manual-copy fallback without falsely reporting success.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
