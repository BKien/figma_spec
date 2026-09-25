# UC-11: Manage Notification Preferences

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Manage Notification Preferences

Description:

- Allows a signed-in Job Seeker to choose Email and/or Text preferences independently for Recommendations, Contacted Employers, and Introduction Video Requests, then save those choices.
- This UC implements preference persistence only. UC-01–10 define no notification event producer, outbound email/SMS delivery, employer-contact workflow, or video-request workflow. A preference can be saved for a future event category without pretending that an event or message has already been delivered.
- The source supports six checkboxes and contact displays. Default values, read-only contact treatment, revision behavior, route, and API contracts are research decisions, not backend rules inferred from Figma or quotations from a Technical Report.

Primary Actor:

Authenticated ACTIVE JOB_SEEKER.

Preconditions:

- UC-01 supplies the canonical account email/mobile and UC-02 supplies the current browser session.
- Implement `/settings/notifications` as a reloadable route. The authenticated account menu's Settings action opens this route; the notifications tab is active.
- Preference persistence is available independently of any messaging provider. No email or SMS service is required to complete this UC.

Postconditions:

- Success: All six channel choices are saved together, the notification-settings revision advances once, and the page displays the returned canonical choices.
- Failure: The previous choices remain intact. Recoverable form/conflict errors preserve the draft within the same session.
- Reading, selecting, or saving does not send a message, verify a contact, edit account email/mobile, create a recommendation event, contact an employer, or request a video. Profile fields, UC-06 job preferences, and UC-07 ranking remain unchanged.

Main Flow:

1. Select Settings from the account menu and load notification preferences.
2. Display the current account email/mobile as read-only contact information, the six channel checkboxes, and the delivery-availability notice.
3. Toggle Email and Text independently within each category. Neither, either, or both channels may be selected.
4. Select Save Changes and submit all six booleans with the loaded expectedRevision.
5. The backend checks session eligibility, the exact input contract, and the current revision, then commits one complete preferences update.
6. Show `Notification preferences saved.` and replace the form's baseline with the response. Keep the delivery notice visible.

Alternative Flow:

A.1 — First visit or all channels disabled

- A missing settings record returns revision 0, all six booleans false, and updatedAt null. GET does not create a record or preselect a channel.
- Saving all false is valid. It means no selected channels, not an invalid form or a deleted account. A successful explicit save creates/advances the record revision.

A.2 — Contacts and future categories

- Display email and mobileNumber from the canonical Account; no notification-specific copies are editable. Replace source placeholder contact values with the actual account values.
- The source Mobile control appears editable, but this research UC deliberately makes both contacts read-only. Contact changes require a separately specified account-contact workflow; do not silently change UC-01 data here.
- Contacted Employers and Introduction Video Requests are retained as preference category labels. Saving them does not imply those business workflows currently exist.

A.3 — Leave without saving or return after sign-in

- Checkbox changes remain a local draft until Save succeeds. Navigating away before submission discards that draft; no autosave occurs. A supplementary Discard changes action restores the loaded values.
- Add exactly `/settings/notifications` to UC-02's accepted local next destinations, without query/fragment. Encode it as the next parameter for unauthenticated direct entry; preserve the existing default `/jobs` route.

Exception Flow:

E.1 — Invalid payload or unavailable service

- Missing/wrong-type channel values return VALIDATION_ERROR. No unknown event category is silently accepted or ignored.
- A read outage shows Retry, not a fabricated all-false state. A save outage leaves confirmed preferences intact and clearly indicates that the draft has not been confirmed saved.

E.2 — Concurrent changes

- A stale expectedRevision returns NOTIFICATION_PREFERENCES_VERSION_CONFLICT. Keep the draft and offer Reload latest for review. Do not silently merge checkbox values or overwrite another session's changes.
- A basic-profile or job-preferences update does not affect this independent revision.

E.3 — Unknown save outcome or session loss

- After a lost save response, GET settings. If the canonical channel values match the draft, show the current saved settings. If they differ, retain the draft for comparison and require an explicit decision before another save.
- A failed reconciliation remains an unresolved state; do not resubmit automatically. A 401 clears private contacts/preferences/drafts and returns through sign-in. A 403 displays that this feature is unavailable for the current role.

UI Integration:

- File DH Dental Recruitment (Community), Pages / Job Seeker (`1:2`).
- [Settings / Notifications, frame `2:4229`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4229): account contact fields, three category cards with Email/Text checkboxes, settings tabs, and Save Changes.
- [Account menu, frame `2:4121`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4121): Settings entry point.
- Live contexts/screenshots inspected on 2026-09-23. These desktop references do not establish expanded behavior, delivery events, or a frozen dataset.
- Keep the source category layout, teal settings banner, and save action. Normalize the heading to `Notification Settings`.
- Replace the source promises that messages will be received with `These are your account contact details.` Show `Preferences can be saved. Email and text delivery are not enabled in this research prototype.` immediately above the channel choices.
- Read-only contacts, the notice, Discard changes, and loading/error/conflict/responsive states are explicit supplements. On narrow screens stack the category cards and keep every checkbox associated with both its category and channel label.
- Change Password opens UC-12 `/settings/change-password` when integrated. Close Account and Switch Account remain visibly unavailable until their UCs define working behavior; do not use nonexistent destinations. The bell icon is not implemented as an inbox by this UC.

API Endpoint:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/v1/job-seeker/notification-preferences` | Read saved choices and canonical account contacts |
| PUT | `/api/v1/job-seeker/notification-preferences` | Replace all channel choices |

Both require the UC-02 session, reject query parameters, and accept no account ID. GET has no body. PUT accepts application/json.

Request Body:

PUT accepts exactly expectedRevision and channels. Every nested key is required:

```json
{
  "expectedRevision": 0,
  "channels": {
    "recommendations": {
      "email": true,
      "text": false
    },
    "contactedEmployers": {
      "email": false,
      "text": false
    },
    "introductionVideoRequests": {
      "email": true,
      "text": false
    }
  }
}
```

expectedRevision is an integer >= 0. channels has exactly recommendations, contactedEmployers, and introductionVideoRequests. Each has exactly email and text, both JSON booleans. Strings, null, arrays, omitted flags, extra categories, and extra keys are invalid. All 64 combinations of the six booleans are valid; selecting one channel never forces the other.

No email address, phone number, contact-verification flag, delivery status, global notification switch, or event payload is accepted in this request.

Successful Response:

Both endpoints return HTTP 200. PUT example:

```json
{
  "success": true,
  "message": "Notification preferences saved.",
  "data": {
    "asOf": "2026-09-23T16:00:00.000Z",
    "contacts": {
      "email": "alex.morgan@example.com",
      "mobileNumber": "+12025550123"
    },
    "deliveryStatus": "NOT_IMPLEMENTED",
    "notificationPreferences": {
      "revision": 1,
      "channels": {
        "recommendations": {
          "email": true,
          "text": false
        },
        "contactedEmployers": {
          "email": false,
          "text": false
        },
        "introductionVideoRequests": {
          "email": true,
          "text": false
        }
      },
      "updatedAt": "2026-09-23T16:00:00.000Z"
    }
  }
}
```

GET uses message `Notification preferences loaded.` data has exactly asOf, contacts, deliveryStatus, and notificationPreferences. contacts contains exactly email and mobileNumber, read from UC-01's canonical Account using its existing normalization and non-null fields. This endpoint does not change the UC-02 user response schema.

In this release deliveryStatus is always NOT_IMPLEMENTED, describing feature availability rather than delivery success or account eligibility. notificationPreferences has exactly revision, channels, and updatedAt. channels is the exact shape in the request; its values are persisted choices, not inferred from verification flags.

Before any save, revision is 0, every channel flag is false, and updatedAt is null. Each successful PUT increments the independent revision once, including an explicitly submitted unchanged form. updatedAt becomes server UTC ISO 8601. GET is nonmutating. No sent count, queue ID, verification code, or message receipt is returned.

Error Response:

All errors contain success false, statusCode matching the HTTP status, code, message, timestamp (server UTC ISO 8601), and path (actual request pathname without query). Only VALIDATION_ERROR adds errors, mapping field paths to nonempty arrays of messages. A 429 additionally includes the positive integer retryAfterSeconds and an equal Retry-After header. Other errors omit these extensions. No error response contains data: null.

| HTTP | code | message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | Please sign in to continue. |
| 403 | ROLE_NOT_ALLOWED | This action is not available for your account role. |
| 409 | NOTIFICATION_PREFERENCES_VERSION_CONFLICT | Your notification preferences changed in another session. Reload the latest version before saving. |
| 503 | NOTIFICATION_PREFERENCES_UNAVAILABLE | Notification preferences are temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

409 applies only to PUT. A missing record is the initial 200 representation, not 404. Wrong PUT content type uses VALIDATION_ERROR with errors.request. There is no delivery failure error in this preference-only operation and no endpoint-specific 429 budget introduced here.

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-23T16:00:00.000Z",
  "path": "/api/v1/job-seeker/notification-preferences",
  "errors": {
    "channels.recommendations.email": [
      "Choose true or false."
    ]
  }
}
```

```json
{
  "success": false,
  "statusCode": 409,
  "code": "NOTIFICATION_PREFERENCES_VERSION_CONFLICT",
  "message": "Your notification preferences changed in another session. Reload the latest version before saving.",
  "timestamp": "2026-09-23T16:00:00.000Z",
  "path": "/api/v1/job-seeker/notification-preferences"
}
```

## Project-Specific Implementation Context

### Backend Implementation Context

Require UC-02's cookie-based session for an ACTIVE JOB_SEEKER. Missing, expired, or account-ineligible sessions return 401 UNAUTHENTICATED. An otherwise valid unsupported-role session returns 403 ROLE_NOT_ALLOWED. An incomplete profile and unverified contact flags do not block this feature. Resolve the account from its session; no caller-supplied account identifier is accepted.

Implement one NotificationPreferences record per Account in the proposed NestJS/TypeScript backend. Persist its revision, six channel booleans, and updatedAt. Read contacts directly from Account, without storing a divergent email or mobile number in the preference record.

GET of an absent record returns the explicit all-false initial state without writing. PUT validates the complete structure and expectedRevision, then commits all choices together and advances once. Concurrent first saves against revision 0 cannot both succeed. Failure/conflict preserves the previous choices.

This service saves preferences only: it does not call email/SMS providers, enqueue events, send a confirmation message, or change contact verification. The fixed deliveryStatus makes that scope observable. A future delivery UC must define actual event sources, eligible recipients, contact handling, and delivery behavior before these preferences can drive sending.

Do not conflate this record with UC-06 JobPreferences, UC-07 recommendation ranking, or future notification inbox state. Their revisions and behaviors remain independent.

### Frontend UI Context

Use React/TypeScript/Tailwind and reuse the authenticated account menu and profile-style shell. Add the settings tab composition from the source rather than making a new dashboard. Render canonical contact data read-only and never seed checkboxes from an illustration.

Place the delivery-status notice where the actor sees it before saving. A checked Text box means a saved preference; it must not be styled as a verified phone number or successful SMS delivery. Use a success message about saved preferences only.

Keep loading, never-saved, saved, dirty, submitting, conflict, and load-error states distinct. Group checkbox labels by category; keyboard operation and focus should identify both the category and channel.

### Frontend Logic and API Context

Fetch session and preferences before initializing the form. Capture expectedRevision, keep local channel choices separate from the confirmed baseline, and submit the complete exact channels object on Save. Do not send read-only contacts or deliveryStatus back in PUT.

On success, adopt the returned settings/revision and clear dirty state. Discard changes restores the confirmed baseline without a request. While a save/reconciliation is pending, prevent duplicate submission and do not imply that local discard cancels an in-flight server write.

On conflict or unknown outcome, follow the explicit refetch/review flow. Ignore old responses after account changes and clear private contacts/preferences on session loss. The app must not display delivery success merely because the preference request returned 200.

Integrate Settings and the new next destination into the existing menu/sign-in flow. Saving preferences stays on `/settings/notifications`; it does not automatically redirect to jobs or open an email/SMS application.

### Validation and Error-Handling Context

Reject unknown keys at all levels, wrong booleans, missing categories, invalid revision values, and unsupported GET body/query input. Use paths such as channels.recommendations.email, channels.contactedEmployers.text, expectedRevision, and request for validation errors.

All-false preferences, unverified contacts, and an incomplete profile are valid states. Do not impose a fictional email/SMS verification flow or silently deselect choices based on a delivery service that is not implemented.

Keep the last saved state on validation/conflict/persistence failure. A service failure is not an initial empty record. Announce confirmed preference saving only, and retain the explicit delivery-status notice after success.
