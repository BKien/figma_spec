# UC-11: Manage Account Profile

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

View and Update Account Profile

Description:

- Allows an authenticated customer to view account information and update profile names, optional secondary contact details, and an optional profile location.
- Implements the Account Setting section of the inspected settings frame, using the account established by UC-01 and session defined by UC-02.
- Field semantics, editable boundaries, location fixtures, concurrency behavior, and API contracts are project decisions. Figma establishes the desktop controls and layout.
- Changing the primary email, password, avatar, billing/shipping addresses, or account status is outside this UC. Profile updates do not modify previously placed orders or browser-scoped cart, wishlist, and comparison data.

Primary Actor:

Signed-in Customer with an active, verified account.

Preconditions:

- UC-01 supplies the shared account identity, fullName, normalized email, status, and emailVerifiedAt.
- UC-02 supplies an unexpired browser session and `GET /api/v1/auth/session`. Its eight-hour lifetime and cookie-based transport remain unchanged.
- `/account/settings` supports direct navigation and reload. `/account/dashboard` remains the existing account integration shell.
- The shared success/error envelope applies.

Postconditions:

- Success: The complete accepted profile update is saved for the current account, its revision advances, and the form reflects the returned normalized values.
- Success: Changes to fullName are reflected in subsequent session responses and the account shell without creating a different account.
- Failure: A rejected update saves no subset of the submitted fields. Unsaved values remain local unless the documented conflict/reconciliation behavior replaces them.
- Primary email, verification, password, account status, session expiry, order snapshots, and browser shopping collections are unchanged.

Main Flow:

1. The customer opens `/account/settings` from a Settings link added to the existing account shell or the account sidebar.
2. The frontend resolves the UC-02 session. Missing/expired authentication follows E.1; service failure shows retry feedback.
3. The frontend loads `GET /api/v1/account/profile` and displays the current profile and primary email.
4. The customer edits permitted fields. Primary Email and the avatar remain read-only.
5. The customer selects `SAVE CHANGES`. The frontend validates the complete form and sends `PUT /api/v1/account/profile` with the loaded revision.
6. The backend resolves the current authenticated account, validates the revision and input, and saves the complete update.
7. The backend returns HTTP 200 with the new profile snapshot. The frontend replaces its saved/draft values, clears dirty state, and displays `Profile updated.`
8. The frontend refreshes the shared session-facing user data so the account shell uses the saved fullName. This does not renew the session.

Alternative Flow:

A.1 — Newly registered account

- Existing fullName and primary email come from UC-01. Optional profile fields initially contain null; do not infer a username, location, phone number, or secondary email from the Figma example.
- The initial profile revision is 0. GET returns this representation without requiring a separate user-created profile record.

A.2 — Clear optional fields

- Empty optional text inputs are submitted as null. Clearing displayName, username, secondaryEmail, or phone removes only that profile value.
- Location is either entirely null or contains all three fields countryCode, regionCode, and postalCode. Selecting no country clears its dependent state/postal code.
- Optional secondary email and phone are informational contacts only; they are not verified identities or sign-in/recovery destinations in this UC.

A.3 — Name semantics

- fullName is the canonical account name already used by UC-01/UC-02 and is required.
- displayName is an optional presentation alias. It does not replace fullName in the existing session response contract.
- The source's Username is an optional profile label, not a login identifier. It is not globally unique or used to locate an account. Display helper text `Profile label only; sign in with your email.`

A.4 — Leave without saving

- Edits are local until SAVE CHANGES succeeds. Navigating away or reloading discards them; the next load shows persisted values.
- Show `Unsaved changes will be lost if you leave this page.` while dirty. No automatic save or additional confirmation modal is required.

Exception Flow:

E.1 — Authentication no longer valid

- Missing/expired session, or an account no longer active/verified, returns HTTP 401 UNAUTHENTICATED. Clear displayed profile data and navigate to `/sign-in`.
- Do not retain or replay unsaved profile changes after reauthentication. UC-02 still returns to its existing dashboard; the customer can reopen Settings.

E.2 — Invalid fields

- Return HTTP 400 VALIDATION_ERROR with field-specific feedback when possible. Preserve the current draft for correction; no field is saved.
- Primary email, account ID, status, verification fields, password, avatar, and billing/shipping fields are not accepted in this update contract.

E.3 — Profile changed elsewhere

- A mismatched expectedRevision returns HTTP 409 PROFILE_CHANGED. Keep the unsaved draft visible with `Your profile changed elsewhere. Reload it before saving again.` and disable saving.
- A deliberate `Reload profile` action discards the draft, fetches the current profile, and displays the latest revision. Do not automatically overwrite another session's changes or retry the stale update.

E.4 — Service failure or uncertain save result

- Explicit validation/conflict rejection saves nothing. For a lost/malformed save response or ambiguous server failure, show `We could not confirm your profile update. Reload your profile before trying again.`
- Disable further saves until GET resolves the current state. The reload replaces the draft with persisted values and must not automatically resend the old update.
- If reload fails, retain the recovery state with a manual retry. Never claim successful persistence from local form values alone.

UI Integration:

- Source: `34_Dasboard_Setting`, node `478:17305`, desktop 1920 × 2712; scope is the Account Setting panel and shared account navigation.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=478-17305
- Live design context and rendered screenshot were inspected on 2026-09-18. No frozen dataset, responsive frame, or unseen validation/loading state is claimed.

| Observed element | Integration |
| --- | --- |
| Avatar | Read-only current avatar when available, otherwise neutral initials placeholder |
| Display name | Optional displayName |
| Username | Optional non-authentication profile label username |
| Full Name | Required canonical fullName |
| Email | Read-only primary email from UC-01 |
| Secondary Email / Phone Number | Optional informational contacts |
| Country/Region / States / Zip Code | Optional complete profile location |
| SAVE CHANGES within Account Setting | Save only this panel's editable fields |
| Setting sidebar item | Active `/account/settings` navigation |
| Billing Address / Shipping Address / Change Password panels | Separate UC integration areas, not editable in this UC |

- Reuse the shared Clicon shell, sidebar, Public Sans, bordered two-column account form, orange actions (#FA8232), and light borders (#E4E7E9).
- The source breadcrumb ends in Cards & Address while Setting is selected. Use Home > User Account > Settings for this route rather than repeating the inconsistent sample.
- Show `Email changes are not available here.` beside read-only primary email. No upload interaction is inferred from the avatar image.
- Keep subsequent address/password panel headings as disabled integration areas with `Available in a separate account feature.` Do not display editable forms, sample personal data, or active save buttons that cannot work.
- Sidebar routes already implemented are Dashboard, Track Order, Shopping Cart, Wishlist, Compare, and Settings. Order History, Cards & Address, Browsing History, and Log-out remain disabled with scope explanations until their owning UCs exist.
- Country/state choices use the explicit experiment fixture below. Figma's Bangladesh/Dhaka sample is not a required account location or a source of address validation rules.
- Loading, field errors, conflict reload, dirty feedback, and placeholder avatar are project supplements. Profile location is not a delivery address and does not prefill checkout automatically.

API Endpoint:

| Method and path | Purpose |
| --- | --- |
| `GET /api/v1/account/profile` | Read the currently authenticated account profile and location options |
| `PUT /api/v1/account/profile` | Save its complete editable profile field set |

Request Body:

GET has no body or query parameters. PUT accepts:

```json
{
  "expectedRevision": 0,
  "fullName": "Alex Nguyen",
  "displayName": "Alex",
  "username": null,
  "secondaryEmail": null,
  "phone": "+14155550123",
  "location": {
    "countryCode": "US",
    "regionCode": "CA",
    "postalCode": "94105"
  }
}
```

- All shown top-level keys are required. Reject unknown fields, query parameters, and incorrect types; do not silently ignore attempted primary-email or account-status updates.
- expectedRevision is a nonnegative JSON integer. fullName is trimmed and contains 2–100 Unicode code points, matching UC-01.
- displayName is null or trimmed text of 1–100 Unicode code points. username is null or 3–30 ASCII letters, digits, or underscores, preserving case; uniqueness is not required.
- secondaryEmail is null or a trimmed/lowercased valid email address of at most 254 characters. It may equal the primary email, without changing verification or identity.
- phone is null or a plus sign followed by 8–15 ASCII digits with the first digit nonzero. Blank optional inputs become null before submission.
- location is null or an object containing exactly countryCode, regionCode, and postalCode. The only experiment location is US/CA; postalCode must contain exactly five ASCII digits. This deliberately limited fixture is consistent with UC-07's California experiment coverage, not a worldwide address directory.
- Body identity is never used to select an account; the authenticated session determines the target. No password or session token is submitted in this profile body.

Successful Response:

GET and PUT return HTTP 200 with the same data schema. Messages are `Profile retrieved.` and `Profile updated.` respectively.

```json
{
  "success": true,
  "message": "Profile updated.",
  "data": {
    "profile": {
      "id": "7217276b-056c-494c-9709-aa30913e013b",
      "revision": 1,
      "fullName": "Alex Nguyen",
      "displayName": "Alex",
      "username": null,
      "email": "customer@example.com",
      "secondaryEmail": null,
      "phone": "+14155550123",
      "location": {"countryCode": "US", "regionCode": "CA", "postalCode": "94105"},
      "avatarUrl": null
    },
    "locationOptions": [{
      "code": "US",
      "name": "United States",
      "regions": [{"code": "CA", "name": "California"}]
    }]
  }
}
```

- All keys are required. id is the existing account UUID, not a separate profile identity. email is the account's normalized primary email.
- Editable values follow the request schema. avatarUrl is a string or null and is read-only; null uses the declared placeholder.
- revision starts at 0 and increments by one per accepted PUT, including an accepted unchanged body. GET and failed PUT do not advance it.
- locationOptions is the complete supported fixture. The response does not modify checkout's distinct options endpoint or delivery/contact snapshots.
- The existing session response retains its original schema and canonical fullName. Profile reads/updates neither issue authentication tokens in JSON nor extend session expiry.

Error Response:

Use the centralized envelope; errors omit data. timestamp is server-generated ISO 8601 UTC; path is the actual endpoint pathname.

```json
{
  "success": false,
  "statusCode": 409,
  "code": "PROFILE_CHANGED",
  "message": "Your profile changed elsewhere. Reload it before saving again.",
  "timestamp": "2026-09-18T10:00:00.000Z",
  "path": "/api/v1/account/profile"
}
```

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-18T10:00:00.000Z",
  "path": "/api/v1/account/profile",
  "errors": {"fullName": ["Full name must contain 2 to 100 characters."]}
}
```

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | `Please correct the highlighted fields.` |
| 401 | UNAUTHENTICATED | `You must sign in to continue.` |
| 409 | PROFILE_CHANGED | `Your profile changed elsewhere. Reload it before saving again.` |
| 503 | PROFILE_UNAVAILABLE | `Your profile is temporarily unavailable. Please try again later.` |
| 500 | INTERNAL_ERROR | `Unable to complete your request. Please try again later.` |

- Optional errors appears only for VALIDATION_ERROR, mapping input paths such as location.postalCode to nonempty arrays of messages. Body-level errors may omit it.
- A missing optional profile extension is the initial profile representation, not a 404. An absent/ineligible authenticated account follows UNAUTHENTICATED.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement the two profile endpoints in NestJS using the existing UC-01 account and UC-02 session integration.

- Resolve the current active, verified account for each request. Reuse its identity and canonical fullName/email; optional profile fields extend it without creating competing authentication semantics.
- Serve the declared initial nullable fields and revision for existing accounts. Keep primary email, verification, status, password, and avatar outside the editable field set.
- Compare expectedRevision and save all accepted editable values as one business outcome. Concurrent stale requests cannot overwrite a newer profile snapshot or produce a partially updated profile.
- Keep canonical fullName consistent with subsequent session reads. Do not change the original session expiry or require a new registration merely because a name changes.
- Profile location/contact fields remain separate from address-book entries and immutable checkout/order contact snapshots. No automatic history rewrite or account-to-browser-cart merge is introduced.

### Frontend UI Context

Build the Account Setting portion of `/account/settings` in React, TypeScript, and Tailwind CSS.

- Add a reachable Settings link to the existing `/account/dashboard` shell; reuse its authenticated routing behavior. Do not implement the full business Dashboard as part of this UC.
- Render the observed account-panel structure and editable fields with explicit labels, read-only primary email, and noninteractive avatar.
- Use API location options for the two selectors. Clearing/changing country resets an incompatible region and postal code; show the complete-location requirement before saving.
- Show dirty state and SAVE CHANGES only enabled for a changed, valid draft with no request in progress. Keep other panels and unavailable sidebar destinations scoped as specified.

### Frontend Logic and API Context

- Maintain a saved profile snapshot, revision, editable draft, loading state, field errors, conflict state, and save/reconciliation state.
- Resolve authentication before displaying personal data. Initialize the form from GET and preserve a distinct primary-email display value outside the PUT body.
- Submit the complete editable field set and loaded revision. On success, replace the draft with the normalized response and update the shared user's fullName before refreshing the session endpoint.
- If the subsequent session refresh fails temporarily, retain the confirmed profile-save result and show a session-refresh retry; do not resubmit PUT. A definitive 401 clears account state and returns to Sign In.
- After a conflict, wait for deliberate Reload profile before discarding the draft. After an uncertain save outcome, require GET reconciliation before another save.
- Ignore obsolete requests after navigation or account/session changes. A response belonging to a previous signed-in account must not populate the current account screen.

### Validation and Error-Handling Context

- Validate complete field shape, lengths, optional-null semantics, contact syntax, and fixture location on the server. Client validation supplies feedback but does not determine persisted values.
- Distinguish missing authentication, field errors, revision conflict, and service failure. A service outage is not a reason to display another account's cached profile.
- Primary email and status are not writable even when extra fields are submitted directly. username/secondaryEmail never become alternative login or recovery identifiers through this UC.
- No HTTP response displays `Unable to connect. Please check your connection and try again.` For uncertain saves, also follow the reconciliation flow rather than automatically retrying the update.
- Malformed profile data displays `Unable to load your profile. Please try again.` Do not populate the form with Figma example identities or assume unknown fields are confirmed empty values.
- All settings navigation must resolve to an implemented route or a visibly disabled integration control. No success message is shown for address, password, email, or avatar changes that this UC does not implement.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
