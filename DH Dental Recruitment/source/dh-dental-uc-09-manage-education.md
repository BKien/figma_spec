# UC-09: Manage Education

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Manage Education

Description:

- Allows a Job Seeker to view, add, revise, and remove completed education/program entries in one profile section, then save the complete list.
- Figma shows repeatable Dental Program/Degree and In Year controls. This UC treats the year as the completion year and does not collect institution, transcript, license, accreditation, or planned graduation data.
- Program choices beyond visible samples, duplicate rules, year limits, ordering, routes, and contracts are explicit research decisions. Education entries are self-declared and are not a credential-verification result.

Primary Actor:

Authenticated ACTIVE JOB_SEEKER.

Preconditions:

- UC-01/02 supply the shared account/session and UC-05 supplies the profile shell. No completed basic-profile, experience section, or verified contact is required.
- `/profile/education` and `/profile/education/edit` exist as reloadable routes. Activate the Education tab in the shared profile shell.
- Use the finite program options defined below consistently in the backend and frontend. The actor can use Other program or qualification when the two visible source examples do not represent their background.

Postconditions:

- Success: The complete submitted education list replaces the saved list as one update, the education revision advances once, and the read view renders its canonical order.
- Failure: The previous list remains intact; recoverable errors preserve the draft and identify the affected entry.
- Adding/removing a row before Save and Cancel are nonmutating. An empty saved list is allowed. Saving does not verify credentials, publish the profile, create an application, alter UC-07 ranking, or change global profileCompletionStatus.

Main Flow:

1. Open Profile → Education and load the current list.
2. Select Edit to open a draft of that list with its revision.
3. Select Add More to insert a blank row. Choose Dental Program/Degree and completion year; for Other, supply its name.
4. Revise existing rows or remove unwanted rows with the row's delete control.
5. Select Save Changes. Validate the entire draft, including duplicates and row limits, then submit the complete list with expectedRevision.
6. The backend validates eligibility, the list, and the current education revision, then replaces all entries together.
7. Show `Education saved.` and return to `/profile/education` with the canonical response.

Alternative Flow:

A.1 — No education entries

- An absent section returns revision 0, entries [], and updatedAt null without creating a record. Show `No education added yet.` with Edit/Add education.
- In an empty editor, offer Add More; do not silently insert the source's sample qualifications. Saving [] is permitted and creates or advances the section revision.
- Removing the last draft row results in [] only when Save succeeds. The actor may cancel instead; no arbitrary qualification is required to keep an account active.

A.2 — Other qualification

- Selecting OTHER reveals Other program or qualification, a required free-text name for that row. It supports applicants whose qualification is not one of the source's two examples.
- Selecting a named program clears the submitted otherProgramName to null. Program names do not embed a graduation year; completionYear supplies the one authoritative year.

A.3 — Repeated or similar qualifications

- Two identical program/year entries are not permitted. The same named program in different years is allowed because this form has no institution or certificate identifier with which to determine equivalence.
- Two OTHER entries are duplicates only when completionYear and normalized case-insensitive names match. Different names in the same year are allowed.
- No institution or verified degree is inferred from the selected program label.

A.4 — Cancel or return after sign-in

- Cancel before submission discards all draft rows and returns to the read page. Row deletion is local until Save; it does not call a delete endpoint.
- This UC adds exactly `/profile/education` and `/profile/education/edit` to UC-02's permitted local next destinations, with no query/fragment. Encode the complete local destination as the next parameter. Keep the existing `/jobs` default.

Exception Flow:

E.1 — Invalid or incomplete row

- A blank added row must be completed or removed; it is not silently dropped on Save. Mark missing program/year, invalid Other name, duplicate row, or exceeded entry limit without clearing the draft.
- If the actor supplies a future year, explain that this section records completed education. No in-progress status or expected-completion field is introduced implicitly.

E.2 — Another education save occurred

- A stale expectedRevision returns EDUCATION_VERSION_CONFLICT. Keep the draft and offer Reload latest for review; do not merge arrays or overwrite someone else's newer edit automatically.
- A revision change in basic profile, work experience, preferences, or video alone does not cause this section conflict.

E.3 — Uncertain write or load failure

- If the save response is lost, GET the current list. Compare normalized entries in canonical order, not draft row order. If equal, display the current saved list; otherwise let the actor review it alongside their draft before another explicit save.
- A failed read is a retryable error, not an empty education list. A lost/ineligible session clears account-specific drafts and routes through UC-02.

UI Integration:

- File DH Dental Recruitment (Community), page Pages / Job Seeker (`1:2`).
- [Profile / Education, frame `2:5235`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-5235): Education card, program rows, completion-year badges, and Edit.
- [Profile / Edit Education, frame `2:5306`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-5306): repeatable program/year rows, row-delete icons, Add More, Cancel, and Save Changes.
- Both contexts/screenshots inspected on 2026-09-23. The edit frame's card is incorrectly titled `Edit Work Experience`; implement `Edit Education` and keep Education active.
- The read frame contains `Predoctoral (DDS/DMD) in 2021` beside `In Year 2009`. Normalize it to program label `Predoctoral (DDS/DMD)` plus the stored completionYear. Do not store contradictory years in program labels.
- Preserve the repeated-row form and the year badge. Show `Completion year` as the clearer input label for source `In Year`. OTHER, its conditional text input, empty/error/conflict states, and narrow-screen behavior are project supplements.
- These inspections do not establish expanded dropdown contents or a frozen dataset. The source's duplicate sample editor rows are not a rule permitting duplicate records.
- Each delete icon is a named `Remove education entry <n>` button. After removing a row, move focus to the next row, previous row, or Add More as appropriate. Keep Add More available until the declared limit and stack the two selectors on narrow screens.

API Endpoint:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/v1/job-seeker/profile/education` | Read the current education section |
| PUT | `/api/v1/job-seeker/profile/education` | Replace the entire education list |

Both require the UC-02 session and reject query parameters. GET has no body. PUT accepts application/json. Add/edit/remove row operations are represented by one complete PUT; no row-level API or caller-supplied account ID is needed.

Request Body:

PUT body; both top-level fields and every entry field are required:

```json
{
  "expectedRevision": 0,
  "entries": [
    {
      "programCode": "AEGD_12_MONTHS",
      "otherProgramName": null,
      "completionYear": 2011
    },
    {
      "programCode": "DDS_DMD",
      "otherProgramName": null,
      "completionYear": 2009
    }
  ]
}
```

| Field | Exact rule |
| --- | --- |
| expectedRevision | Integer >= 0, matching the last loaded education revision |
| entries | Array of 0–20 entry objects |
| entries[i].programCode | AEGD_12_MONTHS, DDS_DMD, or OTHER |
| entries[i].otherProgramName | Required string for OTHER; null for the two named codes |
| entries[i].completionYear | JSON integer from 1900 through the server's current UTC calendar year, inclusive |

Program labels: AEGD_12_MONTHS = Advanced Education in General Dentistry (12 months); DDS_DMD = Predoctoral (DDS/DMD); OTHER = Other program or qualification. The first two are normalized source examples, not an exhaustive catalog of legitimate qualifications.

For OTHER, reject control characters; trim surrounding whitespace and collapse runs of ordinary spaces to one, then require 1–160 Unicode code points. Preserve display capitalization and accents. Duplicate comparison lowercases the normalized name; it does not remove accents or guess abbreviations. Named-program duplicates have the same programCode and completionYear; OTHER duplicates additionally have the same case-insensitive normalized name.

No row IDs appear in the contract: entries are owned values within this complete section replacement, not independently addressable records. Local draft keys are frontend-only. Reject extra fields such as institution, certificateUrl, verified, startYear, expectedGraduationYear, or profileCompletionStatus rather than pretending to persist unsupported information.

Successful Response:

HTTP 200 for GET and PUT, with exactly data.asOf and data.education. PUT example:

```json
{
  "success": true,
  "message": "Education saved.",
  "data": {
    "asOf": "2026-09-23T15:00:00.000Z",
    "education": {
      "revision": 1,
      "entries": [
        {
          "programCode": "AEGD_12_MONTHS",
          "otherProgramName": null,
          "completionYear": 2011
        },
        {
          "programCode": "DDS_DMD",
          "otherProgramName": null,
          "completionYear": 2009
        }
      ],
      "updatedAt": "2026-09-23T15:00:00.000Z"
    }
  }
}
```

GET uses message `Education loaded.` education contains exactly revision, entries, and updatedAt. Each returned entry contains exactly programCode, otherProgramName, and completionYear, using the same normalized values as the request contract. There is no credential-verification flag.

Canonical order: completionYear descending, then programCode lexicographically ascending, then normalized lowercase otherProgramName lexicographically ascending (null sorts as empty string). Duplicate validation ensures no otherwise identical entries remain. The server returns this order regardless of draft order; manual ordering is not supported.

An initial read is:

```json
{
  "success": true,
  "message": "Education loaded.",
  "data": {
    "asOf": "2026-09-23T15:00:00.000Z",
    "education": {
      "revision": 0,
      "entries": [],
      "updatedAt": null
    }
  }
}
```

Every successful PUT increments revision once (initial save becomes 1), including an explicit unchanged or empty list. updatedAt is server UTC ISO 8601. Deleting all entries preserves the section's new revision and updatedAt; it does not revert to the never-saved revision-0 representation.

Error Response:

All JSON errors contain exactly success false, statusCode, code, message, timestamp (UTC ISO 8601), and path (actual pathname without query). VALIDATION_ERROR additionally contains errors, an object mapping field paths to nonempty arrays of messages. Other codes omit errors. Do not add data: null. Binary download/playback successes are explicitly identified; their errors still use this JSON envelope.

| HTTP | code | message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | Please sign in to continue. |
| 403 | ROLE_NOT_ALLOWED | This action is not available for your account role. |
| 409 | EDUCATION_VERSION_CONFLICT | Your education changed in another session. Reload the latest version before saving. |
| 503 | EDUCATION_UNAVAILABLE | Education is temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

409 applies to PUT. An absent section is a successful initial representation, not 404. Wrong request content type uses 400 VALIDATION_ERROR with errors.request. Error indices refer to the original submitted array before sorting, so the client can identify the draft row.

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-23T15:00:00.000Z",
  "path": "/api/v1/job-seeker/profile/education",
  "errors": {
    "entries.1.completionYear": [
      "Choose a completed year from 1900 through 2026."
    ],
    "entries.2.programCode": [
      "This education entry duplicates another submitted entry."
    ]
  }
}
```

```json
{
  "success": false,
  "statusCode": 409,
  "code": "EDUCATION_VERSION_CONFLICT",
  "message": "Your education changed in another session. Reload the latest version before saving.",
  "timestamp": "2026-09-23T15:00:00.000Z",
  "path": "/api/v1/job-seeker/profile/education"
}
```

The example year 2026 reflects its timestamp. Runtime error text uses the current UTC year. For duplicates, identify each occurrence after the first using errors.entries.<index>.programCode (or otherProgramName when OTHER names duplicate); do not silently discard entries.

## Project-Specific Implementation Context

### Backend Implementation Context

Use the UC-02 cookie-based browser session. All feature endpoints require the account resolved from that session to be an ACTIVE JOB_SEEKER. Unverified email/mobile, an incomplete basic profile, and global profileCompletionStatus INCOMPLETE do not block this feature. A missing, expired, or account-ineligible session returns 401 UNAUTHENTICATED; an otherwise valid unsupported-role session returns 403 ROLE_NOT_ALLOWED. No endpoint accepts a caller-supplied account ID.

Implement an Education section per Account using the proposed NestJS/TypeScript stack. It contains an independent revision, an owned collection of program/year values, and updatedAt. Use the exact finite program vocabulary and optional OTHER name, not values copied from unrelated project UCs.

GET of an absent section returns revision 0 without creating a record. A valid PUT with the expected revision replaces all entries together and advances the section revision once. Concurrent first writes against revision 0 cannot both succeed. Validation or persistence failure cannot delete old rows while retaining only part of the replacement.

Normalize and validate entries before canonical sorting; preserve original request indices for validation errors. Capture the server UTC year once per request for year validation. An entry saved in a past year remains valid as time advances; no annual migration is needed.

An empty saved collection is legitimate and distinct from never saved through its revision/timestamp. Education changes do not alter work-experience revision, UC-05 basic values, UC-06 preferences, contact verification, or account status. Do not infer a licensing or professional eligibility result from this self-declared list. Do not calculate a global completion percentage here.

### Frontend UI Context

Reuse the React/TypeScript/Tailwind profile shell. The read card lists normalized program labels with completion-year badges; no fixed 2009/2011/2021 source values appear unless returned for that account.

Use the source's repeatable row layout. Start with the saved list; Add More creates a visibly unsaved blank row with no program/year preselection. OTHER reveals its labeled text field. The year selector contains 1900 through the current UTC year in descending order, supports keyboard selection, and remains subject to server validation.

Empty state offers Add education/Edit. Show the current draft entry count out of 20; at the limit, explain why another row cannot be added. Removing a draft row changes only the draft; deleting the final row clearly shows that Save will leave no education entries. The Save/Cancel actions remain visible without creating a separate deletion workflow.

### Frontend Logic and API Context

Fetch the session and current education section before editing. Keep stable local keys for draft rows so indexed field errors remain attached to the submitted row even if rendering updates. While a save is pending, prevent row mutation so its error indices cannot point to a different row.

Send the complete entries array and loaded expectedRevision. Normalize Other names consistently, but let the server be authoritative. When a named program replaces OTHER, send otherProgramName null. Removing entries is expressed solely by their omission from the final list.

After a confirmed save, use the returned canonical order and revision rather than assuming the draft order is authoritative. Cancel restores the last loaded state. On a version conflict, keep the draft for review and explicitly load the latest list; do not auto-merge qualifications.

For an uncertain response, compare normalized canonical values from GET with the intended list. Display the current saved state if they agree without asserting which request won. Clear local account-specific data on session change and ignore superseded responses. Integrate the two declared next destinations into UC-02 before exposing direct-entry links.

### Validation and Error-Handling Context

Reject unknown top-level/entry keys, non-array entries, more than 20 entries, missing/null program or year, unknown program codes, noninteger years, years outside the declared range, and wrong OTHER-name combinations. Empty entries [] is valid; blank row objects are not.

Do not coerce "2009" to a number in the API. The frontend selector converts its chosen year to a JSON integer before submission. Do not strip a year out of arbitrary OTHER text to invent another completionYear; a named program's display label comes from its fixed option label.

Preserve Unicode names and use the declared normalization only. Mark duplicate errors at original array indices. A validation/service failure preserves the old section, and an error must not be rendered as a successful empty education list. Saving or removing qualifications is not evidence of credential verification or a change in professional status.
