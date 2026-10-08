---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-08
uc_name: "Book a Stay"
---

# UC-08: Book a Stay

## Functional Use-Case Specification

### Use Case ID

UC-08

### Use Case Name

Book a Stay

### Description

As an authenticated traveller, I want to provide guest details and confirm an available stay offer.

### Actor(s)

Authenticated Traveller; Stay Service; Payment Provider.

### Priority

P0.

### Trigger

The traveller chooses to continue from a stay offer to checkout.

### Pre-Condition(s)

PRE-1: The traveller is viewing checkout for a selected stay-offer context.

### Post-Condition(s)

POST-1: The client displays the checkout outcome returned by the system.

POST-2: The interface exposes the continuation supplied with that outcome.

### Basic Flow

1. The traveller opens checkout from a selected stay offer.
2. The client requests a checkout summary for the current context.
3. The system processes the request and returns a checkout-summary outcome.
4. The client presents the returned summary and the contact, home-address, booking-party, work-travel, payment, and save-card controls shown in checkout.
5. The traveller reviews the summary, completes the displayed controls, and confirms.
6. The client submits the confirmation request.
7. The system processes the request and returns a booking outcome.
8. The client renders the returned outcome and its available continuation.

### Alternative Flow

AF-1: Review a Refreshed Stay Checkout Summary

4a: If a refreshed checkout summary is returned, the client presents it for review before confirmation.

AF-2: Use Stay Booking Recovery Actions

8a: After a recoverable outcome, the traveller uses one of the displayed recovery actions.

### Exception Flow

EF-1: Retry Stay Booking Confirmation

7a: If the client receives no confirmation response, it displays a retry state.

7b: The traveller chooses retry and the client resubmits the confirmation request.

7c: The client displays the returned booking outcome.

### Related UI

hotel reservation page; stay checkoutmobile; Your Selection; Your Details; Final Step; Home Address; Who are you booking for?; Are you travelling for work?; Save card details; Book now.

### Related API IDs

API-STAY-QUOTE; API-STAY-BOOKING-CREATE.

### Notes

None.

## UML Model

~~~plantuml
@startuml
hide empty members

enum BookingStatus {
  PENDING
  CONFIRMED
  FAILED
  CANCELLED
}

enum BookingFor {
  MAIN_GUEST
  SOMEONE_ELSE
}

enum QuoteStatus {
  ACTIVE
  EXPIRED
  CONSUMED
  UNAVAILABLE
}

enum PaymentStatus {
  REFUNDED
  PENDING
  AUTHORIZED
  FAILED
  NOT_REQUIRED
}

class String {
  +trim(): String
}

class DateTime {
  +<=(other: DateTime): Boolean
  +>(other: DateTime): Boolean
}

class RequestContext {
  +{static} authenticatedUserId: String
  +{static} startedAt: DateTime
}

class User {
  +id: String
  +active: Boolean
}

class Money {
  +amount: Real
  +currency: String
}

class StayOffer {
  +id: String
  +rooms: Integer
  +available: Boolean
  +total: Money
  +availableRooms: Integer
  +expiresAt: DateTime
  +version: Integer
}

class StayQuote {
  +id: String
  +available: Boolean
  +total: Money
  +expiresAt: DateTime
  +user: User
  +offer: StayOffer
  +offerVersion: Integer
  +status: QuoteStatus
}

class StayBooking {
  +user: User
  +offer: StayOffer
  +quote: StayQuote
  +status: BookingStatus
  +total: Money
  +idempotencyKey: String
  +paymentReference: PaymentReference
  +requestFingerprint: String
  +providerReservationRef: String
  +guest: GuestDetails
  +savedPaymentMethod: SavedPaymentMethod
}

class SavedPaymentMethod {
  +user: User
  +providerReference: String
}

class PaymentReference {
  +tokenFingerprint: String
  +status: PaymentStatus
}

class StayService {
  +quote(offerId: String): StayQuote
  +book(command: StayBookingCommand): StayBooking
}

class GuestDetails {
  +firstName: String
  +lastName: String
  +homeAddress: String
  +email: String
  +phone: String
  +countryCode: String
  +bookingFor: BookingFor
  +workTravel: Boolean
}

class StayBookingCommand {
  +guest: GuestDetails
  +paymentToken: String
  +savePaymentMethod: Boolean
  +idempotencyKey: String
  +quoteId: String
  +requestFingerprint: String
}

class Validation {
  +{static} isEmail(value: String): Boolean
  +{static} isPhone(value: String): Boolean
  +{static} isCountryCode(value: String): Boolean
}

class PaymentFingerprint {
  +{static} of(value: String): String
}

class RequestFingerprint {
  +{static} of(command: StayBookingCommand): String
}

class ReadState {
  +{static} stayBookings(): String
  +{static} payments(): String
}

class ProviderInventory {
  +{static} reservations(): String
}

StayQuote --> User : user
StayQuote --> StayOffer : offer
StayQuote --> QuoteStatus : status
StayBooking --> User : user
StayBooking --> StayOffer : offer
StayBooking --> StayQuote : quote
StayBooking --> BookingStatus : status
StayBooking --> PaymentReference : paymentReference
StayBooking --> GuestDetails : guest
StayBooking --> SavedPaymentMethod : savedPaymentMethod
SavedPaymentMethod --> User : user
PaymentReference --> PaymentStatus : status
GuestDetails --> BookingFor : bookingFor
StayBookingCommand --> GuestDetails : guest
StayOffer --> "1" Money : total
StayQuote --> "1" Money : total
StayBooking --> "1" Money : total

@enduml
~~~

## Business Rules

~~~text
BR-BOOK-STAY-01 - New Booking Uses Live Quote Or Replays Existing Intent
Source: Assumption
context StayService::book(command: StayBookingCommand): StayBooking
pre BR_BOOK_STAY_01_NewBookingUsesLiveQuoteOrReplaysExistingIntent:
  let prior = StayBooking.allInstances()->select(b |
    b.user.id = RequestContext::authenticatedUserId and b.idempotencyKey = command.idempotencyKey) in
  if prior->notEmpty() then
    prior->one(b | b.requestFingerprint = command.requestFingerprint and b.quote.id = command.quoteId)
  else
    StayQuote.allInstances()->one(q |
      q.id = command.quoteId and q.user.id = RequestContext::authenticatedUserId and
      q.status = QuoteStatus::ACTIVE and q.expiresAt > RequestContext::startedAt and
      q.offer.available and q.offer.expiresAt > RequestContext::startedAt and
      q.offer.version = q.offerVersion) and
    StayBooking.allInstances()->forAll(b | b.quote.id <> command.quoteId)
  endif
~~~

~~~text
BR-BOOK-STAY-02 - Fingerprint Is Server Derived And Key Matches Intent
Source: Assumption
context StayService::book(command: StayBookingCommand): StayBooking
pre BR_BOOK_STAY_02_FingerprintIsServerDerivedAndKeyMatchesIntent:
  command.idempotencyKey.trim().size() > 0 and
  command.requestFingerprint = RequestFingerprint::of(command) and
  StayBooking.allInstances()->select(b |
    b.user.id = RequestContext::authenticatedUserId and b.idempotencyKey = command.idempotencyKey)
    ->forAll(b | b.requestFingerprint = command.requestFingerprint)
~~~

~~~text
BR-BOOK-STAY-03 - Booking Is Owned And Bound To One Quote
Source: Assumption
context StayService::book(command: StayBookingCommand): StayBooking
post BR_BOOK_STAY_03_BookingIsOwnedAndBoundToOneQuote:
  result.user.id = RequestContext::authenticatedUserId and
  result.quote.id = command.quoteId and
  StayBooking.allInstances()->select(b |
    b.quote.id = command.quoteId)->size() = 1
~~~

~~~text
BR-BOOK-STAY-04 - Persisted Commercial Terms Come From The Quote
Source: Assumption
context StayService::book(command: StayBookingCommand): StayBooking
post BR_BOOK_STAY_04_PersistedCommercialTermsComeFromTheQuote:
  result.offer = result.quote.offer and
  result.total.amount = result.quote.total.amount and
  result.total.currency = result.quote.total.currency
~~~

~~~text
BR-BOOK-STAY-05 - Quote Is Consumed Atomically With Booking Creation
Source: Assumption
context StayService::book(command: StayBookingCommand): StayBooking
post BR_BOOK_STAY_05_QuoteIsConsumedAtomicallyWithBookingCreation:
  result.quote.status = QuoteStatus::CONSUMED and
  StayBooking.allInstances()->select(b |
    b.user.id = RequestContext::authenticatedUserId and
    b.idempotencyKey = command.idempotencyKey)->size() = 1
~~~

~~~text
BR-BOOK-STAY-06 - Initial State Reflects Payment Authorization
Source: Assumption
context StayService::book(command: StayBookingCommand): StayBooking
post BR_BOOK_STAY_06_InitialStateReflectsPaymentAuthorization:
  StayBooking.allInstances()@pre->forAll(b |
    b.user.id <> RequestContext::authenticatedUserId or b.idempotencyKey <> command.idempotencyKey) implies
    result.paymentReference <> null and
    ((result.paymentReference.status = PaymentStatus::AUTHORIZED and result.status = BookingStatus::CONFIRMED) or
     (result.paymentReference.status = PaymentStatus::PENDING and result.status = BookingStatus::PENDING))
~~~

~~~text
BR-BOOK-STAY-07 - Payment Reference Contains Only Derived Token Fingerprint
Source: Assumption
context StayService::book(command: StayBookingCommand): StayBooking
post BR_BOOK_STAY_07_PaymentReferenceContainsOnlyDerivedTokenFingerprint:
  result.paymentReference <> null implies
    result.paymentReference.tokenFingerprint = PaymentFingerprint::of(command.paymentToken) and
    result.paymentReference.tokenFingerprint <> command.paymentToken
~~~

~~~text
BR-BOOK-STAY-08 - New Booking Has Payment Credential And Room Capacity
Source: Assumption
context StayService::book(command: StayBookingCommand): StayBooking
pre BR_BOOK_STAY_08_NewBookingHasPaymentCredentialAndRoomCapacity:
  StayBooking.allInstances()->forAll(b |
    b.user.id <> RequestContext::authenticatedUserId or b.idempotencyKey <> command.idempotencyKey) implies
    command.paymentToken <> null and command.paymentToken.trim().size() > 0 and
    StayQuote.allInstances()->one(q | q.id = command.quoteId and q.offer.availableRooms >= q.offer.rooms)
~~~

~~~text
BR-BOOK-STAY-09 - Replay Returns Original Booking Without New Effects
Source: Assumption
context StayService::book(command: StayBookingCommand): StayBooking
post BR_BOOK_STAY_09_ReplayReturnsOriginalBookingWithoutNewEffects:
  let prior = StayBooking.allInstances()@pre->select(b |
    b.user.id = RequestContext::authenticatedUserId and b.idempotencyKey = command.idempotencyKey) in
  result.idempotencyKey = command.idempotencyKey and
  result.requestFingerprint = command.requestFingerprint and
  (if prior->notEmpty() then
    result = prior->any(b | true) and
    ReadState::stayBookings() = ReadState::stayBookings()@pre and
    ReadState::payments() = ReadState::payments()@pre
  else
    result.oclIsNew() and
    StayBooking.allInstances()->size() = StayBooking.allInstances()@pre->size() + 1
  endif)
~~~

~~~text
BR-BOOK-STAY-10 - Quote Requires Authenticated User And Live Offer
Source: Assumption
context StayService::quote(offerId: String): StayQuote
pre BR_BOOK_STAY_10_QuoteRequiresAuthenticatedUserAndLiveOffer:
  User.allInstances()->one(u | u.id = RequestContext::authenticatedUserId and u.active) and
  StayOffer.allInstances()->one(o |
    o.id = offerId and o.available and o.expiresAt > RequestContext::startedAt)
~~~

~~~text
BR-BOOK-STAY-11 - Issued Quote Captures Revalidated Offer Terms
Source: Assumption
context StayService::quote(offerId: String): StayQuote
post BR_BOOK_STAY_11_IssuedQuoteCapturesRevalidatedOfferTerms:
  result.oclIsNew() and result.offer.id = offerId and
  result.user.id = RequestContext::authenticatedUserId and
  result.offerVersion = result.offer.version and result.status = QuoteStatus::ACTIVE and
  result.available and result.total = result.offer.total and
  result.expiresAt > RequestContext::startedAt and result.expiresAt <= result.offer.expiresAt
~~~

~~~text
BR-BOOK-STAY-12 - Guest Contact And Authenticated Owner Are Usable
Source: Assumption
context StayService::book(command: StayBookingCommand): StayBooking
pre BR_BOOK_STAY_12_GuestContactAndAuthenticatedOwnerAreUsable:
  User.allInstances()->one(u | u.id = RequestContext::authenticatedUserId and u.active) and
  command.guest.firstName.trim().size() > 0 and command.guest.lastName.trim().size() > 0 and
  command.guest.homeAddress.trim().size() > 0 and Validation::isEmail(command.guest.email) and Validation::isPhone(command.guest.phone) and
  Validation::isCountryCode(command.guest.countryCode)
~~~

~~~text
BR-BOOK-STAY-13 - New Booking Reserves Provider Inventory Once
Source: Assumption
context StayService::book(command: StayBookingCommand): StayBooking
post BR_BOOK_STAY_13_NewBookingReservesProviderInventoryOnce:
  result.oclIsNew() implies
    result.providerReservationRef <> null and result.providerReservationRef.trim().size() > 0 and
    StayBooking.allInstances()->isUnique(b | b.providerReservationRef)
~~~

~~~text
BR-BOOK-STAY-14 - Quote Does Not Reserve Inventory Or Authorize Payment
Source: Assumption
context StayService::quote(offerId: String): StayQuote
post BR_BOOK_STAY_14_QuoteDoesNotReserveInventoryOrAuthorizePayment:
  StayBooking.allInstances() = StayBooking.allInstances()@pre and
  ReadState::payments() = ReadState::payments()@pre and
  ProviderInventory::reservations() = ProviderInventory::reservations()@pre
~~~

~~~text
BR-BOOK-STAY-15 - Booking Retains The Submitted Guest Contact
Source: Assumption
context StayService::book(command: StayBookingCommand): StayBooking
post BR_BOOK_STAY_15_BookingRetainsTheSubmittedGuestContact:
  result.guest.firstName = command.guest.firstName and result.guest.lastName = command.guest.lastName and
  result.guest.homeAddress = command.guest.homeAddress and result.guest.email = command.guest.email and
  result.guest.phone = command.guest.phone and result.guest.countryCode = command.guest.countryCode and
  result.guest.bookingFor = command.guest.bookingFor and result.guest.workTravel = command.guest.workTravel
~~~


~~~text
BR-BOOK-STAY-16 - Save Card Choice Controls The Saved Provider Reference
Source: Figma
context StayService::book(command: StayBookingCommand): StayBooking
post BR_BOOK_STAY_16_SaveCardChoiceControlsTheSavedProviderReference:
  (command.savePaymentMethod implies
    result.savedPaymentMethod <> null and result.savedPaymentMethod.user = result.user and
    result.savedPaymentMethod.providerReference <> command.paymentToken) and
  (not command.savePaymentMethod implies result.savedPaymentMethod = null)
~~~
