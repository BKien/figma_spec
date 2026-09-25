# UC-14 — Search for Flights

### Description

As a traveller, I want to search for flights by route, dates, and passenger count.

### Actors

Traveller; Flight Service; External Flight Provider.

### Priority

P0.

### Trigger

**TRG-UC-14-01** — The traveller chooses to search for flights.

### Preconditions

- **PRE-UC-14-01** — The traveller can access the flight-search interface.

### Postconditions

- **POST-UC-14-01** — The client displays the flight-search outcome returned by the system.
- **POST-UC-14-02** — The entered search context remains available for the next interaction.

### Basic Flow

1. The traveller opens the flight-search interface.
2. The client presents route, trip-schedule, and passenger controls.
3. The traveller completes or revises the criteria and submits the search.
4. The client sends the selected criteria to the flight-search API.
5. The system processes the request and returns a search outcome.
6. The client renders the returned outcome and its available continuation.

### Alternative Flows

#### AF-UC-14-01

1. The traveller switches between the trip options exposed by the interface before submitting.

#### AF-UC-14-02

1. From flight results, the traveller reopens the search controls, revises the criteria, and submits a replacement search.

### Exception Flows

#### EF-UC-14-01

1. If the response identifies a partial result, the client renders the supplied partial-result state.

#### EF-UC-14-02

1. If the search cannot be completed, the client preserves the criteria and displays a retry action.

### UML Model

```plantuml
@startuml
hide empty members
enum FlightSort {
  CHEAPEST
  BEST
  QUICKEST
}
class String {
  +trim(): String
  +toLower(): String
  +matches(pattern: String): Boolean
  +includes(fragment: String): Boolean
  +concat(value: String): String
  +<(other: String): Boolean
}
class DateTime {
  +{static} now(): DateTime
  +{static} hoursBetween(start: DateTime, end: DateTime): Real
  +<(other: DateTime): Boolean
  +<=(other: DateTime): Boolean
  +>(other: DateTime): Boolean
  +>=(other: DateTime): Boolean
}
class RequestContext {
  +{static} authenticatedUserId: String
  +{static} startedAt: DateTime
}
class Location {
  +id: String
  +name: String
  +countryCode: String
  +active: Boolean
  +serviceAreaId: String
  +timeZone: String
  +airTravel: Boolean
}
class Money {
  +amount: Real
  +currency: String
}
class FlightOffer {
  +snapshotVersion: Integer
  +id: String
  +providerId: String
  +origin: Location
  +destination: Location
  +departureAt: DateTime
  +arrivalAt: DateTime
  +passengers: Integer
  +durationMinutes: Integer
  +available: Boolean
  +total: Money
  +expiresAt: DateTime
  +fareFingerprint: String
  +itinerarySignature: String
  +seatsRemaining: Integer
  +searchContextId: String
  +stopCount: Integer
  +bestScore: Real
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
  +minPrice: Real
  +maxPrice: Real
  +maxDurationMinutes: Integer
  +providerIds: String[*] {ordered}
  +sort: FlightSort
  +limit: Integer
  +offset: Integer
  +searchContextId: String
  +snapshotVersion: Integer
  +currency: String
}
class BusinessCalendar {
  +{static} today(timeZone: String): Date
  +{static} nights(start: Date, end: Date): Integer
}
class FlightSegment {
  +originId: String
  +destinationId: String
  +departureAt: DateTime
  +arrivalAt: DateTime
}
class FlightCalendar {
  +{static} localDate(value: DateTime, timeZone: String): Date
  +{static} minutesBetween(start: DateTime, end: DateTime): Integer
}
class FlightNormalization {
  +{static} signature(outbound: FlightSegment[*], inbound: FlightSegment[*]): String
}
class Date {
  +<(other: Date): Boolean
  +<=(other: Date): Boolean
  +>(other: Date): Boolean
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
FlightOffer --> Location : origin
FlightOffer --> Location : destination
FlightOffer "1" o-- "0..*" FlightSegment : outboundSegments
FlightOffer "1" o-- "0..*" FlightSegment : inboundSegments
FlightSearchCriteria --> FlightSort : sort
@enduml
```

### Business Rules

```ocl
-- BR-UC-14-01
-- Source: Assumption
context FlightService::search(criteria: FlightSearchCriteria): Sequence(FlightOffer)
pre BR_UC_14_01_RouteEndpointsAreActiveAirTravelLocations:
  Location.allInstances()->one(l | l.id = criteria.originId and l.active and l.airTravel) and
  Location.allInstances()->one(l | l.id = criteria.destinationId and l.active and l.airTravel)
```

```ocl
-- BR-UC-14-02
-- Source: Assumption
context FlightService::search(criteria: FlightSearchCriteria): Sequence(FlightOffer)
post BR_UC_14_02_EachJourneyConnectsItsRequestedEndpoints:
  result->forAll(o |
    FlightItinerary::connects(o.outboundSegments, criteria.originId, criteria.destinationId) and
    (if criteria.returnOn = null then o.inboundSegments->isEmpty()
     else FlightItinerary::connects(o.inboundSegments, criteria.destinationId, criteria.originId) endif))
```

```ocl
-- BR-UC-14-03
-- Source: Assumption
context FlightService::search(criteria: FlightSearchCriteria): Sequence(FlightOffer)
post BR_UC_14_03_ConnectionsRespectTheTransferWindowWithinEachJourney:
  result->forAll(o |
    FlightItinerary::hasValidConnections(o.outboundSegments, 45, 1440) and
    FlightItinerary::hasValidConnections(o.inboundSegments, 45, 1440))
```

```ocl
-- BR-UC-14-04
-- Source: Assumption
context FlightService::search(criteria: FlightSearchCriteria): Sequence(FlightOffer)
post BR_UC_14_04_JourneyDatesUseTheirDepartureLocalCalendars:
  let origin = Location.allInstances()->any(l | l.id = criteria.originId) in
  let destination = Location.allInstances()->any(l | l.id = criteria.destinationId) in
  result->forAll(o |
    FlightCalendar::localDate(o.outboundSegments->first().departureAt, origin.timeZone) = criteria.departOn and
    (criteria.returnOn <> null implies
      FlightCalendar::localDate(o.inboundSegments->first().departureAt, destination.timeZone) = criteria.returnOn and
      o.inboundSegments->first().departureAt > o.outboundSegments->last().arrivalAt))
```

```ocl
-- BR-UC-14-05
-- Source: Assumption
context FlightService::search(criteria: FlightSearchCriteria): Sequence(FlightOffer)
post BR_UC_14_05_OnlyLivePartySizedOffersAreSelectable:
  result->forAll(o |
    o.available and o.expiresAt > RequestContext::startedAt and
    o.seatsRemaining >= criteria.passengers)
```

```ocl
-- BR-UC-14-06
-- Source: Assumption
context FlightService::search(criteria: FlightSearchCriteria): Sequence(FlightOffer)
post BR_UC_14_06_ItineraryIdentityIsProviderNormalized:
  result->forAll(o |
    o.itinerarySignature = FlightNormalization::signature(o.outboundSegments, o.inboundSegments)) and
  result->isUnique(o | Tuple{provider = o.providerId, itinerary = o.itinerarySignature, fare = o.fareFingerprint})
```

```ocl
-- BR-UC-14-07
-- Source: Assumption
context FlightService::search(criteria: FlightSearchCriteria): Sequence(FlightOffer)
post BR_UC_14_07_SearchDoesNotReserveProviderInventory:
  ProviderInventory::reservations() = ProviderInventory::reservations()@pre
```

```ocl
-- BR-UC-14-08
-- Source: Assumption
context FlightService::search(criteria: FlightSearchCriteria): Sequence(FlightOffer)
pre BR_UC_14_08_RouteDatesAndPartyAreCoherent:
  criteria.originId <> criteria.destinationId and criteria.passengers >= 1 and
  criteria.departOn >= BusinessCalendar::today(Location.allInstances()->any(l | l.id = criteria.originId).timeZone) and
  (criteria.returnOn = null or criteria.returnOn >= criteria.departOn)
```

```ocl
-- BR-UC-14-09
-- Source: Assumption
context FlightService::search(criteria: FlightSearchCriteria): Sequence(FlightOffer)
post BR_UC_14_09_DurationAndStopsDescribeTheCompleteTrip:
  result->forAll(o |
    o.durationMinutes = FlightItinerary::duration(o.outboundSegments) + FlightItinerary::duration(o.inboundSegments) and
    o.stopCount = (o.outboundSegments->size() - 1).max(0) + (o.inboundSegments->size() - 1).max(0) and
    o.total.amount >= 0 and o.total.currency = criteria.currency)
```

### Related UI

`flights`; `flight destination`; `check in flight`; `check out flight`; `passengers`.

### Related APIs

`API-FLIGHT-SEARCH`.
