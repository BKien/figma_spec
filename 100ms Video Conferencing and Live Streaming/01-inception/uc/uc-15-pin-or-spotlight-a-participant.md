---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-15
uc_name: "Pin or Spotlight a Participant"
---

# UC-15: Pin or Spotlight a Participant

## Functional Use-Case Specification

### Use Case ID

UC-15

### Use Case Name

Pin or Spotlight a Participant

### Description

As a participant, I want to pin a tile for myself or spotlight a tile for everyone so that the intended audience receives the selected visual focus.

### Actor(s)

Participant; Preference Service; Spotlight Service.

### Priority

P2.

### Trigger

The participant chooses a pin or spotlight action on a visible tile.

### Pre-Condition(s)

PRE-1: The client displays participant tiles in a joined session.

### Post-Condition(s)

POST-1: The client renders a pinned tile in the caller's view or a spotlighted tile in the shared session view.

### Basic Flow

1. The participant opens the controls for a participant tile.
2. The client presents the visible pin or spotlight action.
3. The participant chooses the personal pin action.
4. The client submits the preference update.
5. The system returns the caller's updated focused view.
6. The client renders the selected tile with visual prominence.

### Alternative Flow

AF-1: Remove Personal Pin

3a: The participant removes the personal pin.

3b: The client submits the update and restores the returned general layout.

AF-2: Spotlight a Participant

3c: The participant chooses the session spotlight action.

3d: The client submits the session control update.

3e: The system returns the updated shared session representation.

3f: Session clients render the selected tile with shared prominence.

AF-3: Remove Session Spotlight

2a: The participant removes the session spotlight.

2b: The client submits the session control update.

2c: Session clients restore the shared layout returned by the system.

### Exception Flow

EF-1: Focus Preference Update Failure

5a: The preference update cannot be completed.

5b: The client displays the returned failure state and retains the prior focus.

### Related UI

- Video Conferencing Desktop Features 6007:55138.
- Video Conferencing Mobile Layouts 6012:78022.
- Component evidence: Panel/Tile Menu 6073:15912, including Pin Tile for Myself and Spotlight Tile for Everyone.

### Related API IDs

API-PREFERENCES-UPDATE.
API-SPOTLIGHT-UPDATE.
API-PARTICIPANT-LIST.
API-SESSION-STATE.

### Notes

The shared model defines trusted context, persistence mapping, and query helpers. Server mutation execution uses MutationGateway and its common OCL constraints in UC-02. API command dispatch selects the named operation; it does not combine the preconditions of different operations. Read operations have no domain writes.

BR-PIN-SPOTLIGHT-01 through BR-PIN-SPOTLIGHT-03 constrain the personal pin stored by PreferenceService.update. BR-PIN-SPOTLIGHT-04 through BR-PIN-SPOTLIGHT-10 constrain the shared session spotlight stored by SpotlightService.update. Client-local preview operations do not call either server operation.

## UML Model

Classifiers and helper semantics are imported from the [shared domain model](shared-domain-model.md).

~~~plantuml
@startuml
class PreferenceService {
  update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
}
class SpotlightService {
  update(command: SpotlightCommand, session: Session): Session
}
@enduml
~~~

## Business Rules

~~~text
BR-PIN-SPOTLIGHT-01 - Focus Target
Source: Assumption
Assumption: A-15
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_PIN_SPOTLIGHT_01_FocusTarget:
  (command.hasFocusedParticipantId and command.focusedParticipantId <> null) implies
  Participant.allInstances()->exists(p | p.id = command.focusedParticipantId and p.sessionId = command.sessionId and p.status = ParticipantStatus::JOINED)
~~~

~~~text
BR-PIN-SPOTLIGHT-02 - Pin Patch
Source: Assumption
Assumption: A-15
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_PIN_SPOTLIGHT_02_PinPatch:
  view.focusedParticipantId = if command.hasFocusedParticipantId then command.focusedParticipantId else view.focusedParticipantId@pre endif
~~~

~~~text
BR-PIN-SPOTLIGHT-03 - Pin Is Personal
Source: Assumption
Assumption: A-15
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_PIN_SPOTLIGHT_03_PinIsPersonal:
  ViewPreference.allInstances() = ViewPreference.allInstances()@pre and
  ViewPreference.allInstances()@pre->select(v | v.participantId <> command.participantId)->forAll(v |
    v.layout = v.layout@pre and v.focusedParticipantId = v.focusedParticipantId@pre and
    v.sidePanel = v.sidePanel@pre and v.pictureInPicture = v.pictureInPicture@pre and v.updatedAt = v.updatedAt@pre)
~~~

~~~text
BR-PIN-SPOTLIGHT-04 - Authenticated Membership
Source: Assumption
Assumption: A-19
context SpotlightService::update(command: SpotlightCommand, session: Session): Session
pre BR_PIN_SPOTLIGHT_04_AuthenticatedMembership:
  RequestContext::authenticated and RequestContext::sessionId = command.sessionId and
  command.actorParticipantId = RequestContext::participantId and
  Participant.allInstances()->exists(p | p.id = command.actorParticipantId and
    p.principalId = RequestContext::principalId and p.sessionId = command.sessionId and
    p.status = ParticipantStatus::JOINED)
~~~

~~~text
BR-PIN-SPOTLIGHT-05 - Command Key
Source: Assumption
Assumption: A-20
context SpotlightService::update(command: SpotlightCommand, session: Session): Session
pre BR_PIN_SPOTLIGHT_05_CommandKey:
  command.idempotencyKey <> null and command.idempotencyKey.trim().size() > 0
~~~

~~~text
BR-PIN-SPOTLIGHT-06 - Spotlight Target
Source: Assumption
Assumption: A-15
context SpotlightService::update(command: SpotlightCommand, session: Session): Session
pre BR_PIN_SPOTLIGHT_06_SpotlightTarget:
  command.targetParticipantId = null or Participant.allInstances()->exists(p |
    p.id = command.targetParticipantId and p.sessionId = command.sessionId and p.status = ParticipantStatus::JOINED)
~~~

~~~text
BR-PIN-SPOTLIGHT-07 - Spotlight Actor
Source: Assumption
Assumption: A-15
context SpotlightService::update(command: SpotlightCommand, session: Session): Session
pre BR_PIN_SPOTLIGHT_07_SpotlightActor:
  Participant.allInstances()->exists(p | p.id = command.actorParticipantId and
    (p.role = ParticipantRole::HOST or p.role = ParticipantRole::BROADCASTER or p.role = ParticipantRole::STAGE_PARTICIPANT))
~~~

~~~text
BR-PIN-SPOTLIGHT-08 - Session Version
Source: Assumption
Assumption: A-15
context SpotlightService::update(command: SpotlightCommand, session: Session): Session
pre BR_PIN_SPOTLIGHT_08_SessionVersion:
  command.sessionId = session.id and session.status = SessionStatus::LIVE and command.expectedVersion = session.version
~~~

~~~text
BR-PIN-SPOTLIGHT-09 - Shared Spotlight
Source: Assumption
Assumption: A-15
context SpotlightService::update(command: SpotlightCommand, session: Session): Session
post BR_PIN_SPOTLIGHT_09_SharedSpotlight:
  result.id = session.id and result.spotlightedParticipantId = command.targetParticipantId and
  result.version = session.version@pre + 1
~~~

~~~text
BR-PIN-SPOTLIGHT-10 - Personal Pins Unaffected
Source: Assumption
Assumption: A-15
context SpotlightService::update(command: SpotlightCommand, session: Session): Session
post BR_PIN_SPOTLIGHT_10_PersonalPinsUnaffected:
  ViewPreference.allInstances() = ViewPreference.allInstances()@pre
~~~
