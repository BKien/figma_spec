---
artifact_type: business-use-case-specification
status: "Draft"
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

Not specified in the supplied source.

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

AF-1:

1. The actor chooses an available alternative action.
2. The client displays the returned alternative outcome.

### Exception Flow

EF-1:

1. The system returns an unsuccessful outcome.
2. The client displays the returned recovery message.

### Related UI

- [Supporting Figma node 1](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-1174)

### Related API IDs

- [API-UC-18-01](../api/api-uc-18-01.md)
- [API-UC-18-02](../api/api-uc-18-02.md)
- [API-UC-18-03](../api/api-uc-18-03.md)

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

~~~ocl
-- BR-UC-18-01
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_UC_18_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~ocl
-- BR-UC-18-02
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_UC_18_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~ocl
-- BR-UC-18-03
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_UC_18_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~ocl
-- BR-UC-18-04
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_UC_18_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~ocl
-- BR-UC-18-05
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_UC_18_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~ocl
-- BR-UC-18-06
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_UC_18_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~ocl
-- BR-UC-18-07
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_UC_18_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
