---
artifact_type: ocl-utility-definitions
status: Frozen
---

# OCL Utility Definitions

```text
TextSyntax::email(value: String): Boolean
- True for a trimmed ASCII dot-atom address with one @, a local part of at most 64 characters, and a dotted domain of nonempty labels.
- The full address is at most 254 characters; whitespace, quoted local parts, consecutive dots, leading/trailing dots, and domain labels with leading/trailing hyphens are rejected.

TextSyntax::canonicalEmail(value: String): String
- Returns the canonical email value used for customer identity comparison and storage.
- Removes leading and trailing Unicode whitespace, applies Unicode NFC, and lowercases using locale-independent Unicode rules. Internal whitespace and dots are preserved; provider-specific alias rewriting is not applied.

TextSyntax::nonBlank(value: String): Boolean
- True when a string has a non-whitespace value; used for address fields and a delivery reference.

AddressValidation::valid(input: AddressFields): Boolean
- True exactly when firstName, lastName, country, street, city, state, postalCode, and phone each satisfy TextSyntax::nonBlank. Optional instructions do not affect this test.

Clock::now(): Integer
- Returns the server transaction-clock instant as integer milliseconds since 1970-01-01T00:00:00Z.
- The value is captured once per operation for session expiry, reset-delivery creation, and order events; repeated calls in that operation return the same value.

Digest::checkout(input: CheckoutInput, displayedTotal: Money): String
- Produces the request digest compared with or stored on a CheckoutReceipt for idempotent checkout.
- Uses SHA-256 over versioned UTF-8 canonical JSON containing customer/cart identity, the submitted cartVersion, billing and shipping fields, sameAsBilling, and displayedTotal amount/currency.
- Canonical values use sorted object keys, explicit nulls, exact decimal strings, and the immutable request snapshot; later cart consumption cannot change the digest. Mutable cart membership is excluded so an identical checkout can replay after the cart is emptied.
```

The service operations used as OCL contexts, including CheckoutService::place, are specified by their BRs and are outside this utility catalog. Standard OCL operations are also outside it.

## Utility Classes

```text
class TextSyntax <<Utility>> {
  +email(value: String): Boolean
  +canonicalEmail(value: String): String
  +nonBlank(value: String): Boolean
}

class AddressValidation <<Utility>> {
  +valid(input: AddressFields): Boolean
}

class Clock <<Utility>> {
  +now(): Integer
}

class Digest <<Utility>> {
  +checkout(input: CheckoutInput, displayedTotal: Money): String
}

```
