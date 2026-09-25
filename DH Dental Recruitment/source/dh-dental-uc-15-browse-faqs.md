# UC-15: Browse Frequently Asked Questions

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Browse Frequently Asked Questions

Description:

- Allows visitors and signed-in users to select a help category and expand/collapse questions to read project-accurate answers.
- Figma supplies the four-category navigation and accordion composition. Its sample answer promises real-time email/text notifications that UC-11 does not implement; use the research-specific content defined below instead of reproducing a false capability claim.
- The category/answer dataset, interaction rules, route, and API contract are project decisions. This UC does not introduce search, live support, an interview system, or a content-management interface.

Primary Actor:

Visitor or signed-in user.

Preconditions:

- Implement public `/faqs` and enable FAQ links in the footer and authenticated account menu.
- The exact research FAQ content below is available from the backend. UC-01–14 supply the behavior its answers describe.
- Session availability affects only the shared header. No login, complete profile, or verified contact is required to read FAQ content.

Postconditions:

- Success: The selected category and expanded question show the returned published content in a usable accordion.
- Failure: A distinct load-error state offers Retry; it is not displayed as an empty successful category.
- Category changes and expansion/collapse do not mutate accounts, preferences, notifications, applications, or FAQ records.

Main Flow:

1. Open FAQ from a footer/menu link or `/faqs` directly.
2. Request the complete FAQ dataset and render the categories in response order.
3. Initially select Basic and expand its first question.
4. Select another category to show its questions and expand its first question, if any.
5. Select a question to expand its answer while collapsing the previously expanded question. Selecting the open question collapses it, so zero or one answer may be open.
6. Read the answer or select Contact Us to open UC-16 `/contact`. That navigation does not submit a message.

Alternative Flow:

A.1 — Public and authenticated presentation

- Both audiences use the same FAQ payload and accordion. Use the guest header when no eligible UC-02 session is available and the authenticated header only after confirmation.
- A session-check outage must not block a successful public FAQ read or mislabel it as unauthorized. Do not display stale private account identity while its status is uncertain.

A.2 — Empty category or dataset

- If a configured category has items [], display `No questions available in this category.` with no open accordion item. Empty categories remain selectable.
- If categories [] is returned, display `No FAQs available yet.` The baseline seed below contains four nonempty categories; these empty states support deliberate content removal, not fabricated success after a failed API call.

A.3 — Reload or navigation

- Category and expanded-question state is local to this page visit. Reload initializes from the returned dataset again; no deep-link or persisted selection contract is introduced.
- No extra network request is needed for each question or category because the complete dataset was returned.

Exception Flow:

E.1 — Content unavailable

- On FAQ_UNAVAILABLE, display a retry panel and retain no falsely labeled sample answers. A retry reloads the complete dataset.
- A malformed payload is an unavailable-content state; do not partially render duplicate IDs or unlabeled categories that break accordion selection.

E.2 — Selection no longer exists after refresh

- On deliberate reload, select the first available category, preferring Basic when present, and its first question. If no category/item exists, use the documented empty state.
- Never show an answer from the previously selected category under a different question label.

UI Integration:

- File DH Dental Recruitment (Community), Pages / Job Seeker (`1:2`).
- [Public FAQ, frame `2:2677`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-2677) and [signed-in FAQ, frame `2:5503`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-5503): teal category sidebar, Frequently asked questions heading, question dividers, expansion indicators, and first open answer.
- Both contexts/screenshots inspected on 2026-09-23. Source layout and category labels are evidenced; the remaining answers, category contents, empty/error states, and responsive interactions are research supplements, not a frozen dataset.
- Preserve Basic, Profile & Preferences, Job Posts & Preferences, and Interviews. Redistribute the research questions as specified below rather than treating all source sample rows as Basic-only business requirements.
- Avoid the source's unrelated Introduction Video active underline on the authenticated FAQ page. On narrow screens place category navigation above the accordion without horizontal clipping.
- Use real buttons with category selection and expanded/collapsed semantics. Associate each answer with its question, keep keyboard focus on the selected question, and render answers as plain text.
- Contact Us is a supplementary working link to UC-16. Other footer actions follow their existing implemented/unavailable status; FAQ text must not promise unimplemented email, billing, employer, or interview workflows.

API Endpoint:

- `GET /api/v1/faqs`

Public, with no body or query parameters. No category filter, pagination, question write, search, or authenticated variant endpoint is introduced.

Request Body:

None. Reject a supplied body or any query parameter with VALIDATION_ERROR. Selection and accordion expansion are frontend state and are not submitted to the API.

Successful Response:

HTTP 200. The following is the canonical seed content for this research release, authored for this specification rather than quoted from Figma's sample prose:

```json
{
  "success": true,
  "message": "FAQs loaded.",
  "data": {
    "contentVersion": "dh-faq-v1",
    "categories": [
      {
        "id": "basic",
        "label": "Basic",
        "items": [
          {
            "id": "about",
            "question": "What is this DentiHire research prototype?",
            "answer": "It lets job seekers maintain a profile, browse dental vacancies, and view recommendations based on saved preferences. It is a research implementation, not the production DentiHire service."
          },
          {
            "id": "fees",
            "question": "Does this prototype charge a registration fee?",
            "answer": "No billing or payment feature is implemented. Registering a research account does not create a payment obligation in this prototype."
          },
          {
            "id": "getting-started",
            "question": "How do I start looking for a job?",
            "answer": "Browse the public job list, or register and sign in to maintain your profile. Save a desired position in Basic Information to use Recommendations."
          }
        ]
      },
      {
        "id": "profile-preferences",
        "label": "Profile & Preferences",
        "items": [
          {
            "id": "locations",
            "question": "Can I choose cities where I want to work?",
            "answer": "Yes. Job Preferences lets you select the configured cities, regardless of your current address. No selected city means any location; city preferences influence recommendation order rather than blocking job details."
          },
          {
            "id": "notifications",
            "question": "How do notification preferences work?",
            "answer": "Settings lets you save Email and Text choices for the listed categories. Email and text delivery are not implemented, so saving a choice does not send or schedule a message."
          },
          {
            "id": "closing",
            "question": "Can I recover a closed account?",
            "answer": "No. Account closure is permanent. A new registration is a new account and does not restore old profile content. Review the closure screen for deletion timing and the separate retention of Contact Us submissions."
          }
        ]
      },
      {
        "id": "jobs-preferences",
        "label": "Job Posts & Preferences",
        "items": [
          {
            "id": "recommendations",
            "question": "How are recommended jobs selected?",
            "answer": "Visible jobs must match your saved desired position. They are ordered by the number of active preferences they match, then publication time and job ID. Partial matches may appear; the result is not a qualification assessment."
          },
          {
            "id": "licensing",
            "question": "Does the prototype verify where I am licensed to work?",
            "answer": "No. It does not verify licenses, state eligibility, or self-declared qualifications. A listed or recommended job is not confirmation that you meet its professional requirements."
          }
        ]
      },
      {
        "id": "interviews",
        "label": "Interviews",
        "items": [
          {
            "id": "interview-scheduling",
            "question": "Can I schedule an interview here?",
            "answer": "Interview scheduling is not implemented in this research release. Saving an introduction video does not arrange an interview or send the video to an employer."
          }
        ]
      }
    ]
  }
}
```

data has exactly contentVersion and categories. contentVersion is a nonempty revision label for the FAQ content, not a Figma version/checksum. Each category has exactly id, label, and items; each item has exactly id, question, and answer. All these text values are nonempty plain strings; IDs are unique across their respective category/question collections, including across categories for questions.

Array order is display order. The initial research fixture must use the exact IDs, labels, questions, answers, and order above. No HTML, inferred URLs, source marketing claims, or secret account-specific content is inserted into answers. Content updates must change contentVersion and remain consistent with the actual implemented UC behavior; no editing API is in scope.

A successful empty dataset retains contentVersion with categories []. A category may retain its id/label with items []. No 404 is used for an intentionally empty catalog.

Error Response:

JSON errors have exactly success false, statusCode, code, message, timestamp (server UTC ISO 8601), and path (actual pathname without query). VALIDATION_ERROR additionally has errors, mapping field paths to nonempty arrays of messages. Only a documented 429 adds a positive integer retryAfterSeconds and the equal Retry-After header. Other errors omit these extensions. Do not add data: null.

| HTTP | code | message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 503 | FAQ_UNAVAILABLE | FAQs are temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

No session-related 401/403 or endpoint-specific attempt limit applies to this public content read.

```json
{
  "success": false,
  "statusCode": 503,
  "code": "FAQ_UNAVAILABLE",
  "message": "FAQs are temporarily unavailable. Please try again later.",
  "timestamp": "2026-09-23T17:00:00.000Z",
  "path": "/api/v1/faqs"
}
```

## Project-Specific Implementation Context

### Backend Implementation Context

Use the proposed NestJS/TypeScript backend to serve one public FAQ dataset. A versioned application content fixture is sufficient; no database editor, external CMS, search index, or translation service is required.

Return categories/items in the declared order and enforce unique IDs and nonempty labels/questions/answers when loading the configured dataset. Never substitute an empty successful catalog for a missing/corrupt content source. Intentional empty arrays remain valid when explicitly configured.

No account lookup is necessary to produce the FAQ payload. Cookies or an expired session must not gate the public endpoint. The content version describes this FAQ fixture only; it does not certify a frozen design dataset or an external production policy.

### Frontend UI Context

Implement the source composition in React/TypeScript/Tailwind using the existing public/authenticated shell. Reuse one category/accordion component for both audiences. Keep the first open question styling, teal sidebar, and clear question/answer hierarchy.

Show category selection distinctly, allow all questions to be collapsed, and keep exactly one open at most. Use semantic buttons and an expanded state that corresponds to the actual visible answer. Do not render an expansion icon as a nonfunctional image-only action.

Display the declared answers as plain text without generated embellishments. These answers explain the prototype's capabilities rather than directing a user to nonexistent UI features.

### Frontend Logic and API Context

GET the dataset once per page load and keep category/question selection local. Select Basic if returned, otherwise the first category, then its first item. On category change reset expansion to that category's first item; on clicking an open item set the expanded ID to null.

A user action that only expands a question must not call a mutation API, update notifications, or require a login. Public content can render independently of the optional header session request.

On refresh replace the full dataset and reset selection according to the declared rules; ignore responses from an abandoned page load. Wire `/faqs` and `/contact` links to actual routes. Do not add FAQ-category parameters to UC-02's next allowlist because this public page needs no sign-in redirect.

### Validation and Error-Handling Context

Reject unsupported request input at the API boundary. Distinguish HTTP/load failure, malformed content, deliberate empty categories, and an all-collapsed accordion. None is evidence that an account is closed or unauthenticated.

Ensure no question answer from one category remains visible under another category's heading. Stable IDs govern selection, not question text or array indices alone. Server/renderer must preserve the exact response envelope and ordered fixture values.

Maintain factual alignment: notification choices do not send messages, recommendations are deterministic rather than qualification verification, and introduction-video saving does not schedule interviews. Do not copy source promises that contradict the implemented research scope.
