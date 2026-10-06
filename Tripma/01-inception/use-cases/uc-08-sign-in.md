---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-08
uc_name: "Sign In"
---

# UC-08: Sign In

## Functional Use-Case Specification

### Use Case ID

UC-08

### Use Case Name

Sign In

### Description

As a visitor, I want to sign in to my Tripma account so that Tripma can recognize my authenticated session.

### Actor(s)

Visitor

### Priority

High

### Trigger

The visitor initiates sign-in from the Tripma navbar.

### Pre-Condition(s)

PRE-1: The Tripma authentication experience is available.
PRE-2: Tripma can accept an authentication request.

### Post-Condition(s)

POST-1: When sign-in succeeds, an authenticated Tripma session is available to subsequent experiences.
POST-2: When sign-in cannot be completed, no authenticated session is created and Tripma reports the outcome.

### Basic Flow

1. The visitor initiates sign-in from the Tripma navbar.
2. Tripma presents the sign-in experience.
3. The visitor supplies the requested account information.
4. Tripma evaluates the supplied information according to the Business Rules.
5. The visitor submits the sign-in request.
6. Tripma sends the request through API-AUTH-SIGNIN.
7. The authentication service evaluates the request according to the Business Rules.
8. The authentication service establishes an authenticated session.
9. API-AUTH-SIGNIN returns the sign-in outcome.
10. Tripma closes the sign-in experience and continues from the initiating context.

### Alternative Flow

AF-1: Close sign-in
3a. The visitor closes the sign-in experience before submitting.
3b. Tripma returns to the initiating context without creating a session.

### Exception Flow

EF-1: Sign-in information requires attention
4a. If the supplied information cannot be accepted, Tripma identifies the affected input and does not submit the request.

EF-2: Credentials are not accepted
7a. If the submitted credentials cannot authenticate an account, API-AUTH-SIGNIN returns the corresponding outcome.
7b. Tripma preserves the usable sign-in state and permits another attempt.

EF-3: Request cannot be completed
6a. If Tripma cannot complete the request because of a technical failure, it presents a retryable error state.

### Related UI

Navbar sign-in entry; Tripma authentication experience

### Related API IDs

API-AUTH-SIGNIN

### Notes

Scope clarification: UC-08 authenticates an existing Tripma account and establishes its session. Account registration remains assigned to UC-07. Booking and payment behavior remain outside this use case.

## UML Model

~~~plantuml
@startuml
hide empty members

class User <<Entity>> {
  id: UUID [1]
  email: String [1]
  passwordHash: String [1]
  username: String [1]
}

class SignInDto <<DTO>> {
  email: String [1]
  password: String [1]
}

class AuthenticatedUserDto <<DTO>> {
  id: UUID [1]
  email: String [1]
  username: String [1]
}

class JwtClaimsDto <<DTO>> {
  userId: UUID [1]
  email: String [1]
  username: String [1]
  issuedAt: DateTime [1]
  expiresAt: DateTime [1]
}

class SessionDto <<DTO>> {
  expiresAt: DateTime [1]
}

class SignInDataDto <<DTO>> {
  user: AuthenticatedUserDto [1]
  session: SessionDto [1]
}

class SignInResponseDto <<DTO>> {
  success: Boolean [1]
  data: SignInDataDto [0..1]
}

class SignInService <<Service>> {
  signIn(dto: SignInDto): SignInResponseDto
  createJwt(user: User): JwtClaimsDto
  createSession(token: JwtClaimsDto): SessionDto
}

class PasswordHasher <<Service>> {
  matches(password: String, hash: String): Boolean
}

SignInDataDto "1" *-- "1" AuthenticatedUserDto : user
SignInDataDto "1" *-- "1" SessionDto : session
SignInResponseDto "1" *-- "0..1" SignInDataDto : data
SignInService ..> SignInDto
SignInService ..> SignInResponseDto
SignInService ..> JwtClaimsDto
SignInService ..> SessionDto
SignInService ..> User
SignInService ..> PasswordHasher

@enduml
~~~

## Business Rules

The following rules are authoritative for Prompt E. OCL is preserved where applicable; technical or non-OCL constraints remain authoritative natural-language requirements.

~~~text
BR-SIGNIN-001: Required credential input
context SignInService::signIn(
  dto : SignInDto
) : SignInResponseDto
pre BR_SIGNIN_001_Required:
  not dto.email.oclIsUndefined() and trim(dto.email) <> '' and
  not dto.password.oclIsUndefined() and trim(dto.password) <> ''


BR-SIGNIN-002: Accepted credential email
context SignInService::signIn(
  dto : SignInDto
) : SignInResponseDto
pre BR_SIGNIN_002_Email:
  isEmail(normalizeEmail(dto.email))


BR-SIGNIN-003: Credential password length
context SignInService::signIn(
  dto : SignInDto
) : SignInResponseDto
pre BR_SIGNIN_003_PasswordLength:
  dto.password.size() >= 8


BR-SIGNIN-004: Credential authentication
context SignInService::signIn(
  dto : SignInDto
) : SignInResponseDto
post BR_SIGNIN_004_Outcome:
  result.success implies
    User.allInstances()->exists(user |
      normalizeEmail(user.email) = normalizeEmail(dto.email) and
      matches(dto.password, user.passwordHash))


BR-SIGNIN-005: Credential rejection
context SignInService::signIn(
  dto : SignInDto
) : SignInResponseDto
post BR_SIGNIN_005_Rejection:
  not User.allInstances()->exists(user |
    normalizeEmail(user.email) = normalizeEmail(dto.email) and
    matches(dto.password, user.passwordHash))
  implies
    not result.success and result.data.oclIsUndefined()


BR-SIGNIN-006: Authenticated account identity
context SignInService::signIn(
  dto : SignInDto
) : SignInResponseDto
post BR_SIGNIN_006_User:
  result.success implies
    User.allInstances()->one(user |
      user.id = result.data.user.id and
      normalizeEmail(user.email) = normalizeEmail(dto.email))


BR-SIGNIN-007: JWT claims
context SignInService::createJwt(
  user : User
) : JwtClaimsDto
post BR_SIGNIN_007_Claims:
  result.userId = user.id and
  result.email = user.email and
  result.username = user.username and
  result.issuedAt <= result.expiresAt


BR-SIGNIN-008: Session projection
context SignInService::createSession(
  token : JwtClaimsDto
) : SessionDto
post BR_SIGNIN_008_Session:
  result.expiresAt = token.expiresAt


BR-SIGNIN-009: Sign-in response
context SignInService::signIn(
  dto : SignInDto
) : SignInResponseDto
post BR_SIGNIN_009_Response:
  result.success implies
    not result.data.oclIsUndefined() and
    not result.data.session.expiresAt.oclIsUndefined() and
    User.allInstances()->one(user |
      user.id = result.data.user.id and
      user.email = result.data.user.email and
      user.username = result.data.user.username)


BR-SIGNIN-010: Sensitive authentication data
Passwords, password hashes and JWT contents shall not be
returned in the API-AUTH-SIGNIN response.
Technical constraints:
- Authentication secrets and tokens must not appear in URLs, analytics, traces or application logs.
- The session token is transmitted only through a Secure, HttpOnly cookie with an appropriate SameSite policy.

~~~
