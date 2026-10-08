---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-19
uc_name: "Inspect an Enrolled Learner’s Progress"
---

# UC-19: Inspect an Enrolled Learner’s Progress

## Functional Use-Case Specification

### Use Case ID

UC-19

### Use Case Name

Inspect an Enrolled Learner’s Progress

### Description

- Lets the owning Instructor inspect one learner's course/module/unit completion, video coverage, and quiz-attempt results.
- Extends UC-18's summary roster into a detailed diagnostic view. It does not introduce another roster, alter grades, or simulate learning activity.
- The Instructor screen and API are project-designed supplements. Existing Student progress and quiz frames provide visual reference; no Technical Report or dedicated Instructor Figma frame supplies this behavior.

### Actor(s)

Authenticated ACTIVE, email-verified INSTRUCTOR who owns the published course.

### Priority

High

### Trigger

The actor opens the Inspect an Enrolled Learner’s Progress interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-1374)

### Related API IDs

- [API-INSTRUCTOR-LEARNER-PROGRESS-GET](../api/API-INSTRUCTOR-LEARNER-PROGRESS-GET.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [edtech-uc-19-inspect-learner-progress.md](../../source/edtech-uc-19-inspect-learner-progress.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-LEARNER-PROGRESS-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_LEARNER_PROGRESS_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-LEARNER-PROGRESS-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_LEARNER_PROGRESS_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-LEARNER-PROGRESS-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_LEARNER_PROGRESS_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-LEARNER-PROGRESS-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_LEARNER_PROGRESS_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-LEARNER-PROGRESS-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_LEARNER_PROGRESS_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-LEARNER-PROGRESS-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_LEARNER_PROGRESS_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-LEARNER-PROGRESS-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_LEARNER_PROGRESS_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
