---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-15
uc_name: "Manage Cookie Consent"
---

# UC-15: Manage Cookie Consent

## Functional Use-Case Specification

### Use Case ID

UC-15

### Use Case Name

Manage Cookie Consent

### Description

As a visitor, I want to choose which optional cookie categories Tripma may use so that my preference is remembered on the local application.

### Actor(s)

Visitor

### Priority

Low

### Trigger

Tripma cannot find a current cookie-consent decision, or the visitor opens cookie settings.

### Pre-Condition(s)

PRE-1: The Tripma application is available in a browser.

PRE-2: The browser permits Tripma to use its own first-party consent cookie.

### Post-Condition(s)

POST-1: On success, the visitor's current consent decision is stored in the browser.

POST-2: Tripma applies the stored decision to optional cookie categories.

POST-3: On failure, optional categories remain disabled and the visitor can retry.

### Basic Flow

1. The visitor opens Tripma.
2. Tripma requests the current consent state through API-COOKIE-CONSENT-GET.
3. Tripma finds no current decision and presents the cookie-consent experience.
4. The visitor opens cookie settings.
5. Tripma presents the available cookie categories and their current selections.
6. The visitor selects the optional categories to permit.
7. The visitor saves the selection.
8. Tripma submits the selection through API-COOKIE-CONSENT-UPDATE.
9. The consent service evaluates the request according to the Business Rules.
10. The service stores the decision in the Tripma first-party consent cookie.
11. API-COOKIE-CONSENT-UPDATE returns the effective consent state.
12. Tripma applies the effective state and closes the consent experience.

### Alternative Flow

AF-1: Accept all cookies

3a: The visitor chooses to accept all cookies.

3b: Tripma submits all optional categories as enabled through API-COOKIE-CONSENT-UPDATE.

3c: The Basic Flow resumes at step 9.

AF-2: Reject optional cookies

5a: The visitor disables every optional category and saves the selection.

5b: Tripma submits all optional categories as disabled through API-COOKIE-CONSENT-UPDATE.

5c: The Basic Flow resumes at step 9.

AF-3: Use a current saved decision

3a: API-COOKIE-CONSENT-GET returns a current consent decision.

3b: Tripma applies the returned state without presenting the initial consent prompt.

3c: The use case ends.

AF-4: Change a previous decision

3a: The visitor opens cookie settings while a current decision exists.

3b: Tripma presents the saved selections.

3c: The visitor changes and saves the selections.

3d: The Basic Flow resumes at step 8.

AF-5: Dismiss without deciding

3a: The visitor closes the consent experience without accepting, rejecting, or saving settings.

3b: Tripma closes it for the current page view without storing a decision.

3c: Optional cookie categories remain disabled.

### Exception Flow

EF-1: Stored consent cannot be read

2a: If the stored value is missing, expired, or unusable, Tripma treats the visitor as undecided.

2b: The Basic Flow resumes at step 3.

EF-2: Consent update is invalid

9a: If the submitted consent structure cannot be accepted, API-COOKIE-CONSENT-UPDATE returns an invalid-request outcome.

9b: Tripma retains the last effective state and keeps the settings available for correction.

EF-3: Consent cannot be stored

10a: If the browser or local API cannot store the decision, Tripma presents a retryable error state.

10b: Optional cookie categories remain disabled unless a previous current decision still applies.

### Related UI

Cookie-consent popup and cookie-settings experience on Tripma

### Related API IDs

API-COOKIE-CONSENT-GET; API-COOKIE-CONSENT-UPDATE

### Notes

Scope clarification: UC-15 manages consent choices only. It does not define analytics, advertising, or personalization features. The consent state is stored in a browser cookie and does not require a database table or authenticated account.

## UML Model

~~~plantuml
@startuml
hide empty members

enum CookieConsentStatus {
  UNDECIDED
  ACCEPTED_ALL
  REJECTED_OPTIONAL
  CUSTOM
}

class CookieConsent <<ValueObject>> {
  necessary: Boolean [1]
  analytics: Boolean [1]
  personalization: Boolean [1]
  marketing: Boolean [1]
  status: CookieConsentStatus [1]
}

class UpdateCookieConsentDto <<DTO>> {
  analytics: Boolean [1]
  personalization: Boolean [1]
  marketing: Boolean [1]
}

class CookieConsentDto <<DTO>> {
  necessary: Boolean [1]
  analytics: Boolean [1]
  personalization: Boolean [1]
  marketing: Boolean [1]
  status: CookieConsentStatus [1]
  policyVersion: String [1]
  decidedAt: DateTime [0..1]
  expiresAt: DateTime [0..1]
}

class CookieConsentResponseDto <<DTO>> {
  success: Boolean [1]
  data: CookieConsentDto [1]
}

class BrowserCookieStore <<Gateway>> {
  readConsent(): CookieConsent [0..1]
}

class CookieConsentService <<Service>> {
  getConsent(): CookieConsentResponseDto
  updateConsent(dto: UpdateCookieConsentDto): CookieConsentResponseDto
}

class User <<Entity>> {
  id: UUID [1]
}

CookieConsentResponseDto "1" *-- "1" CookieConsentDto : data
CookieConsentService ..> UpdateCookieConsentDto
CookieConsentService ..> CookieConsentResponseDto
CookieConsentService ..> CookieConsent
CookieConsentService ..> BrowserCookieStore
CookieConsent --> "1" CookieConsentStatus : status
CookieConsentDto --> "1" CookieConsentStatus : status

@enduml
~~~

## Business Rules

The following rules are authoritative for Prompt E. OCL is preserved where applicable; browser-storage and non-OCL constraints remain authoritative natural-language requirements.

~~~text
BR-COOKIE-001 - Necessary category
context CookieConsent
inv BR_COOKIE_001_Necessary:
  self.necessary = true


BR-COOKIE-002 - Undecided state
context CookieConsentService::getConsent() : CookieConsentResponseDto
post BR_COOKIE_002_Undecided:
  readConsent().oclIsUndefined()
  implies
    result.success and
    result.data.necessary and
    not result.data.analytics and
    not result.data.personalization and
    not result.data.marketing and
    result.data.status = CookieConsentStatus::UNDECIDED and
    result.data.decidedAt.oclIsUndefined() and
    result.data.expiresAt.oclIsUndefined()


BR-COOKIE-003 - Accepted-all status
context CookieConsent
inv BR_COOKIE_003_AcceptedAll:
  self.status = CookieConsentStatus::ACCEPTED_ALL
  implies
    self.analytics and
    self.personalization and
    self.marketing


BR-COOKIE-004 - Rejected-optional status
context CookieConsent
inv BR_COOKIE_004_RejectedOptional:
  self.status = CookieConsentStatus::REJECTED_OPTIONAL
  implies
    not self.analytics and
    not self.personalization and
    not self.marketing


BR-COOKIE-005 - Custom status
context CookieConsent
inv BR_COOKIE_005_Custom:
  self.status = CookieConsentStatus::CUSTOM
  implies
    Sequence { self.analytics, self.personalization, self.marketing }
      ->select(value | value)->size() > 0 and
    Sequence { self.analytics, self.personalization, self.marketing }
      ->select(value | value)->size() < 3


BR-COOKIE-006 - Status derivation
context CookieConsentService::updateConsent(
  dto : UpdateCookieConsentDto
) : CookieConsentResponseDto
post BR_COOKIE_006_Status:
  result.success implies
    result.data.status =
      if dto.analytics and dto.personalization and dto.marketing
      then CookieConsentStatus::ACCEPTED_ALL
      else
        if not dto.analytics and
           not dto.personalization and
           not dto.marketing
        then CookieConsentStatus::REJECTED_OPTIONAL
        else CookieConsentStatus::CUSTOM
        endif
      endif


BR-COOKIE-007 - Submitted preferences
context CookieConsentService::updateConsent(
  dto : UpdateCookieConsentDto
) : CookieConsentResponseDto
post BR_COOKIE_007_Preferences:
  result.success implies
    result.data.necessary and
    result.data.analytics = dto.analytics and
    result.data.personalization = dto.personalization and
    result.data.marketing = dto.marketing


BR-COOKIE-008 - Decision timestamps
context CookieConsentService::updateConsent(
  dto : UpdateCookieConsentDto
) : CookieConsentResponseDto
post BR_COOKIE_008_Timestamps:
  result.success implies
    result.data.decidedAt = now() and
    result.data.expiresAt = result.data.decidedAt + days(180)


BR-COOKIE-009 - Current policy version
context CookieConsentService::updateConsent(
  dto : UpdateCookieConsentDto
) : CookieConsentResponseDto
post BR_COOKIE_009_PolicyVersion:
  result.success implies
    not result.data.policyVersion.oclIsUndefined() and
    trim(result.data.policyVersion) <> ''


BR-COOKIE-010 - Consent renewal
A stored decision shall be treated as undecided when it is expired or its policy
version differs from the current Tripma consent-policy version. Tripma shall ask
the visitor for a new decision before enabling optional categories.


BR-COOKIE-011 - Complete replacement
Saving new settings shall replace the previous optional-category selections,
decision status, decision time, expiration time, and policy version as one
consent value.


BR-COOKIE-012 - Idempotent effective selection
Submitting the same optional-category selection repeatedly shall produce the
same effective category permissions and shall not create additional browser
consent cookies.


BR-COOKIE-013 - Dismissal is not consent
Closing the consent experience without an explicit accept, reject, or settings
save action shall not store a consent decision. Optional categories shall remain
disabled for that undecided browser.


BR-COOKIE-014 - Optional-category gating
Tripma shall enable analytics, personalization, or marketing cookie behavior
only when the corresponding effective consent value is true. Necessary behavior
does not depend on optional consent.


BR-COOKIE-015 - Browser scope
The consent decision applies only to the browser profile and Tripma origin in
which it was stored. It shall not create or update a User account.


BR-COOKIE-016 - Read-only retrieval
Calling API-COOKIE-CONSENT-GET shall not change the stored consent value or its
decision and expiration timestamps.


BR-COOKIE-017 - Local first-party persistence
API-COOKIE-CONSENT-UPDATE shall store exactly one Tripma first-party consent
cookie for the effective decision. UC-15 requires neither an external service
nor a database record and shall operate on the local Tripma origin.
~~~
