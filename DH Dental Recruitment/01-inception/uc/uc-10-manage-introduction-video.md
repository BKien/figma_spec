---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-10
uc_name: "Record and Manage an Introduction Video"
---

# UC-10: Record and Manage an Introduction Video

## Functional Use-Case Specification

### Use Case ID

UC-10

### Use Case Name

Record and Manage an Introduction Video

### Description

- Allows a Job Seeker to record a short introduction in the browser, review it, and explicitly save it to their account. A compatible local video can be selected as an alternative; a saved video can be played, replaced, or removed.
- The source supports a camera/recording area, Record Your Answers, a policy link, and a sample-video/mobile-app panel. Review, save, replacement, deletion, and upload-fallback states are project supplements needed to define an end-to-end feature.
- This UC stores one account-level introduction, not a job-specific application answer. It sends nothing to a recruiter and does not submit an application. Duration/format limits, routes, state transitions, and backend contracts are declared research decisions.

### Actor(s)

Authenticated ACTIVE JOB_SEEKER.

### Priority

Low

### Trigger

The actor opens the Record and Manage an Introduction Video interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4160)

### Related API IDs

- [API-INTRODUCTION-VIDEO-GET](../api/API-INTRODUCTION-VIDEO-GET.md)
- [API-INTRODUCTION-VIDEO-SAVE](../api/API-INTRODUCTION-VIDEO-SAVE.md)
- [API-INTRODUCTION-VIDEO-DELETE](../api/API-INTRODUCTION-VIDEO-DELETE.md)
- [API-INTRODUCTION-VIDEO-MEDIA-GET](../api/API-INTRODUCTION-VIDEO-MEDIA-GET.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [dh-dental-uc-10-manage-introduction-video.md](../../source/dh-dental-uc-10-manage-introduction-video.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-INTRODUCTION-VIDEO-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_INTRODUCTION_VIDEO_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-INTRODUCTION-VIDEO-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_INTRODUCTION_VIDEO_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-INTRODUCTION-VIDEO-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_INTRODUCTION_VIDEO_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-INTRODUCTION-VIDEO-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_INTRODUCTION_VIDEO_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-INTRODUCTION-VIDEO-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_INTRODUCTION_VIDEO_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-INTRODUCTION-VIDEO-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_INTRODUCTION_VIDEO_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-INTRODUCTION-VIDEO-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_INTRODUCTION_VIDEO_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
