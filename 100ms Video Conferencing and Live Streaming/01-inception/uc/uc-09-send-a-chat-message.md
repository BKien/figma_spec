---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-09
uc_name: "Send a Chat Message"
---

# UC-09: Send a Chat Message

## Functional Use-Case Specification

### Use Case ID

UC-09

### Use Case Name

Send a Chat Message

### Description

As a participant, I want to send a chat message so that I can communicate with people in the session.

### Actor(s)

Participant; Collaboration Service.

### Priority

P1.

### Trigger

The participant opens chat, enters text, and chooses Send.

### Pre-Condition(s)

PRE-1: The client displays the session chat panel.

### Post-Condition(s)

POST-1: The client displays the message returned by the system.

### Basic Flow

1. The participant opens the chat panel.
2. The client displays the returned message history.
3. The participant enters a message and chooses Send.
4. The client submits the message.
5. The system returns the created message.
6. The client appends it to the visible conversation.

### Alternative Flow

AF-1: Close Chat Without Sending

3a: The participant closes chat without sending.

3b: The client restores the session layout.

### Exception Flow

EF-1: Chat Message Creation Failure

5a: The collaboration service cannot create the message.

5b: The client displays a failure notice and preserves the entered text.

### Related UI

- Live Streaming Desktop Features 6007:86770.
- Video Conferencing Desktop Features 6007:55138.
- Live Streaming Mobile Features 6012:90506.
- Video Conferencing Mobile Features 6012:52233.

### Related API IDs

API-CHAT-MESSAGE-CREATE.
API-CHAT-MESSAGE-LIST.

### Notes

The shared model defines trusted context, persistence mapping, and query helpers. Server mutation execution uses MutationGateway and its common OCL constraints in UC-02. API command dispatch selects the named operation; it does not combine the preconditions of different operations. Read operations have no domain writes.

## UML Model

Classifiers and helper semantics are imported from the [shared domain model](shared-domain-model.md).

~~~plantuml
@startuml
class CollaborationService {
  sendMessage(command: ChatCommand, session: Session): ChatMessage
  listMessages(query: MessageQuery, session: Session): MessagePage
}
@enduml
~~~

## Business Rules

~~~text
BR-SEND-CHAT-01 - Authenticated Membership
Source: Assumption
Assumption: A-19
context CollaborationService::sendMessage(command: ChatCommand, session: Session): ChatMessage
pre BR_SEND_CHAT_01_AuthenticatedMembership:
  RequestContext::authenticated and RequestContext::sessionId = command.sessionId and
  command.senderParticipantId = RequestContext::participantId and
  Participant.allInstances()->exists(p | p.id = command.senderParticipantId and
    p.principalId = RequestContext::principalId and p.sessionId = command.sessionId and
    p.status = ParticipantStatus::JOINED)
~~~

~~~text
BR-SEND-CHAT-02 - Target Session
Source: Assumption
Assumption: A-19
context CollaborationService::sendMessage(command: ChatCommand, session: Session): ChatMessage
pre BR_SEND_CHAT_02_TargetSession:
  command.sessionId = session.id and session.status <> SessionStatus::ENDED
~~~

~~~text
BR-SEND-CHAT-03 - Command Key
Source: Assumption
Assumption: A-20
context CollaborationService::sendMessage(command: ChatCommand, session: Session): ChatMessage
pre BR_SEND_CHAT_03_CommandKey:
  command.idempotencyKey <> null and command.idempotencyKey.trim().size() > 0
~~~

~~~text
BR-SEND-CHAT-04 - Message Body
Source: Assumption
Assumption: A-09
context CollaborationService::sendMessage(command: ChatCommand, session: Session): ChatMessage
pre BR_SEND_CHAT_04_MessageBody:
  command.body <> null and command.body.trim().size() > 0 and command.body.trim().size() <= 1000
~~~

~~~text
BR-SEND-CHAT-05 - Created Identity
Source: Assumption
Assumption: A-09
context CollaborationService::sendMessage(command: ChatCommand, session: Session): ChatMessage
post BR_SEND_CHAT_05_CreatedIdentity:
  result.oclIsNew() and result.id <> null and result.sessionId = command.sessionId and result.senderParticipantId = command.senderParticipantId
~~~

~~~text
BR-SEND-CHAT-06 - Message Value
Source: Assumption
Assumption: A-09
context CollaborationService::sendMessage(command: ChatCommand, session: Session): ChatMessage
post BR_SEND_CHAT_06_MessageValue:
  result.body = command.body.trim() and result.sentAt <> null and result.sequence = session.version@pre + 1
~~~

~~~text
BR-SEND-CHAT-07 - Authenticated Membership
Source: Assumption
Assumption: A-19
context CollaborationService::listMessages(query: MessageQuery, session: Session): MessagePage
pre BR_SEND_CHAT_07_AuthenticatedMembership:
  RequestContext::authenticated and RequestContext::sessionId = query.sessionId and
  query.requesterParticipantId = RequestContext::participantId and
  Participant.allInstances()->exists(p | p.id = query.requesterParticipantId and
    p.principalId = RequestContext::principalId and p.sessionId = query.sessionId and
    p.status = ParticipantStatus::JOINED)
~~~

~~~text
BR-SEND-CHAT-08 - Message Page Input
Source: Assumption
Assumption: A-23
context CollaborationService::listMessages(query: MessageQuery, session: Session): MessagePage
pre BR_SEND_CHAT_08_MessagePageInput:
  query.sessionId = session.id and session.status <> SessionStatus::ENDED and query.pageSize > 0 and query.pageSize <= 50 and
  Paging::validCursor(session.id, query.cursor, 'messages')
~~~

~~~text
BR-SEND-CHAT-09 - Message History
Source: Assumption
Assumption: A-23
context CollaborationService::listMessages(query: MessageQuery, session: Session): MessagePage
post BR_SEND_CHAT_09_MessageHistory:
  result = Paging::messages(session.id, query.pageSize, query.cursor) and result.items->forAll(m | m.sessionId = session.id)
~~~
