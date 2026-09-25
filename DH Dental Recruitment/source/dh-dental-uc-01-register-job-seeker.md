# UC-01: Register a Job Seeker Account

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Register a Job Seeker Account

Description:

- Allows a visitor to create a DH Dental Recruitment account for finding dental-sector employment, using the DentiHire-branded Sign Up form.
- Captures first name, last name, email, password, mobile number, optional referral source, and the visitor's declaration that they are at least 18 years old. Selecting Get Started also records agreement to the displayed project terms notice.
- This specification begins the Job Seeker scope. Hiring Professionals registration and account switching require their own defined lifecycle and are not enabled here.
- Form controls and layout are supported by the Figma frame identified below. API contracts, validation, account state, repeat handling, and limits are project requirements for the research implementation; no DH Dental Technical Report or existing backend contract has been supplied.

Primary Actor:

Unauthenticated visitor registering as a Job Seeker.

Preconditions:

- The application provides a reloadable `/sign-up` route and the static `/terms` resource defined in UI Integration.
- The registration service and durable account storage are available. The deployment serves frontend and API under the same application origin.
- This experiment uses first-party email/password accounts. Email/SMS verification, external identity providers, and real recruitment integrations are not dependencies of this UC.

Postconditions:

- Success: Exactly one account exists for the normalized email, with role=JOB_SEEKER, status=ACTIVE, emailVerified=false, mobileVerified=false, and profileCompletionStatus=INCOMPLETE. Persist the supplied identity/contact fields, password credential, and declaration/terms acceptance timestamps.
- Show a confirmed registration result. Registration creates no authenticated session and returns no access/refresh token. Sign-in belongs to UC-02.
- Creating an account does not publish an applicant profile, apply for a job, subscribe to marketing, create an introduction video, or create a completed employment/education record.
- Failure: A rejected request does not create a partial account or overwrite an existing one. A transport failure after submission has an unknown outcome until reconciled; it is not automatically a failed registration.

Main Flow:

1. The visitor opens `/sign-up`. Job Seekers is selected for this experiment.
2. They enter First Name, Last Name, E-Mail Address, Password, and Mobile Number. They may select how they heard about DentiHire.
3. They check `I certify that I am 18 years of age or older.` and can open Terms of use before submitting.
4. Selecting Get Started triggers local validation. If valid, generate registrationRequestId and submit the complete request once. Show a pending state and disable repeated submission.
5. The backend validates the contract, applies the declared registration budget, checks normalized email uniqueness, and creates the account with the server-assigned role and initial state.
6. Account creation, acceptance records, and the successful request receipt become one coherent persisted result.
7. Return HTTP 201 with the account summary. Clear the password and transient registration payload, then replace the form with `Account created. Sign in to continue.`
8. When UC-02 is installed, offer Continue to sign in at `/sign-in`. Do not automatically authenticate or navigate to an unimplemented dashboard.

Alternative Flow:

A.1 — Optional referral source

- The unselected `-- Please Select --` state maps to referralSource=null. It does not block registration.
- The project's finite options are SEARCH_ENGINE, SOCIAL_MEDIA, FRIEND_OR_COLLEAGUE, PROFESSIONAL_ASSOCIATION, and OTHER. Labels are specified in the contract below. Figma shows a collapsed selector; its option values have not been verified from an expanded source state.
- OTHER introduces no additional free-text field in this baseline.

A.2 — Correcting input

- Display field errors beside the relevant controls and focus the first invalid input after submission. Preserve non-password values and selections.
- Local-only validation does not send a request or consume a backend allowance. Clear the password after a definite server rejection; require re-entry before a new submission.
- Correcting a definitively rejected request creates a fresh registrationRequestId on the next submit. It is distinct from retrying an unresolved accepted request.

A.3 — Duplicate action or uncertain result

- A recognized successful registrationRequestId with the exact same accepted payload returns HTTP 200 and the original registration receipt for 24 hours. It does not create another account, change a password, or establish a session.
- A reused successful request ID with different content returns REQUEST_CONFLICT. Bind identity using the normalized fields; compare the password exactly as entered.
- While an outcome is uncertain, retain the frozen submitted payload only in the current page's memory for a deliberate same-ID retry. Do not retry automatically, generate a new ID, or allow a competing submit before resolving or abandoning that request.
- Reload/exit clears the password and retry payload. After that, the user may deliberately resubmit their details; uniqueness prevents a second account. An existing-email response alone does not prove which earlier request created the account.
- After the receipt lifetime expires, a request cannot use that receipt to claim success. Normal validation and email uniqueness apply; an existing account is never re-created or modified.

A.4 — Existing account and navigation

- The source's Already have an account? and header Sign In lead to `/sign-in` only after UC-02 supplies that route and behavior.
- In a standalone UC-01 implementation, keep the confirmed result on `/sign-up`, and show those sign-in actions as unavailable with `Sign-in will be available in the next feature.` They become working links when UC-02 is integrated. Do not supply a fake successful login or a 404 destination.
- If an authenticated browser later reaches registration after UC-02 integration, show `You are already signed in.` with navigation to that role's implemented home. POST with a valid authenticated session returns ALREADY_AUTHENTICATED and does not switch accounts.

A.5 — Hiring Professionals choice

- Preserve the visible Hiring Professionals choice but disable it with `Employer registration is not available in this experiment yet.` Job Seekers remains selected.
- The API accepts no role input. Selecting or modifying browser controls cannot create HIRING_MANAGER, EMPLOYER, or ADMIN accounts.

Exception Flow:

E.1 — Invalid input or missing adult declaration

- Return VALIDATION_ERROR for a missing/invalid required field, adultConfirmed other than literal true, termsAccepted other than literal true, or an unsupported request field.
- The checkbox records a self-declaration only; do not infer a date of birth or represent the user as independently age-verified.

E.2 — Email already registered

- Compare normalized email across all account roles and statuses. Return EMAIL_UNAVAILABLE_FOR_REGISTRATION without changing existing account data.
- Concurrent requests for one normalized email can produce at most one account. Recognized same-request repeats return its receipt; a different registration request receives the unavailable-email response.
- Phone numbers are contact attributes, not unique account identifiers in this baseline. A shared phone number does not merge accounts or permit account recovery.

E.3 — Observable registration limit

- Permit at most three new, structurally valid registration attempts per normalized email and ten per client IP in a rolling hour. Successful creation and duplicate-email rejection count; malformed input and ALREADY_AUTHENTICATED do not.
- A recognized successful exact replay does not consume another allowance. A denied request does not extend the wait. The same limits apply to previously unseen emails.
- Return HTTP 429 RATE_LIMITED with positive integer retryAfterSeconds and matching Retry-After. The UI preserves non-password fields, shows the remaining wait, and requires a deliberate later submission.

E.4 — Service or transport failure

- A known failure before commit returns REGISTRATION_UNAVAILABLE or INTERNAL_ERROR and leaves no partial account/acceptance state.
- If response delivery fails after commit, the browser must treat the result as unknown. Use A.3 to recover without announcing another account creation or resetting credentials.
- This UC sends no email or SMS, so registration success never promises inbox delivery or verified contact ownership.

UI Integration:

- Figma file: **DH Dental Recruitment (Community)**, file key `5PvZvQ4E6DepIhbL8D35cV`.
- Page: **Pages / Job Seeker**, node `1:2`.
- Exact source frame: **Sign up**, node `2:2622` — [Open the registration frame](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-2622).
- Live design context and its rendered screenshot were inspected on **2026-09-23**. Evidence covers visible desktop controls, labels, and layout. It does not establish expanded selector options, submission behavior, loading/error states, mobile layouts, or a frozen dataset/version checksum.

| Visible source control | Application mapping |
| --- | --- |
| Job Seekers / Hiring Professionals | Job Seekers selected; Hiring Professionals unavailable in this scope |
| First Name | firstName |
| Last Name | lastName |
| E-Mail Address | email |
| Password | password; one masked input, no additional Confirm Password field |
| Mobile Number | mobileNumber with an explicit international-format hint |
| How did you here about DentiHire? | referralSource; correct the display typo to `How did you hear about DentiHire?` |
| 18-or-older checkbox | adultConfirmed; unchecked initially |
| Get Started | Explicit registration submit |
| Terms of use | Static `/terms` notice; termsAccepted=true is included only on explicit submit while that notice is displayed |
| Already have an account? | UC-02 integration described in A.4 |

- Preserve DentiHire branding, white header, light page background, centered white form card, desktop two-column field arrangement, teal primary action, and dark footer. Source styles include Inter, Gray900 `#111827`, Gray700 `#374151`, and Teal500 `#14B8A6`.
- Add required-field indicators, optional referral label, validation feedback, submission state, registration confirmation, and narrow-screen single-column layout as project supplements. Reading order on narrow screens is first name, last name, email, password, mobile, referral, adult declaration, submit, account/terms links.
- `/terms` is a supplementary static experiment notice, version `research-v1`, with title `Research prototype terms` and the text: `This application is a research prototype for evaluating AI-generated software. Use fictional applicant and contact information. Job listings and application actions are simulated and do not contact real employers.` Show the notice in a separate tab so registration input is not discarded. This is project-authored experiment content, not the original service's legal terms.
- Header/footer links outside UC-01 must use an implemented destination or be visibly unavailable. Footer newsletter subscription is inactive here and must not subscribe the visitor when registering. No additional use case is created for the header, footer, static notice, or success panel.

API Endpoint:

`POST /api/v1/auth/job-seeker-registrations`

Request Body:

```json
{
  "registrationRequestId": "4d99859c-544f-4866-b7c8-34128216d6d0",
  "firstName": "Alex",
  "lastName": "Morgan",
  "email": "alex.morgan@example.com",
  "password": "ResearchDemo42!",
  "mobileNumber": "+12025550123",
  "referralSource": "FRIEND_OR_COLLEAGUE",
  "adultConfirmed": true,
  "termsAccepted": true,
  "termsVersion": "research-v1"
}
```

All keys are required; referralSource is nullable. No query parameters or additional body fields are accepted.

| Field | Contract |
| --- | --- |
| registrationRequestId | UUID created for this submission; not a user ID |
| firstName, lastName | Strings; trim surrounding whitespace; each 1–100 Unicode code points; preserve internal spaces, accents, apostrophes, and hyphens; reject control characters |
| email | String; trim and lowercase for storage/identity; valid `local@domain` email form, at most 254 characters; preserve dots and plus-address suffixes; do not attempt to establish ownership or deliverability from syntax |
| password | String of 8–128 Unicode code points, exactly as entered; do not trim or normalize; no additional uppercase/digit/symbol composition rule |
| mobileNumber | String; trim surrounding whitespace; match `^\+[1-9][0-9]{7,14}$`; no spaces, hyphens, or inferred country code; maximum 15 digits after `+` |
| referralSource | null, SEARCH_ENGINE (`Search engine`), SOCIAL_MEDIA (`Social media`), FRIEND_OR_COLLEAGUE (`Friend or colleague`), PROFESSIONAL_ASSOCIATION (`Professional association`), or OTHER (`Other`) |
| adultConfirmed | Literal boolean true; not a date-of-birth or identity-verification result |
| termsAccepted | Literal boolean true; tied to the explicit Get Started action and visible agreement notice |
| termsVersion | Exact configured notice version `research-v1`; reject another value with VALIDATION_ERROR and require the current notice to be shown before resubmission |

Role, user/account ID, status, verified flags, profile completion, timestamps, notification preferences, and authentication tokens are not registration inputs.

Successful Response:

HTTP **201** for initial creation; HTTP **200** for a recognized successful exact repeat within 24 hours. Both use the same registration-time receipt:

```json
{
  "success": true,
  "message": "Account created. Sign in to continue.",
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
      "createdAt": "2026-09-23T10:00:00.000Z"
    }
  }
}
```

- All shown keys are required. id is a UUID; names/contact values are the persisted normalized values; createdAt is the original server UTC ISO 8601 creation timestamp.
- The role/status/verification/profile fields have the literal initial values shown. The response contains no credential, password, referral attribution, session, or token. Acceptance records are persisted but not returned here.
- A replay receipt reflects registration-time state, not a fresh profile or proof of current login eligibility. Never use a receipt to restore a later disabled account or overwrite subsequently edited fields.
- For this experiment, ACTIVE and contact verification are separate concepts. A future UC-02 may authenticate an ACTIVE JOB_SEEKER with the correct credential even while these flags are false; it must not silently introduce a verification prerequisite without a corresponding verification flow. Contact ownership and professional qualifications are not certified by registration.

Error Response:

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-23T10:00:00.000Z",
  "path": "/api/v1/auth/job-seeker-registrations",
  "errors": {
    "adultConfirmed": [
      "Confirm that you are at least 18 years old."
    ],
    "mobileNumber": [
      "Enter an international phone number starting with + and containing 8 to 15 digits."
    ]
  }
}
```

Use this centralized error envelope throughout DH Dental: success=false, statusCode equal to HTTP status, code, message, UTC timestamp, and actual request pathname without query. Omit data. VALIDATION_ERROR includes errors mapping rejected input fields to nonempty arrays of strings. Other errors omit errors; HTTP 429 adds retryAfterSeconds.

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 409 | EMAIL_UNAVAILABLE_FOR_REGISTRATION | This email is unavailable for registration. Sign in or use another email. |
| 409 | REQUEST_CONFLICT | This request identifier was already used for different content. |
| 409 | ALREADY_AUTHENTICATED | You are already signed in. |
| 429 | RATE_LIMITED | Too many registration attempts. Please try again later. |
| 503 | REGISTRATION_UNAVAILABLE | Registration is temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

Example rate-limit response:

```json
{
  "success": false,
  "statusCode": 429,
  "code": "RATE_LIMITED",
  "message": "Too many registration attempts. Please try again later.",
  "timestamp": "2026-09-23T10:00:00.000Z",
  "path": "/api/v1/auth/job-seeker-registrations",
  "retryAfterSeconds": 900
}
```

retryAfterSeconds is a positive integer matching the Retry-After response header. Its example value is not a fixed lock duration; calculate the remaining time until both declared budgets permit a new attempt.

## Project-Specific Implementation Context

### Backend Implementation Context

Use NestJS and TypeScript for the proposed research backend. Persist a shared Account identity with firstName, lastName, normalized email, mobileNumber, role, status, contact verification flags, profileCompletionStatus, createdAt, and updatedAt. Registration stores its password credential, referralSource, adultDeclaredAt, acceptedTermsVersion, and termsAcceptedAt. Timestamps come from the server. Both firstName and lastName remain separate source fields; derive display name when needed rather than storing a conflicting second identity.

Email uniqueness spans all roles and statuses. Preserve normalized email as the common identity rule for subsequent sign-in, password, and profile UCs. New accounts are private incomplete Job Seeker accounts; creating one must not populate public candidate listings automatically. Empty professional sections remain empty, and source sample percentages or qualifications are not copied into a real account.

Create the account, declaration/terms records, and completion receipt as one durable business outcome. Persist only the minimal information needed for the defined receipt/repeat behavior for 24 hours; do not retain an additional plaintext password in request logs or replay records. Remove expired receipt data within the following hourly cleanup run. Removal does not remove the account or reset the rolling request budget.

The endpoint has no Mailpit, email, SMS, geocoding, or external recruitment dependency. Registration and later session creation are distinct operations. Do not inherit Clicon/EdTech account schemas, OTP flows, or session assumptions merely because they appeared in earlier experiments.

### Frontend UI Context

Use React, TypeScript, and Tailwind CSS for the proposed frontend. Adapt the inspected desktop frame into a responsive form using its field arrangement, Inter typography, teal action, and source branding/assets. Avoid adding fields absent from the design unless identified above as project supplements. Mark the referral selector optional and provide the explicit phone format hint.

Use labels associated with inputs, a masked Password control, an initially unchecked adult declaration, and a readable inline agreement notice. Keep source visual grouping while using the declared single-column reading order on narrow screens. Loading, rejection, unavailable-feature, and success states are supplementary design decisions, not source-verified variants.

### Frontend Logic and API Context

Track editable form state separately from an unresolved submitted payload. Generate one registrationRequestId per new submission; hold the exact payload during uncertainty only for deliberate same-ID retry. Disable duplicate submission while pending. On definitive rejection clear the password and allow correction; on confirmation clear all credential/retry state and render the result. Never persist passwords in browser storage, URLs, or navigation state.

Map success using the shared success/message/data envelope and errors using code plus field paths. Do not treat HTTP 200 receipt replay as a new account creation or an authenticated session. Preserve the confirmed result until UC-02's sign-in destination is available. Terms navigation must work without submitting, resetting, or publishing the applicant's form.

Header, employer, and newsletter controls follow the stated scope. A future UC-02 replaces the explicitly unavailable sign-in actions with working navigation; a later employer UC must define its own provisioning before the second registration choice becomes active.

### Validation and Error-Handling Context

Apply the same identity, length, enum, declaration, and terms-version rules in client feedback and backend validation. The backend remains authoritative for email availability, attempts, timestamps, and initial account state. Local validation does not certify phone/email ownership, professional qualifications, or adulthood beyond the supplied declaration.

Keep invalid input, unavailable identity, request conflict, rate limit, known service failure, and uncertain network outcome distinct. Show actionable feedback without clearing all non-password work. Never replace an existing account's password to make registration succeed, assume an email was sent, or announce sign-in before a separate authentication flow confirms it.
