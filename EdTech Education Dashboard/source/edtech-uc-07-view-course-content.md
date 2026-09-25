# UC-07: View Course Modules and Learning Content

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

View Course Modules and Learning Content

Description:

- Lets an enrolled Student inspect a module's ordered video lessons and quizzes and open a learning unit.
- Enables UC-06's Start/Resume/View module actions and provides a shared learning shell for UC-08 video and UC-09 quiz.
- Curriculum ordering, read contracts, route behavior, and the normalization of sample content are project requirements. Figma supports the course-material screen; no Technical Report or backend behavior is inferred from it.

Primary Actor:

Authenticated, onboarded Student enrolled in the selected course.

Preconditions:

- UC-01–06 identity, enrollment, catalogue, and unit-weighted progress definitions are in place.
- Course curricula are fixed during the experiment and contain ordered modules, each with at least one required VIDEO or QUIZ unit. There are no optional units or prerequisite locks in this baseline.
- Implement `/student/courses/:courseId/modules/:moduleId` and the learning-unit dispatcher `/student/courses/:courseId/units/:unitId`. All IDs are stable UUIDs.

Postconditions:

- Success: The Student sees the correct enrolled course, module list, unit types/durations/statuses, and available navigation.
- Failure: Inaccessible course content is not exposed; an actionable retry or return to My Courses is shown.
- Reading, expanding, or navigating never writes startedAt, completion, quiz attempts, or learning time.

Main Flow:

1. A UC-06 module Start/Resume/View action opens its module route; all three labels open the overview, not an implicit progress mutation.
2. Load the curriculum overview using courseId and the selected moduleId.
3. Render the course sidebar, selected module heading, actual video/quiz counts, and unit cards in position order.
4. The Student selects another module or opens a unit. Module selection updates the URL; Open navigates to the unit dispatcher using the returned type and ID.
5. VIDEO renders UC-08; QUIZ renders UC-09's overview. Until each respective UC is installed, its Open action is disabled with a clear explanation.
6. Previous/Next on a learning unit follows the flattened module-position then unit-position ordering. A missing previous/next is disabled; the final unit also offers Back to course, returning to its module overview.
7. Return to My Courses opens `/student/my-courses?courseId=<id>`, preserving course context.

Alternative Flow:

A.1 — Shared sidebar and direct links

- The same curriculum endpoint supports direct learning-unit URLs: omit moduleId, load the ordered curriculum, and resolve the requested unit's containing module. Then load the unit-specific API. A unit outside the returned curriculum is unavailable.
- Sidebar completion icons come from persisted unit status. A previously completed unit remains readable; no reset occurs when revisited.
- Grades lists this course's quiz titles and links to their UC-09 overview/results. It is a navigation group, not a separate grading endpoint or invented transcript. Disable it until UC-09 is integrated.

A.2 — Resume behavior

- On a module overview, an optional Continue learning action opens the first IN_PROGRESS unit by unit position, otherwise the first NOT_STARTED unit, otherwise the first unit for review. This is a project supplement, not a new use case.
- Reading an IN_PROGRESS quiz never creates another attempt; UC-09 resumes the existing one. Viewing a video uses UC-08's saved resume position.
- Units may be opened in any order. Do not add hidden lesson locks or require a passing quiz to unlock the next module; quiz passing controls completion only.

A.3 — Source data normalization

- Preserve UC-06's example curriculum cardinality: three modules, three required units per module. The displayed first module uses two videos and one quiz, rather than copying the source's three-video/one-quiz sample and silently changing the nine-unit progress denominator.
- Example first-module durations: 420-second video, 600-second video, 1200-second quiz. Its displayed scheduled content total is 2220 seconds, 37 minutes; video-only duration is 17 minutes. Label which total is displayed.
- CourseCard durationSeconds=25200 from UC-04–06 remains planned study duration including practice, not a claim that media playback sums to seven hours. Media/quiz durations and planned study duration are distinct labelled quantities.
- Unit quiz duration must agree with UC-09's 20-minute attempt limit in all screens. The source's 10-minute quiz label is corrected.

A.4 — Goal tracker

- Retain the weekly-goal card location with `Weekly learning goals are not configured yet.` and a disabled Edit Goal action until a goal-setting UC exists. UC-03 collected motivations, not weekly target hours or study days.
- Do not fabricate weekday activity ticks or copy the source's external-platform name. This feature does not calculate weeklyGoalPercent or measured learningSeconds.

Exception Flow:

E.1 — Missing enrollment/content

- Missing enrollment, wrong course-module/unit relationship, or absent content yields generic LEARNING_CONTENT_NOT_AVAILABLE. Offer My Courses; never fall back to a public catalogue preview as proof of access.

E.2 — Inconsistent or unavailable curriculum

- Missing required units, duplicate positions, invalid unit types, or progress inconsistent with UC-05/06 returns COURSE_CONTENT_UNAVAILABLE. Do not fill missing curriculum with source placeholders.
- A failed read keeps the current route with Retry. Ignore old responses on course/account change. A service outage is distinct from an empty catalogue; an assigned curriculum cannot be empty.

UI Integration:

- `14 Courses Detail`, node `222:1030`.
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-1030
- Live context/screenshot inspected on 2026-09-20. Preserve course sidebar, module selection, unit cards, yellow Open actions, and goal-card placement. Use real titles and counts.
- Correct sample count/duration inconsistencies as specified above. Continue learning, return navigation, deferred-feature text, and error states are supplements. No mobile frame or frozen dataset is claimed.

API Endpoint:

`GET /api/v1/student/courses/:courseId/content`

Request Body:

No body. Accept only optional moduleId UUID query, at most once. Unknown/repeated keys are VALIDATION_ERROR. If omitted, selectedModuleId is the first module's ID; if supplied it must belong to this course, otherwise generic 404. CourseId is a UUID; the session determines enrollment.

Successful Response:

```json
{
  "success": true,
  "message": "Course content retrieved.",
  "data": {
    "courseId": "ba22825a-9acf-4d85-af5f-5c77f83d6ac7",
    "courseTitle": "Introduction to Python Programming",
    "plannedStudySeconds": 25200,
    "selectedModuleId": "a2617ef9-814d-446c-a1b7-5ab37d6c2079",
    "modules": [
      {
        "id": "a2617ef9-814d-446c-a1b7-5ab37d6c2079",
        "title": "Python Fundamentals",
        "position": 1,
        "status": "IN_PROGRESS",
        "progressPercent": 33,
        "units": [
          {
            "id": "af79a45f-d04a-4c78-b5be-30cac0e3d161",
            "title": "Installing Python & VS Code",
            "position": 1,
            "type": "VIDEO",
            "durationSeconds": 420,
            "status": "COMPLETED"
          },
          {
            "id": "c4a6a2e8-5a40-4ccf-981b-ffcafed00b5e",
            "title": "Hello World & Basic Syntax",
            "position": 2,
            "type": "VIDEO",
            "durationSeconds": 600,
            "status": "NOT_STARTED"
          },
          {
            "id": "4be1f7da-a5da-46f2-9ac8-28e5dca03ae2",
            "title": "Quiz: Python Basics",
            "position": 3,
            "type": "QUIZ",
            "durationSeconds": 1200,
            "status": "NOT_STARTED"
          }
        ]
      },
      {
        "id": "e52ecb1f-ff0b-43c3-82bc-c2b5df930e4a",
        "title": "Control Flow in Python",
        "position": 2,
        "status": "IN_PROGRESS",
        "progressPercent": 33,
        "units": [
          {
            "id": "6d47e5f8-c145-4a24-9726-88a19fb0c3a4",
            "title": "Conditions and Branching",
            "position": 1,
            "type": "VIDEO",
            "durationSeconds": 420,
            "status": "COMPLETED"
          },
          {
            "id": "893fc013-dd8f-4db5-9f40-7d6b92993df2",
            "title": "Loops",
            "position": 2,
            "type": "VIDEO",
            "durationSeconds": 600,
            "status": "NOT_STARTED"
          },
          {
            "id": "6db1e670-3a8d-4a73-8093-a888e7ce6640",
            "title": "Quiz: Control Flow",
            "position": 3,
            "type": "QUIZ",
            "durationSeconds": 1200,
            "status": "NOT_STARTED"
          }
        ]
      },
      {
        "id": "97b152cd-0456-40b5-87fb-e0a0cfa92f2f",
        "title": "Build a Simple App",
        "position": 3,
        "status": "IN_PROGRESS",
        "progressPercent": 33,
        "units": [
          {
            "id": "e0e5a9b4-6f10-42cc-b472-5d1142e076ca",
            "title": "Planning a Simple App",
            "position": 1,
            "type": "VIDEO",
            "durationSeconds": 420,
            "status": "COMPLETED"
          },
          {
            "id": "baea916e-202a-4d25-b170-c9c613f62d05",
            "title": "Implementing the App",
            "position": 2,
            "type": "VIDEO",
            "durationSeconds": 600,
            "status": "NOT_STARTED"
          },
          {
            "id": "8b3d3ae1-3ffb-4ce6-b690-226d0fc3e9aa",
            "title": "Quiz: Simple App Concepts",
            "position": 3,
            "type": "QUIZ",
            "durationSeconds": 1200,
            "status": "NOT_STARTED"
          }
        ]
      }
    ]
  }
}
```

- HTTP 200. All shown fields required. modules is a nonempty array; the example returns all three modules from UC-06 in positions 1–3. Each has one completed unit out of three, consistent with the shared 33% course-progress example.
- Each module has exactly id UUID, title nonempty string, position positive consecutive integer, status NOT_STARTED|IN_PROGRESS|COMPLETED, progressPercent integer 0–100, and units nonempty array. Unit objects have exactly id, title, position, type VIDEO|QUIZ, durationSeconds positive integer, and status from the same vocabulary. Unit positions are consecutive within their module.
- Video durationSeconds is its configured media duration. Quiz durationSeconds is its attempt limit. Unit status is from persisted start/completion state, not a viewed flag. Module/course aggregation follows UC-05/06.
- selectedModuleId always identifies one returned module. Responses expose no video URL, correct answer, private learner identity, or mutation capability. All modules/units reflect one coherent read.

Error Response:

```json
{
  "success": false,
  "statusCode": 503,
  "code": "COURSE_CONTENT_UNAVAILABLE",
  "message": "Course content is temporarily unavailable. Please try again later.",
  "timestamp": "2026-09-20T10:00:00.000Z",
  "path": "/api/v1/student/courses/ba22825a-9acf-4d85-af5f-5c77f83d6ac7/content"
}
```

Use the shared envelope from UC-01–06: success=false, statusCode matching HTTP status, code, message, server ISO UTC timestamp, and actual pathname without query. Omit data. Only VALIDATION_ERROR may add errors mapping input paths to nonempty arrays of strings. All shown success keys are required; dates and IDs are examples, not fixed response values.

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | You must sign in to continue. |
| 403 | ONBOARDING_REQUIRED | Complete your learning profile to continue. |
| 404 | LEARNING_CONTENT_NOT_AVAILABLE | This learning content is not available. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

Every endpoint requires an ACTIVE, verified STUDENT session, completed onboarding, and current account enrollment in the requested course. The unit/module must belong to that course. Use the same generic 404 for missing content, wrong nesting/type, or missing enrollment. Malformed UUIDs are 400. 401 clears private state and opens `/sign-in`; 403 opens `/student/onboarding`; service failure is not logout. No query/body field may select another account. These UCs add no new rate-limit policy.

| HTTP | Code | Exact message |
| --- | --- | --- |
| 503 | COURSE_CONTENT_UNAVAILABLE | Course content is temporarily unavailable. Please try again later. |

## Project-Specific Implementation Context

### Backend Implementation Context

Implement the enrolled-course curriculum projection in NestJS/TypeScript using the same fixed module/unit identities and progress records as UC-05/06. Enforce enrollment and nesting for every read, not only UI navigation. Return all modules for sidebar ordering with the selected module ID. This endpoint never creates an attempt, tracks viewing, or updates progress.

### Frontend UI Context

Implement the course/module shell in React/TypeScript/Tailwind from the inspected frame. Reuse it for UC-08/09 unit pages where applicable. Connect UC-06's module actions, render dynamic counts, and retain a truthful unavailable goal-card state. Do not add a separate project-planning or certificate feature.

### Frontend Logic and API Context

Resolve modules and units from the returned curriculum, route by actual type, and compute previous/next navigation from stable positions. Reload progress when returning from UC-08/09 confirmed mutations. Preserve course context for My Courses navigation and discard responses from a previous account/course.

### Validation and Error-Handling Context

Validate IDs, nesting, query shape, and required curriculum coherence. Distinguish content unavailability from service failure and deferred integrations. No navigation action marks a unit complete or reassigns enrollment. Course planned hours and actual media duration must not be displayed as the same metric.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
