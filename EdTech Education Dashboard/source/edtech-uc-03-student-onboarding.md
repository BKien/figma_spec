# UC-03: Set Up a Student Learning Profile

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Set Up a Student Learning Profile

Description:

- Collects the Student's learning goals, interests, current occupation, and education level through the four initial setup screens.
- Replaces UC-02's `/student/onboarding` integration shell. The four steps belong to one onboarding goal, with saved progress and an explicit completion outcome.
- The field choices and selection maxima are supported by Figma. Minimum selections, persistence, API contracts, concurrency behavior, and completion rules below are proposed project requirements, not quotations from a supplied Technical Report.
- The question Your Current Role describes occupation. It must not change account.role, grant Instructor privileges, or act as an application-role selector.

Primary Actor:

Authenticated Student with an incomplete learning profile.

Preconditions:

- UC-01 has created an ACTIVE, verified STUDENT account; UC-02 provides a valid browser session.
- Account onboardingStatus is NOT_STARTED or IN_PROGRESS. COMPLETED accounts are routed to the existing `/student/dashboard` destination.
- The four-step option catalogue defined below is available in the application. No external recommendation, employment, or education service is required.

Postconditions:

- Success: All four valid answers are persisted, onboardingStatus becomes COMPLETED, and completedAt records the completion time. The Student reaches `/student/dashboard`.
- Partial progress: Each confirmed step save is retained for the same account across reloads and devices. After the first save, onboardingStatus is IN_PROGRESS.
- Failure: A rejected save or completion does not change persisted answers or completion state. Previously confirmed progress remains available.
- Completion does not enroll the Student in a course, award a certificate, change account privileges, or guarantee personalized recommendations.

Main Flow:

1. UC-02 routes an incomplete Student to `/student/onboarding`; the frontend retrieves their saved onboarding resource.
2. For a new profile, show step 1, What brings you here?, without preselected answers. The Student selects one or two goals and clicks Next.
3. Save step 1. Advance to step 2 only after confirmation. The Student selects one to five interests and clicks Next; save and advance.
4. At step 3, the Student selects exactly one occupation and clicks Next; save and advance.
5. At step 4, the Student selects exactly one highest education level. The source's highlighted first option is sample state, not a default answer.
6. On Finish setup, save step 4, then request completion using the revision returned by that save.
7. The backend checks all four answers and commits the completed profile together with account.onboardingStatus=COMPLETED.
8. The frontend displays `Your learning profile is ready.`, refreshes UC-02's session summary, and opens `/student/dashboard` once that summary confirms COMPLETED.
9. Until the dashboard UC replaces its contents, UC-02's implemented dashboard shell remains the destination. Do not introduce a missing route or fabricated learning data.

Alternative Flow:

A.1 — Resume saved progress

- GET returns resumeStep as the first step without a saved valid answer, or 4 when all answers are saved but completion is pending. It returns null after completion.
- A reload or later login opens resumeStep using persisted answers. Unsaved local selections are not promised to survive reload or session loss.
- A successful step save normally opens the next numbered step in the current view. resumeStep is a recovery position, not a command that prevents visiting earlier steps.

A.2 — Back and change an answer

- Back on steps 2–4 moves to the previous step without a server mutation. In-memory selections remain while this account's wizard stays mounted; they persist across reload only after a confirmed save.
- Returning to an earlier step and selecting Next saves that step. Independent later answers remain valid and are not silently cleared.
- Only the first incomplete step and earlier saved steps may be submitted. Skipping ahead through a forged request is rejected. When all four answers exist, all steps remain editable until completion.
- Step indicators display progress and do not provide unsupported jump-ahead navigation. There is no Back action on step 1 and no Skip setup action in this baseline.

A.3 — Search options

- Step 2 search filters the displayed interest labels; step 3 search filters occupation labels. Matching is a trimmed, case-insensitive literal substring performed locally over the fixed catalogue.
- Search never creates an option or sends a course-search request. Selected choices remain selected and count toward the maximum when hidden by a filter.
- Display selected-choice chips with removal controls so filtered selections can still be reviewed. A no-match message and Clear search restore the available options.
- Selecting an already selected goal/interest deselects it. Reaching a maximum disables adding another choice until one is removed. Occupation and education choices replace the previous single selection.

A.4 — Completion retry or revisit

- Completion of an already COMPLETED profile returns HTTP 200 with the existing result and original completedAt, even if the supplied expectedRevision is from the earlier completion request. It does not modify answers or create another completion.
- A direct visit to `/student/onboarding` after completion routes to `/student/dashboard`. Editing the completed profile belongs to a later profile/preferences UC; it is not silently enabled through the initial setup API.
- If step 4 was saved but completion failed, keep that answer and offer Finish setup again; do not require the Student to re-enter the first three steps.

Exception Flow:

E.1 — Invalid input or incomplete sequence

- Missing/unknown/duplicate choices, wrong types, invalid selection counts, and extra fields return VALIDATION_ERROR. Show an error by the relevant options and preserve the correctable local selections.
- Saving a later step before its prerequisites returns STEP_NOT_AVAILABLE. A completion request with missing answers returns ONBOARDING_INCOMPLETE; load the saved profile and open resumeStep.

E.2 — Concurrent changes

- Every save requires the current expectedRevision. A different revision returns ONBOARDING_CONFLICT without overwriting answers, even when this tab's values look newer.
- Display `Your setup changed in another tab or device. Load the latest version to continue.` Retain the local selections for review until the Student chooses Load latest; do not automatically merge or overwrite them.
- Loading latest replaces the local draft with the returned account profile and revision. If already completed, route to the dashboard after confirming the session summary.

E.3 — Unknown request outcome or unavailable service

- Disable additional mutations while a save/completion result is uncertain. Read the resource once; if it succeeds, show the actual saved state and revision. Do not automatically replay an old-revision save.
- If the resource is still incomplete, permit deliberate continuation from its saved state. If it is completed, recover the success path. Another tab may have supplied that state; do not falsely attribute it to this tab's failed request.
- A failed reconciliation shows Check saved progress again and keeps mutations disabled. Previously confirmed answers must not be represented as lost.
- A completed response followed by session-refresh failure keeps the completion confirmation visible with Retry session check. Do not repeat completion to solve a session-read failure or redirect using stale NOT_STARTED state.

E.4 — Session no longer usable

- Return 401 UNAUTHENTICATED for a missing/expired/ineligible UC-02 session. Clear private wizard state and return to `/sign-in`. Confirmed progress remains stored; unsaved changes may be lost.
- A service outage does not imply logout. Clear obsolete responses on account change and never reuse another account's draft.

UI Integration:

| Step | Exact Figma frame | Node | Visible purpose |
| --- | --- | --- | --- |
| 1 | 06 Setting Up Student 1 | 222:2355 | What brings you here?; up to two goals |
| 2 | 07 Setting Up Student 2 | 222:2263 | Pick your areas of interest; up to five choices |
| 3 | 08 Setting Up Student 3 | 222:2198 | Your Current Role; one choice |
| 4 | 09 Setting Up Student 4 | 222:2147 | Highest level of education; one choice |

- Step 1: https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-2355
- Step 2: https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-2263
- Step 3: https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-2198
- Step 4: https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-2147
- Live contexts and screenshots inspected on 2026-09-20. Preserve the white canvas, four-step indicator, yellow active/selected controls, option cards, search inputs, decorative stars, and Back/Next placement.
- Correct Select 1 options to Select one option. Rename the final Next action Finish setup so completion is explicit. Add helper text stating the minimum selection requirements rather than assuming the source's up-to wording establishes them.
- Required minima, selected chips, pending/error/conflict feedback, completion confirmation, and responsive wrapping are project supplements. No frozen dataset or mobile design is claimed.
- Use accessible multi-select controls for goals/interests and single-select controls for occupation/education. Do not make selection depend on color alone. Restore useful focus after a step changes.

API Endpoint:

- `GET /api/v1/student/onboarding`
- `PUT /api/v1/student/onboarding/steps/:step`
- `POST /api/v1/student/onboarding/complete`

All endpoints use the UC-02 browser session and address only its Student account. No userId, account role, or email selects the resource. No query parameters are accepted.

Request Body:

GET has no body. Step is the path integer 1, 2, 3, or 4. Each PUT accepts exactly the corresponding shape:

```json
{
  "expectedRevision": 0,
  "goalIds": ["learn-something-new", "advance-career"]
}
```

```json
{
  "expectedRevision": 1,
  "interestIds": ["web-dev", "ui-ux"]
}
```

```json
{
  "expectedRevision": 2,
  "occupationId": "student"
}
```

```json
{
  "expectedRevision": 3,
  "educationLevelId": "bachelors-degree"
}
```

Completion:

```json
{
  "expectedRevision": 4
}
```

expectedRevision is a nonnegative JSON safe integer. Example revisions assume four sequential first saves; clients always use the latest server value. Reject unknown keys, null selections, stringified revisions, and any query parameters. IDs are exact, case-sensitive values from the catalogue; do not trim, invent, or silently coerce IDs. Arrays contain unique IDs; order is not semantically meaningful and responses use catalogue order.

| Field | Count | Allowed IDs and UI labels |
| --- | --- | --- |
| goalIds | 1–2 | learn-something-new = Learn something new; advance-career = Advance my career; master-skill = Master a specific skill; collaborate-network = Collaborate or network; support-study = Support school/university work |
| interestIds | 1–5 | Tech: web-dev = Web Dev, mobile-dev = Mobile Dev, ui-ux = UI/UX, ai = AI, cybersecurity = Cybersecurity. Business: marketing = Marketing, finance = Finance, entrepreneurship = Entrepreneurship. Academic: math = Math, science = Science, languages = Languages |
| occupationId | Exactly 1 | student = Student; working-professional = Working Professional; intern-trainee = Intern / Trainee; freelancer-self-employed = Freelancer / Self-employed; job-seeker = Job Seeker; other = Other |
| educationLevelId | Exactly 1 | below-high-school = Less than high school diploma; high-school = High school diploma; bachelors-degree = Bachelor's degree; masters-degree = Master's degree; doctorate = Doctorate degree |

Other does not require an additional free-text field because none is supplied by the design. Occupation is descriptive profile data, independent of the STUDENT application role. The catalogue is fixed for this baseline; there is no separate catalogue API or administrative editor in this UC.

Successful Response:

GET for a new account returns HTTP 200 without creating progress or changing account state:

```json
{
  "success": true,
  "message": "Learning profile retrieved.",
  "data": {
    "onboardingStatus": "NOT_STARTED",
    "revision": 0,
    "answers": {
      "goalIds": [],
      "interestIds": [],
      "occupationId": null,
      "educationLevelId": null
    },
    "resumeStep": 1,
    "completedAt": null
  }
}
```

PUT step 1, HTTP 200:

```json
{
  "success": true,
  "message": "Setup progress saved.",
  "data": {
    "onboardingStatus": "IN_PROGRESS",
    "revision": 1,
    "answers": {
      "goalIds": ["learn-something-new", "advance-career"],
      "interestIds": [],
      "occupationId": null,
      "educationLevelId": null
    },
    "resumeStep": 2,
    "completedAt": null
  }
}
```

POST completion, HTTP 200:

```json
{
  "success": true,
  "message": "Your learning profile is ready.",
  "data": {
    "onboardingStatus": "COMPLETED",
    "revision": 5,
    "answers": {
      "goalIds": ["learn-something-new", "advance-career"],
      "interestIds": ["web-dev", "ui-ux"],
      "occupationId": "student",
      "educationLevelId": "bachelors-degree"
    },
    "resumeStep": null,
    "completedAt": "2026-09-20T10:30:00.000Z"
  }
}
```

- All data keys are required and shared across all three endpoints. GET of an existing profile returns its current state with the retrieval message. PUT returns the whole saved profile with the save message.
- Missing unsaved array answers are []; missing single-choice answers are null. Only GET/response representations allow these empty values; a submitted step must satisfy its minimum count.
- onboardingStatus is NOT_STARTED, IN_PROGRESS, or COMPLETED. resumeStep is an integer 1–4 for incomplete profiles and null after completion. completedAt is null until completion, then server-generated ISO 8601 UTC.
- Each accepted PUT at the current revision increments revision by one, including a deliberate save of unchanged answers. A stale revision never silently succeeds. First completion also increments once; repeated completion does not increment or alter completedAt.
- A completed profile rejects PUT with ONBOARDING_ALREADY_COMPLETED. For an incomplete profile, completion requires the current revision before checking answer completeness. For an already completed profile, a structurally valid completion request returns the existing result before comparing its expectedRevision.
- Account onboardingStatus and this resource must agree after each successful mutation. A successful completion must be visible to subsequent UC-02 session reads. Responses include no session credential or unrelated private account data.

Error Response:

```json
{
  "success": false,
  "statusCode": 409,
  "code": "ONBOARDING_CONFLICT",
  "message": "Your setup changed in another tab or device. Load the latest version to continue.",
  "timestamp": "2026-09-20T10:25:00.000Z",
  "path": "/api/v1/student/onboarding/steps/2"
}
```

Use UC-01/UC-02's error envelope: success=false, statusCode matching HTTP status, code, message, server ISO UTC timestamp, and actual request pathname without query. Omit data. Only VALIDATION_ERROR may additionally contain errors mapping input field names to nonempty arrays of strings. This UC adds no new rate-limit policy.

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | You must sign in to continue. |
| 409 | STEP_NOT_AVAILABLE | Complete the earlier setup steps first. |
| 409 | ONBOARDING_INCOMPLETE | Complete all four setup steps before finishing. |
| 409 | ONBOARDING_CONFLICT | Your setup changed in another tab or device. Load the latest version to continue. |
| 409 | ONBOARDING_ALREADY_COMPLETED | Your initial setup is already complete. |
| 503 | ONBOARDING_UNAVAILABLE | Learning profile setup is temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

The first accepted step save changes NOT_STARTED to IN_PROGRESS. Only completion changes IN_PROGRESS to COMPLETED. Reading, searching, changing local selections, pressing Back, or reaching step 4 without completion does not complete onboarding. A failed completion leaves all previously saved answers intact.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement the three endpoints in NestJS/TypeScript against UC-01's Student identity and UC-02's session integration. Maintain one learning profile per account, ordered prerequisite validation, revision, and completion timestamp. Treat account onboarding status and profile state as one coherent mutation outcome. Concurrent updates must not lose previously committed answers or generate two completion transitions.

The first incomplete step is derived from persisted answers using the fixed catalogue. Do not accept client-supplied resumeStep, completion timestamp, account role, or onboardingStatus. Keep saved partial answers available for later login; no timed abandonment deletion is introduced by this UC. Enrollment, recommendations, course progress, and Instructor permissions remain unchanged.

### Frontend UI Context

Replace the UC-02 onboarding shell on the existing route with the four inspected screens using React, TypeScript, and Tailwind CSS. Reuse one wizard state and option-control pattern across steps. Expose selection limits, selected chips, Back/Next, and explicit Finish setup. Keep the dashboard shell as a valid destination until its own UC is implemented.

### Frontend Logic and API Context

Load the saved resource after the session guard. Keep a per-account local draft, last confirmed profile, current step, and revision. Send one mutation at a time. Advance only after a confirmed step save; finish with step-4 PUT followed by completion POST using the returned revision. On retry after step-4 save, reuse the saved state and complete rather than repeating earlier saves automatically.

Search filters only visible options. Back changes the local step without persisting new edits. On completion refresh the session summary before navigation; never force onboardingStatus locally to bypass UC-02's guard. Reset all private wizard state and ignore stale responses when the account changes.

### Validation and Error-Handling Context

Apply the fixed ID catalogue, selection bounds, prerequisite order, revision, and completion rules on the server as well as UI feedback. Preserve correctable selections after definite errors; resolve uncertain outcomes through a read before another mutation. Separate expired-session behavior from service failure. Do not infer occupational authority, grant Instructor access, auto-select personal answers, or claim enrollment/recommendation results from setup completion.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
