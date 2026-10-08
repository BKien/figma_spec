---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-16
uc_name: "View Savings Summary"
---

# UC-16: View Savings Summary

## Functional Use-Case Specification

### Use Case ID

UC-16

### Use Case Name

View Savings Summary

### Description

Compare monthly net savings across a selected year and the preceding year.

### Actor(s)

Primary: Account holder. Supporting: application client and application service.

### Priority

High.

### Trigger

The user opens the savings chart on Goals.

### Pre-Condition(s)

PRE-1: The application view is open in the client.

### Post-Condition(s)

POST-1: On success, the client displays the returned savings comparison series.

POST-2: On failure, the client displays a recovery message in the current view.

### Basic Flow

1. The user opens the savings chart on Goals.
2. The client requests the savings summary.
3. The system returns both yearly series.
4. The client displays the comparison chart.
5. The user selects a year.
6. The client requests and displays the returned series.

### Alternative Flow

AF-1: Inspect Savings with No Recorded Activity

3a: The system returns series with no recorded activity.

3b: The client displays the returned chart.

3c: The user points to a chart value.

3d: The client displays its month and amount tooltip.

### Exception Flow

EF-1: Savings Summary Operation Error

3e: The system returns an operation error.

3f: The client displays the error message and keeps the current view open.

3g: The actor revises the interaction or retries the request.

EF-2: Savings Summary Authentication Rejected

3h: The system returns a rejected authentication context.

3i: The client presents the login entry point.

### Related UI

- Product-source UI descriptions: [Use cases rows 336-355](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A336:B355). No Figma node identifier was supplied.

### Related API IDs

- [API-SAVINGS-SUMMARY](../api/API-SAVINGS-SUMMARY.md)

### Notes

See [source mapping](../../coverage-report.md), [review decisions](../../consistency-review.md), and [assumptions](../../ASSUMPTIONS.md). The supplied spreadsheet is specification evidence; no running application or Figma interaction was verified.

## UML Model

~~~plantuml
@startuml
hide empty members

class Account {
  +id: Integer
  +userId: Integer
  +bankName: String
  +accountType: AccountType
  +branchName: String [0..1]
  +numberCiphertext: String
  +numberFingerprint: String
  +last4: String
  +balance: Real
  +version: Integer
  +createdAt: String
}

enum AccountType {
  Checking
  Credit_Card
  Savings
  Investment
  Loan
}

class CalendarDate {
  +year: Integer
  +month: Integer
}

class Numeric {
  +{static} round2(x: Real): Real
}

class RequestContext {
  +userId: Integer
  +authenticated: Boolean
  +today: CalendarDate
}

class SavingsChart {
  +summary: SavingsResult
  +hover(series: String, month: Integer): SavingsTooltip
}

class SavingsMonth {
  +month: Integer
  +amount: Real
}

class SavingsQuery {
  +year: Integer [0..1]
}

class SavingsResult {
  +userId: Integer
  +year: Integer
  +thisYear: Sequence(SavingsMonth)
  +lastYear: Sequence(SavingsMonth)
}

class SavingsService {
  +summary(ctx: RequestContext, cmd: SavingsQuery): SavingsResult
}

class SavingsTooltip {
  +month: Integer
  +amount: Real
  +visible: Boolean
}

class Transaction {
  +id: Integer
  +accountId: Integer
  +categoryId: Integer [0..1]
  +date: CalendarDate
  +type: TransactionType
  +status: TransactionStatus
  +description: String
  +shopName: String
  +paymentMethod: String
  +amount: Real
  +receiptId: String [0..1]
  +createdAt: String
}

enum TransactionStatus {
  Complete
  Pending
  Failed
}

enum TransactionType {
  Revenue
  Expense
}

class User {
  +id: Integer
}

Account --> AccountType : accountType
RequestContext --> CalendarDate : today
SavingsChart --> SavingsResult : summary
SavingsResult --> SavingsMonth : thisYear
SavingsResult --> SavingsMonth : lastYear
Transaction --> CalendarDate : date
Transaction --> TransactionType : type
Transaction --> TransactionStatus : status

@enduml
~~~

## Business Rules

~~~text
BR-SAVINGS-SUMMARY-01 - Authenticated Context
Source: Product source
context SavingsService::summary(ctx: RequestContext, cmd: SavingsQuery): SavingsResult
pre BR_SAVINGS_SUMMARY_01_AuthenticatedContext:
  ctx.authenticated and User.allInstances()->exists(u | u.id = ctx.userId)
~~~

~~~text
BR-SAVINGS-SUMMARY-02 - Year Bounds
Source: Assumption
context SavingsService::summary(ctx: RequestContext, cmd: SavingsQuery): SavingsResult
pre BR_SAVINGS_SUMMARY_02_YearBounds:
  cmd.year.oclIsUndefined() or (cmd.year >= 1900 and cmd.year <= 2100)
~~~

~~~text
BR-SAVINGS-SUMMARY-03 - Resolved Year
Source: Assumption
context SavingsService::summary(ctx: RequestContext, cmd: SavingsQuery): SavingsResult
post BR_SAVINGS_SUMMARY_03_ResolvedYear:
  result.year = (if cmd.year.oclIsUndefined() then ctx.today.year else cmd.year endif)
~~~

~~~text
BR-SAVINGS-SUMMARY-04 - User Identity
Source: Product source
context SavingsService::summary(ctx: RequestContext, cmd: SavingsQuery): SavingsResult
post BR_SAVINGS_SUMMARY_04_UserIdentity:
  result.userId = ctx.userId
~~~

~~~text
BR-SAVINGS-SUMMARY-05 - Complete Series
Source: Product source
context SavingsService::summary(ctx: RequestContext, cmd: SavingsQuery): SavingsResult
post BR_SAVINGS_SUMMARY_05_CompleteSeries:
  result.thisYear->size() = 12 and result.lastYear->size() = 12
~~~

~~~text
BR-SAVINGS-SUMMARY-06 - Month Order
Source: Product source
context SavingsService::summary(ctx: RequestContext, cmd: SavingsQuery): SavingsResult
post BR_SAVINGS_SUMMARY_06_MonthOrder:
  Sequence{1..12}->forAll(i | result.thisYear->at(i).month = i and result.lastYear->at(i).month = i)
~~~

~~~text
BR-SAVINGS-SUMMARY-07 - This Year Net Savings
Source: Assumption
Note: Empty sums are zero; negative savings are retained, without clamping.
context SavingsService::summary(ctx: RequestContext, cmd: SavingsQuery): SavingsResult
post BR_SAVINGS_SUMMARY_07_ThisYearNetSavings:
  result.thisYear->forAll(m | let rows : Set(Transaction) = Transaction.allInstances()->select(t | Account.allInstances()->exists(a | a.id = t.accountId and a.userId = ctx.userId) and t.status = TransactionStatus::Complete and t.date.year = result.year and t.date.month = m.month)->asSet() in m.amount = Numeric::round2(rows->select(t | t.type = TransactionType::Revenue)->collect(amount)->sum() - rows->select(t | t.type = TransactionType::Expense)->collect(amount)->sum()))
~~~

~~~text
BR-SAVINGS-SUMMARY-08 - Previous Year Net Savings
Source: Assumption
Note: Empty sums are zero; negative savings are retained, without clamping.
context SavingsService::summary(ctx: RequestContext, cmd: SavingsQuery): SavingsResult
post BR_SAVINGS_SUMMARY_08_PreviousYearNetSavings:
  result.lastYear->forAll(m | let rows : Set(Transaction) = Transaction.allInstances()->select(t | Account.allInstances()->exists(a | a.id = t.accountId and a.userId = ctx.userId) and t.status = TransactionStatus::Complete and t.date.year = result.year - 1 and t.date.month = m.month)->asSet() in m.amount = Numeric::round2(rows->select(t | t.type = TransactionType::Revenue)->collect(amount)->sum() - rows->select(t | t.type = TransactionType::Expense)->collect(amount)->sum()))
~~~

~~~text
BR-SAVINGS-SUMMARY-09 - Transaction Unchanged
Source: Product source
Note: Equality denotes the complete persistent value snapshot, including every property, not object identity alone.
context SavingsService::summary(ctx: RequestContext, cmd: SavingsQuery): SavingsResult
post BR_SAVINGS_SUMMARY_09_TransactionUnchanged:
  Transaction.allInstances()->collect(e | Tuple{id = e.id, accountId = e.accountId, categoryId = e.categoryId, date = e.date, type = e.type, status = e.status, description = e.description, shopName = e.shopName, paymentMethod = e.paymentMethod, amount = e.amount, receiptId = e.receiptId, createdAt = e.createdAt})->asSet() = Transaction.allInstances()@pre->collect(e | Tuple{id = e.id@pre, accountId = e.accountId@pre, categoryId = e.categoryId@pre, date = e.date@pre, type = e.type@pre, status = e.status@pre, description = e.description@pre, shopName = e.shopName@pre, paymentMethod = e.paymentMethod@pre, amount = e.amount@pre, receiptId = e.receiptId@pre, createdAt = e.createdAt@pre})->asSet()
~~~

~~~text
BR-SAVINGS-SUMMARY-10 - Account Unchanged
Source: Product source
Note: Equality denotes the complete persistent value snapshot, including every property, not object identity alone.
context SavingsService::summary(ctx: RequestContext, cmd: SavingsQuery): SavingsResult
post BR_SAVINGS_SUMMARY_10_AccountUnchanged:
  Account.allInstances()->collect(e | Tuple{id = e.id, userId = e.userId, bankName = e.bankName, accountType = e.accountType, branchName = e.branchName, numberCiphertext = e.numberCiphertext, numberFingerprint = e.numberFingerprint, last4 = e.last4, balance = e.balance, version = e.version, createdAt = e.createdAt})->asSet() = Account.allInstances()@pre->collect(e | Tuple{id = e.id@pre, userId = e.userId@pre, bankName = e.bankName@pre, accountType = e.accountType@pre, branchName = e.branchName@pre, numberCiphertext = e.numberCiphertext@pre, numberFingerprint = e.numberFingerprint@pre, last4 = e.last4@pre, balance = e.balance@pre, version = e.version@pre, createdAt = e.createdAt@pre})->asSet()
~~~

~~~text
BR-SAVINGS-SUMMARY-11 - Tooltip Value
Source: Product source
Note: The caller supplies this_year or last_year and a rendered point; leaving the point hides the tooltip.
context SavingsChart::hover(series: String, month: Integer): SavingsTooltip
post BR_SAVINGS_SUMMARY_11_TooltipValue:
  let points : Sequence(SavingsMonth) = if series = 'this_year' then self.summary.thisYear else self.summary.lastYear endif in result.visible and points->one(p | p.month = month and result.month = p.month and result.amount = p.amount)
~~~
