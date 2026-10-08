---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-15
uc_name: "View Account Order History"
---

# UC-15: View Account Order History

## Functional Use-Case Specification

### Use Case ID

UC-15

### Use Case Name

View Account Order History

### Description

- Allows an authenticated customer to view a paginated summary of orders explicitly associated with their account, including order number, fulfillment summary, placement date, final total, and purchased quantity.
- Includes the account-order association needed to populate this page from future UC-07 checkouts. That association is an explicit integration extension; it was not previously implemented or implied by UC-07's browser-owned confirmation contract.
- Ownership, status mapping, pagination, and API contracts are project decisions. Figma establishes the inspected desktop table, sidebar, and pagination controls.
- Full order details, cancellation, refunds, payment collection, order search, and order-history import are outside this UC. View Details remains an integration point for its owning UC.

### Actor(s)

Signed-in Customer with an active, verified account.

### Priority

High

### Trigger

The actor opens the View Account Order History interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=478-10910)

### Related API IDs

- [API-ACCOUNT-ORDER-LIST](../api/API-ACCOUNT-ORDER-LIST.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [clicon-uc-15-view-order-history.md](../../source/clicon-uc-15-view-order-history.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-ORDER-HISTORY-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_ORDER_HISTORY_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-ORDER-HISTORY-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_ORDER_HISTORY_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-ORDER-HISTORY-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_ORDER_HISTORY_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-ORDER-HISTORY-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_ORDER_HISTORY_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-ORDER-HISTORY-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_ORDER_HISTORY_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-ORDER-HISTORY-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_ORDER_HISTORY_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-ORDER-HISTORY-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_ORDER_HISTORY_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
