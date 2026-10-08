---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-16
uc_name: "View Customer Reviews"
---

# UC-16: View Customer Reviews

## Functional Use-Case Specification

### Use Case ID

UC-16

### Use Case Name

View Customer Reviews

### Description

As a visitor, I want to view published Tripma customer reviews so that I can understand other travelers' experiences.

### Actor(s)

Visitor

### Priority

Low

### Trigger

The visitor opens an experience containing the Tripma customer-reviews section.

### Pre-Condition(s)

PRE-1: The Tripma experience is available.

PRE-2: Tripma can attempt to retrieve published customer reviews.

### Post-Condition(s)

POST-1: On success, Tripma presents the available published reviews.

POST-2: Viewing reviews does not modify review or user data.

POST-3: On failure, Tripma reports that reviews could not be loaded.

### Basic Flow

1. The visitor opens the Tripma experience.
2. Tripma requests the initial customer-review collection through API-CUSTOMER-REVIEWS-LIST.
3. The review service evaluates the request according to the Business Rules.
4. API-CUSTOMER-REVIEWS-LIST returns the published review summaries.
5. Tripma presents each reviewer's display identity, review date, rating, and review preview.
6. The visitor reviews the displayed customer experiences.

### Alternative Flow

AF-1: Read the complete review

5a: The visitor chooses to read more from a displayed review.

5b: Tripma presents the complete content already returned for that review.

5c: No additional API request is required.

AF-2: Load the next review page

6a: If the response indicates that more reviews are available, the visitor requests more.

6b: Tripma calls API-CUSTOMER-REVIEWS-LIST with the returned cursor.

6c: Tripma appends the next collection without duplicating an existing review.

AF-3: No reviews are available

4a: API-CUSTOMER-REVIEWS-LIST returns an empty collection.

4b: Tripma presents the empty customer-reviews experience.

### Exception Flow

EF-1: Review request is invalid

3a: If the supplied list parameters cannot be accepted, API-CUSTOMER-REVIEWS-LIST returns an invalid-request outcome.

3b: Tripma does not replace an already displayed review collection.

EF-2: Reviews cannot be loaded

2a: If Tripma cannot complete the request because of a technical failure, it presents a retryable error state.

### Related UI

Customer-reviews section and review cards in the Tripma experience

### Related API IDs

API-CUSTOMER-REVIEWS-LIST

### Notes

Scope clarification: UC-16 displays published customer reviews. Creating, editing, deleting, rating the helpfulness of, or moderating a review is outside this use case.

## UML Model

~~~plantuml
@startuml
hide empty members

class User <<Entity>> {
  id: UUID [1]
  username: String [1]
  displayName: String [0..1]
  profileImagePath: String [0..1]
}

class CustomerReview <<Entity>> {
  id: UUID [1]
  userId: UUID [1]
  rating: Integer [1]
  content: String [1]
  reviewedAt: DateTime [1]
  published: Boolean [1]
}

class CustomerReviewDto <<DTO>> {
  reviewId: UUID [1]
  reviewerDisplayName: String [1]
  reviewerImagePath: String [1]
  rating: Integer [1]
  content: String [1]
  reviewedAt: DateTime [1]
}

class CustomerReviewPageDto <<DTO>> {
  items: CustomerReviewDto [0..*]
  nextCursor: String [0..1]
}

class CustomerReviewListResponseDto <<DTO>> {
  success: Boolean [1]
  data: CustomerReviewPageDto [1]
}

class CustomerReviewService <<Service>> {
  listPublishedReviews(
    cursor: String,
    limit: Integer
  ): CustomerReviewListResponseDto
}

CustomerReviewPageDto "1" *-- "0..*" CustomerReviewDto : items
CustomerReviewListResponseDto "1" *-- "1" CustomerReviewPageDto : data
CustomerReviewService ..> CustomerReviewListResponseDto
CustomerReviewService ..> CustomerReview
CustomerReviewService ..> User

@enduml
~~~

## Business Rules

The following rules are authoritative for Prompt E. OCL is preserved where applicable; pagination and non-OCL constraints remain authoritative natural-language requirements.

~~~text
BR-REVIEW-001 - Public review retrieval
API-CUSTOMER-REVIEWS-LIST is available without an authenticated Tripma session.


BR-REVIEW-002 - Page size
context CustomerReviewService::listPublishedReviews(
  cursor : String,
  limit : Integer
) : CustomerReviewListResponseDto
pre BR_REVIEW_002_Limit:
  limit.oclIsUndefined() or
  (limit >= 1 and limit <= 20)

When limit is undefined, the effective page size is 3.


BR-REVIEW-003 - Published-review scope
context CustomerReviewService::listPublishedReviews(
  cursor : String,
  limit : Integer
) : CustomerReviewListResponseDto
post BR_REVIEW_003_Published:
  result.success implies
    result.data.items->forAll(item |
      CustomerReview.allInstances()->exists(review |
        review.id = item.reviewId and review.published))


BR-REVIEW-004 - Review author
context CustomerReview
inv BR_REVIEW_004_Author:
  User.allInstances()->exists(user | user.id = self.userId)


BR-REVIEW-005 - Rating range
context CustomerReview
inv BR_REVIEW_005_Rating:
  self.rating >= 1 and self.rating <= 5


BR-REVIEW-006 - Review content
context CustomerReview
inv BR_REVIEW_006_Content:
  not self.content.oclIsUndefined() and
  trim(self.content) <> '' and
  self.content.size() <= 2000


BR-REVIEW-007 - Review projection
context CustomerReviewService::listPublishedReviews(
  cursor : String,
  limit : Integer
) : CustomerReviewListResponseDto
post BR_REVIEW_007_Projection:
  result.success implies
    result.data.items->forAll(item |
      let review : CustomerReview = CustomerReview.allInstances()->any(source |
        source.id = item.reviewId)
      in
        item.rating = review.rating and
        item.content = review.content and
        item.reviewedAt = review.reviewedAt)


BR-REVIEW-008 - Reviewer display name
context CustomerReviewService::listPublishedReviews(
  cursor : String,
  limit : Integer
) : CustomerReviewListResponseDto
post BR_REVIEW_008_DisplayName:
  result.success implies
    result.data.items->forAll(item |
      let review : CustomerReview = CustomerReview.allInstances()->any(source |
        source.id = item.reviewId),
          user : User = User.allInstances()->any(author |
        author.id = review.userId)
      in
        item.reviewerDisplayName =
          if user.displayName.oclIsUndefined() or
             trim(user.displayName) = ''
          then user.username
          else user.displayName
          endif)


BR-REVIEW-009 - Reviewer image fallback
context CustomerReviewService::listPublishedReviews(
  cursor : String,
  limit : Integer
) : CustomerReviewListResponseDto
post BR_REVIEW_009_Image:
  result.success implies
    result.data.items->forAll(item |
      let review : CustomerReview = CustomerReview.allInstances()->any(source |
        source.id = item.reviewId),
          user : User = User.allInstances()->any(author |
        author.id = review.userId)
      in
        item.reviewerImagePath =
          if user.profileImagePath.oclIsUndefined() or
             trim(user.profileImagePath) = ''
          then '/commenter.svg'
          else user.profileImagePath
          endif)


BR-REVIEW-010 - Review ordering
context CustomerReviewService::listPublishedReviews(
  cursor : String,
  limit : Integer
) : CustomerReviewListResponseDto
post BR_REVIEW_010_Order:
  result.success implies
    result.data.items =
      result.data.items->sortedBy(item | item.reviewedAt)->reverse()

When two reviews have the same reviewedAt value, reviewId descending is the
secondary ordering key used for both the response and cursor continuation.


BR-REVIEW-011 - Page uniqueness
context CustomerReviewService::listPublishedReviews(
  cursor : String,
  limit : Integer
) : CustomerReviewListResponseDto
post BR_REVIEW_011_Unique:
  result.success implies
    result.data.items->isUnique(item | item.reviewId) and
    result.data.items->size() <=
      if limit.oclIsUndefined() then 3 else limit endif


BR-REVIEW-012 - Cursor continuity
A non-empty nextCursor shall identify the position immediately after the last
review in the current ordering. Reusing that cursor with the same page size
shall not return a review from the preceding page.


BR-REVIEW-013 - Empty collection
context CustomerReviewService::listPublishedReviews(
  cursor : String,
  limit : Integer
) : CustomerReviewListResponseDto
post BR_REVIEW_013_Empty:
  CustomerReview.allInstances()->select(review | review.published)->isEmpty()
  implies
    result.success and
    result.data.items->isEmpty() and
    result.data.nextCursor.oclIsUndefined()


BR-REVIEW-014 - Public response boundary
The response shall not contain a user ID, email address, password hash, session
data, booking data, payment data, or unpublished review content.


BR-REVIEW-015 - Read-only retrieval
Calling API-CUSTOMER-REVIEWS-LIST shall not create, update, publish, unpublish,
or delete User or CustomerReview records.
~~~
