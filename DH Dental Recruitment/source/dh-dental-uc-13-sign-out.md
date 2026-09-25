# UC-13: Sign Out

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Sign Out

Description:

- Allows an actor to end the browser session presented to the application and return to the public job catalog.
- The source account menu contains Sign out. Session scope, idempotent behavior, reconciliation, destination, and response contract are project decisions needed to make that action functional.
- This is a current-session action. It does not close an account, switch account roles, delete saved profile content, or sign out independent browser sessions. UC-12 separately defines ending all pre-change sessions after a password change.

Primary Actor:

Actor using the current browser session, including a Job Seeker whose session has expired or whose account has become ineligible.

Preconditions:

- UC-02 browser sessions and GET session are implemented. UC-03 provides the public `/jobs` destination.
- The authenticated menu exposes a working Sign out action. A private-page/session-error state also provides a way to clear the presented session.
- No valid-session, verified-contact, profile-completion, or ACTIVE-account prerequisite prevents signing out. The endpoint is usable when no session exists.

Postconditions:

- Confirmed success: The session presented to the successful logout request is invalid for subsequent authenticated requests, its browser credential is cleared, account-specific UI/media/drafts are removed, and the actor reaches the public jobs page after session reconciliation.
- Already signed out: The request returns the same successful contract and leaves the browser without the presented session.
- Failure/unknown outcome: The interface does not falsely announce successful server sign-out. Private content is concealed while the actor retries or checks the actual session state.
- Other independent sessions and all persisted account/profile/preferences/media remain unchanged. Tabs sharing the same presented browser session lose that session on subsequent checks.

Main Flow:

1. Open the authenticated account menu and select Sign out.
2. If there is an unsaved form or local recording, ask whether to stay or discard that local draft and sign out. With no unsaved draft, proceed directly.
3. Stop local recording/playback and submit POST logout once for the browser's presented session. Hide private page content while the result is pending.
4. The backend ends that session if present and clears its browser credential, then returns the standard successful envelope.
5. GET the UC-02 session to determine the current browser state. A 401 confirms no usable session is currently presented.
6. Clear account-specific frontend data, close the menu, navigate to `/jobs`, and display the public header. After a confirmed logout response and the expected session check, show `Signed out successfully.`

Alternative Flow:

A.1 — No session, expired session, or repeat action

- POST returns the same 200 result when the cookie is absent, expired, unrecognized, or already invalidated. It must not return 401 merely because the actor is already signed out.
- A recognizable session belonging to an ineligible or unsupported-role account may still be ended. Logout does not require passing the feature eligibility rules used for profile edits.
- Repeated logout without an intervening login is harmless and does not delete account data. It must not revoke another independently established session.

A.2 — Unsaved draft or active capture

- An explicit Stay choice leaves the session and draft intact. Discard and sign out drops the local draft, stops capture/playback, and starts logout; persisted profile/media are not removed.
- If a profile/password/media write is already in progress, do not present logout as canceling that server write. Explain that it may complete and allow either Stay to resolve it or Sign out anyway. Ignore its late UI result after sign-out.
- A request already authorized before logout may complete; new authenticated requests using the ended session must fail. Signing out is not a rollback mechanism.

A.3 — Other sessions and public access

- Tabs sharing the browser session clear private UI on their next eligibility check or focus/reentry. Protected routes must confirm eligibility before redisplaying cached private content after browser Back.
- Independent browser/device sessions remain valid under UC-02. This action does not implement Sign out everywhere.
- Public `/jobs` and public job details remain available without sign-in. Member-only detail/media cannot be restored from an old component state after logout.

A.4 — Logout response lost

- Do not assume success or immediately issue another logout. GET session first.
- If GET returns 401, clear local private state and open `/jobs` with `No active session in this browser.` This reports the observed state without claiming proof of the lost mutation's result.
- If GET returns 200, show the actual current identity and an explicit Sign out again action. A new sign-in may have occurred meanwhile; do not automatically revoke it.
- If session checking fails, keep the state unresolved with Check session and Retry sign-out actions, each deliberate.

Exception Flow:

E.1 — Logout service unavailable

- A service failure must not claim that server-side revocation succeeded. Keep private content hidden and show the sign-out error with explicit Retry and Check session.
- Do not silently navigate to a signed-out success state merely because local caches were cleared. Do not erase evidence of an unresolved server session by treating a failed request as success.

E.2 — A session is still present after a successful response

- If the follow-up GET returns 200, render the identity it actually returns in the session-status message: `A session is still active. Review it before signing out again.`
- Do not assume it is the same session or automatically loop logout requests; another tab might have signed in. Require a deliberate new Sign out action if desired.

E.3 — Follow-up check unavailable

- After a 200 logout but a failed session check, say `Sign-out was accepted, but the current browser session could not be checked.` Keep private data hidden and offer Check session.
- The server response and current browser state are distinct evidence. Do not fabricate a 401 or a new identity to simplify the UI.

UI Integration:

- File DH Dental Recruitment (Community), Pages / Job Seeker (`1:2`).
- [Account dropdown, frame `2:4121`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4121): account name/email, Profile, Settings, other menu actions, and Sign out.
- Context/screenshot inspected on 2026-09-23. The menu item is design-supported; pending/error, unsaved-draft confirmation, session reconciliation, and public-header transitions are project supplements, not verified prototype behavior or a frozen dataset.
- Use the current UC-02 account identity and existing menu layout. Sign out is an action button, not an anchor that merely changes the URL.
- Make the menu keyboard-accessible and restore focus appropriately if the actor cancels a draft-discard prompt. A pending action disables duplicate activation.
- Make Profile Private, Close Account, and Switch Account are separate goals and are not enabled through this UC. Preserve their existing unavailable state until specified. `/jobs` is the existing real destination; do not create a dummy logout landing page.

API Endpoint:

- `POST /api/v1/auth/logout` — end only the session presented by the current browser request.
- Reuse `GET /api/v1/auth/session` from UC-02 for reconciliation; no schema change.

Logout accepts no query parameters and no request body. It accepts the browser credential using the existing session mechanism; it does not take a token, account ID, target session, or redirect URL in JSON.

Request Body:

None. Send a bodyless POST. An empty JSON object is still an unexpected body and returns VALIDATION_ERROR. Reject query parameters, including next, returnTo, allSessions, and accountId.

The server chooses no client-supplied target session. It ends only the session actually presented with this request. The public `/jobs` destination is a frontend integration decision, not an API redirect parameter.

Successful Response:

HTTP 200 for an ended session and for no usable presented session:

```json
{
  "success": true,
  "message": "Signed out successfully.",
  "data": {
    "signedOut": true
  }
}
```

data has exactly signedOut, always true. This confirms completion for the session presented to that request; it is not a guarantee that no later concurrent login can establish a session. No account object, credential, session ID, or revocation count is returned.

The endpoint clears the presented browser credential and makes a recognized current session unusable for subsequent authenticated requests. It does not create a new anonymous session. Repeating the operation without a new login returns the identical structure and does not affect independent sessions.

Error Response:

All errors contain success false, statusCode matching the HTTP status, code, message, timestamp (server UTC ISO 8601), and path (actual request pathname without query). Only VALIDATION_ERROR adds errors, mapping field paths to nonempty arrays of messages. A 429 additionally includes the positive integer retryAfterSeconds and an equal Retry-After header. Other errors omit these extensions. No error response contains data: null.

| HTTP | code | message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 503 | SIGN_OUT_UNAVAILABLE | Sign-out is temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

POST logout does not return 401/403 for an absent, expired, ineligible, or unsupported-role session, and introduces no endpoint-specific attempt limit. The follow-up UC-02 GET session retains its own errors, including 401 UNAUTHENTICATED and 503 AUTHENTICATION_UNAVAILABLE.

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-23T16:00:00.000Z",
  "path": "/api/v1/auth/logout",
  "errors": {
    "request": [
      "Send this request without a body or query parameters."
    ]
  }
}
```

```json
{
  "success": false,
  "statusCode": 503,
  "code": "SIGN_OUT_UNAVAILABLE",
  "message": "Sign-out is temporarily unavailable. Please try again later.",
  "timestamp": "2026-09-23T16:00:00.000Z",
  "path": "/api/v1/auth/logout"
}
```

## Project-Specific Implementation Context

### Backend Implementation Context

Reuse the NestJS/TypeScript session service established by UC-02. Logout resolves the presented browser session without requiring the ACTIVE JOB_SEEKER eligibility gate used by profile endpoints. A recognized session can be ended even after account eligibility changes.

Make that one session invalid for later authenticated requests and clear the presented browser credential before reporting a successful result. Absent/already-invalid sessions use the same 200 contract; repeated requests need no special client-generated operation ID. Backend unavailability must not be confused with a confirmed absent session.

Do not invalidate all sessions for the account. Independent sessions keep their existing UC-02 expiry and behavior. Do not mutate password, account status/role, contact flags, profileCompletionStatus, any profile section, notification preferences, or persisted media.

This UC specifies session lifetime behavior as observed by the application. It does not prescribe cookie flags, token algorithms, session storage implementation, or credential-digest construction. UC-12's account-wide invalidation after a password change remains a separate operation.

A protected operation accepted before logout can finish according to its own UC; logout does not promise to undo already authorized work. Every subsequent protected request must evaluate current session validity rather than relying on a cached signed-in UI.

### Frontend UI Context

Use the inspected account dropdown and the shared authenticated shell in React/TypeScript/Tailwind. Sign out invokes the API and exposes a pending state. Do not show a success toast on the initial menu click.

Before proceeding, handle unsaved local forms/recordings with the explicit Stay or Discard and sign out prompt. Do not imply that removing a local video preview deletes the saved UC-10 video. In-flight server writes receive the separate explanation in A.2.

While the result is pending or unresolved, conceal private content and show the actionable session/sign-out status. A deliberate retry remains available. After confirmed no-session state, render the actual public jobs header and list, not an authenticated shell with a replaced label.

### Frontend Logic and API Context

Send one bodyless POST logout after the explicit action. Stop capture/playback, discard confirmed-to-discard drafts, and prevent duplicate clicks while pending. Reconcile through UC-02 GET session after success or an ambiguous transport result using the exact cases above.

When no usable session is confirmed, clear cached identity, member job data/media, basic profile/photo, job preferences/recommendations, work experience/resume, education, introduction video, notification preferences, and any mounted password fields. These are local state changes; persisted backend data is retained.

Ignore late account-specific responses after a logout/account transition. Protected-route entry and tab focus/reentry recheck eligibility before revealing private cached content. Do not restore a former user's profile when another account signs in.

A GET session 200 after logout returns the current identity; do not assume the previous user or automatically log the new session out. Keep retry a deliberate action. A failed follow-up read is uncertainty, not evidence of no session. Public navigation never adds passwords, tokens, or private return paths to the URL.

### Validation and Error-Handling Context

Reject any body or query parameters with errors.request. Absence or expiry of the presented session is a successful idempotent condition, not an authentication error for POST logout. Keep this distinction from UC-02 session reads explicit in shared API error handling.

A successful POST means the targeted session was ended or already unusable; a follow-up session read determines what the browser currently presents. Preserve this distinction for concurrent login, timeout, and service-failure handling.

Never equate hiding local content with confirmed server revocation. Do not repeat logout automatically after discovering a current session, as it may belong to a new deliberate login. Failed sign-out must remain visible and recoverable without deleting persisted account data or pretending the account was closed.
