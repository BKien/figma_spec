# UC-09: Take a Course Quiz and View the Result

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Take a Course Quiz and View the Result

Description:

- Lets an enrolled Student start/resume a timed quiz, save answers, submit for grading, and view their result and highest score.
- Treats overview, attempt, draft, submission, and result as one quiz-taking business goal. Completes UC-07 QUIZ navigation and contributes quiz completion to the common course progress.
- Attempt limit, grading, passing threshold, timer authority, repeat behavior, and API contracts are project decisions. Figma supplies the three quiz screens, not an existing Technical Report or backend contract.

Primary Actor:

Authenticated, onboarded Student enrolled in the quiz course.

Preconditions:

- UC-07 resolves a QUIZ unit. Register its overview at `/student/courses/:courseId/units/:unitId` and attempt page at `/student/courses/:courseId/units/:unitId/attempts/:attemptId`, both reloadable.
- Each quiz fixture contains exactly five single-choice questions, four choices per question, one correct choice per question, a 1200-second limit, and maximum score five. These normalize the inspected source for this baseline.
- Quiz definitions and correct answers remain fixed for the experiment. Instructor authoring/version changes are separately scoped.

Postconditions:

- Success: A submitted attempt has one persisted grade, the highest score reflects all submitted attempts, and passing at least once completes this quiz unit exactly once.
- Partial progress: Confirmed drafts can be resumed within the same deadline. Leaving the page does not stop the timer.
- Failure: Rejected requests do not replace saved answers, extend the deadline, or create duplicate attempts/grades. Saved state can be reconciled after an uncertain response.

Main Flow:

1. The Student opens the quiz overview; GET shows title, five questions, 20 minutes, five points, attempt allowance, and any current/highest result.
2. Start sends a start request. The backend creates the first active attempt and fixes expiresAt=startedAt+1200 seconds. Creating an attempt, not reading the overview, starts the quiz unit.
3. Open the returned attempt page and render all five questions with no preselected answer, the server-relative countdown, Save draft, and Submit.
4. The Student selects one choice per question. Save draft persists the complete answer set, including null for unanswered questions, without pausing the timer.
5. Submit sends the current complete answer set and latest revision. Before expiry, the server saves and grades those answers in one completion operation.
6. Award one point per correct answer; unanswered/wrong choices earn zero. Score at least three out of five passes.
7. Render Submitted, the attempt's score/pass status, and highest score; return to the overview or continue through UC-07. Correct-answer explanations are outside this baseline.
8. A first pass completes the unit and updates UC-05–07 aggregation. A failed attempt leaves the unit IN_PROGRESS, even though that attempt is Submitted.

Alternative Flow:

A.1 — Resume and retries

- At most three attempts per enrollment/quiz, including deadline-submitted attempts. At most one attempt may be active. Starting while an unexpired active attempt exists returns it without allocating another attempt or resetting its timer.
- startRequestId is retained with its result. Identical repeats return that same attempt even if it has since been submitted; they never start a retry. A deliberate new attempt uses a new ID.
- Retry quiz is a supplementary action when no active attempt exists and fewer than three attempts have been used. Passing does not prohibit a remaining retry. Keep the highest score; a later lower score cannot undo unit completion.
- At the limit, show the saved results with Retry disabled. No course or account reset is implied.

A.2 — Drafts and multiple tabs

- Draft saves use updateId, expectedRevision, and all five answers. Unanswered values are null. A successful new draft save increments revision; a recognized identical updateId replay does not. Recognized accepted draft repeats return the current attempt state before submitted/expiry checks, even if it was finalized later; the frontend then displays its result rather than continuing editing.
- Concurrent stale revisions return QUIZ_ATTEMPT_CONFLICT. Load the latest saved attempt on explicit user action; do not silently merge two tabs' answers. Preserve the local choices for review until replacing them.
- Back/Previous/Next while there are unsaved choices offers Save draft and leave, Leave without saving, and Stay. Leaving retains the fixed deadline. Reload restores only saved choices.

A.3 — Deadline

- The backend clock is authoritative. Save/submit requests evaluated at or after expiresAt cannot replace the stored draft with new answers. A before-deadline button click is not enough if its request reaches the server too late.
- At the deadline the client stops editing and requests submission; after-deadline submission grades the last confirmed draft, regardless of any supplied newer choices. Clearly state `Time expired. Your saved answers were submitted.`
- The backend also finalizes overdue active attempts within 60 seconds of expiry without requiring a browser. This uses the same single-submission outcome and grades the last saved draft. On a service outage, finalize when processing resumes without extending the original deadline.
- GET remains read-only. During the short finalization interval it may return persisted IN_PROGRESS with serverNow >= expiresAt; the UI then disables edits and offers/checks submission instead of showing extra time. All start/draft/submit mutations resolve an overdue active attempt before allowing further quiz mutations. If a new start request encounters an overdue active attempt, it returns that now-submitted attempt with HTTP 200 and associates the request ID with it; it does not silently allocate the next attempt. A subsequent deliberate Retry uses a new ID.
- submittedAt records actual finalization time; submissionReason=DEADLINE distinguishes expiry from a manual submission. With no saved answers, all five are null and the score is zero. One attempt is consumed.

A.4 — Submission retries and consistent outcomes

- submissionRequestId identifies a submission. Repeating it with unchanged payload returns the saved result; reuse with different content returns REQUEST_CONFLICT. Once an attempt is submitted, a structurally valid new submission request returns its existing result and cannot change answers or score, even with a stale expectedRevision.
- Active, unexpired submission requires current expectedRevision. A late request finalizes the last confirmed draft without applying its stale payload. Successful completion/draft writes and automatic expiry are serialized outcomes: one grade and one unit completion transition at most.
- A failed/unknown start, draft, or submit offers a deliberate same-ID retry with the exact payload. A known attempt can also be read to reconcile its current status. Do not automatically allocate a fresh attempt or claim success after a timeout.

A.5 — Source normalization

- Display five questions, 20 minutes, five maximum points, and a three-point passing threshold across overview, form, result, and UC-07 sidebar. Replace the source's 10-question/10-point text and 10-minute sidebar label.
- Correct the source's ambiguous `type(5.0)` question to ask for the data type of the value 5.0. Replace Summ it/Summited typos with Submit/Submitted where present.
- Source selected radio states are illustrations; new attempts start with all answers null. No code execution is needed for the displayed code question.

Exception Flow:

E.1 — Invalid answers or attempt access

- Each answer must reference one of the attempt's five question IDs and an option belonging to that question, or null. Duplicates, missing question entries, unknown fields, wrong types, or client score/timestamps return VALIDATION_ERROR.
- A different account's attempt or a mismatched quiz/course yields generic LEARNING_CONTENT_NOT_AVAILABLE. Knowing an attempt UUID does not establish enrollment or ownership.

E.2 — Expired, submitted, or exhausted

- Draft save after deadline first resolves finalization and returns QUIZ_ATTEMPT_EXPIRED; load the attempt result. Draft save after an earlier submission returns QUIZ_ATTEMPT_SUBMITTED.
- Starting beyond three attempts returns QUIZ_ATTEMPT_LIMIT_REACHED. Submitted results remain readable and navigation remains available.

E.3 — Service/session interruption

- QUIZ_UNAVAILABLE offers retry and does not pause the deadline. Show saved/unsaved distinction; never announce a draft was saved before confirmation.
- 401 returns to sign-in after clearing private form state. The server deadline continues, and expiry may submit the last saved draft. After login, GET reconciles the result; it does not grant a replacement attempt for the interruption.
- A result-refresh failure after confirmed submission does not negate submission. Retry reading rather than creating a new attempt.

UI Integration:

- Overview: `16 Courses Detail Quiz`, node `222:801`.
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-801
- Attempt: `17 Courses Detail Quiz Detail`, node `222:650`.
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-650
- Result: `18 Courses Detail Quiz Summited`, node `222:535`.
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-535
- Live contexts/screenshots inspected on 2026-09-20. Preserve overview card, Your grade, timed two-column question cards, radio choices, code block, Save draft and Submit, and submitted-result composition.
- Resume/Retry, attempt allowance, pass/fail, saving/conflict/expiry feedback, and unsaved-navigation choices are supplements. No mobile or frozen dataset claim. Retain the sidebar completion icon only when the unit has passed, not merely because an attempt was submitted.

API Endpoint:

- `GET /api/v1/student/courses/:courseId/units/:unitId/quiz`
- `POST /api/v1/student/courses/:courseId/units/:unitId/quiz/attempts`
- `GET /api/v1/student/courses/:courseId/units/:unitId/quiz/attempts/:attemptId`
- `PUT /api/v1/student/courses/:courseId/units/:unitId/quiz/attempts/:attemptId/draft`
- `POST /api/v1/student/courses/:courseId/units/:unitId/quiz/attempts/:attemptId/submit`

Request Body:

All route IDs are UUIDs. No query parameters; GET accepts no body. Start accepts exactly:
```json
{
  "startRequestId": "206dddb0-c44a-4e71-8515-e31b7f5230c6"
}
```

Draft accepts exactly:
```json
{
  "updateId": "cebb8a0b-f887-4ff3-ae0f-f7f0b9bfd4c5",
  "expectedRevision": 0,
  "answers": [
    {
      "questionId": "python-print",
      "optionId": null
    },
    {
      "questionId": "python-name",
      "optionId": null
    },
    {
      "questionId": "python-float",
      "optionId": null
    },
    {
      "questionId": "python-input",
      "optionId": null
    },
    {
      "questionId": "python-add",
      "optionId": null
    }
  ]
}
```

Submit accepts exactly:
```json
{
  "submissionRequestId": "d47d4e67-f7c4-4639-9f81-53bb069c7b85",
  "expectedRevision": 0,
  "answers": [
    {
      "questionId": "python-print",
      "optionId": "c"
    },
    {
      "questionId": "python-name",
      "optionId": "c"
    },
    {
      "questionId": "python-float",
      "optionId": "c"
    },
    {
      "questionId": "python-input",
      "optionId": "a"
    },
    {
      "questionId": "python-add",
      "optionId": "c"
    }
  ]
}
```

expectedRevision is a nonnegative JSON safe integer. Request IDs are UUIDs. answers contains exactly one {questionId,optionId} per question, with optionId either a valid choice ID or null. IDs are case-sensitive nonempty strings up to 64 characters from the returned definition; array order is normalized to question order. No trimming/coercion, duplicate IDs, or extra fields. Empty choices are represented as null, not an omitted answer. Even after expiry/submission, request structure must be valid before lifecycle handling.

Successful Response:

```json
{
  "success": true,
  "message": "Quiz retrieved.",
  "data": {
    "unitId": "4be1f7da-a5da-46f2-9ac8-28e5dca03ae2",
    "title": "Quiz: Python Basics",
    "questionCount": 5,
    "timeLimitSeconds": 1200,
    "maxScore": 5,
    "passingScore": 3,
    "maxAttempts": 3,
    "attemptsUsed": 0,
    "activeAttemptId": null,
    "lastAttemptId": null,
    "bestScore": null,
    "unitStatus": "NOT_STARTED"
  }
}
```

```json
{
  "success": true,
  "message": "Quiz attempt retrieved.",
  "data": {
    "serverNow": "2026-09-20T10:00:00.000Z",
    "attempt": {
      "id": "509c0eaa-f8ed-413c-a395-9954faed5e60",
      "number": 1,
      "status": "IN_PROGRESS",
      "revision": 0,
      "startedAt": "2026-09-20T10:00:00.000Z",
      "expiresAt": "2026-09-20T10:20:00.000Z",
      "submittedAt": null,
      "submissionReason": null,
      "answers": [
        {
          "questionId": "python-print",
          "optionId": null
        },
        {
          "questionId": "python-name",
          "optionId": null
        },
        {
          "questionId": "python-float",
          "optionId": null
        },
        {
          "questionId": "python-input",
          "optionId": null
        },
        {
          "questionId": "python-add",
          "optionId": null
        }
      ],
      "result": null
    },
    "questions": [
      {
        "id": "python-print",
        "prompt": "Which syntax prints Hello, World in Python 3?",
        "code": null,
        "options": [
          {
            "id": "a",
            "text": "print \"Hello, World\""
          },
          {
            "id": "b",
            "text": "echo(\"Hello, World\")"
          },
          {
            "id": "c",
            "text": "print(\"Hello, World\")"
          },
          {
            "id": "d",
            "text": "System.out.print(\"Hello, World\")"
          }
        ]
      },
      {
        "id": "python-name",
        "prompt": "Which is a valid Python variable name?",
        "code": null,
        "options": [
          {
            "id": "a",
            "text": "2name"
          },
          {
            "id": "b",
            "text": "my-name"
          },
          {
            "id": "c",
            "text": "my_name"
          },
          {
            "id": "d",
            "text": "my name"
          }
        ]
      },
      {
        "id": "python-float",
        "prompt": "What is the data type of the value 5.0 in Python?",
        "code": null,
        "options": [
          {
            "id": "a",
            "text": "int"
          },
          {
            "id": "b",
            "text": "str"
          },
          {
            "id": "c",
            "text": "float"
          },
          {
            "id": "d",
            "text": "bool"
          }
        ]
      },
      {
        "id": "python-input",
        "prompt": "Which built-in function reads text input from the user?",
        "code": null,
        "options": [
          {
            "id": "a",
            "text": "input()"
          },
          {
            "id": "b",
            "text": "get()"
          },
          {
            "id": "c",
            "text": "scan()"
          },
          {
            "id": "d",
            "text": "prompt()"
          }
        ]
      },
      {
        "id": "python-add",
        "prompt": "What does this code print?",
        "code": "x = 3\ny = 2\nprint(x + y)",
        "options": [
          {
            "id": "a",
            "text": "32"
          },
          {
            "id": "b",
            "text": "3 + 2"
          },
          {
            "id": "c",
            "text": "5"
          },
          {
            "id": "d",
            "text": "None"
          }
        ]
      }
    ]
  }
}
```

```json
{
  "success": true,
  "message": "Quiz submitted.",
  "data": {
    "serverNow": "2026-09-20T10:10:00.000Z",
    "attempt": {
      "id": "509c0eaa-f8ed-413c-a395-9954faed5e60",
      "number": 1,
      "status": "SUBMITTED",
      "revision": 1,
      "startedAt": "2026-09-20T10:00:00.000Z",
      "expiresAt": "2026-09-20T10:20:00.000Z",
      "submittedAt": "2026-09-20T10:10:00.000Z",
      "submissionReason": "MANUAL",
      "answers": [
        {
          "questionId": "python-print",
          "optionId": "c"
        },
        {
          "questionId": "python-name",
          "optionId": "c"
        },
        {
          "questionId": "python-float",
          "optionId": "c"
        },
        {
          "questionId": "python-input",
          "optionId": "a"
        },
        {
          "questionId": "python-add",
          "optionId": "c"
        }
      ],
      "result": {
        "score": 5,
        "maxScore": 5,
        "passed": true
      }
    },
    "bestScore": 5,
    "unitStatus": "COMPLETED"
  }
}
```

- Overview GET returns 200 with exactly the shown fields. bestScore is null before any submission, otherwise integer 0–5; IDs nullable UUIDs; attemptsUsed is 0–3; unitStatus NOT_STARTED|IN_PROGRESS|COMPLETED. lastAttemptId is the highest attempt number whether active or submitted. An overdue persisted active ID may appear until finalization; opening it uses serverNow/expiresAt.
- Start returns 201 for new creation, 200 for reuse/replay, with message Quiz attempt ready. Its exact data shape matches attempt GET: {serverNow,attempt,questions}. GET uses message Quiz attempt retrieved. Draft PUT returns 200/message Quiz draft saved with that same data shape, refreshed revision/answers, and no grade while active.
- Questions have exactly id, prompt, code (nullable plain text), options (four {id,text} entries). Five questions appear in fixed order. Correct-answer keys, per-question correctness, and explanations are not response fields before or after grading. Correct fixture options are python-print=c, python-name=c, python-float=c, python-input=a, python-add=c; these are backend grading data, not frontend payload fields.
- attempt has exactly id UUID, number integer 1–3, status IN_PROGRESS|SUBMITTED, revision nonnegative integer, startedAt/expiresAt ISO UTC, submittedAt nullable ISO UTC, submissionReason null|MANUAL|DEADLINE, answers in question order, and result null or {score: integer 0–5,maxScore:5,passed:boolean}. IN_PROGRESS has null submission fields/result. SUBMITTED has nonnull submission fields/result. ServerNow is a fresh UTC timestamp for countdown rendering, not a client-selected timer.
- Start sets revision=0. Each accepted new draft increments once. Submission increments once and finalizes; repeats never increment, regrade, or change submittedAt. Request associations remain for the life of the experiment's attempt record. Submitted-attempt replay does not reopen it.
- Submit returns 200 with exactly {serverNow,attempt,bestScore,unitStatus}, using the submitted-result example shape. For deadline finalization, the same message Quiz submitted is paired with reason DEADLINE; the frontend shows the expiry-specific explanation. bestScore is the maximum submitted score across attempts, not a sum. No pass is undone by a lower later result.
- First attempt sets unit.startedAt once. First score >=3 sets unit.completedAt once and updates common module/course aggregation. Accepted new start/draft/manual submission advances lastActivityAt; exact repeats, result reads, and background deadline finalization do not count as new Student activity. Course completion can advance on finalization if the saved draft passes; its completedAt is the actual first all-units-complete time.
- These writes do not populate measured learningSeconds, streakDays, or weeklyGoalPercent; those remain unavailable absent their own measurement/goal sources. Attempt elapsed time is not proof of active study time.

Error Response:

```json
{
  "success": false,
  "statusCode": 503,
  "code": "QUIZ_UNAVAILABLE",
  "message": "Quiz learning is temporarily unavailable. Please try again later.",
  "timestamp": "2026-09-20T10:00:00.000Z",
  "path": "/api/v1/student/courses/ba22825a-9acf-4d85-af5f-5c77f83d6ac7/units/4be1f7da-a5da-46f2-9ac8-28e5dca03ae2/quiz"
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
| 409 | QUIZ_ATTEMPT_CONFLICT | Your quiz answers changed. Load the latest attempt before saving. |
| 409 | QUIZ_ATTEMPT_EXPIRED | Time expired. Load your submitted result. |
| 409 | QUIZ_ATTEMPT_SUBMITTED | This quiz attempt has already been submitted. |
| 409 | QUIZ_ATTEMPT_LIMIT_REACHED | You have used all attempts for this quiz. |
| 409 | REQUEST_CONFLICT | This request identifier was already used for different content. |
| 503 | QUIZ_UNAVAILABLE | Quiz learning is temporarily unavailable. Please try again later. |

## Project-Specific Implementation Context

### Backend Implementation Context

Implement quiz overview, attempt lifecycle, draft, grade, and deadline finalization in NestJS/TypeScript using fixed definitions and shared enrolled-unit progress. Keep one active attempt and at most three attempts per enrollment/quiz. Grade only server-owned correct choices; map five normalized questions to five points. Handle repeats, stale revisions, expiry, and completion as consistent outcomes under competing requests and the deadline processor. GET endpoints remain read-only.

### Frontend UI Context

Implement the overview, complete five-question form, and result using the three inspected frames in React/TypeScript/Tailwind. Use explicit labels and keyboard-operable single-choice groups; code is display-only. Show the actual remaining time, saved/unsaved state, highest score and passing threshold, with accessible expiry/submission feedback. Do not style a failed submitted attempt as a passed unit.

### Frontend Logic and API Context

Create an attempt only after Start/Retry, route to its returned ID, and resume through GET. Maintain the latest confirmed revision and complete local answer set. Save draft explicitly; do not silently imply continuous autosave. Compute countdown from serverNow/expiresAt and recheck on returning to a backgrounded tab. At zero, disable edits and request submission of the stored draft through the declared endpoint. Serialize writes, retain unknown request IDs/payloads for deliberate retry, and refresh UC-05–07 after confirmed grade changes.

### Validation and Error-Handling Context

Validate ownership/nesting, question-option membership, cardinality, revision, attempt limit, and deadline on the server. Client timer, score, or selected role cannot determine eligibility or grade. Recover uncertain outcomes without allocating duplicate attempts. Keep source corrections explicit, protect saved progress from conflicting tabs, and avoid claiming attendance or certificates from a quiz score.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
