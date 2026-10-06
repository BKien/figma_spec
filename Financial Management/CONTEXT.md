# Financial Management

Personal financial tracking for an account holder's recorded accounts, cash flows, obligations and targets.

## Language

**Account holder**:
A person who owns an application identity and the financial records associated with it.
_Avoid_: Customer, financial account, bank account.

**Financial account**:
A manually tracked account at a financial institution, described by its account number, type and current recorded balance.
_Avoid_: Application identity, connected bank feed, credit facility.

**Recorded balance**:
The account holder's latest tracked amount for a financial account, incorporating completed cash flows and manual reconciliations.
_Avoid_: Net savings, goal progress, verified bank balance.

**Balance reconciliation**:
A deliberate correction to a recorded balance, rather than income or spending.
_Avoid_: Revenue transaction, expense transaction.

**Transaction**:
A recorded cash-flow entry for one financial account with a date, positive amount magnitude and revenue or expense direction.
_Avoid_: Bank transfer, bill payment, balance reconciliation.

**Completed transaction**:
A cash-flow entry counted as realized activity. Pending and failed entries remain recorded activity without realized cash flow.
_Avoid_: Any transaction, scheduled payment.

**Revenue**:
A completed incoming cash flow when used in financial totals; as a transaction direction it also labels pending or failed incoming entries.
_Avoid_: Balance deposit correction, savings.

**Expense**:
A completed outgoing cash flow when used in financial totals; as a transaction direction it also labels pending or failed outgoing entries.
_Avoid_: Spending limit, balance withdrawal correction.

**Category**:
A classification shared by transaction records and expense-limit goals. Its identity is distinct from its display name.
_Avoid_: Subcategory, merchant.

**Bill**:
A recorded payment obligation with a due date and optional last-charge date.
_Avoid_: Transaction, executed payment.

**Due cycle**:
The bill obligation represented by a particular due date.
_Avoid_: Calendar month, recurring payment schedule.

**Saving goal**:
A target for net completed cash flow over a stated interval.
_Avoid_: Financial account balance, deposit target.

**Expense-limit goal**:
A spending threshold for one category over a stated interval.
_Avoid_: Savings target, bill.

**Goal progress**:
The cash-flow measure for a goal over the intersection of its interval and the reporting month.
_Avoid_: Lifetime goal balance, total balance.

**Net savings**:
Completed revenue minus completed expenses for a reporting period, including negative outcomes.
_Avoid_: Savings account balance, total assets.

**Reporting month**:
A calendar month used to attribute transactions by their recorded date.
_Avoid_: Rolling thirty-day window, creation month.
