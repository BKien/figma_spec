---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-14
uc_name: "Change Session Layout"
---

# UC-14: Change Session Layout

## Functional Use-Case Specification

### Use Case ID

UC-14

### Use Case Name

Change Session Layout

### Description

As a participant, I want to change my session layout or picture-in-picture view so that I can focus on the content that matters to me.

### Actor(s)

Participant; Preference Service.

### Priority

P2.

### Trigger

The participant chooses a layout or picture-in-picture control.

### Pre-Condition(s)

PRE-1: The client displays a joined-session interface.

### Post-Condition(s)

POST-1: The client renders the returned view preference.

### Basic Flow

1. The participant opens the view controls.
2. The client presents the layouts shown by the design.
3. The participant selects a layout.
4. The client submits the preference update.
5. The system returns the updated view preference.
6. The client renders the selected layout.

### Alternative Flow

AF-1: Enable Picture-in-Picture

3a: The participant enables picture-in-picture.

3b: The client renders the returned picture-in-picture view.

AF-2: Open or Close a Side Panel

3c: The participant opens or closes a side panel.

3d: The client adjusts the returned session layout.

### Exception Flow

EF-1: Layout Preference Update Failure

5a: The preference update cannot be completed.

5b: The client displays the returned failure state and retains the previous layout.

### Related UI

- Live Streaming Desktop Layouts 6007:96234.
- Live Streaming Mobile Layouts 6012:102740.
- Video Conferencing Desktop Layouts 6007:77656.
- Video Conferencing Mobile Layouts 6012:78022.

### Related API IDs

API-PREFERENCES-UPDATE.
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
@enduml
~~~

## Business Rules

~~~text
BR-SESSION-LAYOUT-01 - Non Null Layout And Pi P
Source: Assumption
Assumption: A-14
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_SESSION_LAYOUT_01_NonNullLayoutAndPiP:
  (command.hasLayout implies command.layout <> null) and (command.hasPictureInPicture implies command.pictureInPicture <> null)
~~~

~~~text
BR-SESSION-LAYOUT-02 - Presenter Layout
Source: Assumption
Assumption: A-14
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_SESSION_LAYOUT_02_PresenterLayout:
  (command.hasLayout and command.layout = LayoutMode::PRESENTER) implies
  ContentShare.allInstances()->exists(s | s.sessionId = command.sessionId and s.status = ShareStatus::ACTIVE)
~~~

~~~text
BR-SESSION-LAYOUT-03 - Panel Values
Source: Assumption
Assumption: A-14
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
pre BR_SESSION_LAYOUT_03_PanelValues:
  command.hasSidePanel implies (command.sidePanel = null or command.sidePanel = 'CHAT' or command.sidePanel = 'PARTICIPANTS' or command.sidePanel = 'SETTINGS')
~~~

~~~text
BR-SESSION-LAYOUT-04 - Layout Patch
Source: Assumption
Assumption: A-14
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_SESSION_LAYOUT_04_LayoutPatch:
  view.layout = if command.hasLayout then command.layout else view.layout@pre endif
~~~

~~~text
BR-SESSION-LAYOUT-05 - Pi P Patch
Source: Assumption
Assumption: A-14
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_SESSION_LAYOUT_05_PiPPatch:
  view.pictureInPicture = if command.hasPictureInPicture then command.pictureInPicture else view.pictureInPicture@pre endif
~~~

~~~text
BR-SESSION-LAYOUT-06 - Pi P Clears Panel
Source: Assumption
Assumption: A-14
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_SESSION_LAYOUT_06_PiPClearsPanel:
  view.pictureInPicture implies view.sidePanel = null
~~~

~~~text
BR-SESSION-LAYOUT-07 - Panel Patch
Source: Assumption
Assumption: A-14
context PreferenceService::update(command: PreferencePatch, media: MediaPreference, view: ViewPreference): PreferencesResult
post BR_SESSION_LAYOUT_07_PanelPatch:
  not view.pictureInPicture implies
    view.sidePanel = if command.hasSidePanel then command.sidePanel else view.sidePanel@pre endif
~~~
