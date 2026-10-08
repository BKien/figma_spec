---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-13
uc_name: "Manage Saved Billing and Shipping Addresses"
---

# UC-13: Manage Saved Billing and Shipping Addresses

## Functional Use-Case Specification

### Use Case ID

UC-13

### Use Case Name

Manage Saved Billing and Shipping Addresses

### Description

- Allows an authenticated customer to view, create, and replace one saved billing address and one saved shipping address independently from Account Settings.
- Enables deliberate reuse of saved addresses in UC-07 checkout without changing its request or order-snapshot contracts.
- Address slots, validation, revision handling, and checkout mapping are project decisions. Figma establishes the two desktop address forms and their separate save actions.
- Multiple-address books, deletion, default-address selection, geocoding, payment-card management, and carrier address verification are outside this UC.

### Actor(s)

Signed-in Customer with an active, verified account.

### Priority

Medium

### Trigger

The actor opens the Manage Saved Billing and Shipping Addresses interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=493-12498)
- [Supporting Figma node 2](https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=494-17004)

### Related API IDs

- [API-ACCOUNT-ADDRESS-LIST](../api/API-ACCOUNT-ADDRESS-LIST.md)
- [API-ACCOUNT-ADDRESS-SAVE](../api/API-ACCOUNT-ADDRESS-SAVE.md)
- [API-ADDRESS-CHECKOUT-OPTION-LIST](../api/API-ADDRESS-CHECKOUT-OPTION-LIST.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [clicon-uc-13-manage-saved-addresses.md](../../source/clicon-uc-13-manage-saved-addresses.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-SAVED-ADDRESSES-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SAVED_ADDRESSES_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-SAVED-ADDRESSES-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SAVED_ADDRESSES_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-SAVED-ADDRESSES-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_SAVED_ADDRESSES_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-SAVED-ADDRESSES-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SAVED_ADDRESSES_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-SAVED-ADDRESSES-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SAVED_ADDRESSES_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-SAVED-ADDRESSES-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SAVED_ADDRESSES_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-SAVED-ADDRESSES-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_SAVED_ADDRESSES_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
