---
artifact_type: business-use-case-specification
status: Frozen
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

AF-1: Return to Login

4a: The visitor returns to the login link.

4b: The client opens the login page.

### Exception Flow

EF-1: Registration Operation Error

6a: The system returns an operation error.

6b: The client displays the error message and keeps the current view open.

6c: The actor revises the interaction or retries the request.

### Related UI

- Product-source UI descriptions: [Use cases rows 5-24](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A5:B24). No Figma node identifier was supplied.

### Related API IDs

- [API-AUTH-REGISTER](../api/API-AUTH-REGISTER.md)

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

~~~text
BR-REGISTER-ACCOUNT-01 - Name
Source: Product source
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
pre BR_REGISTER_ACCOUNT_01_Name:
  let n : String = Text::trim(Text::nfc(cmd.fullName)) in n.size() >= 4 and n.size() <= 25 and Text::matches(n, '^[\p{L}]+(?: [\p{L}]+)*$')
~~~

~~~text
BR-REGISTER-ACCOUNT-02 - Email
Source: Product source
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
pre BR_REGISTER_ACCOUNT_02_Email:
  Text::email(Text::lower(Text::trim(cmd.email))) and Text::trim(cmd.email).size() <= 255
~~~

~~~text
BR-REGISTER-ACCOUNT-03 - Unique Email
Source: Product source
context User
inv BR_REGISTER_ACCOUNT_03_UniqueEmail:
  User.allInstances()->isUnique(email)
~~~

~~~text
BR-REGISTER-ACCOUNT-04 - Username
Source: Product source
context User
inv BR_REGISTER_ACCOUNT_04_Username:
  User.allInstances()->isUnique(username)
~~~

~~~text
BR-REGISTER-ACCOUNT-05 - Password
Source: Product source
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
pre BR_REGISTER_ACCOUNT_05_Password:
  cmd.password.size() >= 8 and cmd.password.size() <= 64 and Text::matches(cmd.password, '^[A-Za-z0-9!@#$%^&*(){}_+=\[\],./<>?\\|:;\-]+$') and Text::matches(cmd.password, '.*[a-z].*') and Text::matches(cmd.password, '.*[A-Z].*') and Text::matches(cmd.password, '.*[0-9].*') and Text::matches(cmd.password, '.*[^A-Za-z0-9].*')
~~~

~~~text
BR-REGISTER-ACCOUNT-06 - Confirmation
Source: Product source
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
pre BR_REGISTER_ACCOUNT_06_Confirmation:
  cmd.confirmPassword = cmd.password
~~~

~~~text
BR-REGISTER-ACCOUNT-07 - Created Identity
Source: Product source
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
post BR_REGISTER_ACCOUNT_07_CreatedIdentity:
  result.success implies User.allInstances()->one(u | u.id = result.user.id and u.email = Text::lower(Text::trim(cmd.email)) and u.fullName = Text::trim(Text::nfc(cmd.fullName)))
~~~

~~~text
BR-REGISTER-ACCOUNT-08 - Password Storage
Source: Product source
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
post BR_REGISTER_ACCOUNT_08_PasswordStorage:
  result.success implies User.allInstances()->exists(u | u.id = result.user.id and PasswordHasher::matches(cmd.password, u.passwordHash) and PasswordHasher::cost(u.passwordHash) = 10)
~~~

~~~text
BR-REGISTER-ACCOUNT-09 - No Secrets
Source: Product source
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
post BR_REGISTER_ACCOUNT_09_NoSecrets:
  result.secretFields->intersection(Set{'password','passwordHash','confirmPassword'})->isEmpty() and result.loggedFields->intersection(Set{'password','passwordHash','confirmPassword','accessToken'})->isEmpty()
~~~

~~~text
BR-REGISTER-ACCOUNT-10 - Session
Source: Product source
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
post BR_REGISTER_ACCOUNT_10_Session:
  result.success implies not result.accessToken.oclIsUndefined() and result.accessToken.size() > 0
~~~

~~~text
BR-REGISTER-ACCOUNT-11 - Atomic Failure
Source: Product source
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
post BR_REGISTER_ACCOUNT_11_AtomicFailure:
  not result.success implies User.allInstances()->collect(e | Tuple{id = e.id, fullName = e.fullName, email = e.email, username = e.username, passwordHash = e.passwordHash, version = e.version})->asSet() = User.allInstances()@pre->collect(e | Tuple{id = e.id@pre, fullName = e.fullName@pre, email = e.email@pre, username = e.username@pre, passwordHash = e.passwordHash@pre, version = e.version@pre})->asSet() and result.accessToken.oclIsUndefined()
~~~

~~~text
BR-REGISTER-ACCOUNT-12 - Generated Username
Source: Product source
Note: username uses the normalized email prefix, then the first free positive integer suffix on collision. Creation relies on database username/email uniqueness and retries a username collision within the operation.
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
post BR_REGISTER_ACCOUNT_12_GeneratedUsername:
  result.success implies User.allInstances()->any(u | u.id = result.user.id).username = Text::username(Text::lower(Text::trim(cmd.email)), User.allInstances()@pre->collect(u | u.username@pre)->asSet())
~~~

~~~text
BR-REGISTER-ACCOUNT-13 - Exactly One User
Source: Product source
context AuthService::register(ctx: RequestContext, cmd: RegisterCommand): AuthResult
post BR_REGISTER_ACCOUNT_13_ExactlyOneUser:
  result.success implies User.allInstances()->size() = User.allInstances()@pre->size() + 1
~~~

~~~text
BR-REGISTER-ACCOUNT-14 - Memory Session
Source: Assumption
context AuthClient::establish(response: AuthResult): ClientSession
post BR_REGISTER_ACCOUNT_14_MemorySession:
  response.success implies result.accessToken = response.accessToken and result.user = response.user and result.storage = 'Memory' and result.durableFields->intersection(Set{'accessToken','password','passwordHash','confirmPassword'})->isEmpty()
~~~
