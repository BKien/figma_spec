---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-05
uc_name: "Watch a Live Stream"
---

# UC-05: Watch a Live Stream

## Functional Use-Case Specification

### Use Case ID

UC-05

### Use Case Name

Watch a Live Stream

### Description

As a viewer, I want to open the live session so that I can watch the broadcast and access viewer controls.

### Actor(s)

Viewer; Live Stream Service.

### Priority

P0.

### Trigger

The viewer opens the live-session interface.

### Pre-Condition(s)

PRE-1: The client has a live-session destination to display.

### Post-Condition(s)

POST-1: The client displays live playback and the viewer controls returned by the system.

### Basic Flow

1. The viewer opens the live session.
2. The client requests the current session representation.
3. The system returns the viewer-facing stream state.
4. The client renders playback and viewer controls.

### Alternative Flow

AF-1: Open Viewer Session Menu

4a: The viewer opens the session menu.

4b: The client displays the viewer actions shown by the design.

### Exception Flow

EF-1: Live Session Unavailable

3a: The live-session representation cannot be returned.

3b: The client displays the visible loading or unavailable state.

### Related UI

- Live Streaming Viewer 6007:51397.
- Live Streaming Mobile Preview 6012:44409.

### Related API IDs

API-LIVE-STREAM-VIEW.
API-SESSION-STATE.

### Notes

The shared model defines trusted context, persistence mapping, and query helpers. Server mutation execution uses MutationGateway and its common OCL constraints in UC-02. API command dispatch selects the named operation; it does not combine the preconditions of different operations. Read operations have no domain writes.

## UML Model

Classifiers and helper semantics are imported from the [shared domain model](shared-domain-model.md).

~~~plantuml
@startuml
class LiveStreamService {
  view(sessionId: String, participantId: String, session: Session, stream: LiveStream): ViewerSession
}
@enduml
~~~

## Business Rules

~~~text
BR-WATCH-STREAM-01 - Authenticated Membership
Source: Assumption
Assumption: A-19
context LiveStreamService::view(sessionId: String, participantId: String, session: Session, stream: LiveStream): ViewerSession
pre BR_WATCH_STREAM_01_AuthenticatedMembership:
  RequestContext::authenticated and RequestContext::sessionId = sessionId and
  participantId = RequestContext::participantId and
  Participant.allInstances()->exists(p | p.id = participantId and
    p.principalId = RequestContext::principalId and p.sessionId = sessionId and
    p.status = ParticipantStatus::JOINED)
~~~

~~~text
BR-WATCH-STREAM-02 - Viewer Target
Source: Assumption
Assumption: A-05
context LiveStreamService::view(sessionId: String, participantId: String, session: Session, stream: LiveStream): ViewerSession
pre BR_WATCH_STREAM_02_ViewerTarget:
  session.id = sessionId and stream.sessionId = sessionId and session.kind = SessionKind::LIVE_STREAM and
  session.status <> SessionStatus::ENDED and Participant.allInstances()->exists(p | p.id = participantId and
    (p.role = ParticipantRole::VIEWER or p.role = ParticipantRole::STAGE_PARTICIPANT))
~~~

~~~text
BR-WATCH-STREAM-03 - Viewer Representation
Source: Assumption
Assumption: A-05
context LiveStreamService::view(sessionId: String, participantId: String, session: Session, stream: LiveStream): ViewerSession
post BR_WATCH_STREAM_03_ViewerRepresentation:
  result.sessionId = session.id and result.participantId = participantId and
  result.role = Participant.allInstances()->any(p | p.id = participantId).role
~~~

~~~text
BR-WATCH-STREAM-04 - Stream Snapshot
Source: Assumption
Assumption: A-05
context LiveStreamService::view(sessionId: String, participantId: String, session: Session, stream: LiveStream): ViewerSession
post BR_WATCH_STREAM_04_StreamSnapshot:
  result.streamStatus = stream.status and result.streamVersion = stream.version and result.sessionVersion = session.version
~~~

~~~text
BR-WATCH-STREAM-05 - Playback Availability
Source: Assumption
Assumption: A-05
context LiveStreamService::view(sessionId: String, participantId: String, session: Session, stream: LiveStream): ViewerSession
post BR_WATCH_STREAM_05_PlaybackAvailability:
  result.canPlayMedia = (stream.status = StreamStatus::LIVE)
~~~

~~~text
BR-WATCH-STREAM-06 - Publishing Availability
Source: Assumption
Assumption: A-05
context LiveStreamService::view(sessionId: String, participantId: String, session: Session, stream: LiveStream): ViewerSession
post BR_WATCH_STREAM_06_PublishingAvailability:
  result.canPublishMedia = (stream.status = StreamStatus::LIVE and result.role = ParticipantRole::STAGE_PARTICIPANT)
~~~

~~~text
BR-WATCH-STREAM-07 - Muted Playback Start
Source: Assumption
Assumption: A-05
context LiveStreamService::view(sessionId: String, participantId: String, session: Session, stream: LiveStream): ViewerSession
post BR_WATCH_STREAM_07_MutedPlaybackStart:
  result.initialAudioMuted
~~~
