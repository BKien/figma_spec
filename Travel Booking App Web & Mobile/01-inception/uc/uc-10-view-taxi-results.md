---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-10
uc_name: "View Taxi Rental Results"
---

# UC-10: View Taxi Rental Results

## Functional Use-Case Specification

### Use Case ID

UC-10

### Use Case Name

View Taxi Rental Results

### Description

As a traveller, I want to browse available vehicle-and-driver rental offers for my selected location and period.

### Actor(s)

Traveller; Taxi Rental Service.

### Priority

P0.

### Trigger

The client receives a taxi-rental search result context.

### Pre-Condition(s)

PRE-1: A taxi-rental search result context is available to the client.

### Post-Condition(s)

POST-1: The client displays the returned result-page state.

POST-2: The displayed rental context remains available for navigation or revision.

### Basic Flow

1. The client opens the Taxi results view for the current search context.
2. The client requests the corresponding result page.
3. The system processes the request and returns a page outcome.
4. The client renders the location and period summary with the returned vehicle cards.
5. The traveller reviews vehicle name, rating, capacity, transmission, baggage, mileage allowance, and price.
6. The traveller may select View Details for an offer.

### Alternative Flow

AF-1: Display No Taxi Results

4a: If the response contains no offer presentations, the client displays the designed no-results state and keeps the search summary available.

AF-2: Request Another Taxi Result Page

5a: The traveller requests another result page from the current search context.

### Exception Flow

EF-1: Additional Taxi Result Page Loading Failure

3a: If another result page cannot be loaded, the client keeps the displayed results and offers a retry.

EF-2: Unusable Taxi Search Context

3b: If the system returns an unusable-context outcome, the client presents the supplied recovery action.

### Related UI

taxi list; Kurunegala: 68 Cars available; vehicle result cards; View Details.

### Related API IDs

API-TAXI-SEARCH.

### Notes

None.

## UML Model

~~~plantuml
@startuml
hide empty members

class DateTime {
  +<=(other: DateTime): Boolean
  +>(other: DateTime): Boolean
}

class Money {
  +amount: Real
  +currency: String
}

class TaxiOffer {
  +id: String
  +available: Boolean
  +total: Money
  +mileageAllowanceKm: Real
  +rating: Real
  +vehicle: Vehicle
  +expiresAt: DateTime
  +searchContextId: String
  +snapshotVersion: Integer
  +rank: Integer
}

class Vehicle {
  +seatCapacity: Integer
  +smallBagCapacity: Integer
  +largeBagCapacity: Integer
}

class TaxiResultPage {
  +searchContextId: String
  +snapshotVersion: Integer
  +items: TaxiOffer[*] {ordered}
  +total: Integer
  +limit: Integer
  +offset: Integer
  +hasMore: Boolean
  +capturedAt: DateTime
  +validUntil: DateTime
  +orderedOfferIds: String[*] {ordered}
  +currency: String
}

TaxiOffer --> Vehicle : vehicle
TaxiResultPage "1" o-- "0..*" TaxiOffer : items
TaxiOffer --> "1" Money : total

@enduml
~~~

## Business Rules

~~~text
BR-TAXI-RESULTS-01 - Page Belongs To One Search Snapshot
Source: Assumption
context TaxiResultPage
inv BR_TAXI_RESULTS_01_PageBelongsToOneSearchSnapshot:
  self.items->forAll(o |
    o.searchContextId = self.searchContextId and o.snapshotVersion = self.snapshotVersion)
~~~

~~~text
BR-TAXI-RESULTS-02 - Page Metadata Matches Its Slice
Source: Assumption
context TaxiResultPage
inv BR_TAXI_RESULTS_02_PageMetadataMatchesItsSlice:
  self.total = self.orderedOfferIds->size() and self.limit > 0 and self.offset >= 0 and
  self.items->size() = (self.total - self.offset).max(0).min(self.limit) and
  self.hasMore = (self.offset + self.items->size() < self.total)
~~~

~~~text
BR-TAXI-RESULTS-03 - Page Inventory Was Live At Snapshot Creation
Source: Assumption
context TaxiResultPage
inv BR_TAXI_RESULTS_03_PageInventoryWasLiveAtSnapshotCreation:
  self.items->forAll(o | o.available and o.expiresAt > self.capturedAt) and
  self.validUntil > self.capturedAt and self.items->forAll(o | self.validUntil <= o.expiresAt)
~~~

~~~text
BR-TAXI-RESULTS-04 - Offer Identifiers Do Not Repeat Across The Page
Source: Assumption
context TaxiResultPage
inv BR_TAXI_RESULTS_04_OfferIdentifiersDoNotRepeatAcrossThePage:
  self.items->isUnique(o | o.id)
~~~

~~~text
BR-TAXI-RESULTS-05 - Presentation Order Is Stable Within The Snapshot
Source: Assumption
context TaxiResultPage
inv BR_TAXI_RESULTS_05_PresentationOrderIsStableWithinTheSnapshot:
  self.items->size() <= 1 or
  Sequence{1..self.items->size() - 1}->forAll(i |
    self.items->at(i).rank < self.items->at(i + 1).rank)
~~~

~~~text
BR-TAXI-RESULTS-06 - Page Is Exact Slice Of The Ordered Snapshot
Source: Assumption
context TaxiResultPage
inv BR_TAXI_RESULTS_06_PageIsExactSliceOfTheOrderedSnapshot:
  self.orderedOfferIds->isUnique(id | id) and
  (if self.items->isEmpty() then self.offset >= self.total
   else Sequence{1..self.items->size()}->forAll(i |
     self.items->at(i).id = self.orderedOfferIds->at(self.offset + i)) endif)
~~~

~~~text
BR-TAXI-RESULTS-07 - Cards Contain Comparable Rental Facts
Source: Figma
context TaxiResultPage
inv BR_TAXI_RESULTS_07_CardsContainComparableRentalFacts:
  self.items->forAll(o |
    o.total.currency = self.currency and o.total.amount >= 0 and o.rating >= 0 and o.rating <= 5 and
    o.vehicle.seatCapacity > 0 and o.vehicle.largeBagCapacity >= 0 and
    o.vehicle.smallBagCapacity >= 0 and o.mileageAllowanceKm >= 0)
~~~
