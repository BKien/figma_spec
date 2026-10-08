---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-04
uc_name: "Discover Courses"
---

# UC-04: Discover Courses

## Functional Use-Case Specification

### Use Case ID

UC-04

### Use Case Name

Discover Courses

### Description

- Lets an onboarded Student browse the learning catalogue, search by keyword, filter by category, and inspect a course summary before navigating to an assigned course.
- Implements the Home Student discovery screen. Course access is separate from discovery; viewing a card does not enroll the learner or make lesson content accessible.
- Contracts, catalogue/search behavior, preview panel, and deterministic ranking are project decisions. The Figma screens support the visual composition, not an existing backend contract or supplied Technical Report.

### Actor(s)

Authenticated Student with completed onboarding.

### Priority

High

### Trigger

The actor opens the Discover Courses interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-1888)
- [Supporting Figma node 2](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=231-822)

### Related API IDs

- [API-STUDENT-COURSE-DISCOVERY-GET](../api/API-STUDENT-COURSE-DISCOVERY-GET.md)
- [API-STUDENT-CATALOG-COURSE-LIST](../api/API-STUDENT-CATALOG-COURSE-LIST.md)
- [API-STUDENT-CATALOG-COURSE-DETAIL](../api/API-STUDENT-CATALOG-COURSE-DETAIL.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [edtech-uc-04-discover-courses.md](../../source/edtech-uc-04-discover-courses.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-COURSE-DISCOVERY-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_COURSE_DISCOVERY_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-COURSE-DISCOVERY-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_COURSE_DISCOVERY_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-COURSE-DISCOVERY-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_COURSE_DISCOVERY_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-COURSE-DISCOVERY-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_COURSE_DISCOVERY_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-COURSE-DISCOVERY-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_COURSE_DISCOVERY_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-COURSE-DISCOVERY-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_COURSE_DISCOVERY_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-COURSE-DISCOVERY-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_COURSE_DISCOVERY_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
