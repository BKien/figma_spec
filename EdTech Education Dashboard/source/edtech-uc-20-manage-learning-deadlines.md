# UC-20: Manage Course Learning Deadlines

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Manage Course Learning Deadlines

Description:

- Allows the owning Instructor to set, change, or clear a recommended completion deadline for each published VIDEO or QUIZ unit.
- Activates UC-05 upcoming tasks with authored dates. A learning deadline is advisory: it does not close content, shorten a quiz attempt, reduce scores, or revoke enrollment.
- Schedule is a separate mutable resource. This explicitly extends UC-18's null dueAt baseline without changing its immutable published curriculum, unit IDs, grading, or course revision.
- Instructor scheduling controls and the Student schedule view are project supplements; Figma's Student upcoming-task presentation does not define scheduling behavior.

Primary Actor:

Authenticated ACTIVE, email-verified Instructor who owns the published course. An enrolled Student is the reader of the resulting schedule.

Preconditions:

- UC-16–18 are implemented. The published course contains the requested required unit.
- UC-05 upcomingTasks uses incomplete enrolled units and UTC due dates. UC-09 separately owns the 20-minute quiz attempt timer.
- Instructor schedule reads/writes require INSTRUCTOR. Student schedule reads require ACTIVE, verified STUDENT, completed onboarding, and enrollment.

Postconditions:

- Success: The chosen unit has the confirmed dueAt, and the course schedule has a new revision. Student schedule and subsequent dashboard reads use that same value.
- Failure: No schedule entry or revision changes on rejection. Unknown outcome is reconciled before another edit.
- Progress, completion timestamps, grades, attempt expiry, enrollment, and immutable course content remain unchanged.

Main Flow:

1. The Instructor opens Schedule on the published UC-17/18 course view.
2. Load every required unit and its current dueAt, with the shared schedule revision.
3. Select a unit, enter a UTC date/time, or choose Clear deadline. Show the exact UTC instant before confirmation.
4. Submit the single-unit update with updateId and expectedRevision.
5. The server verifies ownership, publication, unit membership, input time, and current schedule revision, then commits the entry and revision together.
6. Replace the displayed schedule with the confirmed response and show `Learning deadline saved.`
7. Enrolled Students see the date in the schedule; UC-05 includes it among incomplete tasks under its existing ordering and four-item limit.

Alternative Flow:

A.1 — No deadline or clear an existing deadline

- A new published course has revision=0, updatedAt=null, and all dueAt=null. Clear submits dueAt=null and removes the task from upcomingTasks on the next read.
- A new accepted request increments schedule revision once, even if its value equals the existing value. Exact request replays do not increment again.

A.2 — Overdue, completed, or newly assigned learner

- Deadlines apply to all current and future enrollments in this course. A learner assigned after a deadline sees it as overdue if the unit is incomplete; assignment does not shift it.
- An incomplete unit is overdue when dueAt <= current server time. A completed unit never becomes an overdue task. Student schedule can still display its date as context.
- Extending or clearing a date changes only the current schedule. Do not create a historical lateness score or rewrite when the learner completed a unit.

A.3 — Quiz timer and notifications

- Quiz expiresAt remains startedAt+1200 seconds even if a recommended completion deadline is earlier, later, or changed during the attempt. UC-09 finalization remains unchanged.
- UC-12 notification preferences do not create a delivery service. This UC sends no email, reminder, or push notification.

A.4 — Retry or conflicting tabs

- Recognize an exact accepted updateId/payload repeat for 24 hours and return the current schedule plus original appliedRevision, replayed=true. Recheck caller eligibility and ownership, but do not revalidate the old date as a new change.
- A new update with stale expectedRevision returns SCHEDULE_REVISION_CONFLICT. Keep the local proposal and offer reload for explicit reconciliation; never overwrite another tab automatically.
- After a receipt expires, GET the current schedule before a fresh mutation. Reusing a still-recognized ID for a different payload returns REQUEST_CONFLICT.

Exception Flow:

E.1 — Invalid date

- API dueAt must be null or a valid UTC ISO timestamp exactly in `YYYY-MM-DDTHH:mm:ss.sssZ` format. Reject impossible calendar values and unsupported offsets.
- A newly changed non-null dueAt must be strictly later than server evaluation time. Retaining the identical stored timestamp is allowed even if it has passed; clearing is always allowed. Evaluate this after revision validation for a new mutation.

E.2 — Wrong resource or publication state

- Unknown/malformed/unowned course or foreign unit returns SCHEDULE_NOT_AVAILABLE. An owned DRAFT returns COURSE_NOT_PUBLISHED. No draft save can change schedule fields.
- Student reads never reveal a course schedule without enrollment. Invalid nesting or unavailable enrollment returns ENROLLED_COURSE_NOT_AVAILABLE.

E.3 — Service failure

- A rejected save keeps the prior schedule. On timeout retain the update ID and submitted payload for deliberate retry or read reconciliation; do not show a success toast from the local date alone.
- Concurrent unit completion does not block a schedule change or undo learning progress. Each dashboard response must still use coherent current deadline/progress values.

UI Integration:

- Reference: [Student Dashboard, `222:1374`](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-1374), specifically the upcoming learning-task concept already specified in UC-05.
- Add `/instructor/courses/:courseId/schedule` with ordered units, labelled UTC date/time inputs, Save and Clear actions, and explicit pending/conflict states. These are supplementary Instructor controls, not an existing source frame.
- Add `/student/courses/:courseId/schedule`, linked from UC-07, showing each unit's date or `No deadline`. Link unit titles to UC-07's existing unit route. This supplementary page uses the Student schedule endpoint below.
- Preserve the UC-05 dashboard response shape and four-task limit; no new full-dashboard endpoint. Use UTC labels consistently. Calendar import, notification delivery, and date-based content locks are outside this UC.

API Endpoint:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/v1/instructor/courses/:courseId/schedule` | Read complete owned-course schedule |
| PUT | `/api/v1/instructor/courses/:courseId/schedule/units/:unitId` | Set or clear one learning deadline |
| GET | `/api/v1/student/courses/:courseId/schedule` | Read enrolled-course schedule |

All paths use UUIDs. No query parameters. GET has no body.

Request Body:

```json
{
  "updateId": "4d6ae169-744c-4680-8359-4a33e5227c0a",
  "expectedRevision": 0,
  "dueAt": "2026-09-28T16:00:00.000Z"
}
```

PUT accepts exactly these fields. updateId is a UUID, expectedRevision an integer >=0, dueAt a UTC timestamp or null. No client-supplied owner, course-content revision, progress, or time-zone offset field. The target unit is selected only by the path. Unknown fields are rejected.

Successful Response:

```json
{
  "success": true,
  "message": "Course schedule loaded.",
  "data": {
    "schedule": {
      "courseId": "530f6e99-eef1-4b74-828a-faa79c3df4ba",
      "revision": 0,
      "updatedAt": null,
      "units": [
        {
          "moduleId": "c0c909c6-c286-41cc-8206-f5a39d9d1818",
          "moduleTitle": "Getting Started",
          "modulePosition": 1,
          "unitId": "a91a0502-2e8d-47f1-8e32-e2b25c196489",
          "title": "Welcome",
          "position": 1,
          "type": "VIDEO",
          "dueAt": null
        },
        {
          "moduleId": "c0c909c6-c286-41cc-8206-f5a39d9d1818",
          "moduleTitle": "Getting Started",
          "modulePosition": 1,
          "unitId": "7a610f1a-8760-4aa5-b3cc-ab01118d1237",
          "title": "Knowledge Check",
          "position": 2,
          "type": "QUIZ",
          "dueAt": null
        }
      ]
    }
  }
}
```

GET returns HTTP 200 for both roles, with exactly data={schedule}. PUT returns HTTP 200:

```json
{
  "success": true,
  "message": "Learning deadline saved.",
  "data": {
    "schedule": {
      "courseId": "530f6e99-eef1-4b74-828a-faa79c3df4ba",
      "revision": 1,
      "updatedAt": "2026-09-21T10:00:00.000Z",
      "units": [
        {
          "moduleId": "c0c909c6-c286-41cc-8206-f5a39d9d1818",
          "moduleTitle": "Getting Started",
          "modulePosition": 1,
          "unitId": "a91a0502-2e8d-47f1-8e32-e2b25c196489",
          "title": "Welcome",
          "position": 1,
          "type": "VIDEO",
          "dueAt": null
        },
        {
          "moduleId": "c0c909c6-c286-41cc-8206-f5a39d9d1818",
          "moduleTitle": "Getting Started",
          "modulePosition": 1,
          "unitId": "7a610f1a-8760-4aa5-b3cc-ab01118d1237",
          "title": "Knowledge Check",
          "position": 2,
          "type": "QUIZ",
          "dueAt": "2026-09-28T16:00:00.000Z"
        }
      ]
    },
    "receipt": {
      "updateId": "4d6ae169-744c-4680-8359-4a33e5227c0a",
      "appliedRevision": 1,
      "replayed": false
    }
  }
}
```

- schedule has exactly courseId, revision, updatedAt, and units. revision is a nonnegative integer; updatedAt is null before any schedule mutation and otherwise the last accepted new change time in UTC.
- units contains every required unit, at most 200, ordered by modulePosition then position. Each item has exactly the shown keys: moduleId, moduleTitle, modulePosition, unitId, title, position, type, dueAt. Positions are positive one-based integers; dueAt is nullable. There are no answer keys, account details, media URLs, or Student progress fields.
- receipt has exactly updateId, appliedRevision, replayed. Replays expose the current schedule, which can have a later revision than appliedRevision. Do not roll back the client to the old submitted value.
- UC-05's existing upcomingTasks reads the matching schedule entry: incomplete units with non-null dueAt, ordered dueAt ascending then unitId ascending, maximum four, including overdue entries. Other Student endpoints retain their existing JSON shapes.
- Existing fixture dueAt values are imported once into initial schedule entries with revision=0 and updatedAt=null, preserving their dates. Thereafter the schedule is the only dueAt source. Do not re-import fixtures over an Instructor change.

Error Response:

```json
{
  "success": false,
  "statusCode": 409,
  "code": "SCHEDULE_REVISION_CONFLICT",
  "message": "This schedule changed. Reload it before saving again.",
  "timestamp": "2026-09-21T10:00:00.000Z",
  "path": "/api/v1/instructor/courses/530f6e99-eef1-4b74-828a-faa79c3df4ba/schedule/units/7a610f1a-8760-4aa5-b3cc-ab01118d1237"
}
```

All errors contain success=false, statusCode matching the HTTP status, code, message, a server UTC ISO 8601 timestamp, and the actual request pathname without query. Omit data. Only VALIDATION_ERROR may add errors, mapping field paths to nonempty arrays of strings. All success fields described below are required unless explicitly nullable. IDs and timestamps in examples are illustrative.

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | Please sign in to continue. |
| 403 | ROLE_NOT_ALLOWED | This action is not available for your account role. |
| 403 | ONBOARDING_REQUIRED | Complete your learning profile to continue. |
| 404 | SCHEDULE_NOT_AVAILABLE | This course schedule is not available. |
| 404 | ENROLLED_COURSE_NOT_AVAILABLE | This assigned course is not available. |
| 409 | COURSE_NOT_PUBLISHED | Publish this course before managing its schedule. |
| 409 | SCHEDULE_REVISION_CONFLICT | This schedule changed. Reload it before saving again. |
| 409 | REQUEST_CONFLICT | This request identifier was already used for different content. |
| 503 | SCHEDULE_UNAVAILABLE | Course scheduling is temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

ONBOARDING_REQUIRED applies only to Student reads. Route by error code and confirmed role, not every 403 to onboarding. Invalid dueAt uses VALIDATION_ERROR with an errors.dueAt entry; unknown query/body fields use the corresponding field path.

## Project-Specific Implementation Context

### Backend Implementation Context

Use NestJS/TypeScript and a separate course schedule revision with unit-to-date entries. Do not increment UC-17 Course.revision or alter UC-18 published content when a deadline changes. Update one schedule entry, its revision/time, and replay association as one coherent operation. Serialize concurrent mutations against the schedule revision. Use the same schedule source in Instructor, Student, and dashboard reads.

### Frontend UI Context

Implement the supplementary schedule pages with React, TypeScript, and Tailwind. Label time inputs as UTC and show the full date/time before save. Use date plus time inputs with clear removal controls; do not rely solely on color to indicate a due date. Show submission feedback beside the edited unit and preserve local input after rejection.

### Frontend Logic and API Context

Track saved schedule revision separately from local edits. Allow one pending unit mutation per view, then use the returned complete schedule as the new baseline. Exact replay confirms its appliedRevision while showing any later current schedule. Refresh UC-05 and schedule caches after confirmed change. Use UC-15 save/discard/stay behavior on leaving a dirty Instructor form.

### Validation and Error-Handling Context

Validate date syntax, calendar validity, membership, role, published state, revision, and future-date rules at the server. Browser clocks provide convenience feedback only. A deadline is not an attempt expiry, grade rule, or completion event. Display unknown outcomes honestly and never reset Student state to resolve a scheduling conflict.
