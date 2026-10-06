---
artifact_type: ocl-utility-definitions
status: Frozen
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A2:B2"
retrieved_at: 2026-09-28T15:29:00Z
---

# OCL Utility Definitions

> The spreadsheet row is the format reference; the project-specific signatures and constraints below come from `01-inception/uc/` Business Rules. The source row does not define these project-specific helpers. Unspecified implementation details remain unspecified.

```text
TextSyntax::email(value: String): Boolean
- Tests email syntax before a password-reset request. The BRs do not fix a particular email grammar.

TextSyntax::canonicalEmail(value: String): String
- Returns the canonical email value used for customer identity comparison and storage.
- The BRs do not specify the exact normalization sequence.

TextSyntax::nonBlank(value: String): Boolean
- True when a string has a non-whitespace value; used for address fields and a delivery reference.

AddressValidation::valid(input: AddressFields): Boolean
- True exactly when firstName, lastName, country, street, city, state, postalCode, and phone each satisfy TextSyntax::nonBlank, per BR-UC-13-07.

Clock::now(): Integer
- Returns the current time value used for session expiry and creation timestamps.
- Epoch, unit, and clock precision are not defined by the BRs.

Digest::checkout(input: CheckoutInput, displayedTotal: Money): String
- Produces the request digest compared with or stored on a CheckoutReceipt for idempotent checkout.
- Canonical encoding and digest algorithm are not defined by the BRs.
```

The service operations used as OCL contexts, including `CheckoutService::place`, are specified by their BRs and are outside this utility catalog. Standard OCL operations are also outside it.

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
