---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-02
uc_name: "Sign In to a Student Account"
---

# UC-02: Sign In to a Student Account

## Functional Use-Case Specification

### Use Case ID

UC-02

### Use Case Name

Sign In to a Student Account

### Description

- Allows a registered Student to sign in with email and password, optionally remain signed in across browser restarts, and reach the appropriate authenticated destination.
- Continues UC-01 using its normalized email, password, account eligibility, and onboarding state. Registration verification alone does not authenticate a browser.
- Session duration, API contracts, limits, and routing are EdTech project decisions. The Figma Login frame supplies the visible controls. No existing backend contract or Technical Report is being quoted.
- Instructor support remains an approved separate extension. This UC authenticates Student accounts; it neither creates Instructor accounts nor interprets a client-selected role as authority.

### Actor(s)

Student with an existing account.

### Priority

High

### Trigger

The actor opens the Sign In to a Student Account interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-2528)

### Related API IDs

- [API-AUTH-LOGIN](../api/API-AUTH-LOGIN.md)
- [API-AUTH-SESSION-GET](../api/API-AUTH-SESSION-GET.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [edtech-uc-02-sign-in.md](../../source/edtech-uc-02-sign-in.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-SIGN-IN-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SIGN_IN_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-SIGN-IN-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SIGN_IN_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-SIGN-IN-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SIGN_IN_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-SIGN-IN-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SIGN_IN_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-SIGN-IN-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SIGN_IN_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-SIGN-IN-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SIGN_IN_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-SIGN-IN-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SIGN_IN_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
