---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-15
uc_name: "Sign Out of the Current Browser Session"
---

# UC-15: Sign Out of the Current Browser Session

## Functional Use-Case Specification

### Use Case ID

UC-15

### Use Case Name

Sign Out of the Current Browser Session

### Description

- Lets a signed-in Student end the current browser session and return to Login.
- Completes the Logout controls in the account menu and Profile screen. Unlike UC-13/14, this operation does not end every device's session.
- Session termination, unsaved-work behavior, and API contract are project decisions; Figma supports the visible action, not its backend implementation.

### Actor(s)

Signed-in Student, including an account with incomplete onboarding. An already-ended session also receives successful logout.

### Priority

High

### Trigger

The actor opens the Sign Out of the Current Browser Session interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=231-822)
- [Supporting Figma node 2](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-436)

### Related API IDs

- [API-AUTH-LOGOUT](../api/API-AUTH-LOGOUT.md)
- [API-LOGOUT-AUTH-SESSION-GET](../api/API-LOGOUT-AUTH-SESSION-GET.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [edtech-uc-15-sign-out.md](../../source/edtech-uc-15-sign-out.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-SIGN-OUT-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SIGN_OUT_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-SIGN-OUT-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SIGN_OUT_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-SIGN-OUT-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SIGN_OUT_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-SIGN-OUT-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SIGN_OUT_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-SIGN-OUT-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SIGN_OUT_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-SIGN-OUT-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SIGN_OUT_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-SIGN-OUT-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SIGN_OUT_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
