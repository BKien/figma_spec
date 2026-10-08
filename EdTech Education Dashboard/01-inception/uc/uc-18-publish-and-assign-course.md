---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-18
uc_name: "Publish a Course and Assign Learners"
---

# UC-18: Publish a Course and Assign Learners

## Functional Use-Case Specification

### Use Case ID

UC-18

### Use Case Name

Publish a Course and Assign Learners

### Description

- Allows an Instructor to release an owned, complete course to the Student catalog and assign registered Students to its learning content.
- Publication and assignment are separate durable stages of this delivery workflow. A published course can have zero learners; an assignment failure never rolls back publication.
- Replaces the fixture-only enrollment limitation in UC-04–06 with defined Instructor assignment. It preserves existing Student course cards, access rules, and progress calculations. Instructor UI and business rules are project extensions, not existing Figma functionality.

### Actor(s)

Authenticated ACTIVE, verified Instructor who owns the course.

### Priority

High

### Trigger

The actor opens the Publish a Course and Assign Learners interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-1174)

### Related API IDs

- [API-INSTRUCTOR-COURSE-PUBLISH](../api/API-INSTRUCTOR-COURSE-PUBLISH.md)
- [API-INSTRUCTOR-ENROLLMENT-CREATE](../api/API-INSTRUCTOR-ENROLLMENT-CREATE.md)
- [API-INSTRUCTOR-ENROLLMENT-LIST](../api/API-INSTRUCTOR-ENROLLMENT-LIST.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [edtech-uc-18-publish-and-assign-course.md](../../source/edtech-uc-18-publish-and-assign-course.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-PUBLISH-ASSIGN-COURSE-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_PUBLISH_ASSIGN_COURSE_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-PUBLISH-ASSIGN-COURSE-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_PUBLISH_ASSIGN_COURSE_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-PUBLISH-ASSIGN-COURSE-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_PUBLISH_ASSIGN_COURSE_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-PUBLISH-ASSIGN-COURSE-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_PUBLISH_ASSIGN_COURSE_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-PUBLISH-ASSIGN-COURSE-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_PUBLISH_ASSIGN_COURSE_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-PUBLISH-ASSIGN-COURSE-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_PUBLISH_ASSIGN_COURSE_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-PUBLISH-ASSIGN-COURSE-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_PUBLISH_ASSIGN_COURSE_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
