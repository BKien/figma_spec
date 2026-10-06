---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-12
uc_name: "View Upcoming Bills"
---

# UC-12: View Upcoming Bills

## Functional Use-Case Specification

### Use Case ID

UC-12

### Use Case Name

View Upcoming Bills

### Description

Review upcoming recorded bill obligations.

### Actor(s)

Primary: Account holder. Supporting: application client and application service.

### Priority

High.

### Trigger

The user opens the Bills page.

### Pre-Condition(s)

PRE-1: The application view is open in the client.

### Post-Condition(s)

POST-1: On success, the client displays upcoming bills or the empty-bills view.
POST-2: On failure, the client displays a recovery message in the current view.

### Basic Flow

1. The user opens the Bills page.
2. The client requests upcoming bills.
3. The system returns bill rows.
4. The client displays descriptions, due dates, logos, and amounts.

### Alternative Flow

AF-1:

1. The system returns no bills.
2. The client displays the empty-bills state.

### Exception Flow

EF-1:

1. The system returns an operation error.
2. The client displays the error message and keeps the current view open.
3. The actor revises the interaction or retries the request.

EF-2:

1. The system returns a rejected authentication context.
2. The client presents the login entry point.

### Related UI

- Product-source UI descriptions: [Use cases rows 260-277](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A260:B277). No Figma node identifier was supplied.

### Related API IDs

- [API-BILL-LIST](../api/api-bill-list.md)

### Notes

See [source mapping](../../coverage-report.md), [review decisions](../../consistency-review.md), and [assumptions](../../ASSUMPTIONS.md). The supplied spreadsheet is specification evidence; no running application or Figma interaction was verified.

## UML Model

~~~plantuml
@startuml
hide empty members

class Bill {
  +id: Integer
  +userId: Integer
  +description: String
  +logoUrl: String [0..1]
  +dueDate: CalendarDate
  +lastChargeDate: CalendarDate [0..1]
  +amount: Real
}

class BillResult {
  +success: Boolean
  +bills: Sequence(BillView)
}

class BillService {
  +upcoming(ctx: RequestContext): BillResult
}

class BillView {
  +id: Integer
  +userId: Integer
  +description: String
  +logoUrl: String [0..1]
  +dueDate: CalendarDate
  +lastChargeDate: CalendarDate [0..1]
  +amount: Real
}

class CalendarDate {
  +ordinal: Integer
}

class Numeric {
  +{static} round2(x: Real): Real
  +{static} finite(x: Real): Boolean
}

class RequestContext {
  +userId: Integer
  +authenticated: Boolean
  +today: CalendarDate
}

class Text {
  +{static} trim(s: String): String
}

class User {
  +id: Integer
}

Bill --> CalendarDate : dueDate
Bill --> CalendarDate : lastChargeDate
BillResult --> BillView : bills
BillView --> CalendarDate : dueDate
BillView --> CalendarDate : lastChargeDate
RequestContext --> CalendarDate : today

note right of CalendarDate
  ordinal is the calendar-day index in Asia/Saigon.
end note

@enduml
~~~

## Business Rules

~~~ocl
-- BR-UC-12-01
-- Source: Product source
context BillService::upcoming(ctx: RequestContext): BillResult
pre BR_UC_12_01_AuthenticatedContext:
  ctx.authenticated and User.allInstances()->exists(u | u.id = ctx.userId)
~~~

~~~ocl
-- BR-UC-12-02
-- Source: Product source
context BillService::upcoming(ctx: RequestContext): BillResult
post BR_UC_12_02_OwnedBills:
  result.bills->forAll(b | b.userId = ctx.userId)
~~~

~~~ocl
-- BR-UC-12-03
-- Source: Product source
context BillService::upcoming(ctx: RequestContext): BillResult
post BR_UC_12_03_Window:
  result.bills->forAll(b | b.dueDate.ordinal >= ctx.today.ordinal and b.dueDate.ordinal <= ctx.today.ordinal + 30)
~~~

~~~ocl
-- BR-UC-12-04
-- Source: Product source
context BillService::upcoming(ctx: RequestContext): BillResult
post BR_UC_12_04_UnchargedCycle:
  result.bills->forAll(b | b.lastChargeDate.oclIsUndefined() or b.lastChargeDate.ordinal < b.dueDate.ordinal)
~~~

~~~ocl
-- BR-UC-12-05
-- Source: Product source
context BillService::upcoming(ctx: RequestContext): BillResult
post BR_UC_12_05_ExactCoverage:
  result.success implies result.bills->collect(id)->asSet() = Bill.allInstances()->select(b | b.userId = ctx.userId and b.dueDate.ordinal >= ctx.today.ordinal and b.dueDate.ordinal <= ctx.today.ordinal + 30 and (b.lastChargeDate.oclIsUndefined() or b.lastChargeDate.ordinal < b.dueDate.ordinal))->collect(id)->asSet()
~~~

~~~ocl
-- BR-UC-12-06
-- Source: Product source
context BillService::upcoming(ctx: RequestContext): BillResult
post BR_UC_12_06_NoDuplicates:
  result.bills->isUnique(id)
~~~

~~~ocl
-- BR-UC-12-07
-- Source: Product source
context BillService::upcoming(ctx: RequestContext): BillResult
post BR_UC_12_07_UrgencyOrder:
  result.bills->size() <= 1 or Sequence{1..result.bills->size()-1}->forAll(i | let a : BillView = result.bills->at(i) in let b : BillView = result.bills->at(i+1) in a.dueDate.ordinal < b.dueDate.ordinal or (a.dueDate.ordinal = b.dueDate.ordinal and (a.amount > b.amount or (a.amount = b.amount and a.id < b.id))))
~~~

~~~ocl
-- BR-UC-12-08
-- Source: Product source
context BillService::upcoming(ctx: RequestContext): BillResult
post BR_UC_12_08_NormalizedMapping:
  result.bills->forAll(v | Bill.allInstances()->exists(b | b.id = v.id and b.userId = v.userId and v.description = Text::trim(b.description) and v.amount = Numeric::round2(b.amount) and v.dueDate = b.dueDate and v.lastChargeDate = b.lastChargeDate and v.logoUrl = (if b.logoUrl.oclIsUndefined() or Text::trim(b.logoUrl).size() = 0 then null else Text::trim(b.logoUrl) endif)))
~~~

~~~ocl
-- BR-UC-12-09
-- Source: Assumption
context BillService::upcoming(ctx: RequestContext): BillResult
post BR_UC_12_09_Amounts:
  result.bills->forAll(b | Numeric::finite(b.amount) and b.amount >= 0 and b.amount = Numeric::round2(b.amount))
~~~

~~~ocl
-- BR-UC-12-10
-- Source: Product source
-- Equality denotes the complete persistent value snapshot, including every property, not object identity alone.
context BillService::upcoming(ctx: RequestContext): BillResult
post BR_UC_12_10_BillUnchanged:
  Bill.allInstances()->collect(e | Tuple{id = e.id, userId = e.userId, description = e.description, logoUrl = e.logoUrl, dueDate = e.dueDate, lastChargeDate = e.lastChargeDate, amount = e.amount})->asSet() = Bill.allInstances()@pre->collect(e | Tuple{id = e.id@pre, userId = e.userId@pre, description = e.description@pre, logoUrl = e.logoUrl@pre, dueDate = e.dueDate@pre, lastChargeDate = e.lastChargeDate@pre, amount = e.amount@pre})->asSet()
~~~
