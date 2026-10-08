---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-09
uc_name: "Manage Wishlist"
---

# UC-09: Manage Wishlist

## Functional Use-Case Specification

### Use Case ID

UC-09

### Use Case Name

Manage Wishlist

### Description

- Allows a visitor or customer to save selected product configurations, view their current prices and stock status, remove saved configurations, and add an available saved configuration to the shopping cart.
- Connects UC-05's Add to Wishlist action, the shared Wishlist navigation, and UC-06's existing cart API.
- Variant-level identity, browser persistence, limits, API contracts, and interaction behavior below are project decisions. Figma establishes the inspected desktop list and visible actions.
- This UC does not create orders, reserve inventory, send stock/price notifications, share wishlists, or synchronize lists across accounts/devices.

### Actor(s)

Visitor or signed-in Customer using the same browser context.

### Priority

Medium

### Trigger

The actor opens the Manage Wishlist interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=418-11632)

### Related API IDs

- [API-WISHLIST-ITEM-SAVE](../api/API-WISHLIST-ITEM-SAVE.md)
- [API-WISHLIST-GET](../api/API-WISHLIST-GET.md)
- [API-WISHLIST-CART-ITEM-CREATE](../api/API-WISHLIST-CART-ITEM-CREATE.md)
- [API-WISHLIST-ITEM-DELETE](../api/API-WISHLIST-ITEM-DELETE.md)
- [API-WISHLIST-CART-GET](../api/API-WISHLIST-CART-GET.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [clicon-uc-09-manage-wishlist.md](../../source/clicon-uc-09-manage-wishlist.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-WISHLIST-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_WISHLIST_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-WISHLIST-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_WISHLIST_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-WISHLIST-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_WISHLIST_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-WISHLIST-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_WISHLIST_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-WISHLIST-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_WISHLIST_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-WISHLIST-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_WISHLIST_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-WISHLIST-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_WISHLIST_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
