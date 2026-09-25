# UC-16: Submit a Contact Message

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Submit a Contact Message

Description:

- Allows a visitor or signed-in user to submit their contact details, subject, and message into the research prototype's contact intake store and receive a confirmation receipt.
- Figma supplies the contact form and the 500-character message limit. Validation, receipt/idempotency behavior, request limits, retention, routes, and API contract are declared project decisions.
- This UC records a submission; it does not send email/SMS, create a live support conversation, or guarantee a human response. The interface states that scope before submission and confirms recording rather than claiming delivery.

Primary Actor:

Visitor or signed-in user requesting information through Contact Us.

Preconditions:

- Public `/contact` exists and is reachable from footer, FAQ, and the authenticated account menu.
- The backend has durable contact-intake persistence. No email/SMS provider, verified account, employer workflow, or helpdesk integration is required.
- The contact page explains that this is a research form and that its submissions remain for 30 days, independently of account closure.

Postconditions:

- Success: One normalized message is durably recorded with a receipt ID and receivedAt; the UI displays that receipt and clears the submitted draft.
- Replay: Retrying an identical request ID and normalized payload within retention returns its original receipt without another message.
- Failure: Invalid, conflicting, or over-limit submissions do not create a new message. Ambiguous network failure preserves the request ID and draft for deliberate retry.
- No account contact fields, profile, job preferences, notification preferences, or contact-verification flags change. No outbound message or support response is implied.

Main Flow:

1. Open Contact Us and review the research-intake and retention notice.
2. Enter first/last names, email, optional phone, subject, and a message of at most 500 Unicode code points.
3. Select Submit. Validate fields, generate one submissionRequestId for this draft, and send the request once.
4. The backend normalizes/validates the payload, resolves a possible replay, applies the new-submission budget, and stores the message and receipt together.
5. On confirmed success, display `Message recorded.` with the receipt ID and receivedAt. Explain that no email or text message was sent.
6. Clear the submitted draft and request ID. Send another message starts a new blank draft and new request ID.

Alternative Flow:

A.1 — Signed-in prefill

- If UC-02 confirms a session, prefill firstName, lastName, email, and mobileNumber as phone only when the form is still pristine. All contact-form fields remain editable and are independent of Account data.
- Failure/absence of session does not prevent public submission. Do not overwrite user edits when a delayed session response arrives.
- Store no account ID on the public contact record. Account closure does not delete these independently submitted messages, as disclosed in UC-14 and this form.

A.2 — Optional phone or cancellation

- An omitted phone in the UI is submitted as phone null. Choosing not to provide it does not change eligibility or the successful response.
- Leaving before submission saves nothing. There is no autosave or automatic submission on field blur. The draft is local to the mounted form; it is not retained across account changes.

A.3 — Retry after lost response

- Preserve the exact submissionRequestId and normalized draft after timeout. Offer Retry same message, which sends the same ID/payload deliberately; no background retry loop occurs.
- An existing matching record returns its original receipt with HTTP 200, even if the new-submission budget is currently exhausted. A different normalized payload for that ID returns SUBMISSION_REQUEST_CONFLICT.
- Once the outcome is unknown, freeze that draft for retry or let the actor explicitly abandon it. Explain that abandoning does not retract a possibly recorded submission. Editing to send a different message starts a new ID only after that explicit choice; it may create another message.

A.4 — No real support contact configured

- The Figma phone/email/social icons are template content. In this research release do not expose them as live call/mail/social actions.
- Replace them with `Use this research contact form. Messages are recorded for the experiment; no email delivery or response service is connected.` No third party is contacted by reading or submitting this form.

Exception Flow:

E.1 — Invalid fields

- Display inline errors and keep the rest of the draft. Enforce the 500-character message limit consistently in UI and API; do not silently truncate content.
- An invalid email or phone is a format failure, not proof that the contact exists or belongs to the actor.

E.2 — Observable submission limit

- Accept at most three new submissions per normalized email and ten per client IP in a rolling hour. Only newly committed submissions count; validation failures, payload conflicts, service failures without a commit, and matching replays do not consume a new-submission allowance.
- Return RATE_LIMITED with the wait until both budgets permit one more new submission, rounded up to a positive whole second. The user explicitly resubmits after waiting; do not send automatically when a countdown expires.

E.3 — Service failure or receipt uncertainty

- Do not report Message recorded until persistence is confirmed. On a known precommit failure, keep the draft/request ID and show Retry. On an ambiguous result, use A.3.
- No public read-by-email, message listing, or receipt-detail endpoint is introduced. The receipt ID is a confirmation reference, not a link that reveals the submitted message.

E.4 — Reused request ID with different content

- Return SUBMISSION_REQUEST_CONFLICT and create nothing. Retain the user's draft and explain that the identifier belongs to another submission payload; do not silently invent a new ID and resubmit.
- A deliberate new-message action can create a new ID after the actor understands a prior message may already exist.

UI Integration:

- File DH Dental Recruitment (Community), Pages / Job Seeker (`1:2`).
- [Public Contact Us, frame `2:2802`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-2802) and [signed-in Contact Us, frame `2:5410`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-5410): split contact-information panel, first/last name, email, optional phone, subject, message, Max. 500 characters, and Submit.
- Both contexts/screenshots inspected on 2026-09-23. The shared form is evidenced; field validation, persistence, receipt, retry, and responsive states are research supplements, not a frozen dataset.
- Correct inappropriate repeated you@example.com placeholders to match each field. Use actual account values only for confirmed, pristine-form prefill.
- Replace source lorem ipsum and unverified real-world contact destinations with the research-intake copy in A.4. Display `Submissions are retained for 30 days, independently of account closure.` before Submit.
- Add a live remaining-character indicator, sending state, inline errors, and receipt panel. Retain the teal side panel and source form hierarchy. On narrow screens stack the side panel above the form.
- Use the correct guest/authenticated header; do not mark Introduction Video active merely because the source does. Navigation away never simulates a successful submission.

API Endpoint:

- `POST /api/v1/contact-submissions`

Public JSON endpoint with no query parameters. A missing/expired browser session does not block submission. No confirmation email, contact-update endpoint, public submission lookup, administrative inbox, or reply endpoint is in scope.

Request Body:

```json
{
  "submissionRequestId": "f72c34aa-fd03-4d09-a873-853ab873f8c6",
  "firstName": "Alex",
  "lastName": "Morgan",
  "email": "alex.morgan@example.com",
  "phone": null,
  "subject": "Question about job preferences",
  "message": "How can I update the cities used for my job recommendations?"
}
```

All seven fields are required; only phone is nullable. Reject extra keys and unsupported request media type with VALIDATION_ERROR.

| Field | Rule |
| --- | --- |
| submissionRequestId | UUID identifying this logical submission, preserved for a deliberate retry |
| firstName, lastName | Trim surrounding whitespace; each 1–100 Unicode code points; no control characters; preserve internal ordinary spaces, accents, apostrophes, hyphens |
| email | Trim and lowercase; valid email syntax; at most 254 characters; preserve dots and plus suffixes, matching UC-01 normalization |
| phone | null, or trimmed E.164-format string matching ^\+[1-9][0-9]{7,14}$; no automatic country-code guessing |
| subject | Trim; 1–120 Unicode code points; no control characters |
| message | Normalize CRLF/CR to LF, trim outer whitespace, then 1–500 Unicode code points; LF allowed, other control characters rejected |

The normalized payload for replay comparison consists of firstName, lastName, email, phone, subject, and message. Case remains significant in names/subject/message; email uses its canonical lowercase form. The frontend converts an empty optional phone field to null; the API does not silently coerce an empty string to null.

No account ID, recipient address, message status, HTML body, attachment, job ID, or delivery destination may be supplied. Content is stored as text and is not executed or interpreted as instructions to send messages elsewhere.

Successful Response:

```json
{
  "success": true,
  "message": "Message recorded.",
  "data": {
    "submissionId": "60daef40-220a-43b4-8d9c-1b148d9ee260",
    "status": "RECEIVED",
    "receivedAt": "2026-09-23T17:00:00.000Z",
    "deliveryStatus": "NOT_IMPLEMENTED"
  }
}
```

HTTP 201 for a newly committed message; HTTP 200 for an identical replay while its record remains within the 30-day retention period. Both use exactly the same envelope/message and data keys. submissionId is a server-issued UUID, status is always RECEIVED, receivedAt is the original server UTC ISO 8601 timestamp, and deliveryStatus is always NOT_IMPLEMENTED.

A replay returns the original submissionId/receivedAt, not a new timestamp, and creates no second record. Receipt and stored message commit together. No contact fields or message text are echoed in the receipt; no sent/delivered/responded status is invented.

Retain the message, request-ID association, normalized comparison data, and receipt for exactly the active 30-day period beginning at receivedAt. At receivedAt + 30 days, remove them from active storage. Replay guarantees end at that boundary; a later reuse can be treated as a new submission. The client must not offer retries of a locally known request older than 30 days and must disclose that a new message can create a new record.

Error Response:

JSON errors have exactly success false, statusCode, code, message, timestamp (server UTC ISO 8601), and path (actual pathname without query). VALIDATION_ERROR additionally has errors, mapping field paths to nonempty arrays of messages. Only a documented 429 adds a positive integer retryAfterSeconds and the equal Retry-After header. Other errors omit these extensions. Do not add data: null.

| HTTP | code | message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 409 | SUBMISSION_REQUEST_CONFLICT | This submission request was already used with different content. |
| 429 | RATE_LIMITED | Too many contact submissions. Please try again later. |
| 503 | CONTACT_SUBMISSION_UNAVAILABLE | Contact submission is temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

This public endpoint does not return 401/403 because of a missing or expired account session.

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-23T17:00:00.000Z",
  "path": "/api/v1/contact-submissions",
  "errors": {
    "message": [
      "Enter a message of 1 to 500 characters."
    ],
    "phone": [
      "Use an international phone number or leave this field blank."
    ]
  }
}
```

```json
{
  "success": false,
  "statusCode": 429,
  "code": "RATE_LIMITED",
  "message": "Too many contact submissions. Please try again later.",
  "timestamp": "2026-09-23T17:00:00.000Z",
  "path": "/api/v1/contact-submissions",
  "retryAfterSeconds": 600
}
```

The 429 example also sends Retry-After: 600. No data field is added to errors. A timeout with no response remains a client-observed unknown outcome, not a fabricated 503.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement a public contact-intake service in the proposed NestJS/TypeScript backend. Persist submissionId, submissionRequestId, normalized contact/message fields, status RECEIVED, receivedAt, and the retention expiry. No account foreign key or verification claim is attached; a supplied email is a contact value, not account authentication.

For a valid request, resolve an existing request-ID association before counting a new-submission budget. Matching normalized payload returns the original receipt. Mismatch returns 409. Concurrent identical requests must produce one stored message and one new-submission budget consumption; losing retries return its receipt. Only a committed new message consumes the declared allowance.

A new receipt and message must be stored together before returning 201. A storage failure does not produce a success receipt with no corresponding message. Do not call external email/SMS services, a template's phone/email address, or an employer-contact API.

Remove submissions and their replay associations from active storage at the defined 30-day expiry; expiry is an implemented lifecycle rule, not only a displayed notice. Account closure neither extends nor shortens this independent retention. No copy of message/contact content remains in a separate receipt table after expiry.

The research operator can inspect the persisted intake through the chosen project data-management environment; this UC does not add an exposed administrative UI or public read API. No response-time or message-delivery guarantee is implied.

### Frontend UI Context

Use React/TypeScript/Tailwind and one reusable form for the two inspected header variants. Keep visible labels, Phone Optional, and the source's 500-character limit. Use plain-language research-intake and retention notices rather than false production contact information.

Count message characters after the declared line-ending normalization and using Unicode code points, matching server length semantics. Show field feedback without clearing valid input. The receipt panel uses Message recorded and the returned reference/time, never Email sent or an invented support agent response.

While pending or outcome-unknown, prevent duplicate submits and preserve the exact draft for an intentional retry. A deliberate abandon/new-message choice explains that it does not withdraw a potentially recorded prior submission.

### Frontend Logic and API Context

Optional session prefill must not delay the public form or overwrite edits. On an observed account transition, clear any account-prefilled local draft rather than reuse it for another actor. Contact submission remains independent of login and does not update the Account.

Create one UUID when beginning a logical submit attempt. Retain it and the normalized payload for retry after an ambiguous result; do not generate a new UUID on every click. Fixing a known validation failure may reuse the ID because no record was created. After a confirmed success, discard the draft/ID before enabling Send another message.

Submit exactly the request schema. A 201 or matching 200 displays the canonical receipt. A 409 requires an explicit decision rather than automatic resubmission under a new ID. A 429 uses its returned delay; no automatic send follows expiry. A transport timeout uses the same-message retry flow.

Keep drafts and receipts local to the mounted page and clear account-specific prefill on identity change. Do not put contact information/message text in the URL, navigation state, or a guessed receipt lookup. Enable `/contact` from UC-15 and existing footer/menu links without requiring UC-02 next-destination changes.

### Validation and Error-Handling Context

Apply the exact field normalization before replay comparison and before length validation where specified. Reject wrong types, unsupported fields, invalid UUID, unknown query parameters, invalid phone/email, empty required strings, and over-limit subject/message. Do not silently truncate or coerce null/booleans into text.

Report field errors under submissionRequestId, firstName, lastName, email, phone, subject, message, or request. Enforce the same 500-code-point rule in frontend and backend, with normalized LF allowed. Contact syntax validation does not establish ownership or delivery availability.

Distinguish newly recorded, replayed, conflicting, rate-limited, precommit-failed, and unknown outcomes. A saved record may survive account closure under its disclosed retention; a lost response must not silently create duplicates. All success messages describe intake persistence only.
