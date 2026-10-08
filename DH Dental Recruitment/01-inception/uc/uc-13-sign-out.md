---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-13
uc_name: "Sign Out"
---

# UC-13: Sign Out

## Functional Use-Case Specification

### Use Case ID

UC-13

### Use Case Name

Sign Out

### Description

- Allows an actor to end the browser session presented to the application and return to the public job catalog.
- The source account menu contains Sign out. Session scope, idempotent behavior, reconciliation, destination, and response contract are project decisions needed to make that action functional.
- This is a current-session action. It does not close an account, switch account roles, delete saved profile content, or sign out independent browser sessions. UC-12 separately defines ending all pre-change sessions after a password change.

### Actor(s)

Actor using the current browser session, including a Job Seeker whose session has expired or whose account has become ineligible.

### Priority

High

### Trigger

The actor opens the Sign Out interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4121)

### Related API IDs

- [API-AUTH-LOGOUT](../api/API-AUTH-LOGOUT.md)
- [API-LOGOUT-AUTH-SESSION-GET](../api/API-LOGOUT-AUTH-SESSION-GET.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [dh-dental-uc-13-sign-out.md](../../source/dh-dental-uc-13-sign-out.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
