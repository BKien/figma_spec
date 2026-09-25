# UC-09 — View Booking History

### Description

A customer reviews reserved, completed, and cancelled bookings.

### Actors

Customer; client; system.

### Priority

P0.

### Trigger

**TRG-UC-09-01** — The customer opens History.

### Preconditions

- **PRE-UC-09-01** — The customer is signed in.

### Postconditions

- **POST-UC-09-01** — The client displays returned booking groups.

### Basic Flow

1. The customer opens booking history.
2. The client requests the customer's bookings.
3. The system returns booking summaries.
4. The client renders the history and status views.

### Alternative Flows

#### AF-UC-09-01

1. The customer opens a booking detail from the history list.

### Exception Flows

#### EF-UC-09-01

1. The client displays a history loading error and retry action.

### UML Model

```plantuml
@startuml

enum AccountStatus {
  PENDING_VERIFICATION
  ACTIVE
  SUSPENDED
}

enum RestaurantStatus {
  DRAFT
  PUBLISHED
}

enum BookingStatus {
  CONFIRMED
  CANCELLED
  COMPLETED
}

enum Role {
  CUSTOMER
  MANAGER
  SUPER_ADMIN
}

class Account {
  +id: String
  +emailCanonical: String
  +displayName: String
  +passwordHash: String
  +status: AccountStatus
  +version: Integer
  +pointsBalance: Integer
}

class Restaurant {
  +id: String
  +name: String
  +city: String
  +cuisine: String
  +rating: Real
  +timezone: String
  +address: String
  +status: RestaurantStatus
  +heroImageUrl: String
  +version: Integer
}

class ReservationSlot {
  +id: String
  +restaurant: Restaurant
  +date: Date
  +startsAt: DateTime
  +mealName: String
  +seatCapacity: Integer
  +remainingSeats: Integer
  +version: Integer
}

class Booking {
  +id: String
  +account: Account
  +restaurant: Restaurant
  +slot: ReservationSlot
  +status: BookingStatus
  +partySize: Integer
  +pointsUsed: Integer
  +contactPhoneEncrypted: String
  +idempotencyKey: String
  +requestFingerprint: String
  +version: Integer
  +createdAt: DateTime
}

class Notification {
  +id: String
  +account: Account
  +booking: Booking
  +title: String
  +body: String
  +createdAt: DateTime
}

class BookingService {
  +myBookings(): Sequence(Booking)
}

class RequestContext <<utility>> {
  +{static} accountId: String
  +{static} restaurantId: String
  +{static} role: Role
}

class Date <<primitive>> {
  +{static} today(): Date
}

class DateTime <<primitive>> {
  +{static} now(): DateTime
}

class SequenceUtils <<utility>> {
  +{static} isDescendingByCreatedAt(items: Sequence(Booking)): Boolean
  +{static} isDescendingByCreatedAt(items: Sequence(Notification)): Boolean
  +{static} isAscendingByStartTime(items: Sequence(ReservationSlot)): Boolean
}

Account "1" -- "*" Booking

Restaurant "1" -- "*" Booking

Restaurant "1" -- "*" ReservationSlot

ReservationSlot "1" -- "*" Booking

Account "1" -- "*" Notification

Booking "1" -- "*" Notification

@enduml
```

### Business Rules

```ocl
-- BR-UC-09-01
-- Source: Assumption
context BookingService::myBookings(): Sequence(Booking)
post BR_UC_09_01_HistoryIsOwned:
  result->forAll(b | b.account.id = RequestContext::accountId)
```
```ocl
-- BR-UC-09-02
-- Source: Assumption
context BookingService::myBookings(): Sequence(Booking)
post BR_UC_09_02_HistoryIsNewestFirst:
  SequenceUtils::isDescendingByCreatedAt(result)
```
```ocl
-- BR-UC-09-03
-- Source: Assumption
context BookingService::myBookings(): Sequence(Booking)
post BR_UC_09_03_HistoryRowsAreUnique:
  result->isUnique(b | b.id)
```
```ocl
-- BR-UC-09-04
-- Source: Assumption
context BookingService::myBookings(): Sequence(Booking)
post BR_UC_09_04_HistoryHasPositivePartySize:
  result->forAll(b | b.partySize > 0)
```
```ocl
-- BR-UC-09-05
-- Source: Assumption
context BookingService::myBookings(): Sequence(Booking)
post BR_UC_09_05_HistorySlotsMatchRestaurants:
  result->forAll(b | b.slot.restaurant.id = b.restaurant.id)
```
```ocl
-- BR-UC-09-06
-- Source: Assumption
context BookingService::myBookings(): Sequence(Booking)
post BR_UC_09_06_HistoryTimestampsArePast:
  result->forAll(b | b.createdAt <= DateTime::now())
```
```ocl
-- BR-UC-09-07
-- Source: Assumption
context BookingService::myBookings(): Sequence(Booking)
post BR_UC_09_07_HistoryPointsAreNonnegative:
  result->forAll(b | b.pointsUsed >= 0)
```

### Related UI

- [history](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=4611-4772) (`4611:4772`)
- [Reserved Table](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=772-1244) (`772:1244`)
- [Cancelled Booking](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=772-1245) (`772:1245`)
- [Completed Booking](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=772-1246) (`772:1246`)

### Related APIs

- [API-BOOKING-LIST](../api/api-booking-list.md)


### Notes

The UI establishes the interaction boundary. Rule values and persistence behavior are explicit assumptions in [ASSUMPTIONS.md](../ASSUMPTIONS.md).
