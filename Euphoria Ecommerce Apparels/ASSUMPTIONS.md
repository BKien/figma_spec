# Assumption Register

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
