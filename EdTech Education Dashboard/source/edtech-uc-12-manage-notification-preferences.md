# UC-12: Manage Notification Preferences

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Manage Notification Preferences

Description:

- Lets a Student choose which learning-notification categories are enabled and temporarily pause them all without losing individual choices.
- Implements the Notification Settings screen as a preference-management feature. It does not create notifications, send email/SMS, open browser push permissions, or implement an inbox/scheduler.
- Initial values, master-pause behavior, delivery boundary, and contracts are project decisions. The source's highlighted switches are example state, not a new account's consent or subscription settings.

Primary Actor:

Authenticated Student with completed onboarding.

Preconditions:

- UC-01–03 account/session/onboarding exist. Implement `/student/settings/notifications` with direct navigation/reload support and UC-11's settings shell.
- Notification preference storage is available. Actual notification producers/delivery are not a dependency for saving these settings and remain separately scoped.

Postconditions:

- Success: All six switches persist for the current account with a new revision; reload restores them. Effective category preferences reflect the master pause.
- Failure: No rejected update replaces prior settings. The form distinguishes saved values from an unsaved draft.
- A successful save is never presented as sent, scheduled, or delivered content. Course progress, deadlines, language, profile contact method, and security/account emails are unchanged.

Main Flow:

1. The Student opens Notification Settings from the settings sidebar.
2. Load stored settings or the explicit first-use defaults. Render Pause All Notifications and five category switches.
3. The Student changes one or more switches. Changes remain a local draft until Save Changes, a supplementary action, is selected.
4. Validate and submit the full preference payload with expectedRevision.
5. Save the values together and return both stored choices and their effective paused/unpaused values.
6. Display `Notification preferences saved.` and the permanent explanatory note `These preferences are saved. Notification delivery is not available in this version.`

Alternative Flow:

A.1 — Master pause

- pauseAll=true makes every effective category false while retaining each individual stored choice. Disable category editing while the master pause is on; show their saved positions dimmed with Paused labels.
- Turning pauseAll off restores the effect of saved category choices. It does not enable every category, schedule a backlog, or send catch-up messages.
- Individual category values submitted by a client may still be changed with pauseAll=true; the server stores valid complete values and computes effective flags. The UI's disabled state is presentation, not an alternative schema.

A.2 — Category meaning and scope

- courseProgressReminders corresponds to Course Progress Reminders; assignmentDeadlines to Assignment Deadlines; liveEventsWebinars to Live Events & Webinars; weeklyLearningTips to Weekly Learning Tips; promotionsDiscounts to Promotions & Discounts.
- Labels establish preference categories only. Existing quiz due dates do not automatically create reminders; project-upload assignments, webinars, promotions, and weekly tips do not become implemented features because their switches exist.
- These preferences do not suppress UC-01 verification messages or future transactional account-recovery messages. Pause All applies only to the five learning/marketing categories on this screen; explanatory copy states that account-verification messages are unaffected.
- A future delivery UC must check current effective preference at send time and define its channels, eligibility, schedule, and content. This UC neither promises those mechanisms nor prescribes their implementation.

A.3 — Defaults and navigation

- Initial stored/default values are false for every category and pauseAll=false. No sample checked switch is imported as account choice.
- Leaving a dirty form offers Stay or Discard changes. Navigation does not autosave. A failed preference load disables editing until a current revision is available.
- Settings links to UC-11 Learning Preferences and UC-12 Notifications are enabled. Account Settings, Security & Privacy, notification bell/inbox, and undefined destinations remain disabled until separately implemented.

Exception Flow:

E.1 — Invalid or contradictory input

- All six preference fields must be JSON booleans. Reject omitted values, strings/numbers, client-supplied effective values, delivery channels, account IDs, timestamps, and unknown keys.
- Having pauseAll=false and all categories=false is valid; it means no category is enabled. Having pauseAll=true and some categories=true is also valid, preserving choices for later unpause.

E.2 — Conflicts and unknown saves

- A save uses the latest expectedRevision. A stale revision returns SETTINGS_CONFLICT without changing any field, even if some requested values match. Show Load latest, preserve the local draft for review until the user accepts replacement, and never silently overwrite a newer device's values.
- Every accepted PUT increments revision once, including an unchanged deliberate save. GET does not create a persisted record or change revision. Initial defaults have revision=0 and updatedAt=null; the first write creates the account-scoped settings record.
- After a timeout or malformed response, stop further writes and read the resource. Show the actual saved values without falsely attributing another tab's changes to this request. If they differ from the local draft, offer Load latest or a deliberate reapplication using the current revision. Never replay a stale save automatically.
- If reconciliation also fails, show Check saved settings again and keep mutations disabled. A successful later read establishes the current state. Account changes clear drafts, cached private data, and obsolete requests.

E.3 — Service failure

- NOTIFICATION_PREFERENCES_UNAVAILABLE shows a retry without replacing stored values with defaults. A failed save never produces an Email sent, Notifications enabled on this device, or Push permission granted message.

UI Integration:

- `21 Settings Notification`, node `222:221`.
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-221
- Live context/screenshot inspected on 2026-09-20. Preserve settings sidebar, six labelled switch rows, grouping, and descriptive hierarchy.
- Add explicit Save Changes, saved/unsaved feedback, paused labels, and the delivery-unavailable/account-email explanation. Reword source receive/get-notified claims so they describe category preferences without promising active delivery.
- Default switch states, master-pause semantics, errors, and dirty-form notice are supplements. No mobile design or frozen dataset is claimed. Switches expose accessible checked/disabled states and keyboard interaction.

API Endpoint:

`GET /api/v1/student/notification-preferences`

`PUT /api/v1/student/notification-preferences`

Request Body:

```json
{
  "expectedRevision": 0,
  "pauseAll": true,
  "courseProgressReminders": true,
  "assignmentDeadlines": true,
  "liveEventsWebinars": false,
  "weeklyLearningTips": false,
  "promotionsDiscounts": false
}
```

All seven keys are required: expectedRevision is a nonnegative JSON safe integer; the six preferences are booleans. PUT is a complete replacement of these six stored choices, not a patch and not a command to send anything. No body/query input is accepted by GET.

Successful Response:

```json
{
  "success": true,
  "message": "Notification preferences retrieved.",
  "data": {
    "revision": 0,
    "preferences": {
      "pauseAll": false,
      "courseProgressReminders": false,
      "assignmentDeadlines": false,
      "liveEventsWebinars": false,
      "weeklyLearningTips": false,
      "promotionsDiscounts": false
    },
    "effective": {
      "courseProgressReminders": false,
      "assignmentDeadlines": false,
      "liveEventsWebinars": false,
      "weeklyLearningTips": false,
      "promotionsDiscounts": false
    },
    "updatedAt": null
  }
}
```

```json
{
  "success": true,
  "message": "Notification preferences saved.",
  "data": {
    "revision": 1,
    "preferences": {
      "pauseAll": true,
      "courseProgressReminders": true,
      "assignmentDeadlines": true,
      "liveEventsWebinars": false,
      "weeklyLearningTips": false,
      "promotionsDiscounts": false
    },
    "effective": {
      "courseProgressReminders": false,
      "assignmentDeadlines": false,
      "liveEventsWebinars": false,
      "weeklyLearningTips": false,
      "promotionsDiscounts": false
    },
    "updatedAt": "2026-09-20T10:00:00.000Z"
  }
}
```

HTTP 200. data has exactly revision, preferences, effective, updatedAt. preferences contains exactly the six booleans in the request excluding expectedRevision. effective contains exactly the five category booleans; for each category it equals preferences[category] AND NOT preferences.pauseAll. It contains no pauseAll field and signifies eligibility preference, not proof of actual delivery availability. updatedAt is null before the first write, otherwise server ISO UTC. GET defaults have revision=0 without a mutation. All response keys are required; no channels, messages, jobs, or subscription tokens are returned.

Error Response:

```json
{
  "success": false,
  "statusCode": 503,
  "code": "NOTIFICATION_PREFERENCES_UNAVAILABLE",
  "message": "Notification preferences are temporarily unavailable. Please try again later.",
  "timestamp": "2026-09-20T10:00:00.000Z",
  "path": "/api/v1/student/notification-preferences"
}
```

All endpoints require UC-02's ACTIVE, verified STUDENT session and completed UC-03 onboarding. The session selects the account; no userId, role, or email query may select another profile. GET has no body; no endpoint accepts query parameters. Reject unknown body keys and wrong JSON types.

Use the established error envelope: success=false, statusCode matching HTTP status, code, message, server ISO UTC timestamp, and actual pathname without query. Omit data. Only VALIDATION_ERROR may add errors mapping field paths to nonempty arrays of strings.

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | You must sign in to continue. |
| 403 | ONBOARDING_REQUIRED | Complete your learning profile to continue. |
| 409 | SETTINGS_CONFLICT | These settings changed. Load the latest values to continue. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

401 clears private draft state and opens `/sign-in`; 403 opens `/student/onboarding`. A service error does not imply logout. These UCs add no new request-limit policy.

503 NOTIFICATION_PREFERENCES_UNAVAILABLE: `Notification preferences are temporarily unavailable. Please try again later.`.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement account-scoped preference reads/writes in NestJS/TypeScript with all-false category defaults, independent master pause, revision, and timestamp. Persist the six booleans together and calculate effective values from the returned snapshot. Do not queue or transmit messages or modify verification-email handling. Keep this record independent from contact-method and learning-preference revisions.

### Frontend UI Context

Implement NotificationSettingsPage in React/TypeScript/Tailwind using UC-11's shared settings shell and the inspected six-row layout. Add explicit saving and honest availability copy. Preserve saved individual choices visually while paused, and avoid portraying unsaved switch changes as server-confirmed preferences.

### Frontend Logic and API Context

Track confirmed preferences and local draft separately; compute local preview of pause behavior but replace it with server values after save. Send the full set once per Save, handle conflicts/reconciliation through the shared rules, and clear obsolete account state. A save does not request browser notification permission, invoke Mailpit, create an inbox message, or trigger delivery.

### Validation and Error-Handling Context

Require exact boolean payloads, current revision, and authenticated account ownership. Derive effective values on the server, not from a client field. Distinguish a saved preference from an operational notification channel, retain selections when pausing, and never imply that a failed load means the Student opted out.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
