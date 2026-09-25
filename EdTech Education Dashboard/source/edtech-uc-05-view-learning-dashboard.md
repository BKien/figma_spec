# UC-05: View the Learning Dashboard

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

View the Learning Dashboard

Description:

- Gives the Student one account-scoped summary of enrolled-course progress, active/completed courses, upcoming learning units, and course suggestions.
- Replaces UC-02's dashboard integration shell at `/student/dashboard`, including the post-onboarding destination in UC-03.
- The dashboard is a read-only overview. Metric definitions, omitted source features, and response contracts are project decisions, not Figma-derived business rules.

Primary Actor:

Authenticated Student with completed onboarding.

Preconditions:

- UC-01–03 session/onboarding and UC-04 shared CourseCard/catalogue exist.
- Research fixtures may assign published courses to designated accounts. New accounts start with no enrollments; the dashboard never assigns any.
- Enrollment and unit-completion records follow the common rules below and UC-06. Actual learning writes belong to subsequent learning UCs.

Postconditions:

- Success: The Student sees a coherent summary of their own saved learning state, including a truthful empty state when nothing is assigned.
- Failure: No stale or fabricated metric is represented as current. Reading changes no progress, enrollment, goal, or session expiry.

Main Flow:

1. The authenticated, onboarded Student reaches `/student/dashboard` after sign-in/setup or via Dashboard navigation.
2. Request the dashboard resource and render loading independently of the shared navigation.
3. Display the account name, course-completion summary, available metrics, active courses, completed courses, and upcoming units.
4. Load recommendations independently through UC-04's discovery endpoint, using its recommended array.
5. Continue, a course card, or a learning-task action opens `/student/my-courses?courseId=<id>` through UC-06; it must not pretend to start or finish a unit.
6. See more for active/completed courses opens UC-06 with status=IN_PROGRESS or COMPLETED. See more recommendations opens UC-04 with sort=recommended.

Alternative Flow:

A.1 — Empty or not-yet-measured state

- With no enrollments, show `No courses have been assigned yet.` and Browse courses linking to `/student/home`. Render zero enrolled/completed counts and omit Continue.
- Display unavailable time/streak/goal metrics as Not available, not zero. A genuine measured zero may be shown only when the corresponding data source is available.
- Omit percentage-change badges: the source provides sample trends but no required comparison period or baseline. Do not infer them from fixture numbers.

A.2 — Common learning progress

- Each module contains a fixed ordered set of required units of type VIDEO or QUIZ. Each unit has one completed/not-completed outcome per enrollment, and a startedAt that may be null. Later learning UCs own how video completion and quiz completion are earned; these reads never infer them from opening a page.
- Module and course progress are floor(100 * completedRequiredUnits / totalRequiredUnits). A course uses unit totals across all modules, not an unweighted average of module percentages. All totals are positive.
- Status is COMPLETED only when all required units are complete; NOT_STARTED when no unit has started/completed; otherwise IN_PROGRESS. A started course can have 0% completion. Completed units must also have a nonnull startedAt in fixtures.
- Curriculum and enrollment membership remain fixed during an experimental run. Editing/versioning curriculum and revoking assignment belong to later Instructor rules; these UCs do not silently change denominators.

A.3 — Metrics and upcoming tasks

- Summary completionPercent=floor(100 * completedCourses / enrolledCourses), or 0 when enrolledCourses=0. Label it Across your assigned courses; replace the source's unsupported monthly-completion claim.
- coursesCompleted is all-time completed enrollment count. learningSeconds is all-time measured learning duration or null. streakDays is the number of consecutive UTC dates with measured learning activity ending today or yesterday, 0 if a working activity source has no such activity, otherwise null when unavailable.
- weeklyGoalPercent is floor(100 * measuredSecondsThisWeek / targetSeconds), capped at 100; null when target or activity measurement is unavailable. Week begins Monday 00:00 UTC. UC-03 does not set a weekly hours target. Until a later goal/activity UC exists, use null rather than inventing one.
- Upcoming tasks are incomplete required VIDEO/QUIZ units with configured dueAt; return up to four by dueAt ascending then unitId ascending, including overdue units. dueAt is nullable on the underlying unit; units without it are omitted here. Use absolute UTC due labels, not inconsistent Today/Tomorrow samples.
- No project-upload task, assignment submission form, certificate service, or review-writing feature is introduced. View Certificate is disabled with `Certificates are not available yet.` Pending learning actions are labelled Open course and go through UC-06.

A.4 — Independent sections

- Recommendation failure displays a section retry and does not erase a loaded dashboard. No recommendation result changes enrollment or progress.
- Until UC-06 is installed, course actions are disabled with a clear explanation; UC-04 Browse courses remains available. In the combined UC-04–06 baseline these links are enabled.

Exception Flow:

E.1 — Unavailable/inconsistent progress

- If a required course/module has no required units, counts contradict stored status, or an assigned course is missing, return DASHBOARD_UNAVAILABLE. Do not divide by zero, omit enrolled courses silently, or reuse source percentages.
- Optional media failures use a placeholder. Optional unavailable activity metrics use null and are not a whole-dashboard failure.

E.2 — Connection or identity change

- Show retry for a failed dashboard read; no automatic mutation follows. Ignore results from an earlier account or route. Session/onboarding handling follows the shared envelope below.
- When returning after an actual learning write in later UCs, refresh the dashboard; do not update counts just because Continue was clicked.

UI Integration:

- `12 Dashboard`, node `222:1374`.
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-1374
- Live context/screenshot inspected on 2026-09-20. Preserve welcome area, completion ring, four metric tiles, My Active Courses, Completed Courses, Upcoming Tasks / Deadlines, and Recommended Courses.
- Use the actual Student name and internally consistent progress. The source's 60% welcome summary, completed count, and course cards are illustrations, not data requirements.
- Null/empty/error states, corrected metric captions, and course-level navigation are supplements. Source certificate and upload actions remain deferred. No mobile or frozen dataset claim.

API Endpoint:

`GET /api/v1/student/dashboard`

Recommendations reuse `GET /api/v1/student/course-discovery` from UC-04; do not add a second ranking contract.

Request Body:

No body or query parameters. Reject extra input. The UC-02 session selects the account; clients cannot request another Student by ID.

Successful Response:

```json
{
  "success": true,
  "message": "Learning dashboard retrieved.",
  "data": {
    "asOf": "2026-09-20T10:00:00.000Z",
    "studentName": "Alex Nguyen",
    "summary": {
      "enrolledCourses": 1,
      "completedCourses": 0,
      "completionPercent": 0
    },
    "metrics": {
      "coursesCompleted": 0,
      "learningSeconds": null,
      "streakDays": null,
      "weeklyGoalPercent": null
    },
    "continueCourseId": "ba22825a-9acf-4d85-af5f-5c77f83d6ac7",
    "activeCourses": [
      {
        "course": {
          "id": "ba22825a-9acf-4d85-af5f-5c77f83d6ac7",
          "title": "Introduction to Python Programming",
          "thumbnailUrl": "/images/courses/python.jpg",
          "thumbnailAlt": "Python programming course",
          "instructorName": "Alex Morgan",
          "categoryId": "web-development",
          "level": "BEGINNER",
          "durationSeconds": 25200,
          "ratingAverage": null,
          "ratingCount": 0
        },
        "progressPercent": 33
      }
    ],
    "completedCourses": [],
    "upcomingTasks": []
  }
}
```

- HTTP 200. asOf is server ISO UTC; studentName is the persisted fullName. All counts/durations are nonnegative integers; percentages 0–100; the three optional metrics accept null as defined above.
- activeCourses contains up to three IN_PROGRESS enrollments ordered by lastActivityAt descending, then course.id ascending. Each item is exactly {course: CourseCard, progressPercent}. lastActivityAt is the most recent stored learning activity, not the most recent dashboard view.
- completedCourses contains up to three items ordered by completedAt descending/course.id ascending; exact shape {course: CourseCard, completedAt: ISO UTC}. Never substitute enrollment creation time for completedAt.
- continueCourseId is the first active course ID, otherwise the oldest NOT_STARTED enrollment by assignedAt/id, otherwise null. The frontend changes Continue to Start learning for a not-started destination; its underlying action remains Open course until actual unit navigation is implemented.
- upcomingTasks is an array of {unitId: UUID, courseId: UUID, courseTitle: string, title: string, type: VIDEO|QUIZ, dueAt: ISO UTC}. These values refer to the same account's enrollments. No unit media or answer key is included.
- All summary and course/task sections use a consistent account snapshot. Summary counts include every enrollment, even when only three cards are displayed. Recommendation data is separate and may have a later read time.

Error Response:

```json
{
  "success": false,
  "statusCode": 503,
  "code": "DASHBOARD_UNAVAILABLE",
  "message": "Your learning dashboard is temporarily unavailable. Please try again later.",
  "timestamp": "2026-09-20T10:00:00.000Z",
  "path": "/api/v1/student/dashboard"
}
```

Use UC-01–03's envelope: success=false, statusCode equal to HTTP status, code, message, server ISO UTC timestamp, and actual pathname without query. Omit data. Only VALIDATION_ERROR may add errors mapping input names to nonempty arrays of strings. All success keys are required; examples are illustrative values, not fixed runtime output.

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | You must sign in to continue. |
| 403 | ONBOARDING_REQUIRED | Complete your learning profile to continue. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

All endpoints require UC-02's valid ACTIVE, verified STUDENT session and completed UC-03 onboarding. 401 clears private state and opens `/sign-in`; 403 opens `/student/onboarding`. A service failure does not imply logout. GET requests never create enrollments or learning progress.

| HTTP | Code | Exact message |
| --- | --- | --- |
| 503 | DASHBOARD_UNAVAILABLE | Your learning dashboard is temporarily unavailable. Please try again later. |

Recommendation errors retain UC-04's contract and request path.

## Project-Specific Implementation Context

### Backend Implementation Context

Build the account-scoped NestJS dashboard read using common enrollment/unit data shared with UC-06. Follow the declared unit-weighted aggregation, status, due-date, and ordering rules. Use published fixed curricula and explicit fixture assignments during the experiment. Treat optional unavailable measurements differently from a broken required progress record. No tracking write occurs from viewing the dashboard.

### Frontend UI Context

Replace the existing dashboard shell with the inspected React/TypeScript/Tailwind composition. Render real empty states and Not available for unsupported metrics. Keep upcoming task labels truthful and certificate actions disabled. Use the shared CourseCard presentation with a progress overlay for active courses.

### Frontend Logic and API Context

Load dashboard and UC-04 recommendations independently after the same session/onboarding guard. Route course actions to UC-06 and discovery actions to UC-04. Refresh on route entry and after later completed learning operations; discard obsolete requests. Do not mutate local completion records on navigation clicks.

### Validation and Error-Handling Context

Validate empty input, current Student eligibility, enrollment isolation, positive unit totals, and metric consistency. Never present a source placeholder as measured progress or explain a service failure as zero activity. No Instructor/admin statistics are added to the Student dashboard.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
