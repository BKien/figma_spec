# Coverage and Traceability

18 normalized actor goals, 18 API contracts and 183 separately numbered OCL rules. All 17 supplied use-case entries and all 18 supplied endpoints are accounted for. This is a product-source audit, not a Figma screen audit.

## Use Case Mapping

| Source entry | Normalized specification | Source rows | Classification |
| --- | --- | --- | --- |
| UC-01 | [UC-01 — Register an Account](01-inception/uc/uc-01-register-an-account.md) | 5–24 | Source-supported |
| UC-02 | [UC-02 — Log In](01-inception/uc/uc-02-log-in.md) | 26–43 | Source-supported |
| UC-03 | [UC-03 — View Transaction History](01-inception/uc/uc-03-view-transaction-history.md) | 45–62 | Source-supported |
| UC-04 | [UC-04 — Create a Transaction](01-inception/uc/uc-04-create-a-transaction.md) | 64–81 | Source-supported |
| UC-05 | [UC-05 — View Bank Accounts](01-inception/uc/uc-05-view-bank-accounts.md) | 83–104 | Source-supported |
| UC-06 | [UC-06 — Add a Bank Account](01-inception/uc/uc-06-add-a-bank-account.md) | 106–131 | Source-supported |
| UC-07 | [UC-07 — View Bank Account Details](01-inception/uc/uc-07-view-bank-account-details.md) | 133–152 | Source-supported |
| UC-08 | [UC-08 — Edit a Bank Account](01-inception/uc/uc-08-edit-a-bank-account.md) | 155–200 | Source-supported |
| UC-08a quick edit | UC-08 alternative flow | 182–200 | Variant merged; no behavior removed |
| UC-09 | [UC-09 — Delete a Bank Account](01-inception/uc/uc-09-delete-a-bank-account.md) | 202–219 | Source-supported |
| UC-10 | [UC-10 — View Monthly Expense Summary](01-inception/uc/uc-10-view-monthly-expense-summary.md) | 221–239 | Source-supported |
| UC-11 | [UC-11 — View Expenses by Category](01-inception/uc/uc-11-view-expenses-by-category.md) | 241–258 | Source-supported |
| UC-12 | [UC-12 — View Upcoming Bills](01-inception/uc/uc-12-view-upcoming-bills.md) | 260–277 | Source-supported |
| UC-13 | [UC-13 — View Financial Goals](01-inception/uc/uc-13-view-financial-goals.md) | 279–297 | Source-supported |
| UC-14 | [UC-14 — Create a Financial Goal](01-inception/uc/uc-14-create-a-financial-goal.md) | 299–316 | Source-supported |
| UC-15 | [UC-15 — Adjust a Financial Goal](01-inception/uc/uc-15-adjust-a-financial-goal.md) | 318–334 | Source-supported |
| UC-16 | [UC-16 — View Savings Summary](01-inception/uc/uc-16-view-savings-summary.md) | 336–355 | Source-supported |
| UC-03 filter interaction | [UC-17 — Filter Transaction History](01-inception/uc/uc-17-filter-transaction-history.md) | 45–62 | Extracted source-supported goal |
| UC-04/UC-14 category selection + category APIs | [UC-18 — Choose a Category](01-inception/uc/uc-18-choose-a-category.md) | 64–81 | Source-supported selection; proposed detail presentation |

UC-18 also draws on goal form rows 299–316 and API rows 173–205. The category detail presentation is a reviewed addition supported by the supplied endpoint; no separate verified screen is claimed. UC-17 specifies the first page after a filter change; later pages remain UC-03.

## Source Rule Families

| Source scope | Original rule identifiers preserved in snapshot | Normalized rule coverage | Disposition |
| --- | --- | --- | --- |
| Source UC-01 | BR-REG-01, BR-REG-02, BR-REG-04, BR-REG-05, BR-REG-06, BR-REG-03, BR-REG-07, BR-REG-08, BR-REG-09, BR-REG-10, BR-REG-11 | BR-REGISTER-ACCOUNT-01 through BR-REGISTER-ACCOUNT-14 | Retained and formalized; refinements recorded in review |
| Source UC-02 | BR-LOG-01, BR-LOG-02, BR-LOG-03, BR-LOG-04, BR-LOG-05, BR-LOG-06 | BR-LOGIN-01 through BR-LOGIN-09 | Retained and formalized; refinements recorded in review |
| Source UC-03 | BR-TXN-01, BR-TXN-02, BR-TXN-03, BR-TXN-04, BR-TXN-05, BR-TXN-06, BR-TXN-07 | BR-TRANSACTION-HISTORY-01 through BR-TRANSACTION-HISTORY-10 | Retained and formalized; refinements recorded in review |
| Source UC-04 | BR-TXN-08, BR-TXN-09, BR-TXN-10, BR-TXN-11, BR-TXN-12, BR-TXN-13, BR-TXN-14, BR-TXN-15, BR-TXN-01 | BR-CREATE-TRANSACTION-01 through BR-CREATE-TRANSACTION-13 | Revised for Complete-only cash-flow accounting and exact mappings |
| Source UC-05 | BR-ACC-01, BR-ACC-02, BR-ACC-03, BR-ACC-04, BR-ACC-05, BR-ACC-06 | BR-BANK-ACCOUNTS-01 through BR-BANK-ACCOUNTS-08 | Retained and formalized; refinements recorded in review |
| Source UC-06 | BR-ACC-07, BR-ACC-08, BR-ACC-09, BR-ACC-10, BR-ACC-11, BR-ACC-12, BR-ACC-13, BR-ACC-14, BR-ACC-15, BR-ACC-16 | BR-ADD-ACCOUNT-01 through BR-ADD-ACCOUNT-10 | Revised; branch/deposit/capacity restrictions removed and concurrency/storage clarified |
| Source UC-07 | BR-ACC-15, BR-ACC-16, BR-ACC-17 | BR-ACCOUNT-DETAIL-01 through BR-ACCOUNT-DETAIL-09 | Retained and formalized; refinements recorded in review |
| Source UC-08 | BR-ACC-19, BR-ACC-20, BR-ACC-21, BR-ACC-22, BR-ACC-23, BR-ACC-24, BR-ACC-25, BR-ACC-26 | BR-EDIT-ACCOUNT-01 through BR-EDIT-ACCOUNT-14 | Revised; branch/deposit/capacity restrictions removed and concurrency/storage clarified |
| Source UC-09 | BR-ACC-27, BR-ACC-28 | BR-DELETE-ACCOUNT-01 through BR-DELETE-ACCOUNT-09 | Retained and formalized; refinements recorded in review |
| Source UC-10 | BR-EXP-01, BR-EXP-02, BR-EXP-03, BR-EXP-04, BR-EXP-05, BR-EXP-06, BR-EXP-07 | BR-EXPENSE-SUMMARY-01 through BR-EXPENSE-SUMMARY-10 | Revised for Complete-only cash-flow accounting and exact mappings |
| Source UC-11 | BR-EXP-CAT-01, BR-EXP-CAT-02, BR-EXP-CAT-03, BR-EXP-CAT-04, BR-EXP-CAT-05, BR-EXP-CAT-06, BR-EXP-CAT-07 | BR-CATEGORY-EXPENSES-01 through BR-CATEGORY-EXPENSES-10 | Revised for Complete-only cash-flow accounting and exact mappings |
| Source UC-12 | BR-BILL-UP-01, BR-BILL-UP-02, BR-BILL-UP-03, BR-BILL-UP-04, BR-BILL-UP-05, BR-BILL-UP-06 | BR-UPCOMING-BILLS-01 through BR-UPCOMING-BILLS-10 | Retained and formalized; refinements recorded in review |
| Source UC-13 | BR-GOAL-VIEW-01, BR-GOAL-VIEW-02, BR-GOAL-VIEW-03, BR-GOAL-VIEW-04, BR-GOAL-VIEW-05, BR-GOAL-VIEW-06, BR-GOAL-VIEW-07 | BR-FINANCIAL-GOALS-01 through BR-FINANCIAL-GOALS-10 | Revised for Complete-only cash-flow accounting and exact mappings |
| Source UC-14 | BR-GOAL-CREATE-01, BR-GOAL-CREATE-02, BR-GOAL-CREATE-03, BR-GOAL-CREATE-04, BR-GOAL-CREATE-05, BR-GOAL-CREATE-06, BR-GOAL-CREATE-07 | BR-CREATE-GOAL-01 through BR-CREATE-GOAL-09 | Retained and formalized; refinements recorded in review |
| Source UC-15 | BR-GOAL-12, BR-GOAL-13, BR-GOAL-14, BR-GOAL-15, BR-GOAL-16, BR-GOAL-17 | BR-ADJUST-GOAL-01 through BR-ADJUST-GOAL-08 | Retained and formalized; refinements recorded in review |
| Source UC-16 | BR-SAV-01, BR-SAV-02, BR-SAV-03, BR-SAV-04, BR-SAV-05, BR-SAV-06, BR-SAV-07, BR-SAV-08, BR-SAV-09 | BR-SAVINGS-SUMMARY-01 through BR-SAVINGS-SUMMARY-11 | Revised for Complete-only cash-flow accounting and exact mappings |

Source identifiers can be duplicated, embedded in multi-context blocks, or present only as prose. This table maps policy families rather than claiming one-to-one identity. Source variants and original rule text remain available under source/. Removed predicates and added assumptions have explicit decisions in [review](consistency-review.md) and [assumptions](ASSUMPTIONS.md).

## Endpoint Mapping

| Source API / start row | Normalized contract | Use cases |
| --- | --- | --- |
| API-AUTH-LOGIN, row 3 | [API-AUTH-LOGIN](01-inception/api/API-AUTH-LOGIN.md) | UC-02 |
| API-AUTH-REGISTER, row 21 | [API-AUTH-REGISTER](01-inception/api/API-AUTH-REGISTER.md) | UC-01 |
| API-ACCOUNT-LIST, row 39 | [API-ACCOUNT-LIST](01-inception/api/API-ACCOUNT-LIST.md) | UC-04, UC-05 |
| API-ACCOUNT-CREATE, row 55 | [API-ACCOUNT-CREATE](01-inception/api/API-ACCOUNT-CREATE.md) | UC-06 |
| API-ACCOUNT-DETAIL, row 74 | [API-ACCOUNT-DETAIL](01-inception/api/API-ACCOUNT-DETAIL.md) | UC-07, UC-08 |
| API-ACCOUNT-UPDATE, row 95 | [API-ACCOUNT-UPDATE](01-inception/api/API-ACCOUNT-UPDATE.md) | UC-08 |
| API-ACCOUNT-DELETE, row 116 | [API-ACCOUNT-DELETE](01-inception/api/API-ACCOUNT-DELETE.md) | UC-09 |
| API-TRANSACTION-LIST, row 136 | [API-TRANSACTION-LIST](01-inception/api/API-TRANSACTION-LIST.md) | UC-03, UC-17 |
| API-TRANSACTION-CREATE, row 155 | [API-TRANSACTION-CREATE](01-inception/api/API-TRANSACTION-CREATE.md) | UC-04 |
| API-CATEGORY-LIST, row 173 | [API-CATEGORY-LIST](01-inception/api/API-CATEGORY-LIST.md) | UC-04, UC-14, UC-18 |
| API-CATEGORY-DETAIL, row 188 | [API-CATEGORY-DETAIL](01-inception/api/API-CATEGORY-DETAIL.md) | UC-18 |
| API-EXPENSE-SUMMARY, row 206 | [API-EXPENSE-SUMMARY](01-inception/api/API-EXPENSE-SUMMARY.md) | UC-10 |
| API-EXPENSE-BREAKDOWN, row 222 | [API-EXPENSE-BREAKDOWN](01-inception/api/API-EXPENSE-BREAKDOWN.md) | UC-11 |
| API-BILL-LIST, row 242 | [API-BILL-LIST](01-inception/api/API-BILL-LIST.md) | UC-12 |
| API-GOAL-LIST, row 258 | [API-GOAL-LIST](01-inception/api/API-GOAL-LIST.md) | UC-13, UC-15 |
| API-GOAL-CREATE, row 274 | [API-GOAL-CREATE](01-inception/api/API-GOAL-CREATE.md) | UC-14 |
| API-GOAL-UPDATE, row 291 | [API-GOAL-UPDATE](01-inception/api/API-GOAL-UPDATE.md) | UC-15 |
| API-SAVINGS-SUMMARY, row 311 | [API-SAVINGS-SUMMARY](01-inception/api/API-SAVINGS-SUMMARY.md) | UC-16 |

## Persistence Mapping

| Local persistent concept | MySQL table | Principal relationships |
| --- | --- | --- |
| User | users | Owner of accounts, goals and bills |
| Account | accounts | user_id → users.id |
| Transaction | transactions | account_id → accounts.id; optional category_id → categories.id |
| Category | categories | Global catalogue; referenced by transactions and goals |
| Bill | bills | user_id → users.id |
| Goal | goals | user_id → users.id; optional category_id → categories.id |
| BalanceAdjustment | balance_adjustments | (account_id, user_id) → accounts.(id, user_id) |

Commands, queries, contexts, helpers, projected views, chart objects and result envelopes are transient concepts and have no separate persistence table. Goal progress and report totals are derived. Raw passwords, confirmations, JWTs and full account numbers have no plaintext columns.

## Wire and Local Vocabulary Mapping

| Local member | Database column | Wire field spelling |
| --- | --- | --- |
| User.id / fullName | users.id / full_name | data.user.id / fullName |
| Account.id / userId | accounts.id / user_id | id / user_id |
| Account.bankName / accountType / branchName | bank_name / account_type / branch_name | bank_name / account_type / branch_name |
| Account.numberCiphertext / last4 | number_ciphertext / last4 | account_number_full in detail; account_number_last_4 in projections |
| Transaction.id / accountId | transactions.id / account_id | transaction_id / account_id in history; transactionId / accountId in create |
| Transaction.date / description | transaction_date / item_description | transaction_date / item_description in history; transactionDate / itemDescription in create; date / description in recent activity |
| Transaction.shopName / paymentMethod / categoryId | shop_name / payment_method / category_id | shop_name / payment_method in history; shopName / paymentMethod in create; category_id in create |
| Category.id / name | categories.id / name | category_id / category_name |
| BillView.id / description | bills.id / item_description | billId / itemDescription |
| BillView.dueDate / lastChargeDate / logoUrl | due_date / last_charge_date / logo_url | dueDate / lastChargeDate / logoUrl |
| Goal.id / goalType / categoryId | goals.id / goal_type / category_id | goal_id / goal_type / category_id |
| Goal.startDate / endDate / targetAmount | start_date / end_date / target_amount | start_date / end_date / target_amount |
| GoalView.progress | Derived; no column | target_achieved for saving; current_expense for expense limits |
| CalendarDate | DATE column where persistent | YYYY-MM-DD string |
| ExpenseMonth.month | Derived; no column | Jan through Dec month labels |
| SavingsMonth.month | Derived; no column | 01 through 12 two-digit month strings |
| AccountType::Credit_Card | Credit Card enum literal | Credit Card |
| Command.expectedVersion | Compares accounts.version or goals.version | expected_version; quoted If-Match for account delete |

Fields in this table are shorthand for the endpoint-specific payload paths documented in the API contracts. Protected number storage is mapped through the local vault; the plaintext number is not a database column.

## Unsupported and Unverified Scope

| Candidate | Status | Boundary |
| --- | --- | --- |
| Figma pages and node IDs | Missing evidence | No Figma source was supplied. |
| Google login/sign-up | Excluded by source | No OAuth flow or contract. |
| Password recovery/change | Excluded by source | No supported recovery lifecycle. |
| Persistent sign-in, refresh, logout or revocation | Unsupported | Only registration and login are supplied. |
| Pay Now / execute bill payment | Excluded by source | Upcoming bills is read-only. |
| Create or update bills | Unsupported | Bill population is external to this package. |
| Bank synchronization / account transfer / multi-currency | Unsupported | Accounts and transactions are manually tracked. |
| Transaction update or status transition | Unsupported | No supplied endpoint or continuation. |
| Category administration | Unsupported | Catalogue is read-only. |
| Goal deletion or schedule changes | Unsupported | Source adjustment is target-only. |
| Historical report preservation after deletion | Unsupported | Source permanently deletes transactions. |
| Runtime implementation compliance | Unverified | No application code or database was supplied. |

## Validation Scope

[Validation report](validation-report.md) distinguishes new-package structural checks, DBML compilation, source preservation, semantic scenario review and repository-wide failures in pre-existing packages. None of these establishes a live product implementation.
