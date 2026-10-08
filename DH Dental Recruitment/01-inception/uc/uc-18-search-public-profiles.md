---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-18
uc_name: "Search and Filter Public Candidate Profiles"
---

# UC-18: Search and Filter Public Candidate Profiles

## Functional Use-Case Specification

### Use Case ID

UC-18

### Use Case Name

Search and Filter Public Candidate Profiles

### Description

- Allows any visitor to browse, search, filter, and paginate only the candidate profiles explicitly published through UC-17.
- Uses the source's public profile grid and filters. Search semantics, preferred-city interpretation, stable ordering, and API contract are research decisions, not evidence of an employer account or hiring authorization workflow.
- A published position is the candidate's desired position, and skills/experience are self-declared; the directory is not a professional verification service.

### Actor(s)

Visitor or signed-in user.

### Priority

Medium

### Trigger

The actor opens the Search and Filter Public Candidate Profiles interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-1700)

### Related API IDs

- [API-CANDIDATE-PROFILE-LIST](../api/API-CANDIDATE-PROFILE-LIST.md)
- [API-CANDIDATE-PROFILE-JOB-FILTER-OPTION-LIST](../api/API-CANDIDATE-PROFILE-JOB-FILTER-OPTION-LIST.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [dh-dental-uc-18-search-public-profiles.md](../../source/dh-dental-uc-18-search-public-profiles.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-SEARCH-PROFILES-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SEARCH_PROFILES_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-SEARCH-PROFILES-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SEARCH_PROFILES_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-SEARCH-PROFILES-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SEARCH_PROFILES_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-SEARCH-PROFILES-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SEARCH_PROFILES_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-SEARCH-PROFILES-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SEARCH_PROFILES_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-SEARCH-PROFILES-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SEARCH_PROFILES_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-SEARCH-PROFILES-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SEARCH_PROFILES_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
