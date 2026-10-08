---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-10
uc_name: "Resend the password reset email"
---

# UC-10: Resend the password reset email

## Functional Use-Case Specification

### Use Case ID

UC-10

### Use Case Name

Resend the password reset email

### Description

Request another reset email from the Check Email screen without completing a password change.

### Actor(s)

Primary: Visitor. Supporting: web client and application service.

### Priority

Medium.

### Trigger

The visitor chooses Click here to resend.

### Pre-Condition(s)

PRE-1: The Check Email screen is displayed.

### Post-Condition(s)

POST-1: The client displays the returned acknowledgement.

### Basic Flow

1. The visitor chooses Click here to resend.
2. The client submits the email request again.
3. The system returns an acknowledgement.
4. The client displays the acknowledgement on Check Email.

### Alternative Flow

AF-1: Return to login

1a: The visitor chooses Back to Login.

1b: The client displays the sign-in page.

### Exception Flow

EF-1: Retry the resend request

3a: The system returns a temporary service failure.

3b: The client presents the retry action.

3c: The visitor retries the request.

### Related UI

- [Figma node 270:721](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=270-721)
- [Figma node 245:588](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=245-588)

### Related API IDs

- [API-RESET-REQUEST](../api/API-RESET-REQUEST.md)

### Notes

Screen and text-layer evidence establishes the visible goal. Service decomposition, request shapes, and exception recovery are proposed implementation contracts; they are not extracted server behavior. See [assumptions](../../ASSUMPTIONS.md) and [coverage](../../coverage-report.md) for the supported boundary. No prototype interaction wiring was available for verification.

## UML Model

~~~plantuml
@startuml
hide empty members

class ResetService {
  +request(email: String): Accepted
}

class Accepted <<response>> {
  ' Only the type is referenced by this use case's Business Rules.
}

class Customer {
  id: String
  name: String
  email: String
  phone: String [0..1]
}

enum DeliveryStatus {
  QUEUED
  SENT
  FAILED
}

class ResetDelivery {
  customerId: String
  status: DeliveryStatus
  providerReference: String [0..1]
  createdAt: Integer
}

class Session {
  tokenHash: String
  csrfHash: String
  expiresAt: Integer
  revoked: Boolean
}

class TextSyntax <<primitive helper>> {
  {static} +canonicalEmail(value: String): String
  {static} +nonBlank(value: String): Boolean
}

ResetDelivery --> "1" DeliveryStatus : status

@enduml
~~~

## Business Rules

~~~text
BR-RESET-EMAIL-RESEND-01 - Keep Earlier Requests
Source: Assumption
context ResetService::request(email: String): Accepted
post BR_RESET_EMAIL_RESEND_01_KeepEarlierRequests:
  ResetDelivery.allInstances()@pre->forAll(d | ResetDelivery.allInstances()->includes(d) and d.customerId = d.customerId@pre and d.status = d.status@pre and d.providerReference = d.providerReference@pre and d.createdAt = d.createdAt@pre)
~~~
~~~text
BR-RESET-EMAIL-RESEND-02 - Same Destination
Source: Assumption
context ResetService::request(email: String): Accepted
post BR_RESET_EMAIL_RESEND_02_SameDestination:
  ResetDelivery.allInstances()->select(d | d.oclIsNew())->forAll(d | Customer.allInstances()->exists(c | c.id = d.customerId and c.email = TextSyntax::canonicalEmail(email)))
~~~
~~~text
BR-RESET-EMAIL-RESEND-03 - No Account Creation
Source: Assumption
context ResetService::request(email: String): Accepted
post BR_RESET_EMAIL_RESEND_03_NoAccountCreation:
  Customer.allInstances() = Customer.allInstances()@pre
~~~
~~~text
BR-RESET-EMAIL-RESEND-04 - Contact Data Preserved
Source: Assumption
context ResetService::request(email: String): Accepted
post BR_RESET_EMAIL_RESEND_04_ContactDataPreserved:
  Customer.allInstances()->forAll(c | c.email = c.email@pre and c.name = c.name@pre and c.phone = c.phone@pre)
~~~
~~~text
BR-RESET-EMAIL-RESEND-05 - Sessions Preserved
Source: Assumption
context ResetService::request(email: String): Accepted
post BR_RESET_EMAIL_RESEND_05_SessionsPreserved:
  Session.allInstances() = Session.allInstances()@pre and Session.allInstances()->forAll(s | s.tokenHash = s.tokenHash@pre and s.csrfHash = s.csrfHash@pre and s.expiresAt = s.expiresAt@pre and s.revoked = s.revoked@pre)
~~~
~~~text
BR-RESET-EMAIL-RESEND-06 - Queued Dispatch Reference
Source: Assumption
context ResetDelivery
inv BR_RESET_EMAIL_RESEND_06_QueuedDispatchReference:
  self.status = DeliveryStatus::QUEUED implies self.providerReference = null
~~~
~~~text
BR-RESET-EMAIL-RESEND-07 - Sent Dispatch Reference
Source: Assumption
context ResetDelivery
inv BR_RESET_EMAIL_RESEND_07_SentDispatchReference:
  self.status = DeliveryStatus::SENT implies (self.providerReference <> null and TextSyntax::nonBlank(self.providerReference))
~~~
