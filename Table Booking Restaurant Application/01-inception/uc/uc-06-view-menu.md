---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-06
uc_name: "View a Restaurant Menu"
---

# UC-06: View a Restaurant Menu

## Functional Use-Case Specification

### Use Case ID

UC-06

### Use Case Name

View a Restaurant Menu

### Description

A visitor opens the menu shown from a restaurant profile.

### Actor(s)

Visitor; client; system.

### Priority

P1.

### Trigger

The visitor chooses the menu action.

### Pre-Condition(s)

PRE-1: The restaurant profile is visible.

### Post-Condition(s)

POST-1: The client displays the returned menu items.

### Basic Flow

1. The visitor opens the restaurant menu.
2. The client requests menu content.
3. The system returns menu sections and items.
4. The client displays the menu overlay.

### Alternative Flow

AF-1: Close the Menu Overlay

4a: The visitor closes the overlay and returns to restaurant details.

### Exception Flow

EF-1: Menu Loading Error

3a: The client displays a menu loading error with a retry action.

### Related UI

- [menu card overlay](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=321-429) (321:429)
- [restaurant profile](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=88-41) (88:41)

### Related API IDs

- [API-MENU-LIST](../api/API-MENU-LIST.md)

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

enum MenuItemStatus {
  HIDDEN
  VISIBLE
}

class Restaurant {
  +id: String
  +status: RestaurantStatus
}

class MenuItem {
  +id: String
  +restaurant: Restaurant
  +name: String
  +sectionName: String
  +imageUrl: String
  +status: MenuItemStatus
}

class RestaurantId {
  +value: String
}

class RestaurantService {
  +menu(command: RestaurantId): Sequence(MenuItem)
}

Restaurant "1" -- "*" MenuItem
Restaurant --> "1" RestaurantStatus : status
MenuItem --> "1" MenuItemStatus : status

@enduml
~~~

## Business Rules

~~~text
BR-RESTAURANT-MENU-01 - Menu Belongs To Restaurant
Source: Assumption
context RestaurantService::menu(command: RestaurantId): Sequence(MenuItem)
post BR_RESTAURANT_MENU_01_MenuBelongsToRestaurant:
  result->forAll(i | i.restaurant.id = command.value)
~~~
~~~text
BR-RESTAURANT-MENU-02 - Visible Menu Items Only
Source: Assumption
context RestaurantService::menu(command: RestaurantId): Sequence(MenuItem)
post BR_RESTAURANT_MENU_02_VisibleMenuItemsOnly:
  result->forAll(i | i.status = MenuItemStatus::VISIBLE)
~~~
~~~text
BR-RESTAURANT-MENU-03 - Menu Restaurant Is Published
Source: Assumption
context RestaurantService::menu(command: RestaurantId): Sequence(MenuItem)
pre BR_RESTAURANT_MENU_03_MenuRestaurantIsPublished:
  Restaurant.allInstances()->exists(r | r.id = command.value and r.status = RestaurantStatus::PUBLISHED)
~~~
~~~text
BR-RESTAURANT-MENU-04 - Menu Items Are Unique
Source: Assumption
context RestaurantService::menu(command: RestaurantId): Sequence(MenuItem)
post BR_RESTAURANT_MENU_04_MenuItemsAreUnique:
  result->isUnique(i | i.id)
~~~
~~~text
BR-RESTAURANT-MENU-05 - Menu Item Names Are Present
Source: Assumption
context RestaurantService::menu(command: RestaurantId): Sequence(MenuItem)
post BR_RESTAURANT_MENU_05_MenuItemNamesArePresent:
  result->forAll(i | i.name.trim().size() > 0)
~~~
~~~text
BR-RESTAURANT-MENU-06 - Menu Sections Are Present
Source: Assumption
context RestaurantService::menu(command: RestaurantId): Sequence(MenuItem)
post BR_RESTAURANT_MENU_06_MenuSectionsArePresent:
  result->forAll(i | i.sectionName.trim().size() > 0)
~~~
~~~text
BR-RESTAURANT-MENU-07 - Menu Images Are Present
Source: Assumption
context RestaurantService::menu(command: RestaurantId): Sequence(MenuItem)
post BR_RESTAURANT_MENU_07_MenuImagesArePresent:
  result->forAll(i | i.imageUrl <> null and i.imageUrl.trim().size() > 0)
~~~
