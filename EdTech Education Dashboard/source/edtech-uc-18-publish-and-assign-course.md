# UC-18: Publish a Course and Assign Learners

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Publish a Course and Assign Learners

Description:

- Allows an Instructor to release an owned, complete course to the Student catalog and assign registered Students to its learning content.
- Publication and assignment are separate durable stages of this delivery workflow. A published course can have zero learners; an assignment failure never rolls back publication.
- Replaces the fixture-only enrollment limitation in UC-04–06 with defined Instructor assignment. It preserves existing Student course cards, access rules, and progress calculations. Instructor UI and business rules are project extensions, not existing Figma functionality.

Primary Actor:

Authenticated ACTIVE, verified Instructor who owns the course.

Preconditions:

- UC-16 role integration and UC-17 draft management are implemented.
- Publishing requires a saved DRAFT at a known revision. Assigning requires an owned PUBLISHED course.
- Target learners must already be ACTIVE, verified STUDENT accounts. Incomplete Student onboarding does not prevent assignment, but Student application access still follows UC-03 completion requirements.

Postconditions:

- Publication success: An immutable PUBLISHED snapshot exists with publishedAt, a new revision, stable modules/units/questions, and usable asset versions. UC-04 discovery can show it.
- Assignment success: Exactly one enrollment exists for the course and Student. Newly assigned required units are NOT_STARTED, with zero progress, lastActivityAt=null, and completedAt=null. Previously enrolled learners retain all progress/results/timestamps.
- Publication failure: Draft remains unchanged and absent from Student discovery. Assignment failure: No partial enrollment or progress initialization; published content and other enrollments remain intact.

Main Flow:

1. The Instructor opens a saved course in UC-17 and selects Publish.
2. Show a confirmation explaining that publication exposes the course in the Student catalog and freezes its content for this experiment.
3. Submit the current expectedRevision. The backend checks ownership, saved revision, metadata, curriculum, quiz definitions, and assets.
4. On success, publish the frozen snapshot and return its summary. Show PUBLISHED status, a read-only content view, and the learner-assignment panel.
5. The Instructor enters one learner email and selects Assign learner.
6. The backend normalizes the email, resolves an eligible Student, and creates the course enrollment if none exists. No transactional notification email is sent by this UC.
7. Show the confirmed assignment and refresh the course roster. The Student sees the enrollment through UC-05/06 and can use UC-07–09 after required onboarding.

Alternative Flow:

A.1 — Publish now, assign later

- Publication does not require any learner. The Instructor can leave and reopen the published course to assign learners later.
- Catalog visibility permits a preview through UC-04; it does not itself grant access to lessons or quizzes. No self-enrollment/payment action is introduced.

A.2 — Already published or enrolled

- Publishing an already PUBLISHED owned course returns its existing publication summary with HTTP 200; it does not change content, revision, publishedAt, or student denominators. A valid but stale expectedRevision is ignored only in this already-published branch.
- Assigning an already enrolled eligible Student returns HTTP 200 with the existing enrollment and created=false. Never reset progress, attempts, assignedAt, or completion.
- Exact assignment retry within 24 hours returns the saved operation result with HTTP 200 and replayed=true. The original created value remains the result of that operation; it is not an instruction to create again. Role and ownership are rechecked; no new eligibility lookup or mutation is needed for a recognized receipt.

A.3 — Publication readiness corrections

- Return field-addressable publication requirements as VALIDATION_ERROR. Preserve the draft and return to its editor for corrections.
- Every module must contain at least one required unit. A course may consist of videos, quizzes, or both; it needs at least one module and one unit overall, with UC-17 maxima unchanged.
- All metadata needed below must be present. Each VIDEO requires an available frozen asset. Each QUIZ requires exactly five questions, each with exactly four options and one correct option.

Exception Flow:

E.1 — Revision or role mismatch

- An unpublished course whose revision changed returns REVISION_CONFLICT. Reload and review before publishing; never publish unseen changes automatically.
- Another Instructor's course is indistinguishable from an unknown course. A Student cannot use publication, assignment, or roster endpoints.

E.2 — Learner unavailable or course not published

- Unknown email, inactive/unverified account, and an Instructor email all return STUDENT_NOT_AVAILABLE. No broader account search/directory endpoint is supplied.
- Assignment against a draft returns COURSE_NOT_PUBLISHED. No hidden auto-publication occurs.

E.3 — Outcome unknown or service unavailable

- On uncertain publication response, read UC-17 course state. If published, show that state; if draft, permit deliberate retry after revision reconciliation. Disable assignment while publication state is unresolved.
- On uncertain assignment, retain requestId and submitted email for exact retry; do not report success from a local roster insertion. Once resolved, refresh the roster using server data.
- An asset failing availability validation blocks publication. If a frozen asset later becomes unavailable, surface the existing Student media/service failure; do not substitute another lesson, delete its unit, or reset progress.

UI Integration:

- Student output anchors: [My Courses, node `222:1174`](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-1174), Dashboard `222:1374`, and course content `222:1030` in the same file.
- There is no verified Instructor publication or roster frame. Add these controls to UC-17's `/instructor/courses/:courseId/edit` as project-designed UI; do not claim source support for the supplementary form or modal.
- DRAFT shows Publish, confirmation, readiness errors, and return-to-editor links. PUBLISHED shows a read-only badge, publication time, learner email input, Assign learner action, and a paginated roster.
- Roster columns: learner name, email, assigned date, learning status, and progress percent. An empty roster states `No learners assigned yet.`
- Do not display unimplemented Unpublish, Delete published course, Remove learner, Send invitation, or bulk import actions. These operations need separate lifecycle decisions before they can be added.

API Endpoint:

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/api/v1/instructor/courses/:courseId/publish` | Publish current saved draft |
| POST | `/api/v1/instructor/courses/:courseId/enrollments` | Assign one existing Student |
| GET | `/api/v1/instructor/courses/:courseId/enrollments` | Read owned-course roster |

Request Body:

Publish accepts exactly:

```json
{ "expectedRevision": 4 }
```

Assignment accepts exactly:

```json
{
  "requestId": "8b013d3d-63ac-46b7-aaaf-adb87e6a097a",
  "studentEmail": "alex@example.com"
}
```

- courseId and requestId are UUIDs; expectedRevision is an integer >=1. No mutation query parameters or additional body fields.
- studentEmail is trimmed/lowercased, valid, at most 254 characters, preserving dots and plus suffixes. Do not accept an arbitrary owner, role, learning status, or initial progress in input.
- Roster GET accepts only page integer >=1, default 1, fixed pageSize=20. No body. Sort assignedAt descending then enrollment ID ascending.

Publication requirements and Student mappings:

| Saved source | Publication rule and resulting Student value |
| --- | --- |
| title | Required; UC-17 length rules; maps to CourseCard.title |
| description | Non-null, 1–10,000 trimmed code points; UC-04 preview description |
| categoryId / level | Non-null UC-04 enum values |
| plannedStudySeconds | Non-null UC-17 positive range; CourseCard.durationSeconds and UC-07 plannedStudySeconds |
| thumbnailAssetId | Optional; null yields thumbnailUrl=null and the existing placeholder |
| owner account | instructorName snapshots its fullName at publication; owner identity cannot be reassigned |
| interestIds | Zero or more valid tags; UC-04 ranking remains unchanged |
| Modules and units | One or more of each at their required nesting level; consecutive positions derived from saved array order; all units required |
| VIDEO mediaAssetId | Non-null, accessible configured asset/version; UC-08 durationSeconds from measured media, not course effort |
| QUIZ questions | Exactly five; each has four options and one valid correctOptionId; plain optional code text |
| Quiz runtime | UC-09: 1,200 seconds, five maximum points, passing score three, at most three attempts |
| New rating fields | ratingAverage=null; ratingCount=0; do not fabricate seed ratings |
| thumbnailAlt | Course title in both cases, preserving UC-04's nonempty string contract; the UI may render its placeholder decoratively |
| Unit dueAt | null in this scope; assignment does not invent deadlines |

Course duration is planned learning effort and need not equal summed video/quiz durations. Existing fixture enrollments retain their original progress. Fixture courses used with Instructor APIs must have an explicitly provisioned owner; never claim an unowned course automatically.

Successful Response:

Publish HTTP 200, whether newly published or already published:

```json
{
  "success": true,
  "message": "Course published.",
  "data": {
    "courseId": "530f6e99-eef1-4b74-828a-faa79c3df4ba",
    "status": "PUBLISHED",
    "revision": 5,
    "publishedAt": "2026-09-20T12:00:00.000Z",
    "moduleCount": 1,
    "requiredUnitCount": 2
  }
}
```

All fields required. On the first publication revision increments once and updatedAt=publishedAt. Reads/repeats do not modify them. moduleCount/requiredUnitCount are positive integers computed from the frozen snapshot.

Assignment HTTP 201 for a newly created enrollment; HTTP 200 for an existing enrollment or exact replay:

```json
{
  "success": true,
  "message": "Learner assignment confirmed.",
  "data": {
    "enrollment": {
      "id": "9de99e8e-9622-4f62-99d2-921cdf1d04f3",
      "courseId": "530f6e99-eef1-4b74-828a-faa79c3df4ba",
      "studentId": "680f5bb3-bc89-410c-ac65-87988e9ac2f0",
      "assignedAt": "2026-09-20T12:05:00.000Z"
    },
    "created": true,
    "replayed": false
  }
}
```

Enrollment fields are required UUIDs and UTC assignedAt. A new request finding an existing enrollment returns created=false, replayed=false. Exact replay returns the saved enrollment and original created value with replayed=true. Request IDs are scoped to Instructor and bound to course+normalized email; reuse for different content returns REQUEST_CONFLICT. Receipts last 24 hours; after expiry a new request is still protected from duplicate enrollment by course+Student uniqueness, but receives no historical created=true claim.

Roster HTTP 200:

```json
{
  "success": true,
  "message": "Learners loaded.",
  "data": {
    "items": [
      {
        "enrollmentId": "9de99e8e-9622-4f62-99d2-921cdf1d04f3",
        "studentId": "680f5bb3-bc89-410c-ac65-87988e9ac2f0",
        "fullName": "Alex Jordan",
        "email": "alex@example.com",
        "assignedAt": "2026-09-20T12:05:00.000Z",
        "status": "NOT_STARTED",
        "progressPercent": 0
      }
    ],
    "page": 1,
    "pageSize": 20,
    "totalItems": 1,
    "totalPages": 1
  }
}
```

All fields required. Status is NOT_STARTED, IN_PROGRESS, or COMPLETED under UC-05/06. progressPercent=floor(100*completed required units/total required units), integer 0–100. Roster returns existing enrollments even if a Student later becomes inactive; it reports learning status, not account eligibility. Owned draft rosters are empty. totalPages=ceil(totalItems/20), zero for no enrollments; out-of-range pages return empty items. No password, quiz answers, or other-course activity appears.

Error Response:

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-20T11:58:00.000Z",
  "path": "/api/v1/instructor/courses/530f6e99-eef1-4b74-828a-faa79c3df4ba/publish",
  "errors": {
    "content.modules.0.units.1.questions": [
      "A published quiz must contain exactly five questions."
    ]
  }
}
```

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | Please sign in to continue. |
| 403 | ROLE_NOT_ALLOWED | This action is not available for your account role. |
| 404 | COURSE_NOT_AVAILABLE | This course is not available. |
| 409 | REVISION_CONFLICT | This course changed. Reload the saved version before saving again. |
| 409 | COURSE_NOT_PUBLISHED | Publish this course before assigning learners. |
| 409 | REQUEST_CONFLICT | This request identifier was already used for different content. |
| 422 | STUDENT_NOT_AVAILABLE | No eligible learner can be assigned with this email. |
| 503 | COURSE_SERVICE_UNAVAILABLE | Course management is temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

Use success=false, matching statusCode, code, message, UTC timestamp, and actual pathname without query; no data field. Only VALIDATION_ERROR adds errors, mapping input/content field paths to nonempty arrays of strings. Malformed course IDs use COURSE_NOT_AVAILABLE; malformed request IDs, emails, and page values use VALIDATION_ERROR.

## Project-Specific Implementation Context

### Backend Implementation Context

Use the shared NestJS/TypeScript Course, Account, Enrollment, and progress models. Publication validates one saved revision and persists the immutable snapshot, status, revision, and timestamp together. Reject later draft writes; no content replacement, unpublish, owner transfer, or published deletion is provided. Referenced published media/caption versions remain available for the experiment; a fixture refresh cannot silently replace their contents.

Published course cards map exactly to UC-04. Drafts never appear in Student APIs. Quiz correct answers remain in grading/owned Instructor representations and are excluded from every Student question payload. Learner endpoints use the frozen content and UC-08/09 semantics rather than implementing another player or grader.

Enrollment creation is unique per Student/course and must not expose an enrollment before required initial learning state can be read coherently. Repeated/concurrent assignment preserves the existing enrollment and progress. Assignment is not a learning activity, so lastActivityAt stays null for a new enrollment. Existing completion remains unchanged. Read roster progress from the same canonical calculation as UC-06.

This UC explicitly extends UC-04–06's fixture-only enrollment baseline: newly published courses join discovery and newly assigned courses join authenticated Student projections. UC-04 trending counts use actual current enrollments. Each published curriculum stays fixed, preserving UC-05–09 progress denominators; adding another course does not modify existing course completion. No ratings, study-time totals, streaks, or notification delivery are inferred from enrollment.

### Frontend UI Context

Add publication and roster sections to the supplementary Instructor editor with React, TypeScript, and Tailwind. Keep Publish separate from Save draft so saving does not expose work accidentally. Incomplete drafts show actionable readiness messages. Published status remains visible when an individual assignment fails. On narrow screens present roster rows as readable labelled cards without hiding status or assignment errors.

### Frontend Logic and API Context

Publish only the last confirmed saved revision; a dirty form must save successfully first or stay in editing. Disable conflicting operations until resolved. Read server publication state after uncertain outcomes and preserve the assignment request ID for deliberate retry. Refresh list/detail/roster caches after success; Students obtain new enrollments through their normal reads without a forced sign-out or invented real-time channel.

Preserve email input after a failed assignment, clear it after a confirmed result, and distinguish an existing enrollment from a newly created one. Pagination reflects server counts. Opening a course through a Student preview does not bypass its enrollment check.

### Validation and Error-Handling Context

Keep structural draft validation and publication readiness distinct. Check media availability and exact quiz cardinality before release, and report errors against the saved content paths. Unknown and ineligible learner emails share one assignment message. Do not partially publish or initialize an enrollment, fabricate success on timeout, reset progress on retries, or turn a publication error into a draft-content rewrite.
