---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-14
uc_name: "Permanently Close Account"
---

# UC-14: Permanently Close Account

## Functional Use-Case Specification

### Use Case ID

UC-14

### Use Case Name

Permanently Close Account

### Description

- Allows an authenticated Job Seeker to permanently close their own account after reviewing the consequences and confirming the action.
- The Figma source states that closed accounts cannot be reactivated and presents Close Account Now. This UC implements closure and removal of the account's current research data, not merely the current-session sign-out in UC-13.
- Confirmation, lifecycle changes, deletion scope/timing, concurrency rules, and API contract are explicit research decisions. This specification does not claim legal compliance or immediate erasure from infrastructure outside the defined research data stores.

### Actor(s)

Authenticated ACTIVE JOB_SEEKER choosing to close their own account.

### Priority

High

### Trigger

The actor opens the Permanently Close Account interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4425)

### Related API IDs

- [API-AUTH-ACCOUNT-CLOSE](../api/API-AUTH-ACCOUNT-CLOSE.md)
- [API-ACCOUNT-CLOSURE-AUTH-SESSION-GET](../api/API-ACCOUNT-CLOSURE-AUTH-SESSION-GET.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [dh-dental-uc-14-close-account.md](../../source/dh-dental-uc-14-close-account.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-CLOSE-ACCOUNT-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_CLOSE_ACCOUNT_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-CLOSE-ACCOUNT-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_CLOSE_ACCOUNT_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-CLOSE-ACCOUNT-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_CLOSE_ACCOUNT_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-CLOSE-ACCOUNT-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_CLOSE_ACCOUNT_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-CLOSE-ACCOUNT-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_CLOSE_ACCOUNT_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-CLOSE-ACCOUNT-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_CLOSE_ACCOUNT_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-CLOSE-ACCOUNT-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_CLOSE_ACCOUNT_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
