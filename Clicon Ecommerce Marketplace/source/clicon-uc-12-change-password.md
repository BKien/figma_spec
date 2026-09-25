# UC-12: Change Password

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Change Password While Signed In

Description:

- Allows an authenticated customer who knows the current password to replace it from the account-settings Change Password panel.
- Extends `/account/settings` from UC-11 and reuses UC-01's password policy, UC-02's session integration, and UC-03's recovery route.
- Current-password verification, session outcomes, submission limits, and API contracts below are project decisions. Figma establishes the observed three-field desktop panel and controls.
- Forgotten-password recovery remains UC-03. This UC does not change email, profile fields, account status, shopping collections, or previously placed orders.

Primary Actor:

Signed-in Customer with an active, verified account who knows the current password.

Preconditions:

- UC-02 provides an unexpired browser session for an active, verified account.
- `/account/settings`, `/sign-in`, and `/forgot-password` exist through UC-11, UC-02, and UC-03.
- Shared account/password contracts and success/error envelopes apply.

Postconditions:

- Success: The new password replaces the current password. All existing account sessions, including the requesting session, end; outstanding password-recovery links become unusable. The customer must sign in again.
- Success: Primary email, verification, account status, profile values/revision, and order snapshots remain unchanged. Browser-scoped cart, wishlist, and comparison remain available under their existing lifetime rules.
- Failure: A rejected request changes no password and ends no sessions merely because the attempt failed. An uncertain response is not proof of failure or success.
- No automatic login, email notification, new account, or password history feature is introduced.

Main Flow:

1. The customer opens `/account/settings` and the frontend resolves the current session using UC-02.
2. The Change Password panel shows empty Current Password, New Password, and Confirm Password fields, initially masked.
3. The customer enters the current password and a matching new password/confirmation.
4. The customer selects `CHANGE PASSWORD`. The frontend validates the inputs and sends `POST /api/v1/auth/change-password` once.
5. The backend checks authentication, the submission limit, request validity, and the current password, then completes the declared password/session/recovery-link outcome.
6. The API returns HTTP 200 with `Password changed successfully. Please sign in.`
7. The frontend clears all password values, clears authenticated account UI state, navigates to `/sign-in`, and shows the returned success message.
8. Subsequent sign-in uses the new password under UC-02. The old password no longer authenticates the account.

Alternative Flow:

A.1 — Show or hide a password

- Each eye button toggles only its associated field, preserves its value, and does not submit the form. All fields return to masked state after leaving or resetting the panel.

A.2 — Customer cannot remember the current password

- Provide a supplementary `Forgot your password?` link to `/forgot-password`. Clear the change-password form when navigating away.
- UC-03 owns the email recovery process; this panel does not accept a recovery code or bypass the current-password requirement.

A.3 — Independent settings forms

- The Change Password button submits only the three password fields. UC-11's SAVE CHANGES does not submit or persist them.
- If the profile form has unsaved edits, show `Save your profile changes first; changing your password will sign you out.` Disable password submission until the profile draft is saved or the page is deliberately reloaded to discard it.
- No combined profile-and-password save is introduced. Reloading discards all local password inputs.

Exception Flow:

E.1 — Invalid or mismatched fields

- Invalid request shape, invalid password lengths, mismatched confirmation, or a new password identical to the supplied current password returns HTTP 400 VALIDATION_ERROR.
- Local validation highlights the relevant fields without submitting. Server rejection clears password fields and displays feedback for re-entry.

E.2 — Incorrect current password

- A validly shaped request with an incorrect current password returns HTTP 400 CURRENT_PASSWORD_INCORRECT.
- Display `Current password is incorrect.` near Current Password and clear all three password inputs. The current session remains usable unless it independently expires or is ended elsewhere.
- Do not use 401 for this condition; 401 means authentication itself is no longer valid.

E.3 — Authentication ended or account no longer eligible

- A missing/expired session, or an account no longer active/verified, returns HTTP 401 UNAUTHENTICATED.
- Clear password and displayed account state, then navigate to `/sign-in`. Never automatically resubmit the password change after reauthentication.

E.4 — Submission limit reached

- Return HTTP 429 PASSWORD_CHANGE_RATE_LIMITED with retryAfterSeconds and a matching Retry-After header.
- Clear password inputs, display the remaining wait, and disable submission until it ends. The customer may manually submit after re-entering values; no automatic retry occurs.
- Reaching this limit does not permanently lock the account or change its status.

E.5 — Service failure or uncertain result

- A definite service rejection displays the documented error. For a lost, unreadable, or otherwise inconclusive response, clear password inputs and show `We could not confirm whether your password changed.` Do not claim success or automatically resend the request.
- Check `GET /api/v1/auth/session` once. If it returns 401, navigate to Sign In with `Try your new password. If you cannot sign in, use password recovery.` Session absence alone is not a success confirmation.
- If the session check succeeds, remain on Settings with the uncertain-result message. The customer may make a deliberate new attempt by re-entering all fields, or choose password recovery. Session presence is not treated as proof that an earlier operation cannot still complete.
- If the session check fails temporarily, keep submission disabled and offer `Check session again`. Do not add a separate result endpoint or store a plaintext password to replay later.

E.6 — Competing password changes or recovery

- A change must still be valid for the account's current credential/session state when completed. An earlier current-password check cannot authorize overwriting a password already changed by another request.
- Competing requests must not both succeed using the superseded password. A session ended by the winning change receives UNAUTHENTICATED; otherwise an incorrect current password follows E.2.
- The frontend handles the returned state without automatically repeating the operation or changing the account identity.

UI Integration:

- Parent frame: `34_Dasboard_Setting`, node `478:17305`.
- Inspected panel: `Change Password`, node `493:12618`, desktop 984 × 420.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=493-12618
- Live metadata, design context, and the panel screenshot were inspected on 2026-09-18. No frozen dataset, responsive frame, or separately designed feedback state is claimed.

| Observed element | Integration |
| --- | --- |
| CHANGE PASSWORD heading | Settings panel heading |
| Current Password | currentPassword |
| New Password; 8+ characters placeholder | newPassword using the shared policy |
| Confirm Password | confirmPassword matching newPassword |
| Eye icon in each input | Independent visibility toggle |
| CHANGE PASSOWRD button | Correct spelling to CHANGE PASSWORD; submit this panel only |

- Replace UC-11's disabled Change Password integration area with this working panel on `/account/settings`; do not create a duplicate settings page.
- Preserve the vertical field arrangement, Public Sans, light borders (#E4E7E9), and orange button (#FA8232). Keep the account/profile and still-unimplemented address areas under their existing scope.
- Field errors, progress/wait feedback, uncertain-result feedback, the recovery link, and the unsaved-profile notice are project supplements styled consistently with the source.
- Add concise policy guidance `At least 8 characters, up to 72 UTF-8 bytes.` Do not infer additional uppercase, digit, symbol, or password-history rules from the placeholder.
- Success feedback belongs on the existing Sign In page. This UC does not add a new success modal, email screen, or authenticated destination after changing the password.

API Endpoint:

`POST /api/v1/auth/change-password`

Uses the existing browser session. Session inspection for recovery reuses `GET /api/v1/auth/session` unchanged.

Request Body:

```json
{
  "currentPassword": "PreviousExample123!",
  "newPassword": "NewExample456!",
  "confirmPassword": "NewExample456!"
}
```

- Exactly these three required string keys; reject unknown keys, query parameters, missing values, null, and nonstrings. The session identifies the account; no email/account ID or recovery code is accepted here.
- Preserve password values exactly: do not trim, lowercase, normalize, or silently truncate them.
- currentPassword is nonempty and at most 72 UTF-8 bytes. Do not apply a new-password minimum to an existing credential check.
- newPassword has at least 8 Unicode code points and at most 72 UTF-8 bytes, matching UC-01/UC-03. It must differ exactly from currentPassword.
- confirmPassword must match newPassword exactly and satisfy the same input size bounds.
- Example strings illustrate field contracts, not fixed credentials or recommended passwords.

Observable submission limit:

- Admit at most five change-password requests per authenticated account and thirty per client IP in any preceding fifteen minutes. These budgets are independent of sign-in and recovery limits.
- For an authenticated request, admitted requests count whether they succeed, have invalid fields, or contain an incorrect current password. Unauthenticated requests receive 401 and do not consume this endpoint's account budget.
- Once either applicable budget is exhausted, reject with 429 before checking the submitted current password. Rejected requests do not extend the exhausted budget's wait; retryAfterSeconds is the positive whole-second wait until all applicable budgets permit another request.
- These are externally observable experiment rules. Counter storage, password-storage algorithms, cryptographic mechanisms, and cookie-policy details are not prescribed by this UC.

Successful Response:

HTTP 200:

```json
{
  "success": true,
  "message": "Password changed successfully. Please sign in.",
  "data": {
    "requiresSignIn": true
  }
}
```

- All shown fields are required; requiresSignIn is literal true. No password, authentication token, or replacement authenticated session is returned.
- Success means the password replacement and required session/recovery-link invalidation outcomes are complete. A subsequent check of any previously active session returns 401 unless a separate new login has since established another session.

Error Response:

Use the shared envelope, without data. timestamp is server-generated ISO 8601 UTC; path is `/api/v1/auth/change-password` for this operation.

```json
{
  "success": false,
  "statusCode": 400,
  "code": "CURRENT_PASSWORD_INCORRECT",
  "message": "Current password is incorrect.",
  "timestamp": "2026-09-18T10:00:00.000Z",
  "path": "/api/v1/auth/change-password"
}
```

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-18T10:00:00.000Z",
  "path": "/api/v1/auth/change-password",
  "errors": {"confirmPassword": ["Passwords do not match."]}
}
```

```json
{
  "success": false,
  "statusCode": 429,
  "code": "PASSWORD_CHANGE_RATE_LIMITED",
  "message": "Too many password-change attempts. Please try again later.",
  "timestamp": "2026-09-18T10:00:00.000Z",
  "path": "/api/v1/auth/change-password",
  "retryAfterSeconds": 120
}
```

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | `Please correct the highlighted fields.` |
| 400 | CURRENT_PASSWORD_INCORRECT | `Current password is incorrect.` |
| 401 | UNAUTHENTICATED | `You must sign in to continue.` |
| 429 | PASSWORD_CHANGE_RATE_LIMITED | `Too many password-change attempts. Please try again later.` |
| 503 | PASSWORD_CHANGE_UNAVAILABLE | `Password change is temporarily unavailable. Please try again later.` |
| 500 | INTERNAL_ERROR | `Unable to complete your request. Please try again later.` |

- Optional errors appears only for VALIDATION_ERROR and maps request field names to nonempty arrays of messages. A new password equal to currentPassword maps to newPassword with `Choose a different new password.`
- retryAfterSeconds appears only on 429 and matches the Retry-After header. The example 120 is illustrative; the server calculates the actual wait.
- Session-read errors retain UC-02's endpoint path and contract rather than being relabeled as password-change errors.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement the authenticated change-password endpoint in NestJS using the existing account/session/recovery models.

- Resolve the current active, verified account, apply the declared submission budget, and validate the exact body. Keep password change separate from profile PUT and email recovery.
- Verify the submitted current password against the account's current credential and enforce the shared new-password input policy. No alternative account identity is accepted in the request.
- Complete password replacement, termination of existing sessions, and invalidation of outstanding recovery links as one business outcome. Do not report success for a partially completed outcome.
- Preserve current-state correctness when password change and recovery requests compete. A request authorized using a superseded credential/session must not overwrite a more recent completed replacement.
- Leave profile revision, primary email, verification/status, orders, and browser shopping collections unchanged. No email delivery or new session is part of this endpoint.

### Frontend UI Context

Implement the existing Change Password panel inside UC-11's `/account/settings` using React, TypeScript, and Tailwind CSS.

- Replace only the disabled password area with the verified three-field layout. Keep its form submission separate from Account Setting's SAVE CHANGES.
- Start all fields empty/masked and provide independent, accessible show/hide controls that are not submit buttons.
- Show validation at the relevant field and request-level feedback within the panel. Disable submission while pending, rate-limited, uncertain without a resolved session check, or blocked by an unsaved profile draft.
- Use the existing Sign In and Forget Password routes for completion/recovery. No new password-result screen or duplicate account page is required.

### Frontend Logic and API Context

- State includes the three inputs, independent visibility flags, validation messages, request feedback, submitting state, retry deadline, and uncertain-result/session-check state.
- Keep password inputs independent of profile payload/state. Client validation errors leave values available for correction; after an unsuccessful server submission, clear all three inputs before re-entry.
- Send exactly one change request per deliberate submit. Prevent duplicate submits from double-click or keyboard/button overlap.
- On confirmed success, clear password and account UI state and navigate to Sign In with the documented success message. Do not follow the change with an automatic login using the entered new password.
- On 401, clear account/password state and navigate to Sign In without declaring that the password changed. On 429, use the reported wait and require manual re-entry/submission later.
- On uncertain results, clear inputs and follow E.5's session check. Never use a valid/invalid session alone as proof of which password is currently stored.
- Leaving/reloading the panel clears password values and visibility state. Obsolete responses after account navigation must not populate another account's form or automatically repeat a mutation.

### Validation and Error-Handling Context

- Apply Unicode-code-point minimum and UTF-8-byte maximum consistently with UC-01/UC-03. Never truncate a long input to make it pass.
- Distinguish malformed input, incorrect current password, missing authentication, throttling, and temporary service failure. Only definitive 401 triggers the authentication-expiry behavior.
- Correctable rejected attempts do not invalidate otherwise usable sessions or recovery links. Successful changes apply the complete declared invalidation outcome.
- Display unknown results candidly, with session-check/recovery actions; do not infer success from a subsequent session expiry or claim rollback merely because a response was lost.
- Shared account/profile values must not be submitted through this endpoint. No password field may become part of the profile GET/PUT response contract.
- The feature ends at requiring a new UC-02 sign-in. Password recovery remains a distinct UC-03 flow when the current credential is unknown.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
