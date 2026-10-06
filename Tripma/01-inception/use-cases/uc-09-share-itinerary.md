---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-09
uc_name: "Share Itinerary"
---

# UC-09: Share Itinerary

## Functional Use-Case Specification

### Use Case ID

UC-09

### Use Case Name

Share Itinerary

### Description

As a visitor, I want to share an existing Tripma booking itinerary with selected recipients by email.

### Actor(s)

Visitor; Authenticated User

### Priority

Medium

### Trigger

The visitor initiates itinerary sharing from an available booking-confirmation experience.

### Pre-Condition(s)

PRE-1: A booking-confirmation reference is available to the current experience.
PRE-2: Tripma can attempt to resolve the referenced booking.

### Post-Condition(s)

POST-1: When sharing succeeds, Tripma records the sharing outcome for the referenced booking.
POST-2: When sharing cannot be completed, Tripma reports the outcome without changing the booking.

### Basic Flow

1. The visitor initiates itinerary sharing for the current booking confirmation.
2. Tripma presents the itinerary-sharing experience.
3. The visitor supplies the recipient information.
4. Tripma evaluates the supplied information according to the Business Rules.
5. The visitor submits the sharing request.
6. Tripma sends the request through API-BOOKING-ITINERARY-SHARE.
7. The itinerary-sharing service evaluates the request according to the Business Rules.
8. The service prepares and delivers the referenced itinerary.
9. The service records the sharing outcome.
10. API-BOOKING-ITINERARY-SHARE returns the outcome.
11. Tripma presents the successful sharing result.

### Alternative Flow

AF-1: Share with additional recipients
3a. The visitor adds another recipient to the current request.
3b. Tripma retains the previously supplied recipients.
3c. The Basic Flow resumes at step 4.

AF-2: Cancel sharing
3a. The visitor leaves the sharing experience before submitting.
3b. Tripma returns to the booking-confirmation experience without creating a sharing record.

### Exception Flow

EF-1: Recipient information requires attention
4a. If the recipient information cannot be accepted, Tripma identifies the affected input and does not submit the request.

EF-2: Booking access is unavailable
7a. If the referenced booking cannot be accessed, API-BOOKING-ITINERARY-SHARE returns the corresponding outcome.
7b. No itinerary is delivered.

EF-3: Itinerary delivery fails
8a. If an itinerary cannot be delivered, the service records the failed delivery outcome.
8b. Tripma reports the unsuccessful recipients without changing the booking.

EF-4: Request cannot be completed
6a. If Tripma cannot complete the request because of a technical failure, it presents a retryable error state.

### Related UI

Share Itinerary experience associated with the Tripma booking confirmation

### Related API IDs

API-BOOKING-ITINERARY-SHARE

### Notes

Scope clarification: UC-09 shares an existing itinerary only. Viewing the booking confirmation remains assigned to UC-06, and booking management remains outside this use case.

## UML Model

~~~plantuml
@startuml
hide empty members

enum BookingStatus {
  CONFIRMED
}

enum ItineraryDeliveryStatus {
  SENT
  FAILED
}

class Booking <<Entity>> {
  id: UUID [1]
  userId: UUID [0..1]
  status: BookingStatus [1]
  confirmationCode: String [1]
}

class ShareItinerary <<Entity>> {
  id: UUID [1]
  bookingId: UUID [1]
  recipientEmail: String [1]
  deliveryStatus: ItineraryDeliveryStatus [1]
}

class ShareItineraryAccessDto <<DTO>> {
  bookingId: UUID [1]
  confirmationCode: String [0..1]
  currentUserId: UUID [0..1]
}

class ShareItineraryDto <<DTO>> {
  access: ShareItineraryAccessDto [1]
  recipientEmails: String [1..3]
}

class ItineraryDeliveryDto <<DTO>> {
  shareId: UUID [1]
  recipientEmail: String [1]
  deliveryStatus: ItineraryDeliveryStatus [1]
  sentAt: DateTime [0..1]
}

class ShareItineraryDataDto <<DTO>> {
  bookingId: UUID [1]
  deliveries: ItineraryDeliveryDto [1..3]
}

class ShareItineraryResponseDto <<DTO>> {
  success: Boolean [1]
  data: ShareItineraryDataDto [0..1]
}

class ShareItineraryService <<Service>> {
  canShare(dto: ShareItineraryDto): Boolean
  share(dto: ShareItineraryDto): ShareItineraryResponseDto
}

ShareItineraryDto "1" *-- "1" ShareItineraryAccessDto : access
ShareItineraryDataDto "1" *-- "1..3" ItineraryDeliveryDto : deliveries
ShareItineraryResponseDto "1" *-- "0..1" ShareItineraryDataDto : data
ShareItineraryService ..> ShareItineraryDto
ShareItineraryService ..> ShareItineraryResponseDto
ShareItineraryService ..> Booking
ShareItineraryService ..> ShareItinerary
Booking --> "1" BookingStatus : status
ShareItinerary --> "1" ItineraryDeliveryStatus : deliveryStatus
ItineraryDeliveryDto --> "1" ItineraryDeliveryStatus : deliveryStatus

@enduml
~~~

## Business Rules

The following rules are authoritative for Prompt E. OCL is preserved where applicable; technical or non-OCL constraints remain authoritative natural-language requirements.

~~~text
BR-SHARE-001: Confirmation access
context ShareItineraryService::share(
  dto : ShareItineraryDto
) : ShareItineraryResponseDto
pre BR_SHARE_001_Access:
  Booking.allInstances()->one(booking |
    booking.id = dto.access.bookingId and
    booking.status = BookingStatus::CONFIRMED and
    ((not booking.userId.oclIsUndefined() and
      booking.userId = dto.access.currentUserId) or
     (not dto.access.confirmationCode.oclIsUndefined() and
      lower(trim(booking.confirmationCode)) =
        lower(trim(dto.access.confirmationCode)))))


BR-SHARE-002: Recipient count
context ShareItineraryService::share(
  dto : ShareItineraryDto
) : ShareItineraryResponseDto
pre BR_SHARE_002_Count:
  dto.recipientEmails->size() >= 1 and
  dto.recipientEmails->size() <= 3


BR-SHARE-003: Accepted recipients
context ShareItineraryService::share(
  dto : ShareItineraryDto
) : ShareItineraryResponseDto
pre BR_SHARE_003_Emails:
  dto.recipientEmails->forAll(email |
    not email.oclIsUndefined() and
    isEmail(normalizeEmail(email)))


BR-SHARE-004: Distinct recipients
context ShareItineraryService::share(
  dto : ShareItineraryDto
) : ShareItineraryResponseDto
pre BR_SHARE_004_Distinct:
  dto.recipientEmails->isUnique(email | normalizeEmail(email))


BR-SHARE-005: Form readiness
context ShareItineraryService::canShare(
  dto : ShareItineraryDto
) : Boolean
post BR_SHARE_005_Result:
  result =
    dto.recipientEmails->size() >= 1 and
    dto.recipientEmails->size() <= 3 and
    dto.recipientEmails->forAll(email |
      not email.oclIsUndefined() and
      isEmail(normalizeEmail(email))) and
    dto.recipientEmails->isUnique(email | normalizeEmail(email))


BR-SHARE-006: Sharing records
context ShareItineraryService::share(
  dto : ShareItineraryDto
) : ShareItineraryResponseDto
post BR_SHARE_006_Records:
  result.success implies
    result.data.bookingId = dto.access.bookingId and
    result.data.deliveries->size() = dto.recipientEmails->size() and
    result.data.deliveries->forAll(delivery |
      ShareItinerary.allInstances()->one(record |
        record.id = delivery.shareId and
        record.bookingId = dto.access.bookingId and
        record.recipientEmail = delivery.recipientEmail and
        record.deliveryStatus = delivery.deliveryStatus))


BR-SHARE-007: Successful delivery
context ShareItineraryService::share(
  dto : ShareItineraryDto
) : ShareItineraryResponseDto
post BR_SHARE_007_Delivery:
  result.success implies
    result.data.deliveries->forAll(delivery |
      delivery.deliveryStatus = ItineraryDeliveryStatus::SENT and
      not delivery.sentAt.oclIsUndefined())
Technical constraints:
- A delivery is marked SENT only after the configured email provider accepts the itinerary message and returns a delivery reference.


BR-SHARE-008: Failed delivery
context ShareItineraryService::share(
  dto : ShareItineraryDto
) : ShareItineraryResponseDto
post BR_SHARE_008_Failure:
  not result.success and not result.data.oclIsUndefined() implies
    result.data.deliveries->exists(delivery |
      delivery.deliveryStatus = ItineraryDeliveryStatus::FAILED and
      delivery.sentAt.oclIsUndefined())


BR-SHARE-009: Recipient normalization
context ShareItineraryService::share(
  dto : ShareItineraryDto
) : ShareItineraryResponseDto
post BR_SHARE_009_Normalized:
  not result.data.oclIsUndefined() implies
    result.data.deliveries->forAll(delivery |
      delivery.recipientEmail = normalizeEmail(delivery.recipientEmail) and
      dto.recipientEmails->exists(email |
        normalizeEmail(email) = delivery.recipientEmail))


BR-SHARE-010: Itinerary boundary
Calling API-BOOKING-ITINERARY-SHARE shall not create, update, or delete the
referenced Booking or its flight, passenger, seat, baggage, or payment records.


BR-SHARE-011: Sensitive itinerary content
The shared itinerary and API response shall not contain a raw card number,
card security code, payment token, password, password hash, or session token.
Technical constraints:
- Recipient addresses and itinerary content must not appear in URLs, analytics, traces, or application logs.
- Email content is generated from the server-side booking projection after access is established; client-supplied itinerary content is not accepted.

~~~
