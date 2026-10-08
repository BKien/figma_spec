---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-03
uc_name: "Search and Filter Available Jobs"
---

# UC-03: Search and Filter Available Jobs

## Functional Use-Case Specification

### Use Case ID

UC-03

### Use Case Name

Search and Filter Available Jobs

### Description

- Allows visitors and signed-in Job Seekers to browse open published dental jobs, search by text, filter by location/work schedule/specialism, and paginate results.
- Search, filters, and pagination are alternate ways to accomplish one job-discovery goal, not separate use cases. Results lead to UC-04 detail.
- Figma supports the list/card/filter controls. Search semantics, canonical job data, fixture normalization, API contracts, and state rules below are project decisions; this is not a Technical Report quotation.

### Actor(s)

Visitor or authenticated Job Seeker. Public job discovery does not require registration or a complete profile.

### Priority

High

### Trigger

The actor opens the Search and Filter Available Jobs interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-1937)

### Related API IDs

- [API-JOB-FILTER-OPTION-LIST](../api/API-JOB-FILTER-OPTION-LIST.md)
- [API-JOB-LIST](../api/API-JOB-LIST.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [dh-dental-uc-03-search-filter-jobs.md](../../source/dh-dental-uc-03-search-filter-jobs.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-SEARCH-JOBS-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SEARCH_JOBS_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-SEARCH-JOBS-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SEARCH_JOBS_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-SEARCH-JOBS-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SEARCH_JOBS_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-SEARCH-JOBS-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SEARCH_JOBS_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-SEARCH-JOBS-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SEARCH_JOBS_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-SEARCH-JOBS-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SEARCH_JOBS_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-SEARCH-JOBS-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SEARCH_JOBS_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
