# UC-06: View Assigned Courses and Module Progress

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

View Assigned Courses and Module Progress

Description:

- Lets a Student find their assigned courses, filter/sort the collection, expand module progress, and select a module for learning when its destination is implemented.
- Implements My Courses without conflating catalogue discovery with course access. Uses UC-04 CourseCard and UC-05 progress rules.
- Assignment fixtures, query contracts, and deferred learning navigation are project decisions. This UC is not enrollment, course purchasing, lesson playback, or certificate generation.

Primary Actor:

Authenticated Student with completed onboarding.

Preconditions:

- UC-01–03 identity/session/onboarding and the common UC-04 catalogue exist.
- Register `/student/my-courses` with reload support. Designated research accounts may have explicit enrollment rows; new accounts have none.
- Enrollment joins an account to one fixed published curriculum with ordered modules and required units. No request in this UC creates or changes that association.

Postconditions:

- Success: The Student sees only their assigned courses, accurate status/counts, and ordered module progress; a legitimate empty collection is supported.
- Failure: No other Student's enrollment or inaccessible course detail is shown. A failed read changes no learning record.
- Expanding, filtering, or selecting a module does not mark it started or completed.

Main Flow:

1. The Student opens My Courses directly, from UC-04, or through a UC-05 course action.
2. Load the enrolled-course list, status counts, and enrolled category options using the declared query.
3. Render course rows with title, module count, planned duration, and completion state. The Student may change status/category/sort or move between pages.
4. Expanding a course fetches its account-scoped module progress and renders modules in curriculum order.
5. Each module shows Not Started, progress, or completed state with the source's Start, Resume, or View label.
6. Until the module-learning UC supplies its destination, these buttons are disabled with `Lesson access will be available in the course-learning feature.` Once that UC is integrated, bind its verified route without changing this read contract.
7. A completed course may show the completion banner, while certificate View and Add to LinkedIn remain disabled until a certificate UC exists.

Alternative Flow:

A.1 — Filters, sort, and paging

- status is ALL, NOT_STARTED, IN_PROGRESS, or COMPLETED; default ALL. category is one of the current account's enrolled category IDs. Sort is recent, title, or progress; default recent.
- recent sorts by lastActivityAt descending with nulls last, then assignedAt descending/course.id ascending. title uses case-insensitive title ascending then course.id ascending. progress uses progressPercent descending then title/course.id ascending.
- Changing status/category/sort resets page 1 and closes any expanded course. Browser Back restores query state. Status and category filters combine using AND.
- Fixed pageSize=6. Empty filtered results offer Clear filters; no enrollments offers Browse courses linking to `/student/home`, without implying a self-enrollment capability.

A.2 — Course deep link

- `/student/my-courses?courseId=<uuid>` loads the requested assigned course independently of the current list page and expands it in a clearly labelled Selected course panel above the list.
- The panel may contain a course outside the current filter/page. Do not change counts or pretend it belongs to the filtered rows. If also present in the list, show one expanded detail instance only.
- Removing the selection removes only courseId. Unknown/unassigned IDs show `This assigned course is not available.` at panel level; do not disclose whether another Student owns it. The list remains usable.

A.3 — Progress and completed courses

- Follow UC-05's unit-weighted progress/status definitions exactly. A module may be IN_PROGRESS with 0% when a unit has started but none has completed.
- COMPLETED requires all required units complete; never round 99% to completed. Course progress uses all required units, not a simple module average.
- Expand/collapse, card visits, and Start/Resume button clicks are not proof of learning activity. No progress-writing endpoint is introduced here.
- Completed courses remain readable. The completion banner is independent of certificate availability and does not claim a certificate has been issued.

Exception Flow:

E.1 — Invalid query or inaccessible course

- Malformed IDs, unknown/repeated parameters, invalid enums/page, or category outside enrolledCategories returns VALIDATION_ERROR. category omission remains valid for an empty enrollment collection.
- Detail for unknown/unassigned course returns the same 404 ENROLLED_COURSE_NOT_AVAILABLE. Course discovery visibility does not satisfy this endpoint's enrollment requirement.

E.2 — Read or consistency failure

- A broken required curriculum/progress record returns MY_COURSES_UNAVAILABLE, not fabricated modules or zero totals. A failed course expansion has its own retry while loaded list rows remain usable.
- Ignore obsolete list/detail responses after account/query changes. Do not carry expanded private data into another session.
- A missing image uses an accessible placeholder. It does not invalidate the enrollment.

UI Integration:

- `13 My Courses`, node `222:1174`.
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-1174
- Live context/screenshot inspected on 2026-09-20. Preserve Sort/Category controls, status chips with counts, expandable courses, module progress bars, Start/Resume/View labels, and completion banner.
- Sort options, pagination, selected-course deep-link panel, empty/error/loading feedback, and unavailable-feature explanations are supplements. No mobile or frozen dataset claim.
- Source completion percentages and certificate text must not be copied as account facts. Keep displayed hours consistent with durationSeconds and round to one decimal hour when necessary.

API Endpoint:

- `GET /api/v1/student/my-courses`
- `GET /api/v1/student/my-courses/:courseId`

Request Body:

No bodies. List queries: status (ALL|NOT_STARTED|IN_PROGRESS|COMPLETED, default ALL), category (optional enrolled category ID), sort (recent|title|progress, default recent), page (decimal integer 1–1000000, default 1). Fixed pageSize=6. Reject duplicate/unknown keys.

Detail courseId must be a UUID and accepts no query. Browser route additionally accepts courseId for its selected-course panel; do not forward that key to the list API. Filters do not identify the Student; the session does.

Successful Response:

```json
{
  "success": true,
  "message": "Assigned courses retrieved.",
  "data": {
    "items": [
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
        "moduleCount": 3,
        "status": "IN_PROGRESS",
        "progressPercent": 33,
        "assignedAt": "2026-09-18T10:00:00.000Z",
        "lastActivityAt": "2026-09-20T09:00:00.000Z",
        "completedAt": null
      }
    ],
    "statusCounts": {
      "ALL": 1,
      "NOT_STARTED": 0,
      "IN_PROGRESS": 1,
      "COMPLETED": 0
    },
    "enrolledCategories": [
      {
        "id": "web-development",
        "name": "Web Development"
      }
    ],
    "page": 1,
    "pageSize": 6,
    "totalItems": 1,
    "totalPages": 1
  }
}
```

```json
{
  "success": true,
  "message": "Assigned course retrieved.",
  "data": {
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
    "status": "IN_PROGRESS",
    "progressPercent": 33,
    "assignedAt": "2026-09-18T10:00:00.000Z",
    "lastActivityAt": "2026-09-20T09:00:00.000Z",
    "completedAt": null,
    "modules": [
      {
        "id": "a2617ef9-814d-446c-a1b7-5ab37d6c2079",
        "title": "Python Fundamentals",
        "position": 1,
        "requiredUnitCount": 3,
        "completedUnitCount": 1,
        "progressPercent": 33,
        "status": "IN_PROGRESS"
      },
      {
        "id": "e52ecb1f-ff0b-43c3-82bc-c2b5df930e4a",
        "title": "Control Flow in Python",
        "position": 2,
        "requiredUnitCount": 3,
        "completedUnitCount": 1,
        "progressPercent": 33,
        "status": "IN_PROGRESS"
      },
      {
        "id": "97b152cd-0456-40b5-87fb-e0a0cfa92f2f",
        "title": "Build a Simple App",
        "position": 3,
        "requiredUnitCount": 3,
        "completedUnitCount": 1,
        "progressPercent": 33,
        "status": "IN_PROGRESS"
      }
    ]
  }
}
```

- Both endpoints return 200. CourseCard is exactly UC-04's shape. List entries contain exactly the shown course, moduleCount, status, progressPercent, assignedAt, lastActivityAt, and completedAt keys.
- moduleCount is a positive integer equal to the detail modules length. assignedAt is ISO UTC; lastActivityAt is ISO UTC or null for no activity; completedAt is ISO UTC if COMPLETED, otherwise null.
- Module objects have exactly id UUID, title nonempty string, position positive consecutive integer starting at 1, requiredUnitCount positive integer, completedUnitCount integer 0..requiredUnitCount, progressPercent integer 0..100, and status from the same three-state vocabulary. Module status derives from underlying started/completed units, not only its percentage.
- Detail modules are curriculum ordered and use the same total counts as the list projection. Detail exposes no video URLs, quiz answer keys, or private Instructor data.
- statusCounts applies the selected category but ignores the selected status and page. ALL equals the sum of the three statuses. enrolledCategories lists all categories present across the account's enrollments, ignoring current filters, in UC-04 catalogue order.
- totalItems applies both filters; totalPages=ceil(totalItems/6), zero when empty. Out-of-range page returns [] with actual counts. List rows/counts form a consistent snapshot. Detail is a later read and may reflect a subsequent legitimate learning update.
- The shared example course has three modules with three required units each, one completed unit per module, and course progress floor(100 * 3 / 9)=33%. Preview isEnrolled=false in UC-04 illustrates an unassigned viewer; UC-05/06 illustrate an assigned viewer. Deployed fixtures use one consistent curriculum and duration for this course ID.

Error Response:

```json
{
  "success": false,
  "statusCode": 503,
  "code": "MY_COURSES_UNAVAILABLE",
  "message": "Your assigned courses are temporarily unavailable. Please try again later.",
  "timestamp": "2026-09-20T10:00:00.000Z",
  "path": "/api/v1/student/my-courses"
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
| 404 | ENROLLED_COURSE_NOT_AVAILABLE | This assigned course is not available. |
| 503 | MY_COURSES_UNAVAILABLE | Your assigned courses are temporarily unavailable. Please try again later. |

## Project-Specific Implementation Context

### Backend Implementation Context

Implement list/detail in NestJS/TypeScript over account-scoped enrollment records and the same course/module/unit projections used by UC-04/05. Apply filters, sorting, counts, and access consistently. Research fixture assignments are explicit seed data, not hidden enrollment side effects. Validate fixed curricula at loading so an inconsistent module denominator does not produce plausible but wrong progress.

### Frontend UI Context

Implement MyCoursesPage in React/TypeScript/Tailwind using the source expandable course rows and module cards. Reuse shared navigation and progress presentation. Provide selected-course, loading, error, and empty states, with visibly disabled learning/certificate actions until their destinations are implemented.

### Frontend Logic and API Context

Keep filters/sort/page/courseId in the URL. Load list and selected detail independently, avoid duplicate expanded detail rendering, and fetch a course only when expanded or directly selected. Do not alter progress on navigation. UC-04 preview and UC-05 dashboard link to this route; the later course-learning UC owns module navigation and progress writes.

### Validation and Error-Handling Context

Reject malformed queries and inaccessible IDs without exposing another enrollment. Distinguish an empty collection from an unavailable data service and a missing image from missing curriculum. All progress calculations and labels use the shared unit definitions. Certificate, enrollment, and learning success must never be simulated by frontend state.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
