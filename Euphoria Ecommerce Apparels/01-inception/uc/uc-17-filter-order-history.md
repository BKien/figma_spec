---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-17
uc_name: "Filter orders by status"
---

# UC-17: Filter orders by status

## Functional Use-Case Specification

### Use Case ID

UC-17

### Use Case Name

Filter orders by status

### Description

Switch between Active, Cancelled, and Completed order-history views.

### Actor(s)

Primary: Customer. Supporting: web client and application service.

### Priority

Medium.

### Trigger

The customer chooses an order-history tab.

### Pre-Condition(s)

PRE-1: My Orders and its tabs are displayed.

### Post-Condition(s)

POST-1: The client displays the returned order-history view.

### Basic Flow

1. The customer chooses Active, Cancelled, or Completed.
2. The client requests the chosen view.
3. The system returns order summaries.
4. The client displays the summaries and highlights the chosen tab.

### Alternative Flow

AF-1:

1. The customer chooses a different tab.
2. The client requests and displays that view.

### Exception Flow

EF-1:

1. The system returns a temporary service failure.
2. The client presents a retry action in the order list.

### Related UI

- [Figma node 290:1372](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=290-1372)

### Related API IDs

- [API-ORDERS](../api/api-orders.md)

### Notes

Screen and text-layer evidence establishes the visible goal. Service decomposition, request shapes, and exception recovery are proposed implementation contracts; they are not extracted server behavior. See [assumptions](../../ASSUMPTIONS.md) and [coverage](../../coverage-report.md) for the supported boundary. No prototype interaction wiring was available for verification.

## UML Model

~~~plantuml
@startuml
hide empty members

class OrderService {
  +list(ctx: RequestContext, tab: OrderTab): Sequence(Order)
}

class Money <<value>> {
  amount: Real
  currency: String
}

class Order {
  customerId: String
  status: OrderStatus
  paymentMethod: PaymentMethod
  version: Integer
  total: Money
}

class OrderEvent {
  status: OrderStatus
  occurredAt: Integer
  message: String
}

enum OrderStatus {
  PLACED
  IN_PROGRESS
  SHIPPED
  DELIVERED
  CANCELLED
}

enum OrderTab {
  ACTIVE
  CANCELLED
  COMPLETED
}

enum PaymentMethod {
  COD
}

class RequestContext <<input>> {
  customerId: String
}

Order --> "1" OrderStatus : status
Order --> "1" PaymentMethod : paymentMethod
Order --> "1" Money : total
OrderEvent --> "1" OrderStatus : status

@enduml
~~~

## Business Rules

~~~ocl
-- BR-UC-17-01
-- Source: Assumption
context OrderService::list(ctx: RequestContext, tab: OrderTab): Sequence(Order)
post BR_UC_17_01_ActiveMembership:
  tab = OrderTab::ACTIVE implies result->forAll(o | Set{OrderStatus::PLACED, OrderStatus::IN_PROGRESS, OrderStatus::SHIPPED}->includes(o.status))
~~~
~~~ocl
-- BR-UC-17-02
-- Source: Assumption
context OrderService::list(ctx: RequestContext, tab: OrderTab): Sequence(Order)
post BR_UC_17_02_CancelledMembership:
  tab = OrderTab::CANCELLED implies result->forAll(o | o.status = OrderStatus::CANCELLED)
~~~
~~~ocl
-- BR-UC-17-03
-- Source: Assumption
context OrderService::list(ctx: RequestContext, tab: OrderTab): Sequence(Order)
post BR_UC_17_03_CompletedMembership:
  tab = OrderTab::COMPLETED implies result->forAll(o | o.status = OrderStatus::DELIVERED)
~~~
~~~ocl
-- BR-UC-17-04
-- Source: Assumption
context OrderService::list(ctx: RequestContext, tab: OrderTab): Sequence(Order)
post BR_UC_17_04_TabMembership:
  result->asSet() = Order.allInstances()->select(o | o.customerId = ctx.customerId and (if tab = OrderTab::ACTIVE then Set{OrderStatus::PLACED, OrderStatus::IN_PROGRESS, OrderStatus::SHIPPED}->includes(o.status) else if tab = OrderTab::COMPLETED then o.status = OrderStatus::DELIVERED else o.status = OrderStatus::CANCELLED endif endif))
~~~
~~~ocl
-- BR-UC-17-05
-- Source: Assumption
context OrderService::list(ctx: RequestContext, tab: OrderTab): Sequence(Order)
post BR_UC_17_05_NoCancellationAction:
  Order.allInstances() = Order.allInstances()@pre and Order.allInstances()->forAll(o | o.status = o.status@pre and o.version = o.version@pre)
~~~
~~~ocl
-- BR-UC-17-06
-- Source: Assumption
context OrderService::list(ctx: RequestContext, tab: OrderTab): Sequence(Order)
post BR_UC_17_06_EventsPreserved:
  OrderEvent.allInstances() = OrderEvent.allInstances()@pre and OrderEvent.allInstances()->forAll(e | e.status = e.status@pre and e.occurredAt = e.occurredAt@pre and e.message = e.message@pre)
~~~
~~~ocl
-- BR-UC-17-07
-- Source: Assumption
context OrderService::list(ctx: RequestContext, tab: OrderTab): Sequence(Order)
post BR_UC_17_07_PaymentChoicePreserved:
  Order.allInstances()->forAll(o | o.paymentMethod = o.paymentMethod@pre and o.total = o.total@pre)
~~~
