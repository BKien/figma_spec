---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-06
uc_name: "View Booking Confirmation"
---

# UC-06: View Booking Confirmation

## Functional Use-Case Specification

### Use Case ID

UC-06

### Use Case Name

View Booking Confirmation

### Description

As a visitor, I want to view the details of my Tripma booking confirmation after checkout.

### Actor(s)

Visitor; Authenticated User

### Priority

Medium

### Trigger

The visitor opens the Tripma booking-success experience.

### Pre-Condition(s)

PRE-1: A booking-confirmation reference is available to the current experience.
PRE-2: Tripma can attempt to resolve the referenced booking.

### Post-Condition(s)

POST-1: When the request succeeds, Tripma presents the booking-confirmation experience.
POST-2: When the experience cannot be completed, Tripma reports the applicable outcome without changing the booking.

### Basic Flow

1. The visitor opens the booking-success experience.
2. Tripma requests the referenced confirmation through API-BOOKING-CONFIRMATION-GET.
3. The confirmation service evaluates the request according to the Business Rules.
4. The API returns the confirmation view.
5. Tripma presents the confirmation message and trip summary.
6. Tripma presents the associated price and payment summaries.
7. The visitor reviews the confirmation experience.

### Alternative Flow

AF-1: Open the experience again
1a. The visitor reopens or refreshes the booking-success experience.
1b. Tripma resolves the available confirmation reference.
1c. The Basic Flow resumes at step 2.

### Exception Flow

EF-1: Confirmation reference requires attention
3a. If the confirmation request cannot be accepted, Tripma presents the corresponding access outcome.
3b. No confirmation details are presented.

EF-2: Confirmation is unavailable
4a. If the referenced confirmation cannot be resolved, Tripma presents an unavailable state.
4b. The visitor may leave the experience or retry with another available reference.

EF-3: Request cannot be completed
2a. If Tripma cannot complete a request because of a technical failure, it presents a recoverable error state.

### Related UI

Booking-success page (`/successbooking`); confirmation message; flight summary; price breakdown; payment-method summary; flight-route image

### Related API IDs

API-BOOKING-CONFIRMATION-GET

### Notes

Scope clarification: This use case only retrieves and presents the confirmation of an existing Tripma booking. Itinerary sharing is assigned to UC-09, and opening an account trip collection is assigned to UC-12.

## UML Model

~~~plantuml
@startuml
hide empty members

enum BookingStatus {
  CONFIRMED
}

enum PaymentMethod {
  CREDIT_CARD
  GOOGLE_PAY
  APPLE_PAY
  PAYPAL
  CRYPTO
}

enum PaymentStatus {
  COMPLETED
}

class Booking <<Entity>> {
  id: UUID [1]
  userId: UUID [0..1]
  departingFlightId: UUID [1]
  returningFlightId: UUID [0..1]
  status: BookingStatus [1]
  confirmationCode: String [1]
  flightSubtotal: Decimal [1]
  taxesAndFees: Decimal [1]
  baggageFees: Decimal [1]
  upgradeFees: Decimal [1]
  total: Decimal [1]
  currency: String [1]
}

class Flight <<Entity>> {
  id: UUID [1]
}

class PassengerInfo <<Entity>> {
  id: UUID [1]
  bookingId: UUID [1]
  firstName: String [1]
  lastName: String [1]
}

class PassengerBaggage <<Entity>> {
  passengerInfoId: UUID [1]
  flightId: UUID [1]
  checkedBags: Integer [1]
}

class Seat <<Entity>> {
  id: UUID [1]
  seatNumber: String [1]
  seatClass: SeatClass [1]
}

class SeatAssignment <<Entity>> {
  passengerInfoId: UUID [1]
  flightId: UUID [1]
  seatId: UUID [1]
}

enum SeatClass {
  ECONOMY
  BUSINESS
}

class PaymentInfo <<Entity>> {
  bookingId: UUID [1]
  paymentMethod: PaymentMethod [1]
  nameOnCard: String [0..1]
  cardLastFour: String [0..1]
  expireDate: Date [0..1]
}

class ConfirmationAccessDto <<DTO>> {
  bookingId: UUID [1]
  confirmationCode: String [0..1]
  currentUserId: UUID [0..1]
}

class FlightConfirmationViewDto <<DTO>> {
  flightId: UUID [1]
  currency: String [1]
}

class PassengerConfirmationViewDto <<DTO>> {
  passengerId: UUID [1]
  firstName: String [1]
  lastName: String [1]
}

class SeatConfirmationViewDto <<DTO>> {
  passengerId: UUID [1]
  flightId: UUID [1]
  seatNumber: String [1]
  seatClass: SeatClass [1]
}

class BaggageConfirmationViewDto <<DTO>> {
  passengerId: UUID [1]
  flightId: UUID [1]
  checkedBags: Integer [1]
}

class PaymentConfirmationViewDto <<DTO>> {
  paymentMethod: PaymentMethod [1]
  status: PaymentStatus [1]
  nameOnCard: String [0..1]
  cardLastFour: String [0..1]
  expireDate: Date [0..1]
}

class PriceBreakdownDto <<DTO>> {
  flightSubtotal: Decimal [1]
  taxesAndFees: Decimal [1]
  baggageFees: Decimal [1]
  upgradeFees: Decimal [1]
  total: Decimal [1]
  currency: String [1]
}

class BookingConfirmationViewDto <<DTO>> {
  bookingId: UUID [1]
  confirmationCode: String [1]
  status: BookingStatus [1]
  departingFlight: FlightConfirmationViewDto [1]
  returningFlight: FlightConfirmationViewDto [0..1]
  passengers: PassengerConfirmationViewDto [1..*]
  seatAssignments: SeatConfirmationViewDto [1..*]
  baggage: BaggageConfirmationViewDto [1..*]
  payment: PaymentConfirmationViewDto [1]
  priceBreakdown: PriceBreakdownDto [1]
}

class BookingConfirmationResponseDto <<DTO>> {
  success: Boolean [1]
  data: BookingConfirmationViewDto [0..1]
}

class BookingConfirmationService <<Service>> {
  getConfirmation(access: ConfirmationAccessDto): BookingConfirmationResponseDto
}

BookingConfirmationViewDto "1" *-- "1" FlightConfirmationViewDto : departing
BookingConfirmationViewDto "1" *-- "0..1" FlightConfirmationViewDto : returning
BookingConfirmationViewDto "1" *-- "1..*" PassengerConfirmationViewDto : passengers
BookingConfirmationViewDto "1" *-- "1..*" SeatConfirmationViewDto : seats
BookingConfirmationViewDto "1" *-- "1..*" BaggageConfirmationViewDto : baggage
BookingConfirmationViewDto "1" *-- "1" PaymentConfirmationViewDto : payment
BookingConfirmationViewDto "1" *-- "1" PriceBreakdownDto : price
BookingConfirmationResponseDto "1" *-- "0..1" BookingConfirmationViewDto : data
BookingConfirmationService ..> ConfirmationAccessDto
BookingConfirmationService ..> BookingConfirmationResponseDto
Booking --> "1" BookingStatus : status
Seat --> "1" SeatClass : seatClass
PaymentInfo --> "1" PaymentMethod : paymentMethod
SeatConfirmationViewDto --> "1" SeatClass : seatClass
PaymentConfirmationViewDto --> "1" PaymentMethod : paymentMethod
PaymentConfirmationViewDto --> "1" PaymentStatus : status
BookingConfirmationViewDto --> "1" BookingStatus : status

@enduml
~~~

## Business Rules

The following rules are authoritative for Prompt E. OCL is preserved where applicable; technical or non-OCL constraints remain authoritative natural-language requirements.

~~~text
BR-CONFIRM-001: Confirmation access
context BookingConfirmationService::getConfirmation(
  access : ConfirmationAccessDto
) : BookingConfirmationResponseDto
pre BR_CONFIRM_001_BookingAccess:
  Booking.allInstances()->one(booking |
    booking.id = access.bookingId and
    booking.status = BookingStatus::CONFIRMED and
    ((not booking.userId.oclIsUndefined() and
      booking.userId = access.currentUserId) or
     (not access.confirmationCode.oclIsUndefined() and
      lower(trim(booking.confirmationCode)) =
        lower(trim(access.confirmationCode)))))


BR-CONFIRM-002: Confirmation identity
context BookingConfirmationService::getConfirmation(
  access : ConfirmationAccessDto
) : BookingConfirmationResponseDto
post BR_CONFIRM_002_Identity:
  result.success implies
    result.data.bookingId = access.bookingId and
    result.data.status = BookingStatus::CONFIRMED and
    not result.data.confirmationCode.oclIsUndefined() and
    trim(result.data.confirmationCode) <> ''


BR-CONFIRM-003: Flight-leg projection
context BookingConfirmationService::getConfirmation(
  access : ConfirmationAccessDto
) : BookingConfirmationResponseDto
post BR_CONFIRM_003_Flights:
  result.success implies
    result.data.departingFlight.flightId =
      Booking.allInstances()->any(booking |
        booking.id = access.bookingId).departingFlightId and
    result.data.returningFlight.oclIsUndefined() =
      Booking.allInstances()->any(booking |
        booking.id = access.bookingId).returningFlightId.oclIsUndefined() and
    (not result.data.returningFlight.oclIsUndefined() implies
      result.data.returningFlight.flightId =
        Booking.allInstances()->any(booking |
          booking.id = access.bookingId).returningFlightId)


BR-CONFIRM-004: Passenger projection
context BookingConfirmationService::getConfirmation(
  access : ConfirmationAccessDto
) : BookingConfirmationResponseDto
post BR_CONFIRM_004_Passengers:
  result.success implies
    result.data.passengers->isUnique(passenger | passenger.passengerId) and
    result.data.passengers->size() =
      PassengerInfo.allInstances()->select(info |
        info.bookingId = access.bookingId)->size() and
    result.data.passengers->forAll(passenger |
      PassengerInfo.allInstances()->exists(info |
        info.id = passenger.passengerId and
        info.bookingId = access.bookingId and
        info.firstName = passenger.firstName and
        info.lastName = passenger.lastName))


BR-CONFIRM-005: Seat-assignment projection
context BookingConfirmationService::getConfirmation(
  access : ConfirmationAccessDto
) : BookingConfirmationResponseDto
post BR_CONFIRM_005_Seats:
  result.success implies
    result.data.seatAssignments->isUnique(seat |
      Tuple { passengerId : UUID = seat.passengerId,
              flightId : UUID = seat.flightId }) and
    result.data.seatAssignments->size() =
      SeatAssignment.allInstances()->select(assignment |
        PassengerInfo.allInstances()->exists(info |
          info.id = assignment.passengerInfoId and
          info.bookingId = access.bookingId))->size() and
    result.data.seatAssignments->forAll(seat |
      SeatAssignment.allInstances()->exists(assignment |
        assignment.passengerInfoId = seat.passengerId and
        assignment.flightId = seat.flightId and
        Seat.allInstances()->exists(storedSeat |
          storedSeat.id = assignment.seatId and
          storedSeat.seatNumber = seat.seatNumber and
          storedSeat.seatClass = seat.seatClass)))


BR-CONFIRM-006: Baggage projection
context BookingConfirmationService::getConfirmation(
  access : ConfirmationAccessDto
) : BookingConfirmationResponseDto
post BR_CONFIRM_006_Baggage:
  result.success implies
    result.data.baggage->size() =
      PassengerBaggage.allInstances()->select(baggage |
        PassengerInfo.allInstances()->exists(info |
          info.id = baggage.passengerInfoId and
          info.bookingId = access.bookingId))->size() and
    result.data.baggage->forAll(item |
      PassengerBaggage.allInstances()->exists(baggage |
        baggage.passengerInfoId = item.passengerId and
        baggage.flightId = item.flightId and
        baggage.checkedBags = item.checkedBags))


BR-CONFIRM-007: Price breakdown
context BookingConfirmationService::getConfirmation(
  access : ConfirmationAccessDto
) : BookingConfirmationResponseDto
post BR_CONFIRM_007_Price:
  result.success implies
    let price : PriceBreakdownDto = result.data.priceBreakdown
    in
    let booking : Booking = Booking.allInstances()->any(item |
      item.id = access.bookingId)
    in
      price.total = price.flightSubtotal + price.taxesAndFees +
        price.baggageFees + price.upgradeFees and
      price.flightSubtotal = booking.flightSubtotal and
      price.taxesAndFees = booking.taxesAndFees and
      price.baggageFees = booking.baggageFees and
      price.upgradeFees = booking.upgradeFees and
      price.total = booking.total and
      price.currency = booking.currency and
      price.flightSubtotal >= 0 and price.taxesAndFees >= 0 and
      price.baggageFees >= 0 and price.upgradeFees >= 0


BR-CONFIRM-008: Monetary currency
context BookingConfirmationService::getConfirmation(
  access : ConfirmationAccessDto
) : BookingConfirmationResponseDto
post BR_CONFIRM_008_Currency:
  result.success implies
    not result.data.priceBreakdown.currency.oclIsUndefined() and
    trim(result.data.priceBreakdown.currency) <> '' and
    result.data.departingFlight.currency = result.data.priceBreakdown.currency and
    (result.data.returningFlight.oclIsUndefined() or
      result.data.returningFlight.currency = result.data.priceBreakdown.currency)
Technical constraints:
- Currency codes and displayed monetary values use the approved Tripma currency and fixed-precision formatting policy.


BR-CONFIRM-009: Payment summary
context BookingConfirmationService::getConfirmation(
  access : ConfirmationAccessDto
) : BookingConfirmationResponseDto
post BR_CONFIRM_009_Payment:
  result.success implies
    result.data.payment.status = PaymentStatus::COMPLETED and
    PaymentInfo.allInstances()->one(payment |
      payment.bookingId = access.bookingId and
      payment.paymentMethod = result.data.payment.paymentMethod and
      payment.nameOnCard = result.data.payment.nameOnCard and
      payment.cardLastFour = result.data.payment.cardLastFour and
      payment.expireDate = result.data.payment.expireDate)


BR-CONFIRM-010: Sensitive confirmation data
The confirmation view and response shall not contain a raw card number,
card security code, payment token, password, or password hash.


BR-CONFIRM-011: Confirmation retrieval is read-only
Calling API-BOOKING-CONFIRMATION-GET shall not create, update, or delete Booking,
Flight, PassengerInfo, PassengerBaggage, Seat, SeatAssignment, or PaymentInfo records.
Technical constraints:
- Client-side recovery stores only the minimum confirmation reference needed to request the view and must not store raw payment credentials.

~~~
