# Common Wire Contract

These proposed HTTP contracts describe a new application boundary. No deployed Euphoria API was inspected. Field names, routes, envelopes, transport authentication, and public codes are implementation assumptions.

## Transport

HTTPS; JSON UTF-8. Success bodies contain `data` and `requestId`. Error bodies contain `error` and `requestId`; `error` contains `code` and `message`. `requestId` is an opaque string. All timestamps use ISO 8601 UTC text; dates use YYYY-MM-DD. Identifiers are opaque JSON strings. Monetary amounts use decimal strings and currency uses a currency-code string. No binary floating-point number is used for money on the wire.

## Object definitions

Each object below is reusable by reference from the individual contracts. Every field is required unless its individual definition says otherwise. Nullable fields are sent as JSON null. Arrays are JSON arrays. Example values illustrate transport shape. This document defines no domain decisions.

## Money

### `amount`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Decimal string syntax: ^-?[0-9]+(?:\.[0-9]+)?$.
- Description: Decimal monetary amount.
- Example: `"29.00"`.

### `currency`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Three uppercase ASCII letters.
- Description: Currency code.
- Example: `"USD"`.

## ProductCard

### `id`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Product identifier.
- Example: `"prd_01"`.

### `title`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Display title.
- Example: `"Printed shirt"`.

### `brand`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Brand display name.
- Example: `"Euphoria"`.

### `imageUrl`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Absolute URI syntax.
- Description: Image URI.
- Example: `"https://example.com/shirt.jpg"`.

### `price`

- Type: Money.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Displayed price.
- Example: `{"amount": "29.00", "currency": "USD"}`.

## Category

### `id`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Category identifier.
- Example: `"cat_tops"`.

### `name`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Category display name.
- Example: `"Tops"`.

### `imageUrl`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Absolute URI syntax.
- Description: Image URI.
- Example: `"https://example.com/tops.jpg"`.

## Promotion

### `id`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Promotion identifier.
- Example: `"promo_01"`.

### `heading`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Display heading.
- Example: `"New arrivals"`.

### `imageUrl`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Absolute URI syntax.
- Description: Image URI.
- Example: `"https://example.com/banner.jpg"`.

### `targetCategoryId`

- Type: string.
- Required: Yes.
- Nullable: Yes.
- Default: None.
- Validation: JSON type only.
- Description: Category identifier or null.
- Example: `null`.

## Testimonial

### `id`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Testimonial identifier.
- Example: `"test_01"`.

### `name`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Display name.
- Example: `"Sample customer"`.

### `body`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Displayed feedback.
- Example: `"Comfortable fabric."`.

### `rating`

- Type: number.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Displayed rating.
- Example: `4`.

## Storefront

### `promotions`

- Type: Promotion[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Promotional sections.
- Example: `[]`.

### `categories`

- Type: Category[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Category sections.
- Example: `[]`.

### `featured`

- Type: ProductCard[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Featured product cards.
- Example: `[]`.

### `testimonials`

- Type: Testimonial[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Displayed feedback.
- Example: `[]`.

## Facet

### `value`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Selection value.
- Example: `"black"`.

### `label`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Display label.
- Example: `"Black"`.

## CatalogResult

### `items`

- Type: ProductCard[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Product cards.
- Example: `[]`.

### `categories`

- Type: Facet[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Category choices.
- Example: `[]`.

### `colors`

- Type: Facet[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Color choices.
- Example: `[]`.

### `sizes`

- Type: Facet[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Size choices.
- Example: `[]`.

### `styles`

- Type: Facet[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Dress style choices.
- Example: `[]`.

### `total`

- Type: integer.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Result count.
- Example: `0`.

## Variant

### `id`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Variant identifier.
- Example: `"var_01"`.

### `size`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Size display value.
- Example: `"M"`.

### `color`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Color display value.
- Example: `"Black"`.

### `price`

- Type: Money.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Variant price.
- Example: `{"amount": "29.00", "currency": "USD"}`.

### `purchasable`

- Type: boolean.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Public selection state.
- Example: `true`.

## Attribute

### `name`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Attribute label.
- Example: `"Fabric"`.

### `value`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Attribute display value.
- Example: `"Cotton"`.

## ProductDetail

### `product`

- Type: ProductCard.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Main product card.
- Example: `{"id": "prd_01", "title": "Printed shirt", "brand": "Euphoria", "imageUrl": "https://example.com/shirt.jpg", "price": {"amount": "29.00", "currency": "USD"}}`.

### `description`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Description text.
- Example: `"Printed cotton shirt."`.

### `images`

- Type: string[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Absolute URI syntax.
- Description: Image URIs.
- Example: `[]`.

### `rating`

- Type: number.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Displayed rating.
- Example: `3.5`.

### `commentCount`

- Type: integer.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Displayed comment count.
- Example: `120`.

### `questionCount`

- Type: integer.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Displayed question count.
- Example: `4`.

### `attributes`

- Type: Attribute[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Product attributes.
- Example: `[]`.

### `variants`

- Type: Variant[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Variant choices.
- Example: `[]`.

### `similarProducts`

- Type: ProductCard[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Related cards.
- Example: `[]`.

## CartLine

### `id`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Cart line identifier.
- Example: `"cl_01"`.

### `variantId`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Variant identifier.
- Example: `"var_01"`.

### `title`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Product display title.
- Example: `"Printed shirt"`.

### `imageUrl`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Absolute URI syntax.
- Description: Image URI.
- Example: `"https://example.com/shirt.jpg"`.

### `color`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Selected color.
- Example: `"Black"`.

### `size`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Selected size.
- Example: `"M"`.

### `quantity`

- Type: integer.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Displayed quantity.
- Example: `1`.

### `unitPrice`

- Type: Money.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Unit amount.
- Example: `{"amount": "29.00", "currency": "USD"}`.

### `lineTotal`

- Type: Money.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Line amount.
- Example: `{"amount": "29.00", "currency": "USD"}`.

## Cart

### `id`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Cart identifier.
- Example: `"cart_01"`.

### `version`

- Type: integer.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Cart revision value.
- Example: `1`.

### `items`

- Type: CartLine[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Cart lines.
- Example: `[]`.

### `subtotal`

- Type: Money.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Displayed subtotal.
- Example: `{"amount": "29.00", "currency": "USD"}`.

### `shippingEstimate`

- Type: Money.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Displayed shipping estimate.
- Example: `{"amount": "5.00", "currency": "USD"}`.

### `totalEstimate`

- Type: Money.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Displayed total estimate.
- Example: `{"amount": "34.00", "currency": "USD"}`.

## AddressInput

### `firstName`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Given name.
- Example: `"Alex"`.

### `lastName`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Family name.
- Example: `"Lee"`.

### `country`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Country or region.
- Example: `"US"`.

### `company`

- Type: string.
- Required: Yes.
- Nullable: Yes.
- Default: None.
- Validation: JSON type only.
- Description: Company text or null.
- Example: `null`.

### `street`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Street address.
- Example: `"10 Sample Street"`.

### `unit`

- Type: string.
- Required: Yes.
- Nullable: Yes.
- Default: None.
- Validation: JSON type only.
- Description: Apartment text or null.
- Example: `null`.

### `city`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: City text.
- Example: `"Sample City"`.

### `state`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: State or region text.
- Example: `"CA"`.

### `postalCode`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Postal code text.
- Example: `"90001"`.

### `phone`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Telephone text.
- Example: `"+12025550123"`.

### `instructions`

- Type: string.
- Required: Yes.
- Nullable: Yes.
- Default: None.
- Validation: JSON type only.
- Description: Delivery instruction text or null.
- Example: `null`.

## Address

### `id`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Address identifier.
- Example: `"addr_01"`.

### `details`

- Type: AddressInput.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Address fields.
- Example: `{"firstName": "Alex", "lastName": "Lee", "country": "US", "company": null, "street": "10 Sample Street", "unit": null, "city": "Sample City", "state": "CA", "postalCode": "90001", "phone": "+12025550123", "instructions": null}`.

### `defaultShipping`

- Type: boolean.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Displayed default shipping flag.
- Example: `false`.

### `defaultBilling`

- Type: boolean.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Displayed default billing flag.
- Example: `false`.

## Profile

### `id`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Customer identifier.
- Example: `"cust_01"`.

### `name`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Customer display name.
- Example: `"Alex Lee"`.

### `email`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Email address syntax.
- Description: Email address.
- Example: `"alex@example.com"`.

### `phone`

- Type: string.
- Required: Yes.
- Nullable: Yes.
- Default: None.
- Validation: JSON type only.
- Description: Telephone text or null.
- Example: `null`.

## AddressBook

### `version`

- Type: integer.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Address book revision value.
- Example: `1`.

### `items`

- Type: Address[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Saved address entries.
- Example: `[]`.

## CheckoutRequest

### `cartVersion`

- Type: integer.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Cart revision value.
- Example: `1`.

### `billing`

- Type: AddressInput.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Billing fields.
- Example: `{"firstName": "Alex", "lastName": "Lee", "country": "US", "company": null, "street": "10 Sample Street", "unit": null, "city": "Sample City", "state": "CA", "postalCode": "90001", "phone": "+12025550123", "instructions": null}`.

### `shipping`

- Type: AddressInput.
- Required: Yes.
- Nullable: Yes.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Shipping fields or null.
- Example: `null`.

### `sameAsBilling`

- Type: boolean.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Address choice value.
- Example: `true`.

## CheckoutPreview

### `cartVersion`

- Type: integer.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Cart revision value.
- Example: `1`.

### `items`

- Type: CartLine[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Order summary lines.
- Example: `[]`.

### `subtotal`

- Type: Money.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Displayed subtotal.
- Example: `{"amount": "29.00", "currency": "USD"}`.

### `discount`

- Type: Money.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Displayed savings.
- Example: `{"amount": "0.00", "currency": "USD"}`.

### `shipping`

- Type: Money.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Delivery amount.
- Example: `{"amount": "5.00", "currency": "USD"}`.

### `total`

- Type: Money.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Displayed order total.
- Example: `{"amount": "34.00", "currency": "USD"}`.

### `estimatedDelivery`

- Type: string.
- Required: Yes.
- Nullable: Yes.
- Default: None.
- Validation: ISO 8601 date syntax.
- Description: ISO 8601 date or null.
- Example: `null`.

## CheckoutSubmission

### `checkout`

- Type: CheckoutRequest.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Checkout fields.
- Example: `{"cartVersion": 1, "billing": {"firstName": "Alex", "lastName": "Lee", "country": "US", "company": null, "street": "10 Sample Street", "unit": null, "city": "Sample City", "state": "CA", "postalCode": "90001", "phone": "+12025550123", "instructions": null}, "shipping": null, "sameAsBilling": true}`.

### `displayedTotal`

- Type: Money.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Displayed amount value.
- Example: `{"amount": "34.00", "currency": "USD"}`.

### `paymentMethod`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Membership in the public enum stated in the description.
- Description: Public enum: COD.
- Example: `"COD"`.

## OrderSummary

### `id`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Order identifier.
- Example: `"ord_01"`.

### `number`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Display order number.
- Example: `"EU-1001"`.

### `placedAt`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: ISO 8601 date-time syntax.
- Description: ISO 8601 timestamp.
- Example: `"2026-09-24T02:00:00Z"`.

### `status`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Membership in the public enum stated in the description.
- Description: Public enum: PLACED, IN_PROGRESS, SHIPPED, DELIVERED, CANCELLED.
- Example: `"PLACED"`.

### `paymentMethod`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Membership in the public enum stated in the description.
- Description: Public enum: COD.
- Example: `"COD"`.

### `estimatedDelivery`

- Type: string.
- Required: Yes.
- Nullable: Yes.
- Default: None.
- Validation: ISO 8601 date syntax.
- Description: ISO 8601 date or null.
- Example: `null`.

### `total`

- Type: Money.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Order amount.
- Example: `{"amount": "34.00", "currency": "USD"}`.

### `items`

- Type: CartLine[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Order line display fields.
- Example: `[]`.

## OrderEvent

### `status`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Membership in the public enum stated in the description.
- Description: Public enum: PLACED, IN_PROGRESS, SHIPPED, DELIVERED, CANCELLED.
- Example: `"PLACED"`.

### `occurredAt`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: ISO 8601 date-time syntax.
- Description: ISO 8601 timestamp.
- Example: `"2026-09-24T02:00:00Z"`.

### `message`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Timeline display message.
- Example: `"Order received."`.

## OrderDetail

### `order`

- Type: OrderSummary.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Order summary.
- Example: `{"id": "ord_01", "number": "EU-1001", "placedAt": "2026-09-24T02:00:00Z", "status": "PLACED", "paymentMethod": "COD", "estimatedDelivery": null, "total": {"amount": "34.00", "currency": "USD"}, "items": [{"id": "cl_01", "variantId": "var_01", "title": "Printed shirt", "imageUrl": "https://example.com/shirt.jpg", "color": "Black", "size": "M", "quantity": 1, "unitPrice": {"amount": "29.00", "currency": "USD"}, "lineTotal": {"amount": "29.00", "currency": "USD"}}]}`.

### `events`

- Type: OrderEvent[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Timeline entries.
- Example: `[]`.

## OrderResult

### `items`

- Type: OrderSummary[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Order summaries.
- Example: `[]`.

## Wishlist

### `items`

- Type: ProductCard[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Saved product cards.
- Example: `[]`.

### `recentlyViewed`

- Type: ProductCard[].
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Recently viewed cards.
- Example: `[]`.

## Accepted

### `accepted`

- Type: boolean.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Public acknowledgement.
- Example: `true`.

## Confirmation

### `orderId`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Order identifier.
- Example: `"ord_01"`.

### `message`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Confirmation display message.
- Example: `"Your Order is Confirmed"`.

## ResetEmail

### `email`

- Type: string.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Email address syntax.
- Description: Email address.
- Example: `"alex@example.com"`.


## NewAddress

### `details`

- Type: AddressInput.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: Object or array shape defined in common-contract.md.
- Description: Address fields.
- Example: `{"firstName": "Alex", "lastName": "Lee", "country": "US", "company": null, "street": "10 Sample Street", "unit": null, "city": "Sample City", "state": "CA", "postalCode": "90001", "phone": "+12025550123", "instructions": null}`.

### `defaultShipping`

- Type: boolean.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Checkbox value.
- Example: `false`.

### `defaultBilling`

- Type: boolean.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Checkbox value.
- Example: `false`.

### `expectedVersion`

- Type: integer.
- Required: Yes.
- Nullable: No.
- Default: None.
- Validation: JSON type only.
- Description: Address book revision value.
- Example: `1`.

