---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-13
uc_name: "Book a Taxi Rental"
---

# UC-13: Book a Taxi Rental

## Functional Use-Case Specification

### Use Case ID

UC-13

### Use Case Name

Book a Taxi Rental

### Description

As an authenticated traveller, I want to confirm a vehicle-and-driver rental and provide the contact and booking details shown at checkout.

### Actor(s)

Authenticated Traveller; Taxi Rental Service; Payment Provider or Driver Payment Process.

### Priority

P0.

### Trigger

The traveller chooses to continue from a Taxi offer to the reservation form.

### Pre-Condition(s)

PRE-1: The traveller is viewing checkout for a selected Taxi offer context.

### Post-Condition(s)

POST-1: The client displays the reservation outcome returned by the system.

POST-2: The interface exposes the returned continuation, including driver follow-up information when available.

### Basic Flow

1. The traveller opens the reservation form from a selected Taxi offer.
2. The client requests a checkout summary for the current context.
3. The system processes the request and returns the checkout-summary outcome.
4. The client presents the driver, vehicle, schedule, price, contact, booking-party, work-travel, payment, and save-card controls.
5. The traveller reviews the summary, completes the displayed controls, and selects Confirm Your Reservation.
6. The client submits the confirmation request.
7. The system processes the request and returns a reservation outcome.
8. The client renders the returned outcome, including the displayed driver-contact and SMS continuation.

### Alternative Flow

AF-1: Choose Pay the Driver

5a: The traveller chooses the displayed pay-the-driver option and submits the reservation.

AF-2: Reserve for Someone Else

5b: The traveller indicates that the reservation is for someone else and completes the displayed guest details.

AF-3: Review a Refreshed Taxi Checkout Summary

4a: If a refreshed checkout summary is returned, the client presents it for review before confirmation.

### Exception Flow

EF-1: Recover from a Taxi Reservation Outcome

8a: After a recoverable reservation outcome, the client retains the entered details and displays the supplied recovery action.

EF-2: Retry Taxi Reservation Confirmation

7a: If the client receives no confirmation response, it displays a retry state.

7b: The traveller chooses retry and the client resubmits the confirmation request.

7c: The client displays the returned reservation outcome.

### Related UI

Bajaj Details; taxi checkoutmobile; Enter your details; Who are you booking for?; Are you travelling for work?; No Need to Pay Now!; Confirm Your Reservation; Your Driver Will Reach Out.

### Related API IDs

API-TAXI-QUOTE; API-TAXI-BOOKING-CREATE.

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

enum PaymentMode {
  ONLINE
  PAY_DRIVER
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

class TaxiOffer {
  +paymentMode: PaymentMode
  +id: String
  +pickupAt: DateTime
  +dropoffAt: DateTime
  +available: Boolean
  +total: Money
  +deposit: Money
  +driver: Driver
  +vehicle: Vehicle
  +expiresAt: DateTime
  +version: Integer
}

class Driver {
  +id: String
  +active: Boolean
}

class Vehicle {
  +id: String
  +active: Boolean
}

class TaxiQuote {
  +id: String
  +available: Boolean
  +total: Money
  +deposit: Money
  +paymentMode: PaymentMode
  +expiresAt: DateTime
  +user: User
  +offer: TaxiOffer
  +offerVersion: Integer
  +status: QuoteStatus
}

class TaxiBooking {
  +user: User
  +offer: TaxiOffer
  +quote: TaxiQuote
  +driver: Driver
  +vehicle: Vehicle
  +status: BookingStatus
  +total: Money
  +idempotencyKey: String
  +paymentReference: PaymentReference
  +requestFingerprint: String
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

class TaxiService {
  +quote(offerId: String): TaxiQuote
  +book(command: TaxiBookingCommand): TaxiBooking
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

class TaxiBookingCommand {
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

class AllocationCalendar {
  +{static} isFree(driverId: String, vehicleId: String, start: DateTime, end: DateTime): Boolean
}

class PaymentFingerprint {
  +{static} of(value: String): String
}

class RequestFingerprint {
  +{static} ofTaxi(command: TaxiBookingCommand): String
}

class ReadState {
  +{static} taxiBookings(): String
  +{static} payments(): String
}

TaxiOffer --> PaymentMode : paymentMode
TaxiOffer --> Driver : driver
TaxiOffer --> Vehicle : vehicle
TaxiQuote --> PaymentMode : paymentMode
TaxiQuote --> User : user
TaxiQuote --> TaxiOffer : offer
TaxiQuote --> QuoteStatus : status
TaxiBooking --> User : user
TaxiBooking --> TaxiOffer : offer
TaxiBooking --> TaxiQuote : quote
TaxiBooking --> Driver : driver
TaxiBooking --> Vehicle : vehicle
TaxiBooking --> BookingStatus : status
TaxiBooking --> PaymentReference : paymentReference
TaxiBooking --> GuestDetails : guest
TaxiBooking --> SavedPaymentMethod : savedPaymentMethod
SavedPaymentMethod --> User : user
PaymentReference --> PaymentStatus : status
GuestDetails --> BookingFor : bookingFor
TaxiBookingCommand --> GuestDetails : guest
TaxiOffer --> "1" Money : total
TaxiOffer --> "1" Money : deposit
TaxiQuote --> "1" Money : total
TaxiQuote --> "1" Money : deposit
TaxiBooking --> "1" Money : total

@enduml
~~~

## Business Rules

~~~text
BR-BOOK-TAXI-01 - New Reservation Uses Live Quote Or Replays Existing Intent
Source: Assumption
context TaxiService::book(command: TaxiBookingCommand): TaxiBooking
pre BR_BOOK_TAXI_01_NewReservationUsesLiveQuoteOrReplaysExistingIntent:
  let prior = TaxiBooking.allInstances()->select(b |
    b.user.id = RequestContext::authenticatedUserId and b.idempotencyKey = command.idempotencyKey) in
  if prior->notEmpty() then
    prior->one(b | b.requestFingerprint = command.requestFingerprint and b.quote.id = command.quoteId)
  else
    TaxiQuote.allInstances()->one(q |
      q.id = command.quoteId and q.user.id = RequestContext::authenticatedUserId and
      q.status = QuoteStatus::ACTIVE and q.expiresAt > RequestContext::startedAt and
      q.offer.available and q.offer.expiresAt > RequestContext::startedAt and
      q.offer.version = q.offerVersion and q.offer.driver.active and q.offer.vehicle.active and
      AllocationCalendar::isFree(q.offer.driver.id, q.offer.vehicle.id, q.offer.pickupAt, q.offer.dropoffAt)) and
    TaxiBooking.allInstances()->forAll(b | b.quote.id <> command.quoteId)
  endif
~~~

~~~text
BR-BOOK-TAXI-02 - Fingerprint Is Server Derived And Key Matches Intent
Source: Assumption
context TaxiService::book(command: TaxiBookingCommand): TaxiBooking
pre BR_BOOK_TAXI_02_FingerprintIsServerDerivedAndKeyMatchesIntent:
  command.idempotencyKey.trim().size() > 0 and
  command.requestFingerprint = RequestFingerprint::ofTaxi(command) and
  TaxiBooking.allInstances()->select(b |
    b.user.id = RequestContext::authenticatedUserId and b.idempotencyKey = command.idempotencyKey)
    ->forAll(b | b.requestFingerprint = command.requestFingerprint)
~~~

~~~text
BR-BOOK-TAXI-03 - Guest And Authenticated Owner Are Usable
Source: Assumption
context TaxiService::book(command: TaxiBookingCommand): TaxiBooking
pre BR_BOOK_TAXI_03_GuestAndAuthenticatedOwnerAreUsable:
  User.allInstances()->one(u | u.id = RequestContext::authenticatedUserId and u.active) and
  command.guest.firstName.trim().size() > 0 and command.guest.lastName.trim().size() > 0 and
  command.guest.homeAddress.trim().size() > 0 and Validation::isEmail(command.guest.email) and
  Validation::isPhone(command.guest.phone) and Validation::isCountryCode(command.guest.countryCode)
~~~

~~~text
BR-BOOK-TAXI-04 - Payment Input Matches The Selected Mode
Source: Figma
context TaxiService::book(command: TaxiBookingCommand): TaxiBooking
pre BR_BOOK_TAXI_04_PaymentInputMatchesTheSelectedMode:
  TaxiQuote.allInstances()->one(q | q.id = command.quoteId and
    ((q.paymentMode = PaymentMode::PAY_DRIVER and command.paymentToken = null and not command.savePaymentMethod) or
     (q.paymentMode = PaymentMode::ONLINE and command.paymentToken <> null and
      command.paymentToken.trim().size() > 0)))
~~~

~~~text
BR-BOOK-TAXI-05 - Reservation Is Bound To Quote Offer And Owner
Source: Assumption
context TaxiService::book(command: TaxiBookingCommand): TaxiBooking
post BR_BOOK_TAXI_05_ReservationIsBoundToQuoteOfferAndOwner:
  result.user.id = RequestContext::authenticatedUserId and result.quote.id = command.quoteId and
  result.offer = result.quote.offer and result.driver = result.offer.driver and
  result.vehicle = result.offer.vehicle and
  TaxiBooking.allInstances()->select(b | b.quote.id = command.quoteId)->size() = 1
~~~

~~~text
BR-BOOK-TAXI-06 - Reservation Retains The Displayed Checkout Details
Source: Figma
context TaxiService::book(command: TaxiBookingCommand): TaxiBooking
post BR_BOOK_TAXI_06_ReservationRetainsTheDisplayedCheckoutDetails:
  result.guest.firstName = command.guest.firstName and result.guest.lastName = command.guest.lastName and
  result.guest.homeAddress = command.guest.homeAddress and result.guest.email = command.guest.email and
  result.guest.phone = command.guest.phone and result.guest.countryCode = command.guest.countryCode and
  result.guest.bookingFor = command.guest.bookingFor and result.guest.workTravel = command.guest.workTravel
~~~

~~~text
BR-BOOK-TAXI-07 - Commercial Terms Come From The Quote
Source: Assumption
context TaxiService::book(command: TaxiBookingCommand): TaxiBooking
post BR_BOOK_TAXI_07_CommercialTermsComeFromTheQuote:
  result.total.amount = result.quote.total.amount and result.total.currency = result.quote.total.currency and
  result.quote.paymentMode = result.offer.paymentMode
~~~

~~~text
BR-BOOK-TAXI-08 - Quote Is Consumed With One Reservation
Source: Assumption
context TaxiService::book(command: TaxiBookingCommand): TaxiBooking
post BR_BOOK_TAXI_08_QuoteIsConsumedWithOneReservation:
  result.quote.status = QuoteStatus::CONSUMED and
  TaxiBooking.allInstances()->select(b |
    b.user.id = RequestContext::authenticatedUserId and b.idempotencyKey = command.idempotencyKey)->size() = 1
~~~

~~~text
BR-BOOK-TAXI-09 - Initial State Matches The Payment Mode
Source: Figma
context TaxiService::book(command: TaxiBookingCommand): TaxiBooking
post BR_BOOK_TAXI_09_InitialStateMatchesThePaymentMode:
  (result.quote.paymentMode = PaymentMode::PAY_DRIVER implies
    result.paymentReference = null and result.status = BookingStatus::CONFIRMED) and
  (result.quote.paymentMode = PaymentMode::ONLINE implies
    result.paymentReference <> null and
    ((result.paymentReference.status = PaymentStatus::AUTHORIZED and result.status = BookingStatus::CONFIRMED) or
     (result.paymentReference.status = PaymentStatus::PENDING and result.status = BookingStatus::PENDING)))
~~~

~~~text
BR-BOOK-TAXI-10 - Replay Returns Original Reservation Without New Effects
Source: Assumption
context TaxiService::book(command: TaxiBookingCommand): TaxiBooking
post BR_BOOK_TAXI_10_ReplayReturnsOriginalReservationWithoutNewEffects:
  let prior = TaxiBooking.allInstances()@pre->select(b |
    b.user.id = RequestContext::authenticatedUserId and b.idempotencyKey = command.idempotencyKey) in
  result.idempotencyKey = command.idempotencyKey and result.requestFingerprint = command.requestFingerprint and
  (if prior->notEmpty() then
    result = prior->any(b | true) and ReadState::taxiBookings() = ReadState::taxiBookings()@pre and
    ReadState::payments() = ReadState::payments()@pre
   else result.oclIsNew() and
    TaxiBooking.allInstances()->size() = TaxiBooking.allInstances()@pre->size() + 1 endif)
~~~

~~~text
BR-BOOK-TAXI-11 - Online Payment Stores Only A Derived Reference
Source: Assumption
context TaxiService::book(command: TaxiBookingCommand): TaxiBooking
post BR_BOOK_TAXI_11_OnlinePaymentStoresOnlyADerivedReference:
  result.paymentReference <> null implies
    result.paymentReference.tokenFingerprint = PaymentFingerprint::of(command.paymentToken) and
    result.paymentReference.tokenFingerprint <> command.paymentToken
~~~

~~~text
BR-BOOK-TAXI-12 - Save Card Choice Controls The Saved Provider Reference
Source: Figma
context TaxiService::book(command: TaxiBookingCommand): TaxiBooking
post BR_BOOK_TAXI_12_SaveCardChoiceControlsTheSavedProviderReference:
  (command.savePaymentMethod implies
    result.savedPaymentMethod <> null and result.savedPaymentMethod.user = result.user and
    result.savedPaymentMethod.providerReference <> command.paymentToken) and
  (not command.savePaymentMethod implies result.savedPaymentMethod = null)
~~~

~~~text
BR-BOOK-TAXI-13 - New Reservation Claims Driver And Vehicle For The Period
Source: Assumption
context TaxiService::book(command: TaxiBookingCommand): TaxiBooking
post BR_BOOK_TAXI_13_NewReservationClaimsDriverAndVehicleForThePeriod:
  result.oclIsNew() implies
    TaxiBooking.allInstances()->forAll(b |
      b = result or Set{BookingStatus::FAILED, BookingStatus::CANCELLED}->includes(b.status) or
      (b.driver <> result.driver and b.vehicle <> result.vehicle) or
      b.offer.dropoffAt <= result.offer.pickupAt or result.offer.dropoffAt <= b.offer.pickupAt)
~~~

~~~text
BR-BOOK-TAXI-14 - Issued Quote Captures The Rental Offer
Source: Assumption
context TaxiService::quote(offerId: String): TaxiQuote
post BR_BOOK_TAXI_14_IssuedQuoteCapturesTheRentalOffer:
  result.oclIsNew() and result.offer.id = offerId and result.user.id = RequestContext::authenticatedUserId and
  result.offerVersion = result.offer.version and result.status = QuoteStatus::ACTIVE and result.available and
  result.total = result.offer.total and result.deposit = result.offer.deposit and
  result.paymentMode = result.offer.paymentMode and
  result.expiresAt > RequestContext::startedAt and result.expiresAt <= result.offer.expiresAt
~~~

~~~text
BR-BOOK-TAXI-15 - Quote Does Not Allocate Or Charge
Source: Assumption
context TaxiService::quote(offerId: String): TaxiQuote
post BR_BOOK_TAXI_15_QuoteDoesNotAllocateOrCharge:
  TaxiBooking.allInstances() = TaxiBooking.allInstances()@pre and
  ReadState::payments() = ReadState::payments()@pre
~~~
