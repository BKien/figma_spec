---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-02
uc_name: "Log In"
---

# UC-02: Log In

## Functional Use-Case Specification

### Use Case ID

UC-02

### Use Case Name

Log In

### Description

As a registered visitor, I want to authenticate with email and password so that I can access protected features.

### Actor(s)

Visitor; Authentication Service.

### Priority

P0.

### Trigger

The visitor chooses to log in.

### Pre-Condition(s)

PRE-1: The visitor is viewing a login interface.

### Post-Condition(s)

POST-1: The client displays the login outcome returned by the system.

POST-2: The interface reflects the navigation state associated with that outcome.

### Basic Flow

1. The visitor opens the login form.
2. The client presents the credential fields and the available navigation.
3. The visitor enters credentials and submits the form.
4. The client sends the entered credentials to the login API.
5. The system processes the request and returns a login outcome.
6. The client renders the returned outcome and its available continuation.

### Alternative Flow

AF-1: Open Registration Instead of Logging In

3a: The visitor opens the registration interface instead of submitting credentials.

AF-2: Revise Credentials After Rejection

6a: After a returned rejection, the visitor replaces the entered credentials and submits a new request.

### Exception Flow

EF-1: Login Request Failure

5a: If the login request cannot be completed, the client displays a technical-failure state.

5b: The visitor may retry from the login interface.

### Related UI

Login page; log in.

### Related API IDs

API-AUTH-LOGIN.

### Notes

None.

## UML Model

~~~plantuml
@startuml
hide empty members

class DateTime {
  +>(other: DateTime): Boolean
}

class RequestContext {
  +{static} startedAt: DateTime
}

class PasswordHasher {
  +{static} matches(password: String, hash: String): Boolean
}

class User {
  +email: String
  +passwordHash: String
  +active: Boolean
}

class Session {
  +accessToken: String
  +expiresAt: DateTime
  +user: User
  +tokenHash: String
}

class AuthService {
  +login(command: LoginCommand): LoginOutcome
}

class IdentityNormalization {
  +{static} canonicalEmail(value: String): String
}

class LoginCommand {
  +email: String
  +password: String
}

class LoginOutcome {
  +accepted: Boolean
  +publicCode: String
  +session: Session
}

class TokenHasher {
  +{static} hash(value: String): String
}

class ReadState {
  +{static} users(): String
  +{static} sessions(): String
}

Session --> User : user
LoginOutcome --> Session : session

@enduml
~~~

## Business Rules

~~~text
BR-LOGIN-01 - Acceptance Requires One Active Credential Match
Source: Assumption
context AuthService::login(command: LoginCommand): LoginOutcome
post BR_LOGIN_01_AcceptanceRequiresOneActiveCredentialMatch:
  result.accepted =
    (User.allInstances()->select(u |
      u.active and
      IdentityNormalization::canonicalEmail(u.email) =
        IdentityNormalization::canonicalEmail(command.email) and
      PasswordHasher::matches(command.password, u.passwordHash))->size() = 1)
~~~

~~~text
BR-LOGIN-02 - All Credential Rejections Are Publicly Indistinguishable
Source: Assumption
context AuthService::login(command: LoginCommand): LoginOutcome
post BR_LOGIN_02_AllCredentialRejectionsArePubliclyIndistinguishable:
  not result.accepted implies
    result.publicCode = 'INVALID_CREDENTIALS' and result.session = null
~~~

~~~text
BR-LOGIN-03 - Accepted Session Is Bound To Matched Identity
Source: Assumption
context AuthService::login(command: LoginCommand): LoginOutcome
post BR_LOGIN_03_AcceptedSessionIsBoundToMatchedIdentity:
  result.accepted implies
    result.session <> null and
    result.session.user.active and
    IdentityNormalization::canonicalEmail(result.session.user.email) =
      IdentityNormalization::canonicalEmail(command.email) and
    result.session.expiresAt > RequestContext::startedAt
~~~

~~~text
BR-LOGIN-04 - Authentication Does Not Mutate Identity Records
Source: Assumption
context AuthService::login(command: LoginCommand): LoginOutcome
post BR_LOGIN_04_AuthenticationDoesNotMutateIdentityRecords:
  ReadState::users() = ReadState::users()@pre
~~~

~~~text
BR-LOGIN-05 - Accepted Session Is New And Token Is Distinct
Source: Assumption
context AuthService::login(command: LoginCommand): LoginOutcome
post BR_LOGIN_05_AcceptedSessionIsNewAndTokenIsDistinct:
  result.accepted implies
    result.session.oclIsNew() and
    Session.allInstances()@pre->forAll(s |
      s.tokenHash <> result.session.tokenHash)
~~~

~~~text
BR-LOGIN-06 - Rejected Login Creates No Session
Source: Assumption
context AuthService::login(command: LoginCommand): LoginOutcome
post BR_LOGIN_06_RejectedLoginCreatesNoSession:
  not result.accepted implies
    ReadState::sessions() = ReadState::sessions()@pre
~~~

~~~text
BR-LOGIN-07 - Session Persists Only Token Hash
Source: Assumption
context AuthService::login(command: LoginCommand): LoginOutcome
post BR_LOGIN_07_SessionPersistsOnlyTokenHash:
  result.accepted implies
    result.session.tokenHash = TokenHasher::hash(result.session.accessToken) and
    result.session.tokenHash <> result.session.accessToken
~~~
