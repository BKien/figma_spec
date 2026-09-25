# UC-05: Manage Basic Profile Information

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Manage Basic Profile Information

Description:

- Allows a signed-in Job Seeker to view and update their name, fluent languages, desired position, available start month, and optional profile photo as one profile-editing task.
- Names stay consistent with the account created in UC-01. The desired position becomes the category used by UC-07 recommendations; this UC does not publish a candidate profile or verify professional qualifications.
- The Figma read/edit frames establish the visible fields. Field rules, photo handling, routes, version conflicts, and API contracts below are research implementation decisions. They are not quotations from a supplied Technical Report.

Primary Actor:

Authenticated ACTIVE JOB_SEEKER.

Preconditions:

- UC-01 supplies the account and UC-02 supplies a working browser session. UC-03 supplies the canonical specialism vocabulary.
- `/profile/basic` and `/profile/basic/edit` are implemented, reloadable routes. The authenticated account menu has a working Profile link to `/profile/basic`.
- File storage can preserve an optional JPEG/PNG profile photo and retrieve it for its owner. A newly registered account is supported without seeded profile content.

Postconditions:

- Success: All submitted basic fields and the selected photo action are saved together, the profile revision increases once, and the read page shows the returned values. Updated names also appear in the UC-02 session user summary.
- Failure: No partial name, profile, or photo change becomes visible. Recoverable form errors retain the actor's draft; an uncertain network outcome is reconciled before another write.
- Neither reading nor saving creates an application, changes contact verification, updates job preferences, or makes this profile public. Global profileCompletionStatus remains unchanged; this UC supplies no overall completion percentage.

Main Flow:

1. Open Profile and load the current basic profile.
2. Show the stored name, read-only email, languages, desired position, start availability, and photo or neutral avatar.
3. Select Edit Profile. Initialize the edit form from the loaded values and retain its revision.
4. Edit the basic fields; optionally choose a replacement photo and preview it locally.
5. Choose Immediately or select an available start month and year, then select Save Changes.
6. Validate the complete form and submit one multipart request containing metadata and, only for a replacement, the selected photo file.
7. The server checks eligibility, validates the request and expected revision, and saves the account-name and profile changes as one visible update.
8. Show `Basic information saved.`, refresh the local account summary, and return to `/profile/basic` using the canonical response.

Alternative Flow:

A.1 — First profile visit

- If no extended profile exists, GET returns revision 0, the existing account names/email, fluentLanguages [], desiredPosition null, availableStart {mode: "NOT_SPECIFIED", month: null}, photo null, and updatedAt null. These are response defaults, not a precompleted profile.
- Display missing values as `Not provided`. The first successful save requires the editable basic fields below; no work-experience or education entry is required here.

A.2 — Cancel or replace/remove a photo

- Cancel discards the draft and local preview and returns to the read route without an API write. Selecting a file does not upload or save it immediately.
- KEEP preserves the currently saved photo, REPLACE saves the attached file, and REMOVE clears an existing photo. Remove photo is a small explicitly added control next to Upload Photo; it is not shown in the source frame.
- If there is no photo, KEEP or REMOVE results in photo null. Replacing/removing the photo does not alter other profile sections.

A.3 — Availability already started

- Immediately stores mode IMMEDIATELY with month null. A specific month stores mode MONTH with YYYY-MM; the source has no day-level precision.
- A stored or newly chosen past month is allowed and displayed as `Available from <Month Year>`. It means availability has already begun, not an expired account or a failed profile.

A.4 — Return after sign-in

- For unauthenticated entry, open UC-02 `/sign-in?next=/profile/basic` or `/sign-in?next=/profile/basic/edit`. This UC explicitly extends UC-02's permitted local next destinations with these two exact paths; no additional query/fragment or external destination is accepted.
- Keep UC-02's default `/jobs` destination and session durations. On a lost session, clear profile data and require sign-in again; do not preserve personal form drafts across account changes.

Exception Flow:

E.1 — Invalid field or image

- Identify invalid fields inline without clearing valid edits. Oversized uploads and unsupported file formats use the contracts below. A selected file must be a decodable JPEG or PNG; a renamed non-image is not accepted as a profile photo.
- If upload/storage fails, no part of the profile or account-name change is committed. Keep the edit view and let the actor explicitly retry.

E.2 — Another save occurred

- A mismatched expectedRevision returns PROFILE_VERSION_CONFLICT. Keep the local draft and show `Your profile changed in another session. Reload the latest version before saving.`
- Reload latest retrieves the current profile. It does not silently merge or overwrite concurrent changes. After reviewing the refreshed values, the actor can reapply edits with the new revision.

E.3 — Response lost or session ended

- If a save response is lost, mark its outcome unknown and GET the profile. If its canonical fields/photo now reflect the draft, show the current saved state. If they differ, present the current state and retain the local draft for review; do not automatically resubmit with a new revision.
- For a replaced photo whose response is unknown, display the freshly fetched current photo for the actor to confirm; a revision increment alone does not prove that this request saved it.
- Authentication loss clears private profile/preview data. A read failure displays a retry state, not an invented blank profile.

UI Integration:

- File DH Dental Recruitment (Community), page Pages / Job Seeker (`1:2`).
- [Profile / Basic Information, frame `2:4549`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4549): name/email summary, photo, Edit Profile, and stored-field rows.
- [Profile / Edit Basic Information, frame `2:4631`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4631): Upload Photo, first/last names, Fluent Languages, Desired Position, Immediately, month controls, Cancel, and Save Changes.
- Contexts and screenshots inspected on 2026-09-23. This identifies inspected desktop references; it does not claim a frozen dataset or verified prototype behavior.
- Correct the two repeated `Select Month` labels to `Month` and `Year`. Use a multi-select for Fluent Languages; this behavior and the configured language choices are project supplements because the source only shows its collapsed control.
- Email is visible and read-only on the summary; editing email/mobile/password belongs to other UCs. Keep the active profile tab aligned with the current route instead of copying the source's unrelated Introduction Video underline.
- Job Preferences links to UC-06 once integrated. Work Experience, Education, Introduction Video, notifications, and newsletter remain visibly unavailable until their UCs exist; do not route to missing pages or simulate successful actions.
- Loading, validation, conflict, file-error, removal, and narrow-screen states are project supplements. Stack fields vertically when necessary, preserve labels and keyboard operation, and focus the first invalid field after submission.

API Endpoint:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/v1/job-seeker/profile/basic` | Load the current basic profile |
| PUT | `/api/v1/job-seeker/profile/basic` | Save the complete editable basic profile and optional photo action |
| GET | `/api/v1/job-seeker/profile/photo` | Retrieve the current owner's photo bytes |

All endpoints require the UC-02 browser session. All reject query parameters. GET has no body. PUT uses `multipart/form-data`; it is not a JSON-only endpoint.

Request Body:

PUT contains exactly one text part `metadata`, whose content is the following JSON object, and one optional binary part `photo`:

```json
{
  "expectedRevision": 0,
  "firstName": "Alex",
  "lastName": "Morgan",
  "fluentLanguages": [
    "en"
  ],
  "desiredPosition": "GENERAL_DENTIST",
  "availableStart": {
    "mode": "IMMEDIATELY",
    "month": null
  },
  "photoAction": "KEEP"
}
```

| Field | Exact rule |
| --- | --- |
| expectedRevision | Required integer >= 0, equal to the currently loaded basic-profile revision |
| firstName, lastName | Required strings; trim surrounding whitespace, then 1–100 Unicode code points; no control characters; same rules as UC-01 |
| fluentLanguages | Required array of 1–3 distinct strings from en, es, vi; canonical response order en, es, vi |
| desiredPosition | Required non-null UC-03 specialism enum |
| availableStart | Required object with exactly mode and month |
| availableStart.mode | IMMEDIATELY or MONTH for writes; NOT_SPECIFIED is a read-only initial state |
| availableStart.month | null for IMMEDIATELY; valid YYYY-MM from 2000-01 through 2100-12 for MONTH |
| photoAction | Required KEEP, REPLACE, or REMOVE |
| photo | Exactly one JPEG/PNG binary file for REPLACE, absent for KEEP/REMOVE; > 0 and <= 5,242,880 bytes |

Language labels are English (en), Spanish (es), and Vietnamese (vi), a declared finite research vocabulary rather than an exhaustive language catalog. The exact desiredPosition values are GENERAL_DENTIST, DENTIST_SPECIALIST, DENTAL_HYGIENIST, DENTAL_ASSISTANT, OFFICE_STAFF, OFFICE_MANAGER; labels are those of UC-03.

The metadata part may occupy at most 16,384 UTF-8 bytes. The total multipart body may occupy at most 6,291,456 bytes, including multipart framing; exceeding either byte limit returns 413 UPLOAD_TOO_LARGE. Empty/undecodable image, inconsistent photoAction, extra parts, malformed metadata JSON, and unknown object keys return 400 VALIDATION_ERROR. Unsupported request media type or photo format returns 415 UNSUPPORTED_MEDIA_TYPE. `email`, `mobileNumber`, role, verification flags, completion status, account IDs, and photo URL are not writable fields.

Successful Response:

GET and PUT return HTTP 200 with the same data structure. PUT:

```json
{
  "success": true,
  "message": "Basic information saved.",
  "data": {
    "asOf": "2026-09-23T14:00:00.000Z",
    "profile": {
      "revision": 1,
      "firstName": "Alex",
      "lastName": "Morgan",
      "email": "alex.morgan@example.com",
      "fluentLanguages": [
        "en"
      ],
      "desiredPosition": "GENERAL_DENTIST",
      "availableStart": {
        "mode": "IMMEDIATELY",
        "month": null
      },
      "photo": null,
      "updatedAt": "2026-09-23T14:00:00.000Z"
    }
  }
}
```

GET uses message `Basic information loaded.` The data object contains exactly asOf and profile. The profile object contains exactly the keys shown; firstName, lastName, and email are the canonical account values. revision is a nonnegative integer; updatedAt is null only for the initial revision-0 representation, otherwise a UTC ISO 8601 timestamp.

A saved photo replaces photo null with exactly:

```json
{
  "url": "/api/v1/job-seeker/profile/photo",
  "contentType": "image/jpeg",
  "byteSize": 184320
}
```

contentType is image/jpeg or image/png; byteSize is the actual saved file size. The URL requires the current owner's session and is never a public candidate-profile URL. GET photo returns HTTP 200 with image bytes and the matching Content-Type, not a success JSON envelope. A missing photo returns PROFILE_PHOTO_NOT_FOUND. It has no range, query, or alternate-account interface.

After a successful PUT, the next UC-02 GET session returns the updated firstName/lastName in its existing user schema; no new session-user fields are added by this UC.

Error Response:

All JSON errors use exactly `success: false`, `statusCode`, `code`, `message`, `timestamp` (UTC ISO 8601), and `path` (actual request pathname without query). Only VALIDATION_ERROR adds `errors`, an object mapping field paths to nonempty arrays of messages. Do not add `data: null`. Binary success responses are explicitly identified below; their errors still use this JSON envelope. Unknown failures use INTERNAL_ERROR rather than exposing internal details.

| HTTP | code | message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | Please sign in to continue. |
| 403 | ROLE_NOT_ALLOWED | This action is not available for your account role. |
| 404 | PROFILE_PHOTO_NOT_FOUND | No profile photo is available. |
| 409 | PROFILE_VERSION_CONFLICT | Your profile changed in another session. Reload the latest version before saving. |
| 413 | UPLOAD_TOO_LARGE | The profile upload exceeds the allowed size. |
| 415 | UNSUPPORTED_MEDIA_TYPE | Use multipart form data with a JPEG or PNG photo. |
| 503 | PROFILE_UNAVAILABLE | Your profile is temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

404 applies only to GET photo. 409/413/415 apply only to PUT; 400 applies to invalid endpoint input. 503 includes profile persistence or configured photo-storage outages, distinct from a genuinely missing photo.

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-23T14:00:00.000Z",
  "path": "/api/v1/job-seeker/profile/basic",
  "errors": {
    "availableStart.month": [
      "Choose a valid month and year."
    ],
    "fluentLanguages": [
      "Select at least one fluent language."
    ]
  }
}
```

```json
{
  "success": false,
  "statusCode": 409,
  "code": "PROFILE_VERSION_CONFLICT",
  "message": "Your profile changed in another session. Reload the latest version before saving.",
  "timestamp": "2026-09-23T14:00:00.000Z",
  "path": "/api/v1/job-seeker/profile/basic"
}
```

## Project-Specific Implementation Context

### Backend Implementation Context

Require the UC-02 browser session and an ACTIVE JOB_SEEKER account. Unverified email/mobile and an incomplete profile are allowed. Missing, expired, or account-ineligible sessions return 401 UNAUTHENTICATED; an otherwise valid unsupported-role session returns 403 ROLE_NOT_ALLOWED. Resolve the account from the session; no caller-supplied account identifier is accepted. These are feature eligibility rules, not additional verification steps.

Use the proposed NestJS/TypeScript backend and reuse the UC-01 Account. Store one optional BasicProfile per account containing revision, fluentLanguages, desiredPosition, availableStart, photo metadata/reference, and updatedAt. The authenticated profile response composes firstName/lastName/email from Account; do not create divergent copies of account names.

GET without a BasicProfile returns the initial representation without creating a row. The first successful save creates revision 1. Each subsequent successful PUT with the expected revision advances by one, including a submitted unchanged form; GET never increments. Concurrent first saves must not both succeed against revision 0. Name, basic-profile, and photo-pointer changes are committed together; failed/conflicting saves preserve the prior visible photo and clean up any unreferenced upload from that attempt.

Photo replacement must finish storing a usable file before reporting success. Retire an old photo only after the new visible profile state is committed; storage failures must not destroy the last saved photo. Retrieval serves the currently committed photo to its owner. This UC does not provide a public profile or photo gallery.

Saving basic information leaves UC-06 preferences, work/education sections, account eligibility, contact-verification flags, and global profileCompletionStatus unchanged. Do not implement a fabricated 90% completion formula. The desired position is independently usable by UC-07 even while global completion is INCOMPLETE.

These are proposed project contracts. No Clicon/EdTech registration schema, response fields, or extra authentication prerequisites carry into Dental.

### Frontend UI Context

Use React, TypeScript, and Tailwind CSS consistently with UC-01–04. Reuse the authenticated shell and Figma profile read/edit card rather than generating an unrelated dashboard. Retain the teal profile banner, desktop card composition, visible labels, and source icons/assets where applicable.

Show account-specific names/email, never sample User Name or a stock person's avatar as the user's actual identity. For photo null use a neutral avatar or initials. Display the returned image after save; a local preview is marked unsaved until the API confirms the update. Revise labels for month/year as stated above, and display language labels rather than enum codes.

Keep loading and error states distinct from the revision-0 profile. Save is unavailable while sending or reconciling an uncertain result. Cancel before submission is nonmutating; once a submission has started, keep the form present until its outcome is resolved instead of implying Cancel can undo an in-flight server update.

### Frontend Logic and API Context

Load UC-02 session and GET basic before editing. Use the loaded revision as expectedRevision and send a complete normalized editable payload. The browser constructs multipart boundaries; metadata remains JSON text, not multiple loosely coerced form fields. Never send the read-only email or completion status back as writable fields.

Keep file preview and form draft local to this editor. Toggling Immediately clears the submitted month; MONTH requires an explicit month/year. Canonicalize fluentLanguages to the fixed order before comparison and submission. Cancel removes preview state without uploading.

Use the successful PUT response as the read-page profile and refresh UC-02 session data so account menus reflect renamed users. Fetch the authenticated photo again after a successful change; the stable URL alone is not a reason to reuse an old image. Invalidate cached recommendation results when desiredPosition changes; UC-07 will refetch using the new basicProfileRevision.

Scope requests and state to the current account. Ignore superseded load responses and clear profile/photo state when that account changes. On revision conflict or an uncertain result, refetch and let the actor review before another explicit save; no silent overwrite or automatic mutation loop.

### Validation and Error-Handling Context

Reject unknown fields, wrong JSON types, unexpected request/query parameters, and duplicate multipart parts where applicable. Never coerce a string such as "false" to a boolean. Return all safely identifiable field validation errors together. Failed validation or a revision conflict leaves the previously saved state unchanged.

Apply the same name normalization as UC-01; do not impose Latin-only names. Enforce exact language/specialism enums and the mode/month relationship. No day, time zone conversion, age, licensing, or contact-verification requirement is inferred from this form.

Basic-profile error paths use editable field names such as firstName, fluentLanguages, availableStart.month, photo, metadata, and expectedRevision. Multipart-level problems may use request. Distinguish unsupported format (415), oversized input (413), undecodable supported image (400), stale revision (409), absent photo (404), and temporary storage failure (503).

Read or photo failures must not clear a saved profile in the backend. Preserve an editable draft for recoverable errors in the same session, while removing it on session/account change. Announce save success only for a confirmed response or the reconciled saved state described above.
