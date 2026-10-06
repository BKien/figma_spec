---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-07
uc_name: "Sign Up"
---

# UC-07: Sign Up

## Functional Use-Case Specification

### Use Case ID

UC-07

### Use Case Name

Sign Up

### Description

As a visitor, I want to create a Tripma account with email and password so that I can use account-based Tripma experiences.

### Actor(s)

Visitor

### Priority

High

### Trigger

The visitor opens the Tripma sign-up experience from an available entry point.

### Pre-Condition(s)

PRE-1: The Tripma authentication experience is available.
PRE-2: Tripma can accept an account request from the current experience.

### Post-Condition(s)

POST-1: When sign-up succeeds, Tripma makes the new account available to subsequent account experiences.
POST-2: When UC-07 was invoked by another use case, Tripma returns the sign-up outcome to that use case.
POST-3: When sign-up cannot be completed, Tripma preserves the usable form state and reports the outcome.

### Basic Flow

1. The visitor opens the Tripma authentication modal.
2. The visitor chooses the Sign Up experience.
3. Tripma presents the email-and-password sign-up form.
4. The visitor supplies the requested account information and consent selections.
5. Tripma evaluates the form according to the Business Rules.
6. The visitor chooses Create account.
7. Tripma submits the request through API-AUTH-SIGNUP.
8. The account service evaluates the request according to the Business Rules.
9. The account service creates the Tripma account.
10. API-AUTH-SIGNUP returns the sign-up outcome.
11. Tripma presents the successful outcome and closes the sign-up form.

### Alternative Flow

AF-1: Open sign-up directly
1a. The visitor chooses Sign up from the Tripma navigation area.
1b. Tripma opens the authentication modal in Sign Up mode.
1c. The Basic Flow resumes at step 3.

AF-2: Sign up during checkout
1a. UC-05 invokes UC-07 from its account-creation entry point.
1b. Tripma opens the Sign Up experience without replacing the usable checkout context.
1c. When UC-07 succeeds, control returns to UC-05.

AF-3: Decline optional deal alerts
4a. The visitor leaves the optional deal-alert selection disabled.
4b. The Basic Flow resumes at step 5.

AF-4: Close the sign-up form
4a. The visitor closes the modal before submitting.
4b. Tripma discards the unsubmitted interaction and returns to the calling experience.

### Exception Flow

EF-1: Sign-up information requires attention
5a. If the form cannot be accepted, Tripma identifies the affected input and does not submit the request.

EF-2: Account identifier is unavailable
8a. If the account identifier cannot be used, API-AUTH-SIGNUP returns the corresponding outcome.
8b. Tripma preserves the usable form state.

EF-3: Account creation conflict
9a. If the account cannot be created because the persisted state changed, API-AUTH-SIGNUP returns a conflict outcome.
9b. Tripma does not create a duplicate account.

EF-4: Request cannot be completed
7a. If Tripma cannot complete the request because of a technical failure, it presents a retryable error state.

### Related UI

Navbar sign-up entry; Tripma email-and-password registration experience; account-creation entry point in the UC-05 payment experience

### Related API IDs

API-AUTH-SIGNUP

### Notes

Scope clarification: UC-07 may be invoked from the navbar or referenced by UC-05. Sign-in remains assigned to UC-08.

## UML Model

~~~plantuml
@startuml
hide empty members

class User <<Entity>> {
  id: UUID [1]
  email: String [1]
  passwordHash: String [1]
  username: String [1]
  receiveDealAlerts: Boolean [1]
  termsAcceptedAt: DateTime [1]
}

class SignUpDto <<DTO>> {
  email: String [1]
  password: String [1]
  agreeTerms: Boolean [1]
  receiveDealAlerts: Boolean [1]
}

class RegisteredUserDto <<DTO>> {
  id: UUID [1]
  email: String [1]
  username: String [1]
  receiveDealAlerts: Boolean [1]
  createdAt: DateTime [1]
}

class SignUpResponseDto <<DTO>> {
  success: Boolean [1]
  data: RegisteredUserDto [0..1]
}

class SignUpService <<Service>> {
  signUp(dto: SignUpDto): SignUpResponseDto
  canSubmit(dto: SignUpDto): Boolean
}

class PasswordHasher <<Service>> {
  matches(password: String, hash: String): Boolean
  cost(hash: String): Integer
}

SignUpService ..> SignUpDto
SignUpService ..> SignUpResponseDto
SignUpService ..> PasswordHasher
SignUpService ..> User
SignUpResponseDto "1" *-- "0..1" RegisteredUserDto : data
RegisteredUserDto ..> User : maps from

@enduml
~~~

## Business Rules

The following rules are authoritative for Prompt E. OCL is preserved where applicable; technical or non-OCL constraints remain authoritative natural-language requirements.

~~~text
BR-SIGNUP-001: Required sign-up input
context SignUpService::signUp(
  dto : SignUpDto
) : SignUpResponseDto
pre BR_SIGNUP_001_Required:
  not dto.email.oclIsUndefined() and trim(dto.email) <> '' and
  not dto.password.oclIsUndefined() and trim(dto.password) <> '' and
  not dto.agreeTerms.oclIsUndefined() and
  not dto.receiveDealAlerts.oclIsUndefined()


BR-SIGNUP-002: Accepted email
context SignUpService::signUp(
  dto : SignUpDto
) : SignUpResponseDto
pre BR_SIGNUP_002_Email:
  isEmail(lower(trim(dto.email)))


BR-SIGNUP-003: Unique email
context SignUpService::signUp(
  dto : SignUpDto
) : SignUpResponseDto
pre BR_SIGNUP_003_EmailAvailable:
  User.allInstances()->select(user |
    lower(trim(user.email)) = lower(trim(dto.email)))->isEmpty()
Technical constraints:
- The normalized email is protected by a database unique constraint so concurrent requests cannot create duplicate accounts.


BR-SIGNUP-004: Password length
context SignUpService::signUp(
  dto : SignUpDto
) : SignUpResponseDto
pre BR_SIGNUP_004_PasswordLength:
  dto.password.size() >= 8


BR-SIGNUP-005: Terms acceptance
context SignUpService::signUp(
  dto : SignUpDto
) : SignUpResponseDto
pre BR_SIGNUP_005_Terms:
  dto.agreeTerms = true


BR-SIGNUP-006: Form readiness
context SignUpService::canSubmit(
  dto : SignUpDto
) : Boolean
post BR_SIGNUP_006_Result:
  result =
    not dto.email.oclIsUndefined() and trim(dto.email) <> '' and
    isEmail(lower(trim(dto.email))) and
    not dto.password.oclIsUndefined() and dto.password.size() >= 8 and
    dto.agreeTerms = true


BR-SIGNUP-007: Persisted account
context SignUpService::signUp(
  dto : SignUpDto
) : SignUpResponseDto
post BR_SIGNUP_007_User:
  result.success implies
    User.allInstances()->one(user |
      user.id = result.data.id and
      user.email = lower(trim(dto.email)) and
      not user.termsAcceptedAt.oclIsUndefined())


BR-SIGNUP-008: Generated username
context SignUpService::signUp(
  dto : SignUpDto
) : SignUpResponseDto
post BR_SIGNUP_008_Username:
  result.success implies
    not result.data.username.oclIsUndefined() and
    trim(result.data.username) <> '' and
    User.allInstances()->isUnique(user | lower(trim(user.username)))


BR-SIGNUP-009: Password storage
context SignUpService::signUp(
  dto : SignUpDto
) : SignUpResponseDto
post BR_SIGNUP_009_Hash:
  result.success implies
    let user : User = User.allInstances()->any(item |
      item.id = result.data.id)
    in
      user.passwordHash <> dto.password and
      matches(dto.password, user.passwordHash) and
      cost(user.passwordHash) >= 10
Technical constraints:
- Password hashing uses the approved adaptive password-hashing implementation with a configurable work factor.


BR-SIGNUP-010: Deal-alert preference
context SignUpService::signUp(
  dto : SignUpDto
) : SignUpResponseDto
post BR_SIGNUP_010_Alerts:
  result.success implies
    User.allInstances()->any(user |
      user.id = result.data.id).receiveDealAlerts = dto.receiveDealAlerts


BR-SIGNUP-011: Registration response
context SignUpService::signUp(
  dto : SignUpDto
) : SignUpResponseDto
post BR_SIGNUP_011_Response:
  result.success implies
    result.data.email = lower(trim(dto.email)) and
    result.data.receiveDealAlerts = dto.receiveDealAlerts and
    not result.data.createdAt.oclIsUndefined()


BR-SIGNUP-012: Sign-up boundary
UC-07 shall not create a booking, process a payment, or create an authenticated
session. Authentication is handled by UC-08 after the account has been created.


BR-SIGNUP-013: Sensitive sign-up data
The raw password and password hash shall not be returned by API-AUTH-SIGNUP.
Technical constraints:
- The raw password is accepted only in the HTTPS request body and must not appear in URLs, query strings, analytics, traces, or application logs.
- The password hash is excluded from default ORM selection and from all API response mappings.

~~~
