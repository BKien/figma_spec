---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-04
uc_name: "Create a Transaction"
---

# UC-04: Create a Transaction

## Functional Use-Case Specification

### Use Case ID

UC-04

### Use Case Name

Create a Transaction

### Description

Record income or an expense against a financial account.

### Actor(s)

Primary: Account holder. Supporting: application client and application service.

### Priority

High.

### Trigger

The user opens the Add Transaction form.

### Pre-Condition(s)

PRE-1: The application view is open in the client.

### Post-Condition(s)

POST-1: On success, the client displays transaction confirmation and opens history.

POST-2: On failure, the client displays a recovery message in the current view.

### Basic Flow

1. The user opens the Add Transaction form.
2. The client requests accounts and categories.
3. The system returns the form choices.
4. The user enters transaction details and submits the form.
5. The client sends the transaction request.
6. The system returns the creation result.
7. The client displays confirmation and opens transaction history.

### Alternative Flow

AF-1: Submit Without a Category

4a: The user leaves the category selection empty.

4b: The client submits the form and displays the returned result.

### Exception Flow

EF-1: Transaction Creation Operation Error

6a: The system returns an operation error.

6b: The client displays the error message and keeps the current view open.

6c: The actor revises the interaction or retries the request.

EF-2: Transaction Creation Authentication Rejected

6d: The system returns a rejected authentication context.

6e: The client presents the login entry point.

EF-3: Transaction Creation Conflict

6f: The system returns an operation conflict.

6g: The client offers to reload the current resource.

6h: The user reloads the view and submits the interaction again.

### Related UI

- Product-source UI descriptions: [Use cases rows 64-81](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A64:B81). No Figma node identifier was supplied.

### Related API IDs

- [API-TRANSACTION-CREATE](../api/API-TRANSACTION-CREATE.md)
- [API-ACCOUNT-LIST](../api/API-ACCOUNT-LIST.md)
- [API-CATEGORY-LIST](../api/API-CATEGORY-LIST.md)

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

enum AccountType {
  Checking
  Credit_Card
  Savings
  Investment
  Loan
}

class CalendarDate {
  +ordinal: Integer
}

class Category {
  +id: Integer
}

class CreateTransactionCommand {
  +accountId: Integer
  +categoryId: Integer [0..1]
  +date: CalendarDate
  +type: TransactionType
  +status: TransactionStatus
  +description: String
  +shopName: String
  +paymentMethod: String
  +amount: Real
  +expectedVersion: Integer
}

class Numeric {
  +{static} finite(x: Real): Boolean
  +{static} scale(x: Real): Integer
}

class RequestContext {
  +userId: Integer
  +authenticated: Boolean
  +today: CalendarDate
  +now: String
}

class Text {
  +{static} trim(s: String): String
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

class TransactionResult {
  +success: Boolean
  +transaction: Transaction [0..1]
}

class TransactionService {
  +create(ctx: RequestContext, cmd: CreateTransactionCommand): TransactionResult
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
CreateTransactionCommand --> CalendarDate : date
CreateTransactionCommand --> TransactionType : type
CreateTransactionCommand --> TransactionStatus : status
RequestContext --> CalendarDate : today
Transaction --> CalendarDate : date
Transaction --> TransactionType : type
Transaction --> TransactionStatus : status
TransactionResult --> Transaction : transaction

note right of CalendarDate
  ordinal is the calendar-day index in Asia/Saigon.
end note

@enduml
~~~

## Business Rules

~~~text
BR-CREATE-TRANSACTION-01 - Authenticated Context
Source: Product source
context TransactionService::create(ctx: RequestContext, cmd: CreateTransactionCommand): TransactionResult
pre BR_CREATE_TRANSACTION_01_AuthenticatedContext:
  ctx.authenticated and User.allInstances()->exists(u | u.id = ctx.userId)
~~~

~~~text
BR-CREATE-TRANSACTION-02 - Owned Account
Source: Product source
context TransactionService::create(ctx: RequestContext, cmd: CreateTransactionCommand): TransactionResult
pre BR_CREATE_TRANSACTION_02_OwnedAccount:
  Account.allInstances()->exists(a | a.id = cmd.accountId and a.userId = ctx.userId)
~~~

~~~text
BR-CREATE-TRANSACTION-03 - Exact Amount
Source: Assumption
Note: Exact decimal arithmetic; upper bound matches DECIMAL(18,2). Source positivity and precision are retained.
context TransactionService::create(ctx: RequestContext, cmd: CreateTransactionCommand): TransactionResult
pre BR_CREATE_TRANSACTION_03_ExactAmount:
  Numeric::finite(cmd.amount) and cmd.amount > 0 and Numeric::scale(cmd.amount) <= 2 and cmd.amount < 10000000000000000
~~~

~~~text
BR-CREATE-TRANSACTION-04 - Completed Date
Source: Assumption
Note: A future dated entry may be Pending/Failed; a realized cash flow cannot be future dated in this manually tracked ledger.
context TransactionService::create(ctx: RequestContext, cmd: CreateTransactionCommand): TransactionResult
pre BR_CREATE_TRANSACTION_04_CompletedDate:
  cmd.status = TransactionStatus::Complete implies cmd.date.ordinal <= ctx.today.ordinal
~~~

~~~text
BR-CREATE-TRANSACTION-05 - Text
Source: Assumption
context TransactionService::create(ctx: RequestContext, cmd: CreateTransactionCommand): TransactionResult
pre BR_CREATE_TRANSACTION_05_Text:
  Text::trim(cmd.description).size() > 0 and Text::trim(cmd.shopName).size() > 0 and Text::trim(cmd.paymentMethod).size() > 0 and Text::trim(cmd.description).size() <= 255 and Text::trim(cmd.shopName).size() <= 255 and Text::trim(cmd.paymentMethod).size() <= 100
~~~

~~~text
BR-CREATE-TRANSACTION-06 - Category
Source: Product source
context TransactionService::create(ctx: RequestContext, cmd: CreateTransactionCommand): TransactionResult
pre BR_CREATE_TRANSACTION_06_Category:
  cmd.categoryId.oclIsUndefined() or Category.allInstances()->exists(c | c.id = cmd.categoryId)
~~~

~~~text
BR-CREATE-TRANSACTION-07 - Current Version
Source: Assumption
context TransactionService::create(ctx: RequestContext, cmd: CreateTransactionCommand): TransactionResult
pre BR_CREATE_TRANSACTION_07_CurrentVersion:
  Account.allInstances()->exists(a | a.id = cmd.accountId and a.version = cmd.expectedVersion)
~~~

~~~text
BR-CREATE-TRANSACTION-08 - Funds
Source: Assumption
context TransactionService::create(ctx: RequestContext, cmd: CreateTransactionCommand): TransactionResult
pre BR_CREATE_TRANSACTION_08_Funds:
  (cmd.type = TransactionType::Expense and cmd.status = TransactionStatus::Complete) implies Account.allInstances()->exists(a | a.id = cmd.accountId and a.balance >= cmd.amount)
~~~

~~~text
BR-CREATE-TRANSACTION-09 - Revenue Balance Range
Source: Assumption
Note: Check the resulting balance before database conversion, preventing DECIMAL(18,2) overflow.
context TransactionService::create(ctx: RequestContext, cmd: CreateTransactionCommand): TransactionResult
pre BR_CREATE_TRANSACTION_09_RevenueBalanceRange:
  (cmd.type = TransactionType::Revenue and cmd.status = TransactionStatus::Complete) implies Account.allInstances()->exists(a | a.id = cmd.accountId and a.balance + cmd.amount < 10000000000000000)
~~~

~~~text
BR-CREATE-TRANSACTION-10 - Balance Effect
Source: Assumption
context TransactionService::create(ctx: RequestContext, cmd: CreateTransactionCommand): TransactionResult
post BR_CREATE_TRANSACTION_10_BalanceEffect:
  result.success implies Account.allInstances()->exists(a | a.id = cmd.accountId and a.version = a.version@pre + 1 and a.balance = a.balance@pre + (if cmd.status <> TransactionStatus::Complete then 0 else if cmd.type = TransactionType::Revenue then cmd.amount else -cmd.amount endif endif))
~~~

~~~text
BR-CREATE-TRANSACTION-11 - Exact Persistence
Source: Assumption
context TransactionService::create(ctx: RequestContext, cmd: CreateTransactionCommand): TransactionResult
post BR_CREATE_TRANSACTION_11_ExactPersistence:
  result.success implies Transaction.allInstances()->one(t | t.id = result.transaction.id and t.accountId = cmd.accountId and t.categoryId = cmd.categoryId and t.date = cmd.date and t.type = cmd.type and t.status = cmd.status and t.description = Text::trim(cmd.description) and t.shopName = Text::trim(cmd.shopName) and t.paymentMethod = Text::trim(cmd.paymentMethod) and t.amount = cmd.amount and t.createdAt = ctx.now and t.receiptId.oclIsUndefined())
~~~

~~~text
BR-CREATE-TRANSACTION-12 - Atomic Failure
Source: Product source
Note: Insertion and account version/balance write commit together; version comparison and expense balance check occur within the locked account transaction.
context TransactionService::create(ctx: RequestContext, cmd: CreateTransactionCommand): TransactionResult
post BR_CREATE_TRANSACTION_12_AtomicFailure:
  not result.success implies Transaction.allInstances()->collect(e | Tuple{id = e.id, accountId = e.accountId, categoryId = e.categoryId, date = e.date, type = e.type, status = e.status, description = e.description, shopName = e.shopName, paymentMethod = e.paymentMethod, amount = e.amount, receiptId = e.receiptId, createdAt = e.createdAt})->asSet() = Transaction.allInstances()@pre->collect(e | Tuple{id = e.id@pre, accountId = e.accountId@pre, categoryId = e.categoryId@pre, date = e.date@pre, type = e.type@pre, status = e.status@pre, description = e.description@pre, shopName = e.shopName@pre, paymentMethod = e.paymentMethod@pre, amount = e.amount@pre, receiptId = e.receiptId@pre, createdAt = e.createdAt@pre})->asSet() and Account.allInstances()->collect(e | Tuple{id = e.id, userId = e.userId, bankName = e.bankName, accountType = e.accountType, branchName = e.branchName, numberCiphertext = e.numberCiphertext, numberFingerprint = e.numberFingerprint, last4 = e.last4, balance = e.balance, version = e.version, createdAt = e.createdAt})->asSet() = Account.allInstances()@pre->collect(e | Tuple{id = e.id@pre, userId = e.userId@pre, bankName = e.bankName@pre, accountType = e.accountType@pre, branchName = e.branchName@pre, numberCiphertext = e.numberCiphertext@pre, numberFingerprint = e.numberFingerprint@pre, last4 = e.last4@pre, balance = e.balance@pre, version = e.version@pre, createdAt = e.createdAt@pre})->asSet()
~~~

~~~text
BR-CREATE-TRANSACTION-13 - Exactly One
Source: Product source
context TransactionService::create(ctx: RequestContext, cmd: CreateTransactionCommand): TransactionResult
post BR_CREATE_TRANSACTION_13_ExactlyOne:
  result.success implies Transaction.allInstances()->size() = Transaction.allInstances()@pre->size() + 1
~~~
