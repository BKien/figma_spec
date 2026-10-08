---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-12
uc_name: "View Notifications"
---

# UC-12: View Notifications

## Functional Use-Case Specification

### Use Case ID

UC-12

### Use Case Name

View Notifications

### Description

A customer views booking and account notifications.

### Actor(s)

Customer; client; system.

### Priority

P1.

### Trigger

The customer opens Notifications.

### Pre-Condition(s)

PRE-1: The customer is signed in.

### Post-Condition(s)

POST-1: The client displays returned notifications.

### Basic Flow

1. The customer opens notifications.
2. The client requests notification items.
3. The system returns notification summaries.
4. The client displays the list and individual items.

### Alternative Flow

AF-1: Open a Booking from a Notification

4a: The customer opens a related booking from a notification.

### Exception Flow

EF-1: Notifications Unavailable

3a: The client shows a retry state for unavailable notifications.

### Related UI

- [notifications](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=4611-4549) (4611:4549)
- [notifications mobile variant](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=4594-4145) (4594:4145)

### Related API IDs

- [API-NOTIFICATION-LIST](../api/API-NOTIFICATION-LIST.md)

### Notes

The UI establishes the interaction boundary. Rule values and persistence behavior are explicit assumptions in [ASSUMPTIONS.md](../../ASSUMPTIONS.md).

## UML Model

~~~plantuml
@startuml
hide empty members

class Account {
  +id: String
}

class Booking {
  +account: Account
}

class Notification {
  +id: String
  +account: Account
  +booking: Booking
  +title: String
  +body: String
  +createdAt: DateTime
}

class AccountService {
  +notifications(): Sequence(Notification)
}

class RequestContext <<utility>> {
  +{static} accountId: String
}

class DateTime <<primitive>> {
  +{static} now(): DateTime
}

class SequenceUtils <<utility>> {
  +{static} isDescendingByCreatedAt(items: Sequence(Notification)): Boolean
}

Account "1" -- "*" Booking
Account "1" -- "*" Notification
Booking "1" -- "*" Notification

@enduml
~~~

## Business Rules

~~~text
BR-NOTIFICATIONS-01 - Notifications Are Owned
Source: Assumption
context AccountService::notifications(): Sequence(Notification)
post BR_NOTIFICATIONS_01_NotificationsAreOwned:
  result->forAll(n | n.account.id = RequestContext::accountId)
~~~
~~~text
BR-NOTIFICATIONS-02 - Newest Notifications First
Source: Assumption
context AccountService::notifications(): Sequence(Notification)
post BR_NOTIFICATIONS_02_NewestNotificationsFirst:
  SequenceUtils::isDescendingByCreatedAt(result)
~~~
~~~text
BR-NOTIFICATIONS-03 - Notifications Are Unique
Source: Assumption
context AccountService::notifications(): Sequence(Notification)
post BR_NOTIFICATIONS_03_NotificationsAreUnique:
  result->isUnique(n | n.id)
~~~
~~~text
BR-NOTIFICATIONS-04 - Notification Times Are Past
Source: Assumption
context AccountService::notifications(): Sequence(Notification)
post BR_NOTIFICATIONS_04_NotificationTimesArePast:
  result->forAll(n | n.createdAt <= DateTime::now())
~~~
~~~text
BR-NOTIFICATIONS-05 - Notification Titles Are Present
Source: Assumption
context AccountService::notifications(): Sequence(Notification)
post BR_NOTIFICATIONS_05_NotificationTitlesArePresent:
  result->forAll(n | n.title.trim().size() > 0)
~~~
~~~text
BR-NOTIFICATIONS-06 - Notification Bodies Are Present
Source: Assumption
context AccountService::notifications(): Sequence(Notification)
post BR_NOTIFICATIONS_06_NotificationBodiesArePresent:
  result->forAll(n | n.body.trim().size() > 0)
~~~
~~~text
BR-NOTIFICATIONS-07 - Linked Bookings Belong To Recipient
Source: Assumption
context AccountService::notifications(): Sequence(Notification)
post BR_NOTIFICATIONS_07_LinkedBookingsBelongToRecipient:
  result->forAll(n | n.booking = null or n.booking.account.id = n.account.id)
~~~
