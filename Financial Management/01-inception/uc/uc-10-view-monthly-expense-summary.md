---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-10
uc_name: "View Monthly Expense Summary"
---

# UC-10: View Monthly Expense Summary

## Functional Use-Case Specification

### Use Case ID

UC-10

### Use Case Name

View Monthly Expense Summary

### Description

Compare monthly spending in the current reporting year.

### Actor(s)

Primary: Account holder. Supporting: application client and application service.

### Priority

High.

### Trigger

The user opens the Expenses page.

### Pre-Condition(s)

PRE-1: The application view is open in the client.

### Post-Condition(s)

POST-1: On success, the client displays the monthly expense chart.

POST-2: On failure, the client displays a recovery message in the current view.

### Basic Flow

1. The user opens the Expenses page.
2. The client requests the monthly expense summary.
3. The system returns monthly totals.
4. The client displays the expense comparison chart.

### Alternative Flow

AF-1: Display No Monthly Spending

3a: The system returns an empty monthly result.

3b: The client displays a chart with no recorded spending.

### Exception Flow

EF-1: Monthly Expense Operation Error

3c: The system returns an operation error.

3d: The client displays the error message and keeps the current view open.

3e: The actor revises the interaction or retries the request.

EF-2: Monthly Expense Authentication Rejected

3f: The system returns a rejected authentication context.

3g: The client presents the login entry point.

### Related UI

- Product-source UI descriptions: [Use cases rows 221-239](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A221:B239). No Figma node identifier was supplied.

### Related API IDs

- [API-EXPENSE-SUMMARY](../api/API-EXPENSE-SUMMARY.md)

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

class ExpenseChart {
  +months: Sequence(ExpenseMonth)
  +build(summary: ExpenseSummaryResult): ExpenseChart
}

class ExpenseMonth {
  +month: Integer
  +totalExpense: Real
}

class ExpenseService {
  +summary(ctx: RequestContext): ExpenseSummaryResult
}

class ExpenseSummaryResult {
  +success: Boolean
  +year: Integer
  +months: Sequence(ExpenseMonth)
}

class Numeric {
  +{static} round2(x: Real): Real
}

class RequestContext {
  +userId: Integer
  +authenticated: Boolean
  +today: CalendarDate
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
ExpenseChart --> ExpenseMonth : months
ExpenseSummaryResult --> ExpenseMonth : months
RequestContext --> CalendarDate : today
Transaction --> CalendarDate : date
Transaction --> TransactionType : type
Transaction --> TransactionStatus : status

@enduml
~~~

## Business Rules

~~~text
BR-EXPENSE-SUMMARY-01 - Authenticated Context
Source: Product source
context ExpenseService::summary(ctx: RequestContext): ExpenseSummaryResult
pre BR_EXPENSE_SUMMARY_01_AuthenticatedContext:
  ctx.authenticated and User.allInstances()->exists(u | u.id = ctx.userId)
~~~

~~~text
BR-EXPENSE-SUMMARY-02 - Reporting Year
Source: Product source
Note: today is resolved once per request in Asia/Saigon, independent of host timezone.
context ExpenseService::summary(ctx: RequestContext): ExpenseSummaryResult
post BR_EXPENSE_SUMMARY_02_ReportingYear:
  result.success implies result.year = ctx.today.year
~~~

~~~text
BR-EXPENSE-SUMMARY-03 - Exact Month Coverage
Source: Assumption
context ExpenseService::summary(ctx: RequestContext): ExpenseSummaryResult
post BR_EXPENSE_SUMMARY_03_ExactMonthCoverage:
  result.success implies result.months->collect(month)->asSet() = Transaction.allInstances()->select(t | Account.allInstances()->exists(a | a.id = t.accountId and a.userId = ctx.userId) and t.status = TransactionStatus::Complete and t.type = TransactionType::Expense and t.date.year = ctx.today.year)->collect(t | t.date.month)->asSet()
~~~

~~~text
BR-EXPENSE-SUMMARY-04 - Month Total
Source: Assumption
context ExpenseService::summary(ctx: RequestContext): ExpenseSummaryResult
post BR_EXPENSE_SUMMARY_04_MonthTotal:
  result.months->forAll(m | m.totalExpense = Numeric::round2(Transaction.allInstances()->select(t | Account.allInstances()->exists(a | a.id = t.accountId and a.userId = ctx.userId) and t.status = TransactionStatus::Complete and t.type = TransactionType::Expense and t.date.year = ctx.today.year and t.date.month = m.month)->collect(amount)->sum()))
~~~

~~~text
BR-EXPENSE-SUMMARY-05 - Month Uniqueness
Source: Product source
context ExpenseService::summary(ctx: RequestContext): ExpenseSummaryResult
post BR_EXPENSE_SUMMARY_05_MonthUniqueness:
  result.months->isUnique(month)
~~~

~~~text
BR-EXPENSE-SUMMARY-06 - Month Order
Source: Product source
context ExpenseService::summary(ctx: RequestContext): ExpenseSummaryResult
post BR_EXPENSE_SUMMARY_06_MonthOrder:
  result.months->size() <= 1 or Sequence{1..result.months->size()-1}->forAll(i | result.months->at(i).month < result.months->at(i+1).month)
~~~

~~~text
BR-EXPENSE-SUMMARY-07 - Valid Months
Source: Product source
context ExpenseService::summary(ctx: RequestContext): ExpenseSummaryResult
post BR_EXPENSE_SUMMARY_07_ValidMonths:
  result.months->forAll(m | m.month >= 1 and m.month <= 12)
~~~

~~~text
BR-EXPENSE-SUMMARY-08 - Transaction Unchanged
Source: Product source
Note: Equality denotes the complete persistent value snapshot, including every property, not object identity alone.
context ExpenseService::summary(ctx: RequestContext): ExpenseSummaryResult
post BR_EXPENSE_SUMMARY_08_TransactionUnchanged:
  Transaction.allInstances()->collect(e | Tuple{id = e.id, accountId = e.accountId, categoryId = e.categoryId, date = e.date, type = e.type, status = e.status, description = e.description, shopName = e.shopName, paymentMethod = e.paymentMethod, amount = e.amount, receiptId = e.receiptId, createdAt = e.createdAt})->asSet() = Transaction.allInstances()@pre->collect(e | Tuple{id = e.id@pre, accountId = e.accountId@pre, categoryId = e.categoryId@pre, date = e.date@pre, type = e.type@pre, status = e.status@pre, description = e.description@pre, shopName = e.shopName@pre, paymentMethod = e.paymentMethod@pre, amount = e.amount@pre, receiptId = e.receiptId@pre, createdAt = e.createdAt@pre})->asSet()
~~~

~~~text
BR-EXPENSE-SUMMARY-09 - Account Unchanged
Source: Product source
Note: Equality denotes the complete persistent value snapshot, including every property, not object identity alone.
context ExpenseService::summary(ctx: RequestContext): ExpenseSummaryResult
post BR_EXPENSE_SUMMARY_09_AccountUnchanged:
  Account.allInstances()->collect(e | Tuple{id = e.id, userId = e.userId, bankName = e.bankName, accountType = e.accountType, branchName = e.branchName, numberCiphertext = e.numberCiphertext, numberFingerprint = e.numberFingerprint, last4 = e.last4, balance = e.balance, version = e.version, createdAt = e.createdAt})->asSet() = Account.allInstances()@pre->collect(e | Tuple{id = e.id@pre, userId = e.userId@pre, bankName = e.bankName@pre, accountType = e.accountType@pre, branchName = e.branchName@pre, numberCiphertext = e.numberCiphertext@pre, numberFingerprint = e.numberFingerprint@pre, last4 = e.last4@pre, balance = e.balance@pre, version = e.version@pre, createdAt = e.createdAt@pre})->asSet()
~~~

~~~text
BR-EXPENSE-SUMMARY-10 - Chart Normalization
Source: Assumption
Note: Handles an empty summary as well as partial months; charts show every calendar month.
context ExpenseChart::build(summary: ExpenseSummaryResult): ExpenseChart
post BR_EXPENSE_SUMMARY_10_ChartNormalization:
  result.months->size() = 12 and Sequence{1..12}->forAll(i | result.months->at(i).month = i and result.months->at(i).totalExpense = (if summary.months->exists(m | m.month = i) then summary.months->any(m | m.month = i).totalExpense else 0 endif))
~~~
