---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-12
uc_name: "Configure Audio and Video Devices"
---

# UC-12: Configure Audio and Video Devices

## Functional Use-Case Specification

### Use Case ID

UC-12

### Use Case Name

Configure Audio and Video Devices

### Description

As a participant, I want to select my microphone, camera, and audio output so that the session uses my preferred devices.

### Actor(s)

Participant; Preference Service.

### Priority

P1.

### Trigger

The participant opens device settings.

### Pre-Condition(s)

PRE-1: The client displays a preview or joined-session interface.

### Post-Condition(s)

POST-1: The client displays and applies the returned device preferences.

### Basic Flow

1. The participant opens device settings.
2. The client presents the available microphone, camera, and audio-output choices.
3. The participant selects the desired values and confirms.
4. The client applies the selection locally in preview, or submits the preference update from the joined session.
5. The client receives the local result or the returned device preferences.
6. The client applies the returned settings to the preview or session.

### Alternative Flow

AF-1: Close Settings Without Confirming

3a: The participant closes settings without confirming.

3b: The client restores the previous preview or session state.

### Exception Flow

EF-1: Device Preference Application Failure

5a: The selected preference cannot be applied.

5b: The client displays the returned failure state and keeps the previous visible selection.

### Related UI

- Settings 6007:51132.
- Video Conferencing Desktop Preview 6066:89727.
- Video Conferencing Mobile Preview 6066:89005.

### Related API IDs

API-PREFERENCES-UPDATE.
API-SESSION-JOIN.
API-SESSION-STATE.

### Notes

The shared model defines trusted context, persistence mapping, and query helpers. Server mutation execution uses MutationGateway and its common OCL constraints in UC-02. API command dispatch selects the named operation; it does not combine the preconditions of different operations. Read operations have no domain writes.

UC-12 through UC-14 and the personal-pin rules in UC-15 constrain one atomic PreferenceService.update operation. Field-presence guards determine which values change. Client-local preview operations do not call this server operation.

## UML Model

Classifiers and helper semantics are imported from the [shared domain model](shared-domain-model.md).

~~~plantuml
@startuml
class PreferenceService {
  update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
}
class ClientPreferenceService {
  selectDevices(draft: PreviewDraft, microphone: String, camera: String, speaker: String): PreviewDraft
}
@enduml
~~~

## Business Rules

~~~text
BR-CONFIGURE-DEVICES-01 - Authenticated Membership
Source: Assumption
Assumption: A-19
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_CONFIGURE_DEVICES_01_AuthenticatedMembership:
  RequestContext::authenticated and RequestContext::sessionId = command.sessionId and
  command.participantId = RequestContext::participantId and
  Participant.allInstances()->exists(p | p.id = command.participantId and
    p.principalId = RequestContext::principalId and p.sessionId = command.sessionId and
    p.status = ParticipantStatus::JOINED)
~~~

~~~text
BR-CONFIGURE-DEVICES-02 - Command Key
Source: Assumption
Assumption: A-20
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_CONFIGURE_DEVICES_02_CommandKey:
  command.idempotencyKey <> null and command.idempotencyKey.trim().size() > 0
~~~

~~~text
BR-CONFIGURE-DEVICES-03 - Preference Target
Source: Assumption
Assumption: A-12
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_CONFIGURE_DEVICES_03_PreferenceTarget:
  media.participantId = command.participantId and view.participantId = command.participantId and
  Session.allInstances()->exists(s | s.id = command.sessionId and s.status <> SessionStatus::ENDED)
~~~

~~~text
BR-CONFIGURE-DEVICES-04 - Preference Identity
Source: Assumption
Assumption: A-12
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_CONFIGURE_DEVICES_04_PreferenceIdentity:
  result.media = media and result.view = view and media.updatedAt <> null and view.updatedAt <> null
~~~

~~~text
BR-CONFIGURE-DEVICES-05 - microphone Device Id Syntax
Source: Assumption
Assumption: A-12
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_CONFIGURE_DEVICES_05_microphoneDeviceIdSyntax:
  command.hasMicrophoneDeviceId implies (command.microphoneDeviceId = null or command.microphoneDeviceId.trim().size() > 0)
~~~

~~~text
BR-CONFIGURE-DEVICES-06 - microphone Device Id Patch
Source: Assumption
Assumption: A-12
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_CONFIGURE_DEVICES_06_microphoneDeviceIdPatch:
  media.microphoneDeviceId = if command.hasMicrophoneDeviceId then command.microphoneDeviceId else media.microphoneDeviceId@pre endif
~~~

~~~text
BR-CONFIGURE-DEVICES-07 - camera Device Id Syntax
Source: Assumption
Assumption: A-12
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_CONFIGURE_DEVICES_07_cameraDeviceIdSyntax:
  command.hasCameraDeviceId implies (command.cameraDeviceId = null or command.cameraDeviceId.trim().size() > 0)
~~~

~~~text
BR-CONFIGURE-DEVICES-08 - camera Device Id Patch
Source: Assumption
Assumption: A-12
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_CONFIGURE_DEVICES_08_cameraDeviceIdPatch:
  media.cameraDeviceId = if command.hasCameraDeviceId then command.cameraDeviceId else media.cameraDeviceId@pre endif
~~~

~~~text
BR-CONFIGURE-DEVICES-09 - speaker Device Id Syntax
Source: Assumption
Assumption: A-12
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_CONFIGURE_DEVICES_09_speakerDeviceIdSyntax:
  command.hasSpeakerDeviceId implies (command.speakerDeviceId = null or command.speakerDeviceId.trim().size() > 0)
~~~

~~~text
BR-CONFIGURE-DEVICES-10 - speaker Device Id Patch
Source: Assumption
Assumption: A-12
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_CONFIGURE_DEVICES_10_speakerDeviceIdPatch:
  media.speakerDeviceId = if command.hasSpeakerDeviceId then command.speakerDeviceId else media.speakerDeviceId@pre endif
~~~

~~~text
BR-CONFIGURE-DEVICES-11 - Other Media Unchanged
Source: Assumption
Assumption: A-12
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_CONFIGURE_DEVICES_11_OtherMediaUnchanged:
  MediaPreference.allInstances() = MediaPreference.allInstances()@pre and
  MediaPreference.allInstances()@pre->select(m | m.participantId <> command.participantId)->forAll(m |
    m.microphoneDeviceId = m.microphoneDeviceId@pre and m.cameraDeviceId = m.cameraDeviceId@pre and
    m.speakerDeviceId = m.speakerDeviceId@pre and m.virtualBackgroundId = m.virtualBackgroundId@pre and m.updatedAt = m.updatedAt@pre)
~~~

~~~text
BR-CONFIGURE-DEVICES-12 - Local Device Availability
Source: Assumption
Assumption: A-12
context ClientPreferenceService::selectDevices(draft: PreviewDraft, microphone: String, camera: String, speaker: String): PreviewDraft
pre BR_CONFIGURE_DEVICES_12_LocalDeviceAvailability:
  (microphone = null or DeviceCatalog::isAvailable(draft.participantKey, microphone)) and
  (camera = null or DeviceCatalog::isAvailable(draft.participantKey, camera)) and
  (speaker = null or DeviceCatalog::isAvailable(draft.participantKey, speaker))
~~~

~~~text
BR-CONFIGURE-DEVICES-13 - Local Device Draft
Source: Assumption
Assumption: A-12
context ClientPreferenceService::selectDevices(draft: PreviewDraft, microphone: String, camera: String, speaker: String): PreviewDraft
post BR_CONFIGURE_DEVICES_13_LocalDeviceDraft:
  result = draft and draft.microphoneDeviceId = microphone and draft.cameraDeviceId = camera and
  draft.speakerDeviceId = speaker and draft.virtualBackgroundId = draft.virtualBackgroundId@pre
~~~
