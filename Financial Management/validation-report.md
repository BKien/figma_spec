# Validation Report

Validated on 2026-09-30, Asia/Saigon. This report concerns a specification package, not an implemented application.

## New-Package Gates

- The repository package validator passes for Financial Management: 18 use cases, 18 sequential API contracts and 183 individually numbered OCL rules. Every use case contains a complete local PlantUML declaration set and at least seven rules.
- Additional package checks verify source SHA-256 checksums, all supplied endpoint identities, source-entry coverage, public enums, typed UML dependency closure, resource version fields, persistence concepts and local document links. Results: [package-checks.json](evidence/package-checks.json).
- `schema.dbml` compiles with pinned `@dbml/cli@9.1.1` using the MySQL dialect. Generated output: [schema.mysql.sql](evidence/schema.mysql.sql).
- Commands, exit codes and saved output are available in [validation-results.json](evidence/validation-results.json) and [package-validator log](evidence/package-validation.txt).

## Repository Gate

Repository-wide validation fails in the pre-existing `100ms Video Conferencing and Live Streaming` package before reaching later packages. Its source manifest omits the current contract marker, and its use cases refer to a shared model and lack local UML vocabulary required by the current repository skill. The new Financial Management package passes its own gate. The repository-wide failure is recorded in [repository-validation.txt](evidence/repository-validation.txt); no existing specification package was rewritten by this import.

## Reviewed Edge Scenarios

The following are consistency checks of the written rules and transaction boundaries. They are not runtime tests of a backend or results from a formal OCL engine.

| Scenario | Expected result in the reviewed specification | Supporting constraints |
| --- | --- | --- |
| Two Complete expenses of 60 use the same version of an account with balance 100 | One can commit; the other encounters a version conflict. Retrying with the latest version cannot spend the remaining 40 as an expense of 60. | UC-04 version, funds, balance effect and atomic rollback |
| A Pending expense of 200 is recorded against balance 100 | Entry remains visible; balance stays 100; expense and savings reports exclude it. Account version advances. | UC-04 status-aware balance effect; UC-10/11/13/16 Complete-only totals |
| A Complete revenue would exceed DECIMAL(18,2) balance range | Reject before storage, with no inserted transaction or changed balance. | UC-04 revenue balance range and failure rollback |
| Account edit and expense creation submit the same old version | At most one succeeds; account reload supplies the next version before resubmission. | UC-04 and UC-08 version checks under account lock |
| An opening balance of 1000 is later corrected to 900 with no cash-flow entry | Account balance is 900; correction is audited; net savings and expenses remain zero. | UC-06 opening balance; UC-08 audit correction; cash-flow report eligibility |
| Quick edit opens a masked account card | Client loads the owner detail before displaying full-number edit fields. | UC-08 alternative flow; account-detail API |
| Two accounts share a number across different holders | Allowed; same holder and same exact number conflict. Leading zeros are retained. | UC-06/08 owner-scoped fingerprint uniqueness; schema unique index |
| An account is deleted | Its transactions and adjustments disappear atomically; unrelated accounts remain; derived totals use remaining records. | UC-09 frame and deletion constraints; cascade relationships |
| No eligible monthly expenses exist | API returns data: []; chart represents Jan–Dec with zeros. | UC-10 exact sparse coverage and chart normalization |
| Two category IDs have the same display name | Separate identity-based groups and goal progress; labels do not merge totals. | UC-11 group identity; UC-13 category progress |
| January category breakdown compares to previous month | Uses December of the preceding year. Previous zero/current positive retains the source's 100 percent convention. | UC-11 previous-month helper and comparison rule |
| Bill is due today or in exactly 30 calendar days | Included when its current due cycle is uncharged. Day +31 and overdue bills are excluded. | UC-12 inclusive window and charge-cycle exclusion |
| Existing goal ends on a requested goal's start date | Inclusive overlap rejects a same-scope interval. Different expense categories may overlap. | UC-14 overlap predicate and serialized creation |
| Concurrent same-scope goal creation requests overlap | User-row lock serializes check and insertion; the later request detects the committed overlap. | UC-14 transactional conflict handling; schema notes |
| Goal target is updated with extra significant fractional digits or a stale version | Reject without changing the goal; type, category and dates remain unchanged. | UC-15 precision, version and failure frame |
| Saving progress is negative | Return the negative cash-flow value without clamping. | UC-13 saving calculation |
| Savings year is omitted | Use the request's reporting year and compare with exactly the preceding year. | UC-16 resolved-year and series rules |
| Savings year is 2025abc, NaN or out of range | Malformed syntax or invalid domain input receives HTTP 400; no silent year substitution. | Common wire contract; UC-16 year bounds |
| Another holder's account or goal ID is requested | Return the same 404 public outcome as an absent resource. | Reviewed resource boundary; owning-use-case preconditions and API errors |

## Limits

No backend, browser interaction, live Figma node, MySQL server, PlantUML renderer or formal OCL runtime was executed. The compiled SQL establishes DBML syntax and dialect output; supplementary `persistence.sql` constraints have been inspected but not applied to a live database. UML dependency checks establish declarations and local closure, not full formal OCL typechecking. Requirements for row locks, conditional version updates and decimal validation must be implemented before the specified guarantees hold.

The source snapshots contain connector-returned cell values rather than native workbook bytes; formula definitions, formatting, comments and revision history are outside the snapshot. SHA-256 verification protects the saved snapshots from subsequent drift.
