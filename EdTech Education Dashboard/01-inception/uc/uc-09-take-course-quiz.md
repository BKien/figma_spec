---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-09
uc_name: "Take a Course Quiz and View the Result"
---

# UC-09: Take a Course Quiz and View the Result

## Functional Use-Case Specification

### Use Case ID

UC-09

### Use Case Name

Take a Course Quiz and View the Result

### Description

- Lets an enrolled Student start/resume a timed quiz, save answers, submit for grading, and view their result and highest score.
- Treats overview, attempt, draft, submission, and result as one quiz-taking business goal. Completes UC-07 QUIZ navigation and contributes quiz completion to the common course progress.
- Attempt limit, grading, passing threshold, timer authority, repeat behavior, and API contracts are project decisions. Figma supplies the three quiz screens, not an existing Technical Report or backend contract.

### Actor(s)

Authenticated, onboarded Student enrolled in the quiz course.

### Priority

High

### Trigger

The actor opens the Take a Course Quiz and View the Result interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-801)
- [Supporting Figma node 2](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-650)
- [Supporting Figma node 3](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-535)

### Related API IDs

- [API-STUDENT-QUIZ-GET](../api/API-STUDENT-QUIZ-GET.md)
- [API-STUDENT-QUIZ-ATTEMPT-CREATE](../api/API-STUDENT-QUIZ-ATTEMPT-CREATE.md)
- [API-STUDENT-QUIZ-ATTEMPT-DETAIL](../api/API-STUDENT-QUIZ-ATTEMPT-DETAIL.md)
- [API-STUDENT-QUIZ-ATTEMPT-DRAFT-SAVE](../api/API-STUDENT-QUIZ-ATTEMPT-DRAFT-SAVE.md)
- [API-STUDENT-QUIZ-ATTEMPT-SUBMIT](../api/API-STUDENT-QUIZ-ATTEMPT-SUBMIT.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [edtech-uc-09-take-course-quiz.md](../../source/edtech-uc-09-take-course-quiz.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-COURSE-QUIZ-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_COURSE_QUIZ_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-COURSE-QUIZ-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_COURSE_QUIZ_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-COURSE-QUIZ-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_COURSE_QUIZ_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-COURSE-QUIZ-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_COURSE_QUIZ_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-COURSE-QUIZ-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_COURSE_QUIZ_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-COURSE-QUIZ-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_COURSE_QUIZ_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-COURSE-QUIZ-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_COURSE_QUIZ_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
