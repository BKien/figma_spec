# UC-22: Sign Out of the Current Session

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Sign Out of the Current Session

Description:

- Allows a signed-in customer to end the current browser account session and continue browsing as a guest.
- Completes the Log-out sidebar control previously left disabled. All-device session termination remains the password-change/recovery outcome of UC-12/UC-03, not an extra logout feature.
- Session termination, uncertain-result handling, and navigation are project decisions; Figma establishes the visible sidebar action.

Primary Actor:

Signed-in Customer; the operation also succeeds when the presented session is already absent/expired.

Preconditions:

- UC-02 session transport/read and `/sign-in` exist; `/shop` is provided by UC-04.
- Implemented account pages share their sidebar and authenticated frontend state. Logout is a deliberate action, not a GET navigation side effect.

Postconditions:

- Success: The session presented for logout is ended and no longer authenticates requests. Its browser credential is cleared through the existing session integration, private frontend state is cleared, and `/sign-in` displays `You have signed out.`
- Other independent account sessions remain valid. Account profile, saved addresses, account history, order ownership, and saved reviews persist.
- Browser cart/wishlist/comparison and original-browser receipt/tracking access persist under their existing rules. Logout is not account deletion or a request to erase a guest cart.
- Failure/unknown outcome: The frontend does not declare the server session ended without a successful logout response or confirming unauthenticated session read.

Main Flow:

1. The customer selects Log-out in an implemented account sidebar.
2. If settings have dirty drafts, show the supplementary discard notice described below; continue only after the customer chooses Sign out and discard.
3. The frontend sends `POST /api/v1/auth/logout` once and disables duplicate logout actions.
4. The backend ends the presented session when it exists and completes browser-session clearing. A missing/already-ended session returns the same success.
5. The frontend clears account-specific cached data and password/draft state, then navigates to `/sign-in` with `You have signed out.`
6. Opening a protected page again requires a valid new login; public shop/cart routes remain available.

Alternative Flow:

A.1 — Already signed out

- A request with an absent/expired/already-ended session returns HTTP 200 with the same body, not a new login requirement or account-not-found error. Repeated logout does not affect a different independent session.

A.2 — Unsaved settings

- Dirty UC-11 profile or UC-13 addresses trigger `Sign out and discard unsaved changes?` with Stay and Sign out and discard. Stay does not call the endpoint. Proceed clears drafts only after confirmed logout or the user leaves account state during recovery.
- Password fields are always cleared when leaving their panel. In-progress mutation buttons, including logout, are mutually disabled within that account view so the page does not deliberately launch conflicting save/logout actions.

A.3 — Checkout after logout

- An open account-bound checkout quote does not become a guest quote by logout. UC-15's first-placement authentication/account-change rules still apply.
- On returning to checkout, resolve the current session and quote state. Obtain a fresh guest quote only after any unresolved placement is reconciled under UC-07. Never replay a pending order merely to resume guest checkout.

A.4 — Another login occurs concurrently

- The endpoint ends only the session attached to its request. A session created separately afterward is not implicitly revoked as part of all-device logout.
- On an eventual private route load, the standard session check determines current authentication. Do not promise that a logout response prevents another tab/device from independently signing in.

Exception Flow:

E.1 — Network or ambiguous response

- Clear displayed private content while resolving the result and show `We could not confirm sign-out. Checking your session.` Do not show the success banner yet.
- Call UC-02's session endpoint once. A 401 confirms no current usable session and completes guest navigation. A 200 means a session is still present; display `You are still signed in. Try signing out again.` and require a deliberate new logout action.
- A failed session check leaves authentication unresolved with Check session again; do not automatically repeat POST or announce success.

E.2 — Service failure

- 503 LOGOUT_UNAVAILABLE and unexpected/malformed responses follow the same session-reconciliation path when the actual session outcome is uncertain.
- Do not implement local-only credential removal as proof of server-side logout. Do not clear unrelated browser shopping collections to simulate a successful account action.

UI Integration:

- Observed Log-out item in account sidebars, including `34_Dasboard_Setting` node `478:17305` and `28_Dasboard_Order History` node `478:10910`.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=478-17305
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=478-10910
- The Log-out action was visible in the account sidebar contexts/screenshots inspected for this series. No separate logout success/error screen or modal was verified.
- Enable the existing item on all implemented account pages. Pending, discard-confirmation, uncertain-result, and Sign In feedback are project supplements. Reuse Public Sans, existing sidebar styling, and UC-02's Sign In route; no new logout route/page or frozen dataset is claimed.
- The minimal account dashboard shell receives a Sign out action so the feature is reachable even when no full dashboard UC exists.

API Endpoint:

`POST /api/v1/auth/logout`

Result reconciliation reuses `GET /api/v1/auth/session`.

Request Body:

No body or query parameters. The existing browser session identifies the session being ended. Reject supplied bodies/query keys with VALIDATION_ERROR; no accountId, allDevices flag, password, or token JSON field is accepted.

No 401 is returned merely because the logout session is absent; that is successful idempotent logout.

Successful Response:

```json
{
  "success": true,
  "message": "You have signed out.",
  "data": {
    "signedOut": true
  }
}
```
HTTP 200. All fields required; signedOut is literal true and describes completion for the session presented to this logout operation. Return success only after the session-ending outcome is complete. No new user/session/token is returned. Browser credential clearing uses the existing project session integration, without specifying its underlying cookie/cryptographic implementation here.

Error Response:

Use the shared error envelope: success=false, statusCode matching HTTP status, code, message, server-generated ISO 8601 UTC timestamp, and actual request pathname without query string. Omit data. Optional errors is only for VALIDATION_ERROR and maps input paths to nonempty arrays of strings. All shown success keys are required; examples illustrate contracts rather than fixed data.

```json
{
  "success": false,
  "statusCode": 503,
  "code": "LOGOUT_UNAVAILABLE",
  "message": "Sign-out is temporarily unavailable. Please try again later.",
  "timestamp": "2026-09-19T10:00:00.000Z",
  "path": "/api/v1/auth/logout"
}
```

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 503 | LOGOUT_UNAVAILABLE | Sign-out is temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

UC-02 session-read errors retain their existing path and contract, including 401 UNAUTHENTICATED.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement logout in NestJS using the existing session store/transport. Terminate only the presented session; missing/ended sessions are successful. Do not update user status, revoke every device, erase history, or shorten browser-cart identity lifetime. Keep password-change/recovery invalidation behavior unchanged.

### Frontend UI Context

Enable the shared sidebar action in React/TypeScript/Tailwind and the minimal account shell action. Add the declared dirty-settings notice, pending state, and uncertain-result recovery. Success uses the existing Sign In page, not a new visual feature.

### Frontend Logic and API Context

Disable duplicate submission, clear account/profile/address/history/order/review caches after confirmed logout, and discard obsolete private responses from the preceding session. Public browsing data and browser shopping collections remain. Protected route guards still use the session endpoint on entry. Reconciliation distinguishes confirmed 401 from service failure and does not auto-retry POST.

### Validation and Error-Handling Context

Validate the empty request contract. Success must reflect server termination, not just local UI clearing. Unknown outcomes use session inspection without exposing another account's cached data. Logout cannot claim account deletion, password change, all-device termination, or guest-order reassignment.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
