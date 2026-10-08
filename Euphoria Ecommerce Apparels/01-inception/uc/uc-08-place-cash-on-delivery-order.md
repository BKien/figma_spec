---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-08
uc_name: "Place a cash-on-delivery order"
---

# UC-08: Place a cash-on-delivery order

## Functional Use-Case Specification

### Use Case ID

UC-08

### Use Case Name

Place a cash-on-delivery order

### Description

Submit the reviewed checkout using Cash on delivery and read the resulting order confirmation.

### Actor(s)

Primary: Shopper. Supporting: web client and application service.

### Priority

High.

### Trigger

The shopper chooses Pay Now after selecting Cash on delivery.

### Pre-Condition(s)

PRE-1: The checkout summary and payment choices are displayed.

### Post-Condition(s)

POST-1: The client displays the returned order confirmation.

### Basic Flow

1. The shopper selects Cash on delivery.
2. The shopper chooses Pay Now.
3. The client submits the checkout request.
4. The system returns the order confirmation.
5. The client displays Your Order is Confirmed.

### Alternative Flow

AF-1: Return to billing details

2a: The shopper returns to the billing details.

2b: The client displays the checkout form.

### Exception Flow

EF-1: Review refreshed checkout summary

4a: The system returns an operation conflict.

4b: The client requests a refreshed cart and checkout summary.

4c: The client shows the returned summary and asks the shopper to review it before submitting again.

### Related UI

- [Figma node 235:1056](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=235-1056)
- [Figma node 273:839](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=273-839)
- [Figma node 181:393](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=181-393)

### Related API IDs

- [API-CART](../api/API-CART.md)
- [API-CHECKOUT-PREVIEW](../api/API-CHECKOUT-PREVIEW.md)
- [API-ORDER-CREATE](../api/API-ORDER-CREATE.md)

### Notes

Screen and text-layer evidence establishes the visible goal. Service decomposition, request shapes, and exception recovery are proposed implementation contracts; they are not extracted server behavior. See [assumptions](../../ASSUMPTIONS.md) and [coverage](../../coverage-report.md) for the supported boundary. No prototype interaction wiring was available for verification.

## UML Model

~~~plantuml
@startuml
hide empty members

class CheckoutService {
  +preview(ctx: RequestContext, input: CheckoutInput): CheckoutPreview
  +place(ctx: RequestContext, input: CheckoutInput, key: String, displayedTotal: Money): Order
  deliveryCharge: Real
}

class AddressFields <<value>> {
  firstName: String
  lastName: String
  country: String
  company: String [0..1]
  street: String
  unit: String [0..1]
  city: String
  state: String
  postalCode: String
  phone: String
  instructions: String [0..1]
}

class AddressValidation <<primitive helper>> {
  {static} +valid(input: AddressFields): Boolean
}

class Cart {
  customerId: String
  version: Integer
  items: Sequence(CartLine)
}

class CartLine {
  variantId: String
  variant: Variant
  title: String
  imageUrl: String
  size: String
  color: String
  quantity: Integer
  unitPrice: Money
  lineTotal: Money
}

class CheckoutInput <<input>> {
  cart: Cart
  cartVersion: Integer
  billing: AddressFields
  shipping: AddressFields [0..1]
  sameAsBilling: Boolean
}

class CheckoutPreview <<response>> {
  total: Money
}

class CheckoutReceipt {
  customerId: String
  key: String
  requestDigest: String
  order: Order
}

class Clock <<primitive helper>> {
  {static} +now(): Integer
}

class Digest <<primitive helper>> {
  {static} +checkout(input: CheckoutInput, displayedTotal: Money): String
}

class Money <<value>> {
  amount: Real
  currency: String
}

class Order {
  id: String
  number: String
  customerId: String
  placedAt: Integer
  status: OrderStatus
  paymentMethod: PaymentMethod
  version: Integer
  billing: AddressFields
  shipping: AddressFields
  items: Sequence(OrderLine)
  events: Set(OrderEvent)
  subtotal: Money
  discount: Money
  shippingCharge: Money
  total: Money
}

class OrderEvent {
  orderId: String
  status: OrderStatus
  occurredAt: Integer
}

class OrderLine {
  orderId: String
  variantId: String
  title: String
  imageUrl: String
  size: String
  color: String
  quantity: Integer
  unitPrice: Money
}

enum OrderStatus {
  PLACED
  IN_PROGRESS
  SHIPPED
  DELIVERED
  CANCELLED
}

enum PaymentMethod {
  COD
}

class RequestContext <<input>> {
  customerId: String
  authenticated: Boolean
  csrfValid: Boolean
}

class Variant {
  id: String
  price: Money
  sellable: Boolean
  stock: Integer
  version: Integer
}

Cart "1" *-- "0..*" CartLine
CartLine "0..*" --> "1" Variant
Order "1" *-- "1..*" OrderLine
Order "1" *-- "1..*" OrderEvent
Order "1" -- "1" CheckoutReceipt
CartLine --> "1" Money : unitPrice
CartLine --> "1" Money : lineTotal
CheckoutInput --> "1" Cart : cart
CheckoutInput --> "1" AddressFields : billing
CheckoutInput --> "0..1" AddressFields : shipping
CheckoutPreview --> "1" Money : total
Order --> "1" OrderStatus : status
Order --> "1" PaymentMethod : paymentMethod
Order --> "1" AddressFields : billing
Order --> "1" AddressFields : shipping
Order --> "1" Money : subtotal
Order --> "1" Money : discount
Order --> "1" Money : shippingCharge
Order --> "1" Money : total
OrderEvent --> "1" OrderStatus : status
OrderLine --> "1" Money : unitPrice
Variant --> "1" Money : price

@enduml
~~~

## Business Rules

~~~text
BR-COD-ORDER-01 - Identity
Source: Assumption
context CheckoutService::place(ctx: RequestContext, input: CheckoutInput, key: String, displayedTotal: Money): Order
pre BR_COD_ORDER_01_Identity:
  ctx.authenticated and input.cart.customerId = ctx.customerId and key.size() > 0
~~~
~~~text
BR-COD-ORDER-02 - New Or Replay
Source: Assumption
context CheckoutService::place(ctx: RequestContext, input: CheckoutInput, key: String, displayedTotal: Money): Order
pre BR_COD_ORDER_02_NewOrReplay:
  let receipts : Set(CheckoutReceipt) = CheckoutReceipt.allInstances()->select(r | r.customerId = ctx.customerId and r.key = key) in if receipts->notEmpty() then receipts->forAll(r | r.requestDigest = Digest::checkout(input, displayedTotal)) else input.cartVersion = input.cart.version and input.cart.items->notEmpty() and AddressValidation::valid(input.billing) and (input.sameAsBilling or (input.shipping <> null and AddressValidation::valid(input.shipping))) and input.cart.items->forAll(l | l.variant.sellable and l.variant.stock >= l.quantity and l.unitPrice = l.variant.price) and displayedTotal = self.preview(ctx, input).total endif
~~~
~~~text
BR-COD-ORDER-03 - Replay Or Create
Source: Assumption
context CheckoutService::place(ctx: RequestContext, input: CheckoutInput, key: String, displayedTotal: Money): Order
post BR_COD_ORDER_03_ReplayOrCreate:
  let prior : Set(CheckoutReceipt) = CheckoutReceipt.allInstances()@pre->select(r | r.customerId = ctx.customerId and r.key = key) in if prior->notEmpty() then result = prior->any(true).order else result.oclIsNew() and result.customerId = ctx.customerId and result.status = OrderStatus::PLACED and result.paymentMethod = PaymentMethod::COD and result.total = displayedTotal and result.billing = input.billing and result.shipping = (if input.sameAsBilling then input.billing else input.shipping endif) and result.items->size() = input.cart.items@pre->size() and result.items->forAll(o | input.cart.items@pre->one(c | o.variantId = c.variantId and o.quantity = c.quantity and o.unitPrice = c.unitPrice and o.title = c.title)) and input.cart.items->isEmpty() and input.cart.version = input.cart.version@pre + 1 endif
~~~
~~~text
BR-COD-ORDER-04 - Receipt And Stock
Source: Assumption
context CheckoutService::place(ctx: RequestContext, input: CheckoutInput, key: String, displayedTotal: Money): Order
post BR_COD_ORDER_04_ReceiptAndStock:
  let prior : Set(CheckoutReceipt) = CheckoutReceipt.allInstances()@pre->select(r | r.customerId = ctx.customerId and r.key = key) in if prior->isEmpty() then CheckoutReceipt.allInstances()->one(r | r.oclIsNew() and r.customerId = ctx.customerId and r.key = key and r.order = result and r.requestDigest = Digest::checkout(input, displayedTotal)) and Variant.allInstances()->forAll(v | v.stock = v.stock@pre - input.cart.items@pre->select(l | l.variantId = v.id)->collect(l | l.quantity)->sum()) else Variant.allInstances()->forAll(v | v.stock = v.stock@pre) and input.cart.items = input.cart.items@pre and input.cart.version = input.cart.version@pre endif
~~~
~~~text
BR-COD-ORDER-05 - Receipt Identity
Source: Assumption
context CheckoutReceipt
inv BR_COD_ORDER_05_ReceiptIdentity:
  CheckoutReceipt.allInstances()->isUnique(r | Tuple{customerId = r.customerId, key = r.key})
~~~
~~~text
BR-COD-ORDER-06 - Request Binding
Source: Assumption
context CheckoutService::place(ctx: RequestContext, input: CheckoutInput, key: String, displayedTotal: Money): Order
pre BR_COD_ORDER_06_RequestBinding:
  ctx.csrfValid
~~~
~~~text
BR-COD-ORDER-07 - Initial Snapshot
Source: Assumption
context CheckoutService::place(ctx: RequestContext, input: CheckoutInput, key: String, displayedTotal: Money): Order
post BR_COD_ORDER_07_InitialSnapshot:
  if result.oclIsNew() then result.subtotal.amount = input.cart.items@pre->collect(l | l.lineTotal.amount)->sum() and result.discount.amount = 0 and result.shippingCharge.amount = self.deliveryCharge and result.placedAt = Clock::now() and result.version = 0 and result.events->one(e | e.oclIsNew() and e.status = OrderStatus::PLACED and e.occurredAt = result.placedAt and e.orderId = result.id) and result.items->forAll(o | input.cart.items@pre->one(c | o.variantId = c.variantId and o.size = c.size and o.color = c.color and o.imageUrl = c.imageUrl)) else result.items = result.items@pre and result.events = result.events@pre endif
~~~
~~~text
BR-COD-ORDER-08 - Atomic Commit
Source: Assumption
Note: The operation is atomic across the cart, inventory, order, lines, addresses, event and receipt.
Note: Concurrent calls serialize the receipt key and cart revision checks with these writes.
context CheckoutService::place(ctx: RequestContext, input: CheckoutInput, key: String, displayedTotal: Money): Order
post BR_COD_ORDER_08_AtomicCommit:
  if result.oclIsNew() then Order.allInstances() = Order.allInstances()@pre->including(result) and Variant.allInstances()->forAll(v | v.version = v.version@pre + (if input.cart.items@pre->exists(l | l.variantId = v.id) then 1 else 0 endif)) else Order.allInstances() = Order.allInstances()@pre and CheckoutReceipt.allInstances() = CheckoutReceipt.allInstances()@pre and Variant.allInstances()->forAll(v | v.version = v.version@pre) endif
~~~
~~~text
BR-COD-ORDER-09 - Public Identity
Source: Assumption
context Order
inv BR_COD_ORDER_09_PublicIdentity:
  Order.allInstances()->isUnique(number) and self.items->isUnique(variantId) and self.items->forAll(l | l.orderId = self.id)
~~~
~~~text
BR-COD-ORDER-10 - Supported Address Choice
Source: Assumption
context CheckoutService::place(ctx: RequestContext, input: CheckoutInput, key: String, displayedTotal: Money): Order
pre BR_COD_ORDER_10_SupportedAddressChoice:
  input.sameAsBilling and input.shipping = null
~~~
~~~text
BR-COD-ORDER-11 - Stock And Revision
Source: Assumption
context Variant
inv BR_COD_ORDER_11_StockAndRevision:
  self.stock >= 0 and self.version >= 0 and self.price.amount >= 0
~~~
