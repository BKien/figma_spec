# Assumptions and Reviewed Product Decisions

The spreadsheet establishes observable product behavior but also contains inconsistent policy and implementation claims. The user authorized corrections. Entries below are explicit product choices for this package, not facts about an existing running service. Rules changed or added on that basis use Source: Assumption; inherited rules use Source: Product source.

| ID | Decision | Affected use cases / contracts |
| --- | --- | --- |
| A-01 | All monetary records use one configured currency, VND, with two-decimal exact arithmetic and DECIMAL(18,2) bounds. Additional significant decimal places and overflowing resulting balances are rejected before persistence. No multi-currency conversion is inferred. | UC-04, UC-06, UC-08, UC-10–16; numeric API fields and schema |
| A-02 | Reporting dates use Asia/Saigon and are captured once per request. Transaction date is a date-only value. Creation timestamps use UTC and are persisted. | UC-04, UC-10–16 |
| A-03 | Only Complete transactions affect account balances or report totals; Pending/Failed remain visible in history. No status transition operation is inferred. | UC-04, UC-10, UC-11, UC-13, UC-16 |
| A-04 | Manually recording a financial account does not require a bank deposit, a branch for specific types, or proof of investment capacity. All five source type labels remain allowed. Credit Card and Loan are descriptive labels; debt, overdraft, interest and credit-limit semantics are outside scope. | UC-06, UC-08 |
| A-05 | Account creation and replacement updates accept an optional branch; omission means null. Account numbers are digit strings retaining leading zeros. Full number is available through detail only, and stored as authenticated ciphertext plus keyed fingerprint. | UC-05–08; account contracts |
| A-06 | Every account mutation compares a client version with the locked resource and increments version on success. A manual balance change creates an audit correction excluded from cash-flow reports. Version conflicts receive HTTP 409. | UC-04, UC-08, UC-09; expected_version / If-Match |
| A-07 | Account deletion is permanent and removes its transactions and balance corrections, as the source requests. Reports are recalculated from remaining records; no historical report snapshot is promised. | UC-09, reporting use cases |
| A-08 | Goal target updates also compare resource versions and preserve type, category and dates. Goal creation serializes inclusive interval overlap checks using the user's database row. Conflict receives HTTP 409. | UC-14, UC-15 |
| A-09 | Missing and other-user resources both produce HTTP 404 for account and goal operations. Login credential failures have one HTTP 401 outcome. | UC-02, UC-04, UC-07–09, UC-15 |
| A-10 | Monthly expense APIs retain sparse months from the source. The chart always fills Jan–Dec with zeros, including completely empty input. Breakdown no-data returns HTTP 200 with an empty array. | UC-10, UC-11 |
| A-11 | Savings year is strictly parsed; omitted year uses the reporting year, while malformed or out-of-range input is rejected. A numeric prefix such as 2025abc is no longer accepted. The retained domain range is 1900–2100; the prior-year comparison may therefore reach 1899. | UC-16; savings query |
| A-12 | Pagination limit defaults to 10 and has a reviewed upper bound of 100; offset defaults to zero. Type defaults to All. Date ties use transaction ID descending. Changing filter resets the first page. | UC-03, UC-17 |
| A-13 | Category catalogue is global and read-only. IDs are identities; duplicate display names can exist. Category choices sort by ID. Category detail presentation is proposed from the source API, and not claimed as a verified design screen. | UC-18; category APIs |
| A-14 | Public success envelopes are normalized to success/message/data while retaining source payload spelling. Errors use success/message/error.code. New version, category identity and recent transaction identity fields complete the response mappings. | All APIs |
| A-15 | Application clients keep access tokens in memory for this boundary; source localStorage persistence and the misleading Keep me signed in behavior are removed. Reload requires login. Persistent sessions, refresh/revocation, logout and OAuth remain outside scope. | UC-01, UC-02 |
| A-16 | Text fields are trimmed and bounded by declared persistence lengths; Unicode NFC is applied to registration names. Password rules and bcrypt cost 10 are retained from the supplied source. | UC-01, UC-04, UC-06, UC-08 |
| A-17 | No request replay guarantee is introduced. A mutation is one attempt; the client reloads after an uncertain outcome before creating a replacement operation. Version comparison prevents a successful account/goal mutation from being replayed with its old version. | UC-04, UC-08, UC-09, UC-15 |
| A-18 | Complete cash flows cannot have a future transaction date. Future Pending/Failed entries remain history records without balance/report effects. | UC-04 |

The source's arbitrary initial-deposit and investment-capacity thresholds are deliberately removed rather than transferred into assumptions. The category-detail interaction is the only proposed screen behavior; the filter goal is extracted from existing source interaction. See [review decisions](consistency-review.md) for source row anchors and [coverage](coverage-report.md) for unsupported flows.

## 2026-10-07 — Template completion decisions

These decisions complete the utility contracts under the user-authorized template update; they are repository specification choices rather than claims about a deployed implementation.

- CalendarDate.ordinal uses 1970-01-01 as its fixed Gregorian epoch. Existing Asia/Saigon reporting dates, UTC creation timestamps, exact decimal arithmetic, and bcrypt behavior remain the established package decisions.
- Text.lower is locale-independent Unicode lowercase. Text.email accepts bounded ASCII dot-atom addresses and rejects whitespace, quoted local parts, and malformed dotted domains.
- The utility catalog includes operations declared in active local UML. Wire date parsing and account encryption remain prose-level transport/storage conventions rather than additional undeclared utility operations.
