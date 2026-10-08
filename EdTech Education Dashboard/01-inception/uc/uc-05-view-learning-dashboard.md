---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-05
uc_name: "View the Learning Dashboard"
---

# UC-05: View the Learning Dashboard

## Functional Use-Case Specification

### Use Case ID

UC-05

### Use Case Name

View the Learning Dashboard

### Description

- Gives the Student one account-scoped summary of enrolled-course progress, active/completed courses, upcoming learning units, and course suggestions.
- Replaces UC-02's dashboard integration shell at /student/dashboard, including the post-onboarding destination in UC-03.
- The dashboard is a read-only overview. Metric definitions, omitted source features, and response contracts are project decisions, not Figma-derived business rules.

### Actor(s)

Authenticated Student with completed onboarding.

### Priority

High

### Trigger

The actor opens the View the Learning Dashboard interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-1374)

### Related API IDs

- [API-STUDENT-DASHBOARD-GET](../api/API-STUDENT-DASHBOARD-GET.md)
- [API-STUDENT-DASHBOARD-COURSE-DISCOVERY-GET](../api/API-STUDENT-DASHBOARD-COURSE-DISCOVERY-GET.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [edtech-uc-05-view-learning-dashboard.md](../../source/edtech-uc-05-view-learning-dashboard.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-LEARNING-DASHBOARD-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_LEARNING_DASHBOARD_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-LEARNING-DASHBOARD-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_LEARNING_DASHBOARD_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-LEARNING-DASHBOARD-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_LEARNING_DASHBOARD_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-LEARNING-DASHBOARD-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_LEARNING_DASHBOARD_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-LEARNING-DASHBOARD-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_LEARNING_DASHBOARD_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-LEARNING-DASHBOARD-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_LEARNING_DASHBOARD_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-LEARNING-DASHBOARD-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_LEARNING_DASHBOARD_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
