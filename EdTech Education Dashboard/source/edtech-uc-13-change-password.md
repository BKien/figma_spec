# UC-13: Change the Current Account Password

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Change the Current Account Password

Description:

- Allows a signed-in Student to replace their password after entering the current password, then sign in again with the new password.
- Enables the Change Password / Password Change entries in the source account/security settings. The actual password form is a project supplement; the file provides menu entries only.
- Eligibility, session termination, limits, and API contract are business requirements for the experiment. This UC contains no cryptographic, cookie-flag, or limiter implementation prescriptions.

Primary Actor:

Authenticated Student changing their own password.

Preconditions:

- UC-01's account identity/password policy and UC-02's browser session exist. Require an ACTIVE, verified STUDENT session.
- Onboarding completion is not required for this account-maintenance operation. An incomplete Student can reach `/student/settings/password` directly or through a supplementary Change password link in the onboarding shell/header.
- Register `/student/settings/account`, `/student/settings/security`, and `/student/settings/password` with reload support. The first two implement the inspected menus as navigation surfaces; neither creates an additional use case.

Postconditions:

- Success: The new password is effective; all previously issued sessions for this account, including the current one, are ended. All outstanding password-recovery grants for the account become unusable. The user must sign in again.
- Failure: A rejected request changes neither password nor sessions. A service response with unknown outcome does not justify claiming the password remained unchanged.
- Account role, verification, onboarding, enrollment, profile, saved settings, learning progress, and quiz attempts remain intact. A running quiz deadline is not paused.

Main Flow:

1. The Student selects Change Password from an implemented account/security menu.
2. The supplementary form requests Current password, New password, and Confirm new password; explain that success signs out all devices.
3. The Student enters values and selects Change password. Validate the form and submit once.
4. The backend checks the current session, request limits, current password, and new-password policy against the latest account credential state.
5. Commit the new credential, end pre-existing sessions, and invalidate outstanding recovery grants as one completed outcome before returning success.
6. Clear password fields and private frontend state, complete browser-session clearing, and open `/sign-in` with `Password changed. Please sign in again.`
7. UC-02 accepts the new password and applies its existing onboarding routing. The old password no longer authenticates.

Alternative Flow:

A.1 — Password values and cancel

- Passwords follow UC-01: 8–128 Unicode code points, exact entered values with no trimming/normalization. Confirmation must match. The new password must differ from the current password; no additional composition rule is introduced.
- Visibility toggles affect display only. Cancel clears all password fields and returns to the previous implemented settings page, or onboarding/dashboard according to current account state.
- Passwords are never persisted across reload. Do not add a Remember Me option to this form.

A.2 — Source settings menus

- Enable Account Settings and Security & Privacy sidebar entries. Both password items navigate to the same form. Settings menu entry remains compatible with UC-11's implemented landing route.
- Change Email, Connected Accounts, 2-Factor Authentication, Active Sessions, Download My Data, and Delete My Account remain disabled with explanations until their own UCs. Do not imply that merely displaying those entries implements them.
- Students still in onboarding may use account/security/password routes, but returning to learning preferences, notifications, profile, or learning routes still obeys each UC's onboarding requirement.

A.3 — Observable limit

- Permit five current-password evaluations per account and twenty per client IP in a rolling 15 minutes. Successful and unsuccessful evaluations count; malformed requests and unauthenticated requests do not consume an evaluation.
- Deny further evaluations with 429 RATE_LIMITED until both budgets allow one. Denied requests do not extend the wait. Existing sessions remain valid unless a password change succeeds; this limit is independent of UC-02 login limits.

A.4 — Concurrent credential changes

- A change must validate the current password against the same credential state it replaces. Two competing changes using the same old credential cannot both succeed as independent replacements.
- A competing successful change/recovery makes an old session unusable. Return 401 if it is no longer eligible, or CURRENT_PASSWORD_INCORRECT if the session is still valid but the supplied current password fails. Do not return the winning password or account details.
- A later legitimate sign-in using the new password creates a new session and is not undone by a delayed success response from this completed operation.

Exception Flow:

E.1 — Validation or incorrect current password

- Invalid fields return VALIDATION_ERROR; the same new/current password returns NEW_PASSWORD_UNCHANGED. A wrong current password returns CURRENT_PASSWORD_INCORRECT without changing credentials.
- Preserve only non-sensitive navigation/form feedback; clear password fields on a rejected credential attempt and require re-entry. Session expiry returns to Sign in.

E.2 — Unknown outcome

- After timeout/malformed response or an ambiguous 503, clear password fields and show `We could not confirm the password change. Sign in again; if it succeeded, use your new password.` Do not automatically repeat the POST.
- A session read may determine whether this browser remains signed in, but 401 alone does not prove the password changed. Provide a Sign in link and UC-14 recovery link when installed. If a session remains valid, the user can deliberately revisit the form and re-enter the current password.
- Never infer successful credential replacement merely from local cookie removal or redirect.

UI Integration:

- `20 Settings Account`, node `222:334`, and `23 Security & Privacy`, node `222:2`.
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-334
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-2
- Live contexts/screenshots inspected on 2026-09-20. The menu labels and settings-shell composition are verified. No current/new-password form or success/error state is present in these frames.
- Add a three-field form with labelled password visibility controls, Change password, Cancel, and all-device sign-out explanation using the existing settings styling. It is explicitly a project-designed UI addition, not a verified Figma frame. No mobile/frozen dataset claim.

API Endpoint:

`POST /api/v1/auth/password/change`

Request Body:

```json
{
  "currentPassword": "ExamplePass123!",
  "newPassword": "NewExamplePass456!",
  "confirmNewPassword": "NewExamplePass456!"
}
```

Exactly three required string keys; no query parameters. Enforce the common length/exact-value policy. No email, accountId, role, session selector, token, or onboarding field is accepted. The current session identifies the account.

Successful Response:

```json
{
  "success": true,
  "message": "Password changed. Please sign in again.",
  "data": {
    "passwordChanged": true,
    "signedOut": true
  }
}
```

HTTP 200. Both booleans are literal true and describe the completed operation: credential replaced and its pre-existing account sessions ended. No account, password, session, or token is returned. Repeating the request with the old session after success yields 401; this UC does not promise an unauthenticated replay receipt. Browser credential clearing follows the existing cookie-session integration.

Error Response:

```json
{
  "success": false,
  "statusCode": 503,
  "code": "PASSWORD_CHANGE_UNAVAILABLE",
  "message": "Password change is temporarily unavailable. Please try again later.",
  "timestamp": "2026-09-20T10:00:00.000Z",
  "path": "/api/v1/auth/password/change"
}
```

Use the existing project envelope: success=false, statusCode matching HTTP status, code, message, server ISO UTC timestamp, and actual pathname without query. Omit data. Only VALIDATION_ERROR may add errors mapping input fields to nonempty arrays of strings. Every 429 includes positive integer retryAfterSeconds matching the Retry-After header. All success keys shown are required; dates/IDs are illustrative.

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

| HTTP | Code | Exact message |
| --- | --- | --- |
| 401 | UNAUTHENTICATED | You must sign in to continue. |
| 400 | CURRENT_PASSWORD_INCORRECT | Your current password is incorrect. |
| 400 | NEW_PASSWORD_UNCHANGED | Choose a password different from your current password. |
| 429 | RATE_LIMITED | Too many requests. Please try again later. |
| 503 | PASSWORD_CHANGE_UNAVAILABLE | Password change is temporarily unavailable. Please try again later. |

## Project-Specific Implementation Context

### Backend Implementation Context

Implement authenticated password replacement in NestJS/TypeScript using UC-01 credentials and UC-02 sessions. The current credential check, replacement, pre-existing-session termination, and invalidation of UC-14 grants must describe one coherent success. Reject client identity selection and preserve all unrelated account/learning state. Expose the declared observable limit without prescribing a storage or security algorithm.

### Frontend UI Context

Build the supplementary form and activate the two inspected menu entry points in React/TypeScript/Tailwind. Use clear all-device sign-out wording and disabled unsupported settings entries. Do not render success before the response or turn the account settings page into a fake feature catalogue.

### Frontend Logic and API Context

Serialize submission, clear password values on exit/result, and navigate to existing `/sign-in` after confirmed success. Discard obsolete private reads and in-memory drafts. On ambiguous outcome use the explicit uncertainty message; session checks determine authentication only, not whether a new password took effect. Existing saved quiz/progress data is preserved while unsaved local work may be lost.

### Validation and Error-Handling Context

Match UC-01/02 password semantics exactly. Apply current-account eligibility, limits, differing-new-password validation, and concurrent-change rules. Do not auto-retry credential replacement, claim success from a 401, or pause a quiz deadline during credential recovery. No functional tests or Prompt E implementation recipes are included.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
