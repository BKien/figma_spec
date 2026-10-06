---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-13
uc_name: "View Financial Goals"
---

# UC-13: View Financial Goals

## Functional Use-Case Specification

### Use Case ID

UC-13

### Use Case Name

View Financial Goals

### Description

Review saving progress and category spending limits.

### Actor(s)

Primary: Account holder. Supporting: application client and application service.

### Priority

High.

### Trigger

The user opens the Goals page.

### Pre-Condition(s)

PRE-1: The application view is open in the client.

### Post-Condition(s)

POST-1: On success, the client displays the returned goal cards or create-goal entry point.
POST-2: On failure, the client displays a recovery message in the current view.

### Basic Flow

1. The user opens the Goals page.
2. The client requests goals.
3. The system returns goal cards and progress values.
4. The client displays the saving goal and expense limit cards.

### Alternative Flow

AF-1:

1. The system returns no goal cards.
2. The client displays the create-goal entry point.

### Exception Flow

EF-1:

1. The system returns an operation error.
2. The client displays the error message and keeps the current view open.
3. The actor revises the interaction or retries the request.

EF-2:

1. The system returns a rejected authentication context.
2. The client presents the login entry point.

### Related UI

- Product-source UI descriptions: [Use cases rows 279-297](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A279:B297). No Figma node identifier was supplied.

### Related API IDs

- [API-GOAL-LIST](../api/api-goal-list.md)

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

class CalendarDate {
  +ordinal: Integer
  +{static} monthStart(date: CalendarDate): CalendarDate
  +{static} monthEnd(date: CalendarDate): CalendarDate
}

class Category {
  +id: Integer
  +name: String
}

class Goal {
  +id: Integer
  +userId: Integer
  +goalType: GoalType
  +categoryId: Integer [0..1]
  +startDate: CalendarDate
  +endDate: CalendarDate
  +targetAmount: Real
  +version: Integer
}

class GoalListResult {
  +savingGoal: GoalView [0..1]
  +expenseGoals: Sequence(GoalView)
}

class GoalService {
  +list(ctx: RequestContext): GoalListResult
}

enum GoalType {
  Saving
  Expense_Limit
}

class GoalView {
  +id: Integer
  +goalType: GoalType
  +categoryId: Integer [0..1]
  +category: String [0..1]
  +startDate: CalendarDate
  +endDate: CalendarDate
  +targetAmount: Real
  +progress: Real
  +version: Integer
}

class Numeric {
  +{static} round2(x: Real): Real
}

class RequestContext {
  +userId: Integer
  +authenticated: Boolean
  +today: CalendarDate
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

Goal --> GoalType : goalType
Goal --> CalendarDate : startDate
Goal --> CalendarDate : endDate
GoalListResult --> GoalView : savingGoal
GoalListResult --> GoalView : expenseGoals
GoalView --> GoalType : goalType
GoalView --> CalendarDate : startDate
GoalView --> CalendarDate : endDate
RequestContext --> CalendarDate : today
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
-- BR-UC-13-01
-- Source: Product source
context GoalService::list(ctx: RequestContext): GoalListResult
pre BR_UC_13_01_AuthenticatedContext:
  ctx.authenticated and User.allInstances()->exists(u | u.id = ctx.userId)
~~~

~~~ocl
-- BR-UC-13-02
-- Source: Product source
context GoalService::list(ctx: RequestContext): GoalListResult
post BR_UC_13_02_SavingSelection:
  let candidates : Set(Goal) = Goal.allInstances()->select(g | g.userId = ctx.userId and g.startDate.ordinal <= g.endDate.ordinal and g.startDate.ordinal <= CalendarDate::monthEnd(ctx.today).ordinal and g.endDate.ordinal >= CalendarDate::monthStart(ctx.today).ordinal)->select(g | g.goalType = GoalType::Saving)->asSet() in if candidates->isEmpty() then result.savingGoal.oclIsUndefined() else let latest : Integer = candidates->collect(g | g.startDate.ordinal)->max() in result.savingGoal.id = candidates->select(g | g.startDate.ordinal = latest)->collect(id)->max() endif
~~~

~~~ocl
-- BR-UC-13-03
-- Source: Product source
context GoalService::list(ctx: RequestContext): GoalListResult
post BR_UC_13_03_ExactExpenseCoverage:
  result.expenseGoals->collect(id)->asSet() = Goal.allInstances()->select(g | g.userId = ctx.userId and g.startDate.ordinal <= g.endDate.ordinal and g.startDate.ordinal <= CalendarDate::monthEnd(ctx.today).ordinal and g.endDate.ordinal >= CalendarDate::monthStart(ctx.today).ordinal)->select(g | g.goalType = GoalType::Expense_Limit)->collect(id)->asSet() and result.expenseGoals->isUnique(id)
~~~

~~~ocl
-- BR-UC-13-04
-- Source: Assumption
context GoalService::list(ctx: RequestContext): GoalListResult
post BR_UC_13_04_SavingProgress:
  not result.savingGoal.oclIsUndefined() implies let g : Goal = Goal.allInstances()->any(g | g.id = result.savingGoal.id) in let rows : Set(Transaction) = Transaction.allInstances()->select(t | Account.allInstances()->exists(a | a.id = t.accountId and a.userId = ctx.userId) and t.status = TransactionStatus::Complete and t.date.ordinal >= (if g.startDate.ordinal > CalendarDate::monthStart(ctx.today).ordinal then g.startDate.ordinal else CalendarDate::monthStart(ctx.today).ordinal endif) and t.date.ordinal <= (if g.endDate.ordinal < CalendarDate::monthEnd(ctx.today).ordinal then g.endDate.ordinal else CalendarDate::monthEnd(ctx.today).ordinal endif))->asSet() in result.savingGoal.progress = Numeric::round2(rows->select(t | t.type = TransactionType::Revenue)->collect(amount)->sum() - rows->select(t | t.type = TransactionType::Expense)->collect(amount)->sum())
~~~

~~~ocl
-- BR-UC-13-05
-- Source: Assumption
context GoalService::list(ctx: RequestContext): GoalListResult
post BR_UC_13_05_ExpenseProgress:
  result.expenseGoals->forAll(v | let g : Goal = Goal.allInstances()->any(g | g.id = v.id) in v.progress = Numeric::round2(Transaction.allInstances()->select(t | Account.allInstances()->exists(a | a.id = t.accountId and a.userId = ctx.userId) and t.status = TransactionStatus::Complete and t.type = TransactionType::Expense and t.categoryId = g.categoryId and t.date.ordinal >= (if g.startDate.ordinal > CalendarDate::monthStart(ctx.today).ordinal then g.startDate.ordinal else CalendarDate::monthStart(ctx.today).ordinal endif) and t.date.ordinal <= (if g.endDate.ordinal < CalendarDate::monthEnd(ctx.today).ordinal then g.endDate.ordinal else CalendarDate::monthEnd(ctx.today).ordinal endif))->collect(amount)->sum()))
~~~

~~~ocl
-- BR-UC-13-06
-- Source: Product source
context GoalService::list(ctx: RequestContext): GoalListResult
post BR_UC_13_06_CategoryLabel:
  result.expenseGoals->forAll(v | if v.categoryId.oclIsUndefined() then v.category = 'Uncategorized' else let c : Category = Category.allInstances()->any(c | c.id = v.categoryId) in if c.oclIsUndefined() or Text::trim(c.name).size() = 0 then v.category = 'Unknown' else v.category = Text::trim(c.name) endif endif)
~~~

~~~ocl
-- BR-UC-13-07
-- Source: Product source
context GoalService::list(ctx: RequestContext): GoalListResult
post BR_UC_13_07_GoalProjection:
  result.expenseGoals->including(result.savingGoal)->reject(v | v.oclIsUndefined())->forAll(v | Goal.allInstances()->exists(g | g.id = v.id and g.userId = ctx.userId and g.goalType = v.goalType and g.categoryId = v.categoryId and g.targetAmount = v.targetAmount and g.startDate = v.startDate and g.endDate = v.endDate and g.version = v.version))
~~~

~~~ocl
-- BR-UC-13-08
-- Source: Product source
context GoalService::list(ctx: RequestContext): GoalListResult
post BR_UC_13_08_PriorityOrder:
  result.expenseGoals->size() <= 1 or Sequence{1..result.expenseGoals->size()-1}->forAll(i | let a : GoalView = result.expenseGoals->at(i) in let b : GoalView = result.expenseGoals->at(i+1) in (a.progress >= a.targetAmount and b.progress < b.targetAmount) or ((a.progress >= a.targetAmount) = (b.progress >= b.targetAmount) and (a.endDate.ordinal < b.endDate.ordinal or (a.endDate.ordinal = b.endDate.ordinal and (a.targetAmount < b.targetAmount or (a.targetAmount = b.targetAmount and a.id < b.id))))))
~~~

~~~ocl
-- BR-UC-13-09
-- Source: Product source
-- Equality denotes the complete persistent value snapshot, including every property, not object identity alone.
context GoalService::list(ctx: RequestContext): GoalListResult
post BR_UC_13_09_GoalUnchanged:
  Goal.allInstances()->collect(e | Tuple{id = e.id, userId = e.userId, goalType = e.goalType, categoryId = e.categoryId, startDate = e.startDate, endDate = e.endDate, targetAmount = e.targetAmount, version = e.version})->asSet() = Goal.allInstances()@pre->collect(e | Tuple{id = e.id@pre, userId = e.userId@pre, goalType = e.goalType@pre, categoryId = e.categoryId@pre, startDate = e.startDate@pre, endDate = e.endDate@pre, targetAmount = e.targetAmount@pre, version = e.version@pre})->asSet()
~~~

~~~ocl
-- BR-UC-13-10
-- Source: Product source
-- Equality denotes the complete persistent value snapshot, including every property, not object identity alone.
context GoalService::list(ctx: RequestContext): GoalListResult
post BR_UC_13_10_TransactionUnchanged:
  Transaction.allInstances()->collect(e | Tuple{id = e.id, accountId = e.accountId, categoryId = e.categoryId, date = e.date, type = e.type, status = e.status, description = e.description, shopName = e.shopName, paymentMethod = e.paymentMethod, amount = e.amount, receiptId = e.receiptId, createdAt = e.createdAt})->asSet() = Transaction.allInstances()@pre->collect(e | Tuple{id = e.id@pre, accountId = e.accountId@pre, categoryId = e.categoryId@pre, date = e.date@pre, type = e.type@pre, status = e.status@pre, description = e.description@pre, shopName = e.shopName@pre, paymentMethod = e.paymentMethod@pre, amount = e.amount@pre, receiptId = e.receiptId@pre, createdAt = e.createdAt@pre})->asSet()
~~~
