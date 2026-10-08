---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-16
uc_name: "View Order Details"
---

# UC-16: View Order Details

## Functional Use-Case Specification

### Use Case ID

UC-16

### Use Case Name

View Order Details

### Description

- Displays the saved items, final amounts, addresses, contact, notes, and fulfillment activity of one placed order.
- Completes UC-15's View Details and UC-07's View Order integration points. Account detail and original-browser confirmation access have explicit separate boundaries below.
- Access rules, snapshots, API contracts, and missing-data behavior are project decisions; Figma establishes the desktop detail layout. Modification, cancellation, payment collection, and review submission are outside this UC; reviews belong to UC-17.

### Actor(s)

Signed-in order owner, or the visitor in the original checkout browser context.

### Priority

High

### Trigger

The actor opens the View Order Details interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=478-12692)

### Related API IDs

- [API-ACCOUNT-ORDER-DETAIL](../api/API-ACCOUNT-ORDER-DETAIL.md)
- [API-CHECKOUT-ORDER-DETAIL](../api/API-CHECKOUT-ORDER-DETAIL.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [clicon-uc-16-view-order-details.md](../../source/clicon-uc-16-view-order-details.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-ORDER-DETAIL-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_ORDER_DETAIL_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-ORDER-DETAIL-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_ORDER_DETAIL_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-ORDER-DETAIL-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_ORDER_DETAIL_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-ORDER-DETAIL-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_ORDER_DETAIL_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-ORDER-DETAIL-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_ORDER_DETAIL_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-ORDER-DETAIL-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_ORDER_DETAIL_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-ORDER-DETAIL-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_ORDER_DETAIL_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
