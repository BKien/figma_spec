---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-06
uc_name: "Manage Shopping Cart"
---

# UC-06: Manage Shopping Cart

## Functional Use-Case Specification

### Use Case ID

UC-06

### Use Case Name

Manage Shopping Cart

### Description

- Allows a visitor or customer to add a selected product configuration to a shopping cart, inspect its contents, change quantities, and remove items before checkout.
- Continues UC-05 through its selected variant and quantity. Includes the cart page and shared header cart count.
- Cart persistence, staged editing, pricing rules, and API contracts below are project decisions. Figma establishes the inspected desktop controls and layout, not their backend behavior.
- Coupon application, shipping/tax quotation, checkout, Buy Now, and the homepage cart popup belong to separate integrations. This UC does not reserve stock or create an order.

### Actor(s)

Visitor or signed-in Customer using the same browser.

### Priority

High

### Trigger

The actor opens the Manage Shopping Cart interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=493-14954)

### Related API IDs

- [API-CART-ITEM-CREATE](../api/API-CART-ITEM-CREATE.md)
- [API-CART-GET](../api/API-CART-GET.md)
- [API-CART-UPDATE](../api/API-CART-UPDATE.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [clicon-uc-06-manage-shopping-cart.md](../../source/clicon-uc-06-manage-shopping-cart.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-SHOPPING-CART-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SHOPPING_CART_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-SHOPPING-CART-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SHOPPING_CART_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-SHOPPING-CART-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SHOPPING_CART_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-SHOPPING-CART-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SHOPPING_CART_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-SHOPPING-CART-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SHOPPING_CART_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-SHOPPING-CART-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SHOPPING_CART_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-SHOPPING-CART-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SHOPPING_CART_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
