---
artifact_type: ocl-utility-definitions
status: Frozen
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A2:B2"
retrieved_at: 2026-09-28T15:29:00Z
---

# OCL Utility Definitions

> The spreadsheet row supplies the `trim` and password-match conventions and this document format. The remaining signatures and BR-limited meanings are taken from `01-inception/uc/`. The source row does not define this project's domain helpers.

```text
String.trim(): String
- Removes leading and trailing whitespace; internal whitespace is unchanged.

Date::today(): Date
- Returns the current calendar date used to reject past booking/search dates. The BRs do not specify a timezone.

DateTime::now(): DateTime
- Returns the current instant used for challenge expiry and event timestamps.

Email::normalize(value: String): String
- Returns the canonical email value used for account lookup, storage, and contact records. The exact normalization sequence is unspecified.

PasswordHash::of(value: String): String
- Returns a stored password hash; plaintext must differ from the stored value.

PasswordHash::matches(value: String, storedHash: String): Boolean
- True when the supplied plaintext password verifies against the stored hash.

CodeHash::matches(value: String, storedHash: String): Boolean
- True when the supplied verification code verifies against the stored challenge hash.

TokenHash::of(value: String): String
- Returns a stored access-token hash; the stored value differs from the plaintext token.

PhoneCipher::matches(ciphertext: String, value: String): Boolean
- True when an encrypted contact-phone value represents the supplied phone number.

RequestFingerprint::of(command: CreateBookingCommand): String
- Returns the fingerprint used to compare a create-booking request with a previously accepted idempotency key.
- The canonical input encoding and digest algorithm are unspecified.

TimeUtils::matchesSlotTime(startsAt: DateTime, localTime: String, timezone: String): Boolean
- True when the slot start corresponds to the requested local time in the restaurant timezone.

SequenceUtils::isAscendingByStartTime(items: Sequence(ReservationSlot)): Boolean
- True when slot start times are in ascending order. Tie handling is unspecified.

SequenceUtils::isDescendingByCreatedAt(items: Sequence(Booking)): Boolean
SequenceUtils::isDescendingByCreatedAt(items: Sequence(Notification)): Boolean
- True when creation times are in descending order. Tie handling is unspecified.

GeoTimeZone::forAddress(address: String): String
- Returns the timezone associated with a restaurant address. Address resolution and ambiguous-address policy are unspecified.
```

Service operations that form OCL contexts are outside this catalog. The BRs do not call the UML-declared `CodeHash::of` or `PhoneCipher::encrypt`, so they are not cataloged as used utilities.

## Utility Classes

```text
class String <<Primitive>> {
  +trim(): String
}

class Date <<Primitive>> {
  +today(): Date
}

class DateTime <<Primitive>> {
  +now(): DateTime
}

class Email <<Utility>> {
  +normalize(value: String): String
}

class PasswordHash <<Utility>> {
  +of(value: String): String
  +matches(value: String, storedHash: String): Boolean
}

class CodeHash <<Utility>> {
  +matches(value: String, storedHash: String): Boolean
}

class TokenHash <<Utility>> {
  +of(value: String): String
}

class PhoneCipher <<Utility>> {
  +matches(ciphertext: String, value: String): Boolean
}

class RequestFingerprint <<Utility>> {
  +of(command: CreateBookingCommand): String
}

class TimeUtils <<Utility>> {
  +matchesSlotTime(startsAt: DateTime, localTime: String, timezone: String): Boolean
}

class SequenceUtils <<Utility>> {
  +isAscendingByStartTime(items: Sequence(ReservationSlot)): Boolean
  +isDescendingByCreatedAt(items: Sequence(Booking)): Boolean
  +isDescendingByCreatedAt(items: Sequence(Notification)): Boolean
}

class GeoTimeZone <<Utility>> {
  +forAddress(address: String): String
}

```
