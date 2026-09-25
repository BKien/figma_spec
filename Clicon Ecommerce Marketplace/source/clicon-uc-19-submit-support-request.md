# UC-19: Submit a Support Request

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Submit a Support Request

Description:

- Lets a visitor submit an email address, subject, and optional message through the FAQ support form and receive a durable request reference.
- Successful submission means stored for the research experiment, not delivered email, assigned support staff, live chat, or guaranteed response time. No agent-response/admin interface is added.
- Contracts, retry behavior, limits, and persistence below are project decisions; the form controls are supported by Figma.

Primary Actor:

Visitor or signed-in Customer.

Preconditions:

UC-18 provides `/faqs` and its support anchor. Request storage is available. No login or email-verification flow is required.

Postconditions:

- Success: One request with the submitted normalized fields and status RECEIVED is persisted for the submission identifier; a reference is displayed.
- Failure: A definite rejection stores no request. Unknown response outcomes are retried only with the same submission identifier and unchanged body.
- No email or other external message is sent by this UC.

Main Flow:

1. The visitor opens `/faqs#support`, directly or from Customer Support's Contact Us action.
2. They enter Email address and Subject, optionally Message, then select SEND MESSAGE.
3. The frontend validates fields, assigns a client submission UUID, and submits the request once.
4. The backend stores the request and returns HTTP 201 with its reference and RECEIVED status.
5. The frontend displays `Your support request has been recorded.` plus reference, clears the submitted fields, and permits starting a new request.

Alternative Flow:

A.1 — Optional message

- An empty/whitespace-only message becomes null. A subject is still required; there is no invented mandatory name or order ID field.

A.2 — Duplicate or uncertain submission

- submissionId is unique in this request store. Repeating it with the same normalized email/subject/message returns HTTP 200 with the original reference; different content returns 409 SUBMISSION_CONFLICT and never replaces the first request.
- On a lost response, retain the exact body and ID in the active form, show `We could not confirm receipt. Retry this submission to check.`, and disable editing until the visitor retries or explicitly starts a different request. Explain that starting another request may create a duplicate if the first succeeded.
- Do not auto-retry. A full reload discards this local form state; do not claim the prior request failed. There is no public lookup by email/reference.

A.3 — Observable submission limit

- At most three new requests per normalized email and ten per client IP in the preceding hour. Duplicates with a recognized identical submissionId return the saved result without consuming another new-request allowance.
- A rejected limit request does not extend its wait. Return 429 and the positive seconds until all applicable budgets allow a new request; no account is locked.

Exception Flow:

E.1 — Invalid inputs or conflict

- Field errors return 400 and preserve inputs. SUBMISSION_CONFLICT preserves the original server record; show a form error without claiming this changed submission was saved.

E.2 — Storage/connection failure

- Definite storage rejection returns 503 SUPPORT_UNAVAILABLE. Transport/malformed-response uncertainty uses the same-ID retry behavior. A 429 displays a wait; never show receipt before a confirmed successful envelope.

UI Integration:

- Source: support form in `21_FAQs`, node `436:8148`; entry Contact Us in `24_Customer Support`, `447:9904`.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=436-8148
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=447-9904
- Live contexts/screenshots inspected on 2026-09-19. Preserve pale-yellow panel, Email address, Subject, Message (Optional), and orange SEND MESSAGE. Confirmation/reference, inline errors, and pending states are supplements.
- Replace filler copy with `Send a question about this project. Your request will be recorded.` No fake phone, email-delivery success, agent avatar, or reply deadline is inferred. No frozen dataset or mobile state is claimed.

API Endpoint:

`POST /api/v1/support/requests`

Request Body:

```json
{
  "submissionId": "0dc7d181-b96e-4d89-8e2c-a8daa162d777",
  "email": "customer@example.com",
  "subject": "Question about my order",
  "message": null
}
```
All four keys required, no query/extra keys. submissionId UUID; email trimmed/lowercased valid format max 254 characters; subject trimmed 3–150 Unicode code points; message null or trimmed 1–2000 code points. Browser login does not automatically replace the supplied contact email.

Successful Response:

```json
{
  "success": true,
  "message": "Your support request has been recorded.",
  "data": {
    "request": {
      "reference": "SUP-00001234",
      "status": "RECEIVED",
      "receivedAt": "2026-09-19T10:00:00.000Z"
    }
  }
}
```
HTTP 201 first receipt or 200 identical replay. reference is a unique nonempty display string; its example format is illustrative. receivedAt is server ISO UTC and remains unchanged on replay. Retain submissionId/result association for the lifetime of the request in the experiment; a later retry cannot create a second request under that ID. Do not echo private request content in the receipt.

Error Response:

Use the shared error envelope: success=false, statusCode matching HTTP status, code, message, server-generated ISO 8601 UTC timestamp, and actual request pathname without query string. Omit data. Optional errors is only for VALIDATION_ERROR and maps input paths to nonempty arrays of strings. All shown success keys are required; examples illustrate contracts rather than fixed data.

```json
{
  "success": false,
  "statusCode": 503,
  "code": "SUPPORT_UNAVAILABLE",
  "message": "Support requests are temporarily unavailable. Please try again later.",
  "timestamp": "2026-09-19T10:00:00.000Z",
  "path": "/api/v1/support/requests"
}
```

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 409 | SUBMISSION_CONFLICT | This submission identifier was already used for different content. |
| 429 | SUPPORT_RATE_LIMITED | Too many support requests. Please try again later. |
| 503 | SUPPORT_UNAVAILABLE | Support requests are temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

429 additionally returns positive integer retryAfterSeconds matching Retry-After. No data property is added to errors.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement durable support-request creation in NestJS with normalized fields, submission identity, reference, and timestamp. Preserve one-result-per-ID under competing requests. Apply the observable new-request limits without prescribing counter/storage algorithms. No email adapter, agent assignment, or account/order mutation is required.

### Frontend UI Context

Enable UC-18's existing form in React/TypeScript/Tailwind. Use accessible labels even when placeholders are visible; distinguish message optionality. Show stored-request reference and independent form feedback without replacing the FAQ accordion.

### Frontend Logic and API Context

Maintain draft, submission ID, pending/uncertain state, feedback, and retry wait. Same-ID retries use the original normalized payload. Allocate a fresh ID only for a deliberate new submission. Disable double-submit and never equate a timeout with failed persistence.

### Validation and Error-Handling Context

Reject malformed fields and extra identity/status inputs. Keep errors local to the form; FAQ content may still function during request-service outage. Confirmation means recorded only. Do not expose a public request-content lookup or simulate a support reply.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
