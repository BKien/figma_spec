---
artifact_type: business-use-case-specification
status: "Draft"
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

AF-1:

1. The manager opens an individual booking from the table.

### Exception Flow

EF-1:

1. The client displays a bookings loading error and retry action.

### Related UI

- [Bookings](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=1000-2063) (`1000:2063`)
- [Super admin section](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=1000-4522) (`1000:4522`)

### Related API IDs

- [API-ADMIN-BOOKING-LIST](../api/api-admin-booking-list.md)

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

~~~ocl
-- BR-UC-15-01
-- Source: Assumption
context AdminService::bookings(command: AdminScope): Sequence(Booking)
pre BR_UC_15_01_ManagerHasRestaurantScope:
  RequestContext::role = Role::SUPER_ADMIN or (RequestContext::role = Role::MANAGER and RequestContext::restaurantId = command.restaurantId)
~~~
~~~ocl
-- BR-UC-15-02
-- Source: Assumption
context AdminService::bookings(command: AdminScope): Sequence(Booking)
post BR_UC_15_02_RowsStayInScope:
  result->forAll(b | b.restaurant.id = command.restaurantId)
~~~
~~~ocl
-- BR-UC-15-03
-- Source: Assumption
context AdminService::bookings(command: AdminScope): Sequence(Booking)
post BR_UC_15_03_AdminBookingRowsAreUnique:
  result->isUnique(b | b.id)
~~~
~~~ocl
-- BR-UC-15-04
-- Source: Assumption
context AdminService::bookings(command: AdminScope): Sequence(Booking)
post BR_UC_15_04_AdminBookingRowsHaveOwners:
  result->forAll(b | b.account <> null)
~~~
~~~ocl
-- BR-UC-15-05
-- Source: Assumption
context AdminService::bookings(command: AdminScope): Sequence(Booking)
post BR_UC_15_05_AdminBookingRowsHavePositiveParties:
  result->forAll(b | b.partySize > 0)
~~~
~~~ocl
-- BR-UC-15-06
-- Source: Assumption
context AdminService::bookings(command: AdminScope): Sequence(Booking)
post BR_UC_15_06_AdminBookingSlotsMatchRestaurants:
  result->forAll(b | b.slot.restaurant.id = b.restaurant.id)
~~~
~~~ocl
-- BR-UC-15-07
-- Source: Assumption
context AdminService::bookings(command: AdminScope): Sequence(Booking)
post BR_UC_15_07_AdminBookingRowsHaveCreationTime:
  result->forAll(b | b.createdAt <= DateTime::now())
~~~
