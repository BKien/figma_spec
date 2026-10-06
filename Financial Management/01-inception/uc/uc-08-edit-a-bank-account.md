---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-08
uc_name: "Edit a Bank Account"
---

# UC-08: Edit a Bank Account

## Functional Use-Case Specification

### Use Case ID

UC-08

### Use Case Name

Edit a Bank Account

### Description

Revise account details or reconcile a manually tracked balance.

### Actor(s)

Primary: Account holder. Supporting: application client and application service.

### Priority

High.

### Trigger

The user opens an account and selects Edit.

### Pre-Condition(s)

PRE-1: The application view is open in the client.

### Post-Condition(s)

POST-1: On success, the client displays update confirmation and refreshes the account view.
POST-2: On failure, the client displays a recovery message in the current view.

### Basic Flow

1. The user opens an account and selects Edit.
2. The client requests account details and displays the edit form.
3. The user changes account fields and selects Save Changes.
4. The client sends the update request.
5. The system returns the account result.
6. The client displays confirmation and refreshes the account view.

### Alternative Flow

AF-1:

1. The user selects Edit Accounts on the Accounts page.
2. The user opens the pencil action on an account card.
3. The client requests account details and opens the edit form.
4. The user submits changes.
5. The client displays the returned result and refreshes Accounts.

### Exception Flow

EF-1:

1. The system returns an operation error.
2. The client displays the error message and keeps the current view open.
3. The actor revises the interaction or retries the request.

EF-2:

1. The system returns a rejected authentication context.
2. The client presents the login entry point.

EF-3:

1. The system returns an operation conflict.
2. The client offers to reload the current resource.
3. The user reloads the view and submits the interaction again.

### Related UI

- Product-source UI descriptions: [Use cases rows 155-200](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A155:B200). No Figma node identifier was supplied.

### Related API IDs

- [API-ACCOUNT-DETAIL](../api/api-account-detail.md)
- [API-ACCOUNT-UPDATE](../api/api-account-update.md)

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
  +update(ctx: RequestContext, cmd: UpdateAccountCommand): AccountResult
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

class CalendarDate {
  ' Only the type is referenced by this use case's Business Rules.
}

class Numeric {
  +{static} finite(x: Real): Boolean
  +{static} scale(x: Real): Integer
}

class RequestContext {
  +userId: Integer
  +authenticated: Boolean
  +now: String
}

class Text {
  +{static} trim(s: String): String
  +{static} matches(s: String, pattern: String): Boolean
  +{static} last4(s: String): String
}

class Transaction {
  +id: Integer
  +accountId: Integer
  +categoryId: Integer [0..1]
  +date: CalendarDate
  +type: TransactionType
  +status: TransactionStatus
  +description: String
  +shopName: String
  +paymentMethod: String
  +amount: Real
  +receiptId: String [0..1]
  +createdAt: String
}

enum TransactionStatus {
  Complete
  Pending
  Failed
}

enum TransactionType {
  Revenue
  Expense
}

class UpdateAccountCommand {
  +accountId: Integer
  +bankName: String
  +accountType: AccountType
  +branchName: String [0..1]
  +fullNumber: String
  +balance: Real
  +expectedVersion: Integer
}

class User {
  +id: Integer
}

Account --> AccountType : accountType
AccountResult --> AccountView : account
Transaction --> CalendarDate : date
Transaction --> TransactionType : type
Transaction --> TransactionStatus : status
UpdateAccountCommand --> AccountType : accountType

@enduml
~~~

## Business Rules

~~~ocl
-- BR-UC-08-01
-- Source: Product source
context AccountService::update(ctx: RequestContext, cmd: UpdateAccountCommand): AccountResult
pre BR_UC_08_01_AuthenticatedContext:
  ctx.authenticated and User.allInstances()->exists(u | u.id = ctx.userId)
~~~

~~~ocl
-- BR-UC-08-02
-- Source: Assumption
context AccountService::update(ctx: RequestContext, cmd: UpdateAccountCommand): AccountResult
pre BR_UC_08_02_Text:
  Text::trim(cmd.bankName).size() > 0 and Text::trim(cmd.bankName).size() <= 255 and (cmd.branchName.oclIsUndefined() or Text::trim(cmd.branchName).size() <= 255)
~~~

~~~ocl
-- BR-UC-08-03
-- Source: Product source
context AccountService::update(ctx: RequestContext, cmd: UpdateAccountCommand): AccountResult
pre BR_UC_08_03_Number:
  Text::matches(cmd.fullNumber, '^[0-9]{8,34}$')
~~~

~~~ocl
-- BR-UC-08-04
-- Source: Assumption
context AccountService::update(ctx: RequestContext, cmd: UpdateAccountCommand): AccountResult
pre BR_UC_08_04_Balance:
  Numeric::finite(cmd.balance) and cmd.balance >= 0 and Numeric::scale(cmd.balance) <= 2 and cmd.balance < 10000000000000000
~~~

~~~ocl
-- BR-UC-08-05
-- Source: Product source
context AccountService::update(ctx: RequestContext, cmd: UpdateAccountCommand): AccountResult
pre BR_UC_08_05_UniqueNumber:
  not Account.allInstances()->exists(a | a.userId = ctx.userId and a.numberFingerprint = AccountVault::fingerprint(cmd.fullNumber) and a.id <> cmd.accountId)
~~~

~~~ocl
-- BR-UC-08-06
-- Source: Product source
context AccountService::update(ctx: RequestContext, cmd: UpdateAccountCommand): AccountResult
post BR_UC_08_06_LastFour:
  result.success implies result.account.last4 = Text::last4(cmd.fullNumber) and Account.allInstances()->any(a | a.id = result.account.id).last4 = Text::last4(cmd.fullNumber)
~~~

~~~ocl
-- BR-UC-08-07
-- Source: Assumption
-- Ciphertext is authenticated encryption under an external key. The keyed HMAC identifies the exact number without requiring deterministic encryption.
context AccountService::update(ctx: RequestContext, cmd: UpdateAccountCommand): AccountResult
post BR_UC_08_07_ProtectedStorage:
  result.success implies Account.allInstances()->exists(a | a.id = result.account.id and AccountVault::decrypt(a.numberCiphertext) = cmd.fullNumber and a.numberCiphertext <> cmd.fullNumber and a.numberFingerprint = AccountVault::fingerprint(cmd.fullNumber))
~~~

~~~ocl
-- BR-UC-08-08
-- Source: Product source
context AccountService::update(ctx: RequestContext, cmd: UpdateAccountCommand): AccountResult
post BR_UC_08_08_Projection:
  result.success implies Account.allInstances()->exists(a | a.id = result.account.id and a.userId = ctx.userId and a.bankName = Text::trim(cmd.bankName) and a.accountType = cmd.accountType and a.branchName = (if cmd.branchName.oclIsUndefined() then null else Text::trim(cmd.branchName) endif) and a.balance = cmd.balance)
~~~

~~~ocl
-- BR-UC-08-09
-- Source: Assumption
context AccountService::update(ctx: RequestContext, cmd: UpdateAccountCommand): AccountResult
post BR_UC_08_09_FailureRollback:
  not result.success implies Account.allInstances()->collect(e | Tuple{id = e.id, userId = e.userId, bankName = e.bankName, accountType = e.accountType, branchName = e.branchName, numberCiphertext = e.numberCiphertext, numberFingerprint = e.numberFingerprint, last4 = e.last4, balance = e.balance, version = e.version, createdAt = e.createdAt})->asSet() = Account.allInstances()@pre->collect(e | Tuple{id = e.id@pre, userId = e.userId@pre, bankName = e.bankName@pre, accountType = e.accountType@pre, branchName = e.branchName@pre, numberCiphertext = e.numberCiphertext@pre, numberFingerprint = e.numberFingerprint@pre, last4 = e.last4@pre, balance = e.balance@pre, version = e.version@pre, createdAt = e.createdAt@pre})->asSet() and BalanceAdjustment.allInstances()->collect(e | Tuple{id = e.id, accountId = e.accountId, userId = e.userId, oldBalance = e.oldBalance, newBalance = e.newBalance, accountVersion = e.accountVersion, createdAt = e.createdAt})->asSet() = BalanceAdjustment.allInstances()@pre->collect(e | Tuple{id = e.id@pre, accountId = e.accountId@pre, userId = e.userId@pre, oldBalance = e.oldBalance@pre, newBalance = e.newBalance@pre, accountVersion = e.accountVersion@pre, createdAt = e.createdAt@pre})->asSet()
~~~

~~~ocl
-- BR-UC-08-10
-- Source: Assumption
context AccountService::update(ctx: RequestContext, cmd: UpdateAccountCommand): AccountResult
pre BR_UC_08_10_OwnedVersion:
  Account.allInstances()->exists(a | a.id = cmd.accountId and a.userId = ctx.userId and a.version = cmd.expectedVersion)
~~~

~~~ocl
-- BR-UC-08-11
-- Source: Assumption
context AccountService::update(ctx: RequestContext, cmd: UpdateAccountCommand): AccountResult
post BR_UC_08_11_VersionAdvance:
  result.success implies result.account.id = cmd.accountId and Account.allInstances()->any(a | a.id = cmd.accountId).version = cmd.expectedVersion + 1
~~~

~~~ocl
-- BR-UC-08-12
-- Source: Assumption
context AccountService::update(ctx: RequestContext, cmd: UpdateAccountCommand): AccountResult
post BR_UC_08_12_OtherAccountsPreserved:
  Account.allInstances()->select(a | a.id <> cmd.accountId)->collect(e | Tuple{id = e.id, userId = e.userId, bankName = e.bankName, accountType = e.accountType, branchName = e.branchName, numberCiphertext = e.numberCiphertext, numberFingerprint = e.numberFingerprint, last4 = e.last4, balance = e.balance, version = e.version, createdAt = e.createdAt})->asSet() = Account.allInstances()@pre->select(a | a.id <> cmd.accountId)->collect(e | Tuple{id = e.id@pre, userId = e.userId@pre, bankName = e.bankName@pre, accountType = e.accountType@pre, branchName = e.branchName@pre, numberCiphertext = e.numberCiphertext@pre, numberFingerprint = e.numberFingerprint@pre, last4 = e.last4@pre, balance = e.balance@pre, version = e.version@pre, createdAt = e.createdAt@pre})->asSet()
~~~

~~~ocl
-- BR-UC-08-13
-- Source: Assumption
-- Balance reconciliation is an audited correction; it is not revenue or an expense and never affects spending or savings reports.
context AccountService::update(ctx: RequestContext, cmd: UpdateAccountCommand): AccountResult
post BR_UC_08_13_BalanceAudit:
  result.success implies let old : Account = Account.allInstances()@pre->any(a | a.id = cmd.accountId) in (if old.balance = cmd.balance then BalanceAdjustment.allInstances()->collect(e | Tuple{id = e.id, accountId = e.accountId, userId = e.userId, oldBalance = e.oldBalance, newBalance = e.newBalance, accountVersion = e.accountVersion, createdAt = e.createdAt})->asSet() = BalanceAdjustment.allInstances()@pre->collect(e | Tuple{id = e.id@pre, accountId = e.accountId@pre, userId = e.userId@pre, oldBalance = e.oldBalance@pre, newBalance = e.newBalance@pre, accountVersion = e.accountVersion@pre, createdAt = e.createdAt@pre})->asSet() else BalanceAdjustment.allInstances()->size() = BalanceAdjustment.allInstances()@pre->size() + 1 and BalanceAdjustment.allInstances()->exists(b | b.accountId = cmd.accountId and b.userId = ctx.userId and b.oldBalance = old.balance and b.newBalance = cmd.balance and b.accountVersion = cmd.expectedVersion + 1 and b.createdAt = ctx.now) endif)
~~~

~~~ocl
-- BR-UC-08-14
-- Source: Product source
-- Equality denotes the complete persistent value snapshot, including every property, not object identity alone.
context AccountService::update(ctx: RequestContext, cmd: UpdateAccountCommand): AccountResult
post BR_UC_08_14_TransactionUnchanged:
  Transaction.allInstances()->collect(e | Tuple{id = e.id, accountId = e.accountId, categoryId = e.categoryId, date = e.date, type = e.type, status = e.status, description = e.description, shopName = e.shopName, paymentMethod = e.paymentMethod, amount = e.amount, receiptId = e.receiptId, createdAt = e.createdAt})->asSet() = Transaction.allInstances()@pre->collect(e | Tuple{id = e.id@pre, accountId = e.accountId@pre, categoryId = e.categoryId@pre, date = e.date@pre, type = e.type@pre, status = e.status@pre, description = e.description@pre, shopName = e.shopName@pre, paymentMethod = e.paymentMethod@pre, amount = e.amount@pre, receiptId = e.receiptId@pre, createdAt = e.createdAt@pre})->asSet()
~~~
