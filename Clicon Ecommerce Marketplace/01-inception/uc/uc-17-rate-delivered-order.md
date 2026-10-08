---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-17
uc_name: "Rate a Delivered Order"
---

# UC-17: Rate a Delivered Order

## Functional Use-Case Specification

### Use Case ID

UC-17

### Use Case Name

Rate a Delivered Order

### Description

- Lets the authenticated owner leave one rating and feedback about a delivered order from UC-16's Leave a Rating modal.
- This is an order/service review: the inspected modal has no product selector. It does not alter product ratingAverage/reviewCount in UC-04/UC-05/UC-10, and it does not enable UC-05's product-review tab.
- Eligibility, single-review behavior, contracts, and visibility are project decisions. Editing/deleting reviews and public product reviews are outside this UC.

### Actor(s)

Signed-in Customer whose account owns the delivered order under UC-15.

### Priority

Medium

### Trigger

The actor opens the Rate a Delivered Order interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=510-15928)

### Related API IDs

- [API-ORDER-REVIEW-GET](../api/API-ORDER-REVIEW-GET.md)
- [API-ORDER-REVIEW-CREATE](../api/API-ORDER-REVIEW-CREATE.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [clicon-uc-17-rate-delivered-order.md](../../source/clicon-uc-17-rate-delivered-order.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-RATE-ORDER-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_RATE_ORDER_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-RATE-ORDER-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_RATE_ORDER_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-RATE-ORDER-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_RATE_ORDER_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-RATE-ORDER-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_RATE_ORDER_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-RATE-ORDER-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_RATE_ORDER_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-RATE-ORDER-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_RATE_ORDER_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-RATE-ORDER-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_RATE_ORDER_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
