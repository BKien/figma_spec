---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-11
uc_name: "Filter and Sort Taxi Rental Results"
---

# UC-11: Filter and Sort Taxi Rental Results

## Functional Use-Case Specification

### Use Case ID

UC-11

### Use Case Name

Filter and Sort Taxi Rental Results

### Description

As a traveller, I want to refine taxi-rental offers by car category, pick-up deposit, electric type, and the available sort control.

### Actor(s)

Traveller; Taxi Rental Service.

### Priority

P1.

### Trigger

The traveller chooses to refine the displayed Taxi results.

### Pre-Condition(s)

PRE-1: The traveller is viewing Taxi results for a search context.

### Post-Condition(s)

POST-1: The results view displays the refinement outcome returned by the system.

POST-2: The search context remains available for another result interaction.

### Basic Flow

1. The traveller opens the Taxi filter or sort controls.
2. The client displays car category, deposit, electric-car, and sort selections.
3. The traveller changes one or more selections and applies them.
4. The client submits the revised preferences with the current search context.
5. The system processes the request and returns a refinement outcome.
6. The client renders the returned result state and selections.

### Alternative Flow

AF-1: Clear Taxi Result Refinements

3a: The traveller clears the displayed refinements and requests the base result view.

AF-2: Dismiss Pending Taxi Filters

3b: On mobile, the traveller dismisses the filter panel without applying pending changes.

### Exception Flow

EF-1: Taxi Result Refresh Failure

5a: If the refresh cannot be completed, the client keeps the previously displayed result state.

5b: The client presents the retry action returned for the failed refresh.

### Related UI

taxi filter; taxi filters mobile; Car category; Deposit required at pick-up; Electric Cars; Sort by: Our top picks.

### Related API IDs

API-TAXI-SEARCH.

### Notes

None.

## UML Model

~~~plantuml
@startuml
hide empty members

enum TaxiSort {
  TOP_PICKS
}

enum VehicleCategory {
  SMALL
  MEDIUM
  LARGE
  ESTATE
}

enum ElectricType {
  NONE
  FULLY_ELECTRIC
  HYBRID
}

enum DepositBand {
  LKR_200_500
  LKR_500_1000
  LKR_1000_1200
  LKR_1200_1500
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

class TaxiOffer {
  +id: String
  +total: Money
  +deposit: Money
  +vehicle: Vehicle
  +searchContextId: String
  +recommendationScore: Real
}

class Vehicle {
  +category: VehicleCategory
  +electricType: ElectricType
}

class TaxiService {
  +search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
}

class TaxiSearchCriteria {
  +minPrice: Real
  +maxPrice: Real
  +sort: TaxiSort
  +limit: Integer
  +offset: Integer
  +searchContextId: String
  +snapshotVersion: Integer
  +vehicleCategories: VehicleCategory[*] {ordered}
  +depositBands: DepositBand[*] {ordered}
  +electricTypes: ElectricType[*] {ordered}
}

class RentalFilter {
  +{static} depositMatches(bands: DepositBand[*], amount: Money): Boolean
  +{static} electricMatches(types: ElectricType[*], value: ElectricType): Boolean
}

class SearchSnapshot {
  +{static} refinementChanged(criteria: TaxiSearchCriteria): Boolean
  +{static} accepts(criteria: TaxiSearchCriteria, at: DateTime): Boolean
}

TaxiOffer --> Vehicle : vehicle
Vehicle --> VehicleCategory : category
Vehicle --> ElectricType : electricType
TaxiSearchCriteria --> TaxiSort : sort
TaxiSearchCriteria "1" o-- "0..*" VehicleCategory : vehicleCategories
TaxiSearchCriteria "1" o-- "0..*" DepositBand : depositBands
TaxiSearchCriteria "1" o-- "0..*" ElectricType : electricTypes
TaxiOffer --> "1" Money : total
TaxiOffer --> "1" Money : deposit

@enduml
~~~

## Business Rules

~~~text
BR-FILTER-TAXIS-01 - Refinement Cannot Escape The Accepted Search
Source: Assumption
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
post BR_FILTER_TAXIS_01_RefinementCannotEscapeTheAcceptedSearch:
  result->forAll(o | criteria.searchContextId = null or o.searchContextId = criteria.searchContextId)
~~~

~~~text
BR-FILTER-TAXIS-02 - Selected Car Categories Apply
Source: Figma
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
post BR_FILTER_TAXIS_02_SelectedCarCategoriesApply:
  result->forAll(o |
    criteria.vehicleCategories->isEmpty() or
    criteria.vehicleCategories->includes(o.vehicle.category))
~~~

~~~text
BR-FILTER-TAXIS-03 - Selected Deposit Bands Apply
Source: Figma
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
post BR_FILTER_TAXIS_03_SelectedDepositBandsApply:
  result->forAll(o | RentalFilter::depositMatches(criteria.depositBands, o.deposit))
~~~

~~~text
BR-FILTER-TAXIS-04 - Selected Electric Types Apply
Source: Figma
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
post BR_FILTER_TAXIS_04_SelectedElectricTypesApply:
  result->forAll(o | RentalFilter::electricMatches(criteria.electricTypes, o.vehicle.electricType))
~~~

~~~text
BR-FILTER-TAXIS-05 - Changed Refinement Starts A New Result Traversal
Source: Assumption
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
pre BR_FILTER_TAXIS_05_ChangedRefinementStartsANewResultTraversal:
  criteria.offset >= 0 and criteria.limit > 0 and
  (SearchSnapshot::refinementChanged(criteria) implies criteria.offset = 0)
~~~

~~~text
BR-FILTER-TAXIS-06 - Top Picks Order Is Deterministic
Source: Figma
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
post BR_FILTER_TAXIS_06_TopPicksOrderIsDeterministic:
  criteria.sort = TaxiSort::TOP_PICKS implies
    (result->size() <= 1 or Sequence{1..result->size() - 1}->forAll(i |
      result->at(i).recommendationScore > result->at(i + 1).recommendationScore or
      (result->at(i).recommendationScore = result->at(i + 1).recommendationScore and
       result->at(i).id < result->at(i + 1).id)))
~~~

~~~text
BR-FILTER-TAXIS-07 - Optional Price Bounds Are Coherent
Source: Assumption
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
pre BR_FILTER_TAXIS_07_OptionalPriceBoundsAreCoherent:
  (criteria.minPrice = null or criteria.minPrice >= 0) and
  (criteria.maxPrice = null or criteria.maxPrice >= 0) and
  (criteria.minPrice = null or criteria.maxPrice = null or criteria.minPrice <= criteria.maxPrice)
~~~

~~~text
BR-FILTER-TAXIS-08 - Continuation References A Usable Snapshot
Source: Assumption
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
pre BR_FILTER_TAXIS_08_ContinuationReferencesAUsableSnapshot:
  (criteria.searchContextId = null and criteria.snapshotVersion = null) or
  (criteria.searchContextId <> null and criteria.snapshotVersion <> null and
   SearchSnapshot::accepts(criteria, RequestContext::startedAt))
~~~

~~~text
BR-FILTER-TAXIS-09 - Price Bounds Apply With The Visible Filters
Source: Assumption
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
post BR_FILTER_TAXIS_09_PriceBoundsApplyWithTheVisibleFilters:
  result->forAll(o |
    (criteria.minPrice = null or o.total.amount >= criteria.minPrice) and
    (criteria.maxPrice = null or o.total.amount <= criteria.maxPrice))
~~~
