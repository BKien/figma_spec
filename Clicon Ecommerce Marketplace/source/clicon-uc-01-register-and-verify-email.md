# UC-01: Register Account and Verify Email


## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Register Account and Verify Email

Description:

- Allows a visitor to register a customer account using their name, email address, and password, then verify ownership of the email address using a verification code.
- Registration and email verification form one use case: submitting the registration form alone does not complete account creation.
- Scope: email/password registration. The visible Google and Apple sign-up buttons are outside this use case. Preserve their placement as disabled controls with an accessible explanation that social registration is outside the experiment scope; do not simulate successful OAuth.

Primary Actor:

Visitor (prospective Customer)

Preconditions:

- The visitor is not signed in and can access the Sign Up page.
- The visitor can access the email address they provide.
- The experiment uses a local Mailpit SMTP adapter and synthetic customer data, with external forwarding/relaying disabled. The tester can inspect the local inbox; access to a real external email inbox is not required for this experiment.

Postconditions:

- Success: Exactly one active customer account is created for the normalized email address; its email-verification timestamp is recorded. The verification code is consumed, and the visitor is directed to Sign In. No login session or access token is issued by this use case.
- Failure: No active account is created by the failed operation. Field values other than passwords are retained where appropriate, and the relevant error is displayed. An unexpired pending registration may remain available for another verification attempt.

Main Flow:

1. The visitor opens the Sign Up page.
2. The system displays the registration form, with Name, Email Address, Password, Confirm Password, and a terms-acceptance checkbox, as observed in the supplied screenshot.
3. The visitor enters their information, accepts the terms, and selects Sign Up.
4. The frontend validates the form and submits `POST /api/v1/auth/register`.
5. The backend validates the request, trims the name, normalizes the email, and checks whether an active account already uses that email.
6. After the registration rate-limit checks, the backend creates a registration in `PENDING_DELIVERY`, initializes `verificationAttemptCount = 0`, stores a password hash, generates a six-digit code, and sets `expiresAt = issuedAt + 10 minutes`.
7. The system makes exactly one SMTP delivery attempt to Mailpit. Only final SMTP acceptance followed by a successful state update changes this record to `PENDING`. No verification is allowed in `PENDING_DELIVERY`. The code is not included in the browser-facing response.
8. The API returns HTTP 201 with the pending registration ID, expiry, and resend availability. The frontend clears the password fields, retains the registration ID for verification, and navigates to the Email Verification page.
9. The visitor enters the code received by email in the single Verification Code input and selects VERIFY ME.
10. The frontend submits `POST /api/v1/auth/verify-email` with the registration ID and code.
11. The backend applies verification rate limits, then atomically checks the registration state, expiry, attempt count, and submitted code. A mismatch increments `verificationAttemptCount`; the fifth mismatch invalidates this registration immediately.
12. In one database transaction, the backend creates the active customer account and marks the pending registration as consumed. A unique constraint on the normalized email prevents duplicate accounts.
13. The API returns HTTP 200. The frontend clears the pending-registration state, navigates to Sign In, and displays: "Email verified successfully. Please sign in."

Alternative Flow:

A.1 — Visitor already has an account

- At step 1, the visitor selects the Sign In tab/link and follows the Login use case. No registration request is sent.

A.2 — Email is already registered

- At step 5, the backend returns HTTP 409 with code `EMAIL_ALREADY_REGISTERED`.
- Display "This email is already registered. Please sign in." on the Sign Up page. The visitor can use the existing Sign In navigation.

A.3 — Correct and retry a verification code

- At step 11, mismatches 1–4 return HTTP 400 with code `INVALID_VERIFICATION_CODE`.
- The visitor may correct the code and retry while the registration remains valid and rate limits permit. The fifth mismatch follows E.5; a subsequent correct code cannot reactivate the same registration.

A.4 — Restart an incomplete registration

- If the code has expired, the registration has exhausted its five attempts, or the pending registration ID is missing after navigating to verification, direct the visitor back to the existing Sign Up page through an inline recovery link.
- The visitor submits registration again, subject to persistent per-email and per-IP registration rate limits. For an email with no active account, the backend creates a fresh pending registration and invalidates older pending registrations for that email. Restarting does not reset email/IP limiter counters.
- Only the newest registration remains valid. Resending within a still-valid registration uses A.5, without a new screen.

A.5 — Resend the verification code

- On Email Verification, the visitor selects the observed `Resend Code` link. Submit `POST /api/v1/auth/resend-verification` with the existing `registrationId`.
- Only an unexpired `PENDING` registration with fewer than five failed comparisons is eligible. Enforce a 60-second cooldown since the last admitted send and the shared email/IP send limits.
- Atomically replace the code hash with a newly generated, different six-digit code, increment `codeVersion`, and enter `PENDING_DELIVERY`. The previous code becomes invalid immediately. Keep the same registration ID, original `expiresAt`, and cumulative `verificationAttemptCount`; resend never grants more guesses or more time.
- Make one SMTP attempt. On acceptance and successful state finalization, return HTTP 200 with unchanged expiry and updated `resendAvailableAt`. Remain on this page, clear the input, and display the response message. The new code is usable only before the original expiry.
- Failure or uncertain delivery invalidates this registration under E.3. Expired or exhausted registrations follow A.4; they cannot be renewed through resend.

Exception Flow:

E.1 — Invalid form data

- At steps 4 or 5, missing/invalid fields, a password mismatch, or unaccepted terms prevent registration.
- Client validation displays errors below the relevant fields. Server validation returns HTTP 400 with code `VALIDATION_ERROR` and field-level messages using the same field names as the request.

E.2 — Pending registration expired or unavailable

- During verification or resend, an expired registration returns HTTP 410 with code `VERIFICATION_EXPIRED`.
- An unknown registration ID returns HTTP 404 with code `REGISTRATION_NOT_FOUND`.
- Display the supplied error and follow A.4. An already consumed registration returns HTTP 409 with code `ALREADY_VERIFIED`; direct the visitor to Sign In.

E.3 — Verification email delivery fails or is uncertain

- At step 7 or during A.5, a synchronous delivery-adapter failure returns HTTP 503 with code `VERIFICATION_DELIVERY_FAILED`.
- Invalidate the affected pending registration; do not create an active account. For initial delivery, stay on Sign Up; for resend, clear pending state and offer Sign Up.
- Display "Unable to send the verification email. Please try again." and allow a new registration attempt.
- In the experiment, success means Mailpit returned final SMTP `250` acceptance after DATA; connection or recipient acceptance alone is insufficient. Connection failure, an SMTP rejection, or the ten-second overall delivery deadline is failure. A timeout after sending DATA is treated as uncertain delivery: invalidate the registration and return the same HTTP 503 response, even if an email subsequently appears in Mailpit.
- There is no automatic adapter retry, frontend retry, or background resend. A.5 permits manual resend only while the current registration is valid; after delivery failure, a visitor-initiated restart under A.4 creates a new registration/code after the rate-limit window allows it. Old emails may remain visible but their invalidated codes cannot succeed.

E.4 — Network or server failure

- The frontend stops its loading state, stays on the current page, and displays a retryable error.
- An HTTP 500 response uses code `INTERNAL_ERROR`; do not expose database or delivery-provider details.
- If verification committed but the response was lost, a repeated request returns `ALREADY_VERIFIED`, allowing the visitor to continue to Sign In without creating another account.

E.5 — Verification attempt budget exhausted

- On the fifth well-formed, incorrect code, atomically set `verificationAttemptCount = 5`, state `INVALIDATED`, and reason `ATTEMPTS_EXHAUSTED`; commit these changes before returning an error.
- Return HTTP 409 with code `VERIFICATION_ATTEMPTS_EXHAUSTED`. Subsequent requests for this ID return the same error until the record is cleaned up, unless a request is rejected earlier by the rate limiter.
- Disable further verification and resend for that registration in the UI, clear its stored state, and offer the existing Sign Up route. This is invalidation, not a temporary lock.

E.6 — Request rate limit reached

- Return HTTP 429 with code `RATE_LIMIT_EXCEEDED`, integer `retryAfterSeconds`, and a matching `Retry-After` header in seconds.
- Do not send email, compare codes, increment the code-attempt counter, or invalidate any registration for a throttled request.
- Preserve the current form/pending state and disable the affected action for the returned delay. A resend cooldown alone does not disable verification. The server remains authoritative after the delay expires.

UI Integration:

- Confirmed source file: Clicon — eCommerce Marketplace Website Figma Template, user's copy.
- Visual evidence reviewed on 2026-09-17: the user-supplied Sign Up image `973660f5-af9d-4e00-8532-0841cb3a253a.png` and Email Verification image `7283e741-985a-40fa-826b-413e6ff87bae.png`.
- The images establish the visible fields, labels, buttons, and desktop layout described below. They do not expose Figma node metadata; the exact node links below come from the previously recorded project review, not from the screenshots themselves. Live rereads of those nodes remained blocked by the connector limit.
- Sign Up visibly contains Name, Email Address, Password (`8+ characters` placeholder), Confirm Password, two password-visibility icons, a checked terms checkbox in the captured state, Terms of Condition / Privacy Policy links, SIGN UP, and Google / Apple sign-up controls.
- Email Verification visibly contains Verify Your Email Address, placeholder descriptive text, one Verification Code input, Resend Code, and VERIFY ME. The input is not six separate OTP boxes. Resend is implemented by A.5.
- Preserve these supplied images as the experiment's fixed visual evidence. Screenshot capture date and Figma version are unknown; the date above is the review date. Six digits, ten minutes, five failed attempts, retry/cleanup rules, and API contracts are proposed experiment requirements, not facts established by these images.
- Sign Up: `19_Sign Up`, node `429:8800`.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=429-8800
- Email Verification: `20_Email Verification`, node `429:10404`.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=429-10404
- Successful completion destination: `16_Sign In`, node `429:7940`.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=429-7940
- Match the visible desktop layout, navigation, colors, fields, and button placement using the supplied screenshots. Exact font tokens, pixel dimensions, responsive behavior, and prototype interactions remain unverified.
- Loading indicators, inline errors, success feedback, and the recovery link are proposed interaction states. Dedicated Figma variants for those states have not been confirmed.
- This use case is visually supported by the supplied screenshots for its two core forms. Backend behavior and supplemental loading/error/recovery states remain explicitly proposed. No live-dataset refresh is claimed.

API Endpoint:

The following three public endpoints jointly implement this use case. None requires an existing login session.

| Operation | Endpoint |
| --- | --- |
| Start registration | `POST /api/v1/auth/register` |
| Complete email verification | `POST /api/v1/auth/verify-email` |
| Resend the verification code | `POST /api/v1/auth/resend-verification` |

Request Body:

Content type for all three endpoints: `application/json`. All properties shown are required. Unknown properties are rejected with `VALIDATION_ERROR`.

`POST /api/v1/auth/register`

```json
{
  "fullName": "Nguyen Van A",
  "email": "student@example.com",
  "password": "ExamplePass123!",
  "confirmPassword": "ExamplePass123!",
  "acceptTerms": true
}
```

| Field | Type | Proposed validation |
| --- | --- | --- |
| `fullName` | string | Trim surrounding whitespace; 2–100 characters after trimming. |
| `email` | string | Trim surrounding whitespace; valid email format; at most 254 characters; lowercase for this project's identity comparison. |
| `password` | string | At least 8 Unicode code points and at most 72 UTF-8 bytes; do not trim or otherwise transform. |
| `confirmPassword` | string | Must exactly equal `password`; never persist. |
| `acceptTerms` | boolean | Must be `true`; the string `"true"` is invalid. |

`POST /api/v1/auth/verify-email`

```json
{
  "registrationId": "0ab8c6be-9c13-4b9f-95c5-b4daf89d2ba1",
  "code": "042719"
}
```

- `registrationId`: UUID string returned by the registration endpoint.
- `code`: string matching `^[0-9]{6}$`; preserve leading zeroes. Do not send it as a number.

`POST /api/v1/auth/resend-verification`

```json
{
  "registrationId": "0ab8c6be-9c13-4b9f-95c5-b4daf89d2ba1"
}
```

- `registrationId`: UUID string for the current pending registration. The recipient is resolved on the server; do not accept a replacement email, code, attempt count, or expiry from the client.

Successful Response:

Registration — HTTP 201:

```json
{
  "message": "Verification email sent. Please check your inbox.",
  "registrationId": "0ab8c6be-9c13-4b9f-95c5-b4daf89d2ba1",
  "email": "student@example.com",
  "status": "PENDING_EMAIL_VERIFICATION",
  "expiresAt": "2026-09-17T10:10:00.000Z",
  "resendAvailableAt": "2026-09-17T10:01:00.000Z"
}
```

- `expiresAt` is an ISO 8601 UTC timestamp calculated by the server; the value above is illustrative.
- `registrationId` identifies a pending record, not an authenticated user.
- `resendAvailableAt` is an ISO 8601 UTC timestamp, 60 seconds after the latest admitted send. The server enforces cooldown and shared rate limits; reaching this timestamp alone does not guarantee admission.

Verification — HTTP 200:

```json
{
  "message": "Email verified successfully. Please sign in.",
  "user": {
    "id": "ab40a099-e81b-4cb3-8ae3-9601cb4c258f",
    "fullName": "Nguyen Van A",
    "email": "student@example.com",
    "status": "ACTIVE",
    "emailVerified": true
  }
}
```

Resend — HTTP 200 (example: a resend admitted at 10:02 UTC):

```json
{
  "message": "Verification code resent. Please check your inbox.",
  "registrationId": "0ab8c6be-9c13-4b9f-95c5-b4daf89d2ba1",
  "status": "PENDING_EMAIL_VERIFICATION",
  "expiresAt": "2026-09-17T10:10:00.000Z",
  "resendAvailableAt": "2026-09-17T10:03:00.000Z"
}
```

- Resend retains the original expiry; it does not start a new ten-minute window.
- No successful response contains a password, password hash, verification code, or authentication token.

Error Response:

All server errors use this envelope. `errors` is included only for `VALIDATION_ERROR`; otherwise it is omitted. HTTP 429 additionally includes `retryAfterSeconds` (a positive integer) and the matching `Retry-After` header; that property is absent from other errors.

```json
{
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "errors": {
    "confirmPassword": ["Passwords do not match."],
    "acceptTerms": ["You must accept the terms to continue."]
  }
}
```

`errors` is a map from request-field names to nonempty arrays of error strings. The example shows one possible set of validation failures.

| HTTP | Endpoint | `code` | Exact `message` |
| --- | --- | --- | --- |
| 400 | All three | `VALIDATION_ERROR` | `Please correct the highlighted fields.` |
| 409 | Register; Verify if an account was created concurrently | `EMAIL_ALREADY_REGISTERED` | `This email is already registered. Please sign in.` |
| 400 | Verify | `INVALID_VERIFICATION_CODE` | `The verification code is incorrect.` |
| 410 | Register finalization / Verify / Resend | `VERIFICATION_EXPIRED` | `Your verification code has expired. Please register again.` |
| 404 | Verify / Resend | `REGISTRATION_NOT_FOUND` | `Registration not found. Please register again.` |
| 409 | Verify / Resend | `ALREADY_VERIFIED` | `This email has already been verified. Please sign in.` |
| 409 | Verify / Resend | `VERIFICATION_ATTEMPTS_EXHAUSTED` | `Too many incorrect verification attempts. Please register again.` |
| 409 | Verify / Resend | `VERIFICATION_NOT_READY` | `Verification email is not ready. Please try again shortly.` |
| 429 | All three | `RATE_LIMIT_EXCEEDED` | `Too many requests. Please try again later.` |
| 503 | Register / Resend | `VERIFICATION_DELIVERY_FAILED` | `Unable to send the verification email. Please try again.` |
| 500 | All three | `INTERNAL_ERROR` | `Unable to complete your request. Please try again later.` |

Example non-validation error:

```json
{
  "statusCode": 400,
  "code": "INVALID_VERIFICATION_CODE",
  "message": "The verification code is incorrect."
}
```

Example throttling response — HTTP 429, header `Retry-After: 45`:

```json
{
  "statusCode": 429,
  "code": "RATE_LIMIT_EXCEEDED",
  "message": "Too many requests. Please try again later.",
  "retryAfterSeconds": 45
}
```

The delay is illustrative; calculate it from the actual limiter state.

## Project-Specific Implementation Context

### Backend Implementation Context

Implementation objective:

Implement pending registration and email verification in NestJS according to the proposed contracts above. This section is a new Clicon proposal corresponding to Prompt A, not extracted Technical Report content.

Required project behavior:

- Define the three routes in `AuthController`; put business logic in `AuthService` and email delivery behind a `VerificationEmailService` interface.
- Use DTO validation for request types, required properties, and the rules in Request Body. Ensure validation exceptions follow the documented error envelope instead of returning an incompatible framework-default body.
- Store pending registration data separately from active customer accounts. Required pending data: ID, normalized email, trimmed full name, password hash, terms-acceptance timestamp, verification-code hash, `issuedAt`, `expiresAt`, `verificationAttemptCount`, `codeVersion` (initially 1), `lastSendAttemptAt`, `resendAvailableAt`, `invalidatedAt`, `invalidationReason`, `consumedAt`, `cleanupEligibleAt`, and state (`PENDING_DELIVERY`, `PENDING`, `CONSUMED`, or `INVALIDATED`). Unused event timestamps are null. Sensitive fields must be nullable to allow erasure under the cleanup policy below.
- Hash the password with bcrypt using cost 12 for this proposed implementation. The 72-byte validation limit must be enforced before hashing. Store an HMAC-SHA-256 digest of the verification code keyed by a server secret, bound to registration ID and code version; use a constant-time comparison. Send the plaintext code only to the email adapter.
- Registration must not issue a JWT or create an authenticated session.
- Serialize changes to pending registrations for the same normalized email so restarting registration leaves only one current pending record. A restart must not overwrite an active account.
- A delivery-adapter rejection invalidates the new pending record and returns the documented HTTP 503 response. Verification must never accept an invalidated record.
- At verification or resend, apply rate limits and DTO validation, then lock/recheck the record: missing returns `REGISTRATION_NOT_FOUND`; consumed returns `ALREADY_VERIFIED`; invalidated with reason `ATTEMPTS_EXHAUSTED` returns `VERIFICATION_ATTEMPTS_EXHAUSTED`; other invalidated records return `REGISTRATION_NOT_FOUND`; any remaining record at or past `expiresAt` returns `VERIFICATION_EXPIRED`; unexpired `PENDING_DELIVERY` returns `VERIFICATION_NOT_READY`. Only an unexpired `PENDING` record with attempt count below five can compare a code. A post-cleanup missing record returns `REGISTRATION_NOT_FOUND`, including for previously consumed IDs.
- Within a database transaction, lock/recheck the pending record and compare the code. A mismatch must commit its counter increment and, on the fifth mismatch, invalidation before the service returns its 400/409 response; throwing inside the transaction must not roll back the attempt counter. For a correct code, atomically create the customer with status `ACTIVE` and `emailVerifiedAt` and consume the pending record; roll back both successful-verification changes if that transaction fails.
- Enforce a unique normalized-email constraint on active accounts. Map a uniqueness conflict during verification to `EMAIL_ALREADY_REGISTERED`; do not create another account.

Verification attempt and rate-limit policy (fixed experiment parameters):

| Control | Limit | Scope / window |
| --- | --- | --- |
| Incorrect code budget | 5 mismatches total | Per registration ID across its entire lifetime; not a rolling reset |
| Verify requests | 5 requests / 60 seconds | Per registration ID, across all IPs |
| Verify requests | 30 requests / 60 seconds | Per client IP, across all registration IDs |
| Resend cooldown | At least 60 seconds between admitted sends | Per registration ID, including the initial send; no reset on mismatch |
| Register / restart / resend requests (shared budget) | 3 requests / 15 minutes | Per normalized email, across all IPs |
| Register / restart / resend requests (shared budget) | 10 requests / 15 minutes | Per client IP, across all emails |

- Use shared, atomic server-side sliding-window counters across application instances; no process-local-only limiter. Enforce all applicable scopes, rather than using a combined ID+IP key that would permit IP rotation to bypass the ID limit.
- The IP limiter charges every inbound request to its endpoint, including malformed bodies. If a valid UUID/email key can be parsed, charge the applicable ID/email limiter too. For resend, resolve the normalized email from the pending record and charge the same email budget used by register/restart; do not create a separate resend quota. Missing/erased records still face IP limits. Atomically admit across applicable scopes; a rate-limit-rejected request adds no timestamps to their windows. Requests admitted by the limiter still count if later rejected by DTO/state validation. Rate-limit rejections do not extend the window; compute the wait until all exceeded scopes permit another request and return that delay rounded up to seconds.
- Count well-formed wrong codes only after delivery/state/expiry checks pass. Malformed codes, throttled requests, expired/missing/consumed IDs, and server errors do not increment `verificationAttemptCount`; they still face request rate limits.
- Initialize `lastSendAttemptAt` on the initial admitted send and `resendAvailableAt = lastSendAttemptAt + 60 seconds`; update them on each admitted resend, including attempts that later fail. Compute a cooldown rejection as HTTP 429 with the maximum wait across exceeded scopes.
- Serialize code comparisons for the same record. Parallel requests cannot obtain more than five failed comparisons, and even a correct code cannot succeed after the fifth mismatch committed.
- Rate-limit storage uses hashed/HMAC identifiers for IP/email keys and expires counters at the end of the applicable window. Restarting registration or deleting a pending record must not reset these counters.
- Resolve client IP from the connection or explicitly trusted reverse proxies only; ignore arbitrary forwarded headers. If shared limiter storage is unavailable, fail closed with `INTERNAL_ERROR` before sending email or comparing codes.

Resend transition:

- Lock the pending row and apply the same terminal-state/expiry checks as verification. Admit only one send at a time. Generate a different code (compare its digest at the old version against the old digest before accepting it), increment `codeVersion`, replace the digest, and commit `PENDING_DELIVERY` before starting SMTP.
- Keep `issuedAt`, `expiresAt`, and `verificationAttemptCount` unchanged. Resend does not reset verification request windows or cleanup deadlines. Verification and resend share the row lock so comparison cannot race with code replacement.
- On finalization, compare registration ID, code version, state, current-registration marker, and expiry. A superseded/invalidated attempt cannot finalize. If the original expiry passed during SMTP, return `VERIFICATION_EXPIRED` (410), leave it expired/non-verifiable, and keep expiry-based cleanup deadlines.
- The old code is not restored on delivery failure. Invalidate the registration and require A.4. No SMTP/network operation holds a database transaction open; commit before sending and use guarded finalization afterward.

Pending registration retention and cleanup:

- Set `cleanupEligibleAt` to `expiresAt + 24 hours` for an expired pending record, `invalidatedAt + 24 hours` for an invalidated record, or `consumedAt + 24 hours` for a consumed record. Later retries must not extend these deadlines.
- On consumption or invalidation, erase the pending copy of full name, raw email, password hash, verification-code hash, and terms-acceptance timestamp in the same committed state transition. Keep only the ID, state/reason, attempt count, code version, and lifecycle/cooldown timestamps until deletion. Successful registration keeps the required data in the active user record; it does not keep a second sensitive copy in the pending table.
- Run an idempotent cleanup job hourly and on service startup. It erases sensitive fields of all expired records and permanently deletes records at or past `cleanupEligibleAt`, in bounded batches with row locks so cleanup and verification do not race.
- During normal operation, expired sensitive data is erased within one hour of expiry; terminal metadata is deleted within 25 hours of expiry/invalidation/consumption. On downtime, overdue work runs at startup before registration/verification traffic resumes. This is an operational target, not a promise of deletion during downtime.
- Hourly cleanup treats unfinished `PENDING_DELIVERY` records as expired when `expiresAt` passes. They are never verifiable. No cleanup error may delete an active customer or reactivate a registration.
- Do not log passwords, codes, email bodies, or raw pending records. For this local research dataset, disable persistent database backups and use disposable Mailpit storage; purge captured emails after each run and at least every 24 hours during long runs. These settings prevent deleted pending data from remaining in the experiment mailbox or backups.

Mailpit delivery contract and retry behavior:

- Use Mailpit as the experiment's local SMTP sink. With a Compose service named `mailpit`, the backend connects to `mailpit:1025`; with the backend on the host and the SMTP port published locally, use `127.0.0.1:1025`. Publish the test inbox UI on loopback port `8025`. Do not relay or forward messages externally.
- The adapter receives the recipient email, six-digit code, registration ID, code version, and expiry. Use a message correlation ID derived from registration ID plus code version so the test harness can identify the latest send without confusing older emails.
- Success: final SMTP `250` acceptance after DATA is received within a ten-second overall deadline, and the backend commits the transition from this still-current `PENDING_DELIVERY` record to `PENDING`. Only then return HTTP 201 for register or HTTP 200 for resend. Verify that the record and code version were not superseded and expiry has not passed before transitioning; a superseded send returns HTTP 503 and must not resurrect the older code.
- Failure: refused connection, DNS/socket failure, any SMTP 4xx/5xx rejection, or deadline expiry causes one failure result. Invalidate this record and return `VERIFICATION_DELIVERY_FAILED` (503). If persistence itself fails, return `INTERNAL_ERROR` (500); the unfinalized record remains non-verifiable.
- Treat timeout/disconnection after DATA but before the final reply as uncertain delivery and invalidate the code. A late SMTP callback cannot move an invalidated record back to `PENDING`.
- Make one SMTP attempt per admitted registration or resend request. Disable automatic SMTP retries, job retries, and client automatic POST retries. Do not retry a possibly accepted message with the same code. Visitor-triggered restart follows A.4 and the same registration rate limits, generating a new ID/code and invalidating previous ones.
- SMTP acceptance is the adapter's delivery result; separately, the test harness must confirm the correlated message is visible in Mailpit before extracting its code. Fail the email-delivery test if it cannot find the message; do not substitute a hard-coded code or query a database plaintext code.
- For reproducible failure tests, use an injected adapter mode that returns rejection before SMTP and a separate mode that simulates lost acknowledgement after SMTP acceptance. These are test-only dependency-injection settings, never public API parameters.
- Pin the Mailpit image version/digest and record it with the experiment configuration before runs; the release choice is not defined by Figma.
- Mailpit port and configuration reference: https://mailpit.axllent.org/docs/configuration/


REQUEST FORMAT:

Use the three Request Body contracts exactly, including camelCase names, boolean `acceptTerms`, and string `code`.

SUCCESS RESPONSE FORMAT:

Use the HTTP 201 and HTTP 200 Successful Response contracts exactly. No implicit auto-login.

Error Handling:

Use the HTTP status, code, and message mappings in Error Response consistently across controller validation, service logic, and database-conflict handling.

### Frontend UI Context

Implementation objective:

Build the registration and email-verification views in React, TypeScript, and Tailwind CSS, using the existing Clicon frames as the visual references. This section corresponds to proposed Prompt B.

Required project behavior:

- Implement `SignUpPage` / `SignUpForm` at `/sign-up` and `EmailVerificationPage` / `EmailVerificationForm` at `/verify-email`.
- Reuse Clicon's header, footer, authentication tabs, form styles, and primary-button treatment from the source design.
- Screenshot-verified mapping:

| Visible control | Implementation binding / behavior |
| --- | --- |
| Name | `fullName` |
| Email Address | `email` |
| Password, placeholder `8+ characters` | `password`; independent show/hide toggle |
| Confirm Password | `confirmPassword`; independent show/hide toggle |
| Terms checkbox; Terms of Condition / Privacy Policy links | `acceptTerms`; the captured state is checked, but the screenshot does not establish an initial-state rule |
| SIGN UP | `handleRegister` |
| Sign In tab | `/sign-in` |
| Sign up with Google / Sign up with Apple | Visible, disabled with scope explanation for this email/password experiment |
| Verification Code | One text input bound to string `code`, with `inputMode="numeric"` and leading zeroes preserved |
| Resend Code | `handleResend`; maintain link placement and expose disabled state accessibly |
| VERIFY ME | `handleVerify` |

- Proposed initial-state rule: initialize `acceptTerms = false`; the user checks it before submitting. This behavior is an explicit experiment decision; the supplied screenshot depicts its checked state. Terms/privacy destinations need project content and are not specified by these screenshots; do not invent external policy links.
- Preserve the verification heading `Verify Your Email Address`. Replace the visible placeholder paragraph with the proposed functional copy: `Enter the 6-digit code sent to your email address.`; this text is an implementation proposal.
- Keep Sign In navigation directed to `/sign-in`.
- Keep labels associated with inputs. Display validation feedback next to the corresponding field, and general request failures inside the current form.
- Show loading and success feedback using the existing design language; do not add a separate success screen when the existing Sign In screen can show the completion message.
- The screenshots verify the mapping above. Additional loading, error, cooldown, and recovery states must follow these proposed rules; exact typography tokens and responsive layouts remain unverified.

Figma references:

- Sign Up: https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=429-8800
- Email Verification: https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=429-10404

### Frontend Logic and API Context

Implementation objective:

Connect both forms to the proposed API and preserve the registration-to-verification flow. This section corresponds to proposed Prompt C.

Required project behavior:

State:

- Sign Up: `fullName`, `email`, `password`, `confirmPassword`, `acceptTerms`, `isSubmitting`, `fieldErrors`, and `formError`.
- Verification: `registrationId`, `email`, `expiresAt`, `resendAvailableAt`, `code`, `isVerifying`, `isResending`, per-action retry deadlines, `fieldErrors`, and `formError`.

REQUEST CONTENT:

- `handleRegister`: validate locally, clear outdated errors, set `isSubmitting`, and send the registration request with the exact property names in Request Body.
- On HTTP 201, persist only `{ registrationId, email, expiresAt, resendAvailableAt }` under `clicon.pendingRegistration` in `sessionStorage`, clear both password fields, and navigate to `/verify-email`.
- On verification-page load, recover the pending data from `sessionStorage`. If missing or malformed, return to `/sign-up` with a short explanation; do not submit a request with an empty ID.
- `handleVerify`: validate the six-digit string, set `isVerifying`, and submit `{ registrationId, code }`.
- `handleResend`: submit only `{ registrationId }`, set `isResending`, and clear the old code when the request is sent because the server may invalidate it even if the response is lost. On HTTP 200, keep the ID/email, update expiry/resend availability in session storage, and display the exact resend success message without navigating. Never reset the attempt budget in UI or server state.
- Use server time/expiry validation as authoritative. A client countdown is optional and cannot determine acceptance of a code.

After a successful response:

- On verification HTTP 200, remove `clicon.pendingRegistration`, clear the code, and navigate to `/sign-in` with the exact success message from the response.
- Do not store a login token or mark the user as authenticated.
- For `ALREADY_VERIFIED` or `EMAIL_ALREADY_REGISTERED`, clear pending state and offer the existing Sign In destination.
- For `VERIFICATION_ATTEMPTS_EXHAUSTED`, clear pending state and offer Sign Up; do not automatically re-register.
- For HTTP 429, retain current state, read `retryAfterSeconds`, and display the wait while disabling the affected action. Cooldown for resend does not disable VERIFY ME. If frontend and API are cross-origin, expose `Retry-After` through CORS; the response-body delay remains available to the client.
- Starting a fresh registration replaces the old pending data only after the new registration request succeeds.

### Validation and Error-Handling Context

Implementation objective:

Make success, retry, and failure behavior consistent across the UI and API. This section corresponds to proposed Prompt D.

Loading State:

- While a registration request is in flight, disable Sign Up and prevent duplicate submission.
- While verification or resend is in flight, disable both VERIFY ME and Resend Code to prevent conflicting submissions.
- Clear the loading flag in `finally`. The affected action remains disabled while its rate-limit delay is active; both verification actions remain disabled after expiry or attempt exhaustion; ending network activity alone must not re-enable it.

API Error Handling:

- Map `VALIDATION_ERROR.errors` to the corresponding fields without renaming request keys.
- Display `INVALID_VERIFICATION_CODE` below the verification-code control and allow correction for attempts 1–4.
- Display `VERIFICATION_ATTEMPTS_EXHAUSTED`, disable VERIFY ME and Resend Code for this ID, clear pending state, and offer Sign Up.
- Handle HTTP 429 according to E.6 without retrying automatically. For `VERIFICATION_NOT_READY`, retain state and allow a manual retry; do not create a session.
- Display `VERIFICATION_EXPIRED` or `REGISTRATION_NOT_FOUND`, clear unusable pending state, and provide navigation back to the existing Sign Up page.
- Preserve the pending registration after an unknown verification-network failure so the visitor can retry. A retry returning `ALREADY_VERIFIED` directs them to Sign In.
- For an unknown resend-network failure, retain the registration ID, keep the input cleared, and do not automatically resend. The visitor can inspect the newest local mailbox message and manually verify or retry after any returned cooldown; authoritative state errors determine recovery. For explicit `VERIFICATION_DELIVERY_FAILED` on resend, clear unusable pending state and offer Sign Up.
- For an unknown registration-network failure, do not assume that the server failed to create a pending record. Allow a fresh registration request under the documented restart behavior.
- If no HTTP response exists, display "Unable to connect. Please check your connection and try again." Do not invent a server status code.
- Unexpected or malformed server responses display "Unable to complete your request. Please try again later." and must not trigger a success redirect.

Client-side Validation:

- Apply the same name, email, password, confirmation, and terms rules defined in Request Body.
- Count password minimum length by Unicode code points (`Array.from(password).length`) and maximum length by UTF-8 bytes (`new TextEncoder().encode(password).length`).
- Require exactly six ASCII digits for the verification code and preserve leading zeroes.
- Never submit invalid local form data; server-side validation still runs for every request.

Validation examples for the research run:

- Valid registration followed by the delivered code creates one active account and returns the visitor to Sign In.
- Submitting registration alone leaves the visitor unauthenticated and creates no active account.
- A password mismatch or unchecked terms produces field feedback and no registration request.
- An existing active email returns HTTP 409 without creating or overwriting an account.
- A wrong or expired code creates no active account; a valid code such as `042719` is accepted as a six-character string.
- Initial email-adapter failure returns HTTP 503 and keeps the visitor on Sign Up; resend delivery failure offers Sign Up and clears the invalidated registration.
- Repeating a completed verification does not create a second account; a consumed registration directs the visitor to Sign In.

- Five wrong-code submissions result in four HTTP 400 responses followed by HTTP 409 `VERIFICATION_ATTEMPTS_EXHAUSTED`; a later correct code for that ID cannot create an account. A rate-limit response may precede a state error if its window is already full.
- Concurrent wrong-code requests do not increment the counter above five or roll back committed failed-attempt increments.
- Changing IP does not bypass the registration-ID limiter; changing registration IDs does not bypass the IP limiter. Restarts cannot bypass the normalized-email registration limiter.
- HTTP 429 includes consistent `Retry-After` and `retryAfterSeconds`, does not compare a code or send mail, and does not trigger automatic UI retries.
- An expired pending record's secrets are erased at the next hourly cleanup; terminal records are deleted at the specified deadline and active accounts remain unchanged. Cleanup is repeatable and startup catches up overdue work.
- Mailpit final acceptance yields one correlated message and HTTP 201. Connection rejection or a simulated lost acknowledgement yields HTTP 503 and a non-verifiable old code. A manual restart after the limiter allows it generates a fresh ID/code.
- Resend succeeds after cooldown for an unexpired registration; it preserves ID, original expiry, and attempt count, makes the previous code invalid, and creates one newly correlated Mailpit message. Shared register/resend limits and the 60-second cooldown apply across IPs.
- After four wrong comparisons, a successful resend leaves the count at four; the next wrong comparison invalidates the registration. Resend near expiry never extends validity. A send accepted by SMTP after expiry does not activate its code and returns HTTP 410.
- Concurrent resend/verification, late callbacks, SMTP failure, and lost HTTP responses cannot restore an older code or reset the attempt budget. A resend network failure triggers no automatic POST.
- Compare the two rendered forms with the supplied screenshots: exact observed labels, single code input, Resend Code placement, password toggles, and shared shell. Record proposed copy/initial-checkbox/OAuth-scope differences explicitly. UI evidence is `VERIFIED_FROM_USER_SCREENSHOTS` for visible controls/layout only; backend tests do not establish live Figma freshness or unseen states.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
