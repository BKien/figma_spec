---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-03
uc_name: "Browse the Restaurant Home Page"
---

# UC-03: Browse the Restaurant Home Page

## Functional Use-Case Specification

### Use Case ID

UC-03

### Use Case Name

Browse the Restaurant Home Page

### Description

A visitor views featured restaurants and entry points on the home page.

### Actor(s)

Visitor; client; system.

### Priority

P0.

### Trigger

The visitor opens the home page.

### Pre-Condition(s)

PRE-1: The site is reachable.

### Post-Condition(s)

POST-1: The client presents the returned home content.

### Basic Flow

1. The visitor opens the home page.
2. The client requests home content.
3. The system returns restaurant cards and navigation content.
4. The client renders the cards and available actions.

### Alternative Flow

AF-1: Open a Featured Restaurant

4a: The visitor chooses a featured restaurant, and the client opens its detail view.

### Exception Flow

EF-1: Home Content Loading Failure

3a: The client displays a retry state when home content cannot be loaded.

### Related UI

- [home](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=102-170) (102:170)
- [home variant 1](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=278-790) (278:790)
- [home variant 2](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=173-362) (173:362)

### Related API IDs

- [API-HOME-GET](../api/API-HOME-GET.md)

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
  +city: String
  +rating: Real
  +status: RestaurantStatus
  +heroImageUrl: String
}

class DiscoveryService {
  +home(): Sequence(Restaurant)
}

Restaurant --> "1" RestaurantStatus : status

@enduml
~~~

## Business Rules

~~~text
BR-BROWSE-HOME-01 - Published Restaurants Only
Source: Assumption
context DiscoveryService::home(): Sequence(Restaurant)
post BR_BROWSE_HOME_01_PublishedRestaurantsOnly:
  result->forAll(r | r.status = RestaurantStatus::PUBLISHED)
~~~
~~~text
BR-BROWSE-HOME-02 - Featured Items Have Images
Source: Assumption
context DiscoveryService::home(): Sequence(Restaurant)
post BR_BROWSE_HOME_02_FeaturedItemsHaveImages:
  result->forAll(r | r.heroImageUrl <> null)
~~~
~~~text
BR-BROWSE-HOME-03 - Featured Restaurants Are Unique
Source: Assumption
context DiscoveryService::home(): Sequence(Restaurant)
post BR_BROWSE_HOME_03_FeaturedRestaurantsAreUnique:
  result->isUnique(r | r.id)
~~~
~~~text
BR-BROWSE-HOME-04 - Featured Names Are Present
Source: Assumption
context DiscoveryService::home(): Sequence(Restaurant)
post BR_BROWSE_HOME_04_FeaturedNamesArePresent:
  result->forAll(r | r.name.trim().size() > 0)
~~~
~~~text
BR-BROWSE-HOME-05 - Featured Cities Are Present
Source: Assumption
context DiscoveryService::home(): Sequence(Restaurant)
post BR_BROWSE_HOME_05_FeaturedCitiesArePresent:
  result->forAll(r | r.city.trim().size() > 0)
~~~
~~~text
BR-BROWSE-HOME-06 - Featured Ratings Are Bounded
Source: Assumption
context DiscoveryService::home(): Sequence(Restaurant)
post BR_BROWSE_HOME_06_FeaturedRatingsAreBounded:
  result->forAll(r | r.rating >= 0 and r.rating <= 5)
~~~
~~~text
BR-BROWSE-HOME-07 - Featured Images Are Nonempty
Source: Assumption
context DiscoveryService::home(): Sequence(Restaurant)
post BR_BROWSE_HOME_07_FeaturedImagesAreNonempty:
  result->forAll(r | r.heroImageUrl.trim().size() > 0)
~~~
