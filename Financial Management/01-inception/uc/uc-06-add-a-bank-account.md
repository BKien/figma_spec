---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-06
uc_name: "Add a Bank Account"
---

# UC-06: Add a Bank Account

## Functional Use-Case Specification

### Use Case ID

UC-06

### Use Case Name

Add a Bank Account

### Description

Add a manually tracked financial account and its opening balance.

### Actor(s)

Primary: Account holder. Supporting: application client and application service.

### Priority

High.

### Trigger

The user opens the Add Account form.

### Pre-Condition(s)

PRE-1: The application view is open in the client.

### Post-Condition(s)

POST-1: On success, the client displays account creation confirmation and returns to Accounts.
POST-2: On failure, the client displays a recovery message in the current view.

### Basic Flow

1. The user opens the Add Account form.
2. The client displays account fields.
3. The user enters account details and submits the form.
4. The client sends the account creation request.
5. The system returns the account result.
6. The client displays confirmation and returns to Accounts.

### Alternative Flow

AF-1:

1. The user cancels the form.
2. The client returns to Accounts.

### Exception Flow

EF-1:

1. The system returns an operation error.
2. The client displays the error message and keeps the current view open.
3. The actor revises the interaction or retries the request.

EF-2:

1. The system returns a rejected authentication context.
2. The client presents the login entry point.

### Related UI

- Product-source UI descriptions: [Use cases rows 106-131](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A106:B131). No Figma node identifier was supplied.

### Related API IDs

- [API-ACCOUNT-CREATE](../api/api-account-create.md)

### Notes

See [source mapping](../../coverage-report.md), [review decisions](../../consistency-review.md), and [assumptions](../../ASSUMPTIONS.md). The supplied spreadsheet is specification evidence; no running application or Figma interaction was verified.

## UML Model

~~~plantuml
@startuml
hide empty members

class Account {
  +id: Integer
  +userId: Integer
  +bankName: String
  +accountType: AccountType
  +branchName: String [0..1]
  +numberCiphertext: String
  +numberFingerprint: String
  +last4: String
  +balance: Real
  +version: Integer
  +createdAt: String
}

class AccountResult {
  +success: Boolean
  +account: AccountView [0..1]
}

class AccountService {
  +create(ctx: RequestContext, cmd: CreateAccountCommand): AccountResult
}

enum AccountType {
  Checking
  Credit_Card
  Savings
  Investment
  Loan
}

class AccountVault {
  +{static} fingerprint(number: String): String
  +{static} decrypt(ciphertext: String): String
}

class AccountView {
  +id: Integer
  +last4: String
  +version: Integer
}

class BalanceAdjustment {
  +id: Integer
  +accountId: Integer
  +userId: Integer
  +oldBalance: Real
  +newBalance: Real
  +accountVersion: Integer
  +createdAt: String
}

class CreateAccountCommand {
  +bankName: String
  +accountType: AccountType
  +branchName: String [0..1]
  +fullNumber: String
  +balance: Real
}

class Numeric {
  +{static} finite(x: Real): Boolean
  +{static} scale(x: Real): Integer
}

class RequestContext {
  +userId: Integer
  +authenticated: Boolean
}

class Text {
  +{static} trim(s: String): String
  +{static} matches(s: String, pattern: String): Boolean
  +{static} last4(s: String): String
}

class User {
  +id: Integer
}

Account --> AccountType : accountType
AccountResult --> AccountView : account
CreateAccountCommand --> AccountType : accountType

@enduml
~~~

## Business Rules

~~~ocl
-- BR-UC-06-01
-- Source: Product source
context AccountService::create(ctx: RequestContext, cmd: CreateAccountCommand): AccountResult
pre BR_UC_06_01_AuthenticatedContext:
  ctx.authenticated and User.allInstances()->exists(u | u.id = ctx.userId)
~~~

~~~ocl
-- BR-UC-06-02
-- Source: Assumption
context AccountService::create(ctx: RequestContext, cmd: CreateAccountCommand): AccountResult
pre BR_UC_06_02_Text:
  Text::trim(cmd.bankName).size() > 0 and Text::trim(cmd.bankName).size() <= 255 and (cmd.branchName.oclIsUndefined() or Text::trim(cmd.branchName).size() <= 255)
~~~

~~~ocl
-- BR-UC-06-03
-- Source: Product source
context AccountService::create(ctx: RequestContext, cmd: CreateAccountCommand): AccountResult
pre BR_UC_06_03_Number:
  Text::matches(cmd.fullNumber, '^[0-9]{8,34}$')
~~~

~~~ocl
-- BR-UC-06-04
-- Source: Assumption
context AccountService::create(ctx: RequestContext, cmd: CreateAccountCommand): AccountResult
pre BR_UC_06_04_Balance:
  Numeric::finite(cmd.balance) and cmd.balance >= 0 and Numeric::scale(cmd.balance) <= 2 and cmd.balance < 10000000000000000
~~~

~~~ocl
-- BR-UC-06-05
-- Source: Product source
context AccountService::create(ctx: RequestContext, cmd: CreateAccountCommand): AccountResult
pre BR_UC_06_05_UniqueNumber:
  not Account.allInstances()->exists(a | a.userId = ctx.userId and a.numberFingerprint = AccountVault::fingerprint(cmd.fullNumber))
~~~

~~~ocl
-- BR-UC-06-06
-- Source: Product source
context AccountService::create(ctx: RequestContext, cmd: CreateAccountCommand): AccountResult
post BR_UC_06_06_LastFour:
  result.success implies result.account.last4 = Text::last4(cmd.fullNumber) and Account.allInstances()->any(a | a.id = result.account.id).last4 = Text::last4(cmd.fullNumber)
~~~

~~~ocl
-- BR-UC-06-07
-- Source: Assumption
-- Ciphertext is authenticated encryption under an external key. The keyed HMAC identifies the exact number without requiring deterministic encryption.
context AccountService::create(ctx: RequestContext, cmd: CreateAccountCommand): AccountResult
post BR_UC_06_07_ProtectedStorage:
  result.success implies Account.allInstances()->exists(a | a.id = result.account.id and AccountVault::decrypt(a.numberCiphertext) = cmd.fullNumber and a.numberCiphertext <> cmd.fullNumber and a.numberFingerprint = AccountVault::fingerprint(cmd.fullNumber))
~~~

~~~ocl
-- BR-UC-06-08
-- Source: Product source
context AccountService::create(ctx: RequestContext, cmd: CreateAccountCommand): AccountResult
post BR_UC_06_08_Projection:
  result.success implies Account.allInstances()->exists(a | a.id = result.account.id and a.userId = ctx.userId and a.bankName = Text::trim(cmd.bankName) and a.accountType = cmd.accountType and a.branchName = (if cmd.branchName.oclIsUndefined() then null else Text::trim(cmd.branchName) endif) and a.balance = cmd.balance)
~~~

~~~ocl
-- BR-UC-06-09
-- Source: Assumption
context AccountService::create(ctx: RequestContext, cmd: CreateAccountCommand): AccountResult
post BR_UC_06_09_FailureRollback:
  not result.success implies Account.allInstances()->collect(e | Tuple{id = e.id, userId = e.userId, bankName = e.bankName, accountType = e.accountType, branchName = e.branchName, numberCiphertext = e.numberCiphertext, numberFingerprint = e.numberFingerprint, last4 = e.last4, balance = e.balance, version = e.version, createdAt = e.createdAt})->asSet() = Account.allInstances()@pre->collect(e | Tuple{id = e.id@pre, userId = e.userId@pre, bankName = e.bankName@pre, accountType = e.accountType@pre, branchName = e.branchName@pre, numberCiphertext = e.numberCiphertext@pre, numberFingerprint = e.numberFingerprint@pre, last4 = e.last4@pre, balance = e.balance@pre, version = e.version@pre, createdAt = e.createdAt@pre})->asSet() and BalanceAdjustment.allInstances()->collect(e | Tuple{id = e.id, accountId = e.accountId, userId = e.userId, oldBalance = e.oldBalance, newBalance = e.newBalance, accountVersion = e.accountVersion, createdAt = e.createdAt})->asSet() = BalanceAdjustment.allInstances()@pre->collect(e | Tuple{id = e.id@pre, accountId = e.accountId@pre, userId = e.userId@pre, oldBalance = e.oldBalance@pre, newBalance = e.newBalance@pre, accountVersion = e.accountVersion@pre, createdAt = e.createdAt@pre})->asSet()
~~~

~~~ocl
-- BR-UC-06-10
-- Source: Product source
context AccountService::create(ctx: RequestContext, cmd: CreateAccountCommand): AccountResult
post BR_UC_06_10_NewAccount:
  result.success implies Account.allInstances()->size() = Account.allInstances()@pre->size() + 1 and result.account.version = 0 and Account.allInstances()->any(a | a.id = result.account.id).version = 0
~~~
