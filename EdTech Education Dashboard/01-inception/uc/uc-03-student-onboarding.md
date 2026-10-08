---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-03
uc_name: "Set Up a Student Learning Profile"
---

# UC-03: Set Up a Student Learning Profile

## Functional Use-Case Specification

### Use Case ID

UC-03

### Use Case Name

Set Up a Student Learning Profile

### Description

- Collects the Student's learning goals, interests, current occupation, and education level through the four initial setup screens.
- Replaces UC-02's /student/onboarding integration shell. The four steps belong to one onboarding goal, with saved progress and an explicit completion outcome.
- The field choices and selection maxima are supported by Figma. Minimum selections, persistence, API contracts, concurrency behavior, and completion rules below are proposed project requirements, not quotations from a supplied Technical Report.
- The question Your Current Role describes occupation. It must not change account.role, grant Instructor privileges, or act as an application-role selector.

### Actor(s)

Authenticated Student with an incomplete learning profile.

### Priority

High

### Trigger

The actor opens the Set Up a Student Learning Profile interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-2355)
- [Supporting Figma node 2](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-2263)
- [Supporting Figma node 3](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-2198)
- [Supporting Figma node 4](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-2147)

### Related API IDs

- [API-STUDENT-ONBOARDING-GET](../api/API-STUDENT-ONBOARDING-GET.md)
- [API-STUDENT-ONBOARDING-STEP-UPDATE](../api/API-STUDENT-ONBOARDING-STEP-UPDATE.md)
- [API-STUDENT-ONBOARDING-COMPLETE](../api/API-STUDENT-ONBOARDING-COMPLETE.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [edtech-uc-03-student-onboarding.md](../../source/edtech-uc-03-student-onboarding.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-STUDENT-ONBOARDING-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_STUDENT_ONBOARDING_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-STUDENT-ONBOARDING-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_STUDENT_ONBOARDING_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-STUDENT-ONBOARDING-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_STUDENT_ONBOARDING_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-STUDENT-ONBOARDING-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_STUDENT_ONBOARDING_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-STUDENT-ONBOARDING-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_STUDENT_ONBOARDING_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-STUDENT-ONBOARDING-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_STUDENT_ONBOARDING_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-STUDENT-ONBOARDING-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_STUDENT_ONBOARDING_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
