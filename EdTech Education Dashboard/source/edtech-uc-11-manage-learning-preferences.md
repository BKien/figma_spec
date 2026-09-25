# UC-11: Manage Learning Preferences

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Manage Learning Preferences

Description:

- Lets the Student save interface theme, default video speed, default subtitles, preferred content language, and an optional weekly learning target.
- Applies supported preferences to the existing Student shell and UC-08 player, and enables target editing in UC-07's goal card.
- Options, defaults, persistence, dark appearance, and the goal editor are project decisions. The source shows the preference controls but not all menus or behavioral rules. No course translation or measured learning-time service is implied.

Primary Actor:

Authenticated Student with completed onboarding.

Preconditions:

- Implement `/student/settings/learning` with reload support and the existing settings sidebar.
- UC-08 player and UC-07 goal-card integration points exist. UC-02 session identifies the preference owner.
- No weekly learning measurement is available in the current baseline. A target can be stored, while dashboard weeklyGoalPercent remains null until a later measurement source exists.

Postconditions:

- Success: Preferences persist for the account. Supported theme changes apply after confirmation; newly opened videos use the saved playback/subtitle defaults; the goal card displays the saved target.
- Failure: A rejected mutation does not change saved preferences or falsely announce a new target. Local draft changes remain distinguishable from confirmed settings.
- Saving preferences changes no enrollment, grade, completed-unit state, UC-03 motivation answers, or notification subscription.

Main Flow:

1. The Student opens Learning Preferences and loads the account's values/defaults.
2. Change theme, video speed, subtitles, or preferred language; open Weekly Learning Goal to set or clear a target in the supplementary inline editor.
3. Select the supplementary Save Changes button. Validate and submit all preferences with expectedRevision.
4. On success, update the confirmed cache, apply the theme, and show `Learning preferences saved.`
5. UC-07's goal card reads the saved target. The next UC-08 video opened applies speed/subtitle defaults while preserving its actual saved playback position and progress.
6. Reload or sign in on another device to retrieve the account settings; AUTO resolves against each device's own color-scheme preference.

Alternative Flow:

A.1 — Theme

- LIGHT, DARK, and AUTO are supported. AUTO uses the browser/OS color-scheme preference. Source frames establish the light appearance; dark colors are an explicitly added theme with legible text, controls, focus, and errors.
- Apply the confirmed theme to authenticated Student pages UC-03–12. Public sign-in/registration retain their established appearance. Changing theme must not reload the page, submit another form, lose a quiz draft, or restart a video.
- Unsaved changes are not applied globally. On session/account change clear the previous account's theme state before loading the new account.

A.2 — Video and language behavior

- Speed choices are 0.5, 1, 1.5, 2, matching UC-08. A local change inside an already-open player overrides only that player; it does not save account preferences. Loading another video applies the saved default again.
- Subtitles off means no track is enabled initially. If on, choose a returned caption track whose language primary subtag matches preferredCourseLanguage; otherwise choose the first track. With captions=[], keep captions unavailable and explain that the lesson has no subtitles.
- preferredCourseLanguage supports en and vi. It is a preference for available content/caption language, not an interface translation switch. The current catalogue has no multilingual variant-selection contract, so saving it does not filter out courses, dub a video, translate questions, or alter ranking. Show this limitation beside the selector.
- A settings change in another tab is applied on next route entry/video load, not by unexpectedly changing the currently playing video's controls. Theme AUTO may react to OS changes immediately.

A.3 — Weekly target

- weeklyGoalMinutes is null (no target) or a multiple of 30 from 30 through 2400. The inline editor offers the corresponding half-hour increments and Clear goal. Save Changes commits the draft; Cancel goal edit restores the last value within that local form.
- Display the target as hours/week with halves where needed. The source's 5 hours/week is a sample, not an automatic default. Initial state is No weekly goal set.
- UC-07's Edit Goal opens `/student/settings/learning#weekly-goal`. After saving, a Back to course link returns to a valid course/module context when the navigation state supplies one; otherwise use My Courses. Do not accept arbitrary external return URLs.
- UC-05's weeklyGoalPercent stays null without measuredSecondsThisWeek. No weekday streak/tick, study timer, goal-completion notification, or progress credit is created merely by setting a target. A future metric uses this target converted to seconds and UC-05's Monday-start UTC week.

A.4 — Unsaved navigation

- Leaving a dirty settings form offers Stay or Discard changes. Preference edits do not autosave. A failed load does not silently initialize saved defaults over existing settings.
- If preference retrieval fails on a learning page, use temporary light appearance, 1x speed, and subtitles off with an unobtrusive Preferences unavailable notice; never persist those fallbacks. A later successful load applies defaults at the next safe navigation/player initialization point.

Exception Flow:

E.1 — Invalid values

- Unsupported enum, stringified speed/goal, fractional revision, out-of-range target, or extra fields yields VALIDATION_ERROR. Preserve the draft and show field-specific feedback.

E.2 — Conflicting or unknown write

- A save uses the latest expectedRevision. A stale revision returns SETTINGS_CONFLICT without changing any field, even if some requested values match. Show Load latest, preserve the local draft for review until the user accepts replacement, and never silently overwrite a newer device's values.
- Every accepted PUT increments revision once, including an unchanged deliberate save. GET does not create a persisted record or change revision. Initial defaults have revision=0 and updatedAt=null; the first write creates the account-scoped settings record.
- After a timeout or malformed response, stop further writes and read the resource. Show the actual saved values without falsely attributing another tab's changes to this request. If they differ from the local draft, offer Load latest or a deliberate reapplication using the current revision. Never replay a stale save automatically.
- If reconciliation also fails, show Check saved settings again and keep mutations disabled. A successful later read establishes the current state. Account changes clear drafts, cached private data, and obsolete requests.

E.3 — Service failure

- LEARNING_PREFERENCES_UNAVAILABLE offers retry. A preferences failure does not block an otherwise accessible lesson or change its completion state. The settings page itself remains read-only until its confirmed revision is loaded.

UI Integration:

- `22 Settings Learning Preference`, node `222:110`.
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-110
- Live context/screenshot inspected on 2026-09-20. Preserve Interface Theme, Default Playback Speed, Enable Subtitles by Default, Default Course Language, and Weekly Learning Goal rows and sidebar.
- Explicit Save Changes, goal editor, menu choices, initial defaults, dark appearance, errors, and dirty-state confirmation are project supplements. The source provides no verified dark/mobile frame or frozen dataset.
- Enable the Learning Preferences sidebar entry and profile-menu Settings entry. In this incremental baseline Settings opens this implemented route; Account Settings and Security & Privacy remain disabled until their own UCs. Notification Settings links to UC-12 once installed.

API Endpoint:

`GET /api/v1/student/learning-preferences`

`PUT /api/v1/student/learning-preferences`

Request Body:

```json
{
  "expectedRevision": 0,
  "theme": "AUTO",
  "defaultPlaybackSpeed": 1.5,
  "subtitlesEnabled": true,
  "preferredCourseLanguage": "vi",
  "weeklyGoalMinutes": 300
}
```

PUT requires exactly all shown keys. expectedRevision is a nonnegative JSON safe integer. theme is LIGHT|DARK|AUTO; defaultPlaybackSpeed a JSON number in {0.5,1,1.5,2}; subtitlesEnabled boolean; preferredCourseLanguage en|vi; weeklyGoalMinutes null or an integer multiple of 30 in [30,2400]. Reject coercions and additional keys.

Successful Response:

```json
{
  "success": true,
  "message": "Learning preferences retrieved.",
  "data": {
    "revision": 0,
    "theme": "AUTO",
    "defaultPlaybackSpeed": 1,
    "subtitlesEnabled": false,
    "preferredCourseLanguage": "en",
    "weeklyGoalMinutes": null,
    "updatedAt": null
  }
}
```

```json
{
  "success": true,
  "message": "Learning preferences saved.",
  "data": {
    "revision": 1,
    "theme": "AUTO",
    "defaultPlaybackSpeed": 1.5,
    "subtitlesEnabled": true,
    "preferredCourseLanguage": "vi",
    "weeklyGoalMinutes": 300,
    "updatedAt": "2026-09-20T10:00:00.000Z"
  }
}
```

HTTP 200. data contains exactly these seven fields: revision, theme, defaultPlaybackSpeed, subtitlesEnabled, preferredCourseLanguage, weeklyGoalMinutes, updatedAt (seven keys total). Values obey the request domains. updatedAt is null for virtual defaults, otherwise server ISO UTC. GET returns defaults without a persistence side effect. PUT returns normalized saved preferences, not learning metrics. No account identity, credentials, course access, or projected completion is returned.

Error Response:

```json
{
  "success": false,
  "statusCode": 503,
  "code": "LEARNING_PREFERENCES_UNAVAILABLE",
  "message": "Learning preferences are temporarily unavailable. Please try again later.",
  "timestamp": "2026-09-20T10:00:00.000Z",
  "path": "/api/v1/student/learning-preferences"
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

503 LEARNING_PREFERENCES_UNAVAILABLE: `Learning preferences are temporarily unavailable. Please try again later.`.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement the account-scoped preference record in NestJS/TypeScript, keeping UC-03 learning-profile data separate. Store the exact defaults, revision, and update timestamp. Validate theme/speed/language/goal domains and save one consistent outcome. No background learning measurement, translation, enrollment, or notification job is created.

### Frontend UI Context

Implement the settings page and added goal editor in React/TypeScript/Tailwind. Supply the declared light/dark/auto theme behavior across authenticated pages, accessible controls, explicit Save Changes, and a concise language/measurement limitation. Enable UC-07's Edit Goal link and supported settings navigation.

### Frontend Logic and API Context

Maintain a confirmed per-account preference cache and isolated local form draft. Apply theme only after confirmed save; use player defaults on new UC-08 loads without changing in-progress playback or quiz answers. Resolve captions by returned track language, and render target-only goal state without inventing completion percentages. Refresh settings on account/route changes and retain no prior account values.

### Validation and Error-Handling Context

Validate complete payload and revision on the server. Distinguish virtual defaults from temporary outage fallbacks and saved settings. A missing caption track is not a preferences-save error. Null goal means no target, not zero achieved progress; a configured goal still needs an independent measurement source.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
