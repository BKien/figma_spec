---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-01
uc_name: "Review Join Preview and Permissions"
---

# UC-01: Review Join Preview and Permissions

## Functional Use-Case Specification

### Use Case ID

UC-01

### Use Case Name

Review Join Preview and Permissions

### Description

As a prospective participant, I want to review my camera and microphone preview so that I understand how I will appear before joining.

### Actor(s)

Prospective Participant; Preview Service.

### Priority

P0.

### Trigger

The prospective participant opens a session preview.

### Pre-Condition(s)

PRE-1: The client displays the pre-join interface.

### Post-Condition(s)

POST-1: The client displays the selected camera and microphone state.

POST-2: The client displays the returned permission outcome when permission is requested.

### Basic Flow

1. The prospective participant opens the pre-join interface.
2. The client presents the camera, microphone, name, and permission controls shown by the design.
3. The prospective participant chooses the displayed permission action.
4. The client requests access and receives an outcome.
5. The client renders the media preview and current control states.

### Alternative Flow

AF-1: Turn Off Preview Media

5a: The prospective participant turns the microphone or camera off.

5b: The client renders the corresponding muted preview state.

### Exception Flow

EF-1: Permission Access Denied

4a: Access is not granted.

4b: The client displays the permission-denied dialog and its visible recovery action.

### Related UI

- Broadcaster Preview 6007:51245.
- Video Conferencing Desktop Preview 6066:89727.
- Video Conferencing Mobile Preview 6066:89005.

### Related API IDs

None

### Notes

Preview preparation is client-local. Its participantKey identifies local draft state, not persisted session membership.

This interaction is client-local.

## UML Model

Classifiers and helper semantics are imported from the [shared domain model](shared-domain-model.md).

~~~plantuml
@startuml
class PreviewService {
  prepare(command: PreviewCommand): PreviewState
}
@enduml
~~~

## Business Rules

~~~text
BR-JOIN-PREVIEW-01 - Permission And Hardware
Source: Assumption
Assumption: A-01
context PreviewService::prepare(command: PreviewCommand): PreviewState
post BR_JOIN_PREVIEW_01_PermissionAndHardware:
  (result.cameraEnabled implies result.cameraPermission = PermissionStatus::GRANTED and result.cameraAvailable and command.requestCamera) and
  (result.microphoneEnabled implies result.microphonePermission = PermissionStatus::GRANTED and result.microphoneAvailable and command.requestMicrophone)
~~~

~~~text
BR-JOIN-PREVIEW-02 - Viewer Preview Muted
Source: Assumption
Assumption: A-01
context PreviewService::prepare(command: PreviewCommand): PreviewState
post BR_JOIN_PREVIEW_02_ViewerPreviewMuted:
  command.role = ParticipantRole::VIEWER implies not result.cameraEnabled and not result.microphoneEnabled
~~~

~~~text
BR-JOIN-PREVIEW-03 - Name Readiness
Source: Assumption
Assumption: A-01
context PreviewService::prepare(command: PreviewCommand): PreviewState
post BR_JOIN_PREVIEW_03_NameReadiness:
  result.isReadyToJoin = (command.displayName <> null and command.displayName.trim().size() > 0 and command.displayName.trim().size() <= 50)
~~~

~~~text
BR-JOIN-PREVIEW-04 - Preview Key
Source: Assumption
Assumption: A-01
context PreviewService::prepare(command: PreviewCommand): PreviewState
post BR_JOIN_PREVIEW_04_PreviewKey:
  result.participantKey = command.participantKey
~~~

~~~text
BR-JOIN-PREVIEW-05 - Camera Denied State
Source: Assumption
Assumption: A-01
context PreviewService::prepare(command: PreviewCommand): PreviewState
post BR_JOIN_PREVIEW_05_CameraDeniedState:
  result.cameraPermission <> PermissionStatus::GRANTED implies not result.cameraEnabled
~~~

~~~text
BR-JOIN-PREVIEW-06 - Microphone Denied State
Source: Assumption
Assumption: A-01
context PreviewService::prepare(command: PreviewCommand): PreviewState
post BR_JOIN_PREVIEW_06_MicrophoneDeniedState:
  result.microphonePermission <> PermissionStatus::GRANTED implies not result.microphoneEnabled
~~~

~~~text
BR-JOIN-PREVIEW-07 - Client Local Preview
Source: Assumption
Assumption: A-01
context PreviewService::prepare(command: PreviewCommand): PreviewState
post BR_JOIN_PREVIEW_07_ClientLocalPreview:
  Participant.allInstances() = Participant.allInstances()@pre and
  MediaPreference.allInstances() = MediaPreference.allInstances()@pre and
  ViewPreference.allInstances() = ViewPreference.allInstances()@pre
~~~
