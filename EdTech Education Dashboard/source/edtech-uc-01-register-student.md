# UC-01: Register a Student Account and Verify Email

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Register a Student Account and Verify Email

Description:

- Allows a visitor to enter their name and email, choose a password, accept the project terms, and verify a six-digit email code to create an active Student account.
- This is one business goal across three screens; password entry and email verification are not separate use cases.
- API contracts, lifecycle, validation, and email behavior below are proposed EdTech project requirements. No Technical Report or existing backend contract was supplied. Figma establishes the visible UI, not these backend rules.
- Instructor support is an approved project extension to be specified separately. This UC creates only STUDENT accounts; choosing Instructor must not silently register a Student or grant Instructor capabilities.

Primary Actor:

Visitor registering as a Student.

Preconditions:

- The visitor is not signed in. The application provides `/sign-up`, `/sign-up/password`, and `/sign-up/verify` routes.
- The experiment has a working local Mailpit instance and a configured sender. The researcher can access its inbox to retrieve messages; real external email delivery is not required.
- A project-authored Terms of Service and Privacy Policy notice is accessible from the consent label. It is experimental content, not text supplied by the design.

Postconditions:

- Success: Exactly one account exists for the normalized email with role STUDENT, status ACTIVE, emailVerified=true, and onboardingStatus=NOT_STARTED. Registration does not create an authenticated session or enroll the account in courses.
- Failure: A rejected or expired attempt creates no usable account. Pending registrations cannot authenticate. An unknown response is reconciled by the repeat rules below, not treated as definite failure.

Main Flow:

1. The visitor opens `/sign-up`; Student is selected. They enter Full name and Email, then select Next.
2. The frontend validates both fields locally and opens the password step while retaining the draft in memory. No account is created at this step.
3. The visitor enters Password and Confirm Password, explicitly accepts the terms, and selects Create Account.
4. The frontend creates a registrationRequestId and sends the complete registration request once.
5. The backend validates the request, reserves the normalized email for this pending registration, and sends a six-digit verification code through the local email adapter.
6. After the adapter accepts the message, the backend returns HTTP 202 and the verification metadata. The frontend clears password values and opens `/sign-up/verify` with the registrationId in in-memory flow state.
7. The visitor enters the emailed code and selects Sign Up. The backend checks the registration state, expiry, and remaining attempts.
8. A correct current code creates the active verified Student account and completes the pending registration. The frontend replaces the form with `Your account is ready. You can now sign in.`
9. The completed screen links to `/sign-in` when UC-02 is installed. Until then, render the success state with the sign-in action disabled and a clear explanation; never navigate to a missing route. Onboarding begins after sign-in in its own UC.

Alternative Flow:

A.1 — Correct details before submission

- A supplementary Back control returns from password to name/email without creating a registration. Preserve name/email; clear both password fields. Reloading a pre-submission route discards the draft and returns to `/sign-up`.
- Opening password or verification routes without the required flow state displays a restart link. Do not place email, password, or verification code in the URL.

A.2 — Resend code

- Resend email is available after 60 seconds from the last accepted message; at most three resends are accepted per registration. The initial message is not a resend.
- A successful resend replaces the previous code and gives the new code a ten-minute lifetime, capped by the registration's absolute 30-minute lifetime. It does not reset verificationAttemptCount.
- Expired codes can be replaced while the registration is still pending and within its lifetime. Invalidated, completed, or expired registrations cannot resend.
- A failed resend keeps the previous code and its expiry unchanged. It does not consume a successful-resend allowance; request-rate limits still apply.

A.3 — Repeated requests and lost responses

- registrationRequestId identifies one initial submission. Repeating the same ID and exact normalized payload returns the original registration metadata without sending another message. Different content under that ID returns REQUEST_CONFLICT.
- The frontend freezes the submitted draft while its initial response is unknown and offers a deliberate same-ID retry. It must not allocate a new ID automatically. On a definite EMAIL_UNAVAILABLE rejection, a deliberate retry uses a new ID because the failed attempt is terminal.
- Every resend carries a resendRequestId. Identical repeats return the same issuance metadata and do not rotate/send again; failed attempts require a new resendRequestId for a deliberate new attempt.
- A completed registration accepts a repeat of the successful verification code for 24 hours and returns the same account result. It creates no duplicate and no session. Other codes return REGISTRATION_NOT_AVAILABLE without revealing account data.
- A full reload may lose flow state. Explain that the previous operation might have succeeded; provide Sign in when available or Restart registration. Do not promise that a timeout means no account was created.

A.4 — Student and Instructor selection

- Preserve the visible role selector. In the UC-01-only implementation, Instructor displays `Instructor registration is not available yet.` and cannot submit. A later Instructor UC will define its own registration and onboarding behavior using a shared account identity model.
- Google, Apple, and Facebook controls are visible but disabled with an explanation until their integrations are separately specified. They must not simulate successful authentication.

Exception Flow:

E.1 — Invalid or unavailable registration

- Validation errors preserve correctable fields. Existing account email or an email reserved by another live registration returns EMAIL_UNAVAILABLE_FOR_REGISTRATION. An unrelated request cannot overwrite a pending password or name.
- Malformed, missing, expired, or invalidated registration IDs return the same REGISTRATION_NOT_AVAILABLE response. Expiry or invalidation releases its email reservation.

E.2 — Invalid verification code

- Codes are six decimal digits, accepted as strings so leading zeroes are preserved. A structurally valid wrong code increments verificationAttemptCount; after the fifth mismatch the registration becomes INVALIDATED and the response is VERIFICATION_LIMIT_REACHED.
- Earlier mismatches return INVALID_VERIFICATION_CODE. Expired codes return VERIFICATION_CODE_EXPIRED without consuming a mismatch attempt. Malformed requests and rate-limited requests do not consume verification attempts.
- Resending does not restore attempts. The UI offers restart after invalidation, or resend after code expiry if the registration remains eligible.

E.3 — Observable request limits

- Initial registration: at most three new attempts per normalized email and ten per IP in a rolling hour. Resend requests: at most five new attempts per registration and ten per IP in a rolling hour, in addition to the cooldown and three-success limit.
- Verification requests: at most ten per registration and thirty per IP in a rolling ten minutes. The five-wrong-code limit remains separate. Recognized exact repeats return their saved result without consuming a new-request allowance.
- Return 429 with positive retryAfterSeconds and matching Retry-After. A denied request does not extend the wait. No limiter algorithms are prescribed here.

E.4 — Email or service failure

- Adapter success means the local SMTP service accepted the message; it does not mean the user read it or that an external mailbox received it. The adapter waits up to five seconds for acceptance and performs no automatic retry.
- Initial send rejection/timeout returns EMAIL_UNAVAILABLE, invalidates that attempt, and releases the reservation. Any message accepted despite a lost acknowledgement may arrive with an unusable code; the user must follow the most recent successful request.
- A resend rejection/timeout leaves the old issuance usable and rejects the new issuance. No success notice appears for the failed send.
- Unknown backend outcomes, concurrent submissions, and delayed responses must not create duplicate accounts or report email acceptance before it occurs.

UI Integration:

- `03 Sign Up Student`, node `222:2480`: Full name, Email, Student/Instructor selector, Next, social controls, Login link.
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-2480
- `04 Sign Up Password Student`, node `225:18`: Password, Confirm Password, visibility controls, consent checkbox, Create Account.
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=225-18
- `05 Sign Up Verification Student`, node `222:2408`: Check your inbox, one six-digit code field, Sign Up, Resend email.
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-2408
- Live design contexts and screenshots inspected on 2026-09-20. Preserve the yellow illustration panel, white form panel, typography, rounded controls, and visible labels. This is live screen inspection, not a frozen dataset release.
- Back/restart controls, completion state, errors, cooldown text, disabled-feature explanations, terms notice, and narrow-screen behavior are project supplements. On narrow screens prioritize the form and hide the decorative panel; no mobile Figma frame is claimed.
- Consent starts unchecked. Code and password inputs have explicit accessible labels; errors are associated with their fields. Submission pending state disables repeated actions.

API Endpoint:

- `POST /api/v1/auth/registrations`
- `POST /api/v1/auth/registrations/:registrationId/verify`
- `POST /api/v1/auth/registrations/:registrationId/resend`

Request Body:

Initial registration:

```json
{
  "registrationRequestId": "d0f3c937-a88d-44ee-955a-fffa589d89ba",
  "fullName": "Alex Nguyen",
  "email": "alex@example.com",
  "password": "ExamplePass123!",
  "confirmPassword": "ExamplePass123!",
  "termsAccepted": true
}
```

- All keys required, no additional keys or query parameters. IDs are UUIDs. fullName is trimmed, 2–100 Unicode code points; internal spaces are retained.
- Email is trimmed and lowercased for storage, identity, and comparisons; maximum 254 characters and a valid email format. Do not remove dots or plus-address suffixes. This normalization is the shared EdTech account rule.
- Password is 8–128 Unicode code points, used exactly as entered; do not trim or normalize it. Confirm Password must match exactly. No additional composition rule is implied. termsAccepted must be literal true.
- The server assigns STUDENT. Client-supplied role, status, verified flags, IDs, or onboarding state are rejected.

Verify:

```json
{
  "code": "042781"
}
```

Resend:

```json
{
  "resendRequestId": "8cfe5de6-7f6b-4cd7-818c-9f636598d642"
}
```

Verify and resend accept exactly the keys shown, without query parameters. registrationId is a UUID; a malformed ID uses the generic registration-unavailable response. Whitespace around a code may be removed by the frontend, but the API accepts exactly six digits.

Successful Response:

Initial registration and resend return HTTP 202, including successful identical replays:

```json
{
  "success": true,
  "message": "Verification email accepted. Check your inbox.",
  "data": {
    "registrationId": "0be64350-1daf-4f4f-838f-ac060526338a",
    "codeExpiresAt": "2026-09-20T10:10:00.000Z",
    "registrationExpiresAt": "2026-09-20T10:30:00.000Z",
    "resendAvailableAt": "2026-09-20T10:01:00.000Z"
  }
}
```

- All fields required; timestamps are server-generated ISO 8601 UTC. Replay returns the metadata of that issuance, not a fresh expiry. After a later successful resend, earlier replay metadata must not replace the newer issuance in frontend state.
- No code, password, account, or session credential is returned. resendAvailableAt expresses cooldown only; it does not override the resend quota or registration expiry.

Verification returns HTTP 201 for first completion and 200 for an accepted repeat:

```json
{
  "success": true,
  "message": "Your account is ready. You can now sign in.",
  "data": {
    "user": {
      "id": "2b527c49-db38-45c3-87bc-dc901ff36782",
      "fullName": "Alex Nguyen",
      "email": "alex@example.com",
      "role": "STUDENT",
      "status": "ACTIVE",
      "emailVerified": true,
      "onboardingStatus": "NOT_STARTED"
    }
  }
}
```

All keys required. id is a UUID; name/email are normalized persisted values. The remaining fields have the literal values shown for a newly created account. This completion receipt reflects registration-time state on replay; it is not a current-profile endpoint. No automatic sign-in occurs.

Error Response:

```json
{
  "success": false,
  "statusCode": 400,
  "code": "INVALID_VERIFICATION_CODE",
  "message": "The verification code is incorrect.",
  "timestamp": "2026-09-20T10:02:00.000Z",
  "path": "/api/v1/auth/registrations/0be64350-1daf-4f4f-838f-ac060526338a/verify"
}
```

The shared EdTech error envelope requires exactly these common fields, with statusCode matching HTTP status and path containing the actual request pathname without query. Omit data. VALIDATION_ERROR may additionally contain errors mapping field names to nonempty arrays of strings. All 429 errors additionally contain positive integer retryAfterSeconds matching Retry-After.

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 400 | INVALID_VERIFICATION_CODE | The verification code is incorrect. |
| 409 | EMAIL_UNAVAILABLE_FOR_REGISTRATION | This email is unavailable for a new registration. Sign in or try again later. |
| 409 | REQUEST_CONFLICT | This request identifier was already used for different content. |
| 410 | REGISTRATION_NOT_AVAILABLE | This registration is no longer available. Start again. |
| 410 | VERIFICATION_CODE_EXPIRED | This code has expired. Request another code. |
| 410 | VERIFICATION_LIMIT_REACHED | Too many incorrect codes. Start registration again. |
| 409 | RESEND_LIMIT_REACHED | No more codes can be requested for this registration. |
| 429 | RATE_LIMITED | Too many requests. Please try again later. |
| 503 | EMAIL_UNAVAILABLE | We could not send the verification email. Please try again. |
| 503 | REGISTRATION_UNAVAILABLE | Registration is temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

The fifth wrong code returns VERIFICATION_LIMIT_REACHED; subsequent requests against that invalidated registration return REGISTRATION_NOT_AVAILABLE. A resend cooldown uses RATE_LIMITED; exhausting three successful resends uses RESEND_LIMIT_REACHED. The frontend must still permit verification with a valid current code when only the resend quota is exhausted.

## Project-Specific Implementation Context

### Backend Implementation Context

Use NestJS and TypeScript for the proposed experiment, with a shared account model and separate pending registrations. Enforce one account per normalized email, server-assigned STUDENT role, and coherent pending-to-completed transitions under concurrent verification. Account creation and registration completion must succeed together. Persist fullName, normalized email, password credential, status, email verification, role, onboarding state, and timestamps. No course enrollment, instructor approval, or onboarding completion occurs here.

Pending states are PENDING, COMPLETED, INVALIDATED, and EXPIRED. A registration expires 30 minutes after initial accepted issuance; reads/mutations enforce expiry even before cleanup runs. Track verificationAttemptCount and successful resend count with the behavior above. Initial send failures are terminal INVALIDATED attempts. Mailpit adapter acceptance/failure follows E.4; do not add real email dependencies.

Cleanup runs hourly. Delete expired/invalidated pending records and their credentials/personal data within 24 hours after termination. After successful account creation remove the pending password credential immediately; retain only the minimum completion/replay association for 24 hours, then delete it. Expired replay identifiers cannot recreate an attempt; clients use fresh IDs to restart. Request-limit accounting must retain its declared rolling-window behavior independently of email reservation cleanup. These are lifecycle outcomes, not prescribed security algorithms.

### Frontend UI Context

Use React, TypeScript, and Tailwind CSS for the proposed experiment. Implement the three linked forms from the inspected frames. Preserve the illustration and visual hierarchy. Show success and recoverable errors within the existing form area. Do not create separate UC documents for the individual registration screens.

### Frontend Logic and API Context

Maintain name/email, password step, submitted request ID, registration metadata, and pending/error state as one flow. Validate locally for feedback and repeat validation on the server. Keep code values as strings. Clear password fields after the accepted initial response or when leaving/restarting registration. A lost initial response may retain the frozen in-memory payload solely for deliberate retry; never persist passwords across reloads.

Use server timestamps to display expiry/cooldown; the backend is authoritative. Serialize resend and verification actions in the current view. Track which issuance is current and ignore obsolete responses. An accepted verification response completes the registration UI without fabricating a session. Future sign-in reads the shared account fields and routes NOT_STARTED students to the separately specified onboarding flow.

### Validation and Error-Handling Context

Apply the exact field, identity, attempt, resend, and expiry rules consistently. Show field errors beside inputs and lifecycle errors at form level. Do not infer email delivery, registration success, or verification from a timer alone. Distinguish definite rejection from unknown outcome and apply the repeat behavior. Keep instructor, social login, and unimplemented sign-in navigation explicit rather than silently simulating them.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
