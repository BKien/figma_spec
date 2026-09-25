# UC-12: Change Password

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Change Password

Description:

- Allows a signed-in Job Seeker who knows their current password to replace it with a new password and then sign in again.
- The Figma form supplies a read-only email, current password, new password, repeated new password, and Save Changes. It is distinct from forgotten-password recovery, which remains unavailable under UC-02.
- Password interpretation follows UC-01/02. Current-password confirmation, observable attempt limits, session-ending behavior, errors, and API contract are explicit project decisions; implementation algorithms are not prescribed by this UC.

Primary Actor:

Authenticated ACTIVE JOB_SEEKER who knows their current password.

Preconditions:

- UC-01/02 account credentials and cookie-based sessions are implemented. The shared password policy is exactly 8–128 Unicode code points, with no trimming, normalization, or additional character-composition rule.
- `/settings/change-password` exists and reloads correctly. The Settings shell links it from Change Password; UC-11 supplies `/settings/notifications` for the neighboring tab.
- The credential service can commit a password replacement and end the account's existing sessions as one observable change. A credential change is not reported successful while old sessions remain usable for new authenticated requests.

Postconditions:

- Success: The new password is active, the old password no longer authenticates, and all sessions established before the successful change, including the submitting session, are no longer valid for new authenticated requests. The actor is directed to sign in again.
- Failure: Rejected validation/current-password/limit/conflict requests do not change the password or terminate otherwise valid sessions. An ambiguous network response is an unknown outcome, not an assumed failure.
- Email/mobile, profile sections, notification preferences, contact verification, account role/status, and global profileCompletionStatus are unchanged. No email, SMS, or recovery code is sent.

Main Flow:

1. Open Settings → Change Password and confirm the current UC-02 session.
2. Display the current account email read-only and three initially empty masked password fields.
3. Enter the current password, a different new password, and the same new password again.
4. Select Save Changes. Validate field presence, policy, and new-password confirmation, then submit once.
5. The backend checks eligibility and the change-password attempt allowance, verifies the current password against the current credential, and commits the replacement with termination of existing sessions.
6. On confirmed success, clear all password fields and authenticated frontend state, stop any account media capture/playback, and show `Password changed. Please sign in again.` on `/sign-in`.
7. Any subsequent login uses UC-02 with the new password and its ordinary Remember me/lifetime rules. No automatic login or session renewal occurs here.

Alternative Flow:

A.1 — Leave before submission

- Leaving the page discards all entered passwords. No autosave, credential check, or mutation occurs when a field loses focus.
- Use the settings tabs for navigation; no mandatory Cancel control is inferred from the source.

A.2 — Current session is absent

- Clear private form state and route through UC-02. Add exactly `/settings/change-password` to its accepted local next destinations, with no query/fragment, encoded as the next parameter.
- Contact verification false or INCOMPLETE profile does not block an eligible signed-in actor from changing their password.

A.3 — Current password is forgotten

- Explain that this page needs the current password. Keep UC-02's existing unavailable-recovery behavior; do not simulate sending a reset link or silently treat this as password recovery.

A.4 — Multiple active sessions

- A successful change ends the submitting session and every other session that predates that change. Other tabs sharing the browser session become unauthenticated on their next session/API check; separate browsers are also required to sign in again.
- A new session legitimately established after the change using the new credential follows UC-02 normally. Changing a password does not permanently prevent new sessions or close the account.

Exception Flow:

E.1 — Invalid new password or confirmation

- A new password outside the shared length policy, a confirmation mismatch, or a new password exactly equal to the submitted current password produces VALIDATION_ERROR without changing credentials.
- Display field feedback without interpreting whitespace differently from UC-01/02. No special-character, uppercase, or password-history requirement is added.

E.2 — Current password is incorrect

- Return CURRENT_PASSWORD_INCORRECT. Keep the current eligible session; do not confuse this 400 response with session expiry.
- Clear the current-password field and show the error. New-password fields may remain only in the mounted form for deliberate correction; clear every password on navigation, session change, success, or an ambiguous outcome.

E.3 — Observable change-password limit

- Allow at most five current-password evaluations per account and 30 per client IP in a rolling 15 minutes. Both successful and failed evaluations count; success does not reset either allowance. These budgets are independent of UC-02 sign-in budgets.
- Malformed/invalid requests and missing/ineligible sessions do not count because no current-password evaluation occurs. Reject over-budget requests with RATE_LIMITED before evaluation, and return the wait until both budgets allow another evaluation, rounded up to a positive whole second.
- Rate limiting does not end existing sessions or change the password. The actor must deliberately resubmit after the wait; the UI never retries credentials automatically.

E.4 — A concurrent change wins

- If the presented session is already invalid when evaluated, return UNAUTHENTICATED. If two requests began with a valid session but another credential change commits before this one can commit, return PASSWORD_CHANGE_CONFLICT for the losing request.
- A losing request must not overwrite the winning password based on an earlier current-password check. Clear its form and require session reconciliation/sign-in; do not retry it automatically.

E.5 — Response lost or service unavailable

- Clear passwords after an ambiguous transport failure and GET the UC-02 session. A 401 establishes only that the browser no longer presents a usable session; it does not by itself prove that the password changed.
- Show `The password change could not be confirmed. Please sign in to continue.` when the outcome is unknown and no usable session remains. Let the actor deliberately enter credentials through normal UC-02 login; do not automatically try old and new passwords.
- A 200 session read likewise does not prove that an in-flight change has failed. Keep an outcome-unknown state with Check session again and navigation back to Settings; any fresh password submission must be deliberate after reviewing current state, never a background retry.
- A service error before commit preserves the old credential/sessions. If commit status cannot be established, treat it as unknown rather than promise that nothing changed.

UI Integration:

- File DH Dental Recruitment (Community), Pages / Job Seeker (`1:2`).
- [Settings / Change Password, frame `2:4345`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4345): read-only email, three password inputs, settings tabs, and Save Changes.
- Context/screenshot inspected on 2026-09-23. Layout and visible controls are supported; submission, errors, limits, session termination, and responsive states are project supplements, not source-defined behavior or a frozen dataset.
- Use actual session email, not user@example.com. Inputs are empty and masked; source bullets are visual placeholders, not a stored password.
- Explain before Save that changing the password signs the account out of its existing sessions. Add the concise shared length guidance and a confirmation-mismatch message beside the relevant input.
- Preserve the source white card and teal settings banner. On narrow screens stack labels/fields. Notifications links to UC-11; Close Account and Switch Account remain unavailable until specified. No password is displayed in a toast, URL, or saved success message.

API Endpoint:

- `PUT /api/v1/auth/password` — replace the authenticated account password.
- Reuse `GET /api/v1/auth/session` from UC-02 only for eligibility/reconciliation; its contract is unchanged.

PUT accepts application/json, no query parameters, and no account ID. It does not accept an email or a session credential in the JSON body.

Request Body:

Exactly three required string fields:

```json
{
  "currentPassword": "ResearchDemo42!",
  "newPassword": "ResearchNext42!",
  "confirmNewPassword": "ResearchNext42!"
}
```

Each password string is 8–128 Unicode code points, exactly as entered; do not trim, case-fold, or normalize. confirmNewPassword must exactly equal newPassword. newPassword must differ from currentPassword. The server authoritatively checks these constraints as well as the actual current credential.

Reject unknown fields, missing/null/nonstrings, extra query parameters, and wrong request content type with VALIDATION_ERROR. The illustrative passwords are example values only; no seeded credential change or automatic submission is required.

Successful Response:

HTTP 200 only after a confirmed change:

```json
{
  "success": true,
  "message": "Password changed. Please sign in again.",
  "data": {
    "requiresSignIn": true
  }
}
```

data has exactly requiresSignIn, always true. No password, credential metadata, token, user object, old session, or new session is returned. The response ends the browser's presented session; all pre-change sessions fail later authenticated checks.

The frontend uses transient navigation state to show the success message on the existing `/sign-in` page; it does not add credentials or an arbitrary redirect to the URL. A successful change must not be followed by an automatic UC-02 login.

Error Response:

All errors contain success false, statusCode matching the HTTP status, code, message, timestamp (server UTC ISO 8601), and path (actual request pathname without query). Only VALIDATION_ERROR adds errors, mapping field paths to nonempty arrays of messages. A 429 additionally includes the positive integer retryAfterSeconds and an equal Retry-After header. Other errors omit these extensions. No error response contains data: null.

| HTTP | code | message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 400 | CURRENT_PASSWORD_INCORRECT | The current password is incorrect. |
| 401 | UNAUTHENTICATED | Please sign in to continue. |
| 403 | ROLE_NOT_ALLOWED | This action is not available for your account role. |
| 409 | PASSWORD_CHANGE_CONFLICT | Your password changed in another session. Please sign in again. |
| 429 | RATE_LIMITED | Too many password change attempts. Please try again later. |
| 503 | PASSWORD_CHANGE_UNAVAILABLE | Password change is temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-23T16:00:00.000Z",
  "path": "/api/v1/auth/password",
  "errors": {
    "confirmNewPassword": [
      "The new passwords must match."
    ]
  }
}
```

```json
{
  "success": false,
  "statusCode": 400,
  "code": "CURRENT_PASSWORD_INCORRECT",
  "message": "The current password is incorrect.",
  "timestamp": "2026-09-23T16:00:00.000Z",
  "path": "/api/v1/auth/password"
}
```

```json
{
  "success": false,
  "statusCode": 429,
  "code": "RATE_LIMITED",
  "message": "Too many password change attempts. Please try again later.",
  "timestamp": "2026-09-23T16:00:00.000Z",
  "path": "/api/v1/auth/password",
  "retryAfterSeconds": 240
}
```

The 429 example also has Retry-After: 240. Messages and limits are endpoint-specific; do not substitute UC-02's sign-in rate-limit wording or reset its independent budgets.

## Project-Specific Implementation Context

### Backend Implementation Context

Require UC-02's cookie-based session for an ACTIVE JOB_SEEKER. Missing, expired, or account-ineligible sessions return 401 UNAUTHENTICATED. An otherwise valid unsupported-role session returns 403 ROLE_NOT_ALLOWED. An incomplete profile and unverified contact flags do not block this feature. Resolve the account from its session; no caller-supplied account identifier is accepted.

Reuse UC-01/02 Account credentials and the existing session service in NestJS/TypeScript. Do not create a second password store or change the shared password policy. Validate the input, apply the observable change-password budget, and compare the presented current password against the current persisted credential.

A successful change and invalidation of all sessions predating it form one observable outcome. Concurrent requests must not both commit based on the same superseded credential. Recheck the condition needed for a valid change at commit; expose the specified conflict/session result instead of overwriting the winner.

This UC specifies externally visible credential/session behavior only. It does not select password hashing, session-token formats, cryptographic algorithms, cookie flags, or limiter storage algorithms. Preserve UC-02's ordinary 8-hour/30-day lifetimes for sessions established by future logins; do not extend a session here.

Do not require a complete profile, verified email/mobile, email delivery, SMS, or knowledge of an account ID. Changing a password does not reset profile sections, preferences, account status, or professional declarations.

### Frontend UI Context

Use the source React/TypeScript/Tailwind settings form and the existing account identity display. Treat passwords as local form values, initially empty, and never prefill from source bullets or echo submitted strings in errors.

Show the sign-out consequence before Save. Distinguish a wrong current password from confirmation mismatch, session expiry, rate limiting, service failure, and unknown outcome. A positive wait message may count down, but reaching zero only re-enables deliberate submission.

On confirmed success, remove authenticated page content and show the sign-in message. On an unknown outcome, use the uncertainty message rather than the success message. Loading and submit-pending states prevent duplicate Save actions without freezing navigation indefinitely.

### Frontend Logic and API Context

Confirm the UC-02 session, render its email, and hold the three passwords only in the mounted form. Validate length and exact new-password equality for immediate feedback; send exactly the request schema once per deliberate Save.

Handle CURRENT_PASSWORD_INCORRECT as a form error, not as a global logout trigger. Handle 401 by clearing authenticated state; 409 clears the password form and reconciles/signs in as described. Map 429 to the returned delay without automatic retries or budget guesses.

A confirmed 200 clears all password fields, account-specific caches/drafts, and any active UC-10 recording/media before navigation to `/sign-in`. Other tabs discover invalidation through their next session/API check; the app should also refresh eligibility on protected-page reentry. Do not claim an already executing protected request was retroactively undone.

An ambiguous network result clears entered passwords and invokes the exact reconciliation flow. Never serialize them into local persistence, browser history, query parameters, navigation state, or diagnostic UI. Do not automatically submit either old or new credentials to diagnose a changed password.

### Validation and Error-Handling Context

Use currentPassword, newPassword, confirmNewPassword, and request error paths. Apply the same exact Unicode length and no-normalization policy as registration/sign-in. Equal new/current strings and mismatched confirmation fail validation before current-password evaluation; no password-history or extra composition rule is inferred.

The limit counts evaluations only, including a concurrent evaluation whose later commit loses. Retry-After and retryAfterSeconds agree and represent the next time both budgets can allow evaluation. Reaching that time does not guarantee authentication or success.

Current-password rejection and validation errors do not terminate otherwise valid sessions. Confirmed credential change does terminate pre-change sessions; ambiguous transport failure does not establish whether that happened. Keep those outcomes distinct in UI and API handling, with no fabricated reset email or success state.
