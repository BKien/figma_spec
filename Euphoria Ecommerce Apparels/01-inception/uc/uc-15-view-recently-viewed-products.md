---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-15
uc_name: "Rediscover recently viewed products"
---

# UC-15: Rediscover recently viewed products

## Functional Use-Case Specification

### Use Case ID

UC-15

### Use Case Name

Rediscover recently viewed products

### Description

Use Recently Viewed on the empty-wishlist screen to reopen a product.

### Actor(s)

Primary: Customer. Supporting: web client and application service.

### Priority

Medium.

### Trigger

The customer opens Recently Viewed from the empty-wishlist screen.

### Pre-Condition(s)

PRE-1: The empty-wishlist screen is displayed.

### Post-Condition(s)

POST-1: The client displays a selected product detail.

### Basic Flow

1. The customer opens Recently Viewed.
2. The client requests the wishlist screen content.
3. The system returns recently viewed cards.
4. The client displays the cards.
5. The customer selects a card.
6. The client requests and displays its product detail.

### Alternative Flow

AF-1: Open the product listing

5a: The customer chooses the Shop entry point.

5b: The client opens the product listing.

### Exception Flow

EF-1: Sign in to view recently viewed products

3a: The system returns a rejected authentication context.

3b: The client presents the sign-in entry point.

### Related UI

- [Figma node 299:1027](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=299-1027)

### Related API IDs

- [API-WISHLIST](../api/API-WISHLIST.md)
- [API-PRODUCT](../api/API-PRODUCT.md)

### Notes

Screen and text-layer evidence establishes the visible goal. Service decomposition, request shapes, and exception recovery are proposed implementation contracts; they are not extracted server behavior. See [assumptions](../../ASSUMPTIONS.md) and [coverage](../../coverage-report.md) for the supported boundary. No prototype interaction wiring was available for verification.

## UML Model

~~~plantuml
@startuml
hide empty members

class WishlistService {
  +read(ctx: RequestContext): WishlistResult
}

class Product {
  id: String
  published: Boolean
  displayRank: Integer
}

class RequestContext <<input>> {
  customerId: String
  authenticated: Boolean
}

class ViewedProduct {
  customerId: String
  product: Product
  viewedAt: Integer
}

class WishlistResult <<response>> {
  recentlyViewed: Sequence(Product)
}

ViewedProduct "0..*" --> "1" Product
WishlistResult --> "0..*" Product : recentlyViewed

@enduml
~~~

## Business Rules

~~~text
BR-RECENT-PRODUCTS-01 - Customer Context
Source: Assumption
context WishlistService::read(ctx: RequestContext): WishlistResult
pre BR_RECENT_PRODUCTS_01_CustomerContext:
  ctx.authenticated
~~~
~~~text
BR-RECENT-PRODUCTS-02 - Viewed Membership
Source: Assumption
context WishlistService::read(ctx: RequestContext): WishlistResult
post BR_RECENT_PRODUCTS_02_ViewedMembership:
  result.recentlyViewed->asSet() = ViewedProduct.allInstances()->select(v | v.customerId = ctx.customerId and v.product.published)->collect(v | v.product)->asSet()
~~~
~~~text
BR-RECENT-PRODUCTS-03 - Recent Once
Source: Assumption
context ViewedProduct
inv BR_RECENT_PRODUCTS_03_RecentOnce:
  ViewedProduct.allInstances()->isUnique(v | Tuple{customerId = v.customerId, productId = v.product.id})
~~~
~~~text
BR-RECENT-PRODUCTS-04 - Recent Sequence
Source: Assumption
context WishlistService::read(ctx: RequestContext): WishlistResult
post BR_RECENT_PRODUCTS_04_RecentSequence:
  result.recentlyViewed->forAll(a,b | let va : ViewedProduct = ViewedProduct.allInstances()->any(v | v.customerId = ctx.customerId and v.product = a) in let vb : ViewedProduct = ViewedProduct.allInstances()->any(v | v.customerId = ctx.customerId and v.product = b) in va.viewedAt > vb.viewedAt implies result.recentlyViewed->indexOf(a) < result.recentlyViewed->indexOf(b))
~~~
~~~text
BR-RECENT-PRODUCTS-05 - Recent Ties
Source: Assumption
context WishlistService::read(ctx: RequestContext): WishlistResult
post BR_RECENT_PRODUCTS_05_RecentTies:
  result.recentlyViewed->forAll(a,b | let va : ViewedProduct = ViewedProduct.allInstances()->any(v | v.customerId = ctx.customerId and v.product = a) in let vb : ViewedProduct = ViewedProduct.allInstances()->any(v | v.customerId = ctx.customerId and v.product = b) in va.viewedAt = vb.viewedAt and a.displayRank < b.displayRank implies result.recentlyViewed->indexOf(a) < result.recentlyViewed->indexOf(b))
~~~
~~~text
BR-RECENT-PRODUCTS-06 - Recent Card Identity
Source: Assumption
context WishlistService::read(ctx: RequestContext): WishlistResult
post BR_RECENT_PRODUCTS_06_RecentCardIdentity:
  result.recentlyViewed->isUnique(id)
~~~
~~~text
BR-RECENT-PRODUCTS-07 - Viewing History Unchanged
Source: Assumption
context WishlistService::read(ctx: RequestContext): WishlistResult
post BR_RECENT_PRODUCTS_07_ViewingHistoryUnchanged:
  ViewedProduct.allInstances() = ViewedProduct.allInstances()@pre and ViewedProduct.allInstances()->forAll(v | v.product = v.product@pre and v.customerId = v.customerId@pre and v.viewedAt = v.viewedAt@pre)
~~~
