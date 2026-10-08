---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-01
uc_name: "Register a Job Seeker Account"
---

# UC-01: Register a Job Seeker Account

## Functional Use-Case Specification

### Use Case ID

UC-01

### Use Case Name

Register a Job Seeker Account

### Description

- Allows a visitor to create a DH Dental Recruitment account for finding dental-sector employment, using the DentiHire-branded Sign Up form.
- Captures first name, last name, email, password, mobile number, optional referral source, and the visitor's declaration that they are at least 18 years old. Selecting Get Started also records agreement to the displayed project terms notice.
- This specification begins the Job Seeker scope. Hiring Professionals registration and account switching require their own defined lifecycle and are not enabled here.
- Form controls and layout are supported by the Figma frame identified below. API contracts, validation, account state, repeat handling, and limits are project requirements for the research implementation; no DH Dental Technical Report or existing backend contract has been supplied.

### Actor(s)

Unauthenticated visitor registering as a Job Seeker.

### Priority

High

### Trigger

The actor opens the Register a Job Seeker Account interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-2622)

### Related API IDs

- [API-JOB-SEEKER-REGISTRATION-CREATE](../api/API-JOB-SEEKER-REGISTRATION-CREATE.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [dh-dental-uc-01-register-job-seeker.md](../../source/dh-dental-uc-01-register-job-seeker.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-REGISTER-JOB-SEEKER-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_REGISTER_JOB_SEEKER_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-REGISTER-JOB-SEEKER-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_REGISTER_JOB_SEEKER_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-REGISTER-JOB-SEEKER-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_REGISTER_JOB_SEEKER_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-REGISTER-JOB-SEEKER-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_REGISTER_JOB_SEEKER_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-REGISTER-JOB-SEEKER-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_REGISTER_JOB_SEEKER_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-REGISTER-JOB-SEEKER-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_REGISTER_JOB_SEEKER_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-REGISTER-JOB-SEEKER-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_REGISTER_JOB_SEEKER_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
