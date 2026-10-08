---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-06
uc_name: "Filter and Sort Stay Results"
---

# UC-06: Filter and Sort Stay Results

## Functional Use-Case Specification

### Use Case ID

UC-06

### Use Case Name

Filter and Sort Stay Results

### Description

As a traveller, I want to filter and sort stays so that I can narrow the results.

### Actor(s)

Traveller; Stay Service.

### Priority

P1.

### Trigger

The traveller chooses to refine the displayed stay results.

### Pre-Condition(s)

PRE-1: The traveller is viewing stay results for a search context.

### Post-Condition(s)

POST-1: The results view displays the refinement outcome returned by the system.

POST-2: The search context remains available for another result interaction.

### Basic Flow

1. The traveller opens the stay filter or sort controls.
2. The client displays the current selections.
3. The traveller changes one or more selections and applies them.
4. The client submits the revised result preferences with the current search context.
5. The system processes the request and returns a refinement outcome.
6. The client renders the returned result state and selections.

### Alternative Flow

AF-1: Clear Stay Result Refinements

3a: The traveller clears the displayed refinements and requests the base result view.

AF-2: Dismiss Pending Stay Filters

3b: On mobile, the traveller dismisses the filter panel without applying pending changes.

### Exception Flow

EF-1: Stay Result Refresh Failure

5a: If the refresh cannot be completed, the client keeps the previously displayed result state.

5b: The client presents the retry action returned for the failed refresh.

### Related UI

hotel filter; stay filters mobile.

### Related API IDs

API-STAY-SEARCH.

### Notes

None.

## UML Model

~~~plantuml
@startuml
hide empty members

enum StaySort {
  RECOMMENDED
  PRICE
  RATING
}

class String {
  +<(other: String): Boolean
}

class RequestContext {
  +{static} startedAt: DateTime
}

class Money {
  +amount: Real
}

class StayOffer {
  +id: String
  +total: Money
  +searchContextId: String
  +rating: Real
  +recommendationScore: Real
}

class StayService {
  +search(criteria: StaySearchCriteria): Sequence(StayOffer)
}

class StaySearchCriteria {
  +minPrice: Real
  +maxPrice: Real
  +minRating: Real
  +sort: StaySort
  +limit: Integer
  +offset: Integer
  +searchContextId: String
  +snapshotVersion: Integer
}

class SearchSnapshot {
  +{static} refinementChanged(criteria: StaySearchCriteria): Boolean
  +{static} accepts(criteria: StaySearchCriteria, at: DateTime): Boolean
}

StaySearchCriteria --> StaySort : sort
StayOffer --> "1" Money : total

@enduml
~~~

## Business Rules

~~~text
BR-FILTER-STAYS-01 - Refinement Cannot Escape The Accepted Search
Source: Assumption
context StayService::search(criteria: StaySearchCriteria): Sequence(StayOffer)
post BR_FILTER_STAYS_01_RefinementCannotEscapeTheAcceptedSearch:
  result->forAll(o | (criteria.searchContextId = null or o.searchContextId = criteria.searchContextId))
~~~

~~~text
BR-FILTER-STAYS-02 - All Accepted Filters Apply Together
Source: Assumption
context StayService::search(criteria: StaySearchCriteria): Sequence(StayOffer)
post BR_FILTER_STAYS_02_AllAcceptedFiltersApplyTogether:
  result->forAll(o |
    (criteria.minPrice = null or o.total.amount >= criteria.minPrice) and
    (criteria.maxPrice = null or o.total.amount <= criteria.maxPrice) and
    (criteria.minRating = null or o.rating >= criteria.minRating))
~~~

~~~text
BR-FILTER-STAYS-03 - Changed Refinement Starts A New Result Traversal
Source: Assumption
context StayService::search(criteria: StaySearchCriteria): Sequence(StayOffer)
pre BR_FILTER_STAYS_03_ChangedRefinementStartsANewResultTraversal:
  criteria.offset >= 0 and criteria.limit > 0 and
  (SearchSnapshot::refinementChanged(criteria) implies criteria.offset = 0)
~~~

~~~text
BR-FILTER-STAYS-04 - Price Order Uses Rating And Identifier As Tie Breakers
Source: Assumption
context StayService::search(criteria: StaySearchCriteria): Sequence(StayOffer)
post BR_FILTER_STAYS_04_PriceOrderUsesRatingAndIdentifierAsTieBreakers:
  criteria.sort = StaySort::PRICE implies
    (result->size() <= 1 or
      Sequence{1..result->size() - 1}->forAll(i |
        result->at(i).total.amount < result->at(i + 1).total.amount or
        (result->at(i).total.amount = result->at(i + 1).total.amount and
          (result->at(i).rating > result->at(i + 1).rating or
           (result->at(i).rating = result->at(i + 1).rating and
            result->at(i).id < result->at(i + 1).id)))))
~~~

~~~text
BR-FILTER-STAYS-05 - Rating Order Uses Price And Identifier As Tie Breakers
Source: Assumption
context StayService::search(criteria: StaySearchCriteria): Sequence(StayOffer)
post BR_FILTER_STAYS_05_RatingOrderUsesPriceAndIdentifierAsTieBreakers:
  criteria.sort = StaySort::RATING implies
    (result->size() <= 1 or
      Sequence{1..result->size() - 1}->forAll(i |
        result->at(i).rating > result->at(i + 1).rating or
        (result->at(i).rating = result->at(i + 1).rating and
          (result->at(i).total.amount < result->at(i + 1).total.amount or
           (result->at(i).total.amount = result->at(i + 1).total.amount and
            result->at(i).id < result->at(i + 1).id)))))
~~~

~~~text
BR-FILTER-STAYS-06 - Recommended Order Is Deterministic
Source: Assumption
context StayService::search(criteria: StaySearchCriteria): Sequence(StayOffer)
post BR_FILTER_STAYS_06_RecommendedOrderIsDeterministic:
  criteria.sort = StaySort::RECOMMENDED implies
    (result->size() <= 1 or
      Sequence{1..result->size() - 1}->forAll(i |
        result->at(i).recommendationScore > result->at(i + 1).recommendationScore or
        (result->at(i).recommendationScore = result->at(i + 1).recommendationScore and
          result->at(i).id < result->at(i + 1).id)))
~~~

~~~text
BR-FILTER-STAYS-07 - Optional Filter Bounds Are Coherent
Source: Assumption
context StayService::search(criteria: StaySearchCriteria): Sequence(StayOffer)
pre BR_FILTER_STAYS_07_OptionalFilterBoundsAreCoherent:
  (criteria.minPrice = null or criteria.minPrice >= 0) and
  (criteria.maxPrice = null or criteria.maxPrice >= 0) and
  (criteria.minPrice = null or criteria.maxPrice = null or criteria.minPrice <= criteria.maxPrice) and
  (criteria.minRating = null or (criteria.minRating >= 0 and criteria.minRating <= 5))
~~~

~~~text
BR-FILTER-STAYS-08 - Continuation References A Usable Snapshot
Source: Assumption
context StayService::search(criteria: StaySearchCriteria): Sequence(StayOffer)
pre BR_FILTER_STAYS_08_ContinuationReferencesAUsableSnapshot:
  (criteria.searchContextId = null and criteria.snapshotVersion = null) or
  (criteria.searchContextId <> null and criteria.snapshotVersion <> null and
   SearchSnapshot::accepts(criteria, RequestContext::startedAt))
~~~
