---
artifact_type: business-use-case-specification
status: "Draft"
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

Enter the application with an existing identity.

### Actor(s)

Primary: Visitor. Supporting: application client and application service.

### Priority

High.

### Trigger

The visitor opens the login page.

### Pre-Condition(s)

PRE-1: The application view is open in the client.

### Post-Condition(s)

POST-1: On success, the client opens the home page with the returned user session.
POST-2: On failure, the client displays a recovery message in the current view.

### Basic Flow

1. The visitor opens the login page.
2. The client displays the login form.
3. The visitor enters email and password.
4. The visitor submits the form.
5. The client sends the login request.
6. The system returns the session result.
7. The client opens the home page.

### Alternative Flow

AF-1:

1. The visitor selects Create an account.
2. The client opens the registration page.

### Exception Flow

EF-1:

1. The system returns an operation error.
2. The client displays the error message and keeps the current view open.
3. The actor revises the interaction or retries the request.

### Related UI

- Product-source UI descriptions: [Use cases rows 26-43](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A26:B43). No Figma node identifier was supplied.

### Related API IDs

- [API-AUTH-LOGIN](../api/api-auth-login.md)

### Notes

See [source mapping](../../coverage-report.md), [review decisions](../../consistency-review.md), and [assumptions](../../ASSUMPTIONS.md). The supplied spreadsheet is specification evidence; no running application or Figma interaction was verified.

## UML Model

~~~plantuml
@startuml
hide empty members

class AuthClient {
  +establish(response: AuthResult): ClientSession
}

class AuthResult {
  +success: Boolean
  +evaluated: Boolean
  +user: PublicUser [0..1]
  +accessToken: String [0..1]
  +secretFields: Set(String)
  +loggedFields: Set(String)
}

class AuthService {
  +login(ctx: RequestContext, cmd: LoginCommand): AuthResult
}

class ClientSession {
  +accessToken: String [0..1]
  +user: PublicUser [0..1]
  +storage: String
  +durableFields: Set(String)
}

class LoginCommand {
  +email: String
  +password: String
}

class PasswordHasher {
  +{static} matches(password: String, hash: String): Boolean
}

class PublicUser {
  +id: Integer
  +fullName: String
  +email: String
}

class RequestContext {
  ' Only the type is referenced by this use case's Business Rules.
}

class Text {
  +{static} trim(s: String): String
  +{static} lower(s: String): String
  +{static} email(s: String): Boolean
}

class User {
  +id: Integer
  +fullName: String
  +email: String
  +username: String
  +passwordHash: String
  +version: Integer
}

AuthResult --> PublicUser : user
ClientSession --> PublicUser : user

@enduml
~~~

## Business Rules

~~~ocl
-- BR-UC-02-01
-- Source: Product source
context AuthService::login(ctx: RequestContext, cmd: LoginCommand): AuthResult
pre BR_UC_02_01_Email:
  Text::email(Text::lower(Text::trim(cmd.email)))
~~~

~~~ocl
-- BR-UC-02-02
-- Source: Product source
context AuthService::login(ctx: RequestContext, cmd: LoginCommand): AuthResult
pre BR_UC_02_02_PasswordPresent:
  cmd.password.size() > 0
~~~

~~~ocl
-- BR-UC-02-03
-- Source: Product source
-- evaluated distinguishes a completed credential evaluation from infrastructure failure; it is internal and not a wire field.
context AuthService::login(ctx: RequestContext, cmd: LoginCommand): AuthResult
post BR_UC_02_03_Credentials:
  result.evaluated implies result.success = User.allInstances()->exists(u | u.email = Text::lower(Text::trim(cmd.email)) and PasswordHasher::matches(cmd.password, u.passwordHash))
~~~

~~~ocl
-- BR-UC-02-04
-- Source: Product source
context AuthService::login(ctx: RequestContext, cmd: LoginCommand): AuthResult
post BR_UC_02_04_CorrectIdentity:
  result.success implies User.allInstances()->exists(u | u.id = result.user.id and u.email = Text::lower(Text::trim(cmd.email)) and u.email = result.user.email and u.fullName = result.user.fullName)
~~~

~~~ocl
-- BR-UC-02-05
-- Source: Product source
context AuthService::login(ctx: RequestContext, cmd: LoginCommand): AuthResult
post BR_UC_02_05_SessionIssued:
  result.success implies not result.accessToken.oclIsUndefined() and result.accessToken.size() > 0
~~~

~~~ocl
-- BR-UC-02-06
-- Source: Product source
context AuthService::login(ctx: RequestContext, cmd: LoginCommand): AuthResult
post BR_UC_02_06_FailureSession:
  not result.success implies result.accessToken.oclIsUndefined() and result.user.oclIsUndefined()
~~~

~~~ocl
-- BR-UC-02-07
-- Source: Product source
context AuthService::login(ctx: RequestContext, cmd: LoginCommand): AuthResult
post BR_UC_02_07_NoSecrets:
  result.secretFields->intersection(Set{'password','passwordHash'})->isEmpty() and result.loggedFields->intersection(Set{'password','passwordHash','accessToken'})->isEmpty()
~~~

~~~ocl
-- BR-UC-02-08
-- Source: Product source
-- Equality denotes the complete persistent value snapshot, including every property, not object identity alone.
context AuthService::login(ctx: RequestContext, cmd: LoginCommand): AuthResult
post BR_UC_02_08_UserUnchanged:
  User.allInstances()->collect(e | Tuple{id = e.id, fullName = e.fullName, email = e.email, username = e.username, passwordHash = e.passwordHash, version = e.version})->asSet() = User.allInstances()@pre->collect(e | Tuple{id = e.id@pre, fullName = e.fullName@pre, email = e.email@pre, username = e.username@pre, passwordHash = e.passwordHash@pre, version = e.version@pre})->asSet()
~~~

~~~ocl
-- BR-UC-02-09
-- Source: Assumption
context AuthClient::establish(response: AuthResult): ClientSession
post BR_UC_02_09_MemorySession:
  response.success implies result.accessToken = response.accessToken and result.user = response.user and result.storage = 'Memory' and result.durableFields->intersection(Set{'accessToken','password','passwordHash'})->isEmpty()
~~~
