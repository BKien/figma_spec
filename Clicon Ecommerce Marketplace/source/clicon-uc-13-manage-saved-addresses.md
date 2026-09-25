# UC-13: Manage Saved Billing and Shipping Addresses

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Manage Saved Billing and Shipping Addresses

Description:

- Allows an authenticated customer to view, create, and replace one saved billing address and one saved shipping address independently from Account Settings.
- Enables deliberate reuse of saved addresses in UC-07 checkout without changing its request or order-snapshot contracts.
- Address slots, validation, revision handling, and checkout mapping are project decisions. Figma establishes the two desktop address forms and their separate save actions.
- Multiple-address books, deletion, default-address selection, geocoding, payment-card management, and carrier address verification are outside this UC.

Primary Actor:

Signed-in Customer with an active, verified account.

Preconditions:

- UC-02 provides an unexpired browser session. UC-11/UC-12 implement `/account/settings` and its existing profile/password panels.
- UC-07 provides `/checkout`, its location options endpoint, and immutable quoted/ordered address snapshots.
- The shared response envelope applies. Profile location, account identity, saved addresses, and checkout snapshots are distinct data.

Postconditions:

- Success: The selected address slot is saved in full and its revision advances. The other address slot and profile revision are unchanged.
- Failure: A rejected save changes no fields in either slot. Unknown transport outcomes require a fresh read before another save decision.
- Checkout reuse copies values into an editable checkout draft. Saving an account address alone never updates an open quote, placed order, primary email, or account verification.

Main Flow:

1. The customer opens `/account/settings`; the frontend resolves the current session using UC-02.
2. The frontend reads saved addresses and supported location options, then renders Billing Address and Shipping Address as independent forms.
3. The customer completes or edits one form: first/last name, optional company, street address, country, region/state, city, postal code, email, and phone.
4. The customer selects that form's `SAVE CHANGES`. The frontend submits only its complete address and loaded slot revision.
5. The backend validates the authenticated account, slot, revision, field values, and location hierarchy, then saves the selected slot as one business operation.
6. The API returns HTTP 200 with the saved slot. The frontend replaces only that form's saved/draft values and displays its success message.
7. The customer may independently edit/save the other slot, or use saved values during a later checkout.

Alternative Flow:

A.1 — First saved address

- A missing slot is `{revision: 0, address: null}`. Show an empty form with `No saved billing address.` or `No saved shipping address.`
- Do not populate Figma sample names or infer a shipping address from account profile location. First successful save creates that slot at revision 1.

A.2 — Independent drafts

- Saving billing does not submit, reset, or validate the shipping draft, and vice versa. The two slots may have the same address and still have independent revisions.
- Navigating away/reloading discards unsaved drafts. Show an unsaved-changes notice; there is no automatic save.
- Blank required fields cannot be used to delete a saved slot. There is no delete action in the inspected forms or this UC.

A.3 — Use saved billing at checkout

- For a signed-in customer, provide a supplementary `Use saved billing address` action when a saved billing slot exists. A guest can still complete UC-07 manually without signing in.
- Clicking it explicitly replaces the checkout billing-address draft with the saved eight address fields, and checkout contact.email/contact.phone with the saved billing email/phone.
- Label the action with `Replaces the current billing and contact fields.` It does not save an order or alter the account address.
- If checkout uses billing as delivery, the effective delivery address follows UC-07's existing rule. If separate delivery is already selected, its draft is unchanged.

A.4 — Use saved shipping at checkout

- `Use saved shipping address` copies its eight address fields into shippingAddress and selects shipToDifferentAddress=true. Label it with `Replaces the current shipping address; checkout contact details stay unchanged.`
- Saved shipping email/phone remain address-book contact metadata. UC-07 has only one order contact, so these two values are not copied or sent as an additional recipient contact.
- After either saved-address action, invalidate any existing checkout quote and obtain a new quote for the current complete form. A new explicit PLACE ORDER action remains required.
- These checkout actions are project supplements, not controls verified in the checkout Figma frame. They never appear enabled for a missing slot or an unresolved placement outcome.

A.5 — Checkout and later address edits

- Once values have been copied, they are a checkout draft snapshot. Later account edits do not silently overwrite that draft; checkout edits do not update saved addresses.
- Quotes and orders keep their submitted effective address/contact snapshots. UC-07's placement and UC-08's lookup rules remain unchanged.
- A change to a saved address email does not change the login email or the billing email needed to track an already placed order.

Exception Flow:

E.1 — Authentication ended

- Missing/expired session or an account no longer active/verified returns HTTP 401 UNAUTHENTICATED.
- In Settings, clear account/address state and return to `/sign-in`; do not replay drafts after login.
- At checkout, disable saved-address actions and clear cached account-address data. Manual guest checkout remains governed by UC-07. Deliberately copied draft values may remain as that checkout's input; they are not treated as a live authenticated account record.

E.2 — Invalid address

- Field-shape/format errors return HTTP 400 VALIDATION_ERROR. A well-formed location outside the fixture returns HTTP 422 ADDRESS_LOCATION_UNSUPPORTED.
- Preserve the affected draft for correction. No partial address or change to the other slot is saved.

E.3 — Slot changed elsewhere

- A stale expectedRevision returns HTTP 409 ADDRESS_CHANGED. Disable saving that slot and offer `Reload this address`.
- The deliberate reload fetches current addresses, replaces only the conflicted slot's draft/snapshot, and preserves an unsaved draft in the other form. Do not silently overwrite newer data or auto-resubmit the stale request.

E.4 — Service failure or uncertain save

- A failed read displays retry feedback, not an empty saved slot. Location-options failure disables saving until choices can be resolved.
- For a lost/malformed save response, show `We could not confirm the address update. Reload this address before trying again.` Disable that slot's save until reconciled through GET.
- A confirmed save followed by a failed refresh remains a confirmed save; do not report that it was rolled back. No automatic mutation retry is required.

UI Integration:

- Parent: `34_Dasboard_Setting`, node `478:17305`.
- Billing Address panel: node `493:12498`, desktop 480 × 860.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=493-12498
- Shipping Address panel: node `494:17004`, desktop 480 × 860. Its internal layer name is Billing Address, but its rendered heading is Shipping Address.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=494-17004
- Live metadata, design contexts, and rendered panel screenshots were inspected on 2026-09-19. No frozen dataset, responsive frames, or separately designed error states are claimed.

| Observed element in each panel | Integration |
| --- | --- |
| First Name / Last Name | firstName / lastName |
| Company Name (Optional) | company, nullable |
| Address | addressLine |
| Country / Region/State / City | Dependent location selectors |
| Zip Code | postalCode |
| Email / Phone Number | Saved address contact metadata |
| SAVE CHANGES | Save only this panel's slot |

- Replace UC-11's disabled address areas with these working forms. Retain UC-11's profile and UC-12's password forms on the same route with independent submissions.
- Preserve side-by-side desktop panels, Public Sans, light borders (#E4E7E9), orange actions (#FA8232), and the shared Settings navigation.
- Use actual saved data, not the source's Bangladesh/Dhaka and sample personal details. The supported fixture remains the US/California locations declared for UC-07.
- Empty, conflict, pending, and error states are project supplements. No Delete, Copy Billing to Shipping, or extra address-card page is inferred from these panels.
- A password change signs the customer out. Extend UC-12's unsaved-profile guard to dirty address forms: `Save or discard your settings changes first; changing your password will sign you out.` Reloading is the existing discard path.
- The sidebar Cards & Address destination remains separately scoped; this UC implements the settings forms, not stored payment cards or that full destination page.

API Endpoint:

| Method and path | Purpose |
| --- | --- |
| `GET /api/v1/account/addresses` | Read the authenticated customer's two saved slots |
| `PUT /api/v1/account/addresses/:type` | Save one complete billing or shipping slot |
| `GET /api/v1/checkout/options` | Reuse UC-07's country/region/city fixture; unchanged contract |

Request Body:

GET endpoints have no body/query parameters. PUT type is exactly `billing` or `shipping`; it accepts:

```json
{
  "expectedRevision": 0,
  "address": {
    "firstName": "Alex",
    "lastName": "Nguyen",
    "company": null,
    "addressLine": "123 Example Street",
    "countryCode": "US",
    "regionCode": "CA",
    "cityCode": "SAN_FRANCISCO",
    "postalCode": "94105",
    "email": "customer@example.com",
    "phone": "+14155550123"
  }
}
```

- All keys are required. Reject unknown keys/query parameters, invalid type values, and non-object/null address values in PUT. The session determines the account; no account ID is accepted.
- expectedRevision is a nonnegative JSON integer belonging to the selected slot, not the profile revision or other slot revision.
- firstName/lastName: trimmed, 1–100 Unicode code points each. company: null or trimmed 1–100 code points. addressLine: trimmed, 1–200 code points.
- countryCode/regionCode/cityCode: strings of 1–40 uppercase ASCII letters or underscores. Membership and parent-child relationships must match the options fixture: US > CA > SAN_FRANCISCO or LOS_ANGELES.
- postalCode contains exactly five ASCII digits. email is trimmed/lowercased, valid format, maximum 254 characters. phone is a plus sign followed by 8–15 ASCII digits, first digit nonzero.
- Blank optional company becomes null. All other address values are required; partial saved addresses are not supported.
- Checkout copies only the eight fields firstName, lastName, company, addressLine, countryCode, regionCode, cityCode, postalCode into UC-07's address objects. Its contact mapping is explicitly defined in A.3/A.4; do not send this ten-field saved-address object unchanged to the quote API.

Successful Response:

GET — HTTP 200:

```json
{
  "success": true,
  "message": "Saved addresses retrieved.",
  "data": {
    "billing": {
      "revision": 1,
      "address": {
        "firstName": "Alex",
        "lastName": "Nguyen",
        "company": null,
        "addressLine": "123 Example Street",
        "countryCode": "US",
        "regionCode": "CA",
        "cityCode": "SAN_FRANCISCO",
        "postalCode": "94105",
        "email": "customer@example.com",
        "phone": "+14155550123"
      }
    },
    "shipping": {"revision": 0, "address": null}
  }
}
```

PUT — HTTP 200:

```json
{
  "success": true,
  "message": "Billing address saved.",
  "data": {
    "type": "billing",
    "revision": 1,
    "address": {
      "firstName": "Alex",
      "lastName": "Nguyen",
      "company": null,
      "addressLine": "123 Example Street",
      "countryCode": "US",
      "regionCode": "CA",
      "cityCode": "SAN_FRANCISCO",
      "postalCode": "94105",
      "email": "customer@example.com",
      "phone": "+14155550123"
    }
  }
}
```

- Shipping PUT uses type `shipping` and message `Shipping address saved.` with the same address schema.
- All keys shown are required. Stored addresses use normalized request values. Each slot starts at revision 0/address null; each accepted PUT increases only its revision by one, including accepted unchanged values.
- Reads/rejected saves do not advance revisions. GET returns both current slots consistently; PUT returns only the saved slot so it cannot overwrite an unrelated frontend draft.
- Account addresses persist across login sessions. They have no cart-style seven-day expiry and are not deleted on password change. This UC adds no account deletion/retention workflow.
- No authentication token or primary-account-identity update appears in these responses.

Error Response:

Use the shared envelope without data. timestamp is generated in UTC; path is the actual endpoint pathname.

```json
{
  "success": false,
  "statusCode": 409,
  "code": "ADDRESS_CHANGED",
  "message": "This address changed elsewhere. Reload it before saving again.",
  "timestamp": "2026-09-19T10:00:00.000Z",
  "path": "/api/v1/account/addresses/billing"
}
```

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-19T10:00:00.000Z",
  "path": "/api/v1/account/addresses/shipping",
  "errors": {"address.postalCode": ["Postal code must contain exactly five digits."]}
}
```

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | `Please correct the highlighted fields.` |
| 401 | UNAUTHENTICATED | `You must sign in to continue.` |
| 409 | ADDRESS_CHANGED | `This address changed elsewhere. Reload it before saving again.` |
| 422 | ADDRESS_LOCATION_UNSUPPORTED | `This location is outside the supported address area.` |
| 503 | ADDRESS_SERVICE_UNAVAILABLE | `Saved addresses are temporarily unavailable. Please try again later.` |
| 500 | INTERNAL_ERROR | `Unable to complete your request. Please try again later.` |

- Optional errors appears only for VALIDATION_ERROR, mapping request paths such as address.email or expectedRevision to nonempty message arrays. Body-level validation may omit it.
- Missing saved slots are successful null values, not 404 errors. The options endpoint retains UC-07's response/error contract and path.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement address read/save endpoints in NestJS against the existing authenticated account.

- Maintain exactly two independently versioned slots per account. Reuse UC-07's field semantics and location source without merging addresses into the UC-11 profile object.
- Validate the entire selected address, compare its revision, and persist it as one business outcome. Stale concurrent writes cannot overwrite a newer slot; billing/shipping saves do not conflict merely because the other slot changed.
- Resolve the target account from the current active, verified session. Saving another contact email does not grant a login identity or change account verification.
- Keep account addresses separate from order/quote snapshots, browser cart ownership, and profile location. Checkout consumes copied values through its existing request contract, not a mutable saved-address reference.
- Reads/saves do not renew the eight-hour session, send email, invoke an address-validation provider, or create payment-card records.

### Frontend UI Context

Implement both inspected panels inside the existing React/TypeScript/Tailwind Settings page.

- Use separate form states, buttons, field errors, loading status, and success feedback for billing and shipping. A button never submits its neighboring form.
- Populate country/region/city selectors from the shared options hierarchy. Changing a parent clears incompatible descendants; preserve meaningful required-field feedback.
- Enable each save only for a loaded, changed, valid draft with resolved options and no pending/uncertain save for that slot.
- Keep profile/password behavior intact, with the shared dirty-settings guard before password change. No duplicate page, delete action, or address picker modal is introduced.
- Add the two explicitly labeled saved-address actions to signed-in checkout as project supplements, without changing the guest flow or making address storage mandatory for purchase.

### Frontend Logic and API Context

- On settings entry, resolve the session and load addresses/options. Maintain independent saved snapshots, revisions, drafts, and conflict states for both slots.
- Submit one slot's complete address and revision. Replace only that slot on success; preserve the other form's unsaved values and profile draft.
- Reconciliation/reload may use the combined GET, but only the requested conflicted slot's draft is replaced. Do not overwrite a dirty neighboring form with a background response.
- Load saved addresses at checkout only for an authenticated customer. No automatic prefill occurs; explicit user actions copy the defined values into the draft and invalidate its quote.
- Disable address-copy actions during quote placement or an unresolved placement result. In-progress order reconciliation follows UC-07 before any new quote/edit workflow resumes.
- Ignore responses from an obsolete account/session. If saved-address loading fails at checkout, show retry feedback for those actions while retaining manual checkout input.

### Validation and Error-Handling Context

- Enforce complete address schema, location relationships, contact syntax, and independent revisions on the server. Client validation does not establish address deliverability.
- Distinguish invalid fields, unsupported fixture locations, stale slots, missing authentication, and service failure. An unavailable service must not appear as confirmed missing addresses.
- Preserve drafts after explicit correctable rejection; after unknown outcomes require a fresh read and deliberate continuation rather than an automatic PUT retry.
- For network failures display `Unable to connect. Please check your connection and try again.` For malformed reads display `Unable to load saved addresses. Please try again.`
- Never apply a shipping-contact email to UC-07's order contact implicitly, overwrite a placed order, change profile revision, or associate guest orders with an account through address saving.
- Success feedback confirms only the selected saved-address change. Checkout placement still requires its own valid quote and explicit PLACE ORDER action.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
