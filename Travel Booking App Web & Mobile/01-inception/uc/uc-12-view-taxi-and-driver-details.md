---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-12
uc_name: "View Taxi Rental and Driver Details"
---

# UC-12: View Taxi Rental and Driver Details

## Functional Use-Case Specification

### Use Case ID

UC-12

### Use Case Name

View Taxi Rental and Driver Details

### Description

As a traveller, I want to inspect the selected vehicle, assigned driver, rental period, allowance, and price before reserving it.

### Actor(s)

Traveller; Taxi Rental Service.

### Priority

P0.

### Trigger

The traveller chooses View Details for a Taxi offer.

### Pre-Condition(s)

PRE-1: A selected Taxi offer reference is available to the client.

### Post-Condition(s)

POST-1: The client displays the Taxi rental detail outcome returned by the system.
POST-2: Navigation back to the originating result context remains available.

### Basic Flow

1. The traveller selects View Details for a Taxi offer.
2. The client requests the detail associated with the selected offer.
3. The system processes the request and returns a detail outcome.
4. The client renders the vehicle, driver, pick-up and drop-off schedule, allowance, and price sections.
5. The traveller reviews the displayed sections.
6. The traveller may continue to the reservation form.

### Alternative Flow

AF-1:

1. The traveller returns to the preserved Taxi result context.

AF-2:

1. If an optional section is absent from the response, the client renders the remaining detail sections.

### Exception Flow

EF-1:

1. If the detail cannot be loaded, the client displays a retry state.
2. The client retains navigation back to the result view.

### Related UI

`Bajaj Details`; `Your Deal`; driver card; vehicle details; `Pick-up and drop-off`; price summary.

### Related API IDs

`API-TAXI-OFFER-DETAIL`.

## UML Model

~~~plantuml
@startuml
hide empty members

enum BookingStatus {
  PENDING
  CONFIRMED
  FAILED
  CANCELLED
}

class DateTime {
  +>(other: DateTime): Boolean
}

class RequestContext {
  +{static} authenticatedUserId: String
  +{static} startedAt: DateTime
}

class User {
  +id: String
}

class Location {
  +id: String
}

class Money {
  +amount: Real
  +currency: String
}

class TaxiOffer {
  +id: String
  +location: Location
  +pickupAt: DateTime
  +dropoffAt: DateTime
  +passengers: Integer
  +available: Boolean
  +total: Money
  +deposit: Money
  +mileageAllowanceKm: Real
  +rating: Real
  +driver: Driver
  +vehicle: Vehicle
  +locationId: String
  +expiresAt: DateTime
}

class Driver {
  +phone: String
}

class Vehicle {
  +registrationNumber: String
  +seatCapacity: Integer
}

class TaxiBooking {
  +user: User
  +offer: TaxiOffer
  +status: BookingStatus
}

class TaxiService {
  +getOffer(offerId: String): TaxiOfferDetail
}

class TaxiOfferDetail {
  +offer: TaxiOffer
  +driver: Driver
  +vehicle: Vehicle
  +displayedDriverPhone: String
  +displayedRegistration: String
}

class ReadState {
  +{static} taxiBookings(): String
}

TaxiOffer --> Location : location
TaxiOffer --> Driver : driver
TaxiOffer --> Vehicle : vehicle
TaxiBooking --> User : user
TaxiBooking --> TaxiOffer : offer
TaxiBooking --> BookingStatus : status
TaxiOfferDetail --> TaxiOffer : offer
TaxiOfferDetail --> Driver : driver
TaxiOfferDetail --> Vehicle : vehicle
TaxiOffer --> "1" Money : total
TaxiOffer --> "1" Money : deposit

@enduml
~~~

## Business Rules

~~~ocl
-- BR-UC-12-01
-- Source: Assumption
context TaxiService::getOffer(offerId: String): TaxiOfferDetail
post BR_UC_12_01_DetailIsLiveOrAccessibleThroughOwnedBooking:
  result <> null and result.offer.id = offerId and
  ((result.offer.available and result.offer.expiresAt > RequestContext::startedAt) or
   TaxiBooking.allInstances()->exists(b |
     b.user.id = RequestContext::authenticatedUserId and b.offer.id = offerId and
     Set{BookingStatus::PENDING, BookingStatus::CONFIRMED}->includes(b.status)))
~~~

~~~ocl
-- BR-UC-12-02
-- Source: Figma
context TaxiService::getOffer(offerId: String): TaxiOfferDetail
post BR_UC_12_02_DetailUsesTheOffersAssignedResources:
  result.driver = result.offer.driver and result.vehicle = result.offer.vehicle and
  result.vehicle.seatCapacity >= result.offer.passengers
~~~

~~~ocl
-- BR-UC-12-03
-- Source: Figma
context TaxiService::getOffer(offerId: String): TaxiOfferDetail
post BR_UC_12_03_DriverContactMatchesTheDisplayedAssignment:
  result.displayedDriverPhone = result.driver.phone
~~~

~~~ocl
-- BR-UC-12-04
-- Source: Figma
context TaxiService::getOffer(offerId: String): TaxiOfferDetail
post BR_UC_12_04_VehicleRegistrationMatchesTheDisplayedVehicle:
  result.displayedRegistration = result.vehicle.registrationNumber
~~~

~~~ocl
-- BR-UC-12-05
-- Source: Assumption
context TaxiService::getOffer(offerId: String): TaxiOfferDetail
post BR_UC_12_05_DetailRetrievalDoesNotAllocateTheOffer:
  ReadState::taxiBookings() = ReadState::taxiBookings()@pre
~~~

~~~ocl
-- BR-UC-12-06
-- Source: Figma
context TaxiService::getOffer(offerId: String): TaxiOfferDetail
post BR_UC_12_06_DisplayedRentalUsesOneLocationAndPositiveDuration:
  result.offer.location.id = result.offer.locationId and result.offer.dropoffAt > result.offer.pickupAt
~~~

~~~ocl
-- BR-UC-12-07
-- Source: Figma
context TaxiService::getOffer(offerId: String): TaxiOfferDetail
post BR_UC_12_07_DisplayedCommercialFactsAreCoherent:
  result.offer.total.amount >= 0 and result.offer.deposit.amount >= 0 and
  result.offer.total.currency = result.offer.deposit.currency and
  result.offer.mileageAllowanceKm >= 0 and result.offer.rating >= 0 and result.offer.rating <= 5
~~~
