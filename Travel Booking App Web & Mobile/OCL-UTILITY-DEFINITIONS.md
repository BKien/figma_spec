---
artifact_type: ocl-utility-definitions
status: Frozen
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A2:B2"
retrieved_at: 2026-09-28T15:29:00Z
---

# OCL Utility Definitions

> The spreadsheet row supplies the `trim` and password-match conventions and this document format. The project-specific signatures and BR-limited meanings below come from `01-inception/uc/`. The source row does not define these travel helpers; unspecified algorithms and thresholds are not invented here.

```text
String.trim(): String
- Removes leading and trailing whitespace; internal whitespace is unchanged.

String.toLower(): String
- Returns a lowercase representation for case-insensitive comparison. Locale behavior is unspecified.

DateTime::now(): DateTime
- Returns the current instant used by time comparisons.

DateTime::hoursBetween(start: DateTime, end: DateTime): Real
- Returns elapsed hours from start to end.

BusinessCalendar::today(timeZone: String): Date
- Returns today's local calendar date in the supplied timezone.

BusinessCalendar::nights(start: Date, end: Date): Integer
- Returns the number of calendar nights between check-in and check-out dates.

BusinessClock::now(timeZone: String): DateTime
- Returns the current time represented for the supplied timezone.

BusinessClock::hoursBetween(start: DateTime, end: DateTime): Real
- Returns elapsed hours between the two instants.

IdentityNormalization::canonicalEmail(value: String): String
- Returns the canonical email used for uniqueness, lookup, and storage. The exact normalization sequence is unspecified.

Validation::isEmail(value: String): Boolean
Validation::isPhone(value: String): Boolean
Validation::isCountryCode(value: String): Boolean
- Return whether the respective contact value is valid. The BRs do not fix their complete grammars.

CredentialPolicy::accepts(password: String, email: String, fullName: String): Boolean
- Tests whether a password satisfies the credential policy relative to canonical email and trimmed full name. Exact policy thresholds are unspecified.

PasswordHasher::matches(password: String, hash: String): Boolean
- True when a plaintext password verifies against the stored hash; plaintext is never the stored hash.

TokenHasher::hash(value: String): String
- Produces the stored token hash, which must differ from the issued plaintext token.

RequestFingerprint::of(command: StayBookingCommand): String
RequestFingerprint::ofTaxi(command: TaxiBookingCommand): String
- Produce server-derived request fingerprints used to match idempotent booking intent. Encoding and digest algorithm are unspecified.

PaymentFingerprint::of(value: String): String
- Produces the derived payment-token reference; the reference differs from the plaintext token.

AllocationCalendar::isFree(driverId: String, vehicleId: String, start: DateTime, end: DateTime): Boolean
- True when driver and vehicle can be allocated for the requested interval.

RentalFilter::depositMatches(bands: DepositBand[*], amount: Money): Boolean
- Tests whether an offer deposit meets the selected deposit bands. Empty-selection behavior is unspecified.

RentalFilter::electricMatches(types: ElectricType[*], value: ElectricType): Boolean
- Tests whether a vehicle electric type meets the selected types. Empty-selection behavior is unspecified.

SearchSnapshot::refinementChanged(criteria: StaySearchCriteria): Boolean
SearchSnapshot::refinementChanged(criteria: TaxiSearchCriteria): Boolean
SearchSnapshot::refinementChanged(criteria: FlightSearchCriteria): Boolean
- True when a search refinement changes and pagination must restart at offset zero. The exact comparison fields depend on the concrete criteria type.

SearchSnapshot::accepts(criteria: StaySearchCriteria, at: DateTime): Boolean
SearchSnapshot::accepts(criteria: TaxiSearchCriteria, at: DateTime): Boolean
SearchSnapshot::accepts(criteria: FlightSearchCriteria, at: DateTime): Boolean
- Tests whether the supplied search-context id and snapshot version are acceptable at request start. Expiry and version policy remain in the BRs.

FlightCalendar::localDate(value: DateTime, timeZone: String): Date
- Converts a flight instant to its local calendar date in the supplied timezone.

FlightItinerary::connects(segments: FlightSegment[*], originId: String, destinationId: String): Boolean
- True when the segment chain connects the requested endpoints.

FlightItinerary::hasValidConnections(segments: FlightSegment[*], minMinutes: Integer, maxMinutes: Integer): Boolean
- True when each transfer interval meets the supplied minute bounds.

FlightItinerary::duration(segments: FlightSegment[*]): Integer
- Returns the journey duration in minutes for the segment chain.

FlightNormalization::signature(outbound: FlightSegment[*], inbound: FlightSegment[*]): String
- Produces the provider-normalized itinerary identity used for deduplication. Encoding is unspecified.

PrivacyMask::personName(value: String): String
- Returns the public author-name projection without exposing the full private identity. Masking format is unspecified.

ContentSafety::isPublicSafe(value: String): Boolean
- True when public review/comment text passes the content-safety projection. Exact moderation policy is unspecified.

ProviderInventory::reservations(): String
- Returns a comparable snapshot of provider reservations; equality before and after a read proves no reservation effect.

ReadState::{users|sessions|stays|stayBookings|taxiBookings|payments|editorial|reviews}(): String
- Each operation returns a comparable snapshot of the named state domain. Equality with its `@pre` value asserts no change to that domain.
```

Service operations used as OCL contexts and standard OCL operations are outside this utility catalog. The three search-criteria overloads are local to their use cases; the BRs do not define one shared search-criteria type.

## Utility Classes

```text
class String <<Primitive>> {
  +trim(): String
  +toLower(): String
}

class DateTime <<Primitive>> {
  +now(): DateTime
  +hoursBetween(start: DateTime, end: DateTime): Real
}

class BusinessCalendar <<Utility>> {
  +today(timeZone: String): Date
  +nights(start: Date, end: Date): Integer
}

class BusinessClock <<Utility>> {
  +now(timeZone: String): DateTime
  +hoursBetween(start: DateTime, end: DateTime): Real
}

class IdentityNormalization <<Utility>> {
  +canonicalEmail(value: String): String
}

class Validation <<Utility>> {
  +isEmail(value: String): Boolean
  +isPhone(value: String): Boolean
  +isCountryCode(value: String): Boolean
}

class CredentialPolicy <<Utility>> {
  +accepts(password: String, email: String, fullName: String): Boolean
}

class PasswordHasher <<Service>> {
  +matches(password: String, hash: String): Boolean
}

class TokenHasher <<Utility>> {
  +hash(value: String): String
}

class RequestFingerprint <<Utility>> {
  +of(command: StayBookingCommand): String
  +ofTaxi(command: TaxiBookingCommand): String
}

class PaymentFingerprint <<Utility>> {
  +of(value: String): String
}

class AllocationCalendar <<Utility>> {
  +isFree(driverId: String, vehicleId: String, start: DateTime, end: DateTime): Boolean
}

class RentalFilter <<Utility>> {
  +depositMatches(bands: DepositBand[*], amount: Money): Boolean
  +electricMatches(types: ElectricType[*], value: ElectricType): Boolean
}

class SearchSnapshot <<Utility>> {
  +refinementChanged(criteria: StaySearchCriteria): Boolean
  +refinementChanged(criteria: TaxiSearchCriteria): Boolean
  +refinementChanged(criteria: FlightSearchCriteria): Boolean
  +accepts(criteria: StaySearchCriteria, at: DateTime): Boolean
  +accepts(criteria: TaxiSearchCriteria, at: DateTime): Boolean
  +accepts(criteria: FlightSearchCriteria, at: DateTime): Boolean
}

class FlightCalendar <<Utility>> {
  +localDate(value: DateTime, timeZone: String): Date
}

class FlightItinerary <<Utility>> {
  +connects(segments: FlightSegment[*], originId: String, destinationId: String): Boolean
  +hasValidConnections(segments: FlightSegment[*], minMinutes: Integer, maxMinutes: Integer): Boolean
  +duration(segments: FlightSegment[*]): Integer
}

class FlightNormalization <<Utility>> {
  +signature(outbound: FlightSegment[*], inbound: FlightSegment[*]): String
}

class PrivacyMask <<Utility>> {
  +personName(value: String): String
}

class ContentSafety <<Utility>> {
  +isPublicSafe(value: String): Boolean
}

class ProviderInventory <<Utility>> {
  +reservations(): String
}

class ReadState <<Utility>> {
  +users(): String
  +sessions(): String
  +stays(): String
  +stayBookings(): String
  +taxiBookings(): String
  +payments(): String
  +editorial(): String
  +reviews(): String
}

```
