# Scope and Coverage Report

This package is complete for the selected, evidence-supported scope below. It is not a claim that every screen or interaction in the source has been fully specified. A visible form, action, and matching outcome state establish support; prototype wiring is not claimed. Service contracts and exception recovery are proposed implementation details with explicit assumptions.

## Supported goals

| Use case | Actor goal | Figma node IDs | Evidence | Status | BRs |
| --- | --- | --- | --- | --- | --- |
| UC-01 | Explore the storefront | 85:1544 | Desktop; metadata | Supported | 7 |
| UC-02 | Browse products by category | 64:33 | Desktop; metadata | Supported | 7 |
| UC-03 | Filter the product listing | 64:33 | Desktop; metadata | Supported | 8 |
| UC-04 | Change product listing order | 64:33 | Desktop; metadata | Supported | 7 |
| UC-05 | View product details | 1:2 | Desktop; metadata | Supported | 10 |
| UC-06 | Review the cart | 181:393, 190:423 | Desktop; metadata | Supported | 8 |
| UC-07 | Enter billing details and review checkout | 181:393, 235:1056 | Desktop; canvas and metadata | Supported | 9 |
| UC-08 | Place a cash-on-delivery order | 235:1056, 273:839, 181:393 | Desktop; canvas and metadata | Supported | 11 |
| UC-09 | Request a password reset email | 245:588, 270:721 | Desktop; metadata | Supported | 7 |
| UC-10 | Resend the password reset email | 270:721, 245:588 | Desktop; metadata | Supported | 7 |
| UC-11 | View contact details | 275:1168 | Desktop; metadata | Supported | 7 |
| UC-12 | View saved addresses | 275:1168 | Desktop; metadata | Supported | 7 |
| UC-13 | Add a delivery address | 279:1003, 275:1168 | Desktop; canvas and metadata | Supported | 7 |
| UC-14 | View saved wishlist products | 290:855, 299:1027 | Desktop; metadata | Supported | 7 |
| UC-15 | Rediscover recently viewed products | 299:1027 | Desktop; metadata | Supported | 7 |
| UC-16 | View order history | 290:1372 | Desktop; metadata | Supported | 7 |
| UC-17 | Filter orders by status | 290:1372 | Desktop; metadata | Supported | 7 |
| UC-18 | View order details and progress | 295:949 | Desktop; metadata | Supported | 8 |

## Partial and missing goals

These rows do not authorize implementation of additional workflows.

| Candidate | Goal or state | Node IDs | Status | Gap |
| --- | --- | --- | --- | --- |
| C-12 | Sign in | 178:381 | Partial | Form exists; complete instance labels and authentication success/failure behavior were not inspected |
| C-13 | Sign up and newsletter consent | 167:524 | Partial | Form and consent text exist; completion and email-verification relationship are unverified |
| C-14 | Complete password reset | 270:792, 250:710, 270:721 | Partial | Link-based reset and separate code verification both appear; token/code purpose, expiry and final outcome are not established |
| C-15 | Card or PayPal checkout | 235:1056 | Partial | Payment entry is visible; provider handoff, challenge, return, failure and settlement screens are absent from the inspected boundary |
| C-16 | Different shipping address; save checkout information | 235:1056 | Partial | Controls exist; expanded form and persistence outcome were not inspected |
| C-17 | Add/update/remove cart lines | 1:2, 181:393 | Partial | Add to cart and quantity/component structures are visible; complete rendered action labels and resulting interactions remain unverified |
| C-18 | Apply coupon | 181:393 | Partial | Apply Coupon exists; applied/rejected coupon states and its connection to savings are not established |
| C-19 | Edit contact details or password; sign out | 275:1168 | Partial | Change and Sign out labels exist; forms, confirmations and outcomes are missing |
| C-20 | Edit/remove addresses or set a default from a card | 275:1168 | Partial | Entry actions exist; edit and confirmation states were not inspected; default selection during Add Address is covered by UC-13 |
| C-21 | Add/remove wishlist entries or transfer to cart | 290:855, 299:1027 | Partial | Row components are present; instance actions and transition outcomes were not inspected |
| C-22 | Read or write comments and questions | 1:2 | Partial | Tabs and counts exist; tab content, submission and feedback are missing |
| C-23 | Search by text | Shared header instances | Partial | Search affordance exists; query submission and search result states are not established |
| C-24 | Cancel order, return goods, request refund | 290:1372; footer links | Missing | A Cancelled list tab and links are not a cancellation/return/refund workflow |
| C-25 | Contact support, FAQ, legal pages, size guide | Footer links; 1:2 | Missing | Destination content and interaction outcomes were not inspected |
| C-26 | Recover from unknown route | 274:1030 | Partial | 404 illustration and message exist; recovery button instance text was not inspected |
| C-27 | Mobile layout, overlays, style tokens | 105:179 enumerated only | Missing | No inspected mobile frame; Styleguide and hidden/overlay variants unavailable within current connector quota |

## Design discrepancies

| ID | Observation | Treatment |
| --- | --- | --- |
| D-01 | Dollar amounts coexist with rupee text in the product-list price table | Currency configuration is provisional in UC-07; no currency conversion is inferred |
| D-02 | Cart displayed line amounts 29, 119 and 123 do not explain subtotal 513 | Illustrative values are not calculation tests; normative arithmetic lives in UC-06/UC-18 |
| D-03 | Checkout shows subtotal 513, savings -30, shipping -5 and total 478, while the delivery section shows a positive charge of 5 | Preserve the discrepancy in this record; do not copy contradictory signs into the contract |
| D-04 | Order detail shows total 143 with two displayed line amounts of 29 | Treat as fixture inconsistency; snapshots and totals are governed by UC-18 |
| D-05 | Product rating header shows 120 comments while the tab badge shows 21 | The proposed response has one commentCount; UI labels should use that response consistently |
| D-06 | Reset screens mention an emailed link and separately a code verification screen | Only email-request acknowledgement is specified; reset completion remains partial |
| D-07 | Reset form displays an email-not-found message | UC-09 deliberately proposes a neutral acknowledgement; this is a documented privacy assumption that differs from the mockup |
| D-08 | Text contains Paypol, Additional fess, comfirm, and generic Label/h1 placeholder names | Preserve raw evidence; use clear terms in specification prose; do not claim all instance labels were read |

## Evidence confidence

High: source identity, two page names, 20 top-level frame IDs and dimensions, metadata-visible text, browser-observed checkout/address labels.

Moderate: association of separate forms and result screens into the supported goals. These associations use matching content and purpose; prototype edges were not inspected.

Proposed: endpoints, database entities, all domain policy, authentication boundary, error protocol, and recovery presentation. These are not facts recovered from a server implementation.

Validation results are recorded in [validation report](validation-report.md).
