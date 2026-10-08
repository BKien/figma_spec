---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-08
uc_name: "Book a Table"
---

# UC-08: Book a Table

## Functional Use-Case Specification

### Use Case ID

UC-08

### Use Case Name

Book a Table

### Description

A customer confirms a restaurant table reservation.

### Actor(s)

Customer; client; system.

### Priority

P0.

### Trigger

The customer chooses Confirm Booking.

### Pre-Condition(s)

PRE-1: The booking form and a selected slot are visible.

### Post-Condition(s)

POST-1: The client displays the booking result.

### Basic Flow

1. The customer selects a time slot and enters booking details.
2. The client displays the confirmation view.
3. The client requests a confirmation code and displays the returned prompt.
4. The customer enters the code and confirms the booking.
5. The client submits the booking request.
6. The system returns a reservation outcome.
7. The client displays the returned confirmation.

### Alternative Flow

AF-1: Return to Slot Selection

2a: The customer returns to slot selection from the confirmation view.

### Exception Flow

EF-1: Booking Conflict

6a: The client displays the returned booking conflict and offers the slot list again.

### Related UI

- [Confirm Booking](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=295-495) (295:495)
- [Confirm Booking OTP](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=2383-2998) (2383:2998)
- [table booked](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=772-1193) (772:1193)

### Related API IDs

- [API-BOOKING-CREATE](../api/API-BOOKING-CREATE.md)
- [API-BOOKING-CHALLENGE](../api/API-BOOKING-CHALLENGE.md)

### Notes

The UI establishes the interaction boundary. Rule values and persistence behavior are explicit assumptions in [ASSUMPTIONS.md](../../ASSUMPTIONS.md).

## UML Model

~~~plantuml
@startuml
hide empty members

enum BookingStatus {
  CONFIRMED
  CANCELLED
  COMPLETED
}

enum ChallengePurpose {
  REGISTRATION
  BOOKING
}

class Account {
  +id: String
}

class Restaurant {
  +id: String
}

class ReservationSlot {
  +id: String
  +restaurant: Restaurant
  +startsAt: DateTime
  +remainingSeats: Integer
  +version: Integer
}

class VerificationChallenge {
  +id: String
  +account: Account
  +codeHash: String
  +purpose: ChallengePurpose
  +expiresAt: DateTime
  +consumedAt: DateTime
}

class Booking {
  +id: String
  +account: Account
  +slot: ReservationSlot
  +status: BookingStatus
  +partySize: Integer
  +contactPhoneEncrypted: String
  +idempotencyKey: String
  +requestFingerprint: String
}

class CreateBookingCommand {
  +restaurantId: String
  +slotId: String
  +partySize: Integer
  +contactPhone: String
  +verificationCode: String
  +idempotencyKey: String
}

class ChallengeCommand {
  ' Only the type is referenced by this use case's Business Rules.
}

class BookingService {
  +issueChallenge(command: ChallengeCommand): VerificationChallenge
  +create(command: CreateBookingCommand): Booking
}

class RequestContext <<utility>> {
  +{static} accountId: String
}

class CodeHash <<utility>> {
  +{static} matches(value: String, storedHash: String): Boolean
}

class PhoneCipher <<utility>> {
  +{static} matches(ciphertext: String, value: String): Boolean
}

class RequestFingerprint <<utility>> {
  +{static} of(command: CreateBookingCommand): String
}

class DateTime <<primitive>> {
  +{static} now(): DateTime
}

Account "1" -- "*" Booking
Restaurant "1" -- "*" ReservationSlot
ReservationSlot "1" -- "*" Booking
Account "1" -- "*" VerificationChallenge
VerificationChallenge --> "1" ChallengePurpose : purpose
Booking --> "1" BookingStatus : status

@enduml
~~~

## Business Rules

~~~text
BR-BOOK-TABLE-01 - Slot Can Serve Party
Source: Assumption
context BookingService::create(command: CreateBookingCommand): Booking
pre BR_BOOK_TABLE_01_SlotCanServeParty:
  Booking.allInstances()->exists(b | b.account.id = RequestContext::accountId and b.idempotencyKey = command.idempotencyKey) or ReservationSlot.allInstances()->exists(s | s.id = command.slotId and s.restaurant.id = command.restaurantId and s.remainingSeats >= command.partySize and s.startsAt > DateTime::now())
~~~
~~~text
BR-BOOK-TABLE-02 - Verified Contact
Source: Assumption
context BookingService::create(command: CreateBookingCommand): Booking
pre BR_BOOK_TABLE_02_VerifiedContact:
  Booking.allInstances()->exists(b | b.account.id = RequestContext::accountId and b.idempotencyKey = command.idempotencyKey) or VerificationChallenge.allInstances()->exists(v | v.account.id = RequestContext::accountId and v.purpose = ChallengePurpose::BOOKING and CodeHash::matches(command.verificationCode, v.codeHash) and v.expiresAt > DateTime::now() and v.consumedAt = null)
~~~
~~~text
BR-BOOK-TABLE-03 - Booking Is Bound To Slot And Owner
Source: Assumption
context BookingService::create(command: CreateBookingCommand): Booking
post BR_BOOK_TABLE_03_BookingIsBoundToSlotAndOwner:
  result.account.id = RequestContext::accountId and result.slot.id = command.slotId and result.status = BookingStatus::CONFIRMED
~~~
~~~text
BR-BOOK-TABLE-04 - Idempotent Creation
Source: Assumption
context BookingService::create(command: CreateBookingCommand): Booking
post BR_BOOK_TABLE_04_IdempotentCreation:
  let prior = Booking.allInstances()@pre->select(b | b.account.id = RequestContext::accountId and b.idempotencyKey = command.idempotencyKey) in if prior->notEmpty() then result.id = prior->any(b | true).id else Booking.allInstances()->select(b | b.account.id = RequestContext::accountId and b.idempotencyKey = command.idempotencyKey)->size() = 1 endif
~~~
~~~text
BR-BOOK-TABLE-05 - Slot Capacity Changes Atomically
Source: Assumption
context BookingService::create(command: CreateBookingCommand): Booking
post BR_BOOK_TABLE_05_SlotCapacityChangesAtomically:
  if Booking.allInstances()@pre->exists(b | b.account.id = RequestContext::accountId and b.idempotencyKey = command.idempotencyKey) then result.slot.remainingSeats = result.slot.remainingSeats@pre else ReservationSlot.allInstances()->one(s | s.id = command.slotId and s.remainingSeats = s.remainingSeats@pre - command.partySize and s.version = s.version@pre + 1) endif
~~~
~~~text
BR-BOOK-TABLE-06 - Challenge Stores Only Hash
Source: Assumption
context BookingService::issueChallenge(command: ChallengeCommand): VerificationChallenge
post BR_BOOK_TABLE_06_ChallengeStoresOnlyHash:
  result.codeHash <> null and result.purpose = ChallengePurpose::BOOKING and result.expiresAt > DateTime::now()
~~~
~~~text
BR-BOOK-TABLE-07 - Existing Key Matches Intent
Source: Assumption
context BookingService::create(command: CreateBookingCommand): Booking
pre BR_BOOK_TABLE_07_ExistingKeyMatchesIntent:
  Booking.allInstances()->select(b | b.account.id = RequestContext::accountId and b.idempotencyKey = command.idempotencyKey)->forAll(b | b.requestFingerprint = RequestFingerprint::of(command))
~~~
~~~text
BR-BOOK-TABLE-08 - Booking Copies Confirmed Party
Source: Assumption
context BookingService::create(command: CreateBookingCommand): Booking
post BR_BOOK_TABLE_08_BookingCopiesConfirmedParty:
  result.partySize = command.partySize and PhoneCipher::matches(result.contactPhoneEncrypted, command.contactPhone)
~~~
~~~text
BR-BOOK-TABLE-09 - Booking Stores Request Fingerprint
Source: Assumption
context BookingService::create(command: CreateBookingCommand): Booking
post BR_BOOK_TABLE_09_BookingStoresRequestFingerprint:
  result.requestFingerprint = RequestFingerprint::of(command)
~~~
~~~text
BR-BOOK-TABLE-10 - Booking Challenge Is Consumed
Source: Assumption
context BookingService::create(command: CreateBookingCommand): Booking
post BR_BOOK_TABLE_10_BookingChallengeIsConsumed:
  Booking.allInstances()@pre->exists(b | b.account.id = RequestContext::accountId and b.idempotencyKey = command.idempotencyKey) or VerificationChallenge.allInstances()->exists(v | v.account.id = RequestContext::accountId and v.purpose = ChallengePurpose::BOOKING and v.consumedAt <> null)
~~~
