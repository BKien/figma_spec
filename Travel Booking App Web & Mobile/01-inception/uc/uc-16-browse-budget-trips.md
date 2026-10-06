---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-16
uc_name: "Browse Budget Trips"
---

# UC-16: Browse Budget Trips

## Functional Use-Case Specification

### Use Case ID

UC-16

### Use Case Name

Browse Budget Trips

### Description

As a traveller, I want to browse active budget-trip ideas so that I can choose an affordable destination.

### Actor(s)

Traveller; Trip Service.

### Priority

P1.

### Trigger

The traveller opens the budget-trips page.

### Pre-Condition(s)

PRE-1: The traveller can access the budget-trips page.

### Post-Condition(s)

POST-1: The client displays the budget-trip page state returned by the system.
POST-2: Available navigation from the displayed content remains accessible.

### Basic Flow

1. The traveller opens the budget-trips page.
2. The client requests a page of budget-trip content.
3. The system processes the request and returns a page outcome.
4. The client renders the returned trip-card presentations.
5. The traveller may request another page or select a trip.

### Alternative Flow

AF-1:

1. If no trip content is returned, the client displays the designed empty state.

AF-2:

1. The client adapts the returned content to the active visual mode or device layout.

### Exception Flow

EF-1:

1. If another page cannot be loaded, the client keeps the displayed content and offers a retry.

EF-2:

1. If the initial request cannot be completed, the client displays the designed unavailable state.

### Related UI

`budget trips main page`; `budget trips mobile`; `budget trips dark mode`.

### Related API IDs

`API-BUDGET-TRIP-LIST`.

## UML Model

~~~plantuml
@startuml
hide empty members

class String {
  +<(other: String): Boolean
}

class DateTime {
  +{static} hoursBetween(start: DateTime, end: DateTime): Real
  +<=(other: DateTime): Boolean
  +>(other: DateTime): Boolean
}

class RequestContext {
  +{static} startedAt: DateTime
}

class Money {
  +amount: Real
  +currency: String
}

class BudgetTrip {
  +id: String
  +active: Boolean
  +startingPrice: Money
  +destinationId: String
  +editorialRank: Integer
  +publishFrom: DateTime
  +publishUntil: DateTime
  +priceEvidence: PriceEvidence[*] {ordered}
}

class TripService {
  +list(limit: Integer, offset: Integer): TripPage
}

class PriceEvidence {
  +amount: Money
  +active: Boolean
  +observedAt: DateTime
}

class TripPage {
  +items: BudgetTrip[*] {ordered}
  +total: Integer
  +limit: Integer
  +offset: Integer
  +hasMore: Boolean
}

class ReadState {
  +{static} editorial(): String
}

BudgetTrip "1" o-- "0..*" PriceEvidence : priceEvidence
TripPage "1" o-- "0..*" BudgetTrip : items
BudgetTrip --> "1" Money : startingPrice
PriceEvidence --> "1" Money : amount

@enduml
~~~

## Business Rules

~~~ocl
-- BR-UC-16-01
-- Source: Assumption
context TripService::list(limit: Integer, offset: Integer): TripPage
post BR_UC_16_01_OnlyCurrentlyPublishedEditorialTripsAppear:
  result.items->forAll(t |
    t.active and t.publishFrom <= RequestContext::startedAt and
    (t.publishUntil = null or t.publishUntil > RequestContext::startedAt))
~~~

~~~ocl
-- BR-UC-16-02
-- Source: Assumption
context TripService::list(limit: Integer, offset: Integer): TripPage
post BR_UC_16_02_OneEditorialCardPerDestination:
  result.items->isUnique(t | t.destinationId)
~~~

~~~ocl
-- BR-UC-16-03
-- Source: Assumption
context TripService::list(limit: Integer, offset: Integer): TripPage
post BR_UC_16_03_IndicativePriceUsesRecentEvidenceInTheSameCurrency:
  result.items->forAll(t |
  let eligible = t.priceEvidence->select(e |
    e.active and e.amount.currency = t.startingPrice.currency and
    e.observedAt <= RequestContext::startedAt and
    DateTime::hoursBetween(e.observedAt, RequestContext::startedAt) <= 24) in
  eligible->notEmpty() and t.startingPrice.amount >= 0 and
  t.startingPrice.amount = eligible->collect(e | e.amount.amount)->min())
~~~

~~~ocl
-- BR-UC-16-04
-- Source: Assumption
context TripService::list(limit: Integer, offset: Integer): TripPage
post BR_UC_16_04_EditorialOrderHasStableTieBreak:
  result.items->size() <= 1 or
  Sequence{1..result.items->size() - 1}->forAll(i |
   result.items->at(i).editorialRank < result.items->at(i + 1).editorialRank or
   (result.items->at(i).editorialRank = result.items->at(i + 1).editorialRank and
    result.items->at(i).id < result.items->at(i + 1).id))
~~~

~~~ocl
-- BR-UC-16-05
-- Source: Assumption
context TripService::list(limit: Integer, offset: Integer): TripPage
post BR_UC_16_05_PageMetadataMatchesItsSlice:
  result.limit = limit and result.offset = offset and result.total >= 0 and
  result.items->size() = (result.total - offset).max(0).min(limit) and
  result.hasMore = (offset + result.items->size() < result.total)
~~~

~~~ocl
-- BR-UC-16-06
-- Source: Assumption
context TripService::list(limit: Integer, offset: Integer): TripPage
post BR_UC_16_06_BrowsingEditorialContentIsReadOnly:
  ReadState::editorial() = ReadState::editorial()@pre
~~~

~~~ocl
-- BR-UC-16-07
-- Source: Assumption
context TripService::list(limit: Integer, offset: Integer): TripPage
pre BR_UC_16_07_PageRequestHasUsableBounds:
  limit > 0 and offset >= 0
~~~
