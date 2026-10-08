---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-04
uc_name: "Change product listing order"
---

# UC-04: Change product listing order

## Functional Use-Case Specification

### Use Case ID

UC-04

### Use Case Name

Change product listing order

### Description

Switch the product listing between New and Recommended views.

### Actor(s)

Primary: Shopper. Supporting: web client and application service.

### Priority

High.

### Trigger

The shopper chooses New or Recommended.

### Pre-Condition(s)

PRE-1: The product listing is displayed.

### Post-Condition(s)

POST-1: The client displays the returned product sequence.

### Basic Flow

1. The shopper chooses New.
2. The client submits the listing request with the chosen view.
3. The system returns product cards.
4. The client displays the returned sequence and highlights the chosen view.

### Alternative Flow

AF-1: Choose Recommended

1a: The shopper chooses Recommended.

1b: The client submits the changed view.

1c: The client displays the returned sequence.

### Exception Flow

EF-1: Retry the product listing

3a: The system returns a temporary service failure.

3b: The client keeps the displayed listing and offers Retry.

### Related UI

- [Figma node 64:33](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=64-33)

### Related API IDs

- [API-CATALOG](../api/API-CATALOG.md)

### Notes

Screen and text-layer evidence establishes the visible goal. Service decomposition, request shapes, and exception recovery are proposed implementation contracts; they are not extracted server behavior. See [assumptions](../../ASSUMPTIONS.md) and [coverage](../../coverage-report.md) for the supported boundary. No prototype interaction wiring was available for verification.

## UML Model

~~~plantuml
@startuml
hide empty members

class CatalogService {
  +list(criteria: CatalogCriteria): CatalogResult
}

class CatalogCriteria <<input>> {
  rawSort: CatalogSort [0..1]
  sort: CatalogSort
}

class CatalogResult <<response>> {
  items: Sequence(Product)
}

enum CatalogSort {
  NEW
  RECOMMENDED
}

class Money <<value>> {
  amount: Real
  currency: String
}

class Product {
  displayRank: Integer
  recommendationRank: Integer
  createdAt: Integer
  displayPrice: Money
}

CatalogCriteria --> "0..1" CatalogSort : rawSort
CatalogCriteria --> "1" CatalogSort : sort
CatalogResult --> "0..*" Product : items
Product --> "1" Money : displayPrice

@enduml
~~~

## Business Rules

~~~text
BR-SORT-PRODUCTS-01 - Default View
Source: Assumption
context CatalogCriteria
inv BR_SORT_PRODUCTS_01_DefaultView:
  self.sort = (if self.rawSort = null then CatalogSort::RECOMMENDED else self.rawSort endif)
~~~
~~~text
BR-SORT-PRODUCTS-02 - New First
Source: Assumption
context CatalogService::list(criteria: CatalogCriteria): CatalogResult
post BR_SORT_PRODUCTS_02_NewFirst:
  criteria.sort = CatalogSort::NEW implies result.items->forAll(a,b | a.createdAt > b.createdAt implies result.items->indexOf(a) < result.items->indexOf(b))
~~~
~~~text
BR-SORT-PRODUCTS-03 - New Ties
Source: Assumption
context CatalogService::list(criteria: CatalogCriteria): CatalogResult
post BR_SORT_PRODUCTS_03_NewTies:
  criteria.sort = CatalogSort::NEW implies result.items->forAll(a,b | a.createdAt = b.createdAt and a.displayRank < b.displayRank implies result.items->indexOf(a) < result.items->indexOf(b))
~~~
~~~text
BR-SORT-PRODUCTS-04 - Recommended First
Source: Assumption
context CatalogService::list(criteria: CatalogCriteria): CatalogResult
post BR_SORT_PRODUCTS_04_RecommendedFirst:
  criteria.sort = CatalogSort::RECOMMENDED implies result.items = result.items->sortedBy(p | p.recommendationRank)
~~~
~~~text
BR-SORT-PRODUCTS-05 - Editorial Rank Identity
Source: Assumption
context Product
inv BR_SORT_PRODUCTS_05_EditorialRankIdentity:
  Product.allInstances()->isUnique(displayRank)
~~~
~~~text
BR-SORT-PRODUCTS-06 - Recommendation Rank Identity
Source: Assumption
context Product
inv BR_SORT_PRODUCTS_06_RecommendationRankIdentity:
  Product.allInstances()->isUnique(recommendationRank)
~~~
~~~text
BR-SORT-PRODUCTS-07 - Stable Catalog Values
Source: Assumption
context CatalogService::list(criteria: CatalogCriteria): CatalogResult
post BR_SORT_PRODUCTS_07_StableCatalogValues:
  Product.allInstances() = Product.allInstances()@pre and Product.allInstances()->forAll(p | p.displayPrice = p.displayPrice@pre and p.displayRank = p.displayRank@pre and p.recommendationRank = p.recommendationRank@pre and p.createdAt = p.createdAt@pre)
~~~
