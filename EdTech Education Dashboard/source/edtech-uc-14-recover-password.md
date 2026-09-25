# UC-14: Recover a Forgotten Password

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Recover a Forgotten Password

Description:

- Allows an eligible Student to request a password-recovery email, open a time-limited link, and set a new password without knowing the old one.
- Enables UC-02's Forgot Password entry. Email-request/reset forms and link-based recovery are project-designed additions; only the entry link is supplied by Figma.
- Uses local Mailpit for the experiment, as UC-01 does. This is account recovery, not registration verification or automatic sign-in.

Primary Actor:

Visitor who controls the email address of an ACTIVE, verified STUDENT account.

Preconditions:

- UC-01 account/email normalization and UC-02 credential/session behavior exist. Pending registrations are not eligible accounts.
- Implement `/forgot-password` and `/reset-password` routes with reload support. The email links to the configured application origin and carries an opaque recovery token in its URL fragment.
- The local email outbox and Mailpit adapter are configured. The researcher can open the Mailpit inbox to retrieve the link; no real external mailbox is required.

Postconditions:

- Request accepted: The service has durably accepted the request for processing. This does not reveal whether the email belongs to an account or promise that a message arrived.
- Reset success: The password is replaced once, all pre-existing sessions and recovery grants for that account are ended/invalidated, and the user must sign in again.
- Failure: An invalid/expired grant or rejected reset changes no password. Profile, enrollment, onboarding, preferences, learning progress, and quiz deadlines are unchanged.

Main Flow:

1. The visitor selects Forgot Password on Login and submits an email address on `/forgot-password`.
2. The service validates format/limits and accepts a uniquely identified request, returning the same generic 202 response regardless of account existence/eligibility.
3. For an eligible account, process a recovery message through Mailpit with a single-use link expiring 15 minutes after request acceptance. Unknown/ineligible emails produce no message.
4. The visitor opens `/reset-password#token=<value>`. The frontend reads the token into this page's memory, removes the fragment from the visible URL, and displays New password and Confirm new password.
5. The visitor selects Reset password; submit the token and matching new password with a completionRequestId.
6. The backend validates the grant and current account eligibility/credential state, replaces the password, consumes the grant, invalidates other grants, and terminates pre-existing sessions.
7. Clear token/password state and show `Password reset. Please sign in again.` with a link to `/sign-in`. No session is created by recovery.

Alternative Flow:

A.1 — Generic request outcome and limits

- The exact accepted response applies to unknown, inactive, unverified, and pending-registration emails as well as eligible accounts. It has no account/grant ID, delivery status, or code.
- Permit three new requests per normalized email and ten per IP in a rolling hour, plus a 60-second minimum interval per normalized email. Count accepted requests whether or not the email is eligible. A rejected limit request does not extend the wait.
- Identical requestId/email replays return the original generic 202 without a second email or new limit consumption. Reuse of that ID with another normalized email returns REQUEST_CONFLICT. Keep this request association for 24 hours, then expire it; the client uses a fresh ID for a genuinely new request.
- A lost response permits a deliberate same-ID/email retry. A deliberate later new request uses a new ID and obeys the same limits. Do not auto-request recovery in a loop.

A.2 — Outbox and email semantics

- 202 means durable request acceptance, not SMTP delivery. If the outbox cannot accept a request, return RECOVERY_UNAVAILABLE consistently before account-specific delivery processing.
- The adapter makes one local SMTP attempt with a five-second timeout; success means Mailpit accepted the message. There is no automatic delivery retry in this baseline. Rejection/timeout invalidates that new grant; any delayed message from an ambiguous SMTP result may contain an unusable link.
- Process only before the 15-minute expiry; delayed jobs after expiry send nothing. The message includes the exact expiry and explains that the link may expire. Do not extend expiry because processing was delayed.
- Issuing an additional link does not invalidate an earlier unexpired link. A successful reset or UC-13 password change invalidates all outstanding grants. Pending jobs are bound to the credential state at request acceptance and must not issue a usable link after that state changes.
- Recovery is an account-verification message and is unaffected by UC-12 learning-notification preferences.

A.3 — Link, reset, and replay

- No separate token-validation GET is required; opening the form does not prove the token is valid. Submit checks all grant rules. Missing token shows Request a new link; a reload after fragment removal requires reopening the email link.
- The token is not returned in the request API's JSON. Treat it as an opaque string, not as an account selector or a registration code.
- A completed reset may return its original success receipt for 24 hours only when the same token, completionRequestId, and exact normalized payload are repeated. This replay performs no password replacement, session termination, or credential-state rollback. It acknowledges the earlier completed reset, not proof the password has not changed again since.
- Reusing the same completionRequestId with different content returns REQUEST_CONFLICT. A consumed token under a different completion ID, or replay outside the receipt window, returns RECOVERY_LINK_UNAVAILABLE.
- At most one competing completion with a grant succeeds. Concurrent grants from the same prior credential state cannot perform two successive replacements using stale authority.

A.4 — New password and session context

- Match UC-01's 8–128 Unicode code points with no password trimming/normalization. Confirmation must match and new password must differ from the current credential; reject unchanged password only after a valid grant is established.
- If a browser has a session for the recovered account, clear it after success. A session for a different account is not ended by recovery; show the recovered-account reset receipt without logging into it. UC-15 provides deliberate sign-out before switching accounts.
- Onboarding need not be completed to recover an account. Instructor recovery will require its own eligibility extension; it is not silently enabled here.

Exception Flow:

E.1 — Invalid/expired/replaced grant

- Missing, unknown, expired, consumed, invalidated, credential-stale, or currently ineligible-account grants return the same RECOVERY_LINK_UNAVAILABLE message. This includes tokens created before a successful UC-13 change.
- Show Request a new link. Do not expose account identity, old-password state, verification flags, or another reset's details.

E.2 — Invalid input

- Malformed request email/password/body returns VALIDATION_ERROR. Apply common email normalization. A structurally valid but unavailable token uses the generic link error, not an account-existence response.
- The reset endpoint permits at most twenty new grant evaluations per IP in 15 minutes, separate from request limits. Accepted exact completion replays do not consume another evaluation. 429 includes the wait and creates no credential mutation.

E.3 — Ambiguous reset response

- Freeze the pending token/completion ID/password payload in memory for a deliberate exact retry; no automatic POST and no fresh completion ID while the outcome is unknown. Do not persist passwords/token across page reload.
- The visitor may leave for Sign in after clearing sensitive draft values; explain that the reset might have succeeded. A fresh link remains available if they cannot sign in.
- Session 401 alone does not establish that recovery succeeded. A definite success receipt does; show it once and clear the sensitive draft.

UI Integration:

- Entry: `02 Login`, node `222:2528`, visible Forgot Password link.
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-2528
- Login live context/screenshot inspected on 2026-09-20. No dedicated recovery/reset frame was found in the inspected Student-page inventory.
- Add email-request and two-password reset forms using the existing yellow/white authentication shell. Include generic request confirmation, expired-link recovery, pending/error feedback, and Back to Login. These forms and email-link behavior are project supplements, not Figma-verified UI. No frozen/mobile dataset claim.

API Endpoint:

`POST /api/v1/auth/password-recovery/requests`

`POST /api/v1/auth/password-recovery/complete`

Request Body:

Request email:
```json
{
  "requestId": "9bbeb9ea-3338-43b5-9ea4-e82b3c6a93c9",
  "email": "alex@example.com"
}
```

Complete reset:
```json
{
  "completionRequestId": "b894609f-4666-48ef-bd0e-2d652ebae1c1",
  "token": "example-opaque-recovery-token-from-the-email",
  "newPassword": "NewExamplePass456!",
  "confirmNewPassword": "NewExamplePass456!"
}
```

Exact required keys, no extra fields/query parameters. Request IDs are UUIDs. Email is trimmed/lowercased, valid format, maximum 254 characters, retaining dots and plus suffixes as UC-01. Token is a nonempty opaque string up to 512 characters; do not transform it. Passwords obey the existing length/exact-value policy. The token example illustrates placement, not a usable or mandated token format.

Successful Response:

```json
{
  "success": true,
  "message": "If this email is eligible, a password reset link will be sent. Check your inbox.",
  "data": {
    "requestAccepted": true
  }
}
```

Request: HTTP 202 for initial acceptance or identical replay. It intentionally contains no account, request-processing, delivery, or eligibility detail.

```json
{
  "success": true,
  "message": "Password reset. Please sign in again.",
  "data": {
    "passwordReset": true
  }
}
```

Completion: HTTP 200 for first completion or its accepted exact replay. The literal true acknowledges the completed reset operation, not a new login or a guarantee that later independent credential changes cannot occur. Both response shapes are exact and contain no session credential, token, or personal account data.

Error Response:

```json
{
  "success": false,
  "statusCode": 410,
  "code": "RECOVERY_LINK_UNAVAILABLE",
  "message": "This reset link is unavailable. Request a new link.",
  "timestamp": "2026-09-20T10:00:00.000Z",
  "path": "/api/v1/auth/password-recovery/complete"
}
```

Use the existing project envelope: success=false, statusCode matching HTTP status, code, message, server ISO UTC timestamp, and actual pathname without query. Omit data. Only VALIDATION_ERROR may add errors mapping input fields to nonempty arrays of strings. Every 429 includes positive integer retryAfterSeconds matching the Retry-After header. All success keys shown are required; dates/IDs are illustrative.

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

| HTTP | Code | Exact message |
| --- | --- | --- |
| 409 | REQUEST_CONFLICT | This request identifier was already used for different content. |
| 400 | NEW_PASSWORD_UNCHANGED | Choose a password different from your current password. |
| 410 | RECOVERY_LINK_UNAVAILABLE | This reset link is unavailable. Request a new link. |
| 429 | RATE_LIMITED | Too many requests. Please try again later. |
| 503 | RECOVERY_UNAVAILABLE | Password recovery is temporarily unavailable. Please try again later. |

No 401 is required: these are recovery endpoints. They do not require onboarding or an existing session.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement generic durable request acceptance, local recovery-email processing, grant eligibility, and reset completion in NestJS/TypeScript. Separate request acceptance from delivery so request responses do not disclose eligibility through account-specific mail failures. Bind grants and pending jobs to the accepted account credential state. Password replacement, grant consumption, other-grant invalidation, and ending pre-existing account sessions must be one consistent success.

An hourly cleanup removes expired/failed grant and outbox personal data within 24 hours after expiry/failure; discard raw reset-password input after processing. Retain only the minimum repeat association/receipt for the declared 24-hour windows, then delete it. Limits retain their rolling-window behavior independently of cleanup. No additional cryptographic/storage recipe is prescribed.

### Frontend UI Context

Build the two supplementary forms in React/TypeScript/Tailwind, enabling UC-02's recovery link. Generic acceptance must say to check the inbox without claiming an email was sent to a verified account. Show the exact unavailable-link recovery and sign-in destinations; no registration/OTP screen is mislabelled as a verified reset design.

### Frontend Logic and API Context

Read the email-link fragment into temporary memory, remove it from the address bar, and post it only for the declared reset operation. Keep request IDs stable while an outcome is unknown. On confirmed reset clear sensitive values and this account's private cached state without declaring a new authenticated session. Recovery never pauses quiz deadlines or discards already saved learning data.

### Validation and Error-Handling Context

Keep email/password rules identical to UC-01/02, apply generic grant failure and observable limits, and distinguish request acceptance from local SMTP acceptance. Do not reveal account existence, resend automatically, reapply an already completed password mutation, or infer reset success from logout alone.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
