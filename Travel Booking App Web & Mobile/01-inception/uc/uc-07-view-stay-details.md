---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-07
uc_name: "View Stay Details"
---

# UC-07: View Stay Details

## Functional Use-Case Specification

### Use Case ID

UC-07

### Use Case Name

View Stay Details

### Description

As a traveller, I want to inspect a stay's details, amenities, reviews, location, and current offer.

### Actor(s)

Traveller; Stay Service.

### Priority

P0.

### Trigger

The traveller chooses a stay from a result view.

### Pre-Condition(s)

PRE-1: A selected stay reference is available to the client.

### Post-Condition(s)

POST-1: The client displays the stay-detail outcome returned by the system.

POST-2: Navigation back to the originating result context remains available.

### Basic Flow

1. The traveller selects a stay result.
2. The client requests the detail associated with the selected stay.
3. The system processes the request and returns a detail outcome.
4. The client renders the detail sections represented by the response.
5. The traveller reviews the displayed sections.
6. The traveller may use an available continuation from the detail view.

### Alternative Flow

AF-1: Return to Stay Results

6a: The traveller returns to the preserved result context.

AF-2: Render Remaining Stay Detail Sections

4a: If an optional section is absent from the response, the client renders the remaining detail sections.

### Exception Flow

EF-1: Stay Detail Loading Failure

3a: If stay detail cannot be loaded, the client displays a retry state.

3b: The client retains navigation back to the result view.

### Related UI

hotel southern details page; stay details mobile.

### Related API IDs

API-STAY-DETAIL.

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

class String {
  +trim(): String
  +toLower(): String
}

class DateTime {
  +<=(other: DateTime): Boolean
  +>(other: DateTime): Boolean
}

class RequestContext {
  +{static} startedAt: DateTime
}

class Stay {
  +id: String
  +active: Boolean
  +amenities: String[*] {ordered}
  +media: StayMedia[*] {ordered}
}

class StayOffer {
  +id: String
  +stay: Stay
  +available: Boolean
  +expiresAt: DateTime
}

class Review {
  +rating: Integer
  +published: Boolean
  +publishedAt: DateTime
  +moderationStatus: ModerationStatus
  +stayId: String
}

class StayService {
  +getDetail(stayId: String, offerId: String): StayDetail
}

class StayMedia {
  +id: String
  +sortOrder: Integer
}

class ReviewSummary {
  +approvedCount: Integer
  +averageRating: Real
  +approvedRatings: Bag(Real)
}

class StayDetail {
  +stay: Stay
  +reviewSummary: ReviewSummary
  +currentOffer: StayOffer
}

class ReadState {
  +{static} stays(): String
}

Stay "1" o-- "0..*" StayMedia : media
StayOffer --> Stay : stay
Review --> ModerationStatus : moderationStatus
StayDetail --> Stay : stay
StayDetail --> ReviewSummary : reviewSummary
StayDetail --> StayOffer : currentOffer

@enduml
~~~

## Business Rules

~~~text
BR-STAY-DETAIL-01 - Detail Represents The Selected Active Stay
Source: Assumption
context StayService::getDetail(stayId: String, offerId: String): StayDetail
post BR_STAY_DETAIL_01_DetailRepresentsTheSelectedActiveStay:
  result <> null and result.stay.id = stayId and result.stay.active
~~~

~~~text
BR-STAY-DETAIL-02 - Amenities Are Canonical And Non Repeating
Source: Assumption
context StayService::getDetail(stayId: String, offerId: String): StayDetail
post BR_STAY_DETAIL_02_AmenitiesAreCanonicalAndNonRepeating:
  result.stay.amenities->forAll(a | a = a.trim().toLower()) and
  result.stay.amenities->isUnique(a | a)
~~~

~~~text
BR-STAY-DETAIL-03 - Media Order Is Stable And Gap Free
Source: Assumption
context StayService::getDetail(stayId: String, offerId: String): StayDetail
post BR_STAY_DETAIL_03_MediaOrderIsStableAndGapFree:
  result.stay.media->isUnique(m | m.id) and
  (result.stay.media->isEmpty() or
   Sequence{1..result.stay.media->size()}->forAll(i | result.stay.media->at(i).sortOrder = i))
~~~

~~~text
BR-STAY-DETAIL-04 - Review Summary Is Derived Only From Approved Ratings
Source: Assumption
context StayService::getDetail(stayId: String, offerId: String): StayDetail
post BR_STAY_DETAIL_04_ReviewSummaryIsDerivedOnlyFromApprovedRatings:
  result.reviewSummary.approvedCount =
    result.reviewSummary.approvedRatings->size() and
  (result.reviewSummary.approvedCount = 0 implies
    result.reviewSummary.averageRating = 0) and
  (result.reviewSummary.approvedCount > 0 implies
    result.reviewSummary.averageRating =
      result.reviewSummary.approvedRatings->sum() /
      result.reviewSummary.approvedCount)
~~~

~~~text
BR-STAY-DETAIL-05 - Current Offer Is Bound To The Selected Context
Source: Assumption
context StayService::getDetail(stayId: String, offerId: String): StayDetail
post BR_STAY_DETAIL_05_CurrentOfferIsBoundToTheSelectedContext:
  (offerId = null implies result.currentOffer = null) and
  (result.currentOffer <> null implies
    result.currentOffer.id = offerId and result.currentOffer.stay = result.stay and
    result.currentOffer.available and result.currentOffer.expiresAt > RequestContext::startedAt)
~~~

~~~text
BR-STAY-DETAIL-06 - Detail Retrieval Is Read Only
Source: Assumption
context StayService::getDetail(stayId: String, offerId: String): StayDetail
post BR_STAY_DETAIL_06_DetailRetrievalIsReadOnly:
  ReadState::stays() = ReadState::stays()@pre
~~~

~~~text
BR-STAY-DETAIL-07 - Review Aggregate Uses The Selected Stay
Source: Assumption
context StayService::getDetail(stayId: String, offerId: String): StayDetail
post BR_STAY_DETAIL_07_ReviewAggregateUsesTheSelectedStay:
  result.reviewSummary.approvedRatings =
    Review.allInstances()->select(r |
      r.stayId = stayId and r.published and
      r.moderationStatus = ModerationStatus::APPROVED and
      r.publishedAt <= RequestContext::startedAt)->collect(r | r.rating)->asBag()
~~~
