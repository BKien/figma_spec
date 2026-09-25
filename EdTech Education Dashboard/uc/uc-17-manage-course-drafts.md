# UC-17 — Create and Edit a Course Draft

### Description

- Allows an Instructor to create an owned draft and save course metadata, ordered modules, video lessons, and single-choice quizzes before publication.
- Defines the authoring counterpart of UC-04 and UC-07–09. Drafts are invisible to Student discovery and cannot receive enrollments.
- Instructor authoring is an approved project extension. The source Figma supplies Student presentation patterns, not an Instructor editor; the API and content constraints below are project decisions.

### Actors

ACTIVE, email-verified Instructor authenticated through UC-16/UC-02.

### Priority

Not specified in the supplied source.

### Trigger

**TRG-UC-17-01** — The actor opens the Create and Edit a Course Draft interface.

### Preconditions

- **PRE-UC-17-01** — The interaction interface is visible to the actor.

### Postconditions

- **POST-UC-17-01** — The client displays the returned interaction outcome.

### Basic Flow

1. The actor opens the interaction interface.
2. The client displays the available controls.
3. The actor submits the interaction.
4. The client sends the request to the system.
5. The system returns an outcome.
6. The client displays the returned outcome.

### Alternative Flows

#### AF-UC-17-01

1. The actor chooses an available alternative action.
2. The client displays the returned alternative outcome.

### Exception Flows

#### EF-UC-17-01

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
-- BR-UC-17-01
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_UC_17_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
```

```ocl
-- BR-UC-17-02
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_UC_17_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
```

```ocl
-- BR-UC-17-03
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_UC_17_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
```

```ocl
-- BR-UC-17-04
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_UC_17_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
```

```ocl
-- BR-UC-17-05
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_UC_17_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
```

```ocl
-- BR-UC-17-06
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_UC_17_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
```

```ocl
-- BR-UC-17-07
-- Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_UC_17_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
```

### Related UI

- [Supporting Figma node 1](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-1030)

### Related APIs

- [API-UC-17-01](../api/api-uc-17-01.md)
- [API-UC-17-02](../api/api-uc-17-02.md)
- [API-UC-17-03](../api/api-uc-17-03.md)
- [API-UC-17-04](../api/api-uc-17-04.md)
- [API-UC-17-05](../api/api-uc-17-05.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [edtech-uc-17-manage-course-drafts.md](../source/edtech-uc-17-manage-course-drafts.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.
