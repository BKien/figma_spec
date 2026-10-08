---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-15
uc_name: "View Admin Bookings"
---

# UC-15: View Admin Bookings

## Functional Use-Case Specification

### Use Case ID

UC-15

### Use Case Name

View Admin Bookings

### Description

A manager reviews restaurant bookings in the administration panel.

### Actor(s)

Restaurant Manager; client; system.

### Priority

P0.

### Trigger

The manager opens Bookings.

### Pre-Condition(s)

PRE-1: The manager is in the administration panel.

### Post-Condition(s)

POST-1: The client displays booking rows and controls.

### Basic Flow

1. The manager opens Bookings.
2. The client requests booking rows.
3. The system returns booking summaries.
4. The client displays the table and available row actions.

### Alternative Flow

AF-1: Open an Individual Admin Booking

4a: The manager opens an individual booking from the table.

### Exception Flow

EF-1: Admin Bookings Loading Error

3a: The client displays a bookings loading error and retry action.

### Related UI

- [Bookings](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=1000-2063) (1000:2063)
- [Super admin section](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=1000-4522) (1000:4522)

### Related API IDs

- [API-ADMIN-BOOKING-LIST](../api/API-ADMIN-BOOKING-LIST.md)

### Notes

The UI establishes the interaction boundary. Rule values and persistence behavior are explicit assumptions in [ASSUMPTIONS.md](../../ASSUMPTIONS.md).

## UML Model

~~~plantuml
@startuml
hide empty members

enum Role {
  CUSTOMER
  MANAGER
  SUPER_ADMIN
}

class Account {
  +id: String
}

class Restaurant {
  +id: String
}

class ReservationSlot {
  +restaurant: Restaurant
}

class Booking {
  +id: String
  +account: Account
  +restaurant: Restaurant
  +slot: ReservationSlot
  +partySize: Integer
  +createdAt: DateTime
}

class AdminScope {
  +restaurantId: String
}

class AdminService {
  +bookings(command: AdminScope): Sequence(Booking)
}

class RequestContext <<utility>> {
  +{static} restaurantId: String
  +{static} role: Role
}

class DateTime <<primitive>> {
  +{static} now(): DateTime
}

Account "1" -- "*" Booking
Restaurant "1" -- "*" Booking
Restaurant "1" -- "*" ReservationSlot
ReservationSlot "1" -- "*" Booking
RequestContext --> "1" Role : role

@enduml
~~~

## Business Rules

~~~text
BR-ADMIN-BOOKINGS-01 - Manager Has Restaurant Scope
Source: Assumption
context AdminService::bookings(command: AdminScope): Sequence(Booking)
pre BR_ADMIN_BOOKINGS_01_ManagerHasRestaurantScope:
  RequestContext::role = Role::SUPER_ADMIN or (RequestContext::role = Role::MANAGER and RequestContext::restaurantId = command.restaurantId)
~~~
~~~text
BR-ADMIN-BOOKINGS-02 - Rows Stay In Scope
Source: Assumption
context AdminService::bookings(command: AdminScope): Sequence(Booking)
post BR_ADMIN_BOOKINGS_02_RowsStayInScope:
  result->forAll(b | b.restaurant.id = command.restaurantId)
~~~
~~~text
BR-ADMIN-BOOKINGS-03 - Admin Booking Rows Are Unique
Source: Assumption
context AdminService::bookings(command: AdminScope): Sequence(Booking)
post BR_ADMIN_BOOKINGS_03_AdminBookingRowsAreUnique:
  result->isUnique(b | b.id)
~~~
~~~text
BR-ADMIN-BOOKINGS-04 - Admin Booking Rows Have Owners
Source: Assumption
context AdminService::bookings(command: AdminScope): Sequence(Booking)
post BR_ADMIN_BOOKINGS_04_AdminBookingRowsHaveOwners:
  result->forAll(b | b.account <> null)
~~~
~~~text
BR-ADMIN-BOOKINGS-05 - Admin Booking Rows Have Positive Parties
Source: Assumption
context AdminService::bookings(command: AdminScope): Sequence(Booking)
post BR_ADMIN_BOOKINGS_05_AdminBookingRowsHavePositiveParties:
  result->forAll(b | b.partySize > 0)
~~~
~~~text
BR-ADMIN-BOOKINGS-06 - Admin Booking Slots Match Restaurants
Source: Assumption
context AdminService::bookings(command: AdminScope): Sequence(Booking)
post BR_ADMIN_BOOKINGS_06_AdminBookingSlotsMatchRestaurants:
  result->forAll(b | b.slot.restaurant.id = b.restaurant.id)
~~~
~~~text
BR-ADMIN-BOOKINGS-07 - Admin Booking Rows Have Creation Time
Source: Assumption
context AdminService::bookings(command: AdminScope): Sequence(Booking)
post BR_ADMIN_BOOKINGS_07_AdminBookingRowsHaveCreationTime:
  result->forAll(b | b.createdAt <= DateTime::now())
~~~
