# UC-21: Read and Post Blog Comments

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Read and Post Blog Comments

Description:

- Allows visitors to read published article comments, load older comments, and submit a name, email, and comment from the inspected article-detail form.
- Completes UC-20's comment count/anchor/form integration. Posting is public in this experimental baseline; displayed names are self-supplied, not verified account identities.
- Pagination, publication, input limits, and retry contracts are project decisions. Moderation tooling, replies, edits/deletion, likes, and notification email are outside this UC.

Primary Actor:

Visitor or signed-in Customer.

Preconditions:

UC-20 article-detail route and a currently published article exist. No login is required; submitted email is private contact metadata, not a sign-in credential.

Postconditions:

- Success: A single comment is persisted for the submission identifier, appears in public comments, and contributes exactly once to the article's commentCount.
- Failure: A rejected submission adds no comment/count. Unknown outcomes reuse the original submission ID; they are not automatically reposted with new IDs.
- Reading or posting does not affect product reviews, order reviews, or account profile.

Main Flow:

1. UC-20 loads the first five comments independently of article content.
2. The visitor reads them and may select LOAD MORE using the returned cursor.
3. They enter Full Name, Email Address, and their comment, then select POST COMMENT.
4. The frontend validates inputs and sends a new submission UUID with the normalized form.
5. The backend checks article publication and submission rules, saves the comment and updates its visible count.
6. On confirmed success, clear the form, display `Comment posted.`, reload the first comment page, and update the displayed article count. A failed refresh does not negate a confirmed post.

Alternative Flow:

A.1 — No comments or newer arrivals

- Empty comments display `No comments yet.` A new first-page load starts a new pagination sequence.
- LOAD MORE uses an opaque cursor bound to this article and the first-page publication boundary. Comments published after that first read are excluded from that sequence, including those sharing its timestamp; reloading page 1 shows them. Sort by createdAt descending then id descending, and append without duplicate IDs.

A.2 — Repeat submission

- A submissionId is unique per article. Same normalized name/email/message with the same ID returns the existing comment (200); first creation returns 201. Different content under that ID returns 409 SUBMISSION_CONFLICT.
- Lost response retains body/ID for a deliberate same-ID retry. Do not clear fields or report failure as certain; no automatic retry/new ID. A full reload may lose the local draft and must not imply the first comment failed.

A.3 — Observable limit

- At most three new comments per normalized email and ten per IP in the preceding hour across all articles. Identical known-ID replays do not count again. A 429 does not extend its wait; retryAfterSeconds reports when all applicable budgets permit a new comment.

Exception Flow:

E.1 — Article removed

- Unknown/unpublished article gives ARTICLE_NOT_FOUND for new posts and public reads. Stop posting and link back to blog. Existing hidden comments are not exposed through another slug or article.

E.2 — Invalid form or service failure

- Validation errors preserve the draft. Conflict preserves the previously saved comment. Service/network uncertainty follows same-ID retry; failed read/load-more has its own retry without discarding the article.
- Invalid/expired cursor returns INVALID_CURSOR; reload page 1 rather than inventing the next page.

UI Integration:

- Source: comment form/list at `26_Blog Detail`, node `494:18663`.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=494-18663
- Live context/screenshot inspected on 2026-09-19. Preserve two-column name/email inputs, full-width comment textarea, orange post action, name/date/text rows, and LOAD MORE.
- Correct source typos to Leave a Comment, Comment, POST COMMENT, and Comments. Use initials/neutral avatars; an entered email does not establish a real avatar or verified identity.
- Loading, validation, retry, and submitted states are project supplements. No frozen dataset or mobile form is claimed. Public output never includes the submitted email.

API Endpoint:

`GET /api/v1/blog/articles/:slug/comments`

`POST /api/v1/blog/articles/:slug/comments`

Request Body:

slug follows UC-20. GET accepts only optional cursor: nonempty opaque string up to 1024 characters returned by this endpoint; fixed limit 5. No GET body. POST has no query and accepts exactly:
```json
{
  "submissionId": "2b3ca1d6-f358-477f-b6e6-3cb9ff0a88d2",
  "fullName": "Alex Nguyen",
  "email": "customer@example.com",
  "message": "The comparison of practical needs was useful."
}
```
submissionId UUID; fullName trimmed 2–100 Unicode code points; email trimmed/lowercased valid format max 254 characters; message trimmed 1–2000 code points. Reject nulls, wrong types, extra/repeated query fields, and client timestamps/status.

Successful Response:

```json
{
  "success": true,
  "message": "Comments retrieved.",
  "data": {
    "items": [
      {
        "id": "b26553e1-d8bb-46f7-ad40-d89feab807ae",
        "fullName": "Alex Nguyen",
        "message": "The comparison of practical needs was useful.",
        "createdAt": "2026-09-19T11:00:00.000Z"
      }
    ],
    "totalItems": 1,
    "nextCursor": null
  }
}
```

```json
{
  "success": true,
  "message": "Comment posted.",
  "data": {
    "comment": {
      "id": "b26553e1-d8bb-46f7-ad40-d89feab807ae",
      "fullName": "Alex Nguyen",
      "message": "The comparison of practical needs was useful.",
      "createdAt": "2026-09-19T11:00:00.000Z"
    },
    "commentCount": 1
  }
}
```
- GET 200: items length 0–5, totalItems counts public comments within the sequence's publication boundary; nextCursor is a nonempty string or null at the end. Cursor validity is 30 minutes from first-page issuance; fresh page 1 starts again. Cursors for another article are invalid.
- POST 201 first creation or 200 exact replay. Comment has exactly id UUID, fullName, message, createdAt ISO UTC. commentCount is the current public article count at the response, not a promise it cannot change later.
- Public comments are plain text; email and submissionId are not returned. Preserve submission/result association while the comment exists; replay does not increment count or change timestamp. No email is sent.

Error Response:

Use the shared error envelope: success=false, statusCode matching HTTP status, code, message, server-generated ISO 8601 UTC timestamp, and actual request pathname without query string. Omit data. Optional errors is only for VALIDATION_ERROR and maps input paths to nonempty arrays of strings. All shown success keys are required; examples illustrate contracts rather than fixed data.

```json
{
  "success": false,
  "statusCode": 400,
  "code": "INVALID_CURSOR",
  "message": "This comment page is no longer available. Reload the comments.",
  "timestamp": "2026-09-19T10:00:00.000Z",
  "path": "/api/v1/blog/articles/choosing-a-laptop/comments"
}
```

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 400 | INVALID_CURSOR | This comment page is no longer available. Reload the comments. |
| 404 | ARTICLE_NOT_FOUND | This article is not available. |
| 409 | SUBMISSION_CONFLICT | This submission identifier was already used for different content. |
| 429 | COMMENT_RATE_LIMITED | Too many comments. Please try again later. |
| 503 | COMMENTS_UNAVAILABLE | Comments are temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

429 includes positive integer retryAfterSeconds matching Retry-After. errors is only for VALIDATION_ERROR, not INVALID_CURSOR.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement public comment reads/creates in NestJS with published-article checks, deterministic cursor pagination, exact-repeat behavior, and one visible count increment per new comment. Keep submitted contact email out of public projections. No moderation/notification service is implied; public persistence is the explicit experiment rule.

### Frontend UI Context

Enable UC-20's comment region using the inspected layout. Show accessible form labels, visible required-field feedback, plain-text comment bodies, UTC dates, and LOAD MORE only when a cursor exists. No nested replies or account-verification badges are invented.

### Frontend Logic and API Context

Keep article comment state independent of primary content. Reset cursor/items on article change, cancel obsolete loads, and append by stable IDs. On post success reload page 1 and update count; distinguish confirmed-post/failed-refresh from failed-post. Unknown outcomes allow only deliberate exact-ID retry until resolved or a clearly separate new submission.

### Validation and Error-Handling Context

Validate article visibility and form values on the server. A missing article cannot receive a new comment. Invalid cursors reset only through an explicit first-page reload. No raw private email, markup execution, simulated moderation, or fabricated post success appears in UI.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
