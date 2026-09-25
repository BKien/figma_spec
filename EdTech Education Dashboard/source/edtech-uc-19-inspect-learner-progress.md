# UC-19: Inspect an Enrolled Learner’s Progress

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Inspect an Enrolled Learner’s Progress

Description:

- Lets the owning Instructor inspect one learner's course/module/unit completion, video coverage, and quiz-attempt results.
- Extends UC-18's summary roster into a detailed diagnostic view. It does not introduce another roster, alter grades, or simulate learning activity.
- The Instructor screen and API are project-designed supplements. Existing Student progress and quiz frames provide visual reference; no Technical Report or dedicated Instructor Figma frame supplies this behavior.

Primary Actor:

Authenticated ACTIVE, email-verified INSTRUCTOR who owns the published course.

Preconditions:

- UC-16–18 account, ownership, publication, and enrollment contracts are implemented.
- The requested enrollment belongs to the requested owned course. The learner need not have started learning or completed onboarding.
- UC-08 and UC-09 are the authoritative producers of video progress and quiz results.

Postconditions:

- Success: The Instructor sees a consistent, server-timestamped view of the selected enrollment and its complete frozen curriculum.
- Failure: No other learner/course data is displayed as a substitute. Previously loaded data, if retained for the same selection, is visibly stale.
- Reading changes no progress, completion, lastActivityAt, attempt count, deadline, or grade.

Main Flow:

1. Open the UC-18 roster and select View progress for a learner.
2. Open `/instructor/courses/:courseId/learners/:enrollmentId` and request the detailed progress resource.
3. The server confirms the current Instructor and course/enrollment relationship, then reads the canonical progress and attempt records.
4. Display learner identity, assignment date, course status, completed/required unit counts, and course completion percentage.
5. Display modules in curriculum order; expand a module to show video coverage and quiz-attempt summaries.
6. The Instructor may refresh explicitly or return to the roster. Refresh replaces the view only after a successful read.

Alternative Flow:

A.1 — No learning activity yet

- Return every required unit with NOT_STARTED, null startedAt/completedAt, and zero video coverage or zero quiz attempts. Course/module progress is zero, not unavailable. Do not create progress merely to render the page.

A.2 — Completed learner or unsuccessful retry

- Completed units stay completed. Show all quiz attempts in attempt-number order, including later unsuccessful retries; bestScore remains the highest submitted score. One passing attempt is enough for quiz completion under UC-09.
- A course can be COMPLETED while a permitted later quiz retry is still IN_PROGRESS. Do not derive completion solely from the latest attempt.

A.3 — Overdue quiz awaiting finalization

- GET reports persisted IN_PROGRESS and its original expiresAt until UC-09 finalizes it. If asOf >= expiresAt, label that attempt `Time expired — result pending` and offer Refresh.
- This view neither finalizes an attempt nor extends its timer. The UC-09 deadline processor remains responsible for finalization, including recovery after an outage.

A.4 — Learner later becomes inactive

- An existing enrollment remains visible to its course owner, consistent with UC-18's roster. Inactivity does not erase historical progress. Do not add an account-reactivation control.

Exception Flow:

E.1 — Invalid relationship

- Unknown/malformed IDs, an unowned course, or an enrollment outside that course return the same PROGRESS_NOT_AVAILABLE. Never look up the learner globally and display another enrollment.

E.2 — Required progress is inconsistent

- A missing published curriculum, empty required module, contradictory completion timestamps/counts, or unavailable required progress storage returns LEARNER_PROGRESS_UNAVAILABLE. Do not manufacture zero progress to conceal an unavailable record.
- Absence of activity rows for a known untouched unit is a valid zero state, not an inconsistency.

E.3 — Session or request failure

- Missing/ineligible session returns 401; a valid non-Instructor session returns 403 ROLE_NOT_ALLOWED. Service failure does not imply logout.
- Changing the selected learner clears the previous learner's detail immediately. Ignore late responses belonging to an old selection.

UI Integration:

- References in the EdTech file: [Student Dashboard `222:1374`](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-1374), course content `222:1030`, and quiz result `222:535`.
- Add the Instructor route above and a View progress action to UC-18. Its learner header, module accordion, coverage values, attempt table, loading/empty/error states, and narrow-screen layout are project supplements, not verified Instructor Figma screens.
- Label coveredSeconds as unique video coverage, not total study time. Show score as `2 / 5`, not an invented percentage trend. Show asOf as last refreshed time.
- No answer editing, manual completion, retry reset, certificates, guessed streaks, or grade overrides are provided.

API Endpoint:

`GET /api/v1/instructor/courses/:courseId/enrollments/:enrollmentId/progress`

Request Body:

None. No query parameters. Both path identifiers are UUIDs. Reject unsupported query parameters with VALIDATION_ERROR; malformed path IDs use PROGRESS_NOT_AVAILABLE.

Successful Response:

```json
{
  "success": true,
  "message": "Learner progress loaded.",
  "data": {
    "asOf": "2026-09-21T10:00:00.000Z",
    "course": {
      "id": "530f6e99-eef1-4b74-828a-faa79c3df4ba",
      "title": "Introduction to Data Analysis"
    },
    "enrollment": {
      "id": "9de99e8e-9622-4f62-99d2-921cdf1d04f3",
      "studentId": "680f5bb3-bc89-410c-ac65-87988e9ac2f0",
      "fullName": "Alex Jordan",
      "email": "alex@example.com",
      "assignedAt": "2026-09-20T12:05:00.000Z",
      "status": "IN_PROGRESS",
      "progressPercent": 50,
      "lastActivityAt": "2026-09-21T09:45:00.000Z",
      "completedAt": null
    },
    "summary": {
      "requiredUnitCount": 2,
      "completedUnitCount": 1
    },
    "modules": [
      {
        "id": "c0c909c6-c286-41cc-8206-f5a39d9d1818",
        "title": "Getting Started",
        "position": 1,
        "status": "IN_PROGRESS",
        "progressPercent": 50,
        "units": [
          {
            "id": "a91a0502-2e8d-47f1-8e32-e2b25c196489",
            "title": "Welcome",
            "position": 1,
            "type": "VIDEO",
            "status": "COMPLETED",
            "startedAt": "2026-09-21T09:00:00.000Z",
            "completedAt": "2026-09-21T09:09:00.000Z",
            "video": {
              "durationSeconds": 600,
              "coveredSeconds": 540,
              "coveragePercent": 90
            }
          },
          {
            "id": "7a610f1a-8760-4aa5-b3cc-ab01118d1237",
            "title": "Knowledge Check",
            "position": 2,
            "type": "QUIZ",
            "status": "IN_PROGRESS",
            "startedAt": "2026-09-21T09:30:00.000Z",
            "completedAt": null,
            "quiz": {
              "attemptsUsed": 1,
              "bestScore": 2,
              "attempts": [
                {
                  "id": "848895df-051c-469f-943d-126b67812a5b",
                  "number": 1,
                  "status": "SUBMITTED",
                  "startedAt": "2026-09-21T09:30:00.000Z",
                  "expiresAt": "2026-09-21T09:50:00.000Z",
                  "submittedAt": "2026-09-21T09:45:00.000Z",
                  "submissionReason": "MANUAL",
                  "result": {
                    "score": 2,
                    "maxScore": 5,
                    "passed": false
                  }
                }
              ]
            }
          }
        ]
      }
    ]
  }
}
```

HTTP 200. Exact response structure is shown, with arrays varying by frozen curriculum and actual attempts:

- asOf is server UTC. course has exactly id and title. enrollment has exactly the shown keys; assignedAt is non-null, lastActivityAt and completedAt nullable. IDs are UUIDs; name/email are the account's stored values.
- summary counts are integers; requiredUnitCount >=1 and 0 <= completedUnitCount <= requiredUnitCount. Course progress is floor(100*completedUnitCount/requiredUnitCount), never an average of module percentages.
- modules/units contain every required item ordered by one-based position. Status is NOT_STARTED, IN_PROGRESS, or COMPLETED using UC-05–09. Module percentage uses that module's completed/required units.
- Each unit has the common fields shown and exactly one type-specific object: video for VIDEO, quiz for QUIZ. startedAt/completedAt are nullable UTC timestamps; completed units have both non-null.
- video contains durationSeconds positive integer, coveredSeconds integer 0..durationSeconds, and coveragePercent=floor(100*coveredSeconds/durationSeconds). Completion follows UC-08's 90% coverage threshold; this differs from the course's completed-unit percentage.
- quiz has attemptsUsed integer 0..3, bestScore null before any submitted attempt or integer 0..5 afterward, and attempts containing all used attempts, at most three. Attempts are ordered by number ascending. No question text, submitted answer choices, correct-answer keys, credentials, or other-course records are returned.
- Attempt has exactly id, number, status, startedAt, expiresAt, submittedAt, submissionReason, and result. IN_PROGRESS has the last three fields null. SUBMITTED has submittedAt non-null, reason MANUAL or DEADLINE, and result={score:0..5,maxScore:5,passed:score>=3}. Original expiry is preserved even after submission.
- Read all aggregates and their detail from one coherent view. Concurrent Student activity may appear on the next refresh; the current response cannot contradict its own counts.

Error Response:

```json
{
  "success": false,
  "statusCode": 404,
  "code": "PROGRESS_NOT_AVAILABLE",
  "message": "This learner progress is not available.",
  "timestamp": "2026-09-21T10:00:00.000Z",
  "path": "/api/v1/instructor/courses/530f6e99-eef1-4b74-828a-faa79c3df4ba/enrollments/9de99e8e-9622-4f62-99d2-921cdf1d04f3/progress"
}
```

All errors contain success=false, statusCode matching the HTTP status, code, message, a server UTC ISO 8601 timestamp, and the actual request pathname without query. Omit data. Only VALIDATION_ERROR may add errors, mapping field paths to nonempty arrays of strings. All success fields described below are required unless explicitly nullable. IDs and timestamps in examples are illustrative.

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | Please sign in to continue. |
| 403 | ROLE_NOT_ALLOWED | This action is not available for your account role. |
| 404 | PROGRESS_NOT_AVAILABLE | This learner progress is not available. |
| 503 | LEARNER_PROGRESS_UNAVAILABLE | Learner progress is temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

## Project-Specific Implementation Context

### Backend Implementation Context

Use NestJS/TypeScript with UC-18 ownership/enrollment and the existing progress projections. Derive summary/module status from the same completed-unit model as Student reads. Return the stored attempt history without initiating quiz mutations. Reading this resource never updates lastActivityAt or a completion timestamp. Keep the complete maximum of 200 units from UC-17; no partial curriculum page is presented as the course total.

### Frontend UI Context

Use React, TypeScript, and Tailwind in the supplementary Instructor shell. Keep learner identity and course title visible above details. Render collapsible modules and a compact attempt table; use labelled cards on narrow screens. Explicitly distinguish no activity, stale data, pending deadline finalization, and service failure.

### Frontend Logic and API Context

Use courseId plus enrollmentId as the detail cache identity. Read when entering or selecting Refresh; no automatic progress writes or polling are needed. Return-to-roster preserves its current page. Clear private data on sign-out, role change, or a changed selection. A failed refresh may retain only the same learner's previous confirmed result with a stale indicator.

### Validation and Error-Handling Context

Validate the nested relationship at the server and keep all projected values consistent with the Student view. Null bestScore means no submitted result; zero means a real submitted score of zero. Never use zero for a failed read or infer full completion from all videos when a required quiz remains incomplete.
