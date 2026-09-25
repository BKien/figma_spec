# UC-04: Discover Courses

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Discover Courses

Description:

- Lets an onboarded Student browse the learning catalogue, search by keyword, filter by category, and inspect a course summary before navigating to an assigned course.
- Implements the Home Student discovery screen. Course access is separate from discovery; viewing a card does not enroll the learner or make lesson content accessible.
- Contracts, catalogue/search behavior, preview panel, and deterministic ranking are project decisions. The Figma screens support the visual composition, not an existing backend contract or supplied Technical Report.

Primary Actor:

Authenticated Student with completed onboarding.

Preconditions:

- UC-01–03 authentication and onboarding are available. Register `/student/home` with reload support.
- Published course fixtures and local image assets exist. Instructor names are display metadata, not evidence that Instructor account provisioning has already been implemented.
- For this baseline, enrollment records are explicitly assigned in research fixtures to designated accounts. A newly registered account has no enrollments. Neither login, onboarding nor catalogue reads assign courses. A later enrollment/Instructor UC may introduce assignment writes.

Postconditions:

- Success: The Student sees real published catalogue results or an explicit empty state and can inspect the selected course summary.
- Failure: Invalid filters, unavailable service, and an unavailable course are distinguishable; no unrelated course or prior-account data is substituted.
- Course ownership, enrollment, learning progress, and account settings are unchanged.

Main Flow:

1. The Student opens Home. The frontend requests discovery sections and displays the welcome area, course groups, and categories.
2. Recommended, Trending, and New sections show up to three course cards each, with their declared See more destinations.
3. A search submission, category selection, or See more action opens a results view on the same route with query parameters.
4. The backend applies the declared filters and returns a page of published courses and consistent counts.
5. Selecting a card opens a supplementary course preview panel and loads its current public summary and enrollment availability.
6. If enrolled, Open my course navigates to `/student/my-courses?courseId=<id>` when UC-06 is integrated. If unassigned, show `This course is not assigned to your account.`; no fake enroll/purchase action is offered.

Alternative Flow:

A.1 — Home sections and ranking

- `recommended` ranks by the number of matches between course interestIds and UC-03's selected interestIds, then publishedAt descending, then id ascending. This is a declared deterministic rule, not an AI service.
- `trending` ranks published courses by current enrollment count descending, then publishedAt descending/id ascending. Counts are project records, not sample popularity claims.
- `newest` ranks by publishedAt descending/id ascending. An item can appear in more than one section. Exclude no item merely because the Student already has access.
- See more preserves the section as sort. Category selection applies category and starts page 1. Search applies q, retains current category/sort, and resets page 1.

A.2 — Results and preview

- Match q as a case-insensitive literal substring in title, description, or instructorName. Combine q/category using AND. Empty results retain filters and offer Clear filters.
- Results layout reuses existing cards; pagination and the preview panel are explicit UI additions. Browser Back restores filters/page. A courseId query opens a preview on reload without changing the underlying list filters.
- Closing preview removes only courseId. Unknown/unpublished course returns a panel-level not-found message while the list remains usable.
- Header Resume My Course opens UC-06's list, which owns Start/Resume behavior; it does not assume a particular enrollment exists. Until UC-06 is installed, disable the action with an explanation.

A.3 — Incomplete source features

- Home testimonials may display clearly authored static experiment content, but cannot be presented as verified user reviews. Omit the section if no curated content is supplied. Course rating fields are nullable fixture metadata; no rating submission is enabled.
- Newsletter, footer destinations, notification bell, My plan, social sharing, and undeclared profile/settings destinations remain disabled with an explanation until their own UCs exist. Home, Dashboard, and My Courses connect to UC-04/05/06 when installed.
- Do not implement payments, instructor publishing, or automatic enrollment from a catalogue card.

Exception Flow:

E.1 — Invalid query

- Unknown category, unsupported sort, duplicate/unknown query fields, malformed course UUID, or invalid page produces VALIDATION_ERROR. Offer an explicit reset instead of silently replacing the requested filter.

E.2 — Stale catalogue or service failure

- A removed/unpublished preview returns COURSE_NOT_AVAILABLE. An asset failure shows a labelled placeholder; it is not a catalogue outage.
- COURSE_CATALOG_UNAVAILABLE offers manual retry for the current query. Ignore older responses after query/account changes; do not let a failed new search display old results as if they matched.
- Home and preview requests fail independently. The same course may change enrollment availability between preview and UC-06; the latter rechecks account access.

UI Integration:

- `10 Home Student`, node `222:1888`, with menu variant `11 Home Menu Student`, node `231:822`.
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-1888
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=231-822
- Home live context/screenshot inspected on 2026-09-20. Preserve header search, welcome hero, Recommended/Trending/New course groups, category explorer, yellow actions, and shared footer.
- Results pagination, preview content, filter state, availability labels, and error/empty states are project supplements. No mobile screen or frozen dataset is claimed. Adapt the grid to available width without inventing extra features.
- Replace placeholder identity with the current account name. No fabricated review counts, prices, or enrollment-success notices.

API Endpoint:

- `GET /api/v1/student/course-discovery`
- `GET /api/v1/student/catalog/courses`
- `GET /api/v1/student/catalog/courses/:courseId`

Request Body:

No request bodies. Discovery and preview accept no API queries; courseId is a UUID.

Catalogue accepts q (trimmed text, 1–100 Unicode code points, blank treated as absent), category (known category ID), sort (recommended, trending, newest; default recommended), and page (decimal integer 1–1000000; default 1). Fixed pageSize=9. Reject unknown/repeated keys.

Browser `/student/home` uses the same query keys and optional courseId for the preview. Do not forward courseId to the list API. No query shows discovery home; any list query shows results. Clearing all filters returns to discovery home.

Successful Response:

```json
{
  "success": true,
  "message": "Course discovery retrieved.",
  "data": {
    "categories": [
      {
        "id": "web-development",
        "name": "Web Development",
        "description": "Build websites and web applications."
      }
    ],
    "recommended": [
      {
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
      }
    ],
    "trending": [
      {
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
      }
    ],
    "newest": [
      {
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
      }
    ]
  }
}
```

```json
{
  "success": true,
  "message": "Courses retrieved.",
  "data": {
    "items": [
      {
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
      }
    ],
    "page": 1,
    "pageSize": 9,
    "totalItems": 1,
    "totalPages": 1
  }
}
```

```json
{
  "success": true,
  "message": "Course preview retrieved.",
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
      "ratingCount": 0,
      "description": "Learn Python fundamentals through video lessons and quizzes.",
      "moduleCount": 3,
      "isEnrolled": false
    }
  }
}
```

- All endpoints return 200. CourseCard has exactly the keys shown: id UUID; title/instructorName/thumbnailAlt nonempty strings; thumbnailUrl nullable local or configured asset URL; categoryId from categories; level BEGINNER, INTERMEDIATE, or ADVANCED; durationSeconds positive integer; ratingCount nonnegative integer. ratingAverage is null when count=0, otherwise a number 0–5.
- Catalogue categories are fixed for this baseline: ui-ux-design, web-development, ai-machine-learning, business-marketing, finance-investing, personal-development, languages, education-teaching. Discovery returns all eight with display names/descriptions in that order; the one-entry example illustrates the element schema.
- Each course has one category and zero or more unique UC-03 interest IDs for ranking; these tags and publication/enrollment ranking fields are internal, not extra response fields. Course fixtures must have at least one module and one required video/quiz unit per module.
- Discovery arrays have 0–3 cards in ranked order. Preview adds exactly description (nonempty text), moduleCount (positive integer), isEnrolled (boolean for the current account). It exposes no lesson media, quiz answers, other students, or private Instructor data.
- Catalogue totalPages=ceil(totalItems/9), zero when empty. Out-of-range pages return empty items with actual counts. Rows and counts use a consistent read. Ranking is a live list, not a frozen pagination snapshot.

Error Response:

```json
{
  "success": false,
  "statusCode": 503,
  "code": "COURSE_CATALOG_UNAVAILABLE",
  "message": "Course discovery is temporarily unavailable. Please try again later.",
  "timestamp": "2026-09-20T10:00:00.000Z",
  "path": "/api/v1/student/catalog/courses"
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
| 404 | COURSE_NOT_AVAILABLE | This course is not available. |
| 503 | COURSE_CATALOG_UNAVAILABLE | Course discovery is temporarily unavailable. Please try again later. |

## Project-Specific Implementation Context

### Backend Implementation Context

Implement discovery, list, and preview in NestJS/TypeScript over a coherent published catalogue. CourseCard is shared by UC-05/06; use one projection rather than duplicating inconsistent labels or durations. Ranking uses UC-03 interests and actual fixture enrollment rows. Published discovery metadata and enrollment-controlled lesson content are separate access decisions. No new enrollment is created by these GET endpoints.

### Frontend UI Context

Implement StudentHomePage and its results/preview states in React/TypeScript/Tailwind. Reuse the source card and shell styles. Preview shows course title, instructor, category, level, duration, module count, description, and an explicit assigned/unassigned action state. This added panel is intentionally simple and must not masquerade as a supplied Figma frame.

### Frontend Logic and API Context

Keep query/page and preview ID in the URL; use local state only for an unsubmitted search draft. Load discovery categories to validate/display filters; preserve list navigation when opening/closing preview. If metadata fails, provide retry rather than substituting invented categories. Wire Dashboard/My Courses to their installed routes; guard all routes with UC-02 and UC-03 state.

### Validation and Error-Handling Context

Apply query bounds, exact category membership, UUID validity, account eligibility, and published visibility on the server. Render description as plain text. Distinguish no matches, removed course, unavailable catalogue, and asset failure. No result implies payment, assignment, or completed learning.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
