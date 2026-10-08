---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-14
uc_name: "Contact Support"
---

# UC-14: Contact Support

## Functional Use-Case Specification

### Use Case ID

UC-14

### Use Case Name

Contact Support

### Description

A visitor submits the contact form shown by the site.

### Actor(s)

Visitor; client; system.

### Priority

P1.

### Trigger

The visitor opens Contact Us.

### Pre-Condition(s)

PRE-1: The contact page is visible.

### Post-Condition(s)

POST-1: The client displays the submission result.

### Basic Flow

1. The visitor opens Contact Us.
2. The client displays the contact form.
3. The visitor enters a message and submits it.
4. The client sends the contact request.
5. The system returns a submission receipt.
6. The client presents the receipt.

### Alternative Flow

AF-1: Leave Contact Form Without Submitting

3a: The visitor returns to the restaurant page without submitting.

### Exception Flow

EF-1: Contact Submission Error

5a: The client displays the returned contact error and keeps the form available.

### Related UI

- [Conatct Us Page](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=2345-2682) (2345:2682)
- [Contact us Page Mobile](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=2375-2627) (2375:2627)

### Related API IDs

- [API-CONTACT-CREATE](../api/API-CONTACT-CREATE.md)

### Notes

The UI establishes the interaction boundary. Rule values and persistence behavior are explicit assumptions in [ASSUMPTIONS.md](../../ASSUMPTIONS.md).

## UML Model

~~~plantuml
@startuml
hide empty members

enum ContactStatus {
  RECEIVED
  CLOSED
}

class ContactMessage {
  +id: String
  +name: String
  +emailCanonical: String
  +message: String
  +status: ContactStatus
  +createdAt: DateTime
}

class ContactCommand {
  +name: String
  +email: String
  +message: String
}

class SupportService {
  +submit(command: ContactCommand): ContactMessage
}

class Email <<utility>> {
  +{static} normalize(value: String): String
}

class DateTime <<primitive>> {
  +{static} now(): DateTime
}

ContactMessage --> "1" ContactStatus : status

@enduml
~~~

## Business Rules

~~~text
BR-CONTACT-SUPPORT-01 - Message Has Content
Source: Assumption
context SupportService::submit(command: ContactCommand): ContactMessage
pre BR_CONTACT_SUPPORT_01_MessageHasContent:
  command.message.trim().size() > 0
~~~
~~~text
BR-CONTACT-SUPPORT-02 - Submission Is Recorded
Source: Assumption
context SupportService::submit(command: ContactCommand): ContactMessage
post BR_CONTACT_SUPPORT_02_SubmissionIsRecorded:
  result.emailCanonical = Email::normalize(command.email) and result.status = ContactStatus::RECEIVED
~~~
~~~text
BR-CONTACT-SUPPORT-03 - Contact Content Is Recorded
Source: Assumption
context SupportService::submit(command: ContactCommand): ContactMessage
post BR_CONTACT_SUPPORT_03_ContactContentIsRecorded:
  result.name = command.name and result.message = command.message
~~~
~~~text
BR-CONTACT-SUPPORT-04 - Contact Name Is Present
Source: Assumption
context SupportService::submit(command: ContactCommand): ContactMessage
pre BR_CONTACT_SUPPORT_04_ContactNameIsPresent:
  command.name.trim().size() > 0
~~~
~~~text
BR-CONTACT-SUPPORT-05 - Contact Email Is Present
Source: Assumption
context SupportService::submit(command: ContactCommand): ContactMessage
pre BR_CONTACT_SUPPORT_05_ContactEmailIsPresent:
  command.email.trim().size() > 0
~~~
~~~text
BR-CONTACT-SUPPORT-06 - Contact Has Identifier
Source: Assumption
context SupportService::submit(command: ContactCommand): ContactMessage
post BR_CONTACT_SUPPORT_06_ContactHasIdentifier:
  result.id.trim().size() > 0
~~~
~~~text
BR-CONTACT-SUPPORT-07 - Contact Has Creation Time
Source: Assumption
context SupportService::submit(command: ContactCommand): ContactMessage
post BR_CONTACT_SUPPORT_07_ContactHasCreationTime:
  result.createdAt <= DateTime::now()
~~~
