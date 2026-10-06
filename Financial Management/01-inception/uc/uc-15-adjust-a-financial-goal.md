---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-15
uc_name: "Adjust a Financial Goal"
---

# UC-15: Adjust a Financial Goal

## Functional Use-Case Specification

### Use Case ID

UC-15

### Use Case Name

Adjust a Financial Goal

### Description

Change the target amount of a displayed goal.

### Actor(s)

Primary: Account holder. Supporting: application client and application service.

### Priority

High.

### Trigger

The user selects Edit on a goal card.

### Pre-Condition(s)

PRE-1: The application view is open in the client.

### Post-Condition(s)

POST-1: On success, the client closes the adjustment dialog and refreshes goal cards.
POST-2: On failure, the client displays a recovery message in the current view.

### Basic Flow

1. The user selects Edit on a goal card.
2. The client displays the target adjustment dialog.
3. The user enters a new target and selects Save.
4. The client sends the update request.
5. The system returns the update result.
6. The client closes the dialog and refreshes Goals.

### Alternative Flow

AF-1:

1. The user cancels the adjustment.
2. The client closes the dialog.

### Exception Flow

EF-1:

1. The system returns an operation error.
2. The client displays the error message and keeps the current view open.
3. The actor revises the interaction or retries the request.

EF-2:

1. The system returns a rejected authentication context.
2. The client presents the login entry point.

EF-3:

1. The system returns an operation conflict.
2. The client offers to reload the current resource.
3. The user reloads the view and submits the interaction again.

### Related UI

- Product-source UI descriptions: [Use cases rows 318-334](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A318:B334). No Figma node identifier was supplied.

### Related API IDs

- [API-GOAL-LIST](../api/api-goal-list.md)
- [API-GOAL-UPDATE](../api/api-goal-update.md)

### Notes

See [source mapping](../../coverage-report.md), [review decisions](../../consistency-review.md), and [assumptions](../../ASSUMPTIONS.md). The supplied spreadsheet is specification evidence; no running application or Figma interaction was verified.

## UML Model

~~~plantuml
@startuml
hide empty members

class CalendarDate {
  ' Only the type is referenced by this use case's Business Rules.
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
  +update(ctx: RequestContext, cmd: UpdateGoalCommand): GoalResult
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
}

class UpdateGoalCommand {
  +goalId: Integer
  +targetAmount: Real
  +expectedVersion: Integer
}

class User {
  +id: Integer
}

Goal --> GoalType : goalType
Goal --> CalendarDate : startDate
Goal --> CalendarDate : endDate
GoalResult --> Goal : goal

@enduml
~~~

## Business Rules

~~~ocl
-- BR-UC-15-01
-- Source: Product source
context GoalService::update(ctx: RequestContext, cmd: UpdateGoalCommand): GoalResult
pre BR_UC_15_01_AuthenticatedContext:
  ctx.authenticated and User.allInstances()->exists(u | u.id = ctx.userId)
~~~

~~~ocl
-- BR-UC-15-02
-- Source: Product source
context GoalService::update(ctx: RequestContext, cmd: UpdateGoalCommand): GoalResult
pre BR_UC_15_02_OwnedGoal:
  Goal.allInstances()->exists(g | g.id = cmd.goalId and g.userId = ctx.userId)
~~~

~~~ocl
-- BR-UC-15-03
-- Source: Assumption
-- Exact decimal arithmetic; upper bound matches DECIMAL(18,2). Source positivity and precision are retained.
context GoalService::update(ctx: RequestContext, cmd: UpdateGoalCommand): GoalResult
pre BR_UC_15_03_TargetAmount:
  Numeric::finite(cmd.targetAmount) and cmd.targetAmount > 0 and Numeric::scale(cmd.targetAmount) <= 2 and cmd.targetAmount < 10000000000000000
~~~

~~~ocl
-- BR-UC-15-04
-- Source: Assumption
context GoalService::update(ctx: RequestContext, cmd: UpdateGoalCommand): GoalResult
pre BR_UC_15_04_Version:
  Goal.allInstances()->exists(g | g.id = cmd.goalId and g.version = cmd.expectedVersion)
~~~

~~~ocl
-- BR-UC-15-05
-- Source: Assumption
context GoalService::update(ctx: RequestContext, cmd: UpdateGoalCommand): GoalResult
post BR_UC_15_05_OnlyTargetChanged:
  result.success implies Goal.allInstances()->exists(g | g.id = cmd.goalId and g.targetAmount = cmd.targetAmount and g.version = g.version@pre + 1 and g.userId = g.userId@pre and g.goalType = g.goalType@pre and g.categoryId = g.categoryId@pre and g.startDate = g.startDate@pre and g.endDate = g.endDate@pre)
~~~

~~~ocl
-- BR-UC-15-06
-- Source: Product source
context GoalService::update(ctx: RequestContext, cmd: UpdateGoalCommand): GoalResult
post BR_UC_15_06_OtherGoalsPreserved:
  Goal.allInstances()->select(g | g.id <> cmd.goalId)->collect(e | Tuple{id = e.id, userId = e.userId, goalType = e.goalType, categoryId = e.categoryId, startDate = e.startDate, endDate = e.endDate, targetAmount = e.targetAmount, version = e.version})->asSet() = Goal.allInstances()@pre->select(g | g.id <> cmd.goalId)->collect(e | Tuple{id = e.id@pre, userId = e.userId@pre, goalType = e.goalType@pre, categoryId = e.categoryId@pre, startDate = e.startDate@pre, endDate = e.endDate@pre, targetAmount = e.targetAmount@pre, version = e.version@pre})->asSet()
~~~

~~~ocl
-- BR-UC-15-07
-- Source: Assumption
context GoalService::update(ctx: RequestContext, cmd: UpdateGoalCommand): GoalResult
post BR_UC_15_07_Identity:
  result.success implies result.goal.id = cmd.goalId and result.goal.targetAmount = cmd.targetAmount and result.goal.version = cmd.expectedVersion + 1
~~~

~~~ocl
-- BR-UC-15-08
-- Source: Product source
context GoalService::update(ctx: RequestContext, cmd: UpdateGoalCommand): GoalResult
post BR_UC_15_08_FailureRollback:
  not result.success implies Goal.allInstances()->collect(e | Tuple{id = e.id, userId = e.userId, goalType = e.goalType, categoryId = e.categoryId, startDate = e.startDate, endDate = e.endDate, targetAmount = e.targetAmount, version = e.version})->asSet() = Goal.allInstances()@pre->collect(e | Tuple{id = e.id@pre, userId = e.userId@pre, goalType = e.goalType@pre, categoryId = e.categoryId@pre, startDate = e.startDate@pre, endDate = e.endDate@pre, targetAmount = e.targetAmount@pre, version = e.version@pre})->asSet()
~~~
