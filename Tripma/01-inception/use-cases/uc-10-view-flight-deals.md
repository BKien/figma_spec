---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-10
uc_name: "View Flight Deals"
---

# UC-10: View Flight Deals

## Functional Use-Case Specification

### Use Case ID

UC-10

### Use Case Name

View Flight Deals

### Description

As a visitor, I want to view Tripma flight deals so that I can discover featured destinations.

### Actor(s)

Visitor

### Priority

Low

### Trigger

The visitor opens a Tripma experience that provides flight deals.

### Pre-Condition(s)

PRE-1: The Tripma flight-deal experience is available.
PRE-2: Tripma can attempt to retrieve the deal collection.

### Post-Condition(s)

POST-1: When retrieval succeeds, Tripma presents the returned flight-deal collection.
POST-2: When retrieval cannot be completed, Tripma reports the outcome without changing deal data.

### Basic Flow

1. The visitor opens a Tripma experience containing flight deals.
2. Tripma requests the deal collection through API-FLIGHT-DEALS-LIST.
3. The flight-deal service evaluates the request according to the Business Rules.
4. API-FLIGHT-DEALS-LIST returns the deal collection.
5. Tripma presents the returned flight-deal summaries.
6. The visitor reviews the available flight deals.

### Alternative Flow

AF-1: View the complete deal collection
6a. The visitor requests the complete flight-deal collection from the current experience.
6b. Tripma presents the complete collection returned by API-FLIGHT-DEALS-LIST.

AF-2: No flight deals are available
4a. API-FLIGHT-DEALS-LIST returns an empty collection.
4b. Tripma presents the empty flight-deal experience.

### Exception Flow

EF-1: Request cannot be completed
2a. If Tripma cannot complete the request because of a technical failure, it presents a retryable error state.

### Related UI

Flight Deals experience available from the Tripma home and flight-discovery pages

### Related API IDs

API-FLIGHT-DEALS-LIST

### Notes

Scope clarification: UC-10 retrieves and presents flight deals only. Flight search remains assigned to UC-01, and selecting a deal does not define additional navigation or search behavior in this use case.

## UML Model

~~~plantuml
@startuml
hide empty members

class City <<Entity>> {
  id: UUID [1]
  name: String [1]
}

class FlightDeal <<Entity>> {
  id: UUID [1]
  destinationCityId: UUID [1]
  placeName: String [1]
  imagePath: String [1]
  price: Decimal [1]
  currency: String [1]
  description: String [1]
  active: Boolean [1]
  displayOrder: Integer [1]
}

class FlightDealDto <<DTO>> {
  id: UUID [1]
  placeName: String [1]
  city: String [1]
  imagePath: String [1]
  price: Decimal [1]
  currency: String [1]
  description: String [1]
}

class FlightDealsResponseDto <<DTO>> {
  success: Boolean [1]
  data: FlightDealDto [0..*]
}

class FlightDealService <<Service>> {
  listDeals(): FlightDealsResponseDto
}

FlightDealsResponseDto "1" *-- "0..*" FlightDealDto : data
FlightDealDto ..> FlightDeal : maps from
FlightDealService ..> FlightDealsResponseDto
FlightDealService ..> FlightDeal
FlightDealService ..> City

@enduml
~~~

## Business Rules

The following rules are authoritative for Prompt E. OCL is preserved where applicable; technical or non-OCL constraints remain authoritative natural-language requirements.

~~~text
BR-DEAL-001: Active deals
context FlightDealService::listDeals() : FlightDealsResponseDto
post BR_DEAL_001_Active:
  result.success implies
    result.data->forAll(item |
      FlightDeal.allInstances()->exists(deal |
        deal.id = item.id and deal.active = true))


BR-DEAL-002: Complete deal collection
context FlightDealService::listDeals() : FlightDealsResponseDto
post BR_DEAL_002_Complete:
  result.success implies
    result.data->isUnique(item | item.id) and
    result.data->size() = FlightDeal.allInstances()->select(deal |
      deal.active = true)->size()


BR-DEAL-003: Deal projection
context FlightDealService::listDeals() : FlightDealsResponseDto
post BR_DEAL_003_Projection:
  result.success implies
    result.data->forAll(item |
      let deal : FlightDeal = FlightDeal.allInstances()->any(candidate |
        candidate.id = item.id)
      in
      let city : City = City.allInstances()->any(candidate |
        candidate.id = deal.destinationCityId)
      in
        item.placeName = deal.placeName and
        item.city = city.name and
        item.imagePath = deal.imagePath and
        item.price = deal.price and
        item.currency = deal.currency and
        item.description = deal.description)


BR-DEAL-004: Deal price
context FlightDealService::listDeals() : FlightDealsResponseDto
post BR_DEAL_004_Price:
  result.success implies
    result.data->forAll(item |
      item.price >= 0 and
      not item.currency.oclIsUndefined() and
      trim(item.currency) <> '')


BR-DEAL-005: Display order
context FlightDealService::listDeals() : FlightDealsResponseDto
post BR_DEAL_005_Order:
  result.success implies
    result.data->size() <= 1 or
    Sequence{1..result.data->size() - 1}->forAll(index |
      let current : FlightDeal = FlightDeal.allInstances()->any(deal |
        deal.id = result.data->at(index).id)
      in
      let following : FlightDeal = FlightDeal.allInstances()->any(deal |
        deal.id = result.data->at(index + 1).id)
      in
        current.displayOrder <= following.displayOrder)


BR-DEAL-006: Empty collection
context FlightDealService::listDeals() : FlightDealsResponseDto
post BR_DEAL_006_Empty:
  FlightDeal.allInstances()->select(deal | deal.active = true)->isEmpty()
  implies result.success and result.data->isEmpty()


BR-DEAL-007: Read-only retrieval
Calling API-FLIGHT-DEALS-LIST shall not create, update, or delete City or
FlightDeal records.

~~~
