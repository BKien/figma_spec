---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-17
uc_name: "View Table Layout"
---

# UC-17: View Table Layout

## Functional Use-Case Specification

### Use Case ID

UC-17

### Use Case Name

View Table Layout

### Description

A manager views the restaurant table inventory and layout.

### Actor(s)

Restaurant Manager; client; system.

### Priority

P1.

### Trigger

The manager opens the table layout view.

### Pre-Condition(s)

PRE-1: The manager is in the administration panel.

### Post-Condition(s)

POST-1: The client displays returned table positions and labels.

### Basic Flow

1. The manager opens the table view.
2. The client requests table inventory.
3. The system returns tables and layout positions.
4. The client renders the table layout.

### Alternative Flow

AF-1: Open a Table Detail Panel

4a: The manager selects a table to view its detail panel.

### Exception Flow

EF-1: Table Layout Loading Error

3a: The client displays a table-view loading error and retry action.

### Related UI

- [list of tables](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=3387-3558) (3387:3558)
- [table layout](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=4657-6383) (4657:6383)

### Related API IDs

- [API-ADMIN-TABLE-LIST](../api/API-ADMIN-TABLE-LIST.md)

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

class Restaurant {
  +id: String
}

class DiningTable {
  +id: String
  +restaurant: Restaurant
  +label: String
  +capacity: Integer
  +layoutX: Integer
  +layoutY: Integer
}

class RestaurantId {
  +value: String
}

class AdminService {
  +tables(command: RestaurantId): Sequence(DiningTable)
}

class RequestContext <<utility>> {
  +{static} restaurantId: String
  +{static} role: Role
}

Restaurant "1" -- "*" DiningTable
RequestContext --> "1" Role : role

@enduml
~~~

## Business Rules

~~~text
BR-TABLE-LAYOUT-01 - Table Scope Authorized
Source: Assumption
context AdminService::tables(command: RestaurantId): Sequence(DiningTable)
pre BR_TABLE_LAYOUT_01_TableScopeAuthorized:
  RequestContext::role = Role::SUPER_ADMIN or RequestContext::restaurantId = command.value
~~~
~~~text
BR-TABLE-LAYOUT-02 - Tables Belong To Restaurant
Source: Assumption
context AdminService::tables(command: RestaurantId): Sequence(DiningTable)
post BR_TABLE_LAYOUT_02_TablesBelongToRestaurant:
  result->forAll(t | t.restaurant.id = command.value)
~~~
~~~text
BR-TABLE-LAYOUT-03 - Table Viewer Has Admin Role
Source: Assumption
context AdminService::tables(command: RestaurantId): Sequence(DiningTable)
pre BR_TABLE_LAYOUT_03_TableViewerHasAdminRole:
  RequestContext::role = Role::MANAGER or RequestContext::role = Role::SUPER_ADMIN
~~~
~~~text
BR-TABLE-LAYOUT-04 - Layout Tables Are Unique
Source: Assumption
context AdminService::tables(command: RestaurantId): Sequence(DiningTable)
post BR_TABLE_LAYOUT_04_LayoutTablesAreUnique:
  result->isUnique(t | t.id)
~~~
~~~text
BR-TABLE-LAYOUT-05 - Table Labels Are Unique Per Restaurant
Source: Assumption
context AdminService::tables(command: RestaurantId): Sequence(DiningTable)
post BR_TABLE_LAYOUT_05_TableLabelsAreUniquePerRestaurant:
  result->isUnique(t | t.label)
~~~
~~~text
BR-TABLE-LAYOUT-06 - Table Capacity Is Positive
Source: Assumption
context AdminService::tables(command: RestaurantId): Sequence(DiningTable)
post BR_TABLE_LAYOUT_06_TableCapacityIsPositive:
  result->forAll(t | t.capacity > 0)
~~~
~~~text
BR-TABLE-LAYOUT-07 - Table Coordinates Are Nonnegative
Source: Assumption
context AdminService::tables(command: RestaurantId): Sequence(DiningTable)
post BR_TABLE_LAYOUT_07_TableCoordinatesAreNonnegative:
  result->forAll(t | t.layoutX >= 0 and t.layoutY >= 0)
~~~
