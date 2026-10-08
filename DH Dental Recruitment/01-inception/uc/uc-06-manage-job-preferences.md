---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-06
uc_name: "Manage Job Preferences"
---

# UC-06: Manage Job Preferences

## Functional Use-Case Specification

### Use Case ID

UC-06

### Use Case Name

Manage Job Preferences

### Description

- Allows an authenticated Job Seeker to view and save practice interest, working availability, health-benefit needs, and preferred cities.
- The profile editor and the Recommendations modal edit one shared preference record. Saved preferences provide ranking inputs to UC-07 and a geographic comparison on UC-04 job details; they do not alter the public search filters of UC-03.
- The Figma frames support the preference fields and editing surfaces. Canonical city selection, defaults, matching meanings, concurrency behavior, and API contracts are declared research decisions, not inferred backend behavior.

### Actor(s)

Authenticated ACTIVE JOB_SEEKER.

### Priority

High

### Trigger

The actor opens the Manage Job Preferences interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4741)
- [Supporting Figma node 2](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4811)
- [Supporting Figma node 3](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-3370)

### Related API IDs

- [API-JOB-PREFERENCE-GET](../api/API-JOB-PREFERENCE-GET.md)
- [API-JOB-PREFERENCE-UPDATE](../api/API-JOB-PREFERENCE-UPDATE.md)
- [API-PREFERENCE-JOB-FILTER-OPTION-LIST](../api/API-PREFERENCE-JOB-FILTER-OPTION-LIST.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [dh-dental-uc-06-manage-job-preferences.md](../../source/dh-dental-uc-06-manage-job-preferences.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-JOB-PREFERENCES-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_JOB_PREFERENCES_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-JOB-PREFERENCES-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_JOB_PREFERENCES_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-JOB-PREFERENCES-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_JOB_PREFERENCES_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-JOB-PREFERENCES-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_JOB_PREFERENCES_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-JOB-PREFERENCES-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_JOB_PREFERENCES_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-JOB-PREFERENCES-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_JOB_PREFERENCES_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-JOB-PREFERENCES-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_JOB_PREFERENCES_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
