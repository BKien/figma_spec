---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-12
uc_name: "View My Trips"
---

# UC-12: View My Trips

## Functional Use-Case Specification

### Use Case ID

UC-12

### Use Case Name

View My Trips

### Description

As an authenticated user, I want to view my Tripma trips so that I can find bookings associated with my account.

### Actor(s)

Authenticated User

### Priority

Medium

### Trigger

The authenticated user opens the Tripma Your Trips experience.

### Pre-Condition(s)

PRE-1: An authenticated Tripma session is available.
PRE-2: Tripma can attempt to retrieve bookings for the current account.

### Post-Condition(s)

POST-1: When retrieval succeeds, Tripma presents the current account's trip collection.
POST-2: When retrieval cannot be completed, Tripma reports the outcome without changing any booking.

### Basic Flow

1. The authenticated user opens the Your Trips experience.
2. Tripma requests the current account's trips through API-MY-TRIPS-LIST.
3. The trip service evaluates the request according to the Business Rules.
4. API-MY-TRIPS-LIST returns the trip collection.
5. Tripma presents the returned trip summaries.
6. The authenticated user reviews the available trips.

### Alternative Flow

AF-1: Open a trip confirmation
6a. The authenticated user selects a trip whose booking status is CONFIRMED.
6b. Tripma invokes UC-06 — View Booking Confirmation for the selected booking.
6c. UC-12 does not redefine confirmation-detail behavior.

AF-2: Review a cancelled trip summary
6a. The authenticated user reviews a trip whose booking status is CANCELLED.
6b. Tripma keeps the user in the My Trips collection and presents the cancellation status carried by the summary.
6c. UC-12 does not invoke UC-06 for that cancelled booking.

AF-3: No trips are available
4a. API-MY-TRIPS-LIST returns an empty trip collection.
4b. Tripma presents the empty Your Trips experience.

### Exception Flow

EF-1: Authentication is unavailable
2a. If an authenticated session is unavailable, Tripma does not request an account trip collection.
2b. Tripma makes UC-08 — Sign In available.

EF-2: Request cannot be completed
2a. If Tripma cannot complete the request because of a technical failure, it presents a retryable error state.

### Related UI

Your Trips entry in the Tripma navbar; Your Trips experience

### Related API IDs

API-MY-TRIPS-LIST; API-BOOKING-CONFIRMATION-GET through UC-06

### Notes

Scope clarification: UC-12 lists bookings associated with the authenticated account. Booking confirmation details remain assigned to UC-06, itinerary sharing remains assigned to UC-09, and booking cancellation remains assigned to UC-14.

## UML Model

~~~plantuml
@startuml
hide empty members

enum BookingStatus {
  CONFIRMED
  CANCELLED
}

enum TripTimingStatus {
  UPCOMING
  COMPLETED
  CANCELLED
}

class User <<Entity>> {
  id: UUID [1]
}

class Booking <<Entity>> {
  id: UUID [1]
  userId: UUID [0..1]
  departingFlightId: UUID [1]
  returningFlightId: UUID [0..1]
  status: BookingStatus [1]
  total: Decimal [1]
  currency: String [1]
  createdAt: DateTime [1]
}

class Flight <<Entity>> {
  id: UUID [1]
}

class PassengerInfo <<Entity>> {
  bookingId: UUID [1]
}

class MyTripFlightDto <<DTO>> {
  flightId: UUID [1]
  date: DateTime [1]
  arrivalAt: DateTime [1]
}

class MyTripSummaryDto <<DTO>> {
  bookingId: UUID [1]
  bookingStatus: BookingStatus [1]
  timingStatus: TripTimingStatus [1]
  departingFlight: MyTripFlightDto [1]
  returningFlight: MyTripFlightDto [0..1]
  journeyEndAt: DateTime [1]
  passengerCount: Integer [1]
  total: Decimal [1]
  currency: String [1]
  bookedAt: DateTime [1]
}

class MyTripsDataDto <<DTO>> {
  upcomingTrips: MyTripSummaryDto [0..*]
  completedTrips: MyTripSummaryDto [0..*]
  cancelledTrips: MyTripSummaryDto [0..*]
}

class MyTripsResponseDto <<DTO>> {
  success: Boolean [1]
  data: MyTripsDataDto [0..1]
}

class MyTripsService <<Service>> {
  listMyTrips(currentUserId: UUID): MyTripsResponseDto
}

class PassengerBaggage <<Entity>> {
  id: UUID [1]
}

class PaymentInfo <<Entity>> {
  id: UUID [1]
}

class SeatAssignment <<Entity>> {
  id: UUID [1]
}

MyTripSummaryDto "1" *-- "1" MyTripFlightDto : departing flight
MyTripSummaryDto "1" *-- "0..1" MyTripFlightDto : returning flight
MyTripsDataDto "1" *-- "0..*" MyTripSummaryDto : upcoming trips
MyTripsDataDto "1" *-- "0..*" MyTripSummaryDto : completed trips
MyTripsDataDto "1" *-- "0..*" MyTripSummaryDto : cancelled trips
MyTripsResponseDto "1" *-- "0..1" MyTripsDataDto : data
MyTripsService ..> MyTripsResponseDto
MyTripsService ..> User
MyTripsService ..> Booking
MyTripsService ..> Flight
MyTripsService ..> PassengerInfo
Booking --> "1" BookingStatus : status
MyTripSummaryDto --> "1" BookingStatus : bookingStatus
MyTripSummaryDto --> "1" TripTimingStatus : timingStatus

@enduml
~~~

## Business Rules

The following rules are authoritative for Prompt E. OCL is preserved where applicable; technical or non-OCL constraints remain authoritative natural-language requirements.

~~~text
BR-TRIPS-001: Authenticated account
context MyTripsService::listMyTrips(
  currentUserId : UUID
) : MyTripsResponseDto
pre BR_TRIPS_001_User:
  not currentUserId.oclIsUndefined() and
  User.allInstances()->exists(user | user.id = currentUserId)


BR-TRIPS-002: Account booking scope
context MyTripsService::listMyTrips(
  currentUserId : UUID
) : MyTripsResponseDto
post BR_TRIPS_002_Scope:
  result.success implies
    let trips : Sequence(MyTripSummaryDto) =
      result.data.upcomingTrips
        ->union(result.data.completedTrips)
        ->union(result.data.cancelledTrips)
    in
      trips->isUnique(trip | trip.bookingId) and
      trips->size() = Booking.allInstances()->select(booking |
        booking.userId = currentUserId and
        Set { BookingStatus::CONFIRMED, BookingStatus::CANCELLED }
          ->includes(booking.status))->size() and
      trips->forAll(trip |
        Booking.allInstances()->exists(booking |
          booking.id = trip.bookingId and
          booking.userId = currentUserId and
          Set { BookingStatus::CONFIRMED, BookingStatus::CANCELLED }
            ->includes(booking.status)))


BR-TRIPS-003: Flight-leg projection
context MyTripsService::listMyTrips(
  currentUserId : UUID
) : MyTripsResponseDto
post BR_TRIPS_003_Flights:
  result.success implies
    result.data.upcomingTrips
      ->union(result.data.completedTrips)
      ->union(result.data.cancelledTrips)->forAll(trip |
      let booking : Booking = Booking.allInstances()->any(item |
        item.id = trip.bookingId)
      in
        trip.departingFlight.flightId = booking.departingFlightId and
        trip.returningFlight.oclIsUndefined() =
          booking.returningFlightId.oclIsUndefined() and
        (not trip.returningFlight.oclIsUndefined() implies
          trip.returningFlight.flightId = booking.returningFlightId))


BR-TRIPS-004: Journey end
context MyTripsService::listMyTrips(
  currentUserId : UUID
) : MyTripsResponseDto
post BR_TRIPS_004_JourneyEnd:
  result.success implies
    result.data.upcomingTrips
      ->union(result.data.completedTrips)
      ->union(result.data.cancelledTrips)->forAll(trip |
      trip.journeyEndAt =
        if trip.returningFlight.oclIsUndefined()
        then trip.departingFlight.arrivalAt
        else trip.returningFlight.arrivalAt
        endif)


BR-TRIPS-005: Trip timing
context MyTripsService::listMyTrips(
  currentUserId : UUID
) : MyTripsResponseDto
post BR_TRIPS_005_Timing:
  result.success implies
    result.data.upcomingTrips->forAll(trip |
      trip.bookingStatus = BookingStatus::CONFIRMED and
      trip.timingStatus = TripTimingStatus::UPCOMING and
      trip.journeyEndAt >= now()) and
    result.data.completedTrips->forAll(trip |
      trip.bookingStatus = BookingStatus::CONFIRMED and
      trip.timingStatus = TripTimingStatus::COMPLETED and
      trip.journeyEndAt < now()) and
    result.data.cancelledTrips->forAll(trip |
      trip.bookingStatus = BookingStatus::CANCELLED and
      trip.timingStatus = TripTimingStatus::CANCELLED)


BR-TRIPS-006: Trip ordering
context MyTripsService::listMyTrips(
  currentUserId : UUID
) : MyTripsResponseDto
post BR_TRIPS_006_Order:
  result.success implies
    result.data.upcomingTrips =
      result.data.upcomingTrips->sortedBy(trip | trip.departingFlight.date) and
    result.data.completedTrips =
      result.data.completedTrips->sortedBy(trip | trip.journeyEndAt)->reverse() and
    result.data.cancelledTrips =
      result.data.cancelledTrips->sortedBy(trip | trip.bookedAt)->reverse()


BR-TRIPS-007: Passenger count
context MyTripsService::listMyTrips(
  currentUserId : UUID
) : MyTripsResponseDto
post BR_TRIPS_007_Passengers:
  result.success implies
    result.data.upcomingTrips
      ->union(result.data.completedTrips)
      ->union(result.data.cancelledTrips)->forAll(trip |
      trip.passengerCount = PassengerInfo.allInstances()->select(passenger |
        passenger.bookingId = trip.bookingId)->size() and
      trip.passengerCount >= 1)


BR-TRIPS-008: Booking summary
context MyTripsService::listMyTrips(
  currentUserId : UUID
) : MyTripsResponseDto
post BR_TRIPS_008_Summary:
  result.success implies
    result.data.upcomingTrips
      ->union(result.data.completedTrips)
      ->union(result.data.cancelledTrips)->forAll(trip |
      let booking : Booking = Booking.allInstances()->any(item |
        item.id = trip.bookingId)
      in
        trip.bookingStatus = booking.status and
        trip.total = booking.total and
        trip.currency = booking.currency and
        trip.bookedAt = booking.createdAt and
        trip.total >= 0 and
        not trip.currency.oclIsUndefined() and
        trim(trip.currency) <> '')


BR-TRIPS-009: Empty collection
context MyTripsService::listMyTrips(
  currentUserId : UUID
) : MyTripsResponseDto
post BR_TRIPS_009_Empty:
  Booking.allInstances()->select(booking |
    booking.userId = currentUserId and
    Set { BookingStatus::CONFIRMED, BookingStatus::CANCELLED }
      ->includes(booking.status))->isEmpty()
  implies
    result.success and
    result.data.upcomingTrips->isEmpty() and
    result.data.completedTrips->isEmpty() and
    result.data.cancelledTrips->isEmpty()


BR-TRIPS-010: Sensitive trip-summary data
The My Trips response shall not contain passenger contact details, raw payment
credentials, payment tokens, passwords, password hashes, session tokens, or
booking-confirmation codes.


BR-TRIPS-011: Read-only retrieval
Calling API-MY-TRIPS-LIST shall not create, update, or delete User, Booking,
Flight, PassengerInfo, SeatAssignment, PassengerBaggage, or PaymentInfo records.

~~~
