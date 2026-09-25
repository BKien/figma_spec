# UC-09 — Search for Taxi Rentals

### Description

As a traveller, I want to search for a vehicle with a driver at a selected location and rental period.

### Actors

Traveller; Taxi Rental Service.

### Priority

P0.

### Trigger

**TRG-UC-09-01** — The traveller chooses the Taxi service.

### Preconditions

- **PRE-UC-09-01** — The traveller can access the Taxi search interface.

### Postconditions

- **POST-UC-09-01** — The client displays the taxi-rental search outcome returned by the system.
- **POST-UC-09-02** — The entered location and rental period remain available for the next interaction.

### Basic Flow

1. The traveller opens the Taxi search interface.
2. The client presents location, pick-up date and time, drop-off date and time, and passenger controls.
3. The traveller completes or revises the displayed controls and submits the search.
4. The client sends the selected criteria to the Taxi search API.
5. The system processes the request and returns a search outcome.
6. The client renders the returned outcome and its available continuation.

### Alternative Flows

#### AF-UC-09-01

1. The traveller selects the rental location from location suggestions.

#### AF-UC-09-02

1. From the results view, the traveller changes the displayed criteria and submits a replacement search.

### Exception Flows

#### EF-UC-09-01

1. If location suggestions are unavailable, the client identifies the affected control and retains the entered criteria.

#### EF-UC-09-02

1. If the search cannot be completed, the client preserves the criteria and displays a retry action.

### UML Model

```plantuml
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
enum TransmissionType {
  MANUAL
  AUTOMATIC
}
enum DepositBand {
  LKR_200_500
  LKR_500_1000
  LKR_1000_1200
  LKR_1200_1500
}
enum PaymentMode {
  ONLINE
  PAY_DRIVER
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
class TaxiOffer {
  +paymentMode: PaymentMode
  +id: String
  +location: Location
  +pickupAt: DateTime
  +dropoffAt: DateTime
  +passengers: Integer
  +available: Boolean
  +total: Money
  +deposit: Money
  +distanceFromCenterKm: Real
  +mileageAllowanceKm: Real
  +rating: Real
  +driver: Driver
  +vehicle: Vehicle
  +providerOfferRef: String
  +locationId: String
  +expiresAt: DateTime
  +searchContextId: String
  +snapshotVersion: Integer
  +rank: Integer
  +recommendationScore: Real
  +version: Integer
}
class Driver {
  +id: String
  +fullName: String
  +phone: String
  +active: Boolean
}
class Vehicle {
  +id: String
  +displayName: String
  +registrationNumber: String
  +seatCapacity: Integer
  +active: Boolean
  +category: VehicleCategory
  +transmission: TransmissionType
  +electricType: ElectricType
  +smallBagCapacity: Integer
  +largeBagCapacity: Integer
}
class TaxiService {
  +search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
}
class TaxiSearchCriteria {
  +locationId: String
  +pickupAt: DateTime
  +dropoffAt: DateTime
  +passengers: Integer
  +minPrice: Real
  +maxPrice: Real
  +sort: TaxiSort
  +limit: Integer
  +offset: Integer
  +searchContextId: String
  +snapshotVersion: Integer
  +currency: String
  +vehicleCategories: VehicleCategory[*] {ordered}
  +depositBands: DepositBand[*] {ordered}
  +electricTypes: ElectricType[*] {ordered}
}
class ServiceArea {
  +id: String
  +active: Boolean
}
class BusinessClock {
  +{static} now(timeZone: String): DateTime
  +{static} hoursBetween(start: DateTime, end: DateTime): Real
}
class AllocationCalendar {
  +{static} isFree(driverId: String, vehicleId: String, start: DateTime, end: DateTime): Boolean
}
class ReadState {
  +{static} users(): String
  +{static} sessions(): String
  +{static} stays(): String
  +{static} stayBookings(): String
  +{static} taxiBookings(): String
  +{static} payments(): String
  +{static} editorial(): String
  +{static} reviews(): String
}
TaxiOffer --> PaymentMode : paymentMode
TaxiOffer --> Location : location
TaxiOffer --> Driver : driver
TaxiOffer --> Vehicle : vehicle
Vehicle --> VehicleCategory : category
Vehicle --> TransmissionType : transmission
Vehicle --> ElectricType : electricType
TaxiSearchCriteria --> TaxiSort : sort
TaxiSearchCriteria "1" o-- "0..*" VehicleCategory : vehicleCategories
TaxiSearchCriteria "1" o-- "0..*" DepositBand : depositBands
TaxiSearchCriteria "1" o-- "0..*" ElectricType : electricTypes
@enduml
```

### Business Rules

```ocl
-- BR-UC-09-01
-- Source: Figma
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
pre BR_UC_09_01_RentalLocationIsSupported:
  Location.allInstances()->one(l | l.id = criteria.locationId and l.active and
    ServiceArea.allInstances()->one(a | a.id = l.serviceAreaId and a.active))
```

```ocl
-- BR-UC-09-02
-- Source: Assumption
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
pre BR_UC_09_02_PickupFallsWithinThePlanningWindow:
  let location: Location = Location.allInstances()->any(l | l.id = criteria.locationId) in
  BusinessClock::hoursBetween(BusinessClock::now(location.timeZone), criteria.pickupAt) >= 2 and
  BusinessClock::hoursBetween(BusinessClock::now(location.timeZone), criteria.pickupAt) <= 4320
```

```ocl
-- BR-UC-09-03
-- Source: Assumption
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
pre BR_UC_09_03_PartyFitsAnAvailableVehicleCategory:
  criteria.passengers >= 1 and criteria.passengers <= 16
```

```ocl
-- BR-UC-09-04
-- Source: Figma
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
post BR_UC_09_04_OffersMatchTheRequestedLocationAndPeriod:
  result->forAll(o |
    o.locationId = criteria.locationId and o.pickupAt = criteria.pickupAt and
    o.dropoffAt = criteria.dropoffAt and o.vehicle.seatCapacity >= criteria.passengers)
```

```ocl
-- BR-UC-09-05
-- Source: Assumption
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
post BR_UC_09_05_OfferedResourcesAreLiveAndUnallocated:
  result->forAll(o |
    o.available and o.expiresAt > RequestContext::startedAt and
    o.driver.active and o.vehicle.active and
    AllocationCalendar::isFree(o.driver.id, o.vehicle.id, o.pickupAt, o.dropoffAt))
```

```ocl
-- BR-UC-09-06
-- Source: Assumption
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
post BR_UC_09_06_ProviderInventoryIsDeduplicated:
  result->isUnique(o | o.providerOfferRef)
```

```ocl
-- BR-UC-09-07
-- Source: Assumption
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
post BR_UC_09_07_SearchDoesNotAllocateResources:
  ReadState::taxiBookings() = ReadState::taxiBookings()@pre
```

```ocl
-- BR-UC-09-08
-- Source: Figma
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
pre BR_UC_09_08_RentalPeriodHasPositiveDuration:
  criteria.dropoffAt > criteria.pickupAt
```

```ocl
-- BR-UC-09-09
-- Source: Assumption
context TaxiService::search(criteria: TaxiSearchCriteria): Sequence(TaxiOffer)
post BR_UC_09_09_SearchPricesUseOneCurrency:
  result->forAll(o |
    o.total.amount >= 0 and o.total.currency = criteria.currency and
    o.deposit.amount >= 0 and o.deposit.currency = criteria.currency)
```

### Related UI

`Taxi`; `taxi home page`; `Smooth Travels Start Here`; location control; `Pick-up Date & Time`; `Drop-off Date & Time`; `Passengers`.

### Related APIs

`API-LOCATION-SUGGEST`; `API-TAXI-SEARCH`.
