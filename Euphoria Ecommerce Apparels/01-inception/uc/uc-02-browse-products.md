---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-02
uc_name: "Browse products by category"
---

# UC-02: Browse products by category

## Functional Use-Case Specification

### Use Case ID

UC-02

### Use Case Name

Browse products by category

### Description

Open the apparel listing from Shop or a category and inspect its product cards.

### Actor(s)

Primary: Shopper. Supporting: web client and application service.

### Priority

High.

### Trigger

The shopper opens Shop or selects a category.

### Pre-Condition(s)

PRE-1: The storefront or category navigation is displayed.

### Post-Condition(s)

POST-1: The client displays the product listing.

### Basic Flow

1. The shopper chooses Shop or a category.
2. The client requests the product listing.
3. The system returns product cards and filter choices.
4. The client displays the listing and the category heading.
5. The shopper selects a product card.
6. The client opens its product detail route.

### Alternative Flow

AF-1: Browse another category

1a: The shopper chooses another category.

1b: The client requests and displays its product listing.

### Exception Flow

EF-1: Unavailable product listing

3a: The system returns an unavailable resource response.

3b: The client displays the returned message.

3c: The shopper returns to category navigation.

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
  categoryId: String [0..1]
}

class CatalogResult <<response>> {
  items: Sequence(Product)
  categories: Set(String)
  total: Integer
}

class Category {
  id: String
}

class Money <<value>> {
  amount: Real
  currency: String
}

class Product {
  id: String
  published: Boolean
  category: Category
  displayPrice: Money
  variants: Set(Variant)
}

class Variant {
  price: Money
}

Category "1" -- "0..*" Product
Product "1" *-- "1..*" Variant
CatalogResult --> "0..*" Product : items
Product --> "1" Money : displayPrice
Variant --> "1" Money : price

@enduml
~~~

## Business Rules

~~~text
BR-BROWSE-PRODUCTS-01 - Category Reference
Source: Assumption
context CatalogService::list(criteria: CatalogCriteria): CatalogResult
pre BR_BROWSE_PRODUCTS_01_CategoryReference:
  criteria.categoryId = null or Category.allInstances()->exists(c | c.id = criteria.categoryId)
~~~
~~~text
BR-BROWSE-PRODUCTS-02 - Published Catalog
Source: Assumption
context CatalogService::list(criteria: CatalogCriteria): CatalogResult
post BR_BROWSE_PRODUCTS_02_PublishedCatalog:
  result.items->forAll(p | p.published)
~~~
~~~text
BR-BROWSE-PRODUCTS-03 - Category Boundary
Source: Assumption
context CatalogService::list(criteria: CatalogCriteria): CatalogResult
post BR_BROWSE_PRODUCTS_03_CategoryBoundary:
  criteria.categoryId = null or result.items->forAll(p | p.category.id = criteria.categoryId)
~~~
~~~text
BR-BROWSE-PRODUCTS-04 - Card Identity
Source: Assumption
context CatalogService::list(criteria: CatalogCriteria): CatalogResult
post BR_BROWSE_PRODUCTS_04_CardIdentity:
  result.items->isUnique(id)
~~~
~~~text
BR-BROWSE-PRODUCTS-05 - Category Choices
Source: Assumption
context CatalogService::list(criteria: CatalogCriteria): CatalogResult
post BR_BROWSE_PRODUCTS_05_CategoryChoices:
  result.categories = Category.allInstances()->collect(c | c.id)->asSet()
~~~
~~~text
BR-BROWSE-PRODUCTS-06 - Result Count
Source: Assumption
context CatalogService::list(criteria: CatalogCriteria): CatalogResult
post BR_BROWSE_PRODUCTS_06_ResultCount:
  result.total = result.items->size()
~~~
~~~text
BR-BROWSE-PRODUCTS-07 - Display Price
Source: Assumption
context Product
inv BR_BROWSE_PRODUCTS_07_DisplayPrice:
  self.displayPrice.amount >= 0 and self.variants->exists(v | v.price = self.displayPrice)
~~~
