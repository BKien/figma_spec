---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-04
uc_name: "View Job Details"
---

# UC-04: View Job Details

## Functional Use-Case Specification

### Use Case ID

UC-04

### Use Case Name

View Job Details

### Description

- Allows a visitor to inspect a published job's public description, requirements, and office summary. An authenticated eligible Job Seeker can additionally view the member-only office information and available media.
- Reuses the public and signed-in detail compositions without inventing a complete Apply flow. Viewing, signing in, and opening media do not create an application or record interest.
- Figma provides the visible detail sections. Audience boundaries, null handling, related-job ranking, media delivery, and API contracts are project decisions; backend behavior is not established by a static frame.

### Actor(s)

Visitor or authenticated ACTIVE JOB_SEEKER. An incomplete profile and unverified contacts do not prevent reading member details under UC-01/02.

### Priority

High

### Trigger

The actor opens the View Job Details interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-2309)
- [Supporting Figma node 2](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-3837)

### Related API IDs

- [API-JOB-DETAIL](../api/API-JOB-DETAIL.md)
- [API-JOB-SEEKER-JOB-DETAIL](../api/API-JOB-SEEKER-JOB-DETAIL.md)
- [API-JOB-SEEKER-JOB-ASSET-GET](../api/API-JOB-SEEKER-JOB-ASSET-GET.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [dh-dental-uc-04-view-job-details.md](../../source/dh-dental-uc-04-view-job-details.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-JOB-DETAIL-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_JOB_DETAIL_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-JOB-DETAIL-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_JOB_DETAIL_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-JOB-DETAIL-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_JOB_DETAIL_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-JOB-DETAIL-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_JOB_DETAIL_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-JOB-DETAIL-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_JOB_DETAIL_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-JOB-DETAIL-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_JOB_DETAIL_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-JOB-DETAIL-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_JOB_DETAIL_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
