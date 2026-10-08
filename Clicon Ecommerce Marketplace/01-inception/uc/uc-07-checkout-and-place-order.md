---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-07
uc_name: "Checkout and Place Order"
---

# UC-07: Checkout and Place Order

## Functional Use-Case Specification

### Use Case ID

UC-07

### Use Case Name

Checkout and Place Order

### Description

- Allows a visitor or customer to provide billing/delivery information, review a checkout quote, and place a Cash on Delivery order from the saved UC-06 cart.
- Includes the checkout form, order creation, and reloadable order-confirmation screen. Continues UC-06 without requiring account registration or login.
- Payment availability, delivery coverage, quote lifetime, pricing, order rules, and API contracts are project decisions. The inspected Figma frames establish desktop layout and visible controls.
- Online payment, coupons, order history/details, tracking, cancellation, email notifications, and saved address management are separate use cases or integrations. Cash on Delivery placement does not imply that payment has been collected.

### Actor(s)

Visitor or signed-in Customer with a browser cart.

### Priority

High

### Trigger

The actor opens the Checkout and Place Order interface.

### Pre-Condition(s)

PRE-1: The interaction interface is visible to the actor.

### Post-Condition(s)

POST-1: The client displays the returned interaction outcome.

### Basic Flow

1. The actor opens the interaction interface.
2. The client displays the available controls.
3. The actor submits the interaction.
4. The client sends the request to the system.
5. The system returns an outcome.
6. The client displays the returned outcome.

### Alternative Flow

AF-1: Choose an alternative action

3a: The actor chooses an available alternative action.

3b: The client displays the returned alternative outcome.

### Exception Flow

EF-1: Unsuccessful interaction outcome

5a: The system returns an unsuccessful outcome.

5b: The client displays the returned recovery message.

### Related UI

- [Supporting Figma node 1](https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=493-15194)
- [Supporting Figma node 2](https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=510-16556)

### Related API IDs

- [API-CHECKOUT-OPTION-LIST](../api/API-CHECKOUT-OPTION-LIST.md)
- [API-CHECKOUT-QUOTE-CREATE](../api/API-CHECKOUT-QUOTE-CREATE.md)
- [API-CHECKOUT-QUOTE-DETAIL](../api/API-CHECKOUT-QUOTE-DETAIL.md)
- [API-ORDER-CREATE](../api/API-ORDER-CREATE.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [clicon-uc-07-checkout-and-place-order.md](../../source/clicon-uc-07-checkout-and-place-order.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

## UML Model

~~~plantuml
@startuml
hide empty members

enum ExecutionStatus {
  REQUESTED
  COMPLETED
  REJECTED
}

class UseCaseCommand {
  +actorId: String
  +requestId: String
  +payload: String
}

class UseCaseResult {
  +executionId: String
  +actorId: String
  +requestId: String
  +status: ExecutionStatus
  +createdAt: DateTime
  +version: Integer
}

class UseCaseService {
  +execute(command: UseCaseCommand): UseCaseResult
}

class DateTime <<primitive>> {
  +{static} now(): DateTime
}

UseCaseService ..> UseCaseCommand
UseCaseService ..> UseCaseResult
UseCaseResult --> "1" ExecutionStatus : status

@enduml
~~~

## Business Rules

~~~text
BR-CHECKOUT-ORDER-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_CHECKOUT_ORDER_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-CHECKOUT-ORDER-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_CHECKOUT_ORDER_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-CHECKOUT-ORDER-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_CHECKOUT_ORDER_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-CHECKOUT-ORDER-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_CHECKOUT_ORDER_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-CHECKOUT-ORDER-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_CHECKOUT_ORDER_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-CHECKOUT-ORDER-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_CHECKOUT_ORDER_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-CHECKOUT-ORDER-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_CHECKOUT_ORDER_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
