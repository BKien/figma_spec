---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-01
uc_name: "Search Flights"
---

# UC-01: Search Flights

## Functional Use-Case Specification

### Use Case ID

UC-01

### Use Case Name

Search Flights

### Description

As a visitor, I want to provide my Tripma travel criteria so that I can review relevant flight options and supporting fare information.

### Actor(s)

Visitor

### Priority

High

### Trigger

The visitor starts a flight search from a Tripma search entry point.

### Pre-Condition(s)

PRE-1: A Tripma flight-search entry point is accessible.

PRE-2: The data required to render the search controls can be retrieved.

### Post-Condition(s)

POST-1: When the search is accepted, Tripma presents the corresponding flight-search experience.

POST-2: When search data is returned, Tripma makes the result set and supporting fare information available to the results interface.

POST-3: When the search cannot be accepted, Tripma informs the visitor and does not start that search.

POST-4: When the results interface has no search context, Tripma presents an informational empty state.

### Basic Flow

1. The visitor opens a Tripma flight-search entry point.
2. Tripma displays the search controls and their supporting travel data.
3. The visitor provides route information.
4. The visitor provides trip timing information.
5. The visitor provides traveller information.
6. The visitor submits the search.
7. Tripma checks the submitted search according to the Business Rules of this use case.
8. Tripma establishes the search context and opens the flight-results experience.
9. Tripma requests flight-search data through API-FLIGHTS-SEARCH.
10. The search service evaluates the request according to the Business Rules of this use case.
11. The search service obtains the relevant Tripma flight and fare data.
12. The search service returns the API-FLIGHTS-SEARCH response.
13. Tripma presents the flight options, fare information, and route context to the visitor.

### Alternative Flow

AF-1: Refine displayed flights

13a: The visitor chooses one or more refinements offered by the results interface.

13b: Tripma refreshes the displayed flight options using the selected refinements.

AF-2: Clear flight filters

13c: The visitor clears the active refinements.

13d: Tripma restores the result presentation for the current search context.

AF-3: Change search criteria

13e: The visitor edits the current travel criteria.

13f: The visitor submits the revised search.

13g: The Basic Flow resumes at step 7.

### Exception Flow

EF-1: No flights available

11a: If the search service has no flight options to return, it returns a successful response with empty flight collections.

11b: Tripma presents a contextual no-results state and any supporting fare information supplied by the response.

EF-2: Client-side validation failure

7a: If the submitted search does not satisfy the Business Rules, Tripma identifies the affected input and does not send the flight-search request.

EF-3: Invalid backend request

10a: If the request is rejected by the search service, the service returns the API-FLIGHTS-SEARCH client-error response.

10b: Tripma informs the visitor that the search needs attention.

EF-4: Network/Server error

9a: If Tripma cannot complete the request because of a technical failure, it presents a recoverable error state.

### Related UI

Homepage search; flight-results page; search controls; flight filters; route map; fare grid; fare history

### Related API IDs

API-FLIGHTS-SEARCH

### Notes

Scope clarification: This use case covers discovering flight options. Selecting a flight and creating a booking are outside scope.

## UML Model

~~~plantuml
@startuml
hide empty members

class City <<Entity>> {
  id: UUID [1]
  name: String [1]
}

class Flight <<Entity>> {
  id: UUID [1]
}

enum SeatClass {
  ECONOMY
  BUSINESS
}

class RoutePriceHistory <<Entity>> {
  originCityId: UUID [1]
  destinationCityId: UUID [1]
  recordedAt: DateTime [1]
  price: Decimal [1]
  currency: String [1]
}

class SearchDto <<DTO>> {
  fromCity: String [1]
  toCity: String [1]
  startDate: Date [1]
  endDate: Date [0..1]
  adults: Integer [1]
  minors: Integer [1]
  type: Boolean [1]
}

class FlightDto <<DTO>> {
  fromCity: String [1]
  toCity: String [1]
  type: Boolean [1]
  subtotalPrice: Decimal [1]
  taxesAndFees: Decimal [1]
  airlineName: String [1]
  date: DateTime [1]
  availableSeats: Integer [1]
  availableSeatClasses: SeatClass [1..*]
  stopsNumber: Integer [1]
}

class PriceGridDto <<DTO>> {
  departingDate: Date [1]
  returningDate: Date [0..1]
  minPrice: Decimal [1]
}

class PriceHistoryDto <<DTO>> {
  recordedDate: Date [1]
  averagePrice: Decimal [1]
}

class PriceRatingDto <<DTO>> {
  ' Only the type is referenced by this use case's Business Rules.
}

enum DepartureTimeBand {
  MORNING
  AFTERNOON
  EVENING
}

class FlightFilterDto <<DTO>> {
  maxTotalPrice: Decimal [0..1]
  departureTimeBand: DepartureTimeBand [0..1]
  airlines: String [0..*]
  stopCounts: Integer [0..*]
  seatClasses: SeatClass [0..*]
}

class SearchResponseDto <<DTO>> {
  currency: String [1]
  departingFlights: FlightDto [0..*]
  arrivingFlights: FlightDto [0..*]
  priceGrid: PriceGridDto [0..*]
  priceHistory: PriceHistoryDto [0..*]
  priceRating: PriceRatingDto [0..1]
}

class FlightService <<Service>> {
  search(dto: SearchDto): SearchResponseDto
  priceGridMinimum(search: SearchDto, gridItem: PriceGridDto): Decimal {query}
  priceRatingFor(flights: FlightDto [0..*], priceHistory: PriceHistoryDto [0..*]): PriceRatingDto [0..1] {query}
}

class FlightFilterService <<Service>> {
  apply(flights: FlightDto [0..*], filter: FlightFilterDto): FlightDto [0..*]
}

FlightService ..> SearchDto
FlightService ..> SearchResponseDto
FlightFilterService ..> FlightFilterDto
FlightFilterService ..> FlightDto
SearchResponseDto "1" -- "0..*" FlightDto : contains
SearchResponseDto "1" -- "0..*" PriceGridDto : contains
SearchResponseDto "1" -- "0..*" PriceHistoryDto : contains
SearchResponseDto "1" -- "0..1" PriceRatingDto : contains
FlightDto ..> Flight : maps from
PriceHistoryDto ..> RoutePriceHistory : aggregates from
FlightDto --> "1..*" SeatClass : availableSeatClasses
FlightFilterDto --> "0..1" DepartureTimeBand : departureTimeBand
FlightFilterDto --> "0..*" SeatClass : seatClasses

note right of FlightDto
  availableSeats is a calculated field 
  derived from the count of related Seat 
  entities where available = true.

  availableSeatClasses is calculated from
  the classes of those available seats.

  type is projected from SearchDto.type;
  it is not persisted on Flight.
end note

note right of SearchDto
  type = false represents one-way.
  type = true represents round-trip.
end note

note right of FlightFilterDto
  maxTotalPrice is expressed in the
  SearchResponseDto.currency of the
  currently displayed search result.
end note

@enduml
~~~

## Business Rules

The following rules are authoritative for Prompt E. OCL is preserved where supplied; technical or non-OCL constraints remain authoritative natural-language requirements.

~~~text
BR-SEARCH-001 - Valid passenger count
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
pre BR_SEARCH_001_NonNegative:
  dto.adults >= 0 and dto.minors >= 0
pre BR_SEARCH_001_TotalPassengers:
  let totalPassengers : Integer = dto.adults + dto.minors
  in
    totalPassengers > 0


BR-SEARCH-002 - Sufficient seating capacity
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
post BR_SEARCH_002_CapacityMet:
  let totalPassengers : Integer = dto.adults + dto.minors
  in
    result.departingFlights->forAll(flight | flight.availableSeats >= totalPassengers) and
    result.arrivingFlights->forAll(flight | flight.availableSeats >= totalPassengers)


BR-SEARCH-003 - Flight date boundaries
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
post BR_SEARCH_003_DepartingDateRange:
  result.departingFlights->forAll(flight |
    isOnLocalDate(flight.date, dto.startDate, dto.fromCity)
  )
post BR_SEARCH_003_ReturningDateRange:
  dto.type = true implies
    result.arrivingFlights->forAll(flight |
      isOnLocalDate(flight.date, dto.endDate, dto.toCity)
    )
BR-SEARCH-004 - Return-date presence
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
pre BR_SEARCH_004_EndDateRequired:
  dto.type = true implies not dto.endDate.oclIsUndefined()
pre BR_SEARCH_004_EndDateOmittedForOneWay:
  dto.type = false implies dto.endDate.oclIsUndefined()


BR-SEARCH-005 - Returned legs match the trip type
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
post BR_SEARCH_005_OnlyWhenRoundTrip:
  dto.type = false implies
    result.arrivingFlights->isEmpty()
post BR_SEARCH_005_TripTypeProjection:
  result.departingFlights->forAll(flight | flight.type = dto.type) and
  result.arrivingFlights->forAll(flight | flight.type = dto.type)


BR-SEARCH-006 - Flight city matching
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
post BR_SEARCH_006_DepartingCities:
  result.departingFlights->forAll(departingFlight |
    lower(trim(departingFlight.fromCity)) = lower(trim(dto.fromCity)) and
    lower(trim(departingFlight.toCity)) = lower(trim(dto.toCity))
  )
post BR_SEARCH_006_ReversedCities:
  result.arrivingFlights->forAll(arrivingFlight |
    lower(trim(arrivingFlight.fromCity)) = lower(trim(dto.toCity)) and
    lower(trim(arrivingFlight.toCity)) = lower(trim(dto.fromCity))
  )
Technical constraints:
The response must not silently omit a flight that satisfies every applicable eligibility rule for its leg.


BR-SEARCH-007 - Required and well-formed search input
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
pre BR_SEARCH_007_RequiredInput:
  not dto.fromCity.oclIsUndefined() and trim(dto.fromCity) <> '' and
  not dto.toCity.oclIsUndefined() and trim(dto.toCity) <> '' and
  not dto.startDate.oclIsUndefined() and
  not dto.adults.oclIsUndefined() and
  not dto.minors.oclIsUndefined() and
  not dto.type.oclIsUndefined()


BR-SEARCH-008 - Supported cities
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
pre BR_SEARCH_008_SupportedCities:
  isSupportedCity(dto.fromCity) and
  isSupportedCity(dto.toCity)


BR-SEARCH-009 - Distinct origin and destination
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
pre BR_SEARCH_009_DifferentCities:
  lower(trim(dto.fromCity)) <> lower(trim(dto.toCity))


BR-SEARCH-010 - Future departure date
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
pre BR_SEARCH_010_NoPastFlights:
  dto.startDate >= todayIn(
    timeZoneForCity(dto.fromCity)
  )


BR-SEARCH-011 - Valid date sequence for round trips
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
pre BR_SEARCH_011_ValidReturnDate:
  dto.type = true implies
    dto.endDate >= dto.startDate


BR-SEARCH-012 - Unaccompanied minor restriction
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
pre BR_SEARCH_012_AdultRequiredForMinors:
  dto.minors > 0 implies dto.adults >= 1


BR-SEARCH-013 - Maximum passenger limit
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
pre BR_SEARCH_013_PassengerCap:
  let totalPassengers : Integer = dto.adults + dto.minors
  in
    totalPassengers <= 9


BR-SEARCH-014 - Advance booking horizon
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
pre BR_SEARCH_014_MaxFutureStartDate:
  dto.startDate <= todayIn(
    timeZoneForCity(dto.fromCity)
  ) + days(330)
pre BR_SEARCH_014_MaxFutureEndDate:
  dto.type = true implies
    dto.endDate <= todayIn(
      timeZoneForCity(dto.fromCity)
    ) + days(330)


BR-SEARCH-015 - Price-grid date range
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
post BR_SEARCH_015_PriceGridBounds:
  result.priceGrid->forAll(gridItem |
    gridItem.departingDate >= dto.startDate - days(3) and
    gridItem.departingDate <= dto.startDate + days(3) and
    gridItem.departingDate >= todayIn(timeZoneForCity(dto.fromCity)) and
    gridItem.departingDate <= todayIn(timeZoneForCity(dto.fromCity)) + days(330) and
    if dto.type = true then
      not gridItem.returningDate.oclIsUndefined() and
      gridItem.returningDate >= dto.endDate - days(3) and
      gridItem.returningDate <= dto.endDate + days(3) and
      gridItem.returningDate >= gridItem.departingDate and
      gridItem.returningDate <= todayIn(timeZoneForCity(dto.fromCity)) + days(330)
    else
      gridItem.returningDate.oclIsUndefined()
    endif
  )


BR-SEARCH-016 - Unique price-grid coordinates
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
post BR_SEARCH_016_UniqueGridCoordinates:
  result.priceGrid->isUnique(gridItem |
    Tuple {
      departingDate : Date = gridItem.departingDate,
      returningDate : Date = gridItem.returningDate
    }
  )
Technical constraints:
A grid coordinate is present exactly once only when the required eligible flight option or pair exists.


BR-SEARCH-017 - Minimum price for each grid coordinate
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
post BR_SEARCH_017_MinimumPrice:
  result.priceGrid->forAll(gridItem |
    gridItem.minPrice = priceGridMinimum(dto, gridItem)
  )


BR-SEARCH-018 - Price-history date range
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
post BR_SEARCH_018_HistoryBounds:
  let today : Date = todayIn(
        timeZoneForCity(dto.fromCity)
      )
  in
    result.priceHistory->forAll(historyItem |
      historyItem.recordedDate < today and
      historyItem.recordedDate >= today - days(30)
    )


BR-SEARCH-019 - Price-history sequence
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
post BR_SEARCH_019_OnePointPerRecordedDate:
  result.priceHistory->isUnique(historyItem | historyItem.recordedDate)
post BR_SEARCH_019_ChronologicalOrder:
  result.priceHistory->size() <= 1 or
  Sequence{1..result.priceHistory->size() - 1}->forAll(index |
    result.priceHistory->at(index).recordedDate <
      result.priceHistory->at(index + 1).recordedDate)


BR-SEARCH-020 - Fare history and price rating
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
post BR_SEARCH_020_DailyAverage:
  result.priceHistory->forAll(item |
    let observations : Set(RoutePriceHistory) =
      RoutePriceHistory.allInstances()->select(observation |
        City.allInstances()->exists(origin |
          origin.id = observation.originCityId and
          lower(trim(origin.name)) = lower(trim(dto.fromCity))) and
        City.allInstances()->exists(destination |
          destination.id = observation.destinationCityId and
          lower(trim(destination.name)) = lower(trim(dto.toCity))) and
        observation.currency = result.currency and
        localDate(
          observation.recordedAt,
          timeZoneForCity(dto.fromCity)
        ) = item.recordedDate)
    in
      not observations->isEmpty() and
      item.averagePrice =
        observations->collect(observation | observation.price)->sum() /
        observations->size()
  )
post BR_SEARCH_020_PriceRating:
  result.priceRating = priceRatingFor(
    result.departingFlights,
    result.priceHistory
  )
post BR_SEARCH_020_PriceRatingAvailability:
  (result.departingFlights->isEmpty() or result.priceHistory->isEmpty())
    implies result.priceRating.oclIsUndefined()
Technical constraints:
A date without an observation is omitted rather than represented by a fabricated zero value.


BR-SEARCH-021 - Monetary currency consistency
context FlightService::search(
  dto : SearchDto
) : SearchResponseDto
post BR_SEARCH_021_CurrencyDefined:
  not result.currency.oclIsUndefined() and trim(result.currency) <> ''
Technical constraints:
result.currency must be an ISO 4217 currency code.
Monetary values must be normalized to result.currency through the approved conversion and rounding policy before comparison or aggregation.


BR-SEARCH-022 - Active flight filters
context FlightFilterService::apply(
  flights : Sequence(FlightDto),
  filter : FlightFilterDto
) : Sequence(FlightDto)
pre BR_SEARCH_022_NonNegativeMaximumPrice:
  filter.maxTotalPrice.oclIsUndefined() or filter.maxTotalPrice >= 0
post BR_SEARCH_022_AllActiveFiltersMatch:
  result->forAll(flight |
    (filter.maxTotalPrice.oclIsUndefined() or
      flight.subtotalPrice + flight.taxesAndFees <= filter.maxTotalPrice) and
    (filter.departureTimeBand.oclIsUndefined() or
      timeBandIn(
        flight.date,
        timeZoneForCity(flight.fromCity)
      ) = filter.departureTimeBand) and
    (filter.airlines->isEmpty() or
      filter.airlines->exists(airline |
        lower(trim(airline)) = lower(trim(flight.airlineName))
      )) and
    (filter.stopCounts->isEmpty() or
      filter.stopCounts->includes(flight.stopsNumber)) and
    (filter.seatClasses->isEmpty() or
      flight.availableSeatClasses->exists(seatClass |
        filter.seatClasses->includes(seatClass)
      ))
  )


BR-SEARCH-023 - Filtered result remains a stable subset
context FlightFilterService::apply(
  flights : Sequence(FlightDto),
  filter : FlightFilterDto
) : Sequence(FlightDto)
post BR_SEARCH_023_ResultSubset:
  result->forAll(flight | flights->includes(flight))
Technical constraints:
Filtering preserves the input order and does not mutate the original search response; clearing filters restores that response order.
~~~
