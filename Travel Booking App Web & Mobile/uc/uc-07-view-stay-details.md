# UC-07 — View Stay Details

### Description

As a traveller, I want to inspect a stay's details, amenities, reviews, location, and current offer.

### Actors

Traveller; Stay Service.

### Priority

P0.

### Trigger

**TRG-UC-07-01** — The traveller chooses a stay from a result view.

### Preconditions

- **PRE-UC-07-01** — A selected stay reference is available to the client.

### Postconditions

- **POST-UC-07-01** — The client displays the stay-detail outcome returned by the system.
- **POST-UC-07-02** — Navigation back to the originating result context remains available.

### Basic Flow

1. The traveller selects a stay result.
2. The client requests the detail associated with the selected stay.
3. The system processes the request and returns a detail outcome.
4. The client renders the detail sections represented by the response.
5. The traveller reviews the displayed sections.
6. The traveller may use an available continuation from the detail view.

### Alternative Flows

#### AF-UC-07-01

1. The traveller returns to the preserved result context.

#### AF-UC-07-02

1. If an optional section is absent from the response, the client renders the remaining detail sections.

### Exception Flows

#### EF-UC-07-01

1. If stay detail cannot be loaded, the client displays a retry state.
2. The client retains navigation back to the result view.

### UML Model

```plantuml
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
  +trim(): String
  +toLower(): String
  +matches(pattern: String): Boolean
  +includes(fragment: String): Boolean
  +concat(value: String): String
  +<(other: String): Boolean
}
class DateTime {
  +{static} now(): DateTime
  +{static} hoursBetween(start: DateTime, end: DateTime): Real
  +<(other: DateTime): Boolean
  +<=(other: DateTime): Boolean
  +>(other: DateTime): Boolean
  +>=(other: DateTime): Boolean
}
class RequestContext {
  +{static} authenticatedUserId: String
  +{static} startedAt: DateTime
}
class Location {
  +id: String
  +name: String
  +countryCode: String
  +active: Boolean
  +serviceAreaId: String
  +timeZone: String
  +airTravel: Boolean
}
class Money {
  +amount: Real
  +currency: String
}
class DateRange {
  +start: Date
  +end: Date
}
class Stay {
  +id: String
  +name: String
  +location: Location
  +rating: Real
  +active: Boolean
  +amenities: String[*] {ordered}
  +media: StayMedia[*] {ordered}
}
class StayOffer {
  +id: String
  +stay: Stay
  +period: DateRange
  +rooms: Integer
  +available: Boolean
  +total: Money
  +providerOfferRef: String
  +destinationId: String
  +adults: Integer
  +availableRooms: Integer
  +expiresAt: DateTime
  +searchContextId: String
  +snapshotVersion: Integer
  +rank: Integer
  +rating: Real
  +recommendationScore: Real
  +version: Integer
}
class Review {
  +id: String
  +authorName: String
  +rating: Integer
  +comment: String
  +published: Boolean
  +publishedAt: DateTime
  +featuredRank: Integer
  +authorId: String
  +displayedAuthorName: String
  +bookingId: String
  +tripCompletionStatus: TripCompletionStatus
  +verifiedBooking: Boolean
  +moderationStatus: ModerationStatus
  +stayId: String
}
class StayService {
  +getDetail(stayId: String, offerId: String): StayDetail
}
class StayMedia {
  +id: String
  +sortOrder: Integer
  +mediaUrl: String
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
class Date {
  +<(other: Date): Boolean
  +<=(other: Date): Boolean
  +>(other: Date): Boolean
  +>=(other: Date): Boolean
}
class ReadState {
  +{static} users(): String
  +{static} sessions(): String
  +{static} stays(): String
  +{static} stayBookings(): String
  +{static} taxiBookings(): String
  +{static} payments(): String
  +{static} editorial(): String
  +{static} reviews(): String
}
Stay --> Location : location
Stay "1" o-- "0..*" StayMedia : media
StayOffer --> Stay : stay
StayOffer --> DateRange : period
Review --> TripCompletionStatus : tripCompletionStatus
Review --> ModerationStatus : moderationStatus
StayDetail --> Stay : stay
StayDetail --> ReviewSummary : reviewSummary
StayDetail --> StayOffer : currentOffer
@enduml
```

### Business Rules

```ocl
-- BR-UC-07-01
-- Source: Assumption
context StayService::getDetail(stayId: String, offerId: String): StayDetail
post BR_UC_07_01_DetailRepresentsTheSelectedActiveStay:
  result <> null and result.stay.id = stayId and result.stay.active
```

```ocl
-- BR-UC-07-02
-- Source: Assumption
context StayService::getDetail(stayId: String, offerId: String): StayDetail
post BR_UC_07_02_AmenitiesAreCanonicalAndNonRepeating:
  result.stay.amenities->forAll(a | a = a.trim().toLower()) and
  result.stay.amenities->isUnique(a | a)
```

```ocl
-- BR-UC-07-03
-- Source: Assumption
context StayService::getDetail(stayId: String, offerId: String): StayDetail
post BR_UC_07_03_MediaOrderIsStableAndGapFree:
  result.stay.media->isUnique(m | m.id) and
  (result.stay.media->isEmpty() or
   Sequence{1..result.stay.media->size()}->forAll(i | result.stay.media->at(i).sortOrder = i))
```

```ocl
-- BR-UC-07-04
-- Source: Assumption
context StayService::getDetail(stayId: String, offerId: String): StayDetail
post BR_UC_07_04_ReviewSummaryIsDerivedOnlyFromApprovedRatings:
  result.reviewSummary.approvedCount =
    result.reviewSummary.approvedRatings->size() and
  (result.reviewSummary.approvedCount = 0 implies
    result.reviewSummary.averageRating = 0) and
  (result.reviewSummary.approvedCount > 0 implies
    result.reviewSummary.averageRating =
      result.reviewSummary.approvedRatings->sum() /
      result.reviewSummary.approvedCount)
```

```ocl
-- BR-UC-07-05
-- Source: Assumption
context StayService::getDetail(stayId: String, offerId: String): StayDetail
post BR_UC_07_05_CurrentOfferIsBoundToTheSelectedContext:
  (offerId = null implies result.currentOffer = null) and
  (result.currentOffer <> null implies
    result.currentOffer.id = offerId and result.currentOffer.stay = result.stay and
    result.currentOffer.available and result.currentOffer.expiresAt > RequestContext::startedAt)
```

```ocl
-- BR-UC-07-06
-- Source: Assumption
context StayService::getDetail(stayId: String, offerId: String): StayDetail
post BR_UC_07_06_DetailRetrievalIsReadOnly:
  ReadState::stays() = ReadState::stays()@pre
```

```ocl
-- BR-UC-07-07
-- Source: Assumption
context StayService::getDetail(stayId: String, offerId: String): StayDetail
post BR_UC_07_07_ReviewAggregateUsesTheSelectedStay:
  result.reviewSummary.approvedRatings =
    Review.allInstances()->select(r |
      r.stayId = stayId and r.published and
      r.moderationStatus = ModerationStatus::APPROVED and
      r.publishedAt <= RequestContext::startedAt)->collect(r | r.rating)->asBag()
```

### Related UI

`hotel southern details page`; `stay details mobile`.

### Related APIs

`API-STAY-DETAIL`.
