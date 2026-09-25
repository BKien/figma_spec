# UC-16: View Order Details

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

View Order Details

Description:

- Displays the saved items, final amounts, addresses, contact, notes, and fulfillment activity of one placed order.
- Completes UC-15's View Details and UC-07's View Order integration points. Account detail and original-browser confirmation access have explicit separate boundaries below.
- Access rules, snapshots, API contracts, and missing-data behavior are project decisions; Figma establishes the desktop detail layout. Modification, cancellation, payment collection, and review submission are outside this UC; reviews belong to UC-17.

Primary Actor:

Signed-in order owner, or the visitor in the original checkout browser context.

Preconditions:

- UC-07 provides a persisted order; UC-15 supplies nullable account association; UC-08 supplies coherent fulfillment records.
- Register `/account/orders/:orderId` and `/orders/:orderId` for account and original-browser access respectively, with direct navigation/reload.
- Existing order totals and address/contact snapshots are authoritative. No current catalog or address-book lookup may replace them.

Postconditions:

- Success: The permitted actor sees the correct order with coherent amounts, purchased configurations, and fulfillment activity.
- Failure: No inaccessible order information is displayed; a generic not-found state or service recovery is shown.
- Reading details changes no order, inventory, cart, session lifetime, payment, or review.

Main Flow:

1. The customer selects View Details in UC-15, or View Order on the confirmed UC-07 success screen.
2. UC-15 navigates to `/account/orders/:orderId`; UC-07 navigates to `/orders/:orderId` using the confirmed order ID, not a guessed number.
3. The frontend calls the endpoint corresponding to that route and shows loading without previous-order content.
4. The backend checks the applicable access rule and returns saved order information and current coherent fulfillment activity.
5. The frontend renders summary, progress, activity, purchased-item table, billing/shipping addresses, and notes.
6. The actor returns to account history or continues shopping through the corresponding implemented destination.

Alternative Flow:

A.1 — Account access

- `/api/v1/account/orders/:orderId` requires an active verified session and exact UC-15 order/account association. It works across browsers for the same owner. A browser receipt alone does not satisfy this endpoint.

A.2 — Original-browser access

- `/api/v1/checkout/orders/:orderId` requires the browser context that placed the order, independent of account login. Knowing the order ID alone is insufficient.
- Availability follows UC-07's at-least-seven-day confirmation access rule. This explicitly extends that confirmation to a complete receipt for the same original browser; it does not broaden UC-08's public tracking lookup.
- Guest detail uses the shared public shell without pretending the visitor owns an authenticated account sidebar. Its back action goes to `/shop`; account detail returns to `/account/orders` (preserve a valid previously visited page in local navigation state when available).

A.3 — Catalog/address changes

- Removed products still display the saved purchased name/options/price and image placeholder where needed. Item names are receipt text, not enabled links requiring live catalog availability.
- Saved-account address changes do not affect this order. Shipping uses UC-07's effective address snapshot; show the one saved order contact in both address sections, labeled Order contact. Do not invent a separate shipping-contact email from UC-13.

A.4 — Notes and activity

- Null orderNotes displays `No order notes.` Missing estimates follow UC-08; DELIVERED uses deliveredAt. Milestone/activity mapping and chronology follow UC-08 exactly.
- Leave a Rating is owned by UC-17. In a UC-16-only build it is disabled with an explanation; the combined baseline enables it through UC-17's eligibility endpoint.

Exception Flow:

E.1 — Missing authentication or inaccessible order

- Account endpoint: absent/ineligible session returns 401 UNAUTHENTICATED, clears personal detail state, and redirects to `/sign-in`.
- Either endpoint: unknown order or wrong access context returns the same 404 ORDER_NOT_FOUND. Show `This order is not available.` and the appropriate safe return link; do not reveal another order's owner/contact.

E.2 — Data unavailable

- Temporary or inconsistent required order/fulfillment data returns 503 ORDER_DETAILS_UNAVAILABLE. Do not reconstruct totals from current prices or fabricate missing addresses.
- A missing image or category label is optional data and uses a placeholder/omitted label. A failed request shows a retry for the current order, not a previous order's content.

UI Integration:

- Source: `29_Dasboard_Order Detail`, node `478:12692`.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=478-12692
- Live design context and screenshot inspected on 2026-09-19. The account desktop layout is verified at that level; guest shell, totals breakdown, and recovery states are project supplements. No frozen dataset or responsive design is claimed.
- Preserve sidebar, back arrow, summary, four milestones, activity list, Products/Price/Quantity/Sub-Total table, and address/notes columns. Reuse Public Sans, orange progress, blue amount, and light borders.
- Use actual itemCount; table heading shows distinct line count while summary shows summed quantities. Correct the source's inconsistent total/progress/sample timestamps.
- Add a compact subtotal/discount/shipping/tax breakdown using saved totals to explain the summary total. This is an explicit supplement, not a new fee calculation.
- Enable UC-15 View Details and UC-07 View Order only once these routes are implemented. Use current persisted data; do not duplicate the source's placeholder identities.

API Endpoint:

`GET /api/v1/account/orders/:orderId`

`GET /api/v1/checkout/orders/:orderId`

Both share the response schema; access checks differ as specified.

Request Body:

No body or query parameters. orderId is a UUID. Reject malformed IDs, bodies, and unknown/repeated query parameters with VALIDATION_ERROR. No email, accountId, or address fields select the order owner.

Successful Response:

```json
{
  "success": true,
  "message": "Order details retrieved.",
  "data": {
    "order": {
      "id": "b5cf395b-fc08-4c2d-9132-bb01924ba70b",
      "orderNumber": "CL-00001234",
      "orderStatus": "PLACED",
      "paymentMethod": "CASH_ON_DELIVERY",
      "paymentStatus": "UNPAID",
      "placedAt": "2026-09-19T10:03:00.000Z",
      "currency": "USD",
      "itemCount": 2,
      "items": [
        {
          "productId": "c168f6e8-a7e4-4efc-b278-2f96da050e8f",
          "variantId": "5c69ff67-1c39-41e3-982f-51ec2016da71",
          "name": "Apple MacBook Pro 14-inch",
          "categoryName": null,
          "options": {
            "color": "Space Gray",
            "size": "14-inch",
            "memory": "16GB",
            "storage": "512GB SSD"
          },
          "imageUrl": null,
          "quantity": 2,
          "unitPrice": 169900,
          "lineTotal": 339800
        }
      ],
      "totals": {
        "subtotal": 339800,
        "discount": 0,
        "shipping": 500,
        "tax": 0,
        "total": 340300
      },
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
      "shippingAddress": {
        "firstName": "Alex",
        "lastName": "Nguyen",
        "company": null,
        "addressLine": "123 Example Street",
        "countryCode": "US",
        "regionCode": "CA",
        "cityCode": "SAN_FRANCISCO",
        "postalCode": "94105"
      },
      "contact": {
        "email": "customer@example.com",
        "phone": "+14155550123"
      },
      "orderNotes": null,
      "tracking": {
        "fulfillmentStatus": "ORDER_PLACED",
        "expectedDeliveryDate": null,
        "deliveryTimeZone": "America/Los_Angeles",
        "deliveredAt": null,
        "events": [
          {
            "id": "c9de7d57-8c69-4f16-8071-549871331ac0",
            "sequence": 1,
            "stage": "ORDER_PLACED",
            "occurredAt": "2026-09-19T10:03:00.000Z",
            "message": "Your order has been placed."
          }
        ]
      }
    }
  }
}
```
- HTTP 200. All keys required. IDs are UUIDs; nullable categoryName/imageUrl/orderNotes are string or null. Item options and the eight address keys reuse UC-05/UC-07. contact is the original checkout contact, not the current profile.
- For new orders, retain optional categoryName/imageUrl with item snapshots; absent older snapshots stay null. Never fetch a current replacement name/price to fill historical data.
- Integer USD cents: lineTotal = quantity × unitPrice; subtotal = sum(lineTotal); total = subtotal − discount + shipping + tax. itemCount = sum(quantity). Items are nonempty and retain original order.
- orderStatus/payment fields retain UC-07's current PLACED/CASH_ON_DELIVERY/UNPAID lifecycle. No automatic paid status is inferred from delivery.
- tracking uses UC-08's enum, ordered event schema, dates, timezone, and consistency rules. The order information and tracking must be read coherently; no inconsistent progress is returned.

Error Response:

Use the shared error envelope: success=false, statusCode matching HTTP status, code, message, server-generated ISO 8601 UTC timestamp, and actual request pathname without query string. Omit data. Optional errors is only for VALIDATION_ERROR and maps input paths to nonempty arrays of strings. All shown success keys are required; examples illustrate contracts rather than fixed data.

```json
{
  "success": false,
  "statusCode": 404,
  "code": "ORDER_NOT_FOUND",
  "message": "This order is not available.",
  "timestamp": "2026-09-19T10:00:00.000Z",
  "path": "/api/v1/account/orders/b5cf395b-fc08-4c2d-9132-bb01924ba70b"
}
```

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | You must sign in to continue. |
| 404 | ORDER_NOT_FOUND | This order is not available. |
| 503 | ORDER_DETAILS_UNAVAILABLE | Order details are temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

## Project-Specific Implementation Context

### Backend Implementation Context

Implement the two NestJS read endpoints with a shared receipt projection and distinct account/original-browser access rules. Reuse UC-15 ownership and UC-07 snapshots; preserve guest orders as unassociated. Resolve fulfillment through UC-08. Do not add order mutation, automatic ownership claims, payment handling, or catalog-based receipt reconstruction.

### Frontend UI Context

Implement both detail routes in React/TypeScript/Tailwind with the inspected layout and declared guest-shell adaptation. Reuse existing milestones and monetary formatting. Render receipt data as text, provide accessible headings/table labels, and use placeholders for optional images. Connect existing View Details/View Order controls to real routes.

### Frontend Logic and API Context

On route changes clear prior order data and request the correct endpoint. Ignore obsolete responses. Account 401 clears private state; 404 shows only the generic recovery state. Independent review eligibility is loaded by UC-17 and cannot block receipt viewing. Do not call the original-browser endpoint as a fallback to circumvent rejection on the account route.

### Validation and Error-Handling Context

Validate IDs, required snapshot fields, arithmetic, and fulfillment consistency. Network failure shows `Unable to connect. Please check your connection and try again.` Malformed data shows `Unable to load order details. Please try again.` A failed read never re-creates the order, recharges payment, or deducts inventory.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
