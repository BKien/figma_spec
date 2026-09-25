# UC-15 — Browse Frequently Asked Questions

### Description

- Allows visitors and signed-in users to select a help category and expand/collapse questions to read project-accurate answers.
- Figma supplies the four-category navigation and accordion composition. Its sample answer promises real-time email/text notifications that UC-11 does not implement; use the research-specific content defined below instead of reproducing a false capability claim.
- The category/answer dataset, interaction rules, route, and API contract are project decisions. This UC does not introduce search, live support, an interview system, or a content-management interface.

### Actors

Visitor or signed-in user.

### Priority

Not specified in the supplied source.

### Trigger

**TRG-UC-15-01** — The actor opens the Browse Frequently Asked Questions interface.

### Preconditions

- **PRE-UC-15-01** — The interaction interface is visible to the actor.

### Postconditions

- **POST-UC-15-01** — The client displays the returned interaction outcome.

### Basic Flow

1. The actor opens the interaction interface.
2. The client displays the available controls.
3. The actor submits the interaction.
4. The client sends the request to the system.
5. The system returns an outcome.
6. The client displays the returned outcome.

### Alternative Flows

#### AF-UC-15-01

1. The actor chooses an available alternative action.
2. The client displays the returned alternative outcome.

### Exception Flows

#### EF-UC-15-01

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
-- BR-UC-15-01
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_UC_15_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
```

```ocl
-- BR-UC-15-02
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_UC_15_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
```

```ocl
-- BR-UC-15-03
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_UC_15_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
```

```ocl
-- BR-UC-15-04
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_UC_15_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
```

```ocl
-- BR-UC-15-05
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_UC_15_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
```

```ocl
-- BR-UC-15-06
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_UC_15_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
```

```ocl
-- BR-UC-15-07
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_UC_15_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
```

### Related UI

- [Supporting Figma node 1](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-2677)
- [Supporting Figma node 2](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-5503)

### Related APIs

- [API-UC-15-01](../api/api-uc-15-01.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [dh-dental-uc-15-browse-faqs.md](../source/dh-dental-uc-15-browse-faqs.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.
