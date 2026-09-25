# UC-08: Manage Work Experience and Resume

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Manage Work Experience and Resume

Description:

- Allows a Job Seeker to maintain their relevant-experience band, self-declared board-certification status, self-ratings in four dental areas, and optional resume in one profile section.
- This is the experience-summary form shown in Figma. It is not an employment-history timeline, employer reference check, licensing service, or professional verification process.
- The visible fields and five-star controls come from the source frames. Dropdown vocabularies, optionality, file constraints, routes, save behavior, and API contracts are explicit project decisions; no Technical Report or existing backend contract has been supplied for this feature.

Primary Actor:

Authenticated ACTIVE JOB_SEEKER.

Preconditions:

- UC-01/02 provide the shared account and browser session; UC-05 provides the profile shell and basic-profile route.
- `/profile/work-experience` and `/profile/work-experience/edit` are implemented as reloadable routes. Activate the previously unavailable Work Experience tab in the shared profile navigation.
- The backend can persist an optional resume and serve the currently saved document to its owner. A newly registered account works without sample experience, ratings, or a resume.

Postconditions:

- Success: The complete experience section and requested resume action are committed together, the section revision advances once, and the read page shows the canonical saved representation.
- Failure: The previous saved experience and resume remain intact. Form errors or conflicts are visible; an uncertain write result is reconciled before another explicit save.
- Self-ratings and certification declarations are not marked verified. Reading/saving does not publish the profile, apply for a job, change account eligibility, or alter UC-05/06 data or UC-07 ranking. Global profileCompletionStatus remains unchanged.

Main Flow:

1. Open Profile → Work Experience and retrieve the saved section.
2. Show the experience band, declared board-certification status, four self-ratings, and a Download resume action if a saved resume exists.
3. Select Edit and initialize the form with the returned revision and values.
4. Select an experience band and certification answer; set or clear applicable self-ratings and optionally select a resume file.
5. Select Save Changes. Validate the draft and submit one multipart request containing metadata and, only when replacing the resume, the selected file.
6. The backend validates eligibility, fields, file, and expected revision, then commits one complete section update.
7. Display `Work experience saved.` and return to `/profile/work-experience` with the returned values.

Alternative Flow:

A.1 — New or nonclinical applicant

- A missing section returns revision 0, experienceBand null, boardCertification null, all four ratings null, resume null, and updatedAt null. GET does not create a section.
- The first save requires an explicit experienceBand and boardCertification answer. NO_EXPERIENCE and NOT_APPLICABLE are valid answers. Ratings and resume remain optional, including for Office Staff and Office Manager applicants.
- Null rating displays `Not rated`; it is not zero ability. Do not prefill the source's 4/2/2/1 stars for a new account.

A.2 — Add, replace, remove, or download a resume

- Selecting/dropping a file changes only the local draft. KEEP preserves the current resume, REPLACE uses exactly one attached file, and REMOVE clears it when Save Changes succeeds.
- Add an explicit Remove resume action beside an existing document. Removal before Save is only a draft action; Cancel restores the saved representation.
- Download resume retrieves the owner's currently committed file. Before a replacement is saved, that link still refers to the old saved file, and the new filename is labeled as an unsaved selection.
- If no resume exists, KEEP or REMOVE leaves resume null. Resume is not a prerequisite for saving ratings or browsing jobs.

A.3 — Cancel and direct entry

- Cancel before submission discards the local draft/file and returns to the read page without a write. After submission starts, retain the editor until the outcome is known; Cancel must not imply that an in-flight server change was undone.
- Add exactly `/profile/work-experience` and `/profile/work-experience/edit` to UC-02's permitted local next destinations. Encode the destination as the next query value when directing an unauthenticated actor to sign-in. No additional queries/fragments are accepted for these destinations.

Exception Flow:

E.1 — Invalid field or resume

- Show field errors without clearing valid inputs. Reject unsupported or unreadable documents using the contracts below. A PDF filename alone is not proof that a usable PDF was supplied.
- Storage failure leaves the previous section and resume unchanged. Retain the selected local file while the same editor/session remains active and offer an explicit retry.

E.2 — Newer work experience exists

- A stale expectedRevision returns WORK_EXPERIENCE_VERSION_CONFLICT. Retain the draft and offer Reload latest. Show the current saved values before the actor reapplies changes; never silently overwrite another editor's save.
- The work-experience revision is independent of basic-profile, preferences, education, and video revisions.

E.3 — Lost response, failed read, or expired session

- After an ambiguous save result, GET the section. If text/rating values now match, show the current saved representation. When a resume replacement was involved, let the actor review/download the current resume; a revision increment or matching filename does not prove which upload was committed.
- If current values differ, retain the same-session draft for review without automatically retrying against a new revision. A failed GET is a load error, not evidence of an empty section.
- Authentication loss clears private section/file state and requires sign-in again. Do not restore one account's draft into another account.

UI Integration:

- File DH Dental Recruitment (Community), page Pages / Job Seeker (`1:2`).
- [Profile / Work Experience, frame `2:4915`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4915): relevant-experience row, Board Certified, Resume, four five-star rating rows, and Edit.
- [Profile / Edit Work Experience, frame `2:5039`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-5039): two dropdowns, resume upload/drop area, star selectors, Cancel, and Save Changes.
- Both contexts and screenshots inspected on 2026-09-23. These are desktop references, not a frozen dataset or verified prototype interactions.
- Keep the source areas Endodontics, Orthodontics, Prosthetics/Restorative, and Oral Surgery/Implants. Explain `Self-assessed, not independently verified.` Read-only stars are display values; editable stars have named values and keyboard controls.
- Normalize the edit label `Year of Relevant Experience` to `Years of Relevant Experience`. The unexpanded dropdowns do not establish all options; the finite choices below are project supplements.
- Add Clear rating, Remove resume, filename/size display, and upload/error states explicitly. Resume supports the file picker and drop area; neither action saves immediately. Use `Not provided` for missing certification rather than conflating it with Not applicable.
- Reuse UC-05's profile shell and correct active tab. Education and Introduction Video become working routes when UC-09/10 are integrated. Other unfinished actions retain the existing unavailable-action behavior. On narrow screens stack the dropdowns and rating rows while keeping their labels visible.

API Endpoint:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/v1/job-seeker/profile/work-experience` | Read the current experience section |
| PUT | `/api/v1/job-seeker/profile/work-experience` | Save all editable fields and the resume action |
| GET | `/api/v1/job-seeker/profile/resume` | Download the current owner's saved resume |

All require the UC-02 session and reject query parameters. GET has no body. PUT uses multipart/form-data. The resume download is whole-file only in this UC; no byte-range contract is introduced.

Request Body:

PUT has exactly one text part metadata containing this JSON object and, only for REPLACE, exactly one binary part resume:

```json
{
  "expectedRevision": 0,
  "experienceBand": "ONE_TO_THREE",
  "boardCertification": "NOT_APPLICABLE",
  "ratings": {
    "endodontics": 4,
    "orthodontics": 2,
    "prostheticsRestorative": 2,
    "oralSurgeryImplants": 1
  },
  "resumeAction": "KEEP"
}
```

| Field | Rule |
| --- | --- |
| expectedRevision | Required integer >= 0, matching the loaded work-experience revision |
| experienceBand | Required non-null enum from the table below |
| boardCertification | Required YES, NO, or NOT_APPLICABLE; a declaration, not evidence of verification |
| ratings | Required object with exactly endodontics, orthodontics, prostheticsRestorative, oralSurgeryImplants |
| Each rating | null, or an integer 1–5; all four keys must appear |
| resumeAction | Required KEEP, REPLACE, or REMOVE |
| resume | One readable, non-password-protected PDF, > 0 and <= 5,242,880 bytes for REPLACE; absent otherwise |

| experienceBand | Display label | Interpretation |
| --- | --- | --- |
| NO_EXPERIENCE | No relevant experience | No relevant work experience declared |
| LESS_THAN_ONE | Less than 1 year | Some experience, less than one completed year |
| ONE_TO_THREE | 1–3 years | 1 through 3 completed years |
| FOUR_TO_SIX | 4–6 years | 4 through 6 completed years |
| SEVEN_TO_TEN | 7–10 years | 7 through 10 completed years |
| MORE_THAN_TEN | More than 10 years | At least 11 completed years |

The years are the actor's estimate; no start/end dates or employer history are collected. Rating labels are 1 Limited exposure, 2 Basic experience, 3 Moderate experience, 4 Strong experience, 5 Extensive experience. These labels explain a self-assessment only; null is Not rated and 0 is invalid.

metadata has a maximum of 16,384 UTF-8 bytes; total multipart body including framing is at most 6,291,456 bytes. Exceeding either limit or the resume size limit returns UPLOAD_TOO_LARGE. Missing/extra parts, invalid JSON, empty file, password-protected/unreadable PDF, or a mismatched resumeAction returns VALIDATION_ERROR. Unsupported request media type or non-PDF format returns UNSUPPORTED_MEDIA_TYPE. Detect document format from content, not only the supplied filename/MIME label.

No caller-supplied download URL, account ID, verified flag, global completion status, or overall rating is accepted.

Successful Response:

GET and PUT return HTTP 200 with exactly data.asOf and data.workExperience. PUT example:

```json
{
  "success": true,
  "message": "Work experience saved.",
  "data": {
    "asOf": "2026-09-23T15:00:00.000Z",
    "workExperience": {
      "revision": 1,
      "experienceBand": "ONE_TO_THREE",
      "boardCertification": "NOT_APPLICABLE",
      "ratings": {
        "endodontics": 4,
        "orthodontics": 2,
        "prostheticsRestorative": 2,
        "oralSurgeryImplants": 1
      },
      "resume": null,
      "updatedAt": "2026-09-23T15:00:00.000Z"
    }
  }
}
```

GET uses message `Work experience loaded.` workExperience contains exactly revision, experienceBand, boardCertification, ratings, resume, and updatedAt. The initial representation uses the null values defined in A.1 and revision 0. After any successful PUT, revision increases by one (first save 1), even for an explicitly submitted unchanged form, and updatedAt is server UTC ISO 8601.

A saved resume replaces null with exactly:

```json
{
  "url": "/api/v1/job-seeker/profile/resume",
  "fileName": "resume.pdf",
  "contentType": "application/pdf",
  "byteSize": 245760
}
```

Use the canonical download/display filename resume.pdf; the original local filename need not be stored or exposed. byteSize is the actual committed file size. A replacement with the same name can contain different bytes.

GET resume returns HTTP 200 with the saved PDF bytes, Content-Type application/pdf, Content-Disposition attachment; filename="resume.pdf", and actual Content-Length. It returns no success JSON envelope. A Range header is ignored and the complete file is returned as 200. If the section has no saved resume, return RESUME_NOT_FOUND.

Error Response:

All JSON errors contain exactly success false, statusCode, code, message, timestamp (UTC ISO 8601), and path (actual pathname without query). VALIDATION_ERROR additionally contains errors, an object mapping field paths to nonempty arrays of messages. Other codes omit errors. Do not add data: null. Binary download/playback successes are explicitly identified; their errors still use this JSON envelope.

| HTTP | code | message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | Please sign in to continue. |
| 403 | ROLE_NOT_ALLOWED | This action is not available for your account role. |
| 404 | RESUME_NOT_FOUND | No resume is available. |
| 409 | WORK_EXPERIENCE_VERSION_CONFLICT | Your work experience changed in another session. Reload the latest version before saving. |
| 413 | UPLOAD_TOO_LARGE | The resume upload exceeds the allowed size. |
| 415 | UNSUPPORTED_MEDIA_TYPE | Use multipart form data with a PDF resume. |
| 503 | WORK_EXPERIENCE_UNAVAILABLE | Work experience is temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

404 applies only to resume download when no committed resume exists. 409/413/415 apply to PUT. If metadata says a resume exists but its storage is unavailable or inconsistent, use 503, not a false empty section or successful empty download.

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-23T15:00:00.000Z",
  "path": "/api/v1/job-seeker/profile/work-experience",
  "errors": {
    "ratings.endodontics": [
      "Choose a whole-number rating from 1 to 5, or clear the rating."
    ],
    "resume": [
      "Choose a readable PDF that does not require a password."
    ]
  }
}
```

```json
{
  "success": false,
  "statusCode": 409,
  "code": "WORK_EXPERIENCE_VERSION_CONFLICT",
  "message": "Your work experience changed in another session. Reload the latest version before saving.",
  "timestamp": "2026-09-23T15:00:00.000Z",
  "path": "/api/v1/job-seeker/profile/work-experience"
}
```

## Project-Specific Implementation Context

### Backend Implementation Context

Use the UC-02 cookie-based browser session. All feature endpoints require the account resolved from that session to be an ACTIVE JOB_SEEKER. Unverified email/mobile, an incomplete basic profile, and global profileCompletionStatus INCOMPLETE do not block this feature. A missing, expired, or account-ineligible session returns 401 UNAUTHENTICATED; an otherwise valid unsupported-role session returns 403 ROLE_NOT_ALLOWED. No endpoint accepts a caller-supplied account ID.

Use the proposed NestJS/TypeScript stack and one WorkExperience section per Account. Persist its independent revision, experienceBand, boardCertification, four nullable ratings, optional resume reference/metadata, and updatedAt. The read endpoint composes only the declared response; no candidate publication or professional verification record is created.

GET of a missing section produces the documented initial state without writing. PUT replaces the whole editable section after checking the revision. Concurrent first saves against revision 0 cannot both succeed. A resume replacement and the scalar/rating update become visible together; a conflict or file failure cannot leave half of the request committed.

Preserve the previous resume until a replacement is usable and its new section state is committed. Clean up unreferenced files from failed/conflicting attempts, and retire replaced/removed files after the section no longer references them. Serve only the current owner's committed resume. No public document URL or employer access is introduced here.

BoardCertified YES is self-reported and does not change Account status, verification flags, profileCompletionStatus, or job eligibility. The four ratings remain separate values; no averaged score is added. Work experience does not become a new ranking input in UC-07 without an explicit future change.

### Frontend UI Context

Implement the read/edit cards in React, TypeScript, and Tailwind CSS using the existing profile shell. The read view renders labels from the finite enum vocabulary; never insert Figma sample values into a new profile. Separate Not provided, Not applicable, No, and Not rated visibly.

Use an accessible single-choice control for each rating, with the dental-area name and value announced together. Provide Clear rating so null can be selected again. Preserve the original dental icons and five-star composition where applicable; avoid representing null as a poor score.

Display the saved resume link and selected replacement as different states. The picker/drop area states PDF and 5 MiB. Show the actual selected filename locally, but use the returned canonical resume.pdf name after save. Show upload progress only if measured; otherwise show a sending indicator without a fabricated percentage.

### Frontend Logic and API Context

Load the current session and section before initializing the draft. Send a complete metadata object with the captured expectedRevision and explicit null ratings. Build multipart using the browser's generated boundary. Do not send the read response object back wholesale because resume metadata and updatedAt are not writable.

Selecting a file sets resumeAction REPLACE; canceling a file picker leaves the existing draft unchanged. Remove resume sets REMOVE and clears a selected replacement. Canceling the editor discards all changes. Save stays disabled while sending or reconciling an uncertain result.

After a confirmed save, replace the read-view state with the response and invalidate the current resume download representation. Do not update the UC-02 user schema or unrelated section revisions. Requests and local file state are scoped to the account; ignore outdated responses and clear private state on session changes.

For conflicts, refetch before the actor reviews/reapplies edits. For uncertain saves with file replacement, show the actual current document for review; do not infer byte equality from the fixed filename or file size alone. Read retry is nonmutating.

### Validation and Error-Handling Context

Reject unknown keys at every object level, unsupported query/body data on GET, missing required metadata fields, duplicate multipart parts, unknown enums, string ratings, fractions, and ratings outside 1–5. Use field paths experienceBand, boardCertification, ratings.<area>, resume, resumeAction, expectedRevision, metadata, or request in validation errors.

All-null ratings and an absent resume are valid. New entrants may explicitly choose NO_EXPERIENCE. Do not impose a dental-specialist certification prerequisite on every job-seeker role or reinterpret NOT_APPLICABLE as verified.

Preserve prior data on validation, conflict, and persistence failure. Distinguish an absent resume (404), unsupported document type (415), unusable PDF (400), size failure (413), and service outage (503). Never display success until a confirmed response or the reconciled current-state flow justifies it.
