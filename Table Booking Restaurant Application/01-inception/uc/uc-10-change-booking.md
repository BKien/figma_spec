---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-10
uc_name: "Change a Booking"
---

# UC-10: Change a Booking

## Functional Use-Case Specification

### Use Case ID

UC-10

### Use Case Name

Change a Booking

### Description

A customer changes a future reservation from its booking view.

### Actor(s)

Customer; client; system.

### Priority

P0.

### Trigger

The customer chooses Edit Booking.

### Pre-Condition(s)

PRE-1: A booking detail is visible.

### Post-Condition(s)

POST-1: The client displays the updated booking result.

### Basic Flow

1. The customer opens the edit booking form.
2. The client displays current booking details and alternative controls.
3. The customer changes the booking and submits it.
4. The client sends the update request.
5. The system returns the booking outcome.
6. The client displays the returned booking.

### Alternative Flow

AF-1: Leave the Booking Edit Form

3a: The customer leaves the edit form and returns to the booking view.

### Exception Flow

EF-1: Booking Update Conflict

5a: The client displays the returned conflict and offers a fresh slot selection.

### Related UI

- [Edit Booking](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=3890-2970) (3890:2970)
- [edit booking mobile](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=4611-4659) (4611:4659)

### Related API IDs

- [API-BOOKING-UPDATE](../api/API-BOOKING-UPDATE.md)

### Notes

The UI establishes the interaction boundary. Rule values and persistence behavior are explicit assumptions in [ASSUMPTIONS.md](../../ASSUMPTIONS.md).

## UML Model

~~~plantuml
@startuml
hide empty members

enum BookingStatus {
  CONFIRMED
  CANCELLED
  COMPLETED
}

class Account {
  +id: String
}

class Restaurant {
  +id: String
}

class ReservationSlot {
  +id: String
  +restaurant: Restaurant
  +startsAt: DateTime
  +remainingSeats: Integer
}

class Booking {
  +id: String
  +account: Account
  +restaurant: Restaurant
  +slot: ReservationSlot
  +status: BookingStatus
  +partySize: Integer
  +version: Integer
}

class ChangeBookingCommand {
  +bookingId: String
  +slotId: String
  +partySize: Integer
  +version: Integer
}

class BookingService {
  +change(command: ChangeBookingCommand): Booking
}

class RequestContext <<utility>> {
  +{static} accountId: String
}

class DateTime <<primitive>> {
  +{static} now(): DateTime
}

Account "1" -- "*" Booking
Restaurant "1" -- "*" Booking
Restaurant "1" -- "*" ReservationSlot
ReservationSlot "1" -- "*" Booking
Booking --> "1" BookingStatus : status

@enduml
~~~

## Business Rules

~~~text
BR-CHANGE-BOOKING-01 - Owner And Editable State
Source: Assumption
context BookingService::change(command: ChangeBookingCommand): Booking
pre BR_CHANGE_BOOKING_01_OwnerAndEditableState:
  Booking.allInstances()->exists(b | b.id = command.bookingId and b.account.id = RequestContext::accountId and b.status = BookingStatus::CONFIRMED and b.slot.startsAt > DateTime::now())
~~~
~~~text
BR-CHANGE-BOOKING-02 - Fresh Slot And Version
Source: Assumption
context BookingService::change(command: ChangeBookingCommand): Booking
pre BR_CHANGE_BOOKING_02_FreshSlotAndVersion:
  ReservationSlot.allInstances()->exists(s | s.id = command.slotId and s.remainingSeats >= command.partySize) and Booking.allInstances()->exists(b | b.id = command.bookingId and b.version = command.version)
~~~
~~~text
BR-CHANGE-BOOKING-03 - Updated Booking Version
Source: Assumption
context BookingService::change(command: ChangeBookingCommand): Booking
post BR_CHANGE_BOOKING_03_UpdatedBookingVersion:
  result.id = command.bookingId and result.slot.id = command.slotId and result.version = command.version + 1
~~~
~~~text
BR-CHANGE-BOOKING-04 - Changed Party Size Is Persisted
Source: Assumption
context BookingService::change(command: ChangeBookingCommand): Booking
post BR_CHANGE_BOOKING_04_ChangedPartySizeIsPersisted:
  result.partySize = command.partySize
~~~
~~~text
BR-CHANGE-BOOKING-05 - Changed Party Size Is Positive
Source: Assumption
context BookingService::change(command: ChangeBookingCommand): Booking
pre BR_CHANGE_BOOKING_05_ChangedPartySizeIsPositive:
  command.partySize > 0
~~~
~~~text
BR-CHANGE-BOOKING-06 - Changed Slot Matches Restaurant
Source: Assumption
context BookingService::change(command: ChangeBookingCommand): Booking
pre BR_CHANGE_BOOKING_06_ChangedSlotMatchesRestaurant:
  Booking.allInstances()->exists(b | b.id = command.bookingId and ReservationSlot.allInstances()->exists(s | s.id = command.slotId and s.restaurant.id = b.restaurant.id and s.startsAt > DateTime::now()))
~~~
~~~text
BR-CHANGE-BOOKING-07 - Changed Booking Remains Confirmed
Source: Assumption
context BookingService::change(command: ChangeBookingCommand): Booking
post BR_CHANGE_BOOKING_07_ChangedBookingRemainsConfirmed:
  result.status = BookingStatus::CONFIRMED
~~~
