# UC-02: Sign In to a Job Seeker Account

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Sign In to a Job Seeker Account

Description:

- Allows a registered Job Seeker to authenticate with email/password, optionally select Remember me, and continue to the available jobs or an inspected job detail.
- Activates UC-01's previously unavailable Sign In links. It uses the account identity and initial flags already defined there; unverified contact fields do not block login in this experiment.
- Figma supplies the visible sign-in controls. Session behavior, observable limits, contracts, and destinations below are project decisions, not a quoted Technical Report or inferred prototype behavior.

Primary Actor:

Registered Job Seeker. An already authenticated eligible Job Seeker may resume the existing session.

Preconditions:

- UC-01 account persistence and credential creation are implemented. Eligible accounts have role=JOB_SEEKER and status=ACTIVE.
- `/sign-in` and `/sign-up` exist. `/jobs` is the post-login destination supplied by UC-03 in the same implementation batch; `/jobs/:jobId` is supplied by UC-04.
- If UC-02 is implemented independently before UC-03, implement a minimal `/jobs` integration shell showing the confirmed account name and `Job listings will be available in the next feature.` It is replaced by UC-03, not counted as a separate UI use case.
- Browser frontend/API use UC-01's same-origin deployment. Browser sessions are cookie-based; authentication tokens are not returned in JSON.

Postconditions:

- Success: The presented browser has an authenticated session for the eligible account, the client confirms it, clears the password, and reaches an implemented destination.
- rememberMe=false gives an eight-hour absolute server lifetime and a nonpersistent browser cookie. rememberMe=true gives a 30-day absolute lifetime and browser persistence up to that expiry. Browser restarts do not guarantee logout if the browser restores nonpersistent cookies; server expiry remains authoritative.
- Reads do not extend expiry. Independent browser sessions may coexist. Login does not alter profile completeness, publish an applicant, verify contact ownership, submit an application, or change roles.
- Failure: No successful sign-in is announced. A lost response is an unknown outcome until session reconciliation.

Main Flow:

1. The visitor opens `/sign-in`. Read the current session before offering a new login.
2. If no eligible session exists, show Email address, Password, and unchecked Remember me.
3. The visitor enters credentials and selects Sign in.
4. Validate locally, submit the exact request, and disable repeat submit while pending.
5. The backend validates fields, enforces the login budget, checks credentials and account eligibility, and establishes the browser session.
6. After successful POST, GET the session to confirm the browser can present it. Clear the password.
7. Navigate to the validated job detail continuation, or `/jobs` by default. Do not send incomplete profiles to an undefined onboarding page.

Alternative Flow:

A.1 — Already signed in

- A successful session read routes to the same validated destination without another credential submission or lifetime extension.
- POST with an already valid eligible session returns ALREADY_AUTHENTICATED and leaves it unchanged, even if different credentials are submitted. Re-read the session rather than treating this as an account-switch feature.

A.2 — Continuing to a job

- `/sign-in` accepts an optional browser-only next value. After normal URL decoding, permit only `/jobs` or `/jobs/<UUID>`, without nested query, fragment, host, or scheme. Invalid values fall back to `/jobs`.
- next is not sent to the authentication API. UC-04 can invoke the same login handler inline and, after session confirmation, reload that current job's member details.
- If the intended job has become unavailable, show UC-04's unavailable state with Back to jobs. Never invent an application or redirect to an arbitrary URL.

A.3 — Sign-up and deferred recovery

- Sign up opens `/sign-up`; UC-01 successful registration can now lead to `/sign-in`. Registration remains a separate unauthenticated operation.
- Keep Forgot your password? visible but unavailable with `Password recovery is not available yet.` until its own UC supplies a real recovery route and contract. Do not simulate sending email or route to a missing screen.

A.4 — Uncertain login or unavailable session confirmation

- Do not automatically re-POST credentials after a timeout. GET the session to reconcile: HTTP 200 confirms its actual account; HTTP 401 means no usable session was presented and permits deliberate login; service failure remains unresolved.
- Always render the identity returned by the confirmed session. A session established in another tab must not be attributed to the email typed into this form.
- If POST succeeds but the follow-up GET returns 401, show `Your session could not be confirmed. Please sign in again.` Do not navigate as authenticated or replay credentials in a loop.

Exception Flow:

E.1 — Invalid credentials or ineligible account

- Unknown email, incorrect password, non-ACTIVE account, and unsupported role all return 401 INVALID_CREDENTIALS with the same message. Contact verification flags false and INCOMPLETE profile are allowed, consistent with UC-01.
- Preserve email and Remember me, clear password, and show the form-level error. No automatic verification or recovery message is sent.

E.2 — Observable login limit

- At most five credential evaluations per normalized email and 30 per client IP in a rolling 15 minutes; successful and failed evaluations count. Success does not reset either allowance.
- Structurally invalid requests and ALREADY_AUTHENTICATED consume no credential evaluation. Apply the same budgets to unknown emails. Denied requests do not extend the wait.
- Return RATE_LIMITED with the remaining time until both budgets permit another evaluation. Existing sessions are not invalidated by this limit. The client does not resubmit automatically when the wait ends.

E.3 — Expired or ineligible session

- GET rechecks current account eligibility and expiry. Missing, expired, disabled-account, or unsupported-role sessions return UNAUTHENTICATED; clear private frontend state.
- Session expiry does not prevent viewing UC-03/04's public content. It does remove access to member detail, which must be cleared before displaying the guest view.

E.4 — Service failure

- AUTHENTICATION_UNAVAILABLE and INTERNAL_ERROR do not establish a confirmed client login. Preserve non-password form state and offer a deliberate retry or session check. Do not expose service diagnostics in UI messages.

UI Integration:

- File: DH Dental Recruitment (Community), `5PvZvQ4E6DepIhbL8D35cV`; page Pages / Job Seeker (`1:2`).
- [Sign in, frame `2:2592`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-2592): Email address, masked Password, Remember me, Forgot your password?, Sign in, and Sign up.
- Public Job Details `2:2309` contains a compact copy of this form; UC-04 reuses the same behavior, not a second authentication mechanism.
- Live design context and screenshot inspected on 2026-09-23. Desktop controls/layout are supported; errors, loading, session behavior, mobile arrangement, and integration shell are project supplements. No frozen Figma version/checksum is claimed.
- Preserve the white card, Inter typography, teal action, and DentiHire header/footer. On narrow screens fit the form without horizontal overflow. After login, replace guest sign-in links with the confirmed display name; do not expose employer controls.
- Source navigation to unfinished features remains visibly unavailable. This UC does not implement sign-out, recovery, or recommendations through placeholder success actions.

API Endpoint:

- `POST /api/v1/auth/login`
- `GET /api/v1/auth/session`

No API query parameters. GET has no body.

Request Body:

```json
{
  "email": "alex.morgan@example.com",
  "password": "ResearchDemo42!",
  "rememberMe": false
}
```

POST accepts exactly these three required keys. email is trimmed/lowercased, valid and at most 254 characters, preserving dots and plus suffixes. password is exactly entered, 8–128 Unicode code points under UC-01; do not trim or normalize. rememberMe must be boolean, not a string. No role, user ID, next, lifetime, or verification flag is accepted.

Successful Response:

```json
{
  "success": true,
  "message": "Signed in successfully.",
  "data": {
    "user": {
      "id": "137a3a0f-dc84-460d-9c97-03f3cf6dcae7",
      "firstName": "Alex",
      "lastName": "Morgan",
      "email": "alex.morgan@example.com",
      "mobileNumber": "+12025550123",
      "role": "JOB_SEEKER",
      "status": "ACTIVE",
      "emailVerified": false,
      "mobileVerified": false,
      "profileCompletionStatus": "INCOMPLETE",
      "createdAt": "2026-09-23T09:00:00.000Z"
    },
    "session": {
      "expiresAt": "2026-09-23T18:00:00.000Z",
      "rememberMe": false
    }
  }
}
```

Both endpoints return HTTP 200. GET uses message `Session loaded.` with the same exact data shape. user has exactly UC-01's summary fields shown above, populated from current persisted state rather than a registration receipt. profileCompletionStatus is INCOMPLETE in this batch; a later profile-completion UC must define any additional state and its calculation. Verification flags are booleans and do not express professional certification.

session has exactly expiresAt (UTC ISO 8601) and rememberMe (boolean). The example begins at 10:00 UTC and expires at 18:00 UTC. With Remember me true, expiry is exactly 30*24 hours from establishment. No access/refresh token, session credential, password, or password metadata appears in JSON.

Error Response:

```json
{
  "success": false,
  "statusCode": 401,
  "code": "INVALID_CREDENTIALS",
  "message": "Email or password is incorrect.",
  "timestamp": "2026-09-23T10:00:00.000Z",
  "path": "/api/v1/auth/login"
}
```

All errors use success=false, statusCode matching HTTP status, code, message, server UTC ISO 8601 timestamp, and actual pathname without query. Omit data. VALIDATION_ERROR includes errors mapping input field paths to nonempty arrays of strings. Other errors omit errors; a 429 response additionally has a positive integer retryAfterSeconds matching Retry-After. All successful fields shown or defined are required unless explicitly nullable.

| Endpoint | HTTP | Code | Exact message |
| --- | --- | --- | --- |
| Both | 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| Login | 401 | INVALID_CREDENTIALS | Email or password is incorrect. |
| Session | 401 | UNAUTHENTICATED | Please sign in to continue. |
| Login | 409 | ALREADY_AUTHENTICATED | You are already signed in. |
| Login | 429 | RATE_LIMITED | Too many sign-in attempts. Please try again later. |
| Both | 503 | AUTHENTICATION_UNAVAILABLE | Sign-in is temporarily unavailable. Please try again later. |
| Both | 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

## Project-Specific Implementation Context

### Backend Implementation Context

Implement NestJS/TypeScript authentication over UC-01 Accounts. Use its normalized email and exact password interpretation, with server-controlled eligibility and lifetime. Login establishes a browser session; GET reads current account/session state without renewing it. Keep observable budgets and generic rejection behavior consistent, without prescribing cryptographic, limiter, or cookie implementation algorithms in this UC.

### Frontend UI Context

Implement the inspected React/TypeScript/Tailwind form and reusable compact variant. Show a pending state during initial session detection and avoid flashing an unauthenticated form for a valid session. Keep labels, Remember me default, password masking, field feedback, and unavailable recovery explanation consistent across variants.

### Frontend Logic and API Context

Confirm POST outcomes through GET before navigating. Preserve only email/checkbox after a definite error; never put credentials in browser URLs or persistent form storage. Use the restricted browser next route rules above. This UC explicitly activates UC-01 sign-in navigation and its ALREADY_AUTHENTICATED behavior; it does not copy EdTech onboarding routes or require verified email.

### Validation and Error-Handling Context

Use client validation for feedback and authoritative backend validation for acceptance. Interpret 401 according to the endpoint: rejected credentials versus absent session. Distinguish rate limits, unknown outcomes, and service failures from bad passwords. A confirmed account name and available destination are required before showing sign-in success.
