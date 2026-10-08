---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-20
uc_name: "Submit a Job Application"
---

# UC-20: Submit a Job Application

## Functional Use-Case Specification

### Use Case ID

UC-20

### Use Case Name

Submit a Job Application

### Description

- Allows an authenticated Job Seeker to review the profile information included in an application and explicitly submit it for a currently visible job. The system stores one application per account/job and returns a persistent receipt.
- This activates UC-04's previously disabled Apply for this job action. It does not turn viewing a job, registering, logging in, or saving an introduction video into an application.
- Figma supports the Apply entry point only. Review/confirmation, submitted state, application persistence, eligibility, duplicate handling, and contracts are explicit research additions; no complete application or Hiring Manager workflow has been verified in the source.
- SUBMITTED means recorded by this research application. Employer delivery, employer review, interview scheduling, email/SMS, and a hiring decision are not implemented or implied.

### Actor(s)

Authenticated ACTIVE JOB_SEEKER applying for a visible job.

### Priority

High

### Trigger

The actor opens the Submit a Job Application interface.

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

- [Supporting Figma node 1](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-3837)

### Related API IDs

- [API-JOB-APPLICATION-GET](../api/API-JOB-APPLICATION-GET.md)
- [API-JOB-APPLICATION-CREATE](../api/API-JOB-APPLICATION-CREATE.md)

### Notes

The complete supplied specification is preserved byte-for-byte at [dh-dental-uc-20-submit-job-application.md](../../source/dh-dental-uc-20-submit-job-application.md). It remains authoritative for detailed flows, payloads, response examples, errors, implementation context, and validation behavior.

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
BR-JOB-APPLICATION-01 - Actor Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_JOB_APPLICATION_01_ActorIsPresent:
  command.actorId <> null and command.actorId.trim().size() > 0
~~~

~~~text
BR-JOB-APPLICATION-02 - Request Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_JOB_APPLICATION_02_RequestIsPresent:
  command.requestId <> null and command.requestId.trim().size() > 0
~~~

~~~text
BR-JOB-APPLICATION-03 - Payload Is Present
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
pre BR_JOB_APPLICATION_03_PayloadIsPresent:
  command.payload <> null and command.payload.trim().size() > 0
~~~

~~~text
BR-JOB-APPLICATION-04 - Execution Is Identified
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_JOB_APPLICATION_04_ExecutionIsIdentified:
  result.executionId <> null and result.executionId.trim().size() > 0
~~~

~~~text
BR-JOB-APPLICATION-05 - Result Matches Request
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_JOB_APPLICATION_05_ResultMatchesRequest:
  result.actorId = command.actorId and result.requestId = command.requestId
~~~

~~~text
BR-JOB-APPLICATION-06 - Result Is Completed
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_JOB_APPLICATION_06_ResultIsCompleted:
  result.status = ExecutionStatus::COMPLETED
~~~

~~~text
BR-JOB-APPLICATION-07 - Result Is Versioned
Source: Product source
context UseCaseService::execute(command: UseCaseCommand): UseCaseResult
post BR_JOB_APPLICATION_07_ResultIsVersioned:
  result.version > 0 and result.createdAt <= DateTime::now()
~~~
