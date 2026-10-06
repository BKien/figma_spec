---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-09
uc_name: "Delete a Bank Account"
---

# UC-09: Delete a Bank Account

## Functional Use-Case Specification

### Use Case ID

UC-09

### Use Case Name

Delete a Bank Account

### Description

Remove a financial account and its recorded activity after confirmation.

### Actor(s)

Primary: Account holder. Supporting: application client and application service.

### Priority

High.

### Trigger

The user selects Delete on an account.

### Pre-Condition(s)

PRE-1: The application view is open in the client.

### Post-Condition(s)

POST-1: On success, the client closes the deletion dialog and refreshes Accounts.
POST-2: On failure, the client displays a recovery message in the current view.

### Basic Flow

1. The user selects Delete on an account.
2. The client displays a confirmation dialog with the account label and deletion warning.
3. The user confirms deletion.
4. The client sends the delete request.
5. The system returns the deletion result.
6. The client displays confirmation and refreshes Accounts.

### Alternative Flow

AF-1:

1. The user cancels the confirmation dialog.
2. The client closes the dialog.

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

- Product-source UI descriptions: [Use cases rows 202-219](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A202:B219). No Figma node identifier was supplied.

### Related API IDs

- [API-ACCOUNT-DELETE](../api/api-account-delete.md)

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

class AccountService {
  +delete(ctx: RequestContext, cmd: DeleteAccountCommand): DeleteResult
}

enum AccountType {
  Checking
  Credit_Card
  Savings
  Investment
  Loan
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

class DeleteAccountCommand {
  +accountId: Integer
  +expectedVersion: Integer
}

class DeleteResult {
  +success: Boolean
  +accountId: Integer
}

class RequestContext {
  +userId: Integer
  +authenticated: Boolean
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

class User {
  +id: Integer
}

Account --> AccountType : accountType
Transaction --> CalendarDate : date
Transaction --> TransactionType : type
Transaction --> TransactionStatus : status

@enduml
~~~

## Business Rules

~~~ocl
-- BR-UC-09-01
-- Source: Product source
context AccountService::delete(ctx: RequestContext, cmd: DeleteAccountCommand): DeleteResult
pre BR_UC_09_01_AuthenticatedContext:
  ctx.authenticated and User.allInstances()->exists(u | u.id = ctx.userId)
~~~

~~~ocl
-- BR-UC-09-02
-- Source: Product source
context AccountService::delete(ctx: RequestContext, cmd: DeleteAccountCommand): DeleteResult
pre BR_UC_09_02_OwnedAccount:
  Account.allInstances()->exists(a | a.id = cmd.accountId and a.userId = ctx.userId)
~~~

~~~ocl
-- BR-UC-09-03
-- Source: Assumption
context AccountService::delete(ctx: RequestContext, cmd: DeleteAccountCommand): DeleteResult
pre BR_UC_09_03_Version:
  Account.allInstances()->exists(a | a.id = cmd.accountId and a.version = cmd.expectedVersion)
~~~

~~~ocl
-- BR-UC-09-04
-- Source: Product source
context AccountService::delete(ctx: RequestContext, cmd: DeleteAccountCommand): DeleteResult
post BR_UC_09_04_AccountDeleted:
  result.success implies not Account.allInstances()->exists(a | a.id = cmd.accountId)
~~~

~~~ocl
-- BR-UC-09-05
-- Source: Product source
context AccountService::delete(ctx: RequestContext, cmd: DeleteAccountCommand): DeleteResult
post BR_UC_09_05_TransactionsDeleted:
  result.success implies not Transaction.allInstances()->exists(t | t.accountId = cmd.accountId)
~~~

~~~ocl
-- BR-UC-09-06
-- Source: Assumption
context AccountService::delete(ctx: RequestContext, cmd: DeleteAccountCommand): DeleteResult
post BR_UC_09_06_AdjustmentDeletion:
  result.success implies not BalanceAdjustment.allInstances()->exists(b | b.accountId = cmd.accountId)
~~~

~~~ocl
-- BR-UC-09-07
-- Source: Product source
context AccountService::delete(ctx: RequestContext, cmd: DeleteAccountCommand): DeleteResult
post BR_UC_09_07_OtherAccountsPreserved:
  result.success implies Account.allInstances()->select(a | a.id <> cmd.accountId)->collect(e | Tuple{id = e.id, userId = e.userId, bankName = e.bankName, accountType = e.accountType, branchName = e.branchName, numberCiphertext = e.numberCiphertext, numberFingerprint = e.numberFingerprint, last4 = e.last4, balance = e.balance, version = e.version, createdAt = e.createdAt})->asSet() = Account.allInstances()@pre->select(a | a.id <> cmd.accountId)->collect(e | Tuple{id = e.id@pre, userId = e.userId@pre, bankName = e.bankName@pre, accountType = e.accountType@pre, branchName = e.branchName@pre, numberCiphertext = e.numberCiphertext@pre, numberFingerprint = e.numberFingerprint@pre, last4 = e.last4@pre, balance = e.balance@pre, version = e.version@pre, createdAt = e.createdAt@pre})->asSet() and Transaction.allInstances()->select(t | t.accountId <> cmd.accountId)->collect(e | Tuple{id = e.id, accountId = e.accountId, categoryId = e.categoryId, date = e.date, type = e.type, status = e.status, description = e.description, shopName = e.shopName, paymentMethod = e.paymentMethod, amount = e.amount, receiptId = e.receiptId, createdAt = e.createdAt})->asSet() = Transaction.allInstances()@pre->select(t | t.accountId <> cmd.accountId)->collect(e | Tuple{id = e.id@pre, accountId = e.accountId@pre, categoryId = e.categoryId@pre, date = e.date@pre, type = e.type@pre, status = e.status@pre, description = e.description@pre, shopName = e.shopName@pre, paymentMethod = e.paymentMethod@pre, amount = e.amount@pre, receiptId = e.receiptId@pre, createdAt = e.createdAt@pre})->asSet()
~~~

~~~ocl
-- BR-UC-09-08
-- Source: Product source
-- Delete uses one database transaction with account version comparison, child deletion and account deletion.
context AccountService::delete(ctx: RequestContext, cmd: DeleteAccountCommand): DeleteResult
post BR_UC_09_08_AtomicFailure:
  not result.success implies Account.allInstances()->collect(e | Tuple{id = e.id, userId = e.userId, bankName = e.bankName, accountType = e.accountType, branchName = e.branchName, numberCiphertext = e.numberCiphertext, numberFingerprint = e.numberFingerprint, last4 = e.last4, balance = e.balance, version = e.version, createdAt = e.createdAt})->asSet() = Account.allInstances()@pre->collect(e | Tuple{id = e.id@pre, userId = e.userId@pre, bankName = e.bankName@pre, accountType = e.accountType@pre, branchName = e.branchName@pre, numberCiphertext = e.numberCiphertext@pre, numberFingerprint = e.numberFingerprint@pre, last4 = e.last4@pre, balance = e.balance@pre, version = e.version@pre, createdAt = e.createdAt@pre})->asSet() and Transaction.allInstances()->collect(e | Tuple{id = e.id, accountId = e.accountId, categoryId = e.categoryId, date = e.date, type = e.type, status = e.status, description = e.description, shopName = e.shopName, paymentMethod = e.paymentMethod, amount = e.amount, receiptId = e.receiptId, createdAt = e.createdAt})->asSet() = Transaction.allInstances()@pre->collect(e | Tuple{id = e.id@pre, accountId = e.accountId@pre, categoryId = e.categoryId@pre, date = e.date@pre, type = e.type@pre, status = e.status@pre, description = e.description@pre, shopName = e.shopName@pre, paymentMethod = e.paymentMethod@pre, amount = e.amount@pre, receiptId = e.receiptId@pre, createdAt = e.createdAt@pre})->asSet() and BalanceAdjustment.allInstances()->collect(e | Tuple{id = e.id, accountId = e.accountId, userId = e.userId, oldBalance = e.oldBalance, newBalance = e.newBalance, accountVersion = e.accountVersion, createdAt = e.createdAt})->asSet() = BalanceAdjustment.allInstances()@pre->collect(e | Tuple{id = e.id@pre, accountId = e.accountId@pre, userId = e.userId@pre, oldBalance = e.oldBalance@pre, newBalance = e.newBalance@pre, accountVersion = e.accountVersion@pre, createdAt = e.createdAt@pre})->asSet()
~~~

~~~ocl
-- BR-UC-09-09
-- Source: Product source
context AccountService::delete(ctx: RequestContext, cmd: DeleteAccountCommand): DeleteResult
post BR_UC_09_09_ResponseIdentity:
  result.success implies result.accountId = cmd.accountId
~~~
