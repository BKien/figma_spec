---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-13
uc_name: "Add a delivery address"
---

# UC-13: Add a delivery address

## Functional Use-Case Specification

### Use Case ID

UC-13

### Use Case Name

Add a delivery address

### Description

Enter a new address and optional default-address selections, then return to the address book.

### Actor(s)

Primary: Customer. Supporting: web client and application service.

### Priority

Medium.

### Trigger

The customer chooses Add New in My Info.

### Pre-Condition(s)

PRE-1: The Add Address form is displayed.

### Post-Condition(s)

POST-1: The client displays the returned address book.

### Basic Flow

1. The customer enters the address fields and delivery instructions.
2. The customer chooses the default shipping and default billing checkboxes as desired.
3. The customer chooses Save.
4. The client submits the address form.
5. The system returns the saved address book.
6. The client displays the address cards.

### Alternative Flow

AF-1: Cancel adding an address

3a: The customer chooses Cancel.

3b: The client returns to My Info.

### Exception Flow

EF-1: Review the refreshed address book

5a: The system returns an operation conflict.

5b: The client refreshes the address book.

5c: The client asks the customer to review and submit the form again.

### Related UI

- [Figma node 279:1003](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=279-1003)
- [Figma node 275:1168](https://www.figma.com/design/WcpUgAYaQJA4J00rMaMgj8/Euphoria?node-id=275-1168)

### Related API IDs

- [API-ADDRESSES](../api/API-ADDRESSES.md)
- [API-ADDRESS-CREATE](../api/API-ADDRESS-CREATE.md)

### Notes

Screen and text-layer evidence establishes the visible goal. Service decomposition, request shapes, and exception recovery are proposed implementation contracts; they are not extracted server behavior. See [assumptions](../../ASSUMPTIONS.md) and [coverage](../../coverage-report.md) for the supported boundary. No prototype interaction wiring was available for verification.

## UML Model

~~~plantuml
@startuml
hide empty members

class AddressService {
  +add(ctx: RequestContext, book: AddressBook, input: AddressFields, shipping: Boolean, billing: Boolean, expectedVersion: Integer): AddressBook
}

class Address {
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

class AddressValidation <<primitive helper>> {
  {static} +valid(input: AddressFields): Boolean
}

class RequestContext <<input>> {
  customerId: String
  authenticated: Boolean
  csrfValid: Boolean
}

class TextSyntax <<primitive helper>> {
  {static} +nonBlank(value: String): Boolean
}

AddressBook "1" *-- "0..*" Address
Address --> "1" AddressFields : details

@enduml
~~~

## Business Rules

~~~text
BR-ADD-ADDRESS-01 - Account Book
Source: Assumption
context AddressService::add(ctx: RequestContext, book: AddressBook, input: AddressFields, shipping: Boolean, billing: Boolean, expectedVersion: Integer): AddressBook
pre BR_ADD_ADDRESS_01_AccountBook:
  ctx.authenticated and ctx.csrfValid and book.customerId = ctx.customerId
~~~
~~~text
BR-ADD-ADDRESS-02 - Expected Revision
Source: Assumption
context AddressService::add(ctx: RequestContext, book: AddressBook, input: AddressFields, shipping: Boolean, billing: Boolean, expectedVersion: Integer): AddressBook
pre BR_ADD_ADDRESS_02_ExpectedRevision:
  expectedVersion = book.version
~~~
~~~text
BR-ADD-ADDRESS-03 - Address Accepted
Source: Assumption
context AddressService::add(ctx: RequestContext, book: AddressBook, input: AddressFields, shipping: Boolean, billing: Boolean, expectedVersion: Integer): AddressBook
pre BR_ADD_ADDRESS_03_AddressAccepted:
  AddressValidation::valid(input)
~~~
~~~text
BR-ADD-ADDRESS-04 - Address Created
Source: Assumption
context AddressService::add(ctx: RequestContext, book: AddressBook, input: AddressFields, shipping: Boolean, billing: Boolean, expectedVersion: Integer): AddressBook
post BR_ADD_ADDRESS_04_AddressCreated:
  result = book and result.version = expectedVersion + 1 and result.items->size() = book.items@pre->size() + 1 and result.items->one(a | a.oclIsNew() and a.customerId = ctx.customerId and a.details = input and a.defaultShipping = shipping and a.defaultBilling = billing)
~~~
~~~text
BR-ADD-ADDRESS-05 - Preserve Entries
Source: Assumption
context AddressService::add(ctx: RequestContext, book: AddressBook, input: AddressFields, shipping: Boolean, billing: Boolean, expectedVersion: Integer): AddressBook
post BR_ADD_ADDRESS_05_PreserveEntries:
  book.items@pre->forAll(a | result.items->includes(a) and a.details = a.details@pre and a.defaultShipping = (if shipping then false else a.defaultShipping@pre endif) and a.defaultBilling = (if billing then false else a.defaultBilling@pre endif))
~~~
~~~text
BR-ADD-ADDRESS-06 - Customer Addresses
Source: Assumption
context AddressBook
inv BR_ADD_ADDRESS_06_CustomerAddresses:
  self.items->forAll(a | a.customerId = self.customerId)
~~~
~~~text
BR-ADD-ADDRESS-07 - Required Address Values
Source: Assumption
context AddressValidation::valid(input: AddressFields): Boolean
post BR_ADD_ADDRESS_07_RequiredAddressValues:
  result = (TextSyntax::nonBlank(input.firstName) and TextSyntax::nonBlank(input.lastName) and TextSyntax::nonBlank(input.country) and TextSyntax::nonBlank(input.street) and TextSyntax::nonBlank(input.city) and TextSyntax::nonBlank(input.state) and TextSyntax::nonBlank(input.postalCode) and TextSyntax::nonBlank(input.phone))
~~~
