---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-09
uc_name: "Request a password reset email"
---

# UC-09: Request a password reset email

## Functional Use-Case Specification

### Use Case ID

UC-09

### Use Case Name

Request a password reset email

### Description

Submit an email address and reach the Check Email acknowledgement screen. Completing the reset is outside this use case.

### Actor(s)

Primary: Visitor. Supporting: web client and application service.

### Priority

Medium.

### Trigger

The visitor chooses Forget your password.

### Pre-Condition(s)

PRE-1: The Reset Your Password form is displayed.

### Post-Condition(s)

POST-1: The client displays the Check Email acknowledgement.

### Basic Flow

1. The visitor enters an email address in the reset form.
2. The client submits the email request.
3. The system returns an acknowledgement.
4. The client displays Check Email and the Back to Login link.

### Alternative Flow

AF-1: Return to login

4a: The visitor chooses Back to Login.

4b: The client displays the sign-in page.

### Exception Flow

EF-1: Retry the reset request

3a: The system returns a temporary service failure.

3b: The client presents the retry action.

3c: The visitor retries the request.

### Related UI

- [Figma node 245:588](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=245-588)
- [Figma node 270:721](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=270-721)

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
  accepted: Boolean
}

class Clock <<primitive helper>> {
  {static} +now(): Integer
}

class Customer {
  id: String
  email: String
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

class TextSyntax <<primitive helper>> {
  {static} +email(value: String): Boolean
  {static} +canonicalEmail(value: String): String
}

ResetDelivery --> "1" DeliveryStatus : status

@enduml
~~~

## Business Rules

~~~text
BR-PASSWORD-RESET-01 - Email Syntax
Source: Assumption
context ResetService::request(email: String): Accepted
pre BR_PASSWORD_RESET_01_EmailSyntax:
  TextSyntax::email(email)
~~~
~~~text
BR-PASSWORD-RESET-02 - Neutral Acknowledgement
Source: Assumption
context ResetService::request(email: String): Accepted
post BR_PASSWORD_RESET_02_NeutralAcknowledgement:
  result.accepted = true
~~~
~~~text
BR-PASSWORD-RESET-03 - Known Account Queue
Source: Assumption
context ResetService::request(email: String): Accepted
post BR_PASSWORD_RESET_03_KnownAccountQueue:
  let matches : Set(Customer) = Customer.allInstances()->select(c | c.email = TextSyntax::canonicalEmail(email)) in matches->notEmpty() implies ResetDelivery.allInstances()->one(d | d.oclIsNew() and d.customerId = matches->any(true).id and d.status = DeliveryStatus::QUEUED)
~~~
~~~text
BR-PASSWORD-RESET-04 - Unknown Address
Source: Assumption
context ResetService::request(email: String): Accepted
post BR_PASSWORD_RESET_04_UnknownAddress:
  Customer.allInstances()->forAll(c | c.email <> TextSyntax::canonicalEmail(email)) implies ResetDelivery.allInstances() = ResetDelivery.allInstances()@pre
~~~
~~~text
BR-PASSWORD-RESET-05 - Queue Cardinality
Source: Assumption
context ResetService::request(email: String): Accepted
post BR_PASSWORD_RESET_05_QueueCardinality:
  ResetDelivery.allInstances()->select(d | d.oclIsNew())->size() = (if Customer.allInstances()->exists(c | c.email = TextSyntax::canonicalEmail(email)) then 1 else 0 endif)
~~~
~~~text
BR-PASSWORD-RESET-06 - Queue Time
Source: Assumption
context ResetService::request(email: String): Accepted
post BR_PASSWORD_RESET_06_QueueTime:
  ResetDelivery.allInstances()->select(d | d.oclIsNew())->forAll(d | d.createdAt = Clock::now())
~~~
~~~text
BR-PASSWORD-RESET-07 - Dispatch Boundary
Source: Assumption
context ResetService::request(email: String): Accepted
post BR_PASSWORD_RESET_07_DispatchBoundary:
  ResetDelivery.allInstances()->select(d | d.oclIsNew())->forAll(d | d.providerReference = null)
~~~
