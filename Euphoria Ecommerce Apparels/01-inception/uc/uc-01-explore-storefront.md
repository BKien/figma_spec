---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-01
uc_name: "Explore the storefront"
---

# UC-01: Explore the storefront

## Functional Use-Case Specification

### Use Case ID

UC-01

### Use Case Name

Explore the storefront

### Description

Discover promotions, apparel categories, featured products, and feedback on the storefront.

### Actor(s)

Primary: Shopper. Supporting: web client and application service.

### Priority

Medium.

### Trigger

The shopper opens the Shop landing page.

### Pre-Condition(s)

PRE-1: The storefront route is open in the client.

### Post-Condition(s)

POST-1: The client displays the storefront sections.

### Basic Flow

1. The shopper opens the storefront.
2. The client requests storefront content.
3. The system returns promotions, categories, featured products, and feedback.
4. The client renders the returned sections.
5. The shopper chooses an Explore Now category.
6. The client opens the product listing and displays the returned cards.

### Alternative Flow

AF-1: Open a featured product

5a: The shopper selects a featured product card.

5b: The client opens the product detail route.

### Exception Flow

EF-1: Retry the storefront request

3a: The system returns a temporary service failure.

3b: The client presents a retry action for the storefront.

3c: The shopper retries the request.

### Related UI

- [Figma node 85:1544](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=85-1544)

### Related API IDs

- [API-STOREFRONT](../api/API-STOREFRONT.md)
- [API-CATALOG](../api/API-CATALOG.md)

### Notes

Screen and text-layer evidence establishes the visible goal. Service decomposition, request shapes, and exception recovery are proposed implementation contracts; they are not extracted server behavior. See [assumptions](../../ASSUMPTIONS.md) and [coverage](../../coverage-report.md) for the supported boundary. No prototype interaction wiring was available for verification.

## UML Model

~~~plantuml
@startuml
hide empty members

class StorefrontService {
  +read(): Storefront
}

class Category {
  id: String
  displayRank: Integer
}

class Product {
  published: Boolean
  featured: Boolean
  displayRank: Integer
}

class Promotion {
  targetCategoryId: String [0..1]
  published: Boolean
  displayRank: Integer
}

class Storefront <<response>> {
  promotions: Sequence(Promotion)
  categories: Sequence(Category)
  featured: Sequence(Product)
  testimonials: Sequence(Testimonial)
}

class Testimonial {
  rating: Real
  published: Boolean
  displayRank: Integer
}

Storefront --> "0..*" Promotion : promotions
Storefront --> "0..*" Category : categories
Storefront --> "0..*" Product : featured
Storefront --> "0..*" Testimonial : testimonials

@enduml
~~~

## Business Rules

~~~text
BR-STOREFRONT-01 - Promotions
Source: Assumption
context StorefrontService::read(): Storefront
post BR_STOREFRONT_01_Promotions:
  result.promotions = Promotion.allInstances()->select(p | p.published)->sortedBy(p | p.displayRank)
~~~
~~~text
BR-STOREFRONT-02 - Categories
Source: Assumption
context StorefrontService::read(): Storefront
post BR_STOREFRONT_02_Categories:
  result.categories = Category.allInstances()->sortedBy(c | c.displayRank)
~~~
~~~text
BR-STOREFRONT-03 - Featured Cards
Source: Assumption
context StorefrontService::read(): Storefront
post BR_STOREFRONT_03_FeaturedCards:
  result.featured = Product.allInstances()->select(p | p.published and p.featured)->sortedBy(p | p.displayRank)
~~~
~~~text
BR-STOREFRONT-04 - Feedback
Source: Assumption
context StorefrontService::read(): Storefront
post BR_STOREFRONT_04_Feedback:
  result.testimonials = Testimonial.allInstances()->select(t | t.published)->sortedBy(t | t.displayRank)
~~~
~~~text
BR-STOREFRONT-05 - Category Destination
Source: Assumption
context Promotion
inv BR_STOREFRONT_05_CategoryDestination:
  self.targetCategoryId = null or Category.allInstances()->exists(c | c.id = self.targetCategoryId)
~~~
~~~text
BR-STOREFRONT-06 - Rating Scale
Source: Assumption
context Testimonial
inv BR_STOREFRONT_06_RatingScale:
  self.rating >= 0 and self.rating <= 5
~~~
~~~text
BR-STOREFRONT-07 - Editorial Positions
Source: Assumption
context Promotion
inv BR_STOREFRONT_07_EditorialPositions:
  Promotion.allInstances()->isUnique(displayRank) and Category.allInstances()->isUnique(displayRank) and Testimonial.allInstances()->isUnique(displayRank)
~~~
