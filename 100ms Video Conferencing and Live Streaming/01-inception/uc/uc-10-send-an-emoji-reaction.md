---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-10
uc_name: "Send an Emoji Reaction"
---

# UC-10: Send an Emoji Reaction

## Functional Use-Case Specification

### Use Case ID

UC-10

### Use Case Name

Send an Emoji Reaction

### Description

As a participant, I want to send an emoji reaction so that I can respond without interrupting the session.

### Actor(s)

Participant; Collaboration Service.

### Priority

P2.

### Trigger

The participant opens the reaction controls and chooses an emoji.

### Pre-Condition(s)

PRE-1: The participant is viewing a joined-session interface.

### Post-Condition(s)

POST-1: The client renders the reaction event returned by the system.

### Basic Flow

1. The participant opens the emoji reaction controls.
2. The client presents the available reaction choices.
3. The participant chooses a reaction.
4. The client submits the reaction.
5. The system returns the created event.
6. The client renders the reaction in the session.

### Alternative Flow

AF-1: Dismiss Reaction Choices

3a: The participant closes the reaction controls without selecting an item.

3b: The client restores the session controls.

### Exception Flow

EF-1: Reaction Creation Failure

5a: The reaction cannot be created.

5b: The client displays the returned failure notice without closing the session.

### Related UI

- Video Conferencing Desktop Features 6007:55138.
- Component evidence: Modal/Emoji Reactions.

### Related API IDs

API-REACTION-CREATE.
API-SESSION-STATE.

### Notes

The shared model defines trusted context, persistence mapping, and query helpers. Server mutation execution uses MutationGateway and its common OCL constraints in UC-02. API command dispatch selects the named operation; it does not combine the preconditions of different operations. Read operations have no domain writes.

## UML Model

Classifiers and helper semantics are imported from the [shared domain model](shared-domain-model.md).

~~~plantuml
@startuml
class CollaborationService {
  sendReaction(command: ReactionCommand, session: Session): ReactionEvent
}
@enduml
~~~

## Business Rules

~~~text
BR-SEND-REACTION-01 - Authenticated Membership
Source: Assumption
Assumption: A-19
context CollaborationService::sendReaction(command: ReactionCommand, session: Session): ReactionEvent
pre BR_SEND_REACTION_01_AuthenticatedMembership:
  RequestContext::authenticated and RequestContext::sessionId = command.sessionId and
  command.participantId = RequestContext::participantId and
  Participant.allInstances()->exists(p | p.id = command.participantId and
    p.principalId = RequestContext::principalId and p.sessionId = command.sessionId and
    p.status = ParticipantStatus::JOINED)
~~~

~~~text
BR-SEND-REACTION-02 - Target Session
Source: Assumption
Assumption: A-19
context CollaborationService::sendReaction(command: ReactionCommand, session: Session): ReactionEvent
pre BR_SEND_REACTION_02_TargetSession:
  command.sessionId = session.id and session.status <> SessionStatus::ENDED
~~~

~~~text
BR-SEND-REACTION-03 - Command Key
Source: Assumption
Assumption: A-20
context CollaborationService::sendReaction(command: ReactionCommand, session: Session): ReactionEvent
pre BR_SEND_REACTION_03_CommandKey:
  command.idempotencyKey <> null and command.idempotencyKey.trim().size() > 0
~~~

~~~text
BR-SEND-REACTION-04 - Created Identity
Source: Assumption
Assumption: A-10
context CollaborationService::sendReaction(command: ReactionCommand, session: Session): ReactionEvent
post BR_SEND_REACTION_04_CreatedIdentity:
  result.oclIsNew() and result.id <> null and result.sessionId = command.sessionId and result.participantId = command.participantId
~~~

~~~text
BR-SEND-REACTION-05 - Reaction Value
Source: Assumption
Assumption: A-10
context CollaborationService::sendReaction(command: ReactionCommand, session: Session): ReactionEvent
post BR_SEND_REACTION_05_ReactionValue:
  result.reaction = command.reaction and result.createdAt <> null and result.sequence = session.version@pre + 1
~~~

~~~text
BR-SEND-REACTION-06 - Participation Unaffected
Source: Assumption
Assumption: A-10
context CollaborationService::sendReaction(command: ReactionCommand, session: Session): ReactionEvent
post BR_SEND_REACTION_06_ParticipationUnaffected:
  Participant.allInstances() = Participant.allInstances()@pre
~~~

~~~text
BR-SEND-REACTION-07 - No Implicit Stage Request
Source: Assumption
Assumption: A-10
context CollaborationService::sendReaction(command: ReactionCommand, session: Session): ReactionEvent
post BR_SEND_REACTION_07_NoImplicitStageRequest:
  StageRequest.allInstances() = StageRequest.allInstances()@pre
~~~
