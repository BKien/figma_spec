---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-14
uc_name: "View and Manage Browsing History"
---

# UC-14: View and Manage Browsing History

## Functional Use-Case Specification

### Use Case ID

UC-14

### Use Case Name

View and Manage Browsing History

### Description

- Allows an authenticated customer to revisit previously viewed products, search/filter their history, load older entries, and enable or disable future recording.
- Connects successful product-detail viewing in UC-05 with the account Browsing History page.
- Recording scope, retention, grouping, filtering, pagination, and API contracts below are project decisions. Figma establishes the inspected desktop controls and dated product groups.
- This UC does not track guests, collect external browser history, recommend products, record cart actions, or implement individual/bulk history deletion.

### Actor(s)

Signed-in Customer with an active, verified account.

### Priority

Low

### Trigger

The actor opens the View and Manage Browsing History interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=478-12199)

### Related API IDs

- [API-BROWSING-HISTORY-LIST](../api/API-BROWSING-HISTORY-LIST.md)
- [API-BROWSING-HISTORY-PREFERENCE-UPDATE](../api/API-BROWSING-HISTORY-PREFERENCE-UPDATE.md)
- [API-BROWSING-HISTORY-VIEW-CREATE](../api/API-BROWSING-HISTORY-VIEW-CREATE.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [clicon-uc-14-manage-browsing-history.md](../../source/clicon-uc-14-manage-browsing-history.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-BROWSING-HISTORY-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_BROWSING_HISTORY_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-BROWSING-HISTORY-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_BROWSING_HISTORY_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-BROWSING-HISTORY-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_BROWSING_HISTORY_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-BROWSING-HISTORY-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_BROWSING_HISTORY_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-BROWSING-HISTORY-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_BROWSING_HISTORY_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-BROWSING-HISTORY-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_BROWSING_HISTORY_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-BROWSING-HISTORY-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_BROWSING_HISTORY_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
