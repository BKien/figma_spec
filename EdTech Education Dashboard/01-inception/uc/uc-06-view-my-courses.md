---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-06
uc_name: "View Assigned Courses and Module Progress"
---

# UC-06: View Assigned Courses and Module Progress

## Functional Use-Case Specification

### Use Case ID

UC-06

### Use Case Name

View Assigned Courses and Module Progress

### Description

- Lets a Student find their assigned courses, filter/sort the collection, expand module progress, and select a module for learning when its destination is implemented.
- Implements My Courses without conflating catalogue discovery with course access. Uses UC-04 CourseCard and UC-05 progress rules.
- Assignment fixtures, query contracts, and deferred learning navigation are project decisions. This UC is not enrollment, course purchasing, lesson playback, or certificate generation.

### Actor(s)

Authenticated Student with completed onboarding.

### Priority

High

### Trigger

The actor opens the View Assigned Courses and Module Progress interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-1174)

### Related API IDs

- [API-STUDENT-MY-COURSE-LIST](../api/API-STUDENT-MY-COURSE-LIST.md)
- [API-STUDENT-MY-COURSE-DETAIL](../api/API-STUDENT-MY-COURSE-DETAIL.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [edtech-uc-06-view-my-courses.md](../../source/edtech-uc-06-view-my-courses.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-MY-COURSES-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_MY_COURSES_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-MY-COURSES-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_MY_COURSES_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-MY-COURSES-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_MY_COURSES_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-MY-COURSES-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_MY_COURSES_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-MY-COURSES-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_MY_COURSES_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-MY-COURSES-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_MY_COURSES_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-MY-COURSES-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_MY_COURSES_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
