---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-05
uc_name: "View Restaurant Details"
---

# UC-05: View Restaurant Details

## Functional Use-Case Specification

### Use Case ID

UC-05

### Use Case Name

View Restaurant Details

### Description

A visitor views a restaurant profile before reserving a table.

### Actor(s)

Visitor; client; system.

### Priority

P0.

### Trigger

The visitor opens a restaurant card.

### Pre-Condition(s)

PRE-1: A restaurant card is visible.

### Post-Condition(s)

POST-1: The client displays the returned restaurant details.

### Basic Flow

1. The visitor selects a restaurant card.
2. The client requests the restaurant detail.
3. The system returns the restaurant profile.
4. The client displays photos, description, address, and booking entry point.

### Alternative Flow

AF-1: Open Menu or Reservation

4a: The visitor moves from the profile to the menu or reservation view.

### Exception Flow

EF-1: Restaurant Detail Unavailable

3a: The client shows an unavailable-detail state with a way back to results.

### Related UI

- [single restaurant view page](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=88-41) (88:41)
- [single restaurant page mobile](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=4594-4056) (4594:4056)

### Related API IDs

- [API-RESTAURANT-DETAIL](../api/API-RESTAURANT-DETAIL.md)

### Notes

The UI establishes the interaction boundary. Rule values and persistence behavior are explicit assumptions in [ASSUMPTIONS.md](../../ASSUMPTIONS.md).

## UML Model

~~~plantuml
@startuml
hide empty members

enum RestaurantStatus {
  DRAFT
  PUBLISHED
}

class Restaurant {
  +id: String
  +name: String
  +rating: Real
  +timezone: String
  +address: String
  +status: RestaurantStatus
}

class RestaurantId {
  +value: String
}

class RestaurantService {
  +detail(command: RestaurantId): Restaurant
}

Restaurant --> "1" RestaurantStatus : status

@enduml
~~~

## Business Rules

~~~text
BR-RESTAURANT-DETAIL-01 - Restaurant Is Published
Source: Assumption
context RestaurantService::detail(command: RestaurantId): Restaurant
pre BR_RESTAURANT_DETAIL_01_RestaurantIsPublished:
  Restaurant.allInstances()->exists(r | r.id = command.value and r.status = RestaurantStatus::PUBLISHED)
~~~
~~~text
BR-RESTAURANT-DETAIL-02 - Requested Restaurant Returned
Source: Assumption
context RestaurantService::detail(command: RestaurantId): Restaurant
post BR_RESTAURANT_DETAIL_02_RequestedRestaurantReturned:
  result.id = command.value
~~~
~~~text
BR-RESTAURANT-DETAIL-03 - Detail Remains Published
Source: Assumption
context RestaurantService::detail(command: RestaurantId): Restaurant
post BR_RESTAURANT_DETAIL_03_DetailRemainsPublished:
  result.status = RestaurantStatus::PUBLISHED
~~~
~~~text
BR-RESTAURANT-DETAIL-04 - Detail Name Is Present
Source: Assumption
context RestaurantService::detail(command: RestaurantId): Restaurant
post BR_RESTAURANT_DETAIL_04_DetailNameIsPresent:
  result.name.trim().size() > 0
~~~
~~~text
BR-RESTAURANT-DETAIL-05 - Detail Address Is Present
Source: Assumption
context RestaurantService::detail(command: RestaurantId): Restaurant
post BR_RESTAURANT_DETAIL_05_DetailAddressIsPresent:
  result.address.trim().size() > 0
~~~
~~~text
BR-RESTAURANT-DETAIL-06 - Detail Timezone Is Present
Source: Assumption
context RestaurantService::detail(command: RestaurantId): Restaurant
post BR_RESTAURANT_DETAIL_06_DetailTimezoneIsPresent:
  result.timezone.trim().size() > 0
~~~
~~~text
BR-RESTAURANT-DETAIL-07 - Detail Rating Is Bounded
Source: Assumption
context RestaurantService::detail(command: RestaurantId): Restaurant
post BR_RESTAURANT_DETAIL_07_DetailRatingIsBounded:
  result.rating >= 0 and result.rating <= 5
~~~
