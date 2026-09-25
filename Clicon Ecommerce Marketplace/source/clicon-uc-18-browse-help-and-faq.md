# UC-18: Find Help and Read FAQs

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Find Help and Read Frequently Asked Questions

Description:

- Provides a public help center and searchable FAQ answers with topic navigation and expandable answers. Both screens serve the same self-service help goal.
- Uses the Customer Support and FAQs designs. Support-message submission is UC-19; this UC provides its visible form location and links.
- Help content, topic IDs, routes, search behavior, and API contracts are project decisions. No live chat, phone-service integration, legal policy, refund, or seller workflow is invented from sample labels.

Primary Actor:

Visitor or signed-in Customer.

Preconditions:

- `/help` and `/faqs` are registered public routes.
- Seeded help answers describe only the implemented experimental features accurately. Published answers are available from the help store; no external knowledge service is required.

Postconditions:

- Success: The visitor reads matching published answers or follows a valid implemented destination.
- Failure: A service failure is identified separately from no matching answers. Viewing help changes no order/account or support-request state.

Main Flow:

1. Customer Support opens `/help`; Need Help opens `/faqs`.
2. The help center loads configured topics and popular questions and displays its search field.
3. The visitor submits a keyword or selects a topic/popular question.
4. The frontend opens `/faqs` with the appropriate q/topic/question query and loads the FAQ collection.
5. The visitor expands an answer. At most one answer is expanded; clicking it again collapses it.
6. If no answer resolves the question, the visitor can use UC-19's support form on the same FAQ screen.

Alternative Flow:

A.1 — Direct FAQ and deep link

- `/faqs` without filters lists all published answers in configured order with all collapsed initially. A question query expands that returned answer if present.
- A valid but absent/filtered-out question displays `This answer is not available in the current results.` without discarding other answers. Clear filters explicitly to search again.

A.2 — Search and topics

- Case-insensitive literal substring q matches question/paragraph/bullet text. Topic and q combine with AND. No fuzzy matching or generated answer is implied.
- The complete fixture contains at most 50 published answers; return the full filtered set, without pagination. No matches displays a clear-filter action and the support form.

A.3 — Help-center shortcuts

- Track Order -> `/track-order`; Reset Password -> `/forgot-password`; User & Account -> `/faqs?topic=account`; Wishlist & Compare -> topic=shopping; Shipping & Billing -> topic=delivery; Shopping Cart & Wallet -> topic=shopping with visible label corrected to Shopping Cart; Payment Option -> topic=payments.
- Sell on Clicon is disabled with `Seller features are not part of this project.` Popular questions link to `/faqs?question=<id>`.
- CONTACT US links to `/faqs#support`. Replace Chat with us with Send a support request; no live-chat availability is asserted. Disable Call now and omit the sample phone/hours when no real service is configured. Do not dial Figma's placeholder phone number.

Exception Flow:

E.1 — Invalid filters

- Invalid/unknown topic IDs or malformed input return 400 VALIDATION_ERROR. Offer a link to unfiltered `/faqs` rather than silently using another topic.

E.2 — Data service failure

- 503 HELP_UNAVAILABLE shows retry. Missing optional topic imagery is not a whole-page error. A FAQ read failure does not disable UC-19's independently functioning form.
- The source uses filler answers and invalid contact timezone text; do not publish them as real project promises.

UI Integration:

- Sources: `24_Customer Support`, `447:9904`, and `21_FAQs`, `436:8148`.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=447-9904
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=436-8148
- Live contexts/screenshots inspected on 2026-09-19. Preserve help hero/search, topic tiles, popular questions, contact cards; preserve FAQ accordion plus yellow support-form column.
- Reuse Public Sans, orange active accordion/search controls, blue/green contact accents, and shared Clicon shell. Filter-result feedback is a project supplement; no frozen dataset/mobile layout is claimed.
- Keep FAQ support fields/buttons for UC-19 integration; in a UC-18-only build they are disabled with an explanation. No duplicated support submission implementation.

API Endpoint:

`GET /api/v1/help/topics`

`GET /api/v1/faqs`

Request Body:

No body. Topics accepts no query. FAQ accepts optional q (trimmed, max 100 Unicode code points; blank means absent) and topic (one returned topic ID). Unknown/repeated keys are validation errors.

Browser-only question is a 1–80 lowercase alphanumeric/hyphen ID; do not forward it to the API. Valid absence from results is UI feedback, not a service error. Topics are orders, account, shopping, delivery, payments.

Successful Response:

```json
{
  "success": true,
  "message": "Help topics retrieved.",
  "data": {
    "topics": [
      {
        "id": "orders",
        "name": "Orders"
      },
      {
        "id": "account",
        "name": "Account"
      },
      {
        "id": "shopping",
        "name": "Shopping"
      },
      {
        "id": "delivery",
        "name": "Shipping and billing"
      },
      {
        "id": "payments",
        "name": "Payments"
      }
    ],
    "popularQuestions": [
      {
        "id": "getting-order-number",
        "question": "Where can I find my order number?"
      }
    ]
  }
}
```

```json
{
  "success": true,
  "message": "FAQs retrieved.",
  "data": {
    "items": [
      {
        "id": "getting-order-number",
        "topic": "orders",
        "question": "Where can I find my order number?",
        "paragraphs": [
          "Your order number is displayed after checkout. Signed-in purchases also appear in account order history."
        ],
        "bullets": [],
        "links": [
          {
            "label": "Track an order",
            "href": "/track-order"
          }
        ]
      }
    ]
  }
}
```
- Both HTTP 200. Topics are the fixed supported set; popularQuestions references published FAQ IDs (zero to nine).
- Each answer has exactly id, topic, question, paragraphs, bullets, links. IDs are unique stable slugs; text fields nonempty; paragraphs/bullets are ordered string arrays and at least one contains content. links is an array of {label,href}; href is one of the already implemented local routes, including query/anchor when appropriate.
- Answers are curated experiment content, not quotations from a supplied Technical Report. They must not claim implemented online payment, cancellation, refunds, seller tools, or confirmation emails where earlier UCs exclude them. Empty matches return items=[].

Error Response:

Use the shared error envelope: success=false, statusCode matching HTTP status, code, message, server-generated ISO 8601 UTC timestamp, and actual request pathname without query string. Omit data. Optional errors is only for VALIDATION_ERROR and maps input paths to nonempty arrays of strings. All shown success keys are required; examples illustrate contracts rather than fixed data.

```json
{
  "success": false,
  "statusCode": 503,
  "code": "HELP_UNAVAILABLE",
  "message": "Help content is temporarily unavailable. Please try again later.",
  "timestamp": "2026-09-19T10:00:00.000Z",
  "path": "/api/v1/faqs"
}
```

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 503 | HELP_UNAVAILABLE | Help content is temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

## Project-Specific Implementation Context

### Backend Implementation Context

Implement public help reads in NestJS over a curated, ordered fixture with stable topic/FAQ IDs. Apply literal search and topic membership validation. Return only published answers; keep popular-question references consistent. Content management UI and external AI answering are out of scope.

### Frontend UI Context

Build HelpCenterPage and FaqPage with React/TypeScript/Tailwind and inspected layouts. Make accordion headings keyboard operable with expanded state. Correct unsupported contact promises and preserve the UC-19 form slot. Use existing shell routes for all enabled shortcuts.

### Frontend Logic and API Context

Keep q/topic/question in the browser URL, load only q/topic through the FAQ endpoint, and ignore older responses after filter changes. Search submits on Enter/button. Selecting a popular question clears incompatible filters. Support submission state is independent of FAQ loading.

### Validation and Error-Handling Context

Distinguish invalid filters, unavailable deep links, no results, and service failure. Render curated paragraphs/bullets as structured text. Network failure provides manual retry; no guessed answers or placeholder contact claims replace failed data.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
