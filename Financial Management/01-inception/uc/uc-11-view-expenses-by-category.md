---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-11
uc_name: "View Expenses by Category"
---

# UC-11: View Expenses by Category

## Functional Use-Case Specification

### Use Case ID

UC-11

### Use Case Name

View Expenses by Category

### Description

Review spending distribution and the previous-month comparison.

### Actor(s)

Primary: Account holder. Supporting: application client and application service.

### Priority

High.

### Trigger

The user opens Expenses and selects a month.

### Pre-Condition(s)

PRE-1: The application view is open in the client.

### Post-Condition(s)

POST-1: On success, the client displays the returned category breakdown or no-data view.
POST-2: On failure, the client displays a recovery message in the current view.

### Basic Flow

1. The user opens Expenses and selects a month.
2. The client requests the category breakdown.
3. The system returns category groups and details.
4. The client displays category totals, comparison values, and transaction details.

### Alternative Flow

AF-1:

1. The system returns an empty breakdown.
2. The client displays the no-data state.

### Exception Flow

EF-1:

1. The system returns an operation error.
2. The client displays the error message and keeps the current view open.
3. The actor revises the interaction or retries the request.

EF-2:

1. The system returns a rejected authentication context.
2. The client presents the login entry point.

### Related UI

- Product-source UI descriptions: [Use cases rows 241-258](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A241:B258). No Figma node identifier was supplied.

### Related API IDs

- [API-EXPENSE-BREAKDOWN](../api/api-expense-breakdown.md)

### Notes

See [source mapping](../../coverage-report.md), [review decisions](../../consistency-review.md), and [assumptions](../../ASSUMPTIONS.md). The supplied spreadsheet is specification evidence; no running application or Figma interaction was verified.

## UML Model

~~~plantuml
@startuml
hide empty members

class Account {
  +id: Integer
  +userId: Integer
}

class BreakdownQuery {
  +month: CalendarDate
}

class BreakdownResult {
  +success: Boolean
  +groups: Sequence(ExpenseGroup)
}

class CalendarDate {
  +year: Integer
  +month: Integer
  +ordinal: Integer
  +{static} previousMonth(date: CalendarDate): CalendarDate
}

class Category {
  +id: Integer
  +name: String
}

class ExpenseGroup {
  +categoryId: Integer [0..1]
  +category: String
  +total: Real
  +changePercent: Real [0..1]
  +details: Sequence(Transaction)
}

class ExpenseService {
  +breakdown(ctx: RequestContext, cmd: BreakdownQuery): BreakdownResult
}

class Numeric {
  +{static} round2(x: Real): Real
}

class RequestContext {
  +userId: Integer
  +authenticated: Boolean
}

class Text {
  +{static} trim(s: String): String
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

BreakdownQuery --> CalendarDate : month
BreakdownResult --> ExpenseGroup : groups
ExpenseGroup --> Transaction : details
Transaction --> CalendarDate : date
Transaction --> TransactionType : type
Transaction --> TransactionStatus : status

note right of CalendarDate
  ordinal is the calendar-day index in Asia/Saigon.
end note

@enduml
~~~

## Business Rules

~~~ocl
-- BR-UC-11-01
-- Source: Product source
context ExpenseService::breakdown(ctx: RequestContext, cmd: BreakdownQuery): BreakdownResult
pre BR_UC_11_01_AuthenticatedContext:
  ctx.authenticated and User.allInstances()->exists(u | u.id = ctx.userId)
~~~

~~~ocl
-- BR-UC-11-02
-- Source: Assumption
context ExpenseService::breakdown(ctx: RequestContext, cmd: BreakdownQuery): BreakdownResult
post BR_UC_11_02_ExactCoverage:
  result.success implies result.groups->collect(g | g.details)->flatten()->collect(id)->asSet() = Transaction.allInstances()->select(t | Account.allInstances()->exists(a | a.id = t.accountId and a.userId = ctx.userId) and t.status = TransactionStatus::Complete and t.type = TransactionType::Expense and t.date.year = cmd.month.year and t.date.month = cmd.month.month)->collect(id)->asSet()
~~~

~~~ocl
-- BR-UC-11-03
-- Source: Assumption
context ExpenseService::breakdown(ctx: RequestContext, cmd: BreakdownQuery): BreakdownResult
post BR_UC_11_03_OneGroupPerCategory:
  result.groups->isUnique(categoryId) and result.groups->collect(g | g.details)->flatten()->isUnique(id)
~~~

~~~ocl
-- BR-UC-11-04
-- Source: Product source
context ExpenseService::breakdown(ctx: RequestContext, cmd: BreakdownQuery): BreakdownResult
post BR_UC_11_04_GroupMembership:
  result.groups->forAll(g | g.details->notEmpty() and g.details->forAll(t | t.categoryId = g.categoryId))
~~~

~~~ocl
-- BR-UC-11-05
-- Source: Product source
context ExpenseService::breakdown(ctx: RequestContext, cmd: BreakdownQuery): BreakdownResult
post BR_UC_11_05_CategoryLabel:
  result.groups->forAll(g | if g.categoryId.oclIsUndefined() then g.category = 'Uncategorized' else let c : Category = Category.allInstances()->any(c | c.id = g.categoryId) in if c.oclIsUndefined() or Text::trim(c.name).size() = 0 then g.category = 'Unknown' else g.category = Text::trim(c.name) endif endif)
~~~

~~~ocl
-- BR-UC-11-06
-- Source: Product source
context ExpenseService::breakdown(ctx: RequestContext, cmd: BreakdownQuery): BreakdownResult
post BR_UC_11_06_Totals:
  result.groups->forAll(g | g.total = Numeric::round2(g.details->collect(amount)->sum()))
~~~

~~~ocl
-- BR-UC-11-07
-- Source: Assumption
-- January compares with December of the preceding year; category identity, not display name, is the grouping key.
context ExpenseService::breakdown(ctx: RequestContext, cmd: BreakdownQuery): BreakdownResult
post BR_UC_11_07_PreviousComparison:
  result.groups->forAll(g | let previous : Real = Transaction.allInstances()->select(t | Account.allInstances()->exists(a | a.id = t.accountId and a.userId = ctx.userId) and t.status = TransactionStatus::Complete and t.type = TransactionType::Expense and t.date.year = CalendarDate::previousMonth(cmd.month).year and t.date.month = CalendarDate::previousMonth(cmd.month).month and t.categoryId = g.categoryId)->collect(amount)->sum() in if previous = 0 then g.changePercent = (if g.total > 0 then 100 else null endif) else g.changePercent = Numeric::round2(((g.total - previous) / previous) * 100) endif)
~~~

~~~ocl
-- BR-UC-11-08
-- Source: Assumption
context ExpenseService::breakdown(ctx: RequestContext, cmd: BreakdownQuery): BreakdownResult
post BR_UC_11_08_GroupOrder:
  result.groups->size() <= 1 or Sequence{1..result.groups->size()-1}->forAll(i | let a : ExpenseGroup = result.groups->at(i) in let b : ExpenseGroup = result.groups->at(i+1) in a.total > b.total or (a.total = b.total and (a.categoryId.oclIsUndefined() or (not b.categoryId.oclIsUndefined() and a.categoryId < b.categoryId))))
~~~

~~~ocl
-- BR-UC-11-09
-- Source: Assumption
context ExpenseService::breakdown(ctx: RequestContext, cmd: BreakdownQuery): BreakdownResult
post BR_UC_11_09_DetailOrder:
  result.groups->forAll(g | g.details->size() <= 1 or Sequence{1..g.details->size()-1}->forAll(i | g.details->at(i).date.ordinal < g.details->at(i+1).date.ordinal or (g.details->at(i).date.ordinal = g.details->at(i+1).date.ordinal and g.details->at(i).id < g.details->at(i+1).id)))
~~~

~~~ocl
-- BR-UC-11-10
-- Source: Product source
-- Equality denotes the complete persistent value snapshot, including every property, not object identity alone.
context ExpenseService::breakdown(ctx: RequestContext, cmd: BreakdownQuery): BreakdownResult
post BR_UC_11_10_TransactionUnchanged:
  Transaction.allInstances()->collect(e | Tuple{id = e.id, accountId = e.accountId, categoryId = e.categoryId, date = e.date, type = e.type, status = e.status, description = e.description, shopName = e.shopName, paymentMethod = e.paymentMethod, amount = e.amount, receiptId = e.receiptId, createdAt = e.createdAt})->asSet() = Transaction.allInstances()@pre->collect(e | Tuple{id = e.id@pre, accountId = e.accountId@pre, categoryId = e.categoryId@pre, date = e.date@pre, type = e.type@pre, status = e.status@pre, description = e.description@pre, shopName = e.shopName@pre, paymentMethod = e.paymentMethod@pre, amount = e.amount@pre, receiptId = e.receiptId@pre, createdAt = e.createdAt@pre})->asSet()
~~~
