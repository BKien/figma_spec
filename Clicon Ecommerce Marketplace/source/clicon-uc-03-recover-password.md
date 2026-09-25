# UC-03: Recover Password

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Recover Password

Description:

- Allows a customer who cannot remember their password to request recovery instructions by email and set a new password.
- Includes Forget Password and Reset Password as one complete user goal. Changing a password from an authenticated account-settings screen belongs to a separate use case.
- Recovery is email-only, consistent with the current UC-01 account model. The email contains a recovery link carrying a recovery code; opening it supplies the code to the Reset Password form without a separate code-entry field.
- Email-only recovery, link navigation, expiry, request limits, and session consequences are project decisions. Figma establishes the two forms and their visible controls, not these backend rules.

Primary Actor:

Customer who has forgotten their password.

Preconditions:

- An active, verified account exists for successful recovery, and the customer can access its email inbox.
- The shared account and API contracts in `PROJECT_CONTEXT.md` apply.
- For the local experiment, recovery emails use the same Mailpit inbox environment as UC-01; no external email account is required for synthetic accounts.
- `/forgot-password`, `/reset-password`, and the UC-02 `/sign-in` route are registered, including direct navigation/reload support.

Postconditions:

- Success: The existing account's password is replaced, the recovery link is no longer usable, other outstanding recovery links for that account are no longer usable, and existing signed-in sessions for that account end. The customer returns to Sign In; no automatic login occurs.
- Failure: No password is changed by the failed operation. Missing, incorrect, expired, or already-used recovery information does not complete recovery. An uncertain network result is not treated as proof that the operation failed.
- Requesting recovery alone does not change a password, end sessions, activate a pending registration, or create an account.

Main Flow:

1. The customer selects Forget Password from UC-02 or opens `/forgot-password` directly.
2. The system displays the Forget Password form with Email Address and SEND CODE.
3. The customer enters their email and selects SEND CODE.
4. The frontend validates the field and submits `POST /api/v1/auth/forgot-password`.
5. The backend validates the request, applies the recovery-request limit, and accepts processing. For an eligible active, verified account, it arranges a recovery email; other identities follow A.1.
6. The API returns HTTP 202 using the same acceptance message for all syntactically valid, admitted email requests. The frontend stays on Forget Password and displays that message; it does not navigate to Reset Password based on the email alone.
7. The customer opens the email and follows its recovery link to `/reset-password?code=<recoveryCode>`. The code belongs to that recovery request and is valid for 15 minutes from issuance.
8. The system displays Reset Password with Password and Confirm Password. The code is supplied by the link, not a visible third input.
9. The customer enters matching passwords and selects RESET PASSWORD. The frontend submits `POST /api/v1/auth/reset-password` with the link code and the two password fields.
10. The backend checks the request and recovery eligibility, then completes the password replacement with the postconditions above.
11. The API returns HTTP 200. The frontend clears both password fields and recovery state, navigates to `/sign-in`, and displays `Password reset successfully. Please sign in.`

Alternative Flow:

A.1 — Email is unknown or ineligible

- Return the same HTTP 202 acceptance body for unknown email, pending-only registration, inactive account, or unverified account.
- No recoverable account is created, no existing account is activated, and no recovery link is sent for an ineligible identity.

A.2 — Request another recovery email

- The customer returns to `/forgot-password` and submits again, subject to the same request limits.
- A newly issued link for the same account replaces its earlier recovery links. Opening or refreshing a link does not renew its expiry.
- There is no separate Resend Code control in either captured recovery frame; do not reuse UC-01's verification resend endpoint.

A.3 — Return to Sign In or create an account

- The observed Sign In and Sign Up links navigate to `/sign-in` and `/sign-up` respectively.

A.4 — Show or hide password

- Each eye control changes only its associated password field's visibility. It preserves the value and does not submit the form.

Exception Flow:

E.1 — Invalid input

- Invalid email, missing fields, a password outside the shared policy, or mismatched confirmation produces field feedback.
- Server validation returns HTTP 400 `VALIDATION_ERROR`. The failed submission does not change the password.

E.2 — Missing or unusable recovery link

- If no nonempty `code` is present in the URL, show `Open the password recovery link from your email.` and provide `Request a new link` to `/forgot-password`; do not submit a reset with an empty code.
- An incorrect, unknown, superseded, already-used code, or a code whose account is no longer eligible, returns HTTP 400 `INVALID_RECOVERY_LINK`.
- Display the error and the same recovery navigation. The frontend must not invent an email-based fallback that bypasses the link.

E.3 — Expired recovery link

- A known otherwise eligible recovery request at or past expiry returns HTTP 410 `RECOVERY_LINK_EXPIRED`.
- Display the message and a link to `/forgot-password`. No password change occurs.

E.4 — Recovery request limit reached

- Return HTTP 429 `RATE_LIMIT_EXCEEDED`, positive integer `retryAfterSeconds`, and a matching `Retry-After` header.
- Stay on the current form and disable its submit action for the stated delay. Permit a manual retry afterward; do not automatically resend email or resubmit a password change.

E.5 — Email processing or service unavailable

- HTTP 202 means a request was accepted, not that delivery to the inbox has been proved. Email delivery may fail after acceptance; the customer can request another link under A.2.
- If the request-acceptance service is unavailable for recovery requests generally, return HTTP 503 `RECOVERY_SERVICE_UNAVAILABLE`. Do not make the public status depend on whether one recipient has an account or one recipient's delivery succeeded.
- Unexpected failures use HTTP 500 `INTERNAL_ERROR`. Do not show successful completion for a failed password update.

E.6 — Response lost

- After an uncertain request-email outcome, remain on Forget Password and tell the customer to check their inbox before requesting again. Do not automatically repeat the request.
- After an uncertain reset outcome, display `We could not confirm the result. Try signing in with your new password, or request a new recovery link.` with links to Sign In and Forget Password. Clear the password inputs; do not automatically repeat the reset.
- A later rejection of a used code is not, by itself, proof that the current browser completed the earlier password change.

UI Integration:

- Forget Password: `17_Forget Password`, node `429:9318`, frame 1920 × 1436.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=429-9318
- Reset Password: `18_Reset Password`, node `429:9808`, frame 1920 × 1364.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=429-9808
- Both exact nodes were read live on 2026-09-18 through metadata, design context, and full-size screenshots. Captured desktop evidence is packaged as `clicon-uc-03-design-v1.zip`; checksums and scope are recorded in its manifest and the accompanying configuration.
- The capture does not establish mobile layouts or working prototype transitions. Original SVG downloads timed out and font binaries are not included; this is a fixed desktop evidence snapshot, not a complete source-generation release. Figma's historical version ID was not returned; local snapshot identity is defined by the stored checksums.

| Frame / observed control | Binding or behavior |
| --- | --- |
| Forget Password heading | Preserve the heading |
| Email Address | `email` |
| SEND CODE | Submit the email recovery request |
| Already have account? Sign In | `/sign-in` |
| Don't have account? Sign Up | `/sign-up` |
| Customer Service text | Preserve the visible text; no clickable behavior is inferred from colored text alone |
| Reset Password heading | Preserve the heading |
| Password; placeholder `8+ characters` | `password` |
| Confirm Password | `confirmPassword` |
| Two eye icons | Independent visibility controls |
| RESET PASSWORD | Submit the new password with the recovery code from the link |

- Retain the Clicon header/footer and breadcrumbs. Card content width is 360 px with 32 px padding; fields are 44 px high and primary actions 48 px high in the captured desktop reference. Public Sans and the resolved colors/styles are included in the snapshot.
- The original Forget Password description mentions mobile phone numbers, but this UC has email-only identity. Replace it with the project copy `Enter the email address associated with your Clicon account.`
- Replace the Reset Password placeholder paragraph with `Enter and confirm your new password.` Preserve SEND CODE as the design label; the email explains that the recovery code is already included in its link.
- No manual OTP screen, phone recovery, or separate success page is added. Confirmation, loading, validation, expired-link, and service-error states are project supplements recorded in the dataset, not discovered Figma variants.

API Endpoint:

| Operation | Endpoint |
| --- | --- |
| Request recovery email | `POST /api/v1/auth/forgot-password` |
| Complete password recovery | `POST /api/v1/auth/reset-password` |

Request Body:

Both endpoints use `Content-Type: application/json`. Fields shown are required; unknown request properties are rejected.

`POST /api/v1/auth/forgot-password`

```json
{
  "email": "student@example.com"
}
```

- Email uses the shared UC-01 normalization: trim surrounding whitespace, lowercase for identity comparison, valid email format, maximum 254 characters.

`POST /api/v1/auth/reset-password`

```json
{
  "recoveryCode": "example-code-from-email-link",
  "password": "NewExamplePass123!",
  "confirmPassword": "NewExamplePass123!"
}
```

- `recoveryCode`: nonempty string taken from the email link's `code` parameter; the example is illustrative and grants no access. Its generation and storage implementation are not specified in this UC. Do not assume it is UC-01's six-digit verification code.
- `password`: at least 8 Unicode code points and at most 72 UTF-8 bytes, matching the shared account policy; preserve its value exactly.
- `confirmPassword`: must exactly match `password`. No current password is required in this forgotten-password flow.
- The account to update is determined by the recovery request. The reset body does not accept an email or user ID to choose another account.

Successful Response:

Request accepted — HTTP 202:

```json
{
  "success": true,
  "message": "If an eligible account exists, you will receive password recovery instructions by email.",
  "data": {
    "status": "REQUEST_ACCEPTED"
  }
}
```

- This body is identical for eligible and ineligible email identities. It contains no recovery code, recovery link, or account-existence flag.

Password updated — HTTP 200:

```json
{
  "success": true,
  "message": "Password reset successfully. Please sign in.",
  "data": {
    "status": "PASSWORD_RESET"
  }
}
```

- No authentication token or session is returned. Sign-in remains UC-02.

Error Response:

Use the shared envelope with `success`, `statusCode`, `code`, `message`, `timestamp`, and `path`. Do not include `data` in errors. Timestamps below are illustrative; generate the actual UTC timestamp at response time. `path` is the actual endpoint pathname without its query string.

Validation — HTTP 400:

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-18T10:00:00.000Z",
  "path": "/api/v1/auth/reset-password",
  "errors": {
    "confirmPassword": ["Passwords do not match."]
  }
}
```

Unusable link — HTTP 400:

```json
{
  "success": false,
  "statusCode": 400,
  "code": "INVALID_RECOVERY_LINK",
  "message": "This recovery link is invalid or no longer available. Please request a new link.",
  "timestamp": "2026-09-18T10:00:00.000Z",
  "path": "/api/v1/auth/reset-password"
}
```

Throttling — HTTP 429, example header `Retry-After: 60`:

```json
{
  "success": false,
  "statusCode": 429,
  "code": "RATE_LIMIT_EXCEEDED",
  "message": "Too many recovery attempts. Please try again later.",
  "timestamp": "2026-09-18T10:00:00.000Z",
  "path": "/api/v1/auth/forgot-password",
  "retryAfterSeconds": 60
}
```

| HTTP | Endpoint | Code | Exact message |
| --- | --- | --- | --- |
| 400 | Both | `VALIDATION_ERROR` | `Please correct the highlighted fields.` |
| 400 | Reset | `INVALID_RECOVERY_LINK` | `This recovery link is invalid or no longer available. Please request a new link.` |
| 410 | Reset | `RECOVERY_LINK_EXPIRED` | `This recovery link has expired. Please request a new link.` |
| 415 | Both | `UNSUPPORTED_MEDIA_TYPE` | `Use application/json for this request.` |
| 429 | Both | `RATE_LIMIT_EXCEEDED` | `Too many recovery attempts. Please try again later.` |
| 503 | Both | `RECOVERY_SERVICE_UNAVAILABLE` | `Password recovery is temporarily unavailable. Please try again later.` |
| 500 | Both | `INTERNAL_ERROR` | `Unable to complete your request. Please try again later.` |

## Project-Specific Implementation Context

### Backend Implementation Context

Implement the two endpoints in NestJS using the shared account model, response envelope, and recovery parameters in `PROJECT_CONTEXT.md`.

- Reuse UC-01's account and password compatibility rules. Recovery must not create another user, change an account's identity, or verify a pending registration.
- Return the documented acceptance result without revealing email eligibility. Only active, verified accounts receive recovery instructions.
- The recovery email contains a link to the configured frontend `/reset-password` route with its recovery code. Use the local Mailpit environment already selected for the experiment. The email states that the link expires 15 minutes after issuance and directs the customer to request again if it is no longer usable.
- A newly issued recovery link replaces prior links for the same account; successful recovery ends outstanding recovery opportunities and existing account sessions. Reading a link or displaying its form does not consume it or extend its validity.
- Apply the observable request limits from the project context. Do not specify a counter algorithm, cryptographic recipe, password-storage implementation, cookie flags, or internal retention mechanism in this UC.
- Return success only when the password update and its required account/session outcomes are complete. Service failure does not result in a partial reported success.
- Ordinary field-validation failure leaves an otherwise valid recovery link available until its original expiry. A valid recovery request can complete password replacement only once.

### Frontend UI Context

Implement `ForgotPasswordPage` at `/forgot-password` and `ResetPasswordPage` at `/reset-password` in React, TypeScript, and Tailwind CSS. This replaces the temporary recovery navigation shell introduced for UC-02.

- Use the frozen desktop screenshots, metadata, and resolved styles referenced in UI Integration. Original SVG assets and font binaries are not bundled; their absence is recorded in the dataset and must be resolved for any evaluation requiring those exact resources.
- Apply the two documented copy changes consistently; they are project supplements, not edits to the source Figma file.
- Keep one email field on Forget Password and exactly two password fields on Reset Password. Use independent visibility controls and the existing orange buttons.
- Preserve Sign In and Sign Up destinations. Treat recovery breadcrumb steps as navigation to their named routes; retain shared shell navigation already owned by the project.
- Render acceptance feedback inside the existing Forget Password card; render invalid/expired-link feedback and `Request a new link` inside the Reset Password card. Do not add a new screen or pretend those states were exported from Figma.
- Associate labels and validation messages with their inputs; allow keyboard submission without triggering password-visibility controls as submit actions.

### Frontend Logic and API Context

- Forget Password state: `email`, `isSubmitting`, `fieldErrors`, `formError`, acceptance feedback, and retry deadline.
- Reset Password state: link `recoveryCode`, `password`, `confirmPassword`, independent visibility state, loading, field errors, form error, and retry deadline.
- Read the `code` query value on direct entry or reload. If absent, empty, or repeated ambiguously, show E.2 and do not submit a reset. Possession of a URL value does not let the frontend declare the link valid; completion is decided by the server.
- Submit the request-email body and parse the project envelope. A 202 keeps the customer on Forget Password with the generic acceptance message. Do not fabricate a code or auto-open Reset Password.
- Opening the real email link supplies the reset credential independently of whether the original form is still open. No UC-01 pending-registration state is needed.
- Submit the exact reset body. On confirmed success, clear password/recovery state, navigate to `/sign-in` without retaining the reset query in the destination, and show the documented success message.
- End the local authenticated state after confirmed recovery if the browser was already signed in; other browsers discover their ended sessions through the existing session contract.
- Handle a lost response according to E.6. Do not automatically replay either POST.

### Validation and Error-Handling Context

- Match shared email normalization and password input rules. Do not trim or transform the password. Map `errors` by the exact request field names.
- A confirmation mismatch appears beneath Confirm Password. Link errors appear at form level because the code is not a visible input.
- Disable duplicate submission while a request is active and keep the affected action disabled for a returned throttle delay. Restore the action after loading only if no delay remains.
- Preserve the email after request failure. Clear both password fields after an unsuccessful reset submission; an ordinary correctable validation error does not itself mean the link is expired.
- Display `message` for documented server failures. For no response use `Unable to connect. Please check your connection and try again.`, supplemented by E.6 when the outcome is uncertain.
- Unexpected/malformed responses display `Unable to complete your request. Please try again later.` and must not trigger a completion redirect.
- Do not interpret an accepted email request as a completed password reset or successful delivery. Do not interpret a reset as successful sign-in.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
