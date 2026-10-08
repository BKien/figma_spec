---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-10
uc_name: "View and Update Student Contact Profile"
---

# UC-10: View and Update Student Contact Profile

## Functional Use-Case Specification

### Use Case ID

UC-10

### Use Case Name

View and Update Student Contact Profile

### Description

- Lets the Student view account identity and completed-course links, and update phone number, preferred contact method, and biography.
- Enables the Profile menu destination. Contact profile data is separate from UC-03's learning goals, interests, occupation, and education answers.
- Editable field boundaries, validation, persistence, and unavailable controls are explicit project decisions. The Profile frame supplies the form composition; no Technical Report has been supplied.

### Actor(s)

Authenticated Student with completed onboarding.

### Priority

Medium

### Trigger

The actor opens the View and Update Student Contact Profile interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-436)

### Related API IDs

- [API-STUDENT-PROFILE-GET](../api/API-STUDENT-PROFILE-GET.md)
- [API-STUDENT-PROFILE-UPDATE](../api/API-STUDENT-PROFILE-UPDATE.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [edtech-uc-10-update-student-profile.md](../../source/edtech-uc-10-update-student-profile.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-STUDENT-PROFILE-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_STUDENT_PROFILE_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-STUDENT-PROFILE-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_STUDENT_PROFILE_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-STUDENT-PROFILE-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_STUDENT_PROFILE_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-STUDENT-PROFILE-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_STUDENT_PROFILE_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-STUDENT-PROFILE-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_STUDENT_PROFILE_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-STUDENT-PROFILE-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_STUDENT_PROFILE_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-STUDENT-PROFILE-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_STUDENT_PROFILE_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
