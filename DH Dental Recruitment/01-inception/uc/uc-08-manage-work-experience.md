---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-08
uc_name: "Manage Work Experience and Resume"
---

# UC-08: Manage Work Experience and Resume

## Functional Use-Case Specification

### Use Case ID

UC-08

### Use Case Name

Manage Work Experience and Resume

### Description

- Allows a Job Seeker to maintain their relevant-experience band, self-declared board-certification status, self-ratings in four dental areas, and optional resume in one profile section.
- This is the experience-summary form shown in Figma. It is not an employment-history timeline, employer reference check, licensing service, or professional verification process.
- The visible fields and five-star controls come from the source frames. Dropdown vocabularies, optionality, file constraints, routes, save behavior, and API contracts are explicit project decisions; no Technical Report or existing backend contract has been supplied for this feature.

### Actor(s)

Authenticated ACTIVE JOB_SEEKER.

### Priority

High

### Trigger

The actor opens the Manage Work Experience and Resume interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4915)
- [Supporting Figma node 2](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-5039)

### Related API IDs

- [API-PROFILE-WORK-EXPERIENCE-GET](../api/API-PROFILE-WORK-EXPERIENCE-GET.md)
- [API-PROFILE-WORK-EXPERIENCE-UPDATE](../api/API-PROFILE-WORK-EXPERIENCE-UPDATE.md)
- [API-PROFILE-RESUME-GET](../api/API-PROFILE-RESUME-GET.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [dh-dental-uc-08-manage-work-experience.md](../../source/dh-dental-uc-08-manage-work-experience.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-WORK-EXPERIENCE-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_WORK_EXPERIENCE_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-WORK-EXPERIENCE-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_WORK_EXPERIENCE_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-WORK-EXPERIENCE-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_WORK_EXPERIENCE_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-WORK-EXPERIENCE-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_WORK_EXPERIENCE_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-WORK-EXPERIENCE-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_WORK_EXPERIENCE_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-WORK-EXPERIENCE-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_WORK_EXPERIENCE_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-WORK-EXPERIENCE-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_WORK_EXPERIENCE_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
