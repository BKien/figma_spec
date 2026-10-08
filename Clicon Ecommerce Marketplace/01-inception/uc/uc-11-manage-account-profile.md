---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-11
uc_name: "Manage Account Profile"
---

# UC-11: Manage Account Profile

## Functional Use-Case Specification

### Use Case ID

UC-11

### Use Case Name

Manage Account Profile

### Description

- Allows an authenticated customer to view account information and update profile names, optional secondary contact details, and an optional profile location.
- Implements the Account Setting section of the inspected settings frame, using the account established by UC-01 and session defined by UC-02.
- Field semantics, editable boundaries, location fixtures, concurrency behavior, and API contracts are project decisions. Figma establishes the desktop controls and layout.
- Changing the primary email, password, avatar, billing/shipping addresses, or account status is outside this UC. Profile updates do not modify previously placed orders or browser-scoped cart, wishlist, and comparison data.

### Actor(s)

Signed-in Customer with an active, verified account.

### Priority

Medium

### Trigger

The actor opens the Manage Account Profile interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=478-17305)

### Related API IDs

- [API-PROFILE-AUTH-SESSION-GET](../api/API-PROFILE-AUTH-SESSION-GET.md)
- [API-ACCOUNT-PROFILE-GET](../api/API-ACCOUNT-PROFILE-GET.md)
- [API-ACCOUNT-PROFILE-UPDATE](../api/API-ACCOUNT-PROFILE-UPDATE.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [clicon-uc-11-manage-account-profile.md](../../source/clicon-uc-11-manage-account-profile.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-ACCOUNT-PROFILE-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_ACCOUNT_PROFILE_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-ACCOUNT-PROFILE-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_ACCOUNT_PROFILE_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-ACCOUNT-PROFILE-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_ACCOUNT_PROFILE_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-ACCOUNT-PROFILE-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_ACCOUNT_PROFILE_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-ACCOUNT-PROFILE-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_ACCOUNT_PROFILE_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-ACCOUNT-PROFILE-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_ACCOUNT_PROFILE_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-ACCOUNT-PROFILE-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_ACCOUNT_PROFILE_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
