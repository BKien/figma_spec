# UC-02: Sign In

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Sign In

Description:

- Allows a customer with an active, email-verified account to sign in using email and password and access their account area.
- Includes establishing a browser session and reading the current session. Account registration, password recovery, social-provider authentication, logout, and full Dashboard features are separate use cases.

Primary Actor:

Customer.

Preconditions:

- The customer has completed UC-01 or has an equivalent active, verified account.
- The shared account contract and response envelope in `PROJECT_CONTEXT.md` apply to this use case.
- The application exposes `/sign-in` and the account integration shell `/account/dashboard` defined below.

Postconditions:

- Success: The customer has an authenticated browser session valid for eight hours from creation. The frontend confirms that session and displays the account integration shell.
- Failure: Invalid credentials do not create a session or navigate to the account area. When a response is lost, the outcome remains uncertain until the current session is checked.
- Signing in does not create an account, activate a pending registration, or send a verification email.

Main Flow:

1. The customer opens `/sign-in`. The frontend checks the current session; an existing valid session follows A.1.
2. The system displays Email Address, Password, the password visibility control, Forget Password, and SIGN IN, with the Sign In tab active.
3. The customer enters their email and password and selects SIGN IN.
4. The frontend validates the form and submits `POST /api/v1/auth/login`.
5. The backend applies the sign-in limit and validates the request using the shared account contract.
6. The backend checks the credentials. Only a user whose status is `ACTIVE` and whose `emailVerifiedAt` is non-null can sign in.
7. The backend establishes an eight-hour browser session and returns HTTP 200 using the project success envelope. No authentication token is returned in JSON.
8. The frontend clears the password and calls `GET /api/v1/auth/session` to confirm the browser session.
9. On successful confirmation, the frontend reads `data.user` and `data.session`, updates authentication state, and navigates to `/account/dashboard`.
10. The account integration shell displays the customer's full name and email. It does not request Dashboard statistics or order data.

Alternative Flow:

A.1 — Existing session

- A successful session check at page entry navigates directly to `/account/dashboard`; no credential submission is required.

A.2 — Show or hide password

- The eye control changes the password's visual visibility without changing its value or submitting the form.

A.3 — Create an account

- Sign Up navigates to `/sign-up` and UC-01.

A.4 — Recover a password

- Forget Password navigates to `/forgot-password`. The full recovery flow belongs to a separate UC.
- Until that UC is integrated, this route renders the navigation shell defined in `PROJECT_CONTEXT.md`, with a return-to-sign-in link. It does not claim to send email or recover an account.

Exception Flow:

E.1 — Invalid form data

- Client validation displays field feedback and prevents submission. Server validation independently returns HTTP 400 `VALIDATION_ERROR` with the project error envelope.

E.2 — Invalid credentials or ineligible account

- Unknown email, wrong password, pending-only registration, inactive user, and unverified user all return HTTP 401 `INVALID_CREDENTIALS` with `Email or password is incorrect.`
- Stay on Sign In, retain email, clear password, and allow correction subject to the sign-in limit.

E.3 — Sign-in limit reached

- Return HTTP 429 `RATE_LIMIT_EXCEEDED` with a positive integer `retryAfterSeconds` and matching `Retry-After` header.
- Preserve email, clear password, and disable SIGN IN for that delay. The customer can submit manually afterward; the server decides whether another attempt is allowed.

E.4 — Missing or expired session

- The session endpoint returns HTTP 401 `UNAUTHENTICATED`. At initial Sign In entry, this simply displays the form.
- At the account shell, clear the displayed account data and navigate to Sign In. A session check does not extend the original eight-hour expiry.

E.5 — Network or service failure

- End the loading state and display the relevant error. A service outage is not reported as an incorrect password.
- If the login response is lost, check the session once. A successful check permits navigation; a 401 permits manual sign-in. If the check also fails, remain on the current screen with a retry action. Do not automatically repeat the login POST.

E.6 — Session could not be retained

- If login returned success but its immediate session check returns 401, stay on Sign In and display `Unable to keep you signed in. Please allow cookies and try again.`

UI Integration:

- Sign In: `16_Sign In`, node `429:7940`.
- Figma reference: https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=429-7940&m=dev&t=dzmB5Gsx6BiSx55z-1
- Evidence: supplied screenshot `d04223f1-a070-4620-9981-db6c20e3a3c6.png`; confirms the visible desktop structure and labels. Live frame metadata, responsive variants, font/color tokens, and error/loading variants have not been captured as a frozen dataset. Source generation awaits the dataset release recorded outside this UC in the researcher notes.

| Visible control | Mapping |
| --- | --- |
| Sign In / Sign Up tabs | Active Sign In; Sign Up links to `/sign-up` |
| Email Address | `email` |
| Password and eye icon | `password` and visibility toggle |
| Forget Password | `/forgot-password` |
| SIGN IN | Submit login |
| Login with Google / Login with Apple | Visible but disabled; provider login is outside this UC |

- Preserve the Clicon header/footer, breadcrumb, centered form card, orange primary action, divider, and control order. No Remember me checkbox is present; do not introduce one.
- Loading, validation feedback, and error messages are functional UI states to be specified in the frozen experiment inputs; the supplied screenshot does not verify their appearance.
- Account integration shell at `/account/dashboard`: reuse the Clicon shell; display heading `My Account`, text `Signed in as`, and the current `fullName` and `email`. Include `Back to home` linking to `/`. No statistics, order lists, charts, or additional business actions are included.
- This shell must be implemented and route-registered as part of UC-02 source generation, including direct navigation/reload support. Before displaying account information, resolve the current session; show loading, redirect on 401, or display a retry action on unavailability.
- The shell is an explicit project integration requirement, not a Figma-derived Dashboard feature and not an additional counted use case. No source code or deployed route is claimed by this specification alone.

API Endpoint:

| Operation | Endpoint |
| --- | --- |
| Sign in | `POST /api/v1/auth/login` |
| Read current session | `GET /api/v1/auth/session` |

Request Body:

Login uses `Content-Type: application/json` and the following required fields:

```json
{
  "email": "student@example.com",
  "password": "ExamplePass123!"
}
```

- Email: trim surrounding whitespace; lowercase for identity comparison; valid email format; at most 254 characters.
- Password: at least 8 Unicode code points and at most 72 UTF-8 bytes, matching the current UC-01 compatibility contract; preserve the value exactly.
- Additional request properties are invalid. No `rememberMe` field is defined.
- The session endpoint has no body and uses the browser session. Session transport follows the project's cookie-based integration contract; cryptographic and cookie-policy implementation choices are outside this UC.

Successful Response:

Use `PROJECT_CONTEXT.md` envelope `success`, `message`, `data` for both endpoints.

Login — HTTP 200:

```json
{
  "success": true,
  "message": "Signed in successfully.",
  "data": {
    "user": {
      "id": "ab40a099-e81b-4cb3-8ae3-9601cb4c258f",
      "fullName": "Nguyen Van A",
      "email": "student@example.com",
      "status": "ACTIVE",
      "emailVerified": true
    },
    "session": {
      "expiresAt": "2026-09-17T18:00:00.000Z"
    }
  }
}
```

Current session — HTTP 200:

```json
{
  "success": true,
  "message": "Current session retrieved.",
  "data": {
    "user": {
      "id": "ab40a099-e81b-4cb3-8ae3-9601cb4c258f",
      "fullName": "Nguyen Van A",
      "email": "student@example.com",
      "status": "ACTIVE",
      "emailVerified": true
    },
    "session": {
      "expiresAt": "2026-09-17T18:00:00.000Z"
    }
  }
}
```

- Timestamps and IDs are illustrative. `expiresAt` is an ISO 8601 UTC timestamp, eight hours after session creation. Reading the session does not renew it.
- Responses contain no authentication token or password. Browser session establishment occurs outside the JSON body.

Error Response:

Use the centralized error envelope supplied by the researcher and defined in `PROJECT_CONTEXT.md`: `success`, `statusCode`, `code`, `message`, `timestamp`, and `path`. Errors contain no `data` property. `statusCode` matches the HTTP status; `timestamp` is generated by the server in ISO 8601 UTC; `path` is the request pathname, excluding the query string. Session errors use `/api/v1/auth/session`; login errors use `/api/v1/auth/login`. Example timestamps below are illustrative.

```json
{
  "success": false,
  "statusCode": 401,
  "code": "INVALID_CREDENTIALS",
  "message": "Email or password is incorrect.",
  "timestamp": "2026-09-17T10:00:00.000Z",
  "path": "/api/v1/auth/login"
}
```

Validation — HTTP 400:

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-17T10:00:00.000Z",
  "path": "/api/v1/auth/login",
  "errors": {
    "email": [
      "Enter a valid email address."
    ]
  }
}
```

Throttling — HTTP 429, example header `Retry-After: 60`:

```json
{
  "success": false,
  "statusCode": 429,
  "code": "RATE_LIMIT_EXCEEDED",
  "message": "Too many sign-in attempts. Please try again later.",
  "timestamp": "2026-09-17T10:00:00.000Z",
  "path": "/api/v1/auth/login",
  "retryAfterSeconds": 60
}
```

| HTTP | Endpoint | Code | Exact message |
| --- | --- | --- | --- |
| 400 | Login | `VALIDATION_ERROR` | `Please correct the highlighted fields.` |
| 401 | Login | `INVALID_CREDENTIALS` | `Email or password is incorrect.` |
| 401 | Session | `UNAUTHENTICATED` | `Please sign in to continue.` |
| 415 | Login | `UNSUPPORTED_MEDIA_TYPE` | `Use application/json for this request.` |
| 429 | Login | `RATE_LIMIT_EXCEEDED` | `Too many sign-in attempts. Please try again later.` |
| 503 | Both | `AUTH_SERVICE_UNAVAILABLE` | `Sign-in is temporarily unavailable. Please try again later.` |
| 500 | Both | `INTERNAL_ERROR` | `Unable to complete your request. Please try again later.` |

## Project-Specific Implementation Context

### Backend Implementation Context

Implement login and session-reading endpoints in NestJS using the shared account contract and centralized response format in `PROJECT_CONTEXT.md`.

- Reuse the account established by UC-01. Do not create a second user model with different email, password, status, or verification semantics.
- Only active, verified users with correct credentials can establish a session. Pending registration is not an authenticated account.
- Return the same documented credential error for every ineligible identity or credential combination.
- Provide a sign-in limit whose externally observable policy is fixed in `PROJECT_CONTEXT.md`; return the documented wait when it is reached. Do not change a user's account status because of throttling.
- Establish an eight-hour session and expose the current customer and expiry through the session endpoint. A session read does not create or extend a session.
- Use the documented success and error envelopes consistently; return service failures distinctly from incorrect credentials.
- These requirements specify behavior and integration. No password-comparison technique, session-token algorithm, rate-limit data structure, cookie flags, or storage-retention implementation is prescribed here.

### Frontend UI Context

Implement `SignInPage` and `SignInForm` at `/sign-in` in React, TypeScript, and Tailwind CSS, using the supplied screenshot and released design inputs.

- Reuse Clicon's shared shell and match the UI Integration mapping.
- Preserve password visibility, Sign Up navigation, and Forget Password navigation. Do not make disabled social controls report successful login.
- Associate labels with inputs and provide keyboard submission and visible field feedback.
- Implement and register the account integration shell described above. Do not redirect to an unimplemented route or substitute an invented full Dashboard.
- Register the temporary recovery navigation shell if the independent recovery UC is not integrated yet.

### Frontend Logic and API Context

Connect the form to the two API endpoints and parse the shared envelope.

- Form state includes email, password, password visibility, loading, field errors, general error, and the retry deadline. Authentication state includes the current customer and session expiry.
- On entry, read the session. HTTP 200 uses `data.user` and `data.session` and follows A.1; 401 displays the sign-in form normally; unavailability displays a retry option.
- Submit the exact login body once. After success, clear password, confirm the session, and navigate to the account shell using the confirmed user data.
- Send browser session credentials with session-dependent requests. Do not expect a token in `data` or at the response root.
- Read field errors from `errors`, general feedback from `message`, and the throttling delay from `retryAfterSeconds` according to the shared error contract.
- For an uncertain login result, perform E.5 rather than automatically repeating the POST.
- Resolve the session when entering the account shell directly or reloading it. Definitive 401 clears account display and returns to Sign In; temporary unavailability permits retry.
- Clear obsolete UC-01 pending-registration UI state after successful session confirmation.

### Validation and Error-Handling Context

- Validate email/password against the shared compatibility rules and keep field names consistent between form, request, and validation errors.
- Display invalid-credential and service errors at form level. Preserve email and clear password after a failed login submission.
- Disable duplicate submission while login or its confirmation is in progress. Keep SIGN IN disabled during a returned throttle delay; allow manual retry when it ends.
- Render session loading before account data; display retry feedback when the session service is unavailable.
- For a network error without a response, use `Unable to connect. Please check your connection and try again.`
- For unexpected or malformed response bodies, use `Unable to complete your request. Please try again later.` and do not treat the result as successful authentication.
- Handle a successful login followed by a 401 session check using E.6, without a navigation loop.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
