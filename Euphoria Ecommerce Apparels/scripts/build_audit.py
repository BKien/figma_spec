from pathlib import Path
import xml.etree.ElementTree as ET
import json

ROOT=Path(__file__).resolve().parents[1]
KEY='WcpUgAYaQJA4J00rMaMgj8'
def write(path,text):
    (ROOT/path).write_text(text.strip()+'\n',encoding='utf-8')
tree=ET.parse(ROOT/'evidence/page-0.xml').getroot()
screens=[dict(n.attrib, parent='0:1',visibility='not exposed by metadata',type=n.tag) for n in tree]
(ROOT/'evidence/screen-inventory.json').write_text(json.dumps(screens,indent=2),encoding='utf-8')
rows='\n'.join(f'| [{n["name"]}](https://www.figma.com/design/{KEY}/Euphoria?node-id={n["id"].replace(":","-")}) | `{n["id"]}` | {n["width"]} x {n["height"]} |' for n in screens)
write('FIGMA.md',f'''# Figma Source Manifest

- Package: Euphoria Ecommerce Apparels.
- Scope: the user-supplied copy of the Euphoria apparel ecommerce website template.
- Design URL: https://www.figma.com/design/{KEY}/Euphoria---Ecommerce--Apparels--Website-Template--Community---Copy-
- Design file key: `{KEY}`.
- Original Community listing: https://www.figma.com/community/file/1250348068101895773/euphoria-ecommerce-apparels-website-template
- Community resource ID: `1250348068101895773`; distinct from the design file key.
- Original template publisher: Jhanvi Shah.
- Audit date: 2026-09-24.
- Document pages enumerated: `0:1` Webpage and `105:179` Styleguide.
- Inspected node boundary: metadata subtree of Webpage `0:1`, plus browser inspection of Checkout `235:1056` and Add Address `279:1003`.
- Source revision: unavailable; this is a dated observation, not a pinned Figma version.

## Evidence and limits

The Figma connector successfully returned the Webpage node hierarchy, screen names, dimensions, positions, and text-layer names. The full returned XML is saved in [page-0.xml](evidence/page-0.xml). The [screen inventory](evidence/screen-inventory.json) is derived from that XML. All listed screens are top-level frames parented by `0:1`.

Visibility flags, complete instance text overrides, prototype transitions, interactive behavior, and hidden-state completeness were not exposed by this metadata. Text-layer names are evidence of design content; they are not a full export of rendered characters. The connector reached its Starter-plan call limit before Styleguide inspection and additional screenshots. Browser canvas inspection supplied readable views of the checkout and address fields and action labels. Styleguide was enumerated but not inspected. No mobile frame was found among the 20 top-level Webpage frames; this does not establish that no mobile design exists elsewhere.

The earlier Community promotional image is contextual evidence only. It is not the source for node-level requirements in this package. No design nodes were changed.

## Screen inventory

| Screen | Node ID | Dimensions |
| --- | --- | --- |
{rows}

## Browser observation record

Checkout: First Name, Last Name, Country / Region, Company Name, Street Address, Apt/suite/unit, City, State, Postal Code, Phone; Continue to delivery; Save my information for a faster checkout; Same as Billing address / Use a different shipping address; delivery charge; Credit Card; Cash on delivery; Paypol; Pay Now. The card area shows card number, name, expiration, and security-code fields. Provider processing and results were not observed.

Add Address: the same address identity fields, Delivery Instruction, default shipping and default billing checkboxes, Save, and Cancel. The address book screen provides the corresponding saved-address display. No prototype edge was verified between them.

## Source chronology

The original Community link required browser authentication to open a design. The user then supplied this design copy. The connector initially required reauthentication, which the user completed; page enumeration and Webpage metadata subsequently succeeded. Later connector requests reported the Starter-plan call limit. These limits are recorded rather than treated as evidence of absent features.
''')

write('coverage-report.md','''# Scope and Coverage Report

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
''')

write('CONTEXT.md','''# Euphoria Apparel Shopping

The customer-facing domain of the inspected Euphoria website. Terms describe the supported shopping, account-reading, and cash-on-delivery order experience.

## Language

**Shopper**: A person exploring apparel or reviewing a shopping cart.
_Avoid_: User when the shopping role matters.

**Customer**: The account holder associated with personal information, saved addresses, wishlist entries, and orders.
_Avoid_: Account as a synonym for the person.

**Product**: An apparel design presented with a title, description, imagery, and category.
_Avoid_: SKU, variant.

**Variant**: A particular size-and-color choice for a product.
_Avoid_: Product when a selected apparel option matters.

**Category**: A named grouping used to discover apparel.
_Avoid_: Dress style, which is a separate filter concept.

**Cart**: The shopper's current collection of selected apparel lines before an order is placed.
_Avoid_: Order, checkout.

**Cart line**: A selected variant and its quantity within a cart.
_Avoid_: Product when quantity and chosen options matter.

**Checkout**: The interaction in which the shopper supplies address details, reviews the order summary, and submits the purchase.
_Avoid_: Payment as a synonym for the whole interaction.

**Order**: The recorded purchase presented in confirmation, order history, and order detail.
_Avoid_: Cart, transaction.

**Order line**: The apparel description, chosen options, quantity, and price recorded with an order.
_Avoid_: Current cart line.

**Cash on delivery**: The checkout payment choice labeled Cash on delivery in the design.
_Avoid_: PayPal, card payment.

**Billing address**: The address supplied for billing details.
_Avoid_: Delivery address when the billing role matters.

**Shipping address**: The address used for delivery of an order.
_Avoid_: Billing address unless the shopper selected the same address for both roles.

**Address book**: The collection of saved customer addresses with displayed shipping and billing defaults.
_Avoid_: Profile as a synonym for the collection.

**Wishlist**: The customer's saved product collection displayed in the Wishlist area.
_Avoid_: Cart.

**Recently viewed product**: A product displayed in the Recently Viewed section.
_Avoid_: Wishlist entry.

**Order event**: A dated progress entry shown with an order.
_Avoid_: Status when referring to an individual historical entry.

**Reset email request**: The request acknowledged by the Check Email screen.
_Avoid_: Password reset completion.
''')

write('ASSUMPTIONS.md','''# Assumption Register

The Figma source establishes interface evidence, not server policy. Every OCL block in this package is explicitly marked `Source: Assumption`. This register identifies decisions for review; their normative predicates and values appear only in the referenced OCL blocks.

| ID | Decision area | Normative location | Review note |
| --- | --- | --- | --- |
| A-01 | Published catalog selection, section sequences and recommendation order | UC-01, UC-02, UC-04 | No content-management or recommendation source was supplied |
| A-02 | Filter combination, default request values and product/variant distinction | UC-02, UC-03, UC-05 | Visible filters establish inputs; their matching semantics are proposed |
| A-03 | Personal-data access and session/CSRF context | UC-06, UC-07, UC-08, UC-11, UC-12, UC-13, UC-14, UC-15, UC-16, UC-18 | Authentication provisioning is outside the inspected complete flows |
| A-04 | Cart arithmetic and shipping estimate | UC-06 | Mockup totals conflict; see D-02 |
| A-05 | Currency, delivery charge and checkout arithmetic | UC-07 | Commercial configuration is provisional; see D-01 and D-03 |
| A-06 | Order creation, address snapshots, stock and retry behavior | UC-08 | The backend contract is proposed; no existing order service was inspected |
| A-07 | Reset email acknowledgement and delivery queue | UC-09, UC-10 | Neutral acknowledgement deliberately differs from email-not-found copy; completion is excluded |
| A-08 | Address field acceptance and default roles | UC-12, UC-13 | Required fields are informed by observed asterisks; semantics remain a proposed policy |
| A-09 | Wishlist and recently viewed response selection | UC-14, UC-15 | Collection mutation and view-event capture are excluded |
| A-10 | Order-tab membership and timeline presentation | UC-16, UC-17, UC-18 | Status maintenance and fulfillment operations are outside this package |

## Implementation assumptions

Routes, methods, wire names, response objects, error codes, and persistence structures are proposed interfaces, not existing Euphoria implementation facts. Responses have no pagination in this version; this is suitable for a bounded template implementation and requires review before a large catalog rollout. Error and retry presentation is proposed where the design does not show it.

The supported checkout scope is the Cash on delivery choice with Same as Billing address. Different-address expansion, saved-checkout preferences, card/PayPal processing, coupons, tax configuration, and guest account provisioning remain outside the frozen scope. No hidden payment gateway, cancellation service, email-verification sequence, or mobile behavior is presumed.

## Operational contract notes

The OCL constraints describe before/after states of application operations, not a particular transaction engine or executable implementation. Wire decimal strings and timestamps map to the modeled value types described in the shared model. SQL constraints support the model, while cross-row calculations and operation postconditions still require service implementation. DBML compilation does not prove those predicates.
''')

write('README.md','''# Euphoria Ecommerce Apparels — Functional Specification

An English specification package for the user-supplied Euphoria Figma copy, audited on 2026-09-24. It contains 18 supported use cases with 138 OCL business rules (7-11 per use case), 13 proposed API contracts, UML/OCL domain models, a DBML persistence schema, and node-level source traceability.

## Read first

1. [Scope and coverage](coverage-report.md): supported goals, partial/missing flows, and design discrepancies.
2. [Use cases](uc/README.md): observable activities and isolated domain constraints.
3. [API contracts](api/README.md): sequential wire contracts and reusable object definitions.
4. [Domain glossary](CONTEXT.md), [shared UML model](uc/shared-domain-model.md), and [database schema](schema.dbml).
5. [Assumptions](ASSUMPTIONS.md), [Figma source manifest](FIGMA.md), and [validation report](validation-report.md).

## Authoring requirements

Each use case contains at least seven distinct OCL business rules. Trigger, precondition, postcondition, basic-flow, alternative-flow and exception-flow prose describe observable interaction only. Rule identifiers, rule names, predicates, thresholds and policy explanations are isolated from those sections. The consistency checker enforces the count and scans for policy leakage; semantic review complements the scan.

## Functional boundary

Covered: storefront discovery; category browsing, filtering and sorting; product details; cart review; checkout review and COD order placement using the billing address for shipping; reset-email request and resend; contact details and address-book viewing; address creation; wishlist and recently viewed products; order history, status filtering, and order detail.

Partial flows are explicitly separated in the coverage report. This is not an implementation specification for authentication completion, card/PayPal processing, cart mutations, wishlist mutations, refunds, or mobile screens.

## Design fidelity

The audit obtained the Webpage hierarchy containing 20 desktop frames. Checkout and Add Address fields were additionally read from the browser canvas. Styleguide details, instance overrides, and prototype wiring were not fully accessible after the Figma connector reached its plan limit. Every policy is a labeled assumption; static sample prices and contradictory totals are not treated as business rules.

## Repository isolation

This directory is the sole specification boundary for file `WcpUgAYaQJA4J00rMaMgj8`. It uses no screen, API, or rule from the repository's other Figma packages. The original Community listing is provenance only. The source Figma file was not edited.
''')
print(f'Generated audit documents and inventory of {len(screens)} frames.')
