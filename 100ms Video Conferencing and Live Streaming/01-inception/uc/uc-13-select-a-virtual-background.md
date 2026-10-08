---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-13
uc_name: "Select a Virtual Background"
---

# UC-13: Select a Virtual Background

## Functional Use-Case Specification

### Use Case ID

UC-13

### Use Case Name

Select a Virtual Background

### Description

As a participant, I want to select a virtual background so that my preview uses the chosen appearance.

### Actor(s)

Participant; Preference Service.

### Priority

P2.

### Trigger

The participant opens virtual-background choices.

### Pre-Condition(s)

PRE-1: The client displays a camera preview.

### Post-Condition(s)

POST-1: The client displays the returned background preference in the preview.

### Basic Flow

1. The participant opens virtual-background choices.
2. The client presents the available background previews.
3. The participant selects a background.
4. The client applies the selection locally in preview, or submits the preference update from the joined session.
5. The client receives the local result or the returned media preference.
6. The client renders the selected background in the preview.

### Alternative Flow

AF-1: Select No Background

3a: The participant selects the no-background choice.

3b: The client removes the background treatment from the preview.

### Exception Flow

EF-1: Background Preference Application Failure

5a: The preference cannot be applied.

5b: The client displays the returned failure state and retains the previous preview.

### Related UI

- Virtual Background 6026:1184329.

### Related API IDs

API-PREFERENCES-UPDATE.
API-SESSION-JOIN.
API-BACKGROUND-LIST.
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
  listBackgrounds(): Set(VirtualBackground)
}
class ClientPreferenceService {
  selectBackground(draft: PreviewDraft, backgroundId: String): PreviewDraft
}
@enduml
~~~

## Business Rules

~~~text
BR-SELECT-BACKGROUND-01 - Available Background
Source: Assumption
Assumption: A-13
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_SELECT_BACKGROUND_01_AvailableBackground:
  command.hasVirtualBackgroundId implies (command.virtualBackgroundId = null or
    VirtualBackground.allInstances()->exists(b | b.id = command.virtualBackgroundId and b.active))
~~~

~~~text
BR-SELECT-BACKGROUND-02 - Background Patch
Source: Assumption
Assumption: A-13
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_SELECT_BACKGROUND_02_BackgroundPatch:
  media.virtualBackgroundId = if command.hasVirtualBackgroundId then command.virtualBackgroundId else media.virtualBackgroundId@pre endif
~~~

~~~text
BR-SELECT-BACKGROUND-03 - Local Background
Source: Assumption
Assumption: A-13
context ClientPreferenceService::selectBackground(draft: PreviewDraft, backgroundId: String): PreviewDraft
pre BR_SELECT_BACKGROUND_03_LocalBackground:
  backgroundId = null or VirtualBackground.allInstances()->exists(b | b.id = backgroundId and b.active)
~~~

~~~text
BR-SELECT-BACKGROUND-04 - Local Background Draft
Source: Assumption
Assumption: A-13
context ClientPreferenceService::selectBackground(draft: PreviewDraft, backgroundId: String): PreviewDraft
post BR_SELECT_BACKGROUND_04_LocalBackgroundDraft:
  result = draft and draft.virtualBackgroundId = backgroundId and
  draft.microphoneDeviceId = draft.microphoneDeviceId@pre and draft.cameraDeviceId = draft.cameraDeviceId@pre and draft.speakerDeviceId = draft.speakerDeviceId@pre
~~~

~~~text
BR-SELECT-BACKGROUND-05 - Catalog Reader
Source: Assumption
Assumption: A-19
context PreferenceService::listBackgrounds(): Set(VirtualBackground)
pre BR_SELECT_BACKGROUND_05_CatalogReader:
  RequestContext::authenticated
~~~

~~~text
BR-SELECT-BACKGROUND-06 - Catalog Result
Source: Assumption
Assumption: A-13
context PreferenceService::listBackgrounds(): Set(VirtualBackground)
post BR_SELECT_BACKGROUND_06_CatalogResult:
  result = VirtualBackground.allInstances()->select(b | b.active)
~~~

~~~text
BR-SELECT-BACKGROUND-07 - Catalog Identity
Source: Assumption
Assumption: A-13
context PreferenceService::listBackgrounds(): Set(VirtualBackground)
post BR_SELECT_BACKGROUND_07_CatalogIdentity:
  result->isUnique(id) and result->forAll(b | b.assetReference <> null and b.assetReference.trim().size() > 0)
~~~
