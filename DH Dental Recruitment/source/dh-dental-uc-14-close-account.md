# UC-14: Permanently Close Account

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Permanently Close Account

Description:

- Allows an authenticated Job Seeker to permanently close their own account after reviewing the consequences and confirming the action.
- The Figma source states that closed accounts cannot be reactivated and presents Close Account Now. This UC implements closure and removal of the account's current research data, not merely the current-session sign-out in UC-13.
- Confirmation, lifecycle changes, deletion scope/timing, concurrency rules, and API contract are explicit research decisions. This specification does not claim legal compliance or immediate erasure from infrastructure outside the defined research data stores.

Primary Actor:

Authenticated ACTIVE JOB_SEEKER choosing to close their own account.

Preconditions:

- UC-01/02 account/session services exist, and UC-05–12 define the account-owned profile, preferences, credential, and media data to remove.
- `/settings/close-account` is a real reloadable route. Enable Close Account in the existing settings tabs; Switch Account remains unavailable until specified.
- The backend can commit closure, remove account-owned database content, invalidate every account session, and durably schedule removal of owned media files. The media cleanup process is part of implementing this UC, not an optional future task.
- No complete-profile or verified-contact prerequisite is imposed.

Postconditions:

- Confirmed success: The account becomes CLOSED, cannot sign in or reactivate, and its existing sessions no longer authorize new requests. Account-owned database content is removed at closure; owned file bytes become inaccessible immediately and are deleted from active storage within 24 hours.
- Failure before commit: Account, sessions, and data remain unchanged. A lost response or unknown commit result is presented as uncertain, not as confirmed closure or guaranteed rollback.
- A minimal nonpersonal tombstone remains with only account ID, status CLOSED, and closedAt. A later registration may reuse the released email but creates a new account ID and restores none of the old content.
- Public jobs and FAQ content remain intact. Independently submitted Contact Us messages follow UC-16's separate 30-day retention and are not removed by account closure.

Main Flow:

1. Open Settings → Close Account and confirm the current UC-02 account identity.
2. Display the closure warning, data-removal scope/timing, and distinction from signing out.
3. Select Close Account Now. Open a confirmation dialog displaying the account email, the irreversible consequence, and Cancel / Permanently close account actions.
4. On confirmation, submit the displayed account ID as an expected-identity guard and confirmed true. Disable duplicate submission.
5. The backend checks the current eligible session and expected identity, then commits closure and the defined database removal, session invalidation, and durable media-cleanup work together.
6. On HTTP 200, clear private frontend state and local drafts, stop recording/playback, navigate to public `/jobs`, and show `Account closed permanently.`
7. Subsequent protected requests or login attempts for that closed account fail under UC-02's existing generic rules. The media cleanup completes within the defined deadline.

Alternative Flow:

A.1 — Cancel or sign out instead

- Cancel closes the dialog without any request or data change. Opening the page or dialog never closes an account.
- Offer a supplementary Sign out instead action using UC-13 when the actor only wants to end the current session. Do not substitute sign-out for confirmed closure.

A.2 — Unsaved draft or in-flight operation

- Explain that local drafts will be discarded if closure succeeds. Stop local capture before submitting; Cancel before submission leaves the account unchanged.
- A previously started profile/media write must not recreate account data after closure. If it commits first, closure removes its result; if closure wins first, the write must fail its account-eligibility check before commit.
- Existing protected transfers may finish if already in progress, but new media requests cannot retrieve closed-account files. Closure does not promise to retract bytes already downloaded.

A.3 — Fresh registration after closure

- The normalized email is released on the committed closure. UC-01 may create a genuinely new account with a new registration request ID and new account UUID; this is not reactivation.
- Remove old UC-01 registration replay receipts associated with the closed account at closure so they cannot return its former user data. A former receipt cannot restore or prove ownership of the closed account.

A.4 — Direct entry

- Add exactly `/settings/close-account` to UC-02's accepted local next destinations, with no query/fragment, encoded as next. An unauthenticated visit goes through sign-in; it never triggers closure automatically after login.

Exception Flow:

E.1 — Session or displayed identity changed

- Missing, expired, or account-ineligible sessions return UNAUTHENTICATED; an otherwise valid unsupported-role session returns ROLE_NOT_ALLOWED.
- If the current session account differs from expectedAccountId, return ACCOUNT_CONTEXT_CHANGED without changing either account. Reload identity and require a new confirmation for the actual current account.
- expectedAccountId is a comparison guard only, never a selector for an account that the session does not own.

E.2 — Concurrent closure or password change

- Recheck ACTIVE status and session validity at the closure commit boundary. A losing request cannot resurrect an account or close a newly registered account that reuses the email.
- If closure already invalidated the session, a repeated request returns UNAUTHENTICATED. Unlike UC-13 logout, this operation does not return success to arbitrary unauthenticated requests.
- If a concurrent password change invalidates the session first, require sign-in again before a new closure confirmation.

E.3 — Service or media-cleanup failure

- If the database closure and durable cleanup scheduling cannot commit, return ACCOUNT_CLOSURE_UNAVAILABLE with no completed closure.
- A media-storage outage after closure is committed does not reopen the account. Keep the files inaccessible through the application and retry deletion until completed. A cleanup process must expose an operational failure if the 24-hour deadline is missed; do not mark deletion complete just because the account is CLOSED.

E.4 — Response lost

- Do not automatically retry an irreversible action or display closure success. Clear private display/capture state and GET the UC-02 session.
- A 401 establishes no usable presented session, not proof of account closure. Show `The account closure could not be confirmed. Your browser has no active session.` with public jobs and sign-in links.
- A 200 shows the actual current identity and leaves the outcome unknown; let the actor deliberately review the closure page again. A failed session check remains unresolved. Never try credentials automatically or claim that a timeout restored deleted data.

UI Integration:

- File DH Dental Recruitment (Community), Pages / Job Seeker (`1:2`).
- [Settings / Close Account, frame `2:4425`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4425): settings tabs, warning card, and red Close Account Now action. Context/screenshot inspected on 2026-09-23.
- Preserve the irreversible-closure emphasis. Replace references to existing connections with the actual implemented scope: account contacts, profile, preferences, saved resume/photo/video, and sessions.
- Display before confirmation: `Closure is permanent. Your account data will be removed and all sessions will end. Saved media will become unavailable immediately and be deleted from active storage within 24 hours. Contact Us submissions are separate and may remain for up to 30 days.`
- The identity-bound confirmation dialog, cleanup timing, Sign out instead, and loading/error/responsive states are project supplements; no frozen dataset or source prototype behavior is claimed.
- The dialog names the current account, supports keyboard focus and Cancel, and has no preselected confirmation. Once submitted, do not offer Cancel as though it can undo a committed closure. Do not copy the source's unrelated Introduction Video active underline.

API Endpoint:

- `POST /api/v1/auth/account-closure`

Requires an eligible UC-02 browser session; accepts application/json, no query parameters. Reuses GET /api/v1/auth/session only for reconciliation. There is no public closure-status lookup by email/account ID and no reactivation endpoint.

Request Body:

```json
{
  "expectedAccountId": "137a3a0f-dc84-460d-9c97-03f3cf6dcae7",
  "confirmed": true
}
```

Both keys are required and no others are accepted. expectedAccountId is a UUID captured from the account displayed in the confirmation dialog. confirmed must be the JSON boolean true. A false/missing/string value is invalid. The target account is always derived from the session; the UUID only prevents closing an unexpected account after a browser identity change.

No email, password, deletion deadline, retention flag, allAccounts option, or redirect target is accepted. This UC does not introduce a new current-password form absent from its source.

Successful Response:

```json
{
  "success": true,
  "message": "Account closed permanently.",
  "data": {
    "accountStatus": "CLOSED",
    "closedAt": "2026-09-23T17:00:00.000Z",
    "mediaDeletionDueAt": "2026-09-24T17:00:00.000Z"
  }
}
```

HTTP 200 only after the closure commit. data has exactly accountStatus (always CLOSED), closedAt (server UTC ISO 8601), and mediaDeletionDueAt (closedAt plus 24 hours). The deadline appears even when there are no owned media files; it is the latest allowed completion time, not a claim that files have already been deleted.

The submitting browser credential is cleared and all sessions for the closed account cease authorizing new requests. No user summary, password, contact data, or new session is returned. Other accounts, including a later account with the same email, remain independent.

Error Response:

JSON errors have exactly success false, statusCode, code, message, timestamp (server UTC ISO 8601), and path (actual pathname without query). VALIDATION_ERROR additionally has errors, mapping field paths to nonempty arrays of messages. Only a documented 429 adds a positive integer retryAfterSeconds and the equal Retry-After header. Other errors omit these extensions. Do not add data: null.

| HTTP | code | message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | Please sign in to continue. |
| 403 | ROLE_NOT_ALLOWED | This action is not available for your account role. |
| 409 | ACCOUNT_CONTEXT_CHANGED | The signed-in account changed. Review the account before confirming closure. |
| 503 | ACCOUNT_CLOSURE_UNAVAILABLE | Account closure is temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

No endpoint-specific attempt limit is introduced. Transport failure is not a fabricated JSON response.

```json
{
  "success": false,
  "statusCode": 409,
  "code": "ACCOUNT_CONTEXT_CHANGED",
  "message": "The signed-in account changed. Review the account before confirming closure.",
  "timestamp": "2026-09-23T17:00:00.000Z",
  "path": "/api/v1/auth/account-closure"
}
```

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-23T17:00:00.000Z",
  "path": "/api/v1/auth/account-closure",
  "errors": {
    "confirmed": [
      "Confirm permanent account closure."
    ]
  }
}
```

## Project-Specific Implementation Context

### Backend Implementation Context

Extend the Account lifecycle with CLOSED while preserving all existing ACTIVE-account contracts. A closed account is represented only by its UUID, CLOSED status, and closedAt in a tombstone. Implement this as a separate tombstone or an equivalent lifecycle representation; do not weaken required identity fields for ACTIVE accounts or return tombstones through UC-02's user summary.

At closure commit remove the account's contact/name/credential/registration data, associated registration replay receipts, basic profile/photo reference, job preferences, work experience/resume reference, education, introduction-video reference, notification preferences, and session authorizations. Retain only nonpersonal media-deletion task references until file cleanup finishes. No work/education or notification record survives as an accessible orphan.

Release the email uniqueness reservation at that same boundary. Registration must not reuse the closed account UUID or replay its old registration receipt. UC-02 continues returning generic INVALID_CREDENTIALS for a closed account's credential; GET session and protected endpoints return their existing UNAUTHENTICATED results.

Account-owned mutations introduced by UC-05–12 must check continued account eligibility before commit so delayed saves cannot repopulate closed accounts. Use their existing UNAUTHENTICATED response when closure invalidates the operation; no new global error envelope is needed. New uploads rejected by that condition are cleaned up as unused files.

Delete current owned media from active storage within 24 hours; the application stops serving them immediately at closure. Use a durable cleanup task included in the closure commit, with recovery after interruption and visible failure tracking. This scope contains no external backup/archival service and makes no claim about such systems. Contact Us records in UC-16 are independent public submissions with their own 30-day retention, as disclosed before closure.

### Frontend UI Context

Use the existing React/TypeScript/Tailwind settings shell with Close Account active. Keep the warning visually distinct and the destructive action clearly named. Explain the implemented data scope and timing rather than claiming instant deletion of every possible copy.

Capture the displayed session identity when opening confirmation. Any observed account change dismisses the old confirmation; require the actor to review the new account. Cancel restores focus to Close Account Now.

After confirmed success, show the public jobs page and the exact success message. After an unknown result, display uncertainty without a success toast or an automatic repeated destructive action. Losing a session is not sufficient evidence to announce account deletion.

### Frontend Logic and API Context

Read UC-02 session before exposing the closure form. Send expectedAccountId from the displayed identity and confirmed true only after explicit confirmation. Keep backend identity comparison authoritative even if another tab changes the browser session after the frontend check.

Disable duplicate submission. On confirmed success clear the same private state listed in UC-13, including account media and local drafts; do not invoke ordinary logout as a substitute for closure or restore caches from the last session read.

Ignore late account-specific save/read responses after closure. Other tabs must refresh eligibility before redisplaying protected cached data. Do not route to profile pages as a success destination.

On 409, discard the stale confirmation and reload identity. On 401, clear private state without asserting that closure occurred. Handle network ambiguity exactly as E.4; no automatic retry, login attempt, or reactivation action is added.

### Validation and Error-Handling Context

Reject unknown JSON keys, missing/invalid UUID, confirmed values other than true, unsupported queries, and wrong request media type. Use expectedAccountId, confirmed, or request field paths in errors. A syntactically valid but different expectedAccountId is the documented 409, not permission to target it.

Validate session eligibility and expected identity before destructive changes, then preserve those conditions through commit. Rejected requests leave account data untouched. Once closure is committed, a failed cleanup attempt must never reverse the CLOSED state or make media readable again.

Distinguish committed closure, precommit failure, and unknown outcome. The API's mediaDeletionDueAt is a deadline backed by cleanup work, not a decorative field. Do not silently report the deadline met when file removal has not completed.
