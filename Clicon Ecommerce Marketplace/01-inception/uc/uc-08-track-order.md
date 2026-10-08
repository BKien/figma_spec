---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-08
uc_name: "Track Order"
---

# UC-08: Track Order

## Functional Use-Case Specification

### Use Case ID

UC-08

### Use Case Name

Track Order

### Description

- Allows a visitor or customer to look up a previously placed order using its displayed order number and checkout billing email, then view fulfillment progress and recorded activity.
- Continues UC-07 using the persisted order and its original browser context. Includes the tracking form and read-only tracking result.
- Lookup eligibility, fulfillment states, API contracts, and recovery behavior below are project decisions. Figma establishes the inspected desktop form, summary, progress indicator, and activity list.
- This UC does not change an order, collect payment, contact a carrier, generate shipment events, send email, or implement order history, cancellation, returns, or full order details.

### Actor(s)

Visitor or signed-in Customer in the browser context that placed the order.

### Priority

High

### Trigger

The actor opens the Track Order interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=418-10475)
- [Supporting Figma node 2](https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=418-11361)

### Related API IDs

- [API-ORDER-TRACK](../api/API-ORDER-TRACK.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [clicon-uc-08-track-order.md](../../source/clicon-uc-08-track-order.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-TRACK-ORDER-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_TRACK_ORDER_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-TRACK-ORDER-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_TRACK_ORDER_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-TRACK-ORDER-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_TRACK_ORDER_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-TRACK-ORDER-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_TRACK_ORDER_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-TRACK-ORDER-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_TRACK_ORDER_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-TRACK-ORDER-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_TRACK_ORDER_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-TRACK-ORDER-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_TRACK_ORDER_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
