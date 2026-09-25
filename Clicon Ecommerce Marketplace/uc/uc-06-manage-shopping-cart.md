# UC-06 — Manage Shopping Cart

### Description

- Allows a visitor or customer to add a selected product configuration to a shopping cart, inspect its contents, change quantities, and remove items before checkout.
- Continues UC-05 through its selected variant and quantity. Includes the cart page and shared header cart count.
- Cart persistence, staged editing, pricing rules, and API contracts below are project decisions. Figma establishes the inspected desktop controls and layout, not their backend behavior.
- Coupon application, shipping/tax quotation, checkout, Buy Now, and the homepage cart popup belong to separate integrations. This UC does not reserve stock or create an order.

### Actors

Visitor or signed-in Customer using the same browser.

### Priority

Not specified in the supplied source.

### Trigger

**TRG-UC-06-01** — The actor opens the Manage Shopping Cart interface.

### Preconditions

- **PRE-UC-06-01** — The interaction interface is visible to the actor.

### Postconditions

- **POST-UC-06-01** — The client displays the returned interaction outcome.

### Basic Flow

1. The actor opens the interaction interface.
2. The client displays the available controls.
3. The actor submits the interaction.
4. The client sends the request to the system.
5. The system returns an outcome.
6. The client displays the returned outcome.

### Alternative Flows

#### AF-UC-06-01

1. The actor chooses an available alternative action.
2. The client displays the returned alternative outcome.

### Exception Flows

#### EF-UC-06-01

1. The system returns an unsuccessful outcome.
2. The client displays the returned recovery message.

### UML Model

```plantuml
@startuml

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

@enduml
```

### Business Rules

```ocl
-- BR-UC-06-01
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_UC_06_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
```

```ocl
-- BR-UC-06-02
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_UC_06_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
```

```ocl
-- BR-UC-06-03
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_UC_06_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
```

```ocl
-- BR-UC-06-04
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_UC_06_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
```

```ocl
-- BR-UC-06-05
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_UC_06_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
```

```ocl
-- BR-UC-06-06
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_UC_06_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
```

```ocl
-- BR-UC-06-07
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_UC_06_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
```

### Related UI

- [Supporting Figma node 1](https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=493-14954)

### Related APIs

- [API-UC-06-01](../api/api-uc-06-01.md)
- [API-UC-06-02](../api/api-uc-06-02.md)
- [API-UC-06-03](../api/api-uc-06-03.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [clicon-uc-06-manage-shopping-cart.md](../source/clicon-uc-06-manage-shopping-cart.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.
