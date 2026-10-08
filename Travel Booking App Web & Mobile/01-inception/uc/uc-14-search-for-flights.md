---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-14
uc_name: "Search for Flights"
---

# UC-14: Search for Flights

## Functional Use-Case Specification

### Use Case ID

UC-14

### Use Case Name

Search for Flights

### Description

As a traveller, I want to search for flights by route, dates, and passenger count.

### Actor(s)

Traveller; Flight Service; External Flight Provider.

### Priority

P0.

### Trigger

The traveller chooses to search for flights.

### Pre-Condition(s)

PRE-1: The traveller can access the flight-search interface.

### Post-Condition(s)

POST-1: The client displays the flight-search outcome returned by the system.

POST-2: The entered search context remains available for the next interaction.

### Basic Flow

1. The traveller opens the flight-search interface.
2. The client presents route, trip-schedule, and passenger controls.
3. The traveller completes or revises the criteria and submits the search.
4. The client sends the selected criteria to the flight-search API.
5. The system processes the request and returns a search outcome.
6. The client renders the returned outcome and its available continuation.

### Alternative Flow

AF-1: Switch Flight Trip Options

3a: The traveller switches between the trip options exposed by the interface before submitting.

AF-2: Replace Flight Search from Results

6a: From flight results, the traveller reopens the search controls, revises the criteria, and submits a replacement search.

### Exception Flow

EF-1: Render Partial Flight Results

6b: If the response identifies a partial result, the client renders the supplied partial-result state.

EF-2: Flight Search Failure

5a: If the search cannot be completed, the client preserves the criteria and displays a retry action.

### Related UI

flights; flight destination; check in flight; check out flight; passengers.

### Related API IDs

API-FLIGHT-SEARCH.

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
  +airTravel: Boolean
}

class Money {
  +amount: Real
  +currency: String
}

class FlightOffer {
  +providerId: String
  +durationMinutes: Integer
  +available: Boolean
  +total: Money
  +expiresAt: DateTime
  +fareFingerprint: String
  +itinerarySignature: String
  +seatsRemaining: Integer
  +stopCount: Integer
  +outboundSegments: FlightSegment[*] {ordered}
  +inboundSegments: FlightSegment[*] {ordered}
}

class FlightService {
  +search(criteria: FlightSearchCriteria): Sequence(FlightOffer)
}

class FlightSearchCriteria {
  +originId: String
  +destinationId: String
  +departOn: Date
  +returnOn: Date
  +passengers: Integer
  +currency: String
}

class BusinessCalendar {
  +{static} today(timeZone: String): Date
}

class FlightSegment {
  +departureAt: DateTime
  +arrivalAt: DateTime
}

class FlightCalendar {
  +{static} localDate(value: DateTime, timeZone: String): Date
}

class FlightNormalization {
  +{static} signature(outbound: FlightSegment[*], inbound: FlightSegment[*]): String
}

class Date {
  +>=(other: Date): Boolean
}

class FlightItinerary {
  +{static} connects(segments: FlightSegment[*], originId: String, destinationId: String): Boolean
  +{static} hasValidConnections(segments: FlightSegment[*], minMinutes: Integer, maxMinutes: Integer): Boolean
  +{static} duration(segments: FlightSegment[*]): Integer
}

class ProviderInventory {
  +{static} reservations(): String
}

FlightOffer "1" o-- "0..*" FlightSegment : outboundSegments
FlightOffer "1" o-- "0..*" FlightSegment : inboundSegments
FlightOffer --> "1" Money : total

@enduml
~~~

## Business Rules

~~~text
BR-SEARCH-FLIGHTS-01 - Route Endpoints Are Active Air Travel Locations
Source: Assumption
context FlightService::search(criteria: FlightSearchCriteria): Sequence(FlightOffer)
pre BR_SEARCH_FLIGHTS_01_RouteEndpointsAreActiveAirTravelLocations:
  Location.allInstances()->one(l | l.id = criteria.originId and l.active and l.airTravel) and
  Location.allInstances()->one(l | l.id = criteria.destinationId and l.active and l.airTravel)
~~~

~~~text
BR-SEARCH-FLIGHTS-02 - Each Journey Connects Its Requested Endpoints
Source: Assumption
context FlightService::search(criteria: FlightSearchCriteria): Sequence(FlightOffer)
post BR_SEARCH_FLIGHTS_02_EachJourneyConnectsItsRequestedEndpoints:
  result->forAll(o |
    FlightItinerary::connects(o.outboundSegments, criteria.originId, criteria.destinationId) and
    (if criteria.returnOn = null then o.inboundSegments->isEmpty()
     else FlightItinerary::connects(o.inboundSegments, criteria.destinationId, criteria.originId) endif))
~~~

~~~text
BR-SEARCH-FLIGHTS-03 - Connections Respect The Transfer Window Within Each Journey
Source: Assumption
context FlightService::search(criteria: FlightSearchCriteria): Sequence(FlightOffer)
post BR_SEARCH_FLIGHTS_03_ConnectionsRespectTheTransferWindowWithinEachJourney:
  result->forAll(o |
    FlightItinerary::hasValidConnections(o.outboundSegments, 45, 1440) and
    FlightItinerary::hasValidConnections(o.inboundSegments, 45, 1440))
~~~

~~~text
BR-SEARCH-FLIGHTS-04 - Journey Dates Use Their Departure Local Calendars
Source: Assumption
context FlightService::search(criteria: FlightSearchCriteria): Sequence(FlightOffer)
post BR_SEARCH_FLIGHTS_04_JourneyDatesUseTheirDepartureLocalCalendars:
  let origin = Location.allInstances()->any(l | l.id = criteria.originId) in
  let destination = Location.allInstances()->any(l | l.id = criteria.destinationId) in
  result->forAll(o |
    FlightCalendar::localDate(o.outboundSegments->first().departureAt, origin.timeZone) = criteria.departOn and
    (criteria.returnOn <> null implies
      FlightCalendar::localDate(o.inboundSegments->first().departureAt, destination.timeZone) = criteria.returnOn and
      o.inboundSegments->first().departureAt > o.outboundSegments->last().arrivalAt))
~~~

~~~text
BR-SEARCH-FLIGHTS-05 - Only Live Party Sized Offers Are Selectable
Source: Assumption
context FlightService::search(criteria: FlightSearchCriteria): Sequence(FlightOffer)
post BR_SEARCH_FLIGHTS_05_OnlyLivePartySizedOffersAreSelectable:
  result->forAll(o |
    o.available and o.expiresAt > RequestContext::startedAt and
    o.seatsRemaining >= criteria.passengers)
~~~

~~~text
BR-SEARCH-FLIGHTS-06 - Itinerary Identity Is Provider Normalized
Source: Assumption
context FlightService::search(criteria: FlightSearchCriteria): Sequence(FlightOffer)
post BR_SEARCH_FLIGHTS_06_ItineraryIdentityIsProviderNormalized:
  result->forAll(o |
    o.itinerarySignature = FlightNormalization::signature(o.outboundSegments, o.inboundSegments)) and
  result->isUnique(o | Tuple{provider = o.providerId, itinerary = o.itinerarySignature, fare = o.fareFingerprint})
~~~

~~~text
BR-SEARCH-FLIGHTS-07 - Search Does Not Reserve Provider Inventory
Source: Assumption
context FlightService::search(criteria: FlightSearchCriteria): Sequence(FlightOffer)
post BR_SEARCH_FLIGHTS_07_SearchDoesNotReserveProviderInventory:
  ProviderInventory::reservations() = ProviderInventory::reservations()@pre
~~~

~~~text
BR-SEARCH-FLIGHTS-08 - Route Dates And Party Are Coherent
Source: Assumption
context FlightService::search(criteria: FlightSearchCriteria): Sequence(FlightOffer)
pre BR_SEARCH_FLIGHTS_08_RouteDatesAndPartyAreCoherent:
  criteria.originId <> criteria.destinationId and criteria.passengers >= 1 and
  criteria.departOn >= BusinessCalendar::today(Location.allInstances()->any(l | l.id = criteria.originId).timeZone) and
  (criteria.returnOn = null or criteria.returnOn >= criteria.departOn)
~~~

~~~text
BR-SEARCH-FLIGHTS-09 - Duration And Stops Describe The Complete Trip
Source: Assumption
context FlightService::search(criteria: FlightSearchCriteria): Sequence(FlightOffer)
post BR_SEARCH_FLIGHTS_09_DurationAndStopsDescribeTheCompleteTrip:
  result->forAll(o |
    o.durationMinutes = FlightItinerary::duration(o.outboundSegments) + FlightItinerary::duration(o.inboundSegments) and
    o.stopCount = (o.outboundSegments->size() - 1).max(0) + (o.inboundSegments->size() - 1).max(0) and
    o.total.amount >= 0 and o.total.currency = criteria.currency)
~~~
