---
artifact_type: ocl-utility-definitions
status: Frozen
---

# OCL Utility Definitions

```text
String.trim(): String
- Removes leading and trailing whitespace; internal whitespace is unchanged.

String.toLower(): String
- Applies locale-independent Unicode lowercase for case-insensitive comparison; whitespace is preserved.

DateTime::hoursBetween(start: DateTime, end: DateTime): Real
- Returns (end - start) in elapsed UTC seconds divided by 3600, retaining fractional hours; local clock changes do not change elapsed duration.

BusinessCalendar::today(timeZone: String): Date
- Converts the captured request-start instant to its Gregorian calendar date in the supplied IANA timezone.

BusinessCalendar::nights(start: Date, end: Date): Integer
- Returns the signed difference in Gregorian calendar-day ordinals, independent of daylight-saving clock changes.

BusinessClock::now(timeZone: String): DateTime
- Returns the captured request-start instant, represented in the supplied IANA timezone; repeated calls during the request denote the same instant.

BusinessClock::hoursBetween(start: DateTime, end: DateTime): Real
- Returns (end - start) in elapsed UTC seconds divided by 3600, retaining fractional hours.

IdentityNormalization::canonicalEmail(value: String): String
- Trims surrounding Unicode whitespace, applies Unicode NFC, and lowercases using locale-independent Unicode rules.
- Internal whitespace and dots remain unchanged; provider-specific alias rewriting is not applied.

Validation::isEmail(value: String): Boolean
- True for a trimmed ASCII dot-atom address with one @, a local part of at most 64 characters, and a dotted domain of nonempty labels.
- The full address is at most 254 characters; whitespace, quoted local parts, consecutive dots, leading/trailing dots, and domain labels with leading/trailing hyphens are rejected.

Validation::isPhone(value: String): Boolean
- True for a trimmed international phone string beginning with + followed by 1-15 ASCII digits, with a nonzero first digit and no separators.

Validation::isCountryCode(value: String): Boolean
- True for a trimmed two-letter uppercase ASCII country code present in the provider adapter's supported-country catalog; unsupported or unknown values return false.

CredentialPolicy::accepts(password: String, email: String, fullName: String): Boolean
- True for an unchanged password of 12-128 Unicode code points, with no control characters and no leading/trailing whitespace.
- Its locale-independent lowercase value must differ from the canonical email and trimmed/lowercased full name; the password itself is never normalized or truncated.

PasswordHasher::matches(password: String, hash: String): Boolean
- Verifies the unchanged plaintext against a self-describing Argon2id hash using the stored salt and parameters.
- Newly generated hashes use a fresh 16-byte salt, 65536 KiB memory, 3 iterations, parallelism 1, and a 32-byte output; malformed hashes return false.

TokenHasher::hash(value: String): String
- Returns HMAC-SHA-256 of the exact token bytes under an external session-token key; plaintext tokens are not persisted.

RequestFingerprint::of(command: StayBookingCommand): String
- Returns SHA-256 of versioned UTF-8 canonical JSON over the immutable stay-booking command fields, excluding idempotencyKey and the supplied requestFingerprint.
- Keys are sorted; nulls are explicit, decimal amounts are exact strings, and timestamps use UTC milliseconds.

RequestFingerprint::ofTaxi(command: TaxiBookingCommand): String
- Applies the same encoding and exclusions to the immutable taxi-booking command fields, with a distinct taxi-booking type/version prefix.

PaymentFingerprint::of(value: String): String
- Returns HMAC-SHA-256 of the exact payment-token bytes under an external key distinct from the session-token key; the raw payment token is not persisted.

AllocationCalendar::isFree(driverId: String, vehicleId: String, start: DateTime, end: DateTime): Boolean
- True when start < end and neither driver nor vehicle has an active allocation overlapping the half-open interval [start, end).
- Adjacent intervals are compatible; the check runs in the resource-locking transaction described by the BRs.

RentalFilter::depositMatches(bands: DepositBand[*], amount: Money): Boolean
- True for an empty selection, or when the LKR deposit lies in any selected band.
- Bands use [200,500), [500,1000), [1000,1200), and [1200,1500] respectively; the final upper endpoint is inclusive.

RentalFilter::electricMatches(types: ElectricType[*], value: ElectricType): Boolean
- True for an empty selection, or when value equals at least one selected type; selected alternatives are combined with OR.

SearchSnapshot::refinementChanged(criteria: StaySearchCriteria): Boolean
- Compares minPrice, maxPrice, minRating, and sort with the accepted traversal's refinements; true when any value changes.
- Initial searches have no previous refinement and return false; limit, offset, searchContextId, and snapshotVersion do not count as refinements.

SearchSnapshot::refinementChanged(criteria: TaxiSearchCriteria): Boolean
- Compares minPrice, maxPrice, sort, vehicleCategories, depositBands, and electricTypes with the accepted traversal's refinements.
- List filters compare as sets, so reordering selected alternatives does not restart traversal. Initial searches return false.

SearchSnapshot::refinementChanged(criteria: FlightSearchCriteria): Boolean
- Compares minPrice, maxPrice, maxDurationMinutes, providerIds, and sort with the accepted traversal's refinements.
- providerIds compares as a set; initial searches return false. Pagination size/offset and context identity/version are excluded.

SearchSnapshot::accepts(criteria: StaySearchCriteria, at: DateTime): Boolean
- True for an initial search with neither context field, or a stay-search snapshot bound to the requester, exact supplied ID/version, and an expiry strictly later than at.

SearchSnapshot::accepts(criteria: TaxiSearchCriteria, at: DateTime): Boolean
- Applies the same requester, ID/version, and expiry checks to a taxi-search snapshot; incomplete context pairs return false.

SearchSnapshot::accepts(criteria: FlightSearchCriteria, at: DateTime): Boolean
- Applies the same requester, ID/version, and expiry checks to a flight-search snapshot; incomplete context pairs return false.

FlightCalendar::localDate(value: DateTime, timeZone: String): Date
- Converts a flight instant to its Gregorian local date in the supplied IANA timezone. Invalid timezone identifiers produce an invalid result.

FlightItinerary::connects(segments: FlightSegment[*], originId: String, destinationId: String): Boolean
- True for a nonempty ordered chain whose provider-resolved first origin and last destination match the requested endpoints and whose adjacent segments share a transfer location.
- Missing endpoint metadata or a broken chain returns false; this check does not reserve provider inventory.

FlightItinerary::hasValidConnections(segments: FlightSegment[*], minMinutes: Integer, maxMinutes: Integer): Boolean
- True when every adjacent transfer interval in elapsed minutes is within the inclusive supplied bounds.
- Empty and single-segment sequences have no transfer interval and return true; malformed chronology returns false.

FlightItinerary::duration(segments: FlightSegment[*]): Integer
- Returns zero for an empty journey; otherwise returns floor((last arrival - first departure) in elapsed seconds / 60).
- It includes transfer time within that journey and excludes a stay between outbound and inbound journeys.

FlightNormalization::signature(outbound: FlightSegment[*], inbound: FlightSegment[*]): String
- Returns SHA-256 of versioned canonical JSON containing the ordered outbound and inbound segment values with UTC-millisecond departure/arrival timestamps.
- Provider identity and fare identity remain separate parts of the BR deduplication key; outbound and inbound boundaries are explicit.

PrivacyMask::personName(value: String): String
- Returns the first Unicode grapheme of the trimmed name followed by ***; an empty name becomes Traveller.
- The full private name is never copied into the public projection.

ContentSafety::isPublicSafe(value: String): Boolean
- True when text contains no HTML markup, private email/phone contact values, or control characters other than tab/newline, and any URL uses https.
- This deterministic text-safety check does not grant publication; approval and visibility remain separate BR conditions.

ProviderInventory::reservations(): String
- Canonically serializes provider reservation identities and persisted properties, ordered by stable identity within the operation's isolated view. Equality before and after a read asserts no reservation effect.

ReadState::users(): String
- Returns the canonical persisted user-state snapshot within the operation's isolated view.

ReadState::sessions(): String
- Returns the canonical persisted session-state snapshot, excluding raw access tokens.

ReadState::stays(): String
- Returns the canonical persisted stay/catalog-state snapshot.

ReadState::stayBookings(): String
- Returns the canonical persisted stay-booking-state snapshot.

ReadState::taxiBookings(): String
- Returns the canonical persisted taxi-booking/allocation-state snapshot.

ReadState::payments(): String
- Returns the canonical persisted payment-reference-state snapshot, excluding raw payment tokens.

ReadState::editorial(): String
- Returns the canonical persisted editorial destination/trip/attraction-state snapshot.

ReadState::reviews(): String
- Returns the canonical persisted review-state snapshot, including publication and approval fields.
```

Time comparisons use instants; Gregorian dates use the explicitly supplied IANA timezone. All request clocks refer to the same captured start instant. Snapshots compare sorted identities and property values in the operation's isolated view, so unrelated concurrent commits are not attributed to the operation. They exclude transient plaintext credentials.

Service operations used as OCL contexts and standard OCL operations are outside this utility catalog. The three search-criteria overloads are local to their use cases; they do not define one shared search-criteria type. Each helper declaration remains repeated in the relevant local UML; external provider metadata belongs to the existing provider adapter boundary.

## Utility Classes

```text
class String <<Primitive>> {
  +trim(): String
  +toLower(): String
}

class DateTime <<Primitive>> {
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

class PasswordHasher <<Utility>> {
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
