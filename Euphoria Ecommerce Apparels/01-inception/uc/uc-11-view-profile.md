---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-11
uc_name: "View contact details"
---

# UC-11: View contact details

## Functional Use-Case Specification

### Use Case ID

UC-11

### Use Case Name

View contact details

### Description

Read the contact information displayed in My Info.

### Actor(s)

Primary: Customer. Supporting: web client and application service.

### Priority

Medium.

### Trigger

The customer chooses My info.

### Pre-Condition(s)

PRE-1: The My Account area is displayed.

### Post-Condition(s)

POST-1: The client displays the returned contact details.

### Basic Flow

1. The customer chooses My info.
2. The client requests the profile.
3. The system returns name, email, and phone information.
4. The client displays Contact Details.

### Alternative Flow

AF-1: Return to My orders

1a: The customer returns to My orders.

1b: The client displays the order-history route.

### Exception Flow

EF-1: Sign in to view the profile

3a: The system returns a rejected authentication context.

3b: The client presents the sign-in entry point.

### Related UI

- [Figma node 275:1168](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=275-1168)

### Related API IDs

- [API-PROFILE](../api/API-PROFILE.md)

### Notes

Screen and text-layer evidence establishes the visible goal. Service decomposition, request shapes, and exception recovery are proposed implementation contracts; they are not extracted server behavior. See [assumptions](../../ASSUMPTIONS.md) and [coverage](../../coverage-report.md) for the supported boundary. No prototype interaction wiring was available for verification.

## UML Model

~~~plantuml
@startuml
hide empty members

class ProfileService {
  +read(ctx: RequestContext): Customer
}

class Clock <<primitive helper>> {
  {static} +now(): Integer
}

class Customer {
  id: String
  name: String
  email: String
  phone: String [0..1]
}

class RequestContext <<input>> {
  customerId: String
  sessionHash: String
  csrfHash: String
  authenticated: Boolean
  csrfValid: Boolean
}

class Session {
  customerId: String
  tokenHash: String
  csrfHash: String
  expiresAt: Integer
  revoked: Boolean
}

class TextSyntax <<primitive helper>> {
  {static} +canonicalEmail(value: String): String
}

@enduml
~~~

## Business Rules

~~~text
BR-PROFILE-01 - Account Context
Source: Assumption
context ProfileService::read(ctx: RequestContext): Customer
pre BR_PROFILE_01_AccountContext:
  ctx.authenticated
~~~
~~~text
BR-PROFILE-02 - Profile Reference
Source: Assumption
context ProfileService::read(ctx: RequestContext): Customer
pre BR_PROFILE_02_ProfileReference:
  Customer.allInstances()->exists(c | c.id = ctx.customerId)
~~~
~~~text
BR-PROFILE-03 - Customer Profile
Source: Assumption
context ProfileService::read(ctx: RequestContext): Customer
post BR_PROFILE_03_CustomerProfile:
  result.id = ctx.customerId
~~~
~~~text
BR-PROFILE-04 - Session Authentication
Source: Assumption
context RequestContext
inv BR_PROFILE_04_SessionAuthentication:
  self.authenticated = Session.allInstances()->exists(s | s.tokenHash = self.sessionHash and s.customerId = self.customerId and not s.revoked and s.expiresAt > Clock::now())
~~~
~~~text
BR-PROFILE-05 - Csrf Context
Source: Assumption
context RequestContext
inv BR_PROFILE_05_CsrfContext:
  self.csrfValid = Session.allInstances()->exists(s | s.tokenHash = self.sessionHash and s.customerId = self.customerId and s.csrfHash = self.csrfHash and not s.revoked and s.expiresAt > Clock::now())
~~~
~~~text
BR-PROFILE-06 - Canonical Identity
Source: Assumption
context Customer
inv BR_PROFILE_06_CanonicalIdentity:
  self.email = TextSyntax::canonicalEmail(self.email) and Customer.allInstances()->isUnique(email)
~~~
~~~text
BR-PROFILE-07 - Contacts Unchanged
Source: Assumption
context ProfileService::read(ctx: RequestContext): Customer
post BR_PROFILE_07_ContactsUnchanged:
  Customer.allInstances()->forAll(c | c.name = c.name@pre and c.email = c.email@pre and c.phone = c.phone@pre)
~~~
