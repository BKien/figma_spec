---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-14
uc_name: "Recover a Forgotten Password"
---

# UC-14: Recover a Forgotten Password

## Functional Use-Case Specification

### Use Case ID

UC-14

### Use Case Name

Recover a Forgotten Password

### Description

- Allows an eligible Student to request a password-recovery email, open a time-limited link, and set a new password without knowing the old one.
- Enables UC-02's Forgot Password entry. Email-request/reset forms and link-based recovery are project-designed additions; only the entry link is supplied by Figma.
- Uses local Mailpit for the experiment, as UC-01 does. This is account recovery, not registration verification or automatic sign-in.

### Actor(s)

Visitor who controls the email address of an ACTIVE, verified STUDENT account.

### Priority

High

### Trigger

The actor opens the Recover a Forgotten Password interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-2528)

### Related API IDs

- [API-AUTH-PASSWORD-RECOVERY-REQUEST](../api/API-AUTH-PASSWORD-RECOVERY-REQUEST.md)
- [API-AUTH-PASSWORD-RECOVERY-COMPLETE](../api/API-AUTH-PASSWORD-RECOVERY-COMPLETE.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [edtech-uc-14-recover-password.md](../../source/edtech-uc-14-recover-password.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-RECOVER-PASSWORD-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_RECOVER_PASSWORD_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-RECOVER-PASSWORD-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_RECOVER_PASSWORD_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-RECOVER-PASSWORD-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_RECOVER_PASSWORD_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-RECOVER-PASSWORD-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_RECOVER_PASSWORD_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-RECOVER-PASSWORD-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_RECOVER_PASSWORD_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-RECOVER-PASSWORD-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_RECOVER_PASSWORD_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-RECOVER-PASSWORD-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_RECOVER_PASSWORD_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
