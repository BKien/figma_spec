---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-09
uc_name: "Manage Education"
---

# UC-09: Manage Education

## Functional Use-Case Specification

### Use Case ID

UC-09

### Use Case Name

Manage Education

### Description

- Allows a Job Seeker to view, add, revise, and remove completed education/program entries in one profile section, then save the complete list.
- Figma shows repeatable Dental Program/Degree and In Year controls. This UC treats the year as the completion year and does not collect institution, transcript, license, accreditation, or planned graduation data.
- Program choices beyond visible samples, duplicate rules, year limits, ordering, routes, and contracts are explicit research decisions. Education entries are self-declared and are not a credential-verification result.

### Actor(s)

Authenticated ACTIVE JOB_SEEKER.

### Priority

Medium

### Trigger

The actor opens the Manage Education interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-5235)
- [Supporting Figma node 2](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-5306)

### Related API IDs

- [API-PROFILE-EDUCATION-GET](../api/API-PROFILE-EDUCATION-GET.md)
- [API-PROFILE-EDUCATION-UPDATE](../api/API-PROFILE-EDUCATION-UPDATE.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [dh-dental-uc-09-manage-education.md](../../source/dh-dental-uc-09-manage-education.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-EDUCATION-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_EDUCATION_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-EDUCATION-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_EDUCATION_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-EDUCATION-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_EDUCATION_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-EDUCATION-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_EDUCATION_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-EDUCATION-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_EDUCATION_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-EDUCATION-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_EDUCATION_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-EDUCATION-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_EDUCATION_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
