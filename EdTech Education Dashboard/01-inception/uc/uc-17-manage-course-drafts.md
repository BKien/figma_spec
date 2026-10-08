---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-17
uc_name: "Create and Edit a Course Draft"
---

# UC-17: Create and Edit a Course Draft

## Functional Use-Case Specification

### Use Case ID

UC-17

### Use Case Name

Create and Edit a Course Draft

### Description

- Allows an Instructor to create an owned draft and save course metadata, ordered modules, video lessons, and single-choice quizzes before publication.
- Defines the authoring counterpart of UC-04 and UC-07–09. Drafts are invisible to Student discovery and cannot receive enrollments.
- Instructor authoring is an approved project extension. The source Figma supplies Student presentation patterns, not an Instructor editor; the API and content constraints below are project decisions.

### Actor(s)

ACTIVE, email-verified Instructor authenticated through UC-16/UC-02.

### Priority

High

### Trigger

The actor opens the Create and Edit a Course Draft interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-1030)

### Related API IDs

- [API-INSTRUCTOR-COURSE-LIST](../api/API-INSTRUCTOR-COURSE-LIST.md)
- [API-INSTRUCTOR-COURSE-CREATE](../api/API-INSTRUCTOR-COURSE-CREATE.md)
- [API-INSTRUCTOR-COURSE-DETAIL](../api/API-INSTRUCTOR-COURSE-DETAIL.md)
- [API-INSTRUCTOR-COURSE-DRAFT-SAVE](../api/API-INSTRUCTOR-COURSE-DRAFT-SAVE.md)
- [API-INSTRUCTOR-COURSE-ASSET-LIST](../api/API-INSTRUCTOR-COURSE-ASSET-LIST.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [edtech-uc-17-manage-course-drafts.md](../../source/edtech-uc-17-manage-course-drafts.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-COURSE-DRAFT-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_COURSE_DRAFT_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-COURSE-DRAFT-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_COURSE_DRAFT_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-COURSE-DRAFT-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_COURSE_DRAFT_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-COURSE-DRAFT-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_COURSE_DRAFT_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-COURSE-DRAFT-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_COURSE_DRAFT_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-COURSE-DRAFT-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_COURSE_DRAFT_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-COURSE-DRAFT-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_COURSE_DRAFT_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
