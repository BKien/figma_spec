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

A visitor creates a customer account from the sign-up form.

### Actor(s)

Visitor; client; system.

### Priority

P0.

### Trigger

The visitor opens Sign Up.

### Pre-Condition(s)

PRE-1: The sign-up form is visible.

### Post-Condition(s)

POST-1: The client displays the registration outcome and its next action.

### Basic Flow

1. The visitor opens the sign-up form.
2. The client displays the form fields and agreement control.
3. The visitor enters account details and submits the form.
4. The client sends the registration request.
5. The system returns the account outcome and verification prompt.
6. The visitor enters the displayed code.
7. The client submits verification and displays the returned completion.

### Alternative Flow

AF-1: Switch to Sign In

3a: The visitor switches to the sign-in form, and the client displays it.

### Exception Flow

EF-1: Registration Error

5a: The client displays the returned registration error and keeps the form available.

### Related UI

- [Sign Up](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=339-1015) (339:1015)
- [Sign Up Popup Web](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=2178-2751) (2178:2751)
- [registration OTP state](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=395-748) (395:748)

### Related API IDs

- [API-ACCOUNT-REGISTER](../api/API-ACCOUNT-REGISTER.md)
- [API-ACCOUNT-VERIFY](../api/API-ACCOUNT-VERIFY.md)

### Notes

The UI establishes the interaction boundary. Rule values and persistence behavior are explicit assumptions in [ASSUMPTIONS.md](../../ASSUMPTIONS.md).

## UML Model

~~~plantuml
@startuml
hide empty members

enum AccountStatus {
  PENDING_VERIFICATION
  ACTIVE
  SUSPENDED
}

enum ChallengePurpose {
  REGISTRATION
  BOOKING
}

class Account {
  +id: String
  +emailCanonical: String
  +displayName: String
  +passwordHash: String
  +status: AccountStatus
}

class VerificationChallenge {
  +account: Account
  +codeHash: String
  +purpose: ChallengePurpose
  +expiresAt: DateTime
  +consumedAt: DateTime
}

class RegistrationCommand {
  +email: String
  +password: String
  +displayName: String
  +agreementAccepted: Boolean
}

class VerifyAccountCommand {
  +accountId: String
  +code: String
}

class AuthService {
  +register(command: RegistrationCommand): Account
  +verify(command: VerifyAccountCommand): Account
}

class Email <<utility>> {
  +{static} normalize(value: String): String
}

class PasswordHash <<utility>> {
  +{static} of(value: String): String
}

class CodeHash <<utility>> {
  +{static} matches(value: String, storedHash: String): Boolean
}

class DateTime <<primitive>> {
  +{static} now(): DateTime
}

Account "1" -- "*" VerificationChallenge
Account --> "1" AccountStatus : status
VerificationChallenge --> "1" ChallengePurpose : purpose

@enduml
~~~

## Business Rules

~~~text
BR-REGISTER-ACCOUNT-01 - Email Is Unique
Source: Assumption
context AuthService::register(command: RegistrationCommand): Account
pre BR_REGISTER_ACCOUNT_01_EmailIsUnique:
  Account.allInstances()->forAll(a | a.emailCanonical <> Email::normalize(command.email))
~~~
~~~text
BR-REGISTER-ACCOUNT-02 - Password Is Stored As Hash
Source: Assumption
context AuthService::register(command: RegistrationCommand): Account
post BR_REGISTER_ACCOUNT_02_PasswordIsStoredAsHash:
  result.passwordHash = PasswordHash::of(command.password) and result.passwordHash <> command.password
~~~
~~~text
BR-REGISTER-ACCOUNT-03 - New Account Awaits Verification
Source: Assumption
context AuthService::register(command: RegistrationCommand): Account
post BR_REGISTER_ACCOUNT_03_NewAccountAwaitsVerification:
  result.status = AccountStatus::PENDING_VERIFICATION
~~~
~~~text
BR-REGISTER-ACCOUNT-04 - Registration Challenge Is Created
Source: Assumption
context AuthService::register(command: RegistrationCommand): Account
post BR_REGISTER_ACCOUNT_04_RegistrationChallengeIsCreated:
  VerificationChallenge.allInstances()->exists(v | v.account.id = result.id and v.purpose = ChallengePurpose::REGISTRATION and v.codeHash <> null and v.expiresAt > DateTime::now())
~~~
~~~text
BR-REGISTER-ACCOUNT-05 - Registration Challenge Matches
Source: Assumption
context AuthService::verify(command: VerifyAccountCommand): Account
pre BR_REGISTER_ACCOUNT_05_RegistrationChallengeMatches:
  VerificationChallenge.allInstances()->exists(v | v.account.id = command.accountId and v.purpose = ChallengePurpose::REGISTRATION and CodeHash::matches(command.code, v.codeHash) and v.expiresAt > DateTime::now() and v.consumedAt = null)
~~~
~~~text
BR-REGISTER-ACCOUNT-06 - Verification Activates Account
Source: Assumption
context AuthService::verify(command: VerifyAccountCommand): Account
post BR_REGISTER_ACCOUNT_06_VerificationActivatesAccount:
  result.id = command.accountId and result.status = AccountStatus::ACTIVE
~~~
~~~text
BR-REGISTER-ACCOUNT-07 - Account Fields Are Canonical
Source: Assumption
context AuthService::register(command: RegistrationCommand): Account
post BR_REGISTER_ACCOUNT_07_AccountFieldsAreCanonical:
  result.emailCanonical = Email::normalize(command.email) and result.displayName = command.displayName
~~~
~~~text
BR-REGISTER-ACCOUNT-08 - Agreement Is Accepted
Source: Assumption
context AuthService::register(command: RegistrationCommand): Account
pre BR_REGISTER_ACCOUNT_08_AgreementIsAccepted:
  command.agreementAccepted = true
~~~
~~~text
BR-REGISTER-ACCOUNT-09 - Registration Challenge Is Consumed
Source: Assumption
context AuthService::verify(command: VerifyAccountCommand): Account
post BR_REGISTER_ACCOUNT_09_RegistrationChallengeIsConsumed:
  VerificationChallenge.allInstances()->exists(v | v.account.id = command.accountId and v.purpose = ChallengePurpose::REGISTRATION and v.consumedAt <> null)
~~~
