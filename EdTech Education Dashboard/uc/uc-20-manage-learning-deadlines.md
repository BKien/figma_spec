# UC-20 — Manage Course Learning Deadlines

### Description

- Allows the owning Instructor to set, change, or clear a recommended completion deadline for each published VIDEO or QUIZ unit.
- Activates UC-05 upcoming tasks with authored dates. A learning deadline is advisory: it does not close content, shorten a quiz attempt, reduce scores, or revoke enrollment.
- Schedule is a separate mutable resource. This explicitly extends UC-18's null dueAt baseline without changing its immutable published curriculum, unit IDs, grading, or course revision.
- Instructor scheduling controls and the Student schedule view are project supplements; Figma's Student upcoming-task presentation does not define scheduling behavior.

### Actors

Authenticated ACTIVE, email-verified Instructor who owns the published course. An enrolled Student is the reader of the resulting schedule.

### Priority

Not specified in the supplied source.

### Trigger

**TRG-UC-20-01** — The actor opens the Manage Course Learning Deadlines interface.

### Preconditions

- **PRE-UC-20-01** — The interaction interface is visible to the actor.

### Postconditions

- **POST-UC-20-01** — The client displays the returned interaction outcome.

### Basic Flow

1. The actor opens the interaction interface.
2. The client displays the available controls.
3. The actor submits the interaction.
4. The client sends the request to the system.
5. The system returns an outcome.
6. The client displays the returned outcome.

### Alternative Flows

#### AF-UC-20-01

1. The actor chooses an available alternative action.
2. The client displays the returned alternative outcome.

### Exception Flows

#### EF-UC-20-01

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
-- BR-UC-20-01
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_UC_20_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
```

```ocl
-- BR-UC-20-02
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_UC_20_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
```

```ocl
-- BR-UC-20-03
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_UC_20_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
```

```ocl
-- BR-UC-20-04
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_UC_20_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
```

```ocl
-- BR-UC-20-05
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_UC_20_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
```

```ocl
-- BR-UC-20-06
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_UC_20_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
```

```ocl
-- BR-UC-20-07
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_UC_20_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
```

### Related UI

- [Supporting Figma node 1](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-1374)

### Related APIs

- [API-UC-20-01](../api/api-uc-20-01.md)
- [API-UC-20-02](../api/api-uc-20-02.md)
- [API-UC-20-03](../api/api-uc-20-03.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [edtech-uc-20-manage-learning-deadlines.md](../source/edtech-uc-20-manage-learning-deadlines.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.
