---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-06
uc_name: "Review the cart"
---

# UC-06: Review the cart

## Functional Use-Case Specification

### Use Case ID

UC-06

### Use Case Name

Review the cart

### Description

Review product lines, quantities, and the subtotal, including the dedicated empty-cart state.

### Actor(s)

Primary: Shopper. Supporting: web client and application service.

### Priority

High.

### Trigger

The shopper opens the cart.

### Pre-Condition(s)

PRE-1: The cart route is open in the client.

### Post-Condition(s)

POST-1: The client displays the returned cart or the empty-cart state.

### Basic Flow

1. The shopper opens the cart.
2. The client requests the cart.
3. The system returns cart lines and the subtotal.
4. The client displays product details, selected options, quantities, subtotal, shipping estimate, and total estimate.
5. The shopper chooses Proceed Check Out.
6. The client opens checkout.

### Alternative Flow

AF-1: Empty cart

3a: The system returns a cart with no lines.

3b: The client displays the empty-cart message.

3c: The shopper returns to shopping.

### Exception Flow

EF-1: Sign in to view the cart

3d: The system returns a rejected authentication context.

3e: The client presents the sign-in entry point.

### Related UI

- [Figma node 181:393](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=181-393)
- [Figma node 190:423](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=190-423)

### Related API IDs

- [API-CART](../api/API-CART.md)

### Notes

Screen and text-layer evidence establishes the visible goal. Service decomposition, request shapes, and exception recovery are proposed implementation contracts; they are not extracted server behavior. See [assumptions](../../ASSUMPTIONS.md) and [coverage](../../coverage-report.md) for the supported boundary. No prototype interaction wiring was available for verification.

## UML Model

~~~plantuml
@startuml
hide empty members

class CartService {
  +read(ctx: RequestContext): Cart
}

class Cart {
  customerId: String
  version: Integer
  items: Sequence(CartLine)
  subtotal: Money
  shippingEstimate: Money
  totalEstimate: Money
}

class CartLine {
  variantId: String
  quantity: Integer
  unitPrice: Money
  lineTotal: Money
}

class Money <<value>> {
  amount: Real
  currency: String
}

class RequestContext <<input>> {
  customerId: String
  authenticated: Boolean
}

Cart "1" *-- "0..*" CartLine
Cart --> "1" Money : subtotal
Cart --> "1" Money : shippingEstimate
Cart --> "1" Money : totalEstimate
CartLine --> "1" Money : unitPrice
CartLine --> "1" Money : lineTotal

@enduml
~~~

## Business Rules

~~~text
BR-REVIEW-CART-01 - Account Context
Source: Assumption
context CartService::read(ctx: RequestContext): Cart
pre BR_REVIEW_CART_01_AccountContext:
  ctx.authenticated
~~~
~~~text
BR-REVIEW-CART-02 - Customer Cart
Source: Assumption
context CartService::read(ctx: RequestContext): Cart
post BR_REVIEW_CART_02_CustomerCart:
  result.customerId = ctx.customerId
~~~
~~~text
BR-REVIEW-CART-03 - Quantity And Amount
Source: Assumption
context CartLine
inv BR_REVIEW_CART_03_QuantityAndAmount:
  self.quantity > 0 and self.unitPrice.amount >= 0
~~~
~~~text
BR-REVIEW-CART-04 - Currency Consistency
Source: Assumption
context Cart
inv BR_REVIEW_CART_04_CurrencyConsistency:
  self.items->forAll(l | l.unitPrice.currency = self.subtotal.currency and l.lineTotal.currency = self.subtotal.currency)
~~~
~~~text
BR-REVIEW-CART-05 - Line Amount
Source: Assumption
context CartLine
inv BR_REVIEW_CART_05_LineAmount:
  self.lineTotal.amount = self.quantity * self.unitPrice.amount
~~~
~~~text
BR-REVIEW-CART-06 - Subtotal
Source: Assumption
context Cart
inv BR_REVIEW_CART_06_Subtotal:
  self.subtotal.amount = self.items->collect(l | l.lineTotal.amount)->sum()
~~~
~~~text
BR-REVIEW-CART-07 - One Variant Line
Source: Assumption
context Cart
inv BR_REVIEW_CART_07_OneVariantLine:
  self.items->isUnique(variantId) and self.version >= 0
~~~
~~~text
BR-REVIEW-CART-08 - Display Estimates
Source: Assumption
context Cart
inv BR_REVIEW_CART_08_DisplayEstimates:
  self.shippingEstimate.amount = (if self.items->isEmpty() then 0 else 5.00 endif) and self.shippingEstimate.currency = self.subtotal.currency and self.totalEstimate.currency = self.subtotal.currency and self.totalEstimate.amount = self.subtotal.amount + self.shippingEstimate.amount
~~~
