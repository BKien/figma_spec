---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-05
uc_name: "View product details"
---

# UC-05: View product details

## Functional Use-Case Specification

### Use Case ID

UC-05

### Use Case Name

View product details

### Description

Inspect product imagery, description, attributes, rating summary, size and color selections, and similar products.

### Actor(s)

Primary: Shopper. Supporting: web client and application service.

### Priority

High.

### Trigger

The shopper selects a product card.

### Pre-Condition(s)

PRE-1: The client has a product identifier from a displayed card.

### Post-Condition(s)

POST-1: The client displays the product detail and variant choices.

### Basic Flow

1. The shopper selects a product card.
2. The client requests the product detail.
3. The system returns images, description, attributes, rating summary, variants, and similar products.
4. The client renders the product detail.
5. The shopper selects an image, size, and color.
6. The client displays the selected image and variant.

### Alternative Flow

AF-1: View a similar product

5a: The shopper selects a similar product.

5b: The client requests and displays that product detail.

### Exception Flow

EF-1: Unavailable product

3a: The system returns an unavailable resource response.

3b: The client displays the unavailable product message.

3c: The shopper returns to the listing.

### Related UI

- [Figma node 1:2](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=1-2)

### Related API IDs

- [API-PRODUCT](../api/API-PRODUCT.md)

### Notes

Screen and text-layer evidence establishes the visible goal. Service decomposition, request shapes, and exception recovery are proposed implementation contracts; they are not extracted server behavior. See [assumptions](../../ASSUMPTIONS.md) and [coverage](../../coverage-report.md) for the supported boundary. No prototype interaction wiring was available for verification.

## UML Model

~~~plantuml
@startuml
hide empty members

class ProductService {
  +read(productId: String): ProductDetail
}

class Category {
  id: String
}

class Product {
  id: String
  description: String
  rating: Real
  commentCount: Integer
  questionCount: Integer
  published: Boolean
  displayRank: Integer
  category: Category
  variants: Set(Variant)
  images: Set(ProductImage)
  attributes: Set(ProductAttribute)
}

class ProductAttribute {
  productId: String
}

class ProductDetail <<response>> {
  product: Product
  description: String
  images: Sequence(ProductImage)
  rating: Real
  commentCount: Integer
  questionCount: Integer
  variants: Sequence(Variant)
  attributes: Set(ProductAttribute)
  similarProducts: Sequence(Product)
}

class ProductImage {
  productId: String
  position: Integer
}

class Variant {
  productId: String
  size: String
  color: String
  sellable: Boolean
  stock: Integer
  purchasable: Boolean
}

Category "1" -- "0..*" Product
Product "1" *-- "1..*" Variant
Product "1" *-- "0..*" ProductImage
Product "1" *-- "0..*" ProductAttribute
ProductDetail --> "1" Product : product
ProductDetail --> "0..*" ProductImage : images
ProductDetail --> "0..*" Variant : variants
ProductDetail --> "0..*" ProductAttribute : attributes
ProductDetail --> "0..*" Product : similarProducts

@enduml
~~~

## Business Rules

~~~text
BR-PRODUCT-DETAIL-01 - Published Product
Source: Assumption
context ProductService::read(productId: String): ProductDetail
pre BR_PRODUCT_DETAIL_01_PublishedProduct:
  Product.allInstances()->exists(p | p.id = productId and p.published)
~~~
~~~text
BR-PRODUCT-DETAIL-02 - Product Identity
Source: Assumption
context ProductService::read(productId: String): ProductDetail
post BR_PRODUCT_DETAIL_02_ProductIdentity:
  result.product.id = productId
~~~
~~~text
BR-PRODUCT-DETAIL-03 - Variant Choices
Source: Assumption
context ProductService::read(productId: String): ProductDetail
post BR_PRODUCT_DETAIL_03_VariantChoices:
  result.variants->asSet() = result.product.variants and result.variants->forAll(v | v.productId = productId)
~~~
~~~text
BR-PRODUCT-DETAIL-04 - Gallery Sequence
Source: Assumption
context ProductService::read(productId: String): ProductDetail
post BR_PRODUCT_DETAIL_04_GallerySequence:
  result.images = result.product.images->sortedBy(i | i.position) and result.images->forAll(i | i.productId = productId)
~~~
~~~text
BR-PRODUCT-DETAIL-05 - Description And Attributes
Source: Assumption
context ProductService::read(productId: String): ProductDetail
post BR_PRODUCT_DETAIL_05_DescriptionAndAttributes:
  result.description = result.product.description and result.attributes = result.product.attributes and result.attributes->forAll(a | a.productId = productId)
~~~
~~~text
BR-PRODUCT-DETAIL-06 - Related Products
Source: Assumption
context ProductService::read(productId: String): ProductDetail
post BR_PRODUCT_DETAIL_06_RelatedProducts:
  result.similarProducts = Product.allInstances()->select(p | p.published and p.id <> productId and p.category = result.product.category)->sortedBy(p | p.displayRank)
~~~
~~~text
BR-PRODUCT-DETAIL-07 - Public Selection
Source: Assumption
context Variant
inv BR_PRODUCT_DETAIL_07_PublicSelection:
  self.purchasable = (self.sellable and self.stock > 0)
~~~
~~~text
BR-PRODUCT-DETAIL-08 - Review Summary
Source: Assumption
context ProductService::read(productId: String): ProductDetail
post BR_PRODUCT_DETAIL_08_ReviewSummary:
  result.rating = result.product.rating and result.commentCount = result.product.commentCount and result.questionCount = result.product.questionCount
~~~
~~~text
BR-PRODUCT-DETAIL-09 - Review Values
Source: Assumption
context Product
inv BR_PRODUCT_DETAIL_09_ReviewValues:
  self.rating >= 0 and self.rating <= 5 and self.commentCount >= 0 and self.questionCount >= 0
~~~
~~~text
BR-PRODUCT-DETAIL-10 - Variant Identity
Source: Assumption
context Product
inv BR_PRODUCT_DETAIL_10_VariantIdentity:
  self.variants->isUnique(v | Tuple{size = v.size, color = v.color}) and self.images->isUnique(position)
~~~
