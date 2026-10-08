---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-10
uc_name: "Compare Products"
---

# UC-10: Compare Products

## Functional Use-Case Specification

### Use Case ID

UC-10

### Use Case Name

Compare Products

### Description

- Allows a visitor or customer to save up to three selected product configurations for side-by-side comparison of customer feedback, price, seller, brand, model, stock status, size, and weight.
- Connects UC-05's Add to Compare control, shared Compare navigation, UC-06's cart operation, and UC-09's wishlist actions.
- Variant identity, capacity, persistence, missing-data rules, and API contracts are project decisions. Figma establishes the inspected desktop comparison table and controls.
- This UC does not recommend a winner, normalize incomparable measurements, create reviews, manage sellers, reserve stock, or create an order.

### Actor(s)

Visitor or signed-in Customer using the same browser context.

### Priority

Medium

### Trigger

The actor opens the Compare Products interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=493-14714)

### Related API IDs

- [API-COMPARISON-ITEM-SAVE](../api/API-COMPARISON-ITEM-SAVE.md)
- [API-COMPARISON-GET](../api/API-COMPARISON-GET.md)
- [API-COMPARISON-ITEM-DELETE](../api/API-COMPARISON-ITEM-DELETE.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [clicon-uc-10-compare-products.md](../../source/clicon-uc-10-compare-products.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-COMPARE-PRODUCTS-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_COMPARE_PRODUCTS_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-COMPARE-PRODUCTS-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_COMPARE_PRODUCTS_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-COMPARE-PRODUCTS-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_COMPARE_PRODUCTS_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-COMPARE-PRODUCTS-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_COMPARE_PRODUCTS_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-COMPARE-PRODUCTS-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_COMPARE_PRODUCTS_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-COMPARE-PRODUCTS-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_COMPARE_PRODUCTS_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-COMPARE-PRODUCTS-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_COMPARE_PRODUCTS_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
