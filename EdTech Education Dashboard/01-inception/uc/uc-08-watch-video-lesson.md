---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-08
uc_name: "Watch a Video Lesson and Save Progress"
---

# UC-08: Watch a Video Lesson and Save Progress

## Functional Use-Case Specification

### Use Case ID

UC-08

### Use Case Name

Watch a Video Lesson and Save Progress

### Description

- Lets an enrolled Student play a course video, resume its saved position, and record completed playback coverage for unit-level progress.
- Completes UC-07 VIDEO navigation and supplies actual video-unit completion to UC-05/06. The experiment records player-reported playback coverage; it does not claim verified attendance, attention, or proctoring.
- The 90% completion threshold, progress contract, and concurrency rules are project decisions. The Figma frame supports the player layout and controls.

### Actor(s)

Authenticated, onboarded Student enrolled in the video course.

### Priority

High

### Trigger

The actor opens the Watch a Video Lesson and Save Progress interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-912)

### Related API IDs

- [API-STUDENT-VIDEO-LESSON-GET](../api/API-STUDENT-VIDEO-LESSON-GET.md)
- [API-STUDENT-VIDEO-PROGRESS-UPDATE](../api/API-STUDENT-VIDEO-PROGRESS-UPDATE.md)
- [API-STUDENT-VIDEO-MEDIA-GET](../api/API-STUDENT-VIDEO-MEDIA-GET.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [edtech-uc-08-watch-video-lesson.md](../../source/edtech-uc-08-watch-video-lesson.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-VIDEO-LESSON-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_VIDEO_LESSON_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-VIDEO-LESSON-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_VIDEO_LESSON_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-VIDEO-LESSON-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_VIDEO_LESSON_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-VIDEO-LESSON-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_VIDEO_LESSON_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-VIDEO-LESSON-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_VIDEO_LESSON_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-VIDEO-LESSON-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_VIDEO_LESSON_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-VIDEO-LESSON-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_VIDEO_LESSON_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
