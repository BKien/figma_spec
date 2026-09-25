# UC-17: Create and Edit a Course Draft

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Create and Edit a Course Draft

Description:

- Allows an Instructor to create an owned draft and save course metadata, ordered modules, video lessons, and single-choice quizzes before publication.
- Defines the authoring counterpart of UC-04 and UC-07–09. Drafts are invisible to Student discovery and cannot receive enrollments.
- Instructor authoring is an approved project extension. The source Figma supplies Student presentation patterns, not an Instructor editor; the API and content constraints below are project decisions.

Primary Actor:

ACTIVE, email-verified Instructor authenticated through UC-16/UC-02.

Preconditions:

- Instructor role routing and the `/instructor/courses` shell exist.
- The project has the shared UC-04 categories and UC-03 interest identifiers.
- Experiment fixtures supply usable video and thumbnail assets. Videos have measured integer durationSeconds, a configured media resource, and zero or more caption tracks. There is no arbitrary file-upload feature in this UC.

Postconditions:

- Success: An owned DRAFT course and its latest confirmed revision are durably stored. Reopening it reconstructs the saved metadata, curriculum order, asset references, and quiz definitions.
- Failure: A rejected save leaves the previous saved revision intact. An uncertain network outcome is reconciled before another save; local edits are not treated as published content.
- Saving creates no enrollment, quiz attempt, progress record, rating, or publication timestamp.

Main Flow:

1. The Instructor opens `/instructor/courses` and selects Create course.
2. They enter a title and submit creation. The server assigns the course ID, owner, revision=1, and DRAFT status.
3. Open `/instructor/courses/:courseId/edit`. The Instructor edits metadata, adds/reorders modules, and adds VIDEO or QUIZ units.
4. For video units, select a configured video asset. For quiz units, compose question text, optional code text, answer options, and a correct answer.
5. Save draft submits the complete editable representation with expectedRevision and an updateId.
6. The server checks ownership, DRAFT status, input structure, referenced assets, and revision. Save the entire valid representation together and increment revision once for a new accepted update.
7. Replace local baseline with the confirmed response and display `Draft saved.` Preview the curriculum outline using saved values.
8. The Instructor may continue editing or open the UC-18 publication controls. A saved draft can still need publication-readiness work.

Alternative Flow:

A.1 — Incomplete draft

- Drafts may have description=null, categoryId=null, level=null, plannedStudySeconds=null, thumbnailAssetId=null, empty modules, empty module units, or a video with mediaAssetId=null.
- A draft quiz may have 0–5 questions, each with 0–4 options and correctOptionId=null. A non-null correctOptionId must identify an option in that question. These incomplete states are saved drafts, not playable Student quizzes.
- Any present title, prompt, or option text must satisfy its nonempty length rule. Keep a half-typed empty row locally until supplied or removed; do not submit invalid strings as saved content.

A.2 — Reorder, remove, and leave

- Array order is canonical; moving an item changes order while keeping its ID. Removing a draft item removes it from the saved representation on the next successful save.
- No published curriculum can be edited or deleted. Within a draft, removed items cannot have Student progress because the draft has never been available for enrollment.
- Leaving a dirty editor offers Save and leave, Discard changes, or Stay. A failed save keeps the draft visible. Browser reload before confirmed save may lose local edits; do not claim autosave.

A.3 — Conflict or uncertain save

- A different saved revision returns REVISION_CONFLICT. Offer Reload saved version or Keep local draft for manual reconciliation; never silently overwrite the newer revision.
- Retain updateId and the exact submitted payload while its outcome is uncertain. A deliberate exact retry within 24 hours returns the current full course with a replay receipt and does not apply the mutation again. The UI displays any later saved revision rather than rolling it back.
- A request ID reused with different content returns REQUEST_CONFLICT. New IDs must not be substituted to bypass an unresolved conflict. Creation retries use the original createRequestId to avoid duplicate courses.

Exception Flow:

E.1 — Course unavailable or read-only

- Unknown and another Instructor's course both return COURSE_NOT_AVAILABLE. An owned PUBLISHED course remains readable but editing returns COURSE_READ_ONLY.
- If another tab publishes between opening and saving, publication wins only if it uses the current revision; a later editor save cannot modify the frozen course.

E.2 — Invalid content or asset

- Invalid enums, oversized arrays, duplicate/reused IDs, missing referenced correct options, and asset type mismatches return VALIDATION_ERROR with paths to fields.
- Select only assets in the experiment asset catalog. Backend validation repeats catalog/type checks. No arbitrary external URL is accepted as a video or thumbnail.

E.3 — Service or transport failure

- A definite rejection preserves saved state; preserve the local draft for correction. A timeout has unknown outcome until an exact retry or authenticated read resolves it.
- Missing session redirects through shared authentication while warning about unsaved work. Wrong application role cannot enter the editor or call its APIs.

UI Integration:

- Student-side anchors in [EdTech](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-1030): course content `222:1030`, video `222:912`, and quizzes `222:801`, `222:650`, `222:535`.
- These frames support the intended Student output, not an Instructor editing layout. The list/editor/asset selector and their responsive/error states are project-designed supplements; no exact Instructor Figma frame is available.
- `/instructor/courses`: owned-course list, title, DRAFT/PUBLISHED badge, updated time, Create course, and Open. Empty state provides Create course.
- `/instructor/courses/new`: title input and Create/Cancel. Creation success opens the editor.
- Editor: course details, ordered modules/units, video asset selector, quiz question/option editor, correct-answer selector, Save draft, and publication controls supplied by UC-18. Published views show read-only content and the UC-18 roster.
- Use accessible Move up/Move down controls for order; drag-and-drop is optional. Show saved versus unsaved state and field errors. Instructor quiz preview is a content outline, not a scored attempt or executable-code runner.

API Endpoint:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/v1/instructor/courses` | List owned courses |
| POST | `/api/v1/instructor/courses` | Create draft |
| GET | `/api/v1/instructor/courses/:courseId` | Read owned draft or published snapshot |
| PUT | `/api/v1/instructor/courses/:courseId/draft` | Replace complete editable draft |
| GET | `/api/v1/instructor/course-assets` | List configured selectable assets |

Request Body:

Create accepts exactly:

```json
{
  "createRequestId": "096880e8-7921-4e46-b3d6-dcb93632a1b2",
  "title": "Introduction to Data Analysis"
}
```

Save accepts exactly this shape; the example is intentionally an incomplete, valid draft:

```json
{
  "updateId": "3b413cb2-383f-471b-8823-02f5a1f36f6b",
  "expectedRevision": 1,
  "content": {
    "title": "Introduction to Data Analysis",
    "description": null,
    "categoryId": null,
    "level": null,
    "plannedStudySeconds": null,
    "thumbnailAssetId": null,
    "interestIds": [],
    "modules": [
      {
        "id": "c0c909c6-c286-41cc-8206-f5a39d9d1818",
        "title": "Getting Started",
        "units": [
          {
            "id": "a91a0502-2e8d-47f1-8e32-e2b25c196489",
            "title": "Welcome",
            "type": "VIDEO",
            "mediaAssetId": null
          },
          {
            "id": "7a610f1a-8760-4aa5-b3cc-ab01118d1237",
            "title": "Knowledge Check",
            "type": "QUIZ",
            "questions": []
          }
        ]
      }
    ]
  }
}
```

A question has exactly this shape, with stable case-sensitive identifiers:

```json
{
  "id": "question-1",
  "prompt": "Which value is an integer?",
  "code": null,
  "options": [
    { "id": "option-a", "text": "7" },
    { "id": "option-b", "text": "7.5" },
    { "id": "option-c", "text": "seven" },
    { "id": "option-d", "text": "None of these" }
  ],
  "correctOptionId": "option-a"
}
```

Contract rules:

| Field | Exact rule |
| --- | --- |
| Request/course/module/unit IDs | UUID; clients create module/unit IDs when adding rows; server assigns course ID |
| expectedRevision | Integer >=1 |
| Course title | Trimmed, 1–150 Unicode code points |
| description | null or trimmed 1–10,000 code points; plain text |
| categoryId | null or one of the eight UC-04 category IDs |
| level | null, BEGINNER, INTERMEDIATE, or ADVANCED |
| plannedStudySeconds | null or integer 60–3,600,000; estimated total learning effort, not summed media duration |
| thumbnailAssetId / mediaAssetId | null or UUID of an available THUMBNAIL / VIDEO asset respectively |
| interestIds | Unique array of 0–11 UC-03 interest IDs |
| modules | Ordered array, 0–20 items |
| Module/unit title | Trimmed 1–150 code points |
| Module units | Ordered array, 0–20 per module; at most 200 across the course |
| Unit type | VIDEO or QUIZ; immutable for an existing unit ID |
| Question ID / option ID | `[A-Za-z0-9_-]{1,64}`; question IDs unique within quiz, option IDs unique within question |
| prompt / option text | Trimmed, respectively 1–2,000 / 1–500 code points |
| code | null or 1–10,000 code points of plain text, preserved without execution |
| questions / options | Ordered arrays, 0–5 questions and 0–4 options per question while drafting |
| correctOptionId | null or an ID present in the same question |

Module and unit IDs are distinct throughout the content and cannot belong to any other course; existing units cannot move between modules under the same ID. Reordering inside a module is allowed. Server-derived positions are one-based array indices and are not accepted in input. VIDEO accepts no questions; QUIZ accepts no mediaAssetId. Unknown fields are rejected.

List uses optional status=ALL|DRAFT|PUBLISHED (default ALL) and page integer >=1 (default 1), fixed pageSize=20; order updatedAt descending then id ascending. No search or client-selected owner parameter. Asset/read endpoints have no query parameters or body. Mutations accept no query parameters.

Successful Response:

Creation HTTP 201, reads/saves HTTP 200. Creation returns message `Course draft created.` and the full Course object defined below, with all nullable metadata null, interestIds/modules empty, and publication timestamps null. Course read uses message `Course loaded.` Save uses `Draft saved.`

```json
{
  "success": true,
  "message": "Course draft created.",
  "data": {
    "course": {
      "id": "530f6e99-eef1-4b74-828a-faa79c3df4ba",
      "ownerInstructorId": "7978c82b-76a1-4c46-a041-0c2db832e106",
      "instructorName": "Taylor Morgan",
      "status": "DRAFT",
      "revision": 1,
      "createdAt": "2026-09-20T11:00:00.000Z",
      "updatedAt": "2026-09-20T11:00:00.000Z",
      "publishedAt": null,
      "content": {
        "title": "Introduction to Data Analysis",
        "description": null,
        "categoryId": null,
        "level": null,
        "plannedStudySeconds": null,
        "thumbnailAssetId": null,
        "interestIds": [],
        "modules": []
      }
    },
    "receipt": {
      "requestId": "096880e8-7921-4e46-b3d6-dcb93632a1b2",
      "appliedRevision": 1,
      "replayed": false
    }
  }
}
```

- Course has exactly the fields shown. content has the save-input shape; question correctOptionId is exposed only through the owned Instructor API. status is DRAFT or PUBLISHED. Timestamps are UTC ISO 8601; publishedAt is null until UC-18.
- Read returns data={course}, without receipt. Save/create return data={course,receipt}. Exact mutation replay returns HTTP 200 with the current course and the original appliedRevision/requestId, replayed=true. Store receipts for 24 hours. After that, clients reconcile through read/list and cannot rely on replay; do not automatically issue another create.
- A newly accepted save increments revision even if normalized content equals the current content. Replays do not change revision/updatedAt. Changing the stored owner is never supported.
- List: message `Courses loaded.`; data={items,page,pageSize,totalItems,totalPages}. Each item has exactly id, title, status, revision, updatedAt, publishedAt. Counts reflect owned courses under the selected status; totalPages=ceil(totalItems/20), including zero; an out-of-range page returns an empty items array.
- Assets: message `Course assets loaded.`; data={items}. Each item has exactly id, type, label, durationSeconds, captions. type is VIDEO or THUMBNAIL; durationSeconds is a positive integer for VIDEO and null for THUMBNAIL. captions is an array of {language,label}, using BCP-47 language tags; THUMBNAIL uses []. The finite fixture catalog is returned completely, sorted by label then id, and capped at 200 assets by experiment configuration. No private filesystem path or arbitrary upload URL is exposed.

Error Response:

```json
{
  "success": false,
  "statusCode": 409,
  "code": "REVISION_CONFLICT",
  "message": "This course changed. Reload the saved version before saving again.",
  "timestamp": "2026-09-20T11:10:00.000Z",
  "path": "/api/v1/instructor/courses/530f6e99-eef1-4b74-828a-faa79c3df4ba/draft"
}
```

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | Please sign in to continue. |
| 403 | ROLE_NOT_ALLOWED | This action is not available for your account role. |
| 404 | COURSE_NOT_AVAILABLE | This course is not available. |
| 409 | COURSE_READ_ONLY | Published courses cannot be edited. |
| 409 | REVISION_CONFLICT | This course changed. Reload the saved version before saving again. |
| 409 | REQUEST_CONFLICT | This request identifier was already used for different content. |
| 503 | COURSE_SERVICE_UNAVAILABLE | Course management is temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

All errors use the example envelope with actual status, UTC timestamp, and pathname, without data. VALIDATION_ERROR additionally provides errors as field-path to nonempty string-array mappings, e.g. `content.modules.0.units.1.questions.0.correctOptionId`. Malformed course IDs use COURSE_NOT_AVAILABLE; invalid query values use VALIDATION_ERROR.

## Project-Specific Implementation Context

### Backend Implementation Context

Use NestJS/TypeScript and the shared account model. Store Course owner, status, revision, timestamps, metadata, ordered modules/units, and quiz definitions. Full-draft replacement either persists completely or leaves the prior revision intact. Draft read/list are owner-scoped. Enforce maximum sizes before committing nested content and retain stable identifiers across reorder operations.

Asset fixtures must point to usable media/captions and validate their declared duration against the actual video within the UC-08 tolerance. This UC selects assets; it does not create an upload/transcoding system. Draft assets can be changed before publication. UC-18 freezes selected asset versions and quiz definitions for Student consumption.

Receipt scope is owner+operation+requestId, bound to course ID where applicable and the complete accepted payload. Recognize exact retries before checking a stale expectedRevision or current PUBLISHED state, then return the current owned course without reapplying changes. Reject different payload reuse. Owner access and current account eligibility still apply on a replay.

### Frontend UI Context

Build the supplementary list/editor with React, TypeScript, and Tailwind, using the same visual hierarchy as the Student app. Display editable metadata and curriculum in distinct sections; show optional versus publication-required fields. Incomplete quiz rows are clearly drafts. The correct-answer selector belongs exclusively to authoring, not Student quiz rendering.

### Frontend Logic and API Context

Load the course before editing and keep its confirmed revision separately from the local draft. Generate stable IDs on row creation. Disable conflicting create/save/publish actions while their outcome is unresolved. On replay, use receipt.appliedRevision and current course.revision to distinguish confirmation from a later version; do not tell the user their stale local content is the current saved content. Preserve unresolved local work for explicit reconciliation.

Published content is read-only. UC-18 publication and enrollment controls use its endpoints, not draft-save side effects. Logout uses UC-15 with this editor's save/discard/stay choices.

### Validation and Error-Handling Context

Repeat client feedback rules on the backend and attach errors to exact nested paths. Preserve the local draft on validation/conflict/service errors. Never silently remove an unsupported asset or correct answer. A saved draft is not necessarily publication-ready; only UC-18 evaluates readiness and makes it visible to learners.
