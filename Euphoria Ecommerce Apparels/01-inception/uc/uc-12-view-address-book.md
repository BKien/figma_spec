---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-12
uc_name: "View saved addresses"
---

# UC-12: View saved addresses

## Functional Use-Case Specification

### Use Case ID

UC-12

### Use Case Name

View saved addresses

### Description

Read saved address cards and their shipping and billing default badges.

### Actor(s)

Primary: Customer. Supporting: web client and application service.

### Priority

Medium.

### Trigger

The customer opens the Address section of My Info.

### Pre-Condition(s)

PRE-1: The My Info screen is displayed.

### Post-Condition(s)

POST-1: The client displays the returned address cards.

### Basic Flow

1. The customer opens the Address section.
2. The client requests the address book.
3. The system returns saved addresses and their displayed badges.
4. The client displays the address cards.

### Alternative Flow

AF-1: Open Add Address

4a: The customer chooses Add New in the address section.

4b: The client opens Add Address.

### Exception Flow

EF-1: Sign in to view addresses

3a: The system returns a rejected authentication context.

3b: The client presents the sign-in entry point.

### Related UI

- [Figma node 275:1168](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=275-1168)

### Related API IDs

- [API-ADDRESSES](../api/API-ADDRESSES.md)

### Notes

Screen and text-layer evidence establishes the visible goal. Service decomposition, request shapes, and exception recovery are proposed implementation contracts; they are not extracted server behavior. See [assumptions](../../ASSUMPTIONS.md) and [coverage](../../coverage-report.md) for the supported boundary. No prototype interaction wiring was available for verification.

## UML Model

~~~plantuml
@startuml
hide empty members

class ProfileService {
  +addresses(ctx: RequestContext): AddressBook
}

class Address {
  id: String
  customerId: String
  details: AddressFields
  defaultShipping: Boolean
  defaultBilling: Boolean
}

class AddressBook {
  customerId: String
  version: Integer
  items: Sequence(Address)
}

class AddressFields <<value>> {
  firstName: String
  lastName: String
  country: String
  company: String [0..1]
  street: String
  unit: String [0..1]
  city: String
  state: String
  postalCode: String
  phone: String
  instructions: String [0..1]
}

class RequestContext <<input>> {
  customerId: String
  authenticated: Boolean
}

AddressBook "1" *-- "0..*" Address
Address --> "1" AddressFields : details

@enduml
~~~

## Business Rules

~~~text
BR-ADDRESS-BOOK-01 - Account Context
Source: Assumption
context ProfileService::addresses(ctx: RequestContext): AddressBook
pre BR_ADDRESS_BOOK_01_AccountContext:
  ctx.authenticated
~~~
~~~text
BR-ADDRESS-BOOK-02 - Book Reference
Source: Assumption
context ProfileService::addresses(ctx: RequestContext): AddressBook
pre BR_ADDRESS_BOOK_02_BookReference:
  AddressBook.allInstances()->exists(b | b.customerId = ctx.customerId)
~~~
~~~text
BR-ADDRESS-BOOK-03 - Book Identity
Source: Assumption
context ProfileService::addresses(ctx: RequestContext): AddressBook
post BR_ADDRESS_BOOK_03_BookIdentity:
  result.customerId = ctx.customerId
~~~
~~~text
BR-ADDRESS-BOOK-04 - Address Entries
Source: Assumption
context ProfileService::addresses(ctx: RequestContext): AddressBook
post BR_ADDRESS_BOOK_04_AddressEntries:
  result.items = Address.allInstances()->select(a | a.customerId = ctx.customerId)->sortedBy(a | a.id)
~~~
~~~text
BR-ADDRESS-BOOK-05 - Single Shipping Default
Source: Assumption
context AddressBook
inv BR_ADDRESS_BOOK_05_SingleShippingDefault:
  self.items->select(a | a.defaultShipping)->size() <= 1
~~~
~~~text
BR-ADDRESS-BOOK-06 - Single Billing Default
Source: Assumption
context AddressBook
inv BR_ADDRESS_BOOK_06_SingleBillingDefault:
  self.items->select(a | a.defaultBilling)->size() <= 1
~~~
~~~text
BR-ADDRESS-BOOK-07 - Book Unchanged
Source: Assumption
context ProfileService::addresses(ctx: RequestContext): AddressBook
post BR_ADDRESS_BOOK_07_BookUnchanged:
  AddressBook.allInstances()->forAll(b | b.version = b.version@pre and b.items = b.items@pre) and Address.allInstances()->forAll(a | a.defaultShipping = a.defaultShipping@pre and a.defaultBilling = a.defaultBilling@pre and a.details = a.details@pre)
~~~
