# UC-21: Rate a Completed Course

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Rate a Completed Course

Description:

- Allows an enrolled Student who completed a course to submit or change one integer rating from one to five stars.
- Gives UC-04–06 CourseCard.ratingAverage/ratingCount a defined source in learner submissions. It explicitly replaces UC-04's fixture-only rating metadata when this UC is enabled.
- A star rating is the full scope: no public written reviews, reviewer directory, testimonial conversion, moderation workflow, or Instructor score editing.
- The rating form is a project-designed extension. Existing Figma course-card ratings support the display concept, not submission eligibility or backend behavior.

Primary Actor:

Authenticated ACTIVE, verified STUDENT with completed onboarding and an enrollment in the published course.

Preconditions:

- UC-05–09 calculate real course completion from required units. Eligibility requires COMPLETED, not a client-supplied percent or simply opening the final lesson.
- UC-04–06 share the same CourseCard projection; UC-18 supplies published courses and assignments.
- Under this extension, initialize rating data from actual rating records only. Standalone legacy fixture averages/counts are not mixed into live totals. A course with no rating records displays count=0 and average=null.

Postconditions:

- Success: One current rating exists for the Student/course pair. Editing it changes the aggregate sum but not the count of raters. Subsequent course-card reads reflect the committed aggregate.
- Failure: No rating or aggregate change on rejection. An uncertain response is reconciled before another mutation.
- Rating never changes course completion, progress, quiz score, lastActivityAt, enrollment, or published curriculum.

Main Flow:

1. The Student opens a completed course's UC-06 detail panel and selects Rate course.
2. Open `/student/courses/:courseId/rating` and read eligibility, the Student's existing rating, and the current course summary.
3. Select one of five labelled star values. Display the numerical choice and require an explicit Save rating action.
4. Submit value, expectedRevision, and updateId. The server rechecks session, enrollment, and canonical completion.
5. Create or update the single current rating and aggregate as one coherent result; return the current representation and mutation receipt.
6. Display `Course rating saved.`, refresh the course-card summary, and allow Return to my course or a later explicit edit.

Alternative Flow:

A.1 — Course not completed

- GET still returns the enrolled Student's rating resource with eligibility=COURSE_NOT_COMPLETED and myRating=null. Disable Save and explain `Complete this course before rating it.` Provide a link back to the UC-07 course content through its implemented route.
- An incomplete Student who bypasses the UI and submits receives COURSE_NOT_COMPLETED. No zero-star placeholder record is created.

A.2 — Edit a previous rating

- Prefill the stored value. Submit its current revision; replace the existing value and increment revision. One Student contributes exactly one value regardless of how many edits they make.
- Submitting the same value with a new valid request is accepted, advances revision/updatedAt once, and leaves count/average unchanged. No delete-rating action is specified.

A.3 — Replay or competing tabs

- Retain exact accepted updateId/payload associations for 24 hours, scoped to Student/course. Exact retries return HTTP 200 with current resource and original appliedRevision, replayed=true, without another aggregate update.
- Recheck current account eligibility and enrollment before returning a receipt. A recognized replay is resolved before expectedRevision validation. Different payload reuse returns REQUEST_CONFLICT.
- A new stale-revision request returns RATING_REVISION_CONFLICT, including the race where two tabs both try to create with expectedRevision=0. Offer Reload my rating and preserve the local proposed value for explicit reconciliation.
- After receipt expiry, reread before issuing another mutation. Course/Student uniqueness still prevents a second rating record.

A.4 — Catalog visibility

- Other Students and course owners see only aggregate rating through existing CourseCard fields. This UC exposes no individual rating list or author names to others.
- Existing ratings remain in the aggregate if their author later becomes inactive; account status changes do not rewrite the history of feedback. The inactive author cannot edit while ineligible.

Exception Flow:

E.1 — Invalid value or access

- Reject fractions, strings, null, and values outside 1–5. expectedRevision is an integer >=0; zero means no prior rating, not an unconditional overwrite.
- Unknown/malformed course, unpublished course, and unassigned course use ENROLLED_COURSE_NOT_AVAILABLE. A valid Instructor session gets ROLE_NOT_ALLOWED; incomplete Student onboarding gets ONBOARDING_REQUIRED.

E.2 — Completion data unavailable

- If canonical required progress cannot be evaluated, return RATING_UNAVAILABLE rather than treating the Student as incomplete or trusting frontend completion.

E.3 — Unknown mutation outcome

- Keep the selected value and original updateId/payload while showing an unresolved state. Offer deliberate exact retry or reload. Do not update the shared aggregate optimistically as if a rating definitely succeeded.
- Failed reads do not imply a zero rating count or no existing personal rating.

UI Integration:

- Reference: [Student My Courses, `222:1174`](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-1174), and Home `222:1888`, whose course-card display is normalized in UC-04.
- Add Rate course / Edit my rating to completed course detail in UC-06. The five-choice form, save/conflict states, and dedicated route are project supplements, not verified source rating-entry frames.
- Use five keyboard-accessible radio choices labelled `1 star` through `5 stars`; visual stars may accompany labels. No value is preselected for a new rating, and hovering does not save.
- Display `No ratings yet` for count=0/average=null. Otherwise show the returned average to one decimal place and its count. Do not treat a missing personal rating as a zero-star vote.
- Return to `/student/my-courses?courseId=<courseId>`, which already exists. Narrow-screen presentation and supplementary messages follow the project styling.

API Endpoint:

- `GET /api/v1/student/courses/:courseId/rating`
- `PUT /api/v1/student/courses/:courseId/rating`

No query parameters. GET has no body. courseId is a UUID. There is no write endpoint accepting another Student's ID.

Request Body:

```json
{
  "updateId": "bc341124-7241-4f8f-bbb1-450ce215b92a",
  "expectedRevision": 0,
  "value": 4
}
```

PUT accepts exactly the keys shown. updateId is a UUID; expectedRevision is integer >=0; value is integer 1–5. Reject additional fields, including studentId, ratingCount, ratingAverage, completedAt, and course status.

Successful Response:

```json
{
  "success": true,
  "message": "Course rating loaded.",
  "data": {
    "courseId": "530f6e99-eef1-4b74-828a-faa79c3df4ba",
    "eligibility": "ELIGIBLE",
    "myRating": null,
    "summary": {
      "ratingCount": 0,
      "ratingAverage": null
    }
  }
}
```

GET HTTP 200; a completed learner without a rating is shown above. PUT HTTP 200 for both creation and updates:

```json
{
  "success": true,
  "message": "Course rating saved.",
  "data": {
    "courseId": "530f6e99-eef1-4b74-828a-faa79c3df4ba",
    "eligibility": "ELIGIBLE",
    "myRating": {
      "value": 4,
      "revision": 1,
      "createdAt": "2026-09-21T10:00:00.000Z",
      "updatedAt": "2026-09-21T10:00:00.000Z"
    },
    "summary": {
      "ratingCount": 1,
      "ratingAverage": 4
    },
    "receipt": {
      "updateId": "bc341124-7241-4f8f-bbb1-450ce215b92a",
      "appliedRevision": 1,
      "replayed": false
    }
  }
}
```

- GET data has exactly courseId, eligibility, myRating, summary. PUT has these same fields plus receipt.
- eligibility is ELIGIBLE or COURSE_NOT_COMPLETED, derived from canonical course completion. Successful PUT always has ELIGIBLE. Under the monotonic completion baseline, an existing personal rating implies the course was completed and remains completed.
- myRating is null if none exists; otherwise exactly {value,revision,createdAt,updatedAt}. value is integer 1–5, revision integer >=1, timestamps non-null UTC ISO 8601. createdAt remains the first accepted rating time; each new accepted write advances revision and updatedAt.
- summary has exactly ratingCount and ratingAverage. Count is the number of unique Student/course rating records, integer >=0. Average is null if count=0; otherwise round half up to one decimal place of sum(values)/count, in 1..5. JSON may represent 4.0 as 4; UI formats one decimal. Preserve the underlying integer sum for aggregation rather than repeatedly rounding an old average.
- receipt has exactly updateId, appliedRevision, replayed. A replay returns the current personal rating and aggregate, possibly newer than the original appliedRevision. It does not replace a later rating with the earlier request value.
- Read rating and summary from a coherent result; concurrent ratings can appear in later reads. Shared CourseCard keys remain unchanged. Do not add rating author identities or comment text to discovery responses.

Error Response:

```json
{
  "success": false,
  "statusCode": 409,
  "code": "COURSE_NOT_COMPLETED",
  "message": "Complete this course before rating it.",
  "timestamp": "2026-09-21T10:00:00.000Z",
  "path": "/api/v1/student/courses/530f6e99-eef1-4b74-828a-faa79c3df4ba/rating"
}
```

All errors contain success=false, statusCode matching the HTTP status, code, message, a server UTC ISO 8601 timestamp, and the actual request pathname without query. Omit data. Only VALIDATION_ERROR may add errors, mapping field paths to nonempty arrays of strings. All success fields described below are required unless explicitly nullable. IDs and timestamps in examples are illustrative.

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | Please sign in to continue. |
| 403 | ROLE_NOT_ALLOWED | This action is not available for your account role. |
| 403 | ONBOARDING_REQUIRED | Complete your learning profile to continue. |
| 404 | ENROLLED_COURSE_NOT_AVAILABLE | This assigned course is not available. |
| 409 | COURSE_NOT_COMPLETED | Complete this course before rating it. |
| 409 | RATING_REVISION_CONFLICT | Your rating changed. Reload it before saving again. |
| 409 | REQUEST_CONFLICT | This request identifier was already used for different content. |
| 503 | RATING_UNAVAILABLE | Course ratings are temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

Validation paths use value, expectedRevision, updateId, or the rejected input field. Do not turn all 403 responses into onboarding redirects; follow the confirmed role and specific code.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement a NestJS/TypeScript rating resource unique per enrolled Student/course. Read completion from the existing shared progress model; do not add a separately writable completion flag. Save the rating, revision, aggregate effect, and request association coherently. First save contributes one value; edits replace its contribution. Rating changes do not modify UC-17 course-content revision or UC-20 schedule revision.

### Frontend UI Context

Implement the supplementary form with React, TypeScript, and Tailwind in the Student shell. Use explicit selection and save, accessible labels, an unsaved-state indicator, and inline validation. Show personal rating separately from the course-wide average. Do not repurpose static Home testimonials as learner-generated reviews.

### Frontend Logic and API Context

Cache the personal resource by account and course. After a confirmed save refresh shared CourseCard-bearing views and the current rating summary; invalidate catalog/dashboard/my-course cached averages for that course. Do not increment counts locally on every save. Preserve the proposed value on conflict and use the returned current revision only after reconciliation. UC-15 save/discard/stay rules apply when leaving an unsaved rating form.

### Validation and Error-Handling Context

Validate numeric types, ranges, membership, completion, and revisions on the backend. Keep absence, zero counts, and failed reads distinct. Never accept an Instructor changing a Student rating or the client supplying an aggregate. This UC defines business outcomes and contracts without prescribing security algorithms or evaluation test procedures.
