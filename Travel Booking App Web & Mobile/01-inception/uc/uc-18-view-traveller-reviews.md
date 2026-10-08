---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-18
uc_name: "View Traveller Reviews"
---

# UC-18: View Traveller Reviews

## Functional Use-Case Specification

### Use Case ID

UC-18

### Use Case Name

View Traveller Reviews

### Description

As a visitor or authenticated user, I want to read published traveller reviews.

### Actor(s)

Visitor; Authenticated User; Review Service.

### Priority

P2.

### Trigger

The actor opens a page or section that presents traveller reviews.

### Pre-Condition(s)

PRE-1: The actor can access a page or section that presents traveller reviews.

### Post-Condition(s)

POST-1: The client displays the review-page state returned by the system.

POST-2: Available pagination or navigation remains accessible.

### Basic Flow

1. The actor opens a review section or a page containing featured reviews.
2. The client requests the relevant review page.
3. The system processes the request and returns a page outcome.
4. The client renders the review presentations represented by the response.
5. The actor reviews the displayed content.
6. The actor may request another review page when that interaction is available.

### Alternative Flow

AF-1: Handle an Empty Review Section

4a: If no reviews are returned, the client displays or omits the section according to the related design.

AF-2: Request the Featured Review Page Size

2a: A featured-review section requests the page size represented by its design.

### Exception Flow

EF-1: Additional Review Page Loading Failure

6a: If another review page cannot be loaded, the client keeps the displayed reviews and offers a retry.

EF-2: Initial Review Request Failure

3a: If the initial request fails, the client displays the designed unavailable state.

### Related UI

reviews; home-page testimonial sections.

### Related API IDs

API-REVIEW-LIST.

### Notes

None.

## UML Model

~~~plantuml
@startuml
hide empty members

enum ModerationStatus {
  PENDING
  APPROVED
  REJECTED
}

enum TripCompletionStatus {
  COMPLETED
  NOT_COMPLETED
}

class String {
  +<(other: String): Boolean
}

class DateTime {
  +<=(other: DateTime): Boolean
  +>(other: DateTime): Boolean
}

class RequestContext {
  +{static} startedAt: DateTime
}

class Review {
  +id: String
  +authorName: String
  +rating: Integer
  +comment: String
  +published: Boolean
  +publishedAt: DateTime
  +displayedAuthorName: String
  +bookingId: String
  +tripCompletionStatus: TripCompletionStatus
  +verifiedBooking: Boolean
  +moderationStatus: ModerationStatus
}

class ReviewService {
  +list(limit: Integer, offset: Integer): ReviewPage
}

class PrivacyMask {
  +{static} personName(value: String): String
}

class ReviewPage {
  +items: Review[*] {ordered}
  +total: Integer
  +limit: Integer
  +offset: Integer
  +hasMore: Boolean
}

class ContentSafety {
  +{static} isPublicSafe(value: String): Boolean
}

class ReadState {
  +{static} reviews(): String
}

Review --> TripCompletionStatus : tripCompletionStatus
Review --> ModerationStatus : moderationStatus
ReviewPage "1" o-- "0..*" Review : items

@enduml
~~~

## Business Rules

~~~text
BR-TRAVELLER-REVIEWS-01 - Only Moderated Public Reviews Are Returned
Source: Assumption
context ReviewService::list(limit: Integer, offset: Integer): ReviewPage
post BR_TRAVELLER_REVIEWS_01_OnlyModeratedPublicReviewsAreReturned:
  result.items->forAll(r |
    r.moderationStatus = ModerationStatus::APPROVED and
    r.published and r.publishedAt <= RequestContext::startedAt)
~~~

~~~text
BR-TRAVELLER-REVIEWS-02 - Verified Badge Reflects Completed Travel
Source: Assumption
context ReviewService::list(limit: Integer, offset: Integer): ReviewPage
post BR_TRAVELLER_REVIEWS_02_VerifiedBadgeReflectsCompletedTravel:
  result.items->forAll(r |
    r.verifiedBooking =
      (r.bookingId <> null and
       r.tripCompletionStatus = TripCompletionStatus::COMPLETED))
~~~

~~~text
BR-TRAVELLER-REVIEWS-03 - Public Author Identity Is Privacy Preserving
Source: Assumption
context ReviewService::list(limit: Integer, offset: Integer): ReviewPage
post BR_TRAVELLER_REVIEWS_03_PublicAuthorIdentityIsPrivacyPreserving:
  result.items->forAll(r |
    r.displayedAuthorName = PrivacyMask::personName(r.authorName))
~~~

~~~text
BR-TRAVELLER-REVIEWS-04 - Public Comment Passes Content Safety Projection
Source: Assumption
context ReviewService::list(limit: Integer, offset: Integer): ReviewPage
post BR_TRAVELLER_REVIEWS_04_PublicCommentPassesContentSafetyProjection:
  result.items->forAll(r | ContentSafety::isPublicSafe(r.comment))
~~~

~~~text
BR-TRAVELLER-REVIEWS-05 - Review Order Is Recent And Deterministic
Source: Assumption
context ReviewService::list(limit: Integer, offset: Integer): ReviewPage
post BR_TRAVELLER_REVIEWS_05_ReviewOrderIsRecentAndDeterministic:
  result.items->size() <= 1 or
  Sequence{1..result.items->size() - 1}->forAll(i |
    result.items->at(i).publishedAt > result.items->at(i + 1).publishedAt or
    (result.items->at(i).publishedAt = result.items->at(i + 1).publishedAt and
      result.items->at(i).id < result.items->at(i + 1).id))
~~~

~~~text
BR-TRAVELLER-REVIEWS-06 - Page Metadata Matches Its Slice
Source: Assumption
context ReviewService::list(limit: Integer, offset: Integer): ReviewPage
post BR_TRAVELLER_REVIEWS_06_PageMetadataMatchesItsSlice:
  result.limit = limit and result.offset = offset and result.total >= 0 and
  result.items->size() = (result.total - offset).max(0).min(limit) and
  result.hasMore = (offset + result.items->size() < result.total)
~~~

~~~text
BR-TRAVELLER-REVIEWS-07 - Review Retrieval Is Read Only
Source: Assumption
context ReviewService::list(limit: Integer, offset: Integer): ReviewPage
post BR_TRAVELLER_REVIEWS_07_ReviewRetrievalIsReadOnly:
  ReadState::reviews() = ReadState::reviews()@pre
~~~

~~~text
BR-TRAVELLER-REVIEWS-08 - Page Request Has Usable Bounds
Source: Assumption
context ReviewService::list(limit: Integer, offset: Integer): ReviewPage
pre BR_TRAVELLER_REVIEWS_08_PageRequestHasUsableBounds:
  limit > 0 and offset >= 0
~~~

~~~text
BR-TRAVELLER-REVIEWS-09 - Ratings And Review Identity Are Well Formed
Source: Assumption
context ReviewService::list(limit: Integer, offset: Integer): ReviewPage
post BR_TRAVELLER_REVIEWS_09_RatingsAndReviewIdentityAreWellFormed:
  result.items->isUnique(r | r.id) and
  result.items->forAll(r | r.rating >= 1 and r.rating <= 5)
~~~
