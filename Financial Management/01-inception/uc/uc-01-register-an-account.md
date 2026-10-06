---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-01
uc_name: "Register an Account"
---

# UC-01: Register an Account

## Functional Use-Case Specification

### Use Case ID

UC-01

### Use Case Name

Register an Account

### Description

Create an application identity and enter the signed-in application.

### Actor(s)

Primary: Visitor. Supporting: application client and application service.

### Priority

High.

### Trigger

The visitor opens the registration page.

### Pre-Condition(s)

PRE-1: The application view is open in the client.

### Post-Condition(s)

POST-1: On success, the client opens the home page with the returned user session.
POST-2: On failure, the client displays a recovery message in the current view.

### Basic Flow

1. The visitor opens the registration page.
2. The client displays the registration form.
3. The visitor enters a full name, email, password, and password confirmation.
4. The visitor submits the form.
5. The client sends the registration request.
6. The system returns the account and session result.
7. The client opens the home page.

### Alternative Flow

AF-1:

1. The visitor returns to the login link.
2. The client opens the login page.

### Exception Flow

EF-1:

1. The system returns an operation error.
2. The client displays the error message and keeps the current view open.
3. The actor revises the interaction or retries the request.

### Related UI

- Product-source UI descriptions: [Use cases rows 5-24](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A5:B24). No Figma node identifier was supplied.

### Related API IDs

- [API-AUTH-REGISTER](../api/api-auth-register.md)

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
  +user: PublicUser [0..1]
  +accessToken: String [0..1]
  +secretFields: Set(String)
  +loggedFields: Set(String)
}

class AuthService {
  +register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
}

class ClientSession {
  +accessToken: String [0..1]
  +user: PublicUser [0..1]
  +storage: String
  +durableFields: Set(String)
}

class PasswordHasher {
  +{static} matches(password: String, hash: String): Boolean
  +{static} cost(hash: String): Integer
}

class PublicUser {
  +id: Integer
}

class RegisterCommand {
  +fullName: String
  +email: String
  +password: String
  +confirmPassword: String
}

class RequestContext {
  ' Only the type is referenced by this use case's Business Rules.
}

class Text {
  +{static} trim(s: String): String
  +{static} nfc(s: String): String
  +{static} lower(s: String): String
  +{static} matches(s: String, pattern: String): Boolean
  +{static} email(s: String): Boolean
  +{static} username(email: String, taken: Set(String)): String
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
-- BR-UC-01-01
-- Source: Product source
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
pre BR_UC_01_01_Name:
  let n : String = Text::trim(Text::nfc(cmd.fullName)) in n.size() >= 4 and n.size() <= 25 and Text::matches(n, '^[\p{L}]+(?: [\p{L}]+)*$')
~~~

~~~ocl
-- BR-UC-01-02
-- Source: Product source
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
pre BR_UC_01_02_Email:
  Text::email(Text::lower(Text::trim(cmd.email))) and Text::trim(cmd.email).size() <= 255
~~~

~~~ocl
-- BR-UC-01-03
-- Source: Product source
context User
inv BR_UC_01_03_UniqueEmail:
  User.allInstances()->isUnique(email)
~~~

~~~ocl
-- BR-UC-01-04
-- Source: Product source
context User
inv BR_UC_01_04_Username:
  User.allInstances()->isUnique(username)
~~~

~~~ocl
-- BR-UC-01-05
-- Source: Product source
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
pre BR_UC_01_05_Password:
  cmd.password.size() >= 8 and cmd.password.size() <= 64 and Text::matches(cmd.password, '^[A-Za-z0-9!@#$%^&*(){}_+=\[\],./<>?\\|:;\-]+$') and Text::matches(cmd.password, '.*[a-z].*') and Text::matches(cmd.password, '.*[A-Z].*') and Text::matches(cmd.password, '.*[0-9].*') and Text::matches(cmd.password, '.*[^A-Za-z0-9].*')
~~~

~~~ocl
-- BR-UC-01-06
-- Source: Product source
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
pre BR_UC_01_06_Confirmation:
  cmd.confirmPassword = cmd.password
~~~

~~~ocl
-- BR-UC-01-07
-- Source: Product source
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
post BR_UC_01_07_CreatedIdentity:
  result.success implies User.allInstances()->one(u | u.id = result.user.id and u.email = Text::lower(Text::trim(cmd.email)) and u.fullName = Text::trim(Text::nfc(cmd.fullName)))
~~~

~~~ocl
-- BR-UC-01-08
-- Source: Product source
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
post BR_UC_01_08_PasswordStorage:
  result.success implies User.allInstances()->exists(u | u.id = result.user.id and PasswordHasher::matches(cmd.password, u.passwordHash) and PasswordHasher::cost(u.passwordHash) = 10)
~~~

~~~ocl
-- BR-UC-01-09
-- Source: Product source
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
post BR_UC_01_09_NoSecrets:
  result.secretFields->intersection(Set{'password','passwordHash','confirmPassword'})->isEmpty() and result.loggedFields->intersection(Set{'password','passwordHash','confirmPassword','accessToken'})->isEmpty()
~~~

~~~ocl
-- BR-UC-01-10
-- Source: Product source
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
post BR_UC_01_10_Session:
  result.success implies not result.accessToken.oclIsUndefined() and result.accessToken.size() > 0
~~~

~~~ocl
-- BR-UC-01-11
-- Source: Product source
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
post BR_UC_01_11_AtomicFailure:
  not result.success implies User.allInstances()->collect(e | Tuple{id = e.id, fullName = e.fullName, email = e.email, username = e.username, passwordHash = e.passwordHash, version = e.version})->asSet() = User.allInstances()@pre->collect(e | Tuple{id = e.id@pre, fullName = e.fullName@pre, email = e.email@pre, username = e.username@pre, passwordHash = e.passwordHash@pre, version = e.version@pre})->asSet() and result.accessToken.oclIsUndefined()
~~~

~~~ocl
-- BR-UC-01-12
-- Source: Product source
-- username uses the normalized email prefix, then the first free positive integer suffix on collision. Creation relies on database username/email uniqueness and retries a username collision within the operation.
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
post BR_UC_01_12_GeneratedUsername:
  result.success implies User.allInstances()->any(u | u.id = result.user.id).username = Text::username(Text::lower(Text::trim(cmd.email)), User.allInstances()@pre->collect(u | u.username@pre)->asSet())
~~~

~~~ocl
-- BR-UC-01-13
-- Source: Product source
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
post BR_UC_01_13_ExactlyOneUser:
  result.success implies User.allInstances()->size() = User.allInstances()@pre->size() + 1
~~~

~~~ocl
-- BR-UC-01-14
-- Source: Assumption
context AuthClient::establish(response: AuthResult): ClientSession
post BR_UC_01_14_MemorySession:
  response.success implies result.accessToken = response.accessToken and result.user = response.user and result.storage = 'Memory' and result.durableFields->intersection(Set{'accessToken','password','passwordHash','confirmPassword'})->isEmpty()
~~~
