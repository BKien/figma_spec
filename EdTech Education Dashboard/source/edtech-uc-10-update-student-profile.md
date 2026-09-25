# UC-10: View and Update Student Contact Profile

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

View and Update Student Contact Profile

Description:

- Lets the Student view account identity and completed-course links, and update phone number, preferred contact method, and biography.
- Enables the Profile menu destination. Contact profile data is separate from UC-03's learning goals, interests, occupation, and education answers.
- Editable field boundaries, validation, persistence, and unavailable controls are explicit project decisions. The Profile frame supplies the form composition; no Technical Report has been supplied.

Primary Actor:

Authenticated Student with completed onboarding.

Preconditions:

- UC-01 account identity and UC-02 session are available. Implement `/student/profile` with direct navigation/reload support.
- Full name and verified sign-in email come from the current account. This UC does not introduce a new email-verification or password-change flow.
- UC-06 supplies the account's completed-course list; profile editing must remain usable if that independent read fails.

Postconditions:

- Success: Submitted contact fields are stored for this Student and returned with a new revision. Reloading shows the saved values.
- Failure: No rejected update changes contact data or authentication identity. A previously saved profile remains intact.
- Updating the profile does not change login email, verification, application role, onboarding status, enrollment, learning progress, or delivery subscriptions.

Main Flow:

1. The Student selects Profile in the existing account menu and opens `/student/profile`.
2. Load the contact profile and independently load completed courses using UC-06 with status=COMPLETED, page=1.
3. Show full name and verified email in the identity area. The Email form field is read-only and labelled Sign-in email. Phone, Preferred Contact Method, and Bio are editable.
4. The Student changes one or more editable values and selects Save Changes.
5. Validate the complete form and send the declared PUT with expectedRevision; disable repeated submission while pending.
6. The backend saves all editable fields together and returns their normalized values. The frontend replaces its confirmed state and shows `Profile changes saved.`
7. A later reload retrieves the same saved profile; completed-course cards link to `/student/my-courses?courseId=<id>`.

Alternative Flow:

A.1 — Empty optional fields

- Phone and biography are optional. Clearing either sends null; the frontend normalizes a whitespace-only input to null. Preferred contact defaults to EMAIL.
- PHONE requires a nonnull phone. Clearing a phone while PHONE is selected shows a validation message and requires selecting EMAIL or providing a phone.
- Preferred contact is descriptive preference data. Selecting PHONE does not verify the number or trigger a call/SMS; EMAIL does not subscribe the Student to notifications.

A.2 — Identity and source controls

- Name is displayed from UC-01 and has no editing control in this baseline. Email is read-only; explanatory text says that changing sign-in email requires a separate verification flow. Do not silently reinterpret this field as a second editable contact address.
- Use the existing neutral avatar or initials. The source avatar-edit icon remains disabled with `Photo upload is not available yet.` No upload route is invented.
- Profile Visibility remains visible but disabled with `Public profiles are not available yet.` This UC exposes no public profile, directory, or sharing toggle that appears effective without a defined audience.
- Logout is disabled until its own UC is installed. These boundaries concern this incremental baseline, not a prohibition on later features.

A.3 — Completed courses and navigation

- Show UC-06's first page of completed courses; See all opens `/student/my-courses?status=COMPLETED`. Use its current titles/completedAt values, not the source's Google certificate example.
- A profile course card means course completion, not certificate issuance. Certificate actions stay disabled under the existing baseline. Empty results say No completed courses yet; a failure shows a section-level retry.
- Leaving a dirty form offers Stay or Discard changes. There is no automatic save on navigation. A failed save preserves correctable fields.

Exception Flow:

E.1 — Validation

- Map field errors to phone, preferredContactMethod, or bio. A phone is an unverified contact number, not a replacement authentication factor.
- Reject client changes to fullName, email, role, verified flags, onboarding data, or course state through this endpoint.

E.2 — Concurrent changes and uncertain saves

- A save uses the latest expectedRevision. A stale revision returns SETTINGS_CONFLICT without changing any field, even if some requested values match. Show Load latest, preserve the local draft for review until the user accepts replacement, and never silently overwrite a newer device's values.
- Every accepted PUT increments revision once, including an unchanged deliberate save. GET does not create a persisted record or change revision. Initial defaults have revision=0 and updatedAt=null; the first write creates the account-scoped settings record.
- After a timeout or malformed response, stop further writes and read the resource. Show the actual saved values without falsely attributing another tab's changes to this request. If they differ from the local draft, offer Load latest or a deliberate reapplication using the current revision. Never replay a stale save automatically.
- If reconciliation also fails, show Check saved settings again and keep mutations disabled. A successful later read establishes the current state. Account changes clear drafts, cached private data, and obsolete requests.

E.3 — Service or session failure

- PROFILE_UNAVAILABLE offers manual retry without substituting source identities. A completed-course read failure does not erase the contact form. Shared session/onboarding behavior applies.

UI Integration:

- `19 Profile`, node `222:436`.
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-436
- Live context/screenshot inspected on 2026-09-20. Preserve identity sidebar, Contact Information, phone/email layout, preferred-contact selector, Bio, Save Changes, and completed-course region.
- Read-only identity, EMAIL/PHONE options, deferred avatar/visibility controls, feedback, and dirty-form notice are project supplements. No mobile or frozen dataset claim. Render stored profile text as text rather than markup.

API Endpoint:

`GET /api/v1/student/profile`

`PUT /api/v1/student/profile`

Completed-course section reuses UC-06; no additional course API.

Request Body:

```json
{
  "expectedRevision": 0,
  "phone": "+84901234567",
  "preferredContactMethod": "PHONE",
  "bio": "I am learning Python and web development."
}
```

PUT requires exactly these four keys. expectedRevision is a nonnegative JSON safe integer. phone is null or an international number matching `+` followed by 8–15 digits, with the first digit nonzero; trim outer whitespace but do not guess a country code or remove arbitrary punctuation. preferredContactMethod is EMAIL or PHONE. bio is null or trimmed text of 1–1000 Unicode code points. Empty trimmed optional strings normalize to null. EMAIL refers to the account's verified sign-in email. All frontend/server normalization rules agree.

Successful Response:

```json
{
  "success": true,
  "message": "Student profile retrieved.",
  "data": {
    "revision": 0,
    "fullName": "Alex Nguyen",
    "email": "alex@example.com",
    "phone": null,
    "preferredContactMethod": "EMAIL",
    "bio": null,
    "updatedAt": null
  }
}
```

```json
{
  "success": true,
  "message": "Profile changes saved.",
  "data": {
    "revision": 1,
    "fullName": "Alex Nguyen",
    "email": "alex@example.com",
    "phone": "+84901234567",
    "preferredContactMethod": "PHONE",
    "bio": "I am learning Python and web development.",
    "updatedAt": "2026-09-20T10:00:00.000Z"
  }
}
```

Both responses are HTTP 200. data has exactly revision, fullName, email, phone, preferredContactMethod, bio, updatedAt. Name/email are current persisted UC-01 identity values, not editable snapshots. updatedAt is null before the first profile write, then server ISO UTC. Each accepted write increments revision; no account credentials are returned. Phone/bio null display as empty inputs. A completed-course response retains UC-06's separate schema.

Error Response:

```json
{
  "success": false,
  "statusCode": 503,
  "code": "PROFILE_UNAVAILABLE",
  "message": "Your profile is temporarily unavailable. Please try again later.",
  "timestamp": "2026-09-20T10:00:00.000Z",
  "path": "/api/v1/student/profile"
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

503 PROFILE_UNAVAILABLE: `Your profile is temporarily unavailable. Please try again later.`.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement account-scoped profile reads/writes in NestJS/TypeScript without changing UC-01 identity or UC-03 onboarding. Store the three editable fields, revision, and update timestamp; commit them as one outcome. Read current name/email from the account. No public-profile endpoint, upload adapter, verification message, or notification delivery is introduced.

### Frontend UI Context

Build StudentProfilePage in React/TypeScript/Tailwind from the inspected frame. Enable the Profile menu link. Clearly distinguish editable contact fields from sign-in identity and deferred controls. Keep profile feedback independent of the completed-course section.

### Frontend Logic and API Context

Track last confirmed values, local draft, revision, dirty state, and pending/reconciliation state. Send the complete editable form once per deliberate Save. Replace it only after confirmation or an explicit load-latest choice. Do not refresh the UC-02 session as if phone/bio edits changed authentication. Fetch completed courses independently.

### Validation and Error-Handling Context

Validate optional-field normalization, international phone syntax, contact-method dependency, bio length, account scope, and revision. Reject protected identity fields rather than ignoring them. Preserve drafts on definite errors, reconcile uncertain writes, and do not claim a verified phone, issued certificate, or public profile.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
