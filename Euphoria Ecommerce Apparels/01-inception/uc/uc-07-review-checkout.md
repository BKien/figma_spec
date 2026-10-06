---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-07
uc_name: "Enter billing details and review checkout"
---

# UC-07: Enter billing details and review checkout

## Functional Use-Case Specification

### Use Case ID

UC-07

### Use Case Name

Enter billing details and review checkout

### Description

Enter billing details and review the delivery information and order summary before submitting an order.

### Actor(s)

Primary: Shopper. Supporting: web client and application service.

### Priority

High.

### Trigger

The shopper chooses Proceed Check Out from the cart.

### Pre-Condition(s)

PRE-1: The checkout screen is open.

### Post-Condition(s)

POST-1: The client displays the returned checkout summary and delivery information.

### Basic Flow

1. The shopper chooses Proceed Check Out.
2. The client displays the billing form and cart summary.
3. The shopper enters billing details and chooses Same as Billing address.
4. The shopper chooses Continue to delivery.
5. The client submits the checkout details.
6. The system returns the checkout summary.
7. The client displays the returned amounts and delivery information.

### Alternative Flow

AF-1:

1. The shopper returns to the billing fields and edits the details.
2. The shopper chooses Continue to delivery again.
3. The client displays the returned checkout summary.

### Exception Flow

EF-1:

1. The system returns an operation conflict.
2. The client requests a refreshed cart and checkout summary.
3. The client shows the returned summary and asks the shopper to review it before submitting again.

### Related UI

- [Figma node 181:393](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=181-393)
- [Figma node 235:1056](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=235-1056)

### Related API IDs

- [API-CART](../api/api-cart.md)
- [API-CHECKOUT-PREVIEW](../api/api-checkout-preview.md)

### Notes

Screen and text-layer evidence establishes the visible goal. Service decomposition, request shapes, and exception recovery are proposed implementation contracts; they are not extracted server behavior. See [assumptions](../../ASSUMPTIONS.md) and [coverage](../../coverage-report.md) for the supported boundary. No prototype interaction wiring was available for verification.

## UML Model

~~~plantuml
@startuml
hide empty members

class CheckoutService {
  +preview(ctx: RequestContext, input: CheckoutInput): CheckoutPreview
  currency: String
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
  subtotal: Money
}

class CartLine {
  id: String
}

class CheckoutInput <<input>> {
  cart: Cart
  cartVersion: Integer
  billing: AddressFields
  shipping: AddressFields [0..1]
  sameAsBilling: Boolean
}

class CheckoutPreview <<response>> {
  cartVersion: Integer
  items: Sequence(CartLine)
  subtotal: Money
  discount: Money
  shipping: Money
  total: Money
}

class CheckoutReceipt {
  id: String
}

class Money <<value>> {
  amount: Real
  currency: String
}

class Order {
  id: String
}

class RequestContext <<input>> {
  customerId: String
  authenticated: Boolean
}

Cart "1" *-- "0..*" CartLine
Cart --> "1" Money : subtotal
CheckoutInput --> "1" Cart : cart
CheckoutInput --> "1" AddressFields : billing
CheckoutInput --> "0..1" AddressFields : shipping
CheckoutPreview --> "0..*" CartLine : items
CheckoutPreview --> "1" Money : subtotal
CheckoutPreview --> "1" Money : discount
CheckoutPreview --> "1" Money : shipping
CheckoutPreview --> "1" Money : total

@enduml
~~~

## Business Rules

~~~ocl
-- BR-UC-07-01
-- Source: Assumption
context CheckoutService::preview(ctx: RequestContext, input: CheckoutInput): CheckoutPreview
pre BR_UC_07_01_AccountCart:
  ctx.authenticated and input.cart.customerId = ctx.customerId
~~~
~~~ocl
-- BR-UC-07-02
-- Source: Assumption
context CheckoutService::preview(ctx: RequestContext, input: CheckoutInput): CheckoutPreview
pre BR_UC_07_02_CartRevision:
  input.cartVersion = input.cart.version and input.cart.items->notEmpty()
~~~
~~~ocl
-- BR-UC-07-03
-- Source: Assumption
context CheckoutService::preview(ctx: RequestContext, input: CheckoutInput): CheckoutPreview
pre BR_UC_07_03_AddressValues:
  AddressValidation::valid(input.billing) and input.sameAsBilling and input.shipping = null
~~~
~~~ocl
-- BR-UC-07-04
-- Source: Assumption
context CheckoutService::preview(ctx: RequestContext, input: CheckoutInput): CheckoutPreview
post BR_UC_07_04_CartSnapshot:
  result.cartVersion = input.cartVersion and result.items = input.cart.items and result.subtotal = input.cart.subtotal
~~~
~~~ocl
-- BR-UC-07-05
-- Source: Assumption
context CheckoutService::preview(ctx: RequestContext, input: CheckoutInput): CheckoutPreview
post BR_UC_07_05_DeliveryAndSavings:
  result.discount.amount = 0 and result.shipping.amount = self.deliveryCharge
~~~
~~~ocl
-- BR-UC-07-06
-- Source: Assumption
context CheckoutService::preview(ctx: RequestContext, input: CheckoutInput): CheckoutPreview
post BR_UC_07_06_TotalAmount:
  result.total.amount = result.subtotal.amount - result.discount.amount + result.shipping.amount
~~~
~~~ocl
-- BR-UC-07-07
-- Source: Assumption
context CheckoutService::preview(ctx: RequestContext, input: CheckoutInput): CheckoutPreview
post BR_UC_07_07_Currency:
  result.total.currency = self.currency and result.subtotal.currency = self.currency and result.discount.currency = self.currency and result.shipping.currency = self.currency
~~~
~~~ocl
-- BR-UC-07-08
-- Source: Assumption
context CheckoutService
inv BR_UC_07_08_ProvisionalConfiguration:
  self.currency = 'USD' and self.deliveryCharge = 5.00
~~~
~~~ocl
-- BR-UC-07-09
-- Source: Assumption
context CheckoutService::preview(ctx: RequestContext, input: CheckoutInput): CheckoutPreview
post BR_UC_07_09_NoOrderCreation:
  Order.allInstances() = Order.allInstances()@pre and CheckoutReceipt.allInstances() = CheckoutReceipt.allInstances()@pre and input.cart.items = input.cart.items@pre and input.cart.version = input.cart.version@pre
~~~
