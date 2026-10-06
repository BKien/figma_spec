---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-05
uc_name: "Make Payment"
---

# UC-05: Make Payment

## Functional Use-Case Specification

### Use Case ID

UC-05

### Use Case Name

Make Payment

### Description

As a visitor, I want to provide payment information and confirm my Tripma checkout so that my booking can be completed.

### Actor(s)

Visitor; Authenticated User

### Priority

High

### Trigger

The visitor continues from the Tripma seat-selection experience to payment.

### Pre-Condition(s)

PRE-1: The current Tripma checkout context is available.
PRE-2: The payment experience can access the context prepared by the preceding booking steps.

### Post-Condition(s)

POST-1: When checkout succeeds, Tripma makes a booking-confirmation context available to the success experience.
POST-2: Tripma associates the completed checkout with the applicable visitor context.
POST-3: When checkout cannot be completed, Tripma keeps the visitor in the payment experience and reports the outcome.

### Basic Flow

1. Tripma opens the payment experience for the current checkout.
2. Tripma presents the available payment and supporting checkout controls.
3. The visitor chooses a payment path and supplies the requested information.
4. The visitor completes the billing-address option offered by the experience.
5. Tripma evaluates the current checkout form according to the Business Rules of this use case.
6. The visitor chooses Confirm and pay.
7. Tripma presents the processing state.
8. Tripma submits the checkout request through API-BOOKING-CREATE.
9. The checkout service evaluates the request and current booking contexts according to the Business Rules.
10. The checkout service processes the selected payment path.
11. The booking service completes the booking operation.
12. API-BOOKING-CREATE returns the booking-confirmation response.
13. Tripma makes the confirmation context available to the current workflow.
14. If an authenticated save-card intent was recorded, Tripma invokes UC-13 — Save Payment Method with the completed booking reference.
15. Tripma opens the booking-success experience.

### Alternative Flow

AF-1: Return to seat selection
6a. The visitor chooses Back to seat select.
6b. Tripma returns to the existing seat-selection context.

AF-2: Create an account during checkout
3a. The visitor chooses the account-creation option exposed by the payment experience.
3b. Tripma invokes UC-07 — Sign Up.
3c. When UC-07 succeeds, Tripma invokes UC-08 — Sign In for the new account.
3d. When UC-08 succeeds, the authenticated checkout context is restored.
3e. The Basic Flow resumes at step 3.

AF-3: Save the payment method
3f. The authenticated visitor chooses the save-card option exposed by the payment experience.
3g. Tripma records the save-card intent without creating a saved payment method yet.
3h. The Basic Flow resumes at step 3; UC-13 is invoked only after step 12 has returned a completed booking reference.

AF-4: Use another payment path
3a. The visitor chooses another payment path offered by Tripma.
3b. Tripma presents the corresponding controls.
3c. The Basic Flow resumes at step 3.

AF-5: Use the primary-passenger billing address
4i. The visitor chooses the corresponding billing-address option.
4j. Tripma updates the checkout form according to the Business Rules.
4k. The Basic Flow resumes at step 5.

### Exception Flow

EF-1: Checkout information requires attention
5a. If the checkout form does not satisfy the Business Rules, Tripma identifies the affected input and does not submit the booking request.

EF-2: Supporting use case cannot be completed
3a. If an invoked supporting use case does not succeed, Tripma returns to the payment experience with its usable checkout state.

EF-3: Payment is not accepted
10a. If payment processing does not succeed, API-BOOKING-CREATE returns the corresponding payment outcome.
10b. Tripma preserves the usable checkout state and does not open the success experience.

EF-4: Booking context changed
9a. If the current booking contexts can no longer be accepted, API-BOOKING-CREATE returns a conflict outcome.
9b. Tripma directs the visitor to the affected booking step.

EF-5: Booking operation fails
11a. If the booking operation cannot be completed, Tripma presents a recoverable outcome.
11b. No success experience is opened.

EF-6: Request cannot be completed
8a. If Tripma cannot complete the request because of a technical failure, it preserves the checkout form and presents a retryable error state.

EF-7: Payment method cannot be saved
14a. If UC-13 cannot save the reusable payment method after booking completion, Tripma reports that outcome without reversing the completed booking or payment.
14b. The Basic Flow resumes at step 15.

### Related UI

Tripma payment experience in the booking workflow

### Related API IDs

API-BOOKING-CREATE; API-AUTH-SIGNUP through UC-07; API-AUTH-SIGNIN through UC-08; API-PAYMENT-METHOD-SAVE through UC-13

### Notes

Scope clarification: This use case covers payment authorization and booking completion. UC-07, UC-08, and UC-13 are referenced only as supporting use cases.

## UML Model

~~~plantuml
@startuml
hide empty members

enum PaymentMethod {
  CREDIT_CARD
  GOOGLE_PAY
  APPLE_PAY
  PAYPAL
  CRYPTO
}

enum PaymentStatus {
  PENDING
  AUTHORIZED
  DECLINED
  COMPLETED
  FAILED
}

enum BookingStatus {
  CONFIRMED
}

class User <<Entity>> {
  id: UUID [1]
}

class Booking <<Entity>> {
  id: UUID [1]
  confirmationCode: String [1]
}

class BookingCancellationTerm <<Entity>> {
  id: UUID [1]
}

class PaymentInfo <<Entity>> {
  bookingId: UUID [1]
  status: PaymentStatus [1]
  providerTransactionId: String [1]
  amount: Decimal [1]
  currency: String [1]
}

class BillingAddressInputDto <<DTO>> {
  ' Only the type is referenced by this use case's Business Rules.
}

class PaymentInputDto <<DTO>> {
  paymentMethod: PaymentMethod [1]
  nameOnCard: String [0..1]
  cardNumber: String [0..1]
  securityCode: String [0..1]
  expireDate: Date [0..1]
  providerToken: String [0..1]
}

class MakePaymentDto <<DTO>> {
  seatSelectionContextKey: String [1]
  payment: PaymentInputDto [1]
  billingAddress: BillingAddressInputDto [1]
}

class CheckoutContextDto <<DTO>> {
  totalUpgradeAmount: Decimal [1]
}

class BookingConfirmationDto <<DTO>> {
  bookingId: UUID [1]
  confirmationCode: String [1]
  status: BookingStatus [1]
  paymentStatus: PaymentStatus [1]
  flightSubtotal: Decimal [1]
  taxesAndFees: Decimal [1]
  baggageFees: Decimal [1]
  upgradeFees: Decimal [1]
  total: Decimal [1]
  currency: String [1]
  createdAt: DateTime [1]
}

class MakePaymentResponseDto <<DTO>> {
  success: Boolean [1]
  data: BookingConfirmationDto [0..1]
}

class MakePaymentService <<Service>> {
  canSubmit(dto: MakePaymentDto, currentUserId: UUID [0..1]): Boolean
  makePayment(dto: MakePaymentDto, currentUserId: UUID [0..1], idempotencyKey: String): MakePaymentResponseDto
  checkoutContextFor(seatSelectionContextKey: String): CheckoutContextDto [0..1] {query}
  hasConsistentCheckoutLineage(context: CheckoutContextDto): Boolean {query}
  isPaymentCardNumber(cardNumber: String): Boolean {query}
  isCardSecurityCode(securityCode: String): Boolean {query}
  isFutureCardExpiry(expireDate: Date): Boolean {query}
  isBillingAddressValid(address: BillingAddressInputDto, context: CheckoutContextDto): Boolean {query}
  isCheckoutInventoryAvailable(context: CheckoutContextDto): Boolean {query}
  baggageFeeTotal(context: CheckoutContextDto): Decimal {query}
  isCompleteBookingGraph(bookingId: UUID, context: CheckoutContextDto): Boolean {query}
}

MakePaymentDto "1" *-- "1" PaymentInputDto : payment
MakePaymentDto "1" *-- "1" BillingAddressInputDto : billing address
MakePaymentDto ..> CheckoutContextDto : resolves
MakePaymentResponseDto "1" *-- "0..1" BookingConfirmationDto : data
MakePaymentService ..> MakePaymentDto
MakePaymentService ..> MakePaymentResponseDto
MakePaymentService ..> CheckoutContextDto
PaymentInfo --> "1" PaymentStatus : status
PaymentInputDto --> "1" PaymentMethod : paymentMethod
BookingConfirmationDto --> "1" BookingStatus : status
BookingConfirmationDto --> "1" PaymentStatus : paymentStatus

@enduml
~~~

## Business Rules

The following rules are authoritative for Prompt E. OCL is preserved where applicable; technical or non-OCL constraints remain authoritative natural-language requirements.

~~~text
BR-PAY-001: Current checkout context
context MakePaymentService::makePayment(
  dto : MakePaymentDto,
  currentUserId : UUID,
  idempotencyKey : String
) : MakePaymentResponseDto
pre BR_PAY_001_ContextAvailable:
  not dto.seatSelectionContextKey.oclIsUndefined() and
  trim(dto.seatSelectionContextKey) <> '' and
  not checkoutContextFor(dto.seatSelectionContextKey).oclIsUndefined()
pre BR_PAY_001_ContextLineage:
  hasConsistentCheckoutLineage(
    checkoutContextFor(dto.seatSelectionContextKey)
  )


BR-PAY-002: Guest or authenticated checkout
context MakePaymentService::makePayment(
  dto : MakePaymentDto,
  currentUserId : UUID,
  idempotencyKey : String
) : MakePaymentResponseDto
pre BR_PAY_002_CurrentUser:
  currentUserId.oclIsUndefined() or
  User.allInstances()->exists(user | user.id = currentUserId)


BR-PAY-003: Supported payment method
context MakePaymentService::makePayment(
  dto : MakePaymentDto,
  currentUserId : UUID,
  idempotencyKey : String
) : MakePaymentResponseDto
pre BR_PAY_003_Method:
  PaymentMethod::allInstances()->includes(dto.payment.paymentMethod)


BR-PAY-004: Credit-card information
context MakePaymentService::makePayment(
  dto : MakePaymentDto,
  currentUserId : UUID,
  idempotencyKey : String
) : MakePaymentResponseDto
pre BR_PAY_004_CardFields:
  dto.payment.paymentMethod = PaymentMethod::CREDIT_CARD implies
    not dto.payment.nameOnCard.oclIsUndefined() and
    trim(dto.payment.nameOnCard) <> '' and
    not dto.payment.cardNumber.oclIsUndefined() and
    not dto.payment.securityCode.oclIsUndefined() and
    not dto.payment.expireDate.oclIsUndefined()


BR-PAY-005: Credit-card number
context MakePaymentService::makePayment(
  dto : MakePaymentDto,
  currentUserId : UUID,
  idempotencyKey : String
) : MakePaymentResponseDto
pre BR_PAY_005_CardNumber:
  dto.payment.paymentMethod = PaymentMethod::CREDIT_CARD implies
    isPaymentCardNumber(dto.payment.cardNumber)


BR-PAY-006: Credit-card security code
context MakePaymentService::makePayment(
  dto : MakePaymentDto,
  currentUserId : UUID,
  idempotencyKey : String
) : MakePaymentResponseDto
pre BR_PAY_006_SecurityCode:
  dto.payment.paymentMethod = PaymentMethod::CREDIT_CARD implies
    isCardSecurityCode(dto.payment.securityCode)


BR-PAY-007: Credit-card expiration
context MakePaymentService::makePayment(
  dto : MakePaymentDto,
  currentUserId : UUID,
  idempotencyKey : String
) : MakePaymentResponseDto
pre BR_PAY_007_Expiration:
  dto.payment.paymentMethod = PaymentMethod::CREDIT_CARD implies
    isFutureCardExpiry(dto.payment.expireDate)


BR-PAY-008: Provider payment information
context MakePaymentService::makePayment(
  dto : MakePaymentDto,
  currentUserId : UUID,
  idempotencyKey : String
) : MakePaymentResponseDto
pre BR_PAY_008_ProviderToken:
  dto.payment.paymentMethod <> PaymentMethod::CREDIT_CARD implies
    not dto.payment.providerToken.oclIsUndefined() and
    trim(dto.payment.providerToken) <> ''


BR-PAY-009: Billing address
context MakePaymentService::makePayment(
  dto : MakePaymentDto,
  currentUserId : UUID,
  idempotencyKey : String
) : MakePaymentResponseDto
pre BR_PAY_009_Address:
  isBillingAddressValid(
    dto.billingAddress,
    checkoutContextFor(dto.seatSelectionContextKey)
  )


BR-PAY-010: Checkout readiness
context MakePaymentService::canSubmit(
  dto : MakePaymentDto,
  currentUserId : UUID
) : Boolean
post BR_PAY_010_Result:
  result =
    not dto.seatSelectionContextKey.oclIsUndefined() and
    trim(dto.seatSelectionContextKey) <> '' and
    not checkoutContextFor(dto.seatSelectionContextKey).oclIsUndefined() and
    hasConsistentCheckoutLineage(
      checkoutContextFor(dto.seatSelectionContextKey)) and
    (currentUserId.oclIsUndefined() or
      User.allInstances()->exists(user | user.id = currentUserId)) and
    PaymentMethod::allInstances()->includes(dto.payment.paymentMethod) and
    (if dto.payment.paymentMethod = PaymentMethod::CREDIT_CARD then
       not dto.payment.nameOnCard.oclIsUndefined() and
       trim(dto.payment.nameOnCard) <> '' and
       isPaymentCardNumber(dto.payment.cardNumber) and
       isCardSecurityCode(dto.payment.securityCode) and
       isFutureCardExpiry(dto.payment.expireDate)
     else
       not dto.payment.providerToken.oclIsUndefined() and
       trim(dto.payment.providerToken) <> ''
     endif) and
    isBillingAddressValid(
      dto.billingAddress,
      checkoutContextFor(dto.seatSelectionContextKey))


BR-PAY-011: Payment authorization
context MakePaymentService::makePayment(
  dto : MakePaymentDto,
  currentUserId : UUID,
  idempotencyKey : String
) : MakePaymentResponseDto
post BR_PAY_011_AuthorizedBeforeConfirmation:
  result.success implies
    result.data.paymentStatus = PaymentStatus::COMPLETED and
    PaymentInfo.allInstances()->one(payment |
      payment.bookingId = result.data.bookingId and
      payment.status = PaymentStatus::COMPLETED and
      payment.amount = result.data.total and
      payment.currency = result.data.currency and
      not payment.providerTransactionId.oclIsUndefined() and
      trim(payment.providerTransactionId) <> '')


BR-PAY-012: Current flight and seat inventory
context MakePaymentService::makePayment(
  dto : MakePaymentDto,
  currentUserId : UUID,
  idempotencyKey : String
) : MakePaymentResponseDto
pre BR_PAY_012_Inventory:
  isCheckoutInventoryAvailable(
    checkoutContextFor(dto.seatSelectionContextKey)
  )


BR-PAY-013: Baggage fee total
context MakePaymentService::makePayment(
  dto : MakePaymentDto,
  currentUserId : UUID,
  idempotencyKey : String
) : MakePaymentResponseDto
post BR_PAY_013_BaggageFees:
  result.success implies
    result.data.baggageFees = baggageFeeTotal(
      checkoutContextFor(dto.seatSelectionContextKey)
    )


BR-PAY-014: Upgrade fee total
context MakePaymentService::makePayment(
  dto : MakePaymentDto,
  currentUserId : UUID,
  idempotencyKey : String
) : MakePaymentResponseDto
post BR_PAY_014_UpgradeFees:
  result.success implies
    result.data.upgradeFees =
      checkoutContextFor(dto.seatSelectionContextKey).totalUpgradeAmount


BR-PAY-015: Booking total
context MakePaymentService::makePayment(
  dto : MakePaymentDto,
  currentUserId : UUID,
  idempotencyKey : String
) : MakePaymentResponseDto
post BR_PAY_015_Total:
  result.success implies
    result.data.total = result.data.flightSubtotal +
      result.data.taxesAndFees +
      result.data.baggageFees +
      result.data.upgradeFees


BR-PAY-016: Atomic and idempotent booking creation
context MakePaymentService::makePayment(
  dto : MakePaymentDto,
  currentUserId : UUID,
  idempotencyKey : String
) : MakePaymentResponseDto
pre BR_PAY_016_IdempotencyKey:
  not idempotencyKey.oclIsUndefined() and trim(idempotencyKey) <> ''
post BR_PAY_016_BookingGraph:
  result.success implies
    isCompleteBookingGraph(
      result.data.bookingId,
      checkoutContextFor(dto.seatSelectionContextKey)
    )
Technical constraints:
- Booking, passenger, emergency-contact, baggage, seat-assignment and payment writes, together with the seat-availability update, must commit in one database transaction.
- Repeating a request with the same idempotency key returns the original outcome and must not create another charge or booking.


BR-PAY-017: Booking confirmation
context MakePaymentService::makePayment(
  dto : MakePaymentDto,
  currentUserId : UUID,
  idempotencyKey : String
) : MakePaymentResponseDto
post BR_PAY_017_Confirmation:
  result.success implies
    result.data.status = BookingStatus::CONFIRMED and
    result.data.confirmationCode.size() = 12 and
    Booking.allInstances()->one(booking |
      booking.id = result.data.bookingId and
      lower(trim(booking.confirmationCode)) =
        lower(trim(result.data.confirmationCode))) and
    not result.data.createdAt.oclIsUndefined()


BR-PAY-018: Sensitive payment-data handling
Raw card numbers and security codes shall not be stored in Booking or
PaymentInfo records and shall not be returned by
API-BOOKING-CREATE.
Technical constraints:
- Raw card data and security codes must not be written to application logs, analytics, URLs or query strings.
- Provider tokens must be encrypted at rest and excluded from default ORM selection and API responses.
- A security code is used only for the immediate authorization attempt and is discarded afterward.


BR-PAY-019: Cancellation-term snapshot
Every successfully created booking shall own one BookingCancellationTerm that
captures the applicable policy code, cancellation deadline, refund rate,
cancellation fee, and currency when the booking is purchased. Later policy
changes shall not modify that recorded term.

~~~
