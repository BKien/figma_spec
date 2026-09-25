# UC-15: Sign Out of the Current Browser Session

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Sign Out of the Current Browser Session

Description:

- Lets a signed-in Student end the current browser session and return to Login.
- Completes the Logout controls in the account menu and Profile screen. Unlike UC-13/14, this operation does not end every device's session.
- Session termination, unsaved-work behavior, and API contract are project decisions; Figma supports the visible action, not its backend implementation.

Primary Actor:

Signed-in Student, including an account with incomplete onboarding. An already-ended session also receives successful logout.

Preconditions:

- UC-02 cookie-based session integration and `/sign-in` exist.
- Shared account menu and Profile contain Logout; add the same action to the minimal onboarding header so an incomplete account can leave its session.
- Confirmed learning progress, saved settings, and quiz drafts are persisted independently of frontend session state.

Postconditions:

- Success: The session attached to the request no longer authenticates, its browser credential is cleared, and private frontend state is cleared before showing Login with `You have signed out.`
- Other independent sessions remain valid. Account identity, onboarding, enrollment, preferences, profile, saved video progress, quiz drafts/results, and deadlines persist.
- Failure/unknown outcome: Do not announce server-side sign-out merely because private content was hidden or local state was cleared.

Main Flow:

1. The Student selects Logout in an implemented account menu, Profile, or onboarding header.
2. If the current view has unsaved settings, video coverage, or quiz choices, apply the unsaved-work handling below.
3. Submit `POST /api/v1/auth/logout` once and disable repeated logout/mutation actions in that view.
4. The backend ends only the presented session when it exists and clears its browser credential. Missing/already-ended session is the same successful outcome.
5. Clear account-scoped frontend caches, passwords, recovery tokens, drafts, and current-account theme/preference state; ignore pending old-account responses.
6. Navigate to `/sign-in` and show `You have signed out.` Protected-route re-entry uses UC-02 session checks.

Alternative Flow:

A.1 — Unsaved work

- If the current page has a supported save operation, offer Save and sign out, Sign out without saving, and Stay. Save and sign out runs that page's defined save first and logs out only after confirmation. A failed/uncertain save keeps the user on the page with its recovery controls.
- For settings this saves their current complete draft; for video it saves pending ranges/position; for quiz it saves the current draft. Saving a quiz does not submit it or pause its deadline.
- If a quiz has expired, its UC-09 lifecycle rules still govern finalization; do not promise a late draft can be saved. Offer sign-out without further edits once its state is resolved, or Stay to inspect the result.
- A non-saveable draft, such as unsent password fields, offers Discard and sign out or Stay. Clear password values on exit.
- A mutation already in flight must be resolved before a second conflicting save/logout is deliberately launched from that view. Abrupt browser closure has no saved-progress guarantee.

A.2 — Missing session or repeat

- Absent, expired, invalid, or already-ended session returns HTTP 200 with the same body, not 401. Repeating logout cannot extend a session or create a new one.
- The operation concerns the session presented to that request. A separate subsequent sign-in in another tab can establish another session; the old logout is not a command to block all future login.

A.3 — Quiz after sign-out

- A running UC-09 attempt keeps its original expiresAt. Its last confirmed draft remains available after sign-in, or is finalized under UC-09 if the deadline passes.
- Logout never resets attempt count, grants extra time, marks a video complete, or cancels an enrollment.

A.4 — Current-session versus all-session behavior

- This endpoint accepts no allDevices parameter. UC-13/14 credential replacement retains its distinct account-wide session effect.
- Other browsers/devices remain signed in until their own expiry/logout or a credential change. Private content in a logged-out tab must not remain visible under another account.

Exception Flow:

E.1 — Unknown outcome

- On a lost/malformed logout response, hide private content and read UC-02's session endpoint once. Do not auto-repeat the logout POST.
- GET 401 confirms this browser has no usable session and completes guest navigation. GET 200 means a current session exists; show `You are still signed in. Try signing out again.` with visible account identity and a deliberate new Logout action.
- A failed session check leaves authentication unresolved; show Check session again. It must not announce successful logout or restore stale private content.

E.2 — Service failure

- LOGOUT_UNAVAILABLE follows the same reconciliation when termination may have occurred. No local-only cleanup is described as proof of server termination.
- A successful logout with a later failed Login-page session check remains a confirmed result for the ended session; do not revive its cached account state.

UI Integration:

- Account-menu entry: `11 Home Menu Student`, node `231:822`.
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=231-822
- Profile entry: `19 Profile`, node `222:436`.
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-436
- Logout appears in the menu metadata inspected for this file and the Profile screenshot inspected on 2026-09-20. No dedicated logout dialog/result design is claimed.
- Enable these existing actions; add unsaved-work/reconciliation feedback and the onboarding-header action as project supplements. Reuse the implemented Login screen after success. No new logout page or frozen/mobile dataset claim.

API Endpoint:

`POST /api/v1/auth/logout`

Reconciliation reuses `GET /api/v1/auth/session`.

Request Body:

No body or query parameters. The presented browser session identifies what is ended. Reject supplied body fields/query keys with VALIDATION_ERROR; do not accept email, userId, allDevices, password, or a JSON session token. Onboarding completion is not required.

Successful Response:

```json
{
  "success": true,
  "message": "You have signed out.",
  "data": {
    "signedOut": true
  }
}
```

HTTP 200, including already absent/ended sessions. signedOut is literal true for the presented session's completed termination/clearing. No account/session/token is returned. Browser credential clearing uses the existing project session transport.

Error Response:

```json
{
  "success": false,
  "statusCode": 503,
  "code": "LOGOUT_UNAVAILABLE",
  "message": "Sign-out is temporarily unavailable. Please try again later.",
  "timestamp": "2026-09-20T10:00:00.000Z",
  "path": "/api/v1/auth/logout"
}
```

Use the existing project envelope: success=false, statusCode matching HTTP status, code, message, server ISO UTC timestamp, and actual pathname without query. Omit data. Only VALIDATION_ERROR may add errors mapping input fields to nonempty arrays of strings. Every 429 includes positive integer retryAfterSeconds matching the Retry-After header. All success keys shown are required; dates/IDs are illustrative.

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

| HTTP | Code | Exact message |
| --- | --- | --- |
| 503 | LOGOUT_UNAVAILABLE | Sign-out is temporarily unavailable. Please try again later. |

Logout returns no 401 merely for an absent session and adds no rate limit. Reconciliation GET retains UC-02's own envelope/path and UNAUTHENTICATED/SESSION_UNAVAILABLE outcomes.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement current-session termination in NestJS/TypeScript through the existing UC-02 session store/transport. Treat absent/already-ended sessions as success; do not modify account eligibility or independent sessions. Keep UC-13/14 account-wide invalidation separate. No deletion of persistent Student data or cancellation of scheduled quiz expiry follows logout.

### Frontend UI Context

Enable shared Logout controls in React/TypeScript/Tailwind, including the onboarding entry. Add truthful save/discard choices for dirty pages and unresolved-result feedback. Reuse Login for completion; no unsupported confirmation screen is attributed to Figma.

### Frontend Logic and API Context

Resolve the active view's save before logout when requested, then submit once. Clear private caches and in-memory credentials/drafts after completion, and discard late responses from the old session. Reconcile ambiguous outcomes with GET session; only a confirmed unauthenticated state or logout success completes navigation. Do not persist a previous account's theme or quiz draft into the next account.

### Validation and Error-Handling Context

Validate the empty request contract and scope termination to the presented session. Distinguish ended current session from all-device termination, account deletion, and an uncertain network result. Preserve saved learning data and quiz deadline semantics; never promise that unsaved work survived a forced departure.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
