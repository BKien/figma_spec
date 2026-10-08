---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-19
uc_name: "Submit a Support Request"
---

# UC-19: Submit a Support Request

## Functional Use-Case Specification

### Use Case ID

UC-19

### Use Case Name

Submit a Support Request

### Description

- Lets a visitor submit an email address, subject, and optional message through the FAQ support form and receive a durable request reference.
- Successful submission means stored for the research experiment, not delivered email, assigned support staff, live chat, or guaranteed response time. No agent-response/admin interface is added.
- Contracts, retry behavior, limits, and persistence below are project decisions; the form controls are supported by Figma.

### Actor(s)

Visitor or signed-in Customer.

### Priority

Medium

### Trigger

The actor opens the Submit a Support Request interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=436-8148)
- [Supporting Figma node 2](https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=447-9904)

### Related API IDs

- [API-SUPPORT-REQUEST-CREATE](../api/API-SUPPORT-REQUEST-CREATE.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [clicon-uc-19-submit-support-request.md](../../source/clicon-uc-19-submit-support-request.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-SUPPORT-REQUEST-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SUPPORT_REQUEST_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-SUPPORT-REQUEST-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SUPPORT_REQUEST_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-SUPPORT-REQUEST-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SUPPORT_REQUEST_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-SUPPORT-REQUEST-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SUPPORT_REQUEST_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-SUPPORT-REQUEST-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SUPPORT_REQUEST_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-SUPPORT-REQUEST-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SUPPORT_REQUEST_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-SUPPORT-REQUEST-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SUPPORT_REQUEST_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
