---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-07
uc_name: "View Personalized Job Recommendations"
---

# UC-07: View Personalized Job Recommendations

## Functional Use-Case Specification

### Use Case ID

UC-07

### Use Case Name

View Personalized Job Recommendations

### Description

- Allows an authenticated Job Seeker to browse visible jobs in their saved desired position, ordered by how many active job preferences they satisfy.
- Uses UC-05 basic information and UC-06 preferences to provide a reproducible personalized listing. It differs from UC-03 manual public search and UC-04 related jobs; it creates no application or saved-job state.
- Figma supplies the Recommendations page, cards, sidebar, pagination, and preference-modal entry point. The recommendation rules, explanations, setup/empty/error states, route, and API contract are explicit research decisions. This is a deterministic feature; the UI does not claim AI prediction, a professional suitability score, or verified qualifications.

### Actor(s)

Authenticated ACTIVE JOB_SEEKER.

### Priority

Medium

### Trigger

The actor opens the View Personalized Job Recommendations interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-2956)
- [Supporting Figma node 2](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-3370)
- [Supporting Figma node 3](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-3837)

### Related API IDs

- [API-JOB-RECOMMENDATION-LIST](../api/API-JOB-RECOMMENDATION-LIST.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [dh-dental-uc-07-view-job-recommendations.md](../../source/dh-dental-uc-07-view-job-recommendations.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-JOB-RECOMMENDATIONS-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_JOB_RECOMMENDATIONS_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-JOB-RECOMMENDATIONS-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_JOB_RECOMMENDATIONS_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-JOB-RECOMMENDATIONS-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_JOB_RECOMMENDATIONS_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-JOB-RECOMMENDATIONS-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_JOB_RECOMMENDATIONS_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-JOB-RECOMMENDATIONS-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_JOB_RECOMMENDATIONS_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-JOB-RECOMMENDATIONS-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_JOB_RECOMMENDATIONS_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-JOB-RECOMMENDATIONS-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_JOB_RECOMMENDATIONS_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
