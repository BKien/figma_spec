---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-05
uc_name: "Manage Basic Profile Information"
---

# UC-05: Manage Basic Profile Information

## Functional Use-Case Specification

### Use Case ID

UC-05

### Use Case Name

Manage Basic Profile Information

### Description

- Allows a signed-in Job Seeker to view and update their name, fluent languages, desired position, available start month, and optional profile photo as one profile-editing task.
- Names stay consistent with the account created in UC-01. The desired position becomes the category used by UC-07 recommendations; this UC does not publish a candidate profile or verify professional qualifications.
- The Figma read/edit frames establish the visible fields. Field rules, photo handling, routes, version conflicts, and API contracts below are research implementation decisions. They are not quotations from a supplied Technical Report.

### Actor(s)

Authenticated ACTIVE JOB_SEEKER.

### Priority

High

### Trigger

The actor opens the Manage Basic Profile Information interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4549)
- [Supporting Figma node 2](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4631)

### Related API IDs

- [API-PROFILE-BASIC-GET](../api/API-PROFILE-BASIC-GET.md)
- [API-PROFILE-BASIC-UPDATE](../api/API-PROFILE-BASIC-UPDATE.md)
- [API-PROFILE-PHOTO-GET](../api/API-PROFILE-PHOTO-GET.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [dh-dental-uc-05-manage-basic-profile.md](../../source/dh-dental-uc-05-manage-basic-profile.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-BASIC-PROFILE-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_BASIC_PROFILE_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-BASIC-PROFILE-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_BASIC_PROFILE_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-BASIC-PROFILE-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_BASIC_PROFILE_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-BASIC-PROFILE-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_BASIC_PROFILE_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-BASIC-PROFILE-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_BASIC_PROFILE_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-BASIC-PROFILE-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_BASIC_PROFILE_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-BASIC-PROFILE-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_BASIC_PROFILE_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
