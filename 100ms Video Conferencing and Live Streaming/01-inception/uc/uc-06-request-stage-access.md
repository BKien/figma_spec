---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-06
uc_name: "Request Stage Access"
---

# UC-06: Request Stage Access

## Functional Use-Case Specification

### Use Case ID

UC-06

### Use Case Name

Request Stage Access

### Description

As a viewer, I want to request stage access so that the host can consider adding me to the live stage.

### Actor(s)

Viewer; Stage Service.

### Priority

P1.

### Trigger

The viewer chooses the visible stage-request action.

### Pre-Condition(s)

PRE-1: The client displays the viewer live-session interface.

### Post-Condition(s)

POST-1: The viewer interface displays the returned request state.

POST-2: The host interface displays the returned stage-request item.

### Basic Flow

1. The viewer chooses to request stage access.
2. The client submits the stage request.
3. The system returns the request representation.
4. The viewer client displays the returned request state.
5. The host client requests session state and displays the request item.

### Alternative Flow

AF-1: Withdraw Stage Request

4a: The viewer withdraws the displayed request.

4b: The client submits the cancellation and removes the pending presentation.

### Exception Flow

EF-1: Stage Request Failure

3a: The stage service cannot complete the request.

3b: The client displays the returned failure state and keeps playback available.

### Related UI

- Live Streaming Viewer 6007:51397.
- Live Streaming Desktop Features 6007:86770.
- Live Streaming Mobile Features 6012:90506.

### Related API IDs

API-STAGE-REQUEST-CREATE.
API-SESSION-STATE.

### Notes

The shared model defines trusted context, persistence mapping, and query helpers. Server mutation execution uses MutationGateway and its common OCL constraints in UC-02. API command dispatch selects the named operation; it does not combine the preconditions of different operations. Read operations have no domain writes.

## UML Model

Classifiers and helper semantics are imported from the [shared domain model](shared-domain-model.md).

~~~plantuml
@startuml
class StageService {
  submitRequest(command: StageCommand, session: Session, stream: LiveStream): StageRequest
}
@enduml
~~~

## Business Rules

~~~text
BR-REQUEST-STAGE-01 - Authenticated Membership
Source: Assumption
Assumption: A-19
context StageService::submitRequest(command: StageCommand, session: Session, stream: LiveStream): StageRequest
pre BR_REQUEST_STAGE_01_AuthenticatedMembership:
  RequestContext::authenticated and RequestContext::sessionId = command.sessionId and
  command.actorParticipantId = RequestContext::participantId and
  Participant.allInstances()->exists(p | p.id = command.actorParticipantId and
    p.principalId = RequestContext::principalId and p.sessionId = command.sessionId and
    p.status = ParticipantStatus::JOINED)
~~~

~~~text
BR-REQUEST-STAGE-02 - Target Session
Source: Assumption
Assumption: A-19
context StageService::submitRequest(command: StageCommand, session: Session, stream: LiveStream): StageRequest
pre BR_REQUEST_STAGE_02_TargetSession:
  command.sessionId = session.id and session.status <> SessionStatus::ENDED
~~~

~~~text
BR-REQUEST-STAGE-03 - Command Key
Source: Assumption
Assumption: A-20
context StageService::submitRequest(command: StageCommand, session: Session, stream: LiveStream): StageRequest
pre BR_REQUEST_STAGE_03_CommandKey:
  command.idempotencyKey <> null and command.idempotencyKey.trim().size() > 0
~~~

~~~text
BR-REQUEST-STAGE-04 - Stream Binding
Source: Assumption
Assumption: A-06
context StageService::submitRequest(command: StageCommand, session: Session, stream: LiveStream): StageRequest
pre BR_REQUEST_STAGE_04_StreamBinding:
  stream.sessionId = session.id and session.kind = SessionKind::LIVE_STREAM and stream.status = StreamStatus::LIVE
~~~

~~~text
BR-REQUEST-STAGE-05 - Request Actions
Source: Assumption
Assumption: A-06
context StageService::submitRequest(command: StageCommand, session: Session, stream: LiveStream): StageRequest
pre BR_REQUEST_STAGE_05_RequestActions:
  command.action = StageRequestAction::CREATE or command.action = StageRequestAction::CANCEL
~~~

~~~text
BR-REQUEST-STAGE-06 - Create Viewer
Source: Assumption
Assumption: A-06
context StageService::submitRequest(command: StageCommand, session: Session, stream: LiveStream): StageRequest
pre BR_REQUEST_STAGE_06_CreateViewer:
  command.action = StageRequestAction::CREATE implies
  command.requestId = null and command.expectedVersion = null and
  Participant.allInstances()->exists(p | p.id = command.actorParticipantId and p.role = ParticipantRole::VIEWER) and
  not StageRequest.allInstances()->exists(r | r.sessionId = session.id and r.participantId = command.actorParticipantId and r.status = StageRequestStatus::PENDING)
~~~

~~~text
BR-REQUEST-STAGE-07 - Cancel Owned Pending
Source: Assumption
Assumption: A-06
context StageService::submitRequest(command: StageCommand, session: Session, stream: LiveStream): StageRequest
pre BR_REQUEST_STAGE_07_CancelOwnedPending:
  command.action = StageRequestAction::CANCEL implies StageRequest.allInstances()->one(r |
    r.id = command.requestId and r.sessionId = session.id and r.participantId = command.actorParticipantId and
    r.status = StageRequestStatus::PENDING and r.version = command.expectedVersion)
~~~

~~~text
BR-REQUEST-STAGE-08 - Request Outcome
Source: Assumption
Assumption: A-06
context StageService::submitRequest(command: StageCommand, session: Session, stream: LiveStream): StageRequest
post BR_REQUEST_STAGE_08_RequestOutcome:
  result.sessionId = session.id and result.participantId = command.actorParticipantId and
  if command.action = StageRequestAction::CREATE then result.oclIsNew() and result.status = StageRequestStatus::PENDING and
    result.version = 1 and result.createdAt <> null and result.decidedAt = null and result.decidedByParticipantId = null
  else result.id = command.requestId and not result.oclIsNew() and result.status = StageRequestStatus::CANCELLED and
    result.version = command.expectedVersion + 1 and result.decidedAt <> null and result.decidedByParticipantId = null endif
~~~

~~~text
BR-REQUEST-STAGE-09 - One Pending Request
Source: Assumption
Assumption: A-22
context StageRequest
inv BR_REQUEST_STAGE_09_OnePendingRequest:
  StageRequest.allInstances()->select(r | r.sessionId = self.sessionId and r.participantId = self.participantId and r.status = StageRequestStatus::PENDING)->size() <= 1
~~~
