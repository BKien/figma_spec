# UC-11 — Filter and Sort Taxi Results

### Description

As a traveller, I want to filter and sort taxi offers by price, vehicle characteristics, or distance.

### Actors

Traveller; Taxi Service.

### Priority

P1.

### Trigger

**TRG-UC-11-01** — The traveller chooses to refine the displayed taxi results.

### Preconditions

- **PRE-UC-11-01** — The traveller is viewing taxi results for a search context.

### Postconditions

- **POST-UC-11-01** — The results view displays the refinement outcome returned by the system.
- **POST-UC-11-02** — The search context remains available for another result interaction.

### Basic Flow

1. The traveller opens the taxi filter or sort controls.
2. The client displays the current selections.
3. The traveller changes one or more selections and applies them.
4. The client submits the revised preferences with the current search context.
5. The system processes the request and returns a refinement outcome.
6. The client renders the returned result state and selections.

### Alternative Flows

#### AF-UC-11-01

1. The traveller clears the displayed refinements and requests the base result view.

#### AF-UC-11-02

1. On mobile, the traveller dismisses the filter panel without applying pending changes.

### Exception Flows

#### EF-UC-11-01

1. If the refresh cannot be completed, the client keeps the previously displayed result state.
2. The client presents the retry action returned for the failed refresh.

### UML Model

Classifiers and operations are defined in the [shared domain model](shared-domain-model.md).

```plantuml
@startuml
enum TaxiSort
class TaxiSearchCriteria
class TaxiOffer
@enduml
```

### Business Rules

```ocl
-- BR-UC-11-01
-- Source: Assumption
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
post BR_UC_11_01_RefinementCannotEscapeTheAcceptedSearch:
  result->forAll(o | (criteria.searchContextId = null or o.searchContextId = criteria.searchContextId))
```

```ocl
-- BR-UC-11-02
-- Source: Assumption
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
post BR_UC_11_02_AllAcceptedFiltersApplyTogether:
  result->forAll(o |
    (criteria.minPrice = null or o.total.amount >= criteria.minPrice) and
    (criteria.maxPrice = null or o.total.amount <= criteria.maxPrice) and
    o.seats >= criteria.passengers and
    (criteria.vehicleTypes->isEmpty() or criteria.vehicleTypes->includes(o.vehicle.vehicleType)))
```

```ocl
-- BR-UC-11-03
-- Source: Assumption
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
pre BR_UC_11_03_ChangedRefinementStartsANewResultTraversal:
  criteria.offset >= 0 and criteria.limit > 0 and
  (SearchSnapshot::refinementChanged(criteria) implies criteria.offset = 0)
```

```ocl
-- BR-UC-11-04
-- Source: Assumption
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
post BR_UC_11_04_PriceOrderUsesDistanceAndIdentifierAsTieBreakers:
  criteria.sort = TaxiSort::PRICE implies
    (result->size() <= 1 or
      Sequence{1..result->size() - 1}->forAll(i |
        result->at(i).total.amount < result->at(i + 1).total.amount or
        (result->at(i).total.amount = result->at(i + 1).total.amount and
          (result->at(i).distanceKm < result->at(i + 1).distanceKm or
           (result->at(i).distanceKm = result->at(i + 1).distanceKm and
            result->at(i).id < result->at(i + 1).id)))))
```

```ocl
-- BR-UC-11-05
-- Source: Assumption
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
post BR_UC_11_05_DistanceOrderUsesPriceAndIdentifierAsTieBreakers:
  criteria.sort = TaxiSort::DISTANCE implies
    (result->size() <= 1 or
      Sequence{1..result->size() - 1}->forAll(i |
        result->at(i).distanceKm < result->at(i + 1).distanceKm or
        (result->at(i).distanceKm = result->at(i + 1).distanceKm and
          (result->at(i).total.amount < result->at(i + 1).total.amount or
           (result->at(i).total.amount = result->at(i + 1).total.amount and
            result->at(i).id < result->at(i + 1).id)))))
```

```ocl
-- BR-UC-11-06
-- Source: Assumption
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
post BR_UC_11_06_RecommendedOrderIsDeterministic:
  criteria.sort = TaxiSort::RECOMMENDED implies
    (result->size() <= 1 or
      Sequence{1..result->size() - 1}->forAll(i |
        result->at(i).recommendationScore > result->at(i + 1).recommendationScore or
        (result->at(i).recommendationScore = result->at(i + 1).recommendationScore and
          result->at(i).id < result->at(i + 1).id)))
```

```ocl
-- BR-UC-11-07
-- Source: Assumption
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
pre BR_UC_11_07_OptionalFilterBoundsAreCoherent:
  (criteria.minPrice = null or criteria.minPrice >= 0) and
  (criteria.maxPrice = null or criteria.maxPrice >= 0) and
  (criteria.minPrice = null or criteria.maxPrice = null or criteria.minPrice <= criteria.maxPrice)
```

```ocl
-- BR-UC-11-08
-- Source: Assumption
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
pre BR_UC_11_08_ContinuationReferencesAUsableSnapshot:
  (criteria.searchContextId = null and criteria.snapshotVersion = null) or
  (criteria.searchContextId <> null and criteria.snapshotVersion <> null and
   SearchSnapshot::accepts(criteria, RequestContext::startedAt))
```

### Related UI

`taxi filter`; `taxi filters mobile`.

### Related APIs

`API-TAXI-SEARCH`.
