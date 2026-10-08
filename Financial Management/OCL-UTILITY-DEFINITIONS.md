---
artifact_type: ocl-utility-definitions
status: Frozen
---

# OCL Utility Definitions

```text
Text::trim(s: String): String
- Removes leading and trailing Unicode whitespace; internal whitespace is unchanged.

Text::nfc(s: String): String
- Returns Unicode NFC-normalized text.

Text::lower(s: String): String
- Applies locale-independent Unicode lowercase without changing whitespace.

Text::matches(s: String, pattern: String): Boolean
- Performs a full regular-expression match; callers use .* to match surrounding text.

Text::email(s: String): Boolean
- True for an ASCII dot-atom email address with one @, a local part of at most 64 characters, and a dotted domain of nonempty labels.
- The full address is at most 254 characters; whitespace, quoted local parts, consecutive dots, leading/trailing dots, and domain labels with leading/trailing hyphens are rejected.

Text::last4(s: String): String
- Returns the final four characters of an already accepted account-number digit string.

Text::username(email: String, taken: Set(String)): String
- Starts with the normalized email prefix before @; if occupied, appends the first unused positive integer suffix.
- Database uniqueness resolves concurrent collisions; registration retries username generation within its transaction.

Numeric::finite(x: Real): Boolean
- True when x is a finite numeric value; NaN and positive/negative infinity are rejected.

Numeric::scale(x: Real): Integer
- Counts significant fractional decimal digits after removing insignificant trailing zeros.

Numeric::round2(x: Real): Real
- Uses exact decimal HALF_UP rounding to two fractional places.

CalendarDate::monthStart(date: CalendarDate): CalendarDate
- Returns the first Gregorian calendar date of the argument's month.

CalendarDate::monthEnd(date: CalendarDate): CalendarDate
- Returns the last Gregorian calendar date of the argument's month, including leap-year handling.

CalendarDate::previousMonth(date: CalendarDate): CalendarDate
- Returns the first date of the immediately preceding month, including the January-to-December year boundary.

PasswordHasher::matches(password: String, hash: String): Boolean
- Verifies the plaintext password against the stored bcrypt hash and its encoded salt/work factor; it never returns a hash or plaintext.

PasswordHasher::cost(hash: String): Integer
- Returns the bcrypt work factor encoded in a valid stored hash.

AccountVault::decrypt(ciphertext: String): String
- Authenticates and decrypts account-number ciphertext using an external key, preserving the original digit sequence and leading zeros.
- Authentication failure produces an operation error rather than unverified plaintext.

AccountVault::fingerprint(number: String): String
- Returns keyed HMAC-SHA-256 of the exact account-number digit sequence under an external key.
- The key is separate from the encryption key; neither key is stored in database columns.
```

Real denotes exact decimal arithmetic; an empty sum is zero. Monetary bounds and rejection of extra significant fractional digits remain in the BRs, before database conversion. CalendarDate is a Gregorian date value with year, month, and ordinal; ordinal counts calendar-day boundaries from 1970-01-01. The request context captures today once in Asia/Saigon and persists creation timestamps as RFC 3339 UTC instants.

Snapshot frame conditions compare every persisted property by value within the operation's isolated transaction view. They do not rely on persistent object identity and do not attribute unrelated concurrent commits to the operation. Read postconditions describe successful returns; protocol errors are exceptional completions. Mutation services additionally describe explicit unsuccessful results and rollback.

Each helper declaration is repeated in the relevant use case's local UML. This catalog documents those declarations; it supplies no missing local vocabulary. Service operations such as AuthService::register and AccountService::update are BR contexts rather than utility helpers. Wire date parsing accepts valid YYYY-MM-DD Gregorian dates and is not modeled as an additional helper operation.

## Utility Classes

```text
class Text <<Utility>> {
  +trim(s: String): String
  +nfc(s: String): String
  +lower(s: String): String
  +matches(s: String, pattern: String): Boolean
  +email(s: String): Boolean
  +last4(s: String): String
  +username(email: String, taken: Set(String)): String
}

class Numeric <<Utility>> {
  +finite(x: Real): Boolean
  +scale(x: Real): Integer
  +round2(x: Real): Real
}

class CalendarDate <<Primitive>> {
  +year: Integer
  +month: Integer
  +ordinal: Integer
  +monthStart(date: CalendarDate): CalendarDate
  +monthEnd(date: CalendarDate): CalendarDate
  +previousMonth(date: CalendarDate): CalendarDate
}

class PasswordHasher <<Utility>> {
  +matches(password: String, hash: String): Boolean
  +cost(hash: String): Integer
}

class AccountVault <<Utility>> {
  +decrypt(ciphertext: String): String
  +fingerprint(number: String): String
}
```
