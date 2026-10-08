---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-12
uc_name: "Manage Notification Preferences"
---

# UC-12: Manage Notification Preferences

## Functional Use-Case Specification

### Use Case ID

UC-12

### Use Case Name

Manage Notification Preferences

### Description

- Lets a Student choose which learning-notification categories are enabled and temporarily pause them all without losing individual choices.
- Implements the Notification Settings screen as a preference-management feature. It does not create notifications, send email/SMS, open browser push permissions, or implement an inbox/scheduler.
- Initial values, master-pause behavior, delivery boundary, and contracts are project decisions. The source's highlighted switches are example state, not a new account's consent or subscription settings.

### Actor(s)

Authenticated Student with completed onboarding.

### Priority

Medium

### Trigger

The actor opens the Manage Notification Preferences interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-221)

### Related API IDs

- [API-STUDENT-NOTIFICATION-PREFERENCE-GET](../api/API-STUDENT-NOTIFICATION-PREFERENCE-GET.md)
- [API-STUDENT-NOTIFICATION-PREFERENCE-UPDATE](../api/API-STUDENT-NOTIFICATION-PREFERENCE-UPDATE.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [edtech-uc-12-manage-notification-preferences.md](../../source/edtech-uc-12-manage-notification-preferences.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-NOTIFICATION-PREFERENCES-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_NOTIFICATION_PREFERENCES_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-NOTIFICATION-PREFERENCES-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_NOTIFICATION_PREFERENCES_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-NOTIFICATION-PREFERENCES-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_NOTIFICATION_PREFERENCES_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-NOTIFICATION-PREFERENCES-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_NOTIFICATION_PREFERENCES_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-NOTIFICATION-PREFERENCES-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_NOTIFICATION_PREFERENCES_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-NOTIFICATION-PREFERENCES-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_NOTIFICATION_PREFERENCES_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-NOTIFICATION-PREFERENCES-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_NOTIFICATION_PREFERENCES_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
