---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-11
uc_name: "View Unique Places"
---

# UC-11: View Unique Places

## Functional Use-Case Specification

### Use Case ID

UC-11

### Use Case Name

View Unique Places

### Description

As a visitor, I want to view unique places so that I can discover travel destinations.

### Actor(s)

Visitor

### Priority

Low

### Trigger

The visitor opens a Tripma experience that provides unique places.

### Pre-Condition(s)

PRE-1: The Tripma unique-places experience is available.
PRE-2: Tripma can attempt to retrieve the unique-place collection.

### Post-Condition(s)

POST-1: When retrieval succeeds, Tripma presents the returned unique-place collection.
POST-2: When retrieval cannot be completed, Tripma reports the outcome without changing unique-place data.

### Basic Flow

1. The visitor opens a Tripma experience containing unique places.
2. Tripma requests the unique-place collection through API-UNIQUE-PLACES-LIST.
3. The unique-place service evaluates the request according to the Business Rules.
4. API-UNIQUE-PLACES-LIST returns the unique-place collection.
5. Tripma presents the returned unique-place summaries.
6. The visitor reviews the available unique places.

### Alternative Flow

AF-1: View the complete unique-place collection
6a. The visitor requests the complete unique-place collection from the current experience.
6b. Tripma presents the complete collection returned by API-UNIQUE-PLACES-LIST.

AF-2: No unique places are available
4a. API-UNIQUE-PLACES-LIST returns an empty collection.
4b. Tripma presents the empty unique-places experience.

### Exception Flow

EF-1: Request cannot be completed
2a. If Tripma cannot complete the request because of a technical failure, it presents a retryable error state.

### Related UI

Unique Places experience available from the Tripma home experience

### Related API IDs

API-UNIQUE-PLACES-LIST

### Notes

Scope clarification: UC-11 retrieves and presents unique places only. It does not define flight searching, booking, or navigation after a place is viewed.

## UML Model

~~~plantuml
@startuml
hide empty members

class City <<Entity>> {
  id: UUID [1]
  name: String [1]
}

class UniquePlace <<Entity>> {
  id: UUID [1]
  destinationCityId: UUID [1]
  placeName: String [1]
  imagePath: String [1]
  price: Decimal [1]
  currency: String [1]
  description: String [1]
  motivation: String [1]
  active: Boolean [1]
  displayOrder: Integer [1]
}

class UniquePlaceDto <<DTO>> {
  id: UUID [1]
  placeName: String [1]
  city: String [1]
  imagePath: String [1]
  price: Decimal [1]
  currency: String [1]
  description: String [1]
  motivation: String [1]
}

class UniquePlacesResponseDto <<DTO>> {
  success: Boolean [1]
  data: UniquePlaceDto [0..*]
}

class UniquePlaceService <<Service>> {
  listPlaces(): UniquePlacesResponseDto
}

UniquePlacesResponseDto "1" *-- "0..*" UniquePlaceDto : data
UniquePlaceDto ..> UniquePlace : maps from
UniquePlaceService ..> UniquePlacesResponseDto
UniquePlaceService ..> UniquePlace
UniquePlaceService ..> City

@enduml
~~~

## Business Rules

The following rules are authoritative for Prompt E. OCL is preserved where applicable; technical or non-OCL constraints remain authoritative natural-language requirements.

~~~text
BR-PLACE-001: Active unique places
context UniquePlaceService::listPlaces() : UniquePlacesResponseDto
post BR_PLACE_001_Active:
  result.success implies
    result.data->forAll(item |
      UniquePlace.allInstances()->exists(place |
        place.id = item.id and place.active = true))


BR-PLACE-002: Complete unique-place collection
context UniquePlaceService::listPlaces() : UniquePlacesResponseDto
post BR_PLACE_002_Complete:
  result.success implies
    result.data->isUnique(item | item.id) and
    result.data->size() = UniquePlace.allInstances()->select(place |
      place.active = true)->size()


BR-PLACE-003: Unique-place projection
context UniquePlaceService::listPlaces() : UniquePlacesResponseDto
post BR_PLACE_003_Projection:
  result.success implies
    result.data->forAll(item |
      let place : UniquePlace = UniquePlace.allInstances()->any(candidate |
        candidate.id = item.id)
      in
      let city : City = City.allInstances()->any(candidate |
        candidate.id = place.destinationCityId)
      in
        item.placeName = place.placeName and
        item.city = city.name and
        item.imagePath = place.imagePath and
        item.price = place.price and
        item.currency = place.currency and
        item.description = place.description and
        item.motivation = place.motivation)


BR-PLACE-004: Unique-place price
context UniquePlaceService::listPlaces() : UniquePlacesResponseDto
post BR_PLACE_004_Price:
  result.success implies
    result.data->forAll(item |
      item.price >= 0 and
      not item.currency.oclIsUndefined() and
      trim(item.currency) <> '')


BR-PLACE-005: Descriptive content
context UniquePlaceService::listPlaces() : UniquePlacesResponseDto
post BR_PLACE_005_Content:
  result.success implies
    result.data->forAll(item |
      not item.placeName.oclIsUndefined() and
      trim(item.placeName) <> '' and
      not item.description.oclIsUndefined() and
      trim(item.description) <> '' and
      not item.motivation.oclIsUndefined() and
      trim(item.motivation) <> '')


BR-PLACE-006: Display order
context UniquePlaceService::listPlaces() : UniquePlacesResponseDto
post BR_PLACE_006_Order:
  result.success implies
    result.data->size() <= 1 or
    Sequence{1..result.data->size() - 1}->forAll(index |
      let current : UniquePlace = UniquePlace.allInstances()->any(place |
        place.id = result.data->at(index).id)
      in
      let following : UniquePlace = UniquePlace.allInstances()->any(place |
        place.id = result.data->at(index + 1).id)
      in
        current.displayOrder <= following.displayOrder)


BR-PLACE-007: Empty collection
context UniquePlaceService::listPlaces() : UniquePlacesResponseDto
post BR_PLACE_007_Empty:
  UniquePlace.allInstances()->select(place | place.active = true)->isEmpty()
  implies result.success and result.data->isEmpty()


BR-PLACE-008: Read-only retrieval
Calling API-UNIQUE-PLACES-LIST shall not create, update, or delete City or
UniquePlace records.

~~~
