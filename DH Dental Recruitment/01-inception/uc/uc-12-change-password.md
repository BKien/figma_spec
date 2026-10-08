---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-12
uc_name: "Change Password"
---

# UC-12: Change Password

## Functional Use-Case Specification

### Use Case ID

UC-12

### Use Case Name

Change Password

### Description

- Allows a signed-in Job Seeker who knows their current password to replace it with a new password and then sign in again.
- The Figma form supplies a read-only email, current password, new password, repeated new password, and Save Changes. It is distinct from forgotten-password recovery, which remains unavailable under UC-02.
- Password interpretation follows UC-01/02. Current-password confirmation, observable attempt limits, session-ending behavior, errors, and API contract are explicit project decisions; implementation algorithms are not prescribed by this UC.

### Actor(s)

Authenticated ACTIVE JOB_SEEKER who knows their current password.

### Priority

High

### Trigger

The actor opens the Change Password interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4345)

### Related API IDs

- [API-AUTH-PASSWORD-UPDATE](../api/API-AUTH-PASSWORD-UPDATE.md)
- [API-PASSWORD-CHANGE-AUTH-SESSION-GET](../api/API-PASSWORD-CHANGE-AUTH-SESSION-GET.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [dh-dental-uc-12-change-password.md](../../source/dh-dental-uc-12-change-password.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-CHANGE-PASSWORD-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_CHANGE_PASSWORD_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-CHANGE-PASSWORD-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_CHANGE_PASSWORD_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-CHANGE-PASSWORD-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_CHANGE_PASSWORD_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-CHANGE-PASSWORD-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_CHANGE_PASSWORD_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-CHANGE-PASSWORD-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_CHANGE_PASSWORD_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-CHANGE-PASSWORD-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_CHANGE_PASSWORD_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-CHANGE-PASSWORD-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_CHANGE_PASSWORD_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
