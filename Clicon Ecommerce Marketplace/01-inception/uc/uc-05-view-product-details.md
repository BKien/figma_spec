---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-05
uc_name: "View Product Details"
---

# UC-05: View Product Details

## Functional Use-Case Specification

### Use Case ID

UC-05

### Use Case Name

View Product Details

### Description

- Allows a visitor or customer to inspect a published product, browse its images, select an available product configuration, and read product information before deciding whether to purchase.
- Continues UC-04 through product-card navigation. Includes read-only image/configuration selection, information tabs, related-product navigation, and copying the product link.
- Adding to cart, Buy Now, wishlist, comparison, reading/submitting individual reviews, and external social sharing belong to separate use cases. Their visible controls remain integration points, not simulated successful actions.
- Variant behavior, API contracts, quantity limits, and content for tabs not shown open in Figma are project decisions. The inspected frame establishes the visible desktop layout and controls.

### Actor(s)

Visitor or signed-in Customer.

### Priority

High

### Trigger

The actor opens the View Product Details interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=394-8951)

### Related API IDs

- [API-PRODUCT-DETAIL](../api/API-PRODUCT-DETAIL.md)
- [API-PRODUCT-MACBOOK-PRO-14-DETAIL](../api/API-PRODUCT-MACBOOK-PRO-14-DETAIL.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [clicon-uc-05-view-product-details.md](../../source/clicon-uc-05-view-product-details.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-PRODUCT-DETAIL-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_PRODUCT_DETAIL_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-PRODUCT-DETAIL-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_PRODUCT_DETAIL_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-PRODUCT-DETAIL-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_PRODUCT_DETAIL_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-PRODUCT-DETAIL-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_PRODUCT_DETAIL_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-PRODUCT-DETAIL-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_PRODUCT_DETAIL_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-PRODUCT-DETAIL-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_PRODUCT_DETAIL_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-PRODUCT-DETAIL-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_PRODUCT_DETAIL_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
