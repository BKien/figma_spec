# UC-02: Sign In to a Student Account

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Sign In to a Student Account

Description:

- Allows a registered Student to sign in with email and password, optionally remain signed in across browser restarts, and reach the appropriate authenticated destination.
- Continues UC-01 using its normalized email, password, account eligibility, and onboarding state. Registration verification alone does not authenticate a browser.
- Session duration, API contracts, limits, and routing are EdTech project decisions. The Figma Login frame supplies the visible controls. No existing backend contract or Technical Report is being quoted.
- Instructor support remains an approved separate extension. This UC authenticates Student accounts; it neither creates Instructor accounts nor interprets a client-selected role as authority.

Primary Actor:

Student with an existing account.

Preconditions:

- UC-01 account persistence and password credentials exist.
- The account has role STUDENT, status ACTIVE, and emailVerified=true to qualify for successful login. Pending registration records are not accounts.
- `/sign-in` and the integration destinations defined below are implemented with direct-navigation and reload support.

Postconditions:

- Success: The browser has a valid cookie-based account session. The frontend obtains the current account summary and session expiry and opens its permitted destination.
- Failure: Rejected credentials create no session. Failed login does not change account status, verification, onboarding, course enrollment, or an existing unrelated session.
- An ambiguous network outcome remains unresolved until a session read or a deliberate new login establishes the current state.

Main Flow:

1. The Student opens `/sign-in`; the frontend checks the current session before displaying an actionable login form.
2. With no valid session, display Email, Password, Remember Me, and Login. Remember Me starts unchecked.
3. The Student enters their credentials, optionally selects Remember Me, and submits once.
4. The backend validates input, applies the declared login limit, and checks credentials and account eligibility.
5. On success, create a browser session with the selected lifetime and return the success envelope. The browser receives its session credential through cookie transport, not the JSON response.
6. The frontend clears the password and reads `/api/v1/auth/session` to confirm that the browser can use the session.
7. Route NOT_STARTED or IN_PROGRESS students to `/student/onboarding`; route COMPLETED students to `/student/dashboard`.
8. The destination renders authenticated account context. Login itself does not mark onboarding complete or fabricate learning progress.

Alternative Flow:

A.1 — Remember Me

- false: session expires eight hours after creation and uses nonpersistent browser-cookie transport. Browser-session restoration may preserve browser state; closing a window is not promised to terminate the server session immediately.
- true: session expires 30 days after creation and may survive browser restarts until that expiry.
- These are absolute lifetimes: navigation and session reads do not extend expiry. Remember Me never stores the password or pre-fills it from project storage.
- At or after expiresAt the session is unusable. Device/browser storage restrictions may prevent persistence even when selected; the application must confirm the current session before entering protected routes.

A.2 — Already signed in

- GET session 200 bypasses the form and routes the returned account according to its current onboarding state.
- If a valid supported session reaches POST login despite the entry check, return 409 ALREADY_AUTHENTICATED without switching accounts or extending that session. The frontend reads the current session and continues as that account with visible account identity.
- Switching accounts belongs to sign-out followed by sign-in. No all-device logout, session-management interface, or implicit account switch is added here.

A.3 — Registration and deferred integrations

- Sign Up opens UC-01's `/sign-up`. UC-01's completed-registration Sign in action becomes enabled when this UC is implemented.
- Keep Forgot Password visible but disabled with `Password recovery is not available yet.` until its own UC defines a working route. Do not link it to an unimplemented page or simulate sending email.
- Google, Apple, and Facebook controls are visible but disabled with an explanation, as in UC-01. No social-provider request is made.

A.4 — Destination integration shells

- Implement `/student/onboarding` now as an authenticated integration shell showing the student's name and `Account setup will be available here.` It leaves onboardingStatus unchanged. A later onboarding UC replaces its content on the same route.
- Implement `/student/dashboard` now as an authenticated integration shell showing the student's name and `Your learning dashboard will be available here.` It does not display fabricated courses, grades, or percentages. A later dashboard UC replaces its content.
- These shells are required integration work within UC-02, not additional UI use cases and not completed implementations of the Figma onboarding/dashboard frames.
- The onboarding shell redirects COMPLETED accounts to the dashboard. The dashboard shell redirects incomplete accounts to onboarding. Guards use the same successful session read, avoiding a redirect loop.
- Ignore any user-supplied returnTo or redirect query when selecting a destination. This UC only supports the two account-state destinations above.

Exception Flow:

E.1 — Incorrect or ineligible credentials

- Unknown account, wrong password, unverified account, inactive account, pending registration, or unsupported role returns the same 401 INVALID_CREDENTIALS message. Do not return the failing condition, account status, or verification state.
- Display a form-level message, preserve email and Remember Me, clear password, and permit correction when no limit applies. Login never automatically resends a registration code.

E.2 — Observable login limit

- Permit at most five credential evaluations per normalized email and 30 per client IP in a rolling 15-minute window. Both successful and unsuccessful evaluations count; success does not reset the window. Malformed requests and ALREADY_AUTHENTICATED responses do not consume an evaluation.
- When either budget is exhausted, reject the next evaluation with 429 RATE_LIMITED. Return the positive whole seconds until both budgets permit another evaluation; denied requests do not extend the wait.
- Apply the same rule to existing and unknown emails. The account is not permanently locked, and existing sessions remain valid. The frontend shows the wait and does not automatically resubmit credentials after it expires.

E.3 — Network failure or unknown login outcome

- A lost/malformed POST response may follow successful session creation. Clear the password and read the session endpoint once instead of automatically repeating POST.
- GET 200 establishes the currently authenticated account, which must be visibly identified; it does not prove that a different submitted account authenticated in a competing-tab scenario. Route according to the returned account, not stale form values.
- GET 401 means the browser has no usable session. Show `Sign-in could not be confirmed. Please sign in again.` and allow a deliberate attempt after password re-entry. Do not claim that no server session was ever created.
- A failed session read keeps authentication unresolved. Show `We could not check your session. Please try again.` with Check session again. Do not expose protected content or automatically post the password again.

E.4 — Session expired or account eligibility changed

- A missing, invalid, expired, ended, or no-longer-eligible session returns 401 UNAUTHENTICATED. Protected pages clear private frontend state and return to `/sign-in` with `Please sign in to continue.`
- A service failure is not evidence of logout. Show recovery for the session check rather than converting 503 into an unauthenticated result.
- If the session changes while a request is in flight, discard obsolete private responses before rendering a different account.

UI Integration:

- Source: `02 Login`, node `222:2528`, in page Student.
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech-Platform-for-online-learning--Community-?node-id=222-2528
- Live design context and screenshot inspected on 2026-09-20. Visible controls are Login heading, Email, Password with visibility toggle, Remember Me, Forgot Password, Login button, Google/Apple/Facebook icons, and Sign Up link.
- Preserve the yellow illustration panel, white form panel, rounded inputs/button, spacing hierarchy, and Inter typography. Remember Me is not a terms-acceptance checkbox; do not reuse a misleading layer name as its semantic label.
- Labels, keyboard submission, password visibility state, pending indicator, inline errors, and cooldown feedback must remain understandable. Changing password visibility does not alter its value.
- Error/loading states, deferred-feature explanations, integration shells, and narrow-screen behavior are project supplements. On narrow screens prioritize the form and hide the decorative panel, consistent with UC-01. No mobile frame or frozen Figma dataset is claimed.

API Endpoint:

- `POST /api/v1/auth/login`
- `GET /api/v1/auth/session`

Request Body:

POST login accepts exactly:

```json
{
  "email": "alex@example.com",
  "password": "ExamplePass123!",
  "rememberMe": false
}
```

- All three keys required. email must be a string with a valid email format and at most 254 characters after trimming/lowercasing. Retain dots and plus-address suffixes, exactly as UC-01.
- password must be a string of 8–128 Unicode code points, used exactly as entered with no trimming/normalization. Registration and login must not disagree about accepted password characters.
- rememberMe must be a JSON boolean, not a string or number. No client role, account ID, onboarding state, expiry, or session credential is accepted.
- Reject extra body fields and any API query parameters with VALIDATION_ERROR. GET session accepts no body/query parameters; its browser cookie identifies the session.

Successful Response:

POST login, HTTP 200:

```json
{
  "success": true,
  "message": "Signed in successfully.",
  "data": {
    "user": {
      "id": "2b527c49-db38-45c3-87bc-dc901ff36782",
      "fullName": "Alex Nguyen",
      "email": "alex@example.com",
      "role": "STUDENT",
      "status": "ACTIVE",
      "emailVerified": true,
      "onboardingStatus": "NOT_STARTED"
    },
    "session": {
      "expiresAt": "2026-09-20T18:00:00.000Z",
      "rememberMe": false
    }
  }
}
```

GET session, HTTP 200:

```json
{
  "success": true,
  "message": "Session retrieved.",
  "data": {
    "user": {
      "id": "2b527c49-db38-45c3-87bc-dc901ff36782",
      "fullName": "Alex Nguyen",
      "email": "alex@example.com",
      "role": "STUDENT",
      "status": "ACTIVE",
      "emailVerified": true,
      "onboardingStatus": "NOT_STARTED"
    },
    "session": {
      "expiresAt": "2026-09-20T18:00:00.000Z",
      "rememberMe": false
    }
  }
}
```

- All fields shown are required. user.id is a UUID; fullName and email are the persisted UC-01 values. Successful responses require role=STUDENT, status=ACTIVE, emailVerified=true.
- onboardingStatus is NOT_STARTED, IN_PROGRESS, or COMPLETED. UC-01 initializes NOT_STARTED; this UC only reads the field. A later onboarding UC owns valid transitions. This extension of the read contract does not alter UC-01's registration result.
- expiresAt is server ISO 8601 UTC. The example assumes creation at 10:00 UTC and rememberMe=false. When true at that same creation time, expiry is 2026-10-20T10:00:00.000Z. GET returns the original absolute expiry, not a renewed one.
- GET reads current account eligibility/profile/onboarding state, not a cached registration receipt. No password, token, session ID, or verification code appears in either JSON response.
- Browser sessions use cookie-based transport as a project-level decision. This UC specifies observable lifetime and authentication behavior, not cookie flags or cryptographic/storage implementation recipes.

Error Response:

```json
{
  "success": false,
  "statusCode": 401,
  "code": "INVALID_CREDENTIALS",
  "message": "Email or password is incorrect.",
  "timestamp": "2026-09-20T10:00:00.000Z",
  "path": "/api/v1/auth/login"
}
```

```json
{
  "success": false,
  "statusCode": 429,
  "code": "RATE_LIMITED",
  "message": "Too many requests. Please try again later.",
  "timestamp": "2026-09-20T10:00:00.000Z",
  "path": "/api/v1/auth/login",
  "retryAfterSeconds": 120
}
```

Match UC-01's shared envelope: success=false, statusCode matching HTTP status, code, message, server ISO UTC timestamp, and actual pathname without query. Omit data. Only VALIDATION_ERROR may add errors, mapping field names to nonempty arrays of strings. Every 429 includes positive integer retryAfterSeconds and a matching Retry-After header; 120 is illustrative.

| Endpoint | HTTP | Code | Exact message |
| --- | --- | --- | --- |
| Both | 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| Login | 401 | INVALID_CREDENTIALS | Email or password is incorrect. |
| Login | 409 | ALREADY_AUTHENTICATED | You are already signed in. |
| Login | 429 | RATE_LIMITED | Too many requests. Please try again later. |
| Login | 503 | LOGIN_UNAVAILABLE | Sign-in is temporarily unavailable. Please try again later. |
| Session | 401 | UNAUTHENTICATED | You must sign in to continue. |
| Session | 503 | SESSION_UNAVAILABLE | Session information is temporarily unavailable. Please try again later. |
| Both | 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

## Project-Specific Implementation Context

### Backend Implementation Context

Implement login and session read in NestJS/TypeScript using UC-01's account identity and credential storage. Validate the request before account-session decisions; a valid supported current session yields ALREADY_AUTHENTICATED before credential evaluation. An expired/ineligible current session does not prevent a new eligible login.

Enforce the declared rolling-window budgets and cookie-based session lifetime. Distinct independent browser sessions may coexist; login does not revoke every device. Session reads re-evaluate account eligibility and expose only the declared summary. Login never changes role, verifies an email, enrolls a learner, or completes onboarding. Instructor provisioning, role-specific eligibility, and Instructor routes must be defined together in that later extension before Instructor login is enabled.

### Frontend UI Context

Implement SignInPage in React/TypeScript/Tailwind from node 222:2528. Reuse UC-01's form feedback conventions and enable its Login links. Include the two minimal protected integration shells in this UC's deliverable so the login flow has an implemented endpoint in the browser. Keep unimplemented recovery/social actions explanatory and disabled.

### Frontend Logic and API Context

Check the session on sign-in entry and protected-route entry. Send credentials with the project browser-cookie integration; do not create a separate JSON-token authentication path. Reconcile the session after successful or ambiguous login, clear password state, and route from current server-provided role/onboarding data. Do not replay login automatically after a timeout or limit expiry.

Discard obsolete account data on authentication change. A successful POST followed by an unavailable session read remains in the checking state; no protected shell is shown until the current browser session is confirmed. All shell routes support refresh, with no loop between incomplete and completed onboarding states.

### Validation and Error-Handling Context

Keep email normalization and password validation identical to UC-01. Return a generic credentials error for ineligible accounts and distinguish it from input validation, limits, and service failure. Remember Me changes only the declared session lifetime/persistence behavior. Error messages must not imply successful registration, email delivery, onboarding, or Instructor access. No functional test protocol or additional security implementation requirements are included in this UC.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
