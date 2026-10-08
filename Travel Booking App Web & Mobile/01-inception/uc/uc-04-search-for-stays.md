---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-04
uc_name: "Search for Stays"
---

# UC-04: Search for Stays

## Functional Use-Case Specification

### Use Case ID

UC-04

### Use Case Name

Search for Stays

### Description

As a traveller, I want to search by destination, dates, rooms, and guests so that I can find suitable stays.

### Actor(s)

Traveller; Stay Service.

### Priority

P0.

### Trigger

The traveller chooses to search for stays.

### Pre-Condition(s)

PRE-1: The traveller can access a stay-search interface.

### Post-Condition(s)

POST-1: The client displays the stay-search outcome returned by the system.

POST-2: The entered search context remains available for the next interaction.

### Basic Flow

1. The traveller opens the stay-search interface.
2. The client presents destination, travel-period, room, and guest controls.
3. The traveller enters or revises the search criteria and submits the search.
4. The client sends the selected criteria to the stay-search API.
5. The system processes the request and returns a search outcome.
6. The client renders the returned outcome and its available continuation.

### Alternative Flow

AF-1: Select a Suggested Destination

3a: While entering a destination, the traveller selects one of the returned location suggestions.

AF-2: Replace Stay Search from Results

6a: From the results view, the traveller reopens the search controls, changes the criteria, and submits a replacement search.

### Exception Flow

EF-1: Destination Suggestions Unavailable

3b: If destination suggestions are unavailable, the client keeps the search form visible and identifies the affected control.

EF-2: Stay Search Failure

5a: If the search cannot be completed, the client preserves the selected criteria and displays a retry action.

### Related UI

stays; stay search bar; check in date picker; check out date picker.

### Related API IDs

API-LOCATION-SUGGEST; API-STAY-SEARCH.

### Notes

None.

## UML Model

~~~plantuml
@startuml
hide empty members

class DateTime {
  +>(other: DateTime): Boolean
}

class RequestContext {
  +{static} startedAt: DateTime
}

class Location {
  +id: String
  +active: Boolean
  +timeZone: String
}

class Money {
  +amount: Real
  +currency: String
}

class DateRange {
  +start: Date
  +end: Date
}

class StayOffer {
  +period: DateRange
  +rooms: Integer
  +available: Boolean
  +total: Money
  +providerOfferRef: String
  +destinationId: String
  +adults: Integer
  +availableRooms: Integer
  +expiresAt: DateTime
}

class StayService {
  +search(criteria: StaySearchCriteria): Sequence(StayOffer)
}

class StaySearchCriteria {
  +destinationId: String
  +checkIn: Date
  +checkOut: Date
  +rooms: Integer
  +adults: Integer
  +currency: String
}

class BusinessCalendar {
  +{static} today(timeZone: String): Date
  +{static} nights(start: Date, end: Date): Integer
}

class Date {
  +>=(other: Date): Boolean
}

class ReadState {
  +{static} stayBookings(): String
}

StayOffer --> DateRange : period
StayOffer --> "1" Money : total

@enduml
~~~

## Business Rules

~~~text
BR-SEARCH-STAYS-01 - Destination Must Be Searchable
Source: Assumption
context StayService::search(criteria: StaySearchCriteria): Sequence(StayOffer)
pre BR_SEARCH_STAYS_01_DestinationMustBeSearchable:
  Location.allInstances()->one(d |
    d.id = criteria.destinationId and d.active)
~~~

~~~text
BR-SEARCH-STAYS-02 - Stay Falls Within The Sellable Window
Source: Assumption
context StayService::search(criteria: StaySearchCriteria): Sequence(StayOffer)
pre BR_SEARCH_STAYS_02_StayFallsWithinTheSellableWindow:
  let destination: Location =
    Location.allInstances()->any(d | d.id = criteria.destinationId) in
  criteria.checkIn >= BusinessCalendar::today(destination.timeZone) and
  BusinessCalendar::nights(criteria.checkIn, criteria.checkOut) >= 1 and
  BusinessCalendar::nights(criteria.checkIn, criteria.checkOut) <= 30
~~~

~~~text
BR-SEARCH-STAYS-03 - Occupancy Can Be Distributed Across Requested Rooms
Source: Assumption
context StayService::search(criteria: StaySearchCriteria): Sequence(StayOffer)
pre BR_SEARCH_STAYS_03_OccupancyCanBeDistributedAcrossRequestedRooms:
  criteria.rooms >= 1 and criteria.rooms <= 8 and
  criteria.adults >= criteria.rooms and
  criteria.adults <= criteria.rooms * 4
~~~

~~~text
BR-SEARCH-STAYS-04 - Returned Inventory Is Bound To The Search Context
Source: Assumption
context StayService::search(criteria: StaySearchCriteria): Sequence(StayOffer)
post BR_SEARCH_STAYS_04_ReturnedInventoryIsBoundToTheSearchContext:
  result->forAll(o |
    o.available and o.expiresAt > RequestContext::startedAt and
    o.destinationId = criteria.destinationId and
    o.period.start = criteria.checkIn and o.period.end = criteria.checkOut and
    o.rooms = criteria.rooms and o.adults = criteria.adults and
    o.availableRooms >= criteria.rooms)
~~~

~~~text
BR-SEARCH-STAYS-05 - Provider Inventory Is Deduplicated
Source: Assumption
context StayService::search(criteria: StaySearchCriteria): Sequence(StayOffer)
post BR_SEARCH_STAYS_05_ProviderInventoryIsDeduplicated:
  result->isUnique(o | o.providerOfferRef)
~~~

~~~text
BR-SEARCH-STAYS-06 - Search Does Not Reserve Inventory
Source: Assumption
context StayService::search(criteria: StaySearchCriteria): Sequence(StayOffer)
post BR_SEARCH_STAYS_06_SearchDoesNotReserveInventory:
  ReadState::stayBookings() = ReadState::stayBookings()@pre
~~~

~~~text
BR-SEARCH-STAYS-07 - Search Prices Use One Currency
Source: Assumption
context StayService::search(criteria: StaySearchCriteria): Sequence(StayOffer)
post BR_SEARCH_STAYS_07_SearchPricesUseOneCurrency:
  result->forAll(o |
    o.total.amount >= 0 and o.total.currency = criteria.currency)
~~~
