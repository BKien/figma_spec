---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-14
uc_name: "Create a Financial Goal"
---

# UC-14: Create a Financial Goal

## Functional Use-Case Specification

### Use Case ID

UC-14

### Use Case Name

Create a Financial Goal

### Description

Define a saving target or a category spending limit.

### Actor(s)

Primary: Account holder. Supporting: application client and application service.

### Priority

High.

### Trigger

The user opens the Create Goal dialog.

### Pre-Condition(s)

PRE-1: The application view is open in the client.

### Post-Condition(s)

POST-1: On success, the client closes the goal dialog and refreshes Goals.
POST-2: On failure, the client displays a recovery message in the current view.

### Basic Flow

1. The user opens the Create Goal dialog.
2. The client requests category choices and displays the goal form.
3. The user enters goal details and submits the form.
4. The client sends the goal creation request.
5. The system returns the creation result.
6. The client closes the dialog and refreshes Goals.

### Alternative Flow

AF-1:

1. The user cancels the dialog.
2. The client closes the dialog and shows Goals.

### Exception Flow

EF-1:

1. The system returns an operation error.
2. The client displays the error message and keeps the current view open.
3. The actor revises the interaction or retries the request.

EF-2:

1. The system returns a rejected authentication context.
2. The client presents the login entry point.

### Related UI

- Product-source UI descriptions: [Use cases rows 299-316](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A299:B316). No Figma node identifier was supplied.

### Related API IDs

- [API-GOAL-CREATE](../api/api-goal-create.md)
- [API-CATEGORY-LIST](../api/api-category-list.md)

### Notes

See [source mapping](../../coverage-report.md), [review decisions](../../consistency-review.md), and [assumptions](../../ASSUMPTIONS.md). The supplied spreadsheet is specification evidence; no running application or Figma interaction was verified.

## UML Model

~~~plantuml
@startuml
hide empty members

class CalendarDate {
  +ordinal: Integer
}

class Category {
  +id: Integer
}

class CreateGoalCommand {
  +goalType: GoalType
  +categoryId: Integer [0..1]
  +startDate: CalendarDate
  +endDate: CalendarDate
  +targetAmount: Real
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

class GoalResult {
  +success: Boolean
  +goal: Goal [0..1]
}

class GoalService {
  +create(ctx: RequestContext, cmd: CreateGoalCommand): GoalResult
}

enum GoalType {
  Saving
  Expense_Limit
}

class Numeric {
  +{static} finite(x: Real): Boolean
  +{static} scale(x: Real): Integer
}

class RequestContext {
  +userId: Integer
  +authenticated: Boolean
  +today: CalendarDate
}

class User {
  +id: Integer
}

CreateGoalCommand --> GoalType : goalType
CreateGoalCommand --> CalendarDate : startDate
CreateGoalCommand --> CalendarDate : endDate
Goal --> GoalType : goalType
Goal --> CalendarDate : startDate
Goal --> CalendarDate : endDate
GoalResult --> Goal : goal
RequestContext --> CalendarDate : today

note right of CalendarDate
  ordinal is the calendar-day index in Asia/Saigon.
end note

@enduml
~~~

## Business Rules

~~~ocl
-- BR-UC-14-01
-- Source: Product source
context GoalService::create(ctx: RequestContext, cmd: CreateGoalCommand): GoalResult
pre BR_UC_14_01_AuthenticatedContext:
  ctx.authenticated and User.allInstances()->exists(u | u.id = ctx.userId)
~~~

~~~ocl
-- BR-UC-14-02
-- Source: Product source
context GoalService::create(ctx: RequestContext, cmd: CreateGoalCommand): GoalResult
pre BR_UC_14_02_CategorySemantics:
  (cmd.goalType = GoalType::Saving implies cmd.categoryId.oclIsUndefined()) and (cmd.goalType = GoalType::Expense_Limit implies not cmd.categoryId.oclIsUndefined() and Category.allInstances()->exists(c | c.id = cmd.categoryId))
~~~

~~~ocl
-- BR-UC-14-03
-- Source: Assumption
-- Exact decimal arithmetic; upper bound matches DECIMAL(18,2). Source positivity and precision are retained.
context GoalService::create(ctx: RequestContext, cmd: CreateGoalCommand): GoalResult
pre BR_UC_14_03_TargetAmount:
  Numeric::finite(cmd.targetAmount) and cmd.targetAmount > 0 and Numeric::scale(cmd.targetAmount) <= 2 and cmd.targetAmount < 10000000000000000
~~~

~~~ocl
-- BR-UC-14-04
-- Source: Product source
context GoalService::create(ctx: RequestContext, cmd: CreateGoalCommand): GoalResult
pre BR_UC_14_04_ProspectiveInterval:
  cmd.startDate.ordinal >= ctx.today.ordinal and cmd.endDate.ordinal > cmd.startDate.ordinal and cmd.endDate.ordinal - cmd.startDate.ordinal <= 366
~~~

~~~ocl
-- BR-UC-14-05
-- Source: Product source
-- Lock the owner User row, then check overlaps and insert within one transaction. MySQL has no exclusion constraint for date intervals.
context GoalService::create(ctx: RequestContext, cmd: CreateGoalCommand): GoalResult
pre BR_UC_14_05_NoOverlap:
  not Goal.allInstances()->exists(g | g.userId = ctx.userId and g.goalType = cmd.goalType and (cmd.goalType = GoalType::Saving or g.categoryId = cmd.categoryId) and g.startDate.ordinal <= cmd.endDate.ordinal and g.endDate.ordinal >= cmd.startDate.ordinal)
~~~

~~~ocl
-- BR-UC-14-06
-- Source: Product source
context GoalService::create(ctx: RequestContext, cmd: CreateGoalCommand): GoalResult
post BR_UC_14_06_ExactPersistence:
  result.success implies Goal.allInstances()->one(g | g.id = result.goal.id and g.userId = ctx.userId and g.goalType = cmd.goalType and g.categoryId = cmd.categoryId and g.startDate = cmd.startDate and g.endDate = cmd.endDate and g.targetAmount = cmd.targetAmount and g.version = 0)
~~~

~~~ocl
-- BR-UC-14-07
-- Source: Product source
context GoalService::create(ctx: RequestContext, cmd: CreateGoalCommand): GoalResult
post BR_UC_14_07_ExactlyOne:
  result.success implies Goal.allInstances()->size() = Goal.allInstances()@pre->size() + 1
~~~

~~~ocl
-- BR-UC-14-08
-- Source: Product source
context GoalService::create(ctx: RequestContext, cmd: CreateGoalCommand): GoalResult
post BR_UC_14_08_ExistingGoalsPreserved:
  result.success implies Goal.allInstances()->select(g | g.id <> result.goal.id)->collect(e | Tuple{id = e.id, userId = e.userId, goalType = e.goalType, categoryId = e.categoryId, startDate = e.startDate, endDate = e.endDate, targetAmount = e.targetAmount, version = e.version})->asSet() = Goal.allInstances()@pre->collect(e | Tuple{id = e.id@pre, userId = e.userId@pre, goalType = e.goalType@pre, categoryId = e.categoryId@pre, startDate = e.startDate@pre, endDate = e.endDate@pre, targetAmount = e.targetAmount@pre, version = e.version@pre})->asSet()
~~~

~~~ocl
-- BR-UC-14-09
-- Source: Product source
context GoalService::create(ctx: RequestContext, cmd: CreateGoalCommand): GoalResult
post BR_UC_14_09_AtomicFailure:
  not result.success implies Goal.allInstances()->collect(e | Tuple{id = e.id, userId = e.userId, goalType = e.goalType, categoryId = e.categoryId, startDate = e.startDate, endDate = e.endDate, targetAmount = e.targetAmount, version = e.version})->asSet() = Goal.allInstances()@pre->collect(e | Tuple{id = e.id@pre, userId = e.userId@pre, goalType = e.goalType@pre, categoryId = e.categoryId@pre, startDate = e.startDate@pre, endDate = e.endDate@pre, targetAmount = e.targetAmount@pre, version = e.version@pre})->asSet()
~~~
