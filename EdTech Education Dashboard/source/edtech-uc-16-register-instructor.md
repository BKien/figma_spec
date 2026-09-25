# UC-16: Register an Instructor Account

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Register an Instructor Account

Description:

- Allows an invited Instructor to register, verify their email, and subsequently access course management through the shared sign-in flow.
- Extends the Instructor tab visible in the Student registration design. Invitation eligibility, Instructor routes, account lifecycle, and API contracts are project requirements; they are not supplied by a Technical Report or inferred from Figma.
- This UC explicitly extends the Student-only eligibility of UC-02, UC-13, and UC-14 to support the account defined here. It does not convert an existing Student into an Instructor.

Primary Actor:

Visitor with a project-issued Instructor invitation for their email address.

Preconditions:

- UC-01 registration and local Mailpit delivery are implemented; UC-02 provides shared browser sessions.
- Experiment setup provisions an invitation with a unique opaque code, normalized email, issuedAt, expiresAt, and state AVAILABLE. Validity is seven days from issuance. The researcher supplies the code to the participant outside the application; no invitation management or email-sending UI is required here.
- Invitations are for previously unregistered emails. One normalized email has at most one application account and one live invitation. Student registration does not accept an invitation or a role parameter.

Postconditions:

- Success: One ACTIVE, email-verified INSTRUCTOR account exists, with onboardingStatus=NOT_REQUIRED. Its invitation is consumed by that account. The visitor returns to `/sign-in`; verification alone does not establish a session.
- Subsequent successful sign-in reaches `/instructor/courses`. No Student onboarding, enrollment, learning preferences, or learning progress is created automatically.
- Failure: No partially created account or consumed invitation remains after a failed account-creation operation. An email-accepted pending registration is not an active Instructor.

Main Flow:

1. The visitor selects Instructor on the registration screen and enters full name, email, and invitation code.
2. They continue to password and confirmation, accept the terms, and submit the complete registration request.
3. The server validates fields and invitation eligibility, reserves the normalized email under an INSTRUCTOR pending registration, and requests the UC-01 verification email.
4. After confirmed local adapter acceptance, display the shared verification screen with its expiry and resend controls.
5. The visitor submits the six-digit code. The server checks registration/code validity and rechecks invitation eligibility.
6. Create the account, complete the registration, and consume its invitation as one coherent outcome. Return the registration receipt and remove pending credential material according to UC-01.
7. Navigate to `/sign-in` with `Instructor account created. Sign in to continue.`
8. UC-02 authenticates the Instructor and confirms the session. Role-aware routing opens `/instructor/courses`.

Alternative Flow:

A.1 — Correcting input or changing account type

- `/sign-up/instructor` holds name, email, and invitation; `/sign-up/instructor/password` holds passwords and terms. Back preserves non-password fields and clears passwords. Switching back to Student clears the invitation and password draft.
- A pending registration cannot change its role or invitation. Restart with a fresh registration request after that pending registration expires or becomes invalidated; do not overwrite it from another registration flow.

A.2 — Resend and repeated requests

- Reuse UC-01 verification/resend behavior and shared endpoints. Code validity is ten minutes, capped by registration expiry; absolute registration validity is 30 minutes from initial accepted issuance, additionally capped by invitation expiry.
- Resend is available after 60 seconds; at most three successful resends. Resend does not reset the cumulative five-wrong-code limit. Initial delivery failure invalidates the pending registration; resend failure preserves the previously accepted code and expiry.
- Recognized exact initial/resend replays follow UC-01, do not send another email, and do not consume a new-request allowance. An initial request ID is bound to the endpoint, normalized identity, invitation, and complete accepted payload; reuse for different content returns REQUEST_CONFLICT.
- Verification completion replay returns HTTP 200 and the original receipt for 24 hours, even though the invitation is now consumed. It creates no second account and does not re-evaluate the receipt as a new invitation use.

A.3 — Shared authentication integration

- Extend UC-02 login/session successful user.role to STUDENT or INSTRUCTOR. Student onboarding values remain NOT_STARTED, IN_PROGRESS, or COMPLETED; Instructor onboardingStatus is always NOT_REQUIRED.
- Evaluate role before onboarding in frontend routing. STUDENT retains UC-02 destinations; INSTRUCTOR goes to `/instructor/courses`. Never send an Instructor to Student onboarding or interpret NOT_REQUIRED as Student completion.
- Retain UC-02 login input, success envelope, generic credential error, five evaluations/email and 30/IP per rolling 15 minutes, and session durations: eight hours without Remember Me or 30 days with it. Limits are shared across roles, not separate extra allowances.
- UC-13 password change and UC-14 recovery accept ACTIVE, verified accounts of either role, with their existing contracts, limits, and session effects. Provide the UC-13 form at `/instructor/settings/password`; public recovery routes remain unchanged. UC-15 current-session logout applies unchanged to both roles.

Exception Flow:

E.1 — Invitation unavailable

- Unknown, consumed, expired, or email-mismatched invitations return INVITATION_NOT_AVAILABLE without distinguishing the reason. A valid-looking code does not reserve an invitation before a pending registration is accepted.
- Invitation expiry while verification is pending invalidates that registration, releases its email reservation, and returns REGISTRATION_NOT_AVAILABLE. No resend extends invitation validity. A researcher may provision a new invitation after the old one expires; this is experiment setup, not a new application feature.
- Existing accounts cannot register a second role. Return UC-01 EMAIL_UNAVAILABLE_FOR_REGISTRATION when identity availability fails after invitation eligibility succeeds.

E.2 — Verification, email, and service failure

- Apply UC-01 code mismatch, expiry, resend, adapter timeout, unknown-outcome, and retention rules. A wrong code consumes one attempt; the fifth invalidates the registration. Invalidating a registration does not consume its still-valid invitation.
- Account creation and invitation consumption cannot partially succeed. Concurrent verification produces one account and a repeat receipt, not two accounts or a lost invitation.

E.3 — Wrong application role

- Missing/expired sessions use 401 UNAUTHENTICATED on protected routes. An authenticated Student calling Instructor APIs, or Instructor calling Student APIs, receives 403 ROLE_NOT_ALLOWED.
- Apply these role boundaries to existing Student endpoints as well as new Instructor endpoints. This explicitly refines earlier Student frontend handling of HTTP 403: route ONBOARDING_REQUIRED to Student onboarding only for a Student; handle ROLE_NOT_ALLOWED by returning to the confirmed role's home, never by looping through onboarding. Do not expose Student-only profile/preferences/onboarding screens in Instructor navigation.

UI Integration:

- File: [EdTech Platform for online learning](https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-2480).
- Source anchors: `222:2480` — Student sign-up with Student/Instructor selection; `225:18` — password and terms; `222:2408` — verification; `222:2528` — shared Login.
- The Instructor invitation field and all Instructor screens are project-designed supplements. These references establish reusable visual structure, not a dedicated Instructor form or verified Instructor prototype behavior.
- Use the same typography, form hierarchy, primary action treatment, and decorative-panel pattern. Instructor remains visibly selected across its two input steps. Social buttons remain unavailable under the existing scope.
- Reuse UC-01 `/sign-up/verify` with the pending registration ID and account type in flow state. Do not introduce another verification endpoint or put invitation/code/password values in the URL. Missing flow state offers a role-selection restart at `/sign-up`; choosing Instructor opens `/sign-up/instructor`.
- `/instructor/courses` must exist in this implementation: header with account name, Courses, Change password, and Logout; body initially supports an empty state and becomes the UC-17 course list when that UC is present. This integration shell is a project supplement and is not counted as another use case.

API Endpoint:

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/api/v1/auth/instructor-registrations` | Begin invited registration |
| POST | `/api/v1/auth/registrations/:registrationId/verify` | Shared typed-registration verification |
| POST | `/api/v1/auth/registrations/:registrationId/resend` | Shared code resend |

UC-02 login/session, UC-13 change password, UC-14 recovery, and UC-15 logout retain their existing paths and request schemas with the role extension stated above.

Request Body:

Initial registration accepts exactly:

```json
{
  "registrationRequestId": "4213b88e-75cc-4c93-b887-20d18365a891",
  "fullName": "Taylor Morgan",
  "email": "taylor@example.com",
  "invitationCode": "INSTRUCTOR-DEMO-001",
  "password": "TeachingPass42!",
  "confirmPassword": "TeachingPass42!",
  "termsAccepted": true
}
```

- registrationRequestId is a UUID. fullName is trimmed, 2–100 Unicode code points. Email is trimmed/lowercased, valid, at most 254 characters; preserve dots and plus suffixes.
- Password is 8–128 Unicode code points, without trimming/normalization; confirmation matches exactly. termsAccepted is literal true.
- invitationCode is a case-sensitive string, 1–128 characters, without whitespace; the shown value is an illustrative fixture, not a universal enrollment credential. The client cannot supply role, status, onboarding state, or verified flags.
- Verify accepts exactly `{ "code": "042781" }`; resend accepts exactly `{ "resendRequestId": "bd4fd93a-a9e9-43ef-8689-394fd61ac1b4" }`. IDs are UUIDs; code is exactly six decimal digits. No endpoint accepts query parameters.

Successful Response:

HTTP 202 for accepted initial issuance/resend; all fields required, with actual UTC timestamps:

```json
{
  "success": true,
  "message": "Verification email accepted. Check your inbox.",
  "data": {
    "registrationId": "41be2085-0d5c-4ced-9b50-425577f8e1ca",
    "codeExpiresAt": "2026-09-20T10:10:00.000Z",
    "registrationExpiresAt": "2026-09-20T10:30:00.000Z",
    "resendAvailableAt": "2026-09-20T10:01:00.000Z"
  }
}
```

Verification HTTP 201 first completion, HTTP 200 recognized completion replay:

```json
{
  "success": true,
  "message": "Instructor account created. Sign in to continue.",
  "data": {
    "user": {
      "id": "7978c82b-76a1-4c46-a041-0c2db832e106",
      "fullName": "Taylor Morgan",
      "email": "taylor@example.com",
      "role": "INSTRUCTOR",
      "status": "ACTIVE",
      "emailVerified": true,
      "onboardingStatus": "NOT_REQUIRED"
    }
  }
}
```

All shown keys are required. No session or token is returned by registration. Shared login/session retain UC-02 data.user and data.session shapes, with the Instructor role/onboarding pair above and unchanged expiresAt/rememberMe fields.

Error Response:

```json
{
  "success": false,
  "statusCode": 400,
  "code": "INVITATION_NOT_AVAILABLE",
  "message": "This invitation cannot be used for this email.",
  "timestamp": "2026-09-20T10:00:00.000Z",
  "path": "/api/v1/auth/instructor-registrations"
}
```

The envelope always contains success=false, statusCode, code, message, timestamp, and actual pathname without query; omit data. VALIDATION_ERROR may add errors mapping field paths to nonempty string arrays. RATE_LIMITED adds positive integer retryAfterSeconds matching Retry-After.

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | INVITATION_NOT_AVAILABLE | This invitation cannot be used for this email. |
| 401 | UNAUTHENTICATED | Please sign in to continue. |
| 403 | ROLE_NOT_ALLOWED | This action is not available for your account role. |

All UC-01 registration errors and exact messages remain applicable: VALIDATION_ERROR, INVALID_VERIFICATION_CODE, EMAIL_UNAVAILABLE_FOR_REGISTRATION, REQUEST_CONFLICT, REGISTRATION_NOT_AVAILABLE, VERIFICATION_CODE_EXPIRED, VERIFICATION_LIMIT_REACHED, RESEND_LIMIT_REACHED, RATE_LIMITED, EMAIL_UNAVAILABLE, REGISTRATION_UNAVAILABLE, and INTERNAL_ERROR. Shared auth operations retain their own existing error contracts.

## Project-Specific Implementation Context

### Backend Implementation Context

Use the existing NestJS/TypeScript account and registration services. Add an explicit pending accountRole and invitation association, and the INSTRUCTOR/NOT_REQUIRED account pair. Student creation remains server-assigned STUDENT/NOT_STARTED. Invitation consumption and account creation are one durable business transition. Expired invitations cannot authorize a late completion; completed replay receipts remain readable for their defined lifetime.

Initial registration budgets of three new attempts/email and ten/IP per hour are shared across Student and Instructor endpoints. Rejected structurally valid invitation attempts consume the same initial-attempt allowance. Shared verify/resend budgets and five mismatches follow UC-01. Keep a consumed invitation's account association; remove its redeemable code at consumption or expiry, and retain that non-secret association for experiment provenance. Pending registration cleanup follows UC-01, including removal within 24 hours after terminal expiry/invalidation.

Apply the declared role extensions to shared authentication and recovery as part of this UC. NOT_REQUIRED is an explicit schema addition, not an omitted/null field. Instructor access never depends on Student onboarding completion. An invitation is not needed again at ordinary login.

### Frontend UI Context

Use React, TypeScript, and Tailwind with the source registration layout. Add the labelled invitation input and short explanation, preserving field order and clear Instructor selection. Put supplementary validation/loading/retry states beside the form. On narrow screens prioritize the form and omit the decorative panel, following the project convention; no Instructor mobile design is claimed.

### Frontend Logic and API Context

Keep pending account type, registration ID, and timestamps in the registration flow. Reuse code entry/resend logic, but route restarts to the correct role-specific form. Never derive application role from a tab after login: use the confirmed shared session. Instructor course-list, password-change, and logout navigation must resolve to working routes. Preserve the UC-15 unsaved-work handling for future course drafts.

### Validation and Error-Handling Context

Use the shared identity/password rules without imposing new password composition requirements. Distinguish invitation input rejection from later registration expiry. Do not claim a pending account is approved, registered, or signed in. Preserve correctable name/email fields, clear credential fields under UC-01 rules, and resolve uncertain submissions through their existing repeat behavior before starting another registration.
