---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-17
uc_name: "Manage Public Profile Visibility"
---

# UC-17: Manage Public Profile Visibility

## Functional Use-Case Specification

### Use Case ID

UC-17

### Use Case Name

Manage Public Profile Visibility

### Description

- Allows a Job Seeker to preview a limited public representation of their existing profile, explicitly publish it, replace that published snapshot after later edits, or make it private again.
- This enables the directory/detail goals in UC-18/19. Registration and private-profile editing remain private by default and do not automatically publish anything.
- The source menu's Make Profile Private action and public profile screens establish a visibility concept. The reverse publish action, preview screen, snapshot scope, confirmation, and contracts are explicit research additions; no owner publication editor or complete workflow has been verified in the source.

### Actor(s)

Authenticated ACTIVE JOB_SEEKER.

### Priority

Medium

### Trigger

The actor opens the Manage Public Profile Visibility interface.

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
- [Supporting Figma node 2](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-1478)
- [Supporting Figma node 3](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-1700)

### Related API IDs

- [API-PROFILE-PUBLICATION-GET](../api/API-PROFILE-PUBLICATION-GET.md)
- [API-PROFILE-PUBLICATION-UPDATE](../api/API-PROFILE-PUBLICATION-UPDATE.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [dh-dental-uc-17-manage-public-profile.md](../../source/dh-dental-uc-17-manage-public-profile.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-PUBLIC-PROFILE-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_PUBLIC_PROFILE_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-PUBLIC-PROFILE-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_PUBLIC_PROFILE_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-PUBLIC-PROFILE-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_PUBLIC_PROFILE_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-PUBLIC-PROFILE-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_PUBLIC_PROFILE_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-PUBLIC-PROFILE-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_PUBLIC_PROFILE_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-PUBLIC-PROFILE-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_PUBLIC_PROFILE_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-PUBLIC-PROFILE-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_PUBLIC_PROFILE_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
