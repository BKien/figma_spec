---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-07
uc_name: "View Bank Account Details"
---

# UC-07: View Bank Account Details

## Functional Use-Case Specification

### Use Case ID

UC-07

### Use Case Name

View Bank Account Details

### Description

Inspect a financial account and its recent transactions.

### Actor(s)

Primary: Account holder. Supporting: application client and application service.

### Priority

High.

### Trigger

The user opens an account card.

### Pre-Condition(s)

PRE-1: The application view is open in the client.

### Post-Condition(s)

POST-1: On success, the client displays the returned account details and recent activity.
POST-2: On failure, the client displays a recovery message in the current view.

### Basic Flow

1. The user opens an account card.
2. The client requests account details.
3. The system returns the account and recent transaction data.
4. The client displays account details and recent transactions.

### Alternative Flow

AF-1:

1. The system returns no recent transactions.
2. The client displays the account with an empty recent-activity panel.

### Exception Flow

EF-1:

1. The system returns an operation error.
2. The client displays the error message and keeps the current view open.
3. The actor revises the interaction or retries the request.

EF-2:

1. The system returns a rejected authentication context.
2. The client presents the login entry point.

### Related UI

- Product-source UI descriptions: [Use cases rows 133-152](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A133:B152). No Figma node identifier was supplied.

### Related API IDs

- [API-ACCOUNT-DETAIL](../api/api-account-detail.md)

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

class AccountDetailQuery {
  +accountId: Integer
}

class AccountDetailResult {
  +success: Boolean
  +account: AccountView [0..1]
  +recent: Sequence(RecentTransaction)
}

class AccountService {
  +detail(ctx: RequestContext, cmd: AccountDetailQuery): AccountDetailResult
}

enum AccountType {
  Checking
  Credit_Card
  Savings
  Investment
  Loan
}

class AccountVault {
  +{static} decrypt(ciphertext: String): String
}

class AccountView {
  +id: Integer
  +bankName: String
  +accountType: AccountType
  +branchName: String [0..1]
  +fullNumber: String [0..1]
  +balance: Real
  +version: Integer
}

class CalendarDate {
  +ordinal: Integer
}

class RecentTransaction {
  +id: Integer
  +date: CalendarDate
  +amount: Real
  +description: String
  +status: TransactionStatus
  +receiptId: String [0..1]
  +type: TransactionType
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
AccountDetailResult --> AccountView : account
AccountDetailResult --> RecentTransaction : recent
AccountView --> AccountType : accountType
RecentTransaction --> CalendarDate : date
RecentTransaction --> TransactionStatus : status
RecentTransaction --> TransactionType : type
Transaction --> CalendarDate : date
Transaction --> TransactionType : type
Transaction --> TransactionStatus : status

note right of CalendarDate
  ordinal is the calendar-day index in Asia/Saigon.
end note

@enduml
~~~

## Business Rules

~~~ocl
-- BR-UC-07-01
-- Source: Product source
context AccountService::detail(ctx: RequestContext, cmd: AccountDetailQuery): AccountDetailResult
pre BR_UC_07_01_AuthenticatedContext:
  ctx.authenticated and User.allInstances()->exists(u | u.id = ctx.userId)
~~~

~~~ocl
-- BR-UC-07-02
-- Source: Product source
context AccountService::detail(ctx: RequestContext, cmd: AccountDetailQuery): AccountDetailResult
pre BR_UC_07_02_Ownership:
  Account.allInstances()->exists(a | a.id = cmd.accountId and a.userId = ctx.userId)
~~~

~~~ocl
-- BR-UC-07-03
-- Source: Product source
context AccountService::detail(ctx: RequestContext, cmd: AccountDetailQuery): AccountDetailResult
post BR_UC_07_03_AccountMapping:
  result.success implies Account.allInstances()->exists(a | a.id = result.account.id and a.id = cmd.accountId and a.userId = ctx.userId and a.bankName = result.account.bankName and a.accountType = result.account.accountType and a.branchName = result.account.branchName and a.balance = result.account.balance and a.version = result.account.version)
~~~

~~~ocl
-- BR-UC-07-04
-- Source: Product source
context AccountService::detail(ctx: RequestContext, cmd: AccountDetailQuery): AccountDetailResult
post BR_UC_07_04_FullNumber:
  result.success implies result.account.fullNumber = AccountVault::decrypt(Account.allInstances()->any(a | a.id = cmd.accountId).numberCiphertext)
~~~

~~~ocl
-- BR-UC-07-05
-- Source: Assumption
context AccountService::detail(ctx: RequestContext, cmd: AccountDetailQuery): AccountDetailResult
post BR_UC_07_05_ExactRecent:
  result.success implies let eligible : Set(Transaction) = Transaction.allInstances()->select(t | t.accountId = cmd.accountId)->asSet() in result.recent->collect(id)->asSet() = eligible->select(t | eligible->select(other | other.date.ordinal > t.date.ordinal or (other.date.ordinal = t.date.ordinal and other.id > t.id))->size() < 5)->collect(id)->asSet() and result.recent->isUnique(id)
~~~

~~~ocl
-- BR-UC-07-06
-- Source: Assumption
context AccountService::detail(ctx: RequestContext, cmd: AccountDetailQuery): AccountDetailResult
post BR_UC_07_06_RecentOrder:
  result.recent->size() <= 1 or Sequence{1..result.recent->size()-1}->forAll(i | result.recent->at(i).date.ordinal > result.recent->at(i+1).date.ordinal or (result.recent->at(i).date.ordinal = result.recent->at(i+1).date.ordinal and result.recent->at(i).id > result.recent->at(i+1).id))
~~~

~~~ocl
-- BR-UC-07-07
-- Source: Product source
context AccountService::detail(ctx: RequestContext, cmd: AccountDetailQuery): AccountDetailResult
post BR_UC_07_07_RecentProjection:
  result.recent->forAll(v | Transaction.allInstances()->exists(t | t.id = v.id and t.accountId = cmd.accountId and t.date = v.date and t.description = v.description and t.type = v.type and t.status = v.status and t.receiptId = v.receiptId and v.amount = (if t.type = TransactionType::Expense then -t.amount else t.amount endif)))
~~~

~~~ocl
-- BR-UC-07-08
-- Source: Product source
-- Equality denotes the complete persistent value snapshot, including every property, not object identity alone.
context AccountService::detail(ctx: RequestContext, cmd: AccountDetailQuery): AccountDetailResult
post BR_UC_07_08_AccountUnchanged:
  Account.allInstances()->collect(e | Tuple{id = e.id, userId = e.userId, bankName = e.bankName, accountType = e.accountType, branchName = e.branchName, numberCiphertext = e.numberCiphertext, numberFingerprint = e.numberFingerprint, last4 = e.last4, balance = e.balance, version = e.version, createdAt = e.createdAt})->asSet() = Account.allInstances()@pre->collect(e | Tuple{id = e.id@pre, userId = e.userId@pre, bankName = e.bankName@pre, accountType = e.accountType@pre, branchName = e.branchName@pre, numberCiphertext = e.numberCiphertext@pre, numberFingerprint = e.numberFingerprint@pre, last4 = e.last4@pre, balance = e.balance@pre, version = e.version@pre, createdAt = e.createdAt@pre})->asSet()
~~~

~~~ocl
-- BR-UC-07-09
-- Source: Product source
-- Equality denotes the complete persistent value snapshot, including every property, not object identity alone.
context AccountService::detail(ctx: RequestContext, cmd: AccountDetailQuery): AccountDetailResult
post BR_UC_07_09_TransactionUnchanged:
  Transaction.allInstances()->collect(e | Tuple{id = e.id, accountId = e.accountId, categoryId = e.categoryId, date = e.date, type = e.type, status = e.status, description = e.description, shopName = e.shopName, paymentMethod = e.paymentMethod, amount = e.amount, receiptId = e.receiptId, createdAt = e.createdAt})->asSet() = Transaction.allInstances()@pre->collect(e | Tuple{id = e.id@pre, accountId = e.accountId@pre, categoryId = e.categoryId@pre, date = e.date@pre, type = e.type@pre, status = e.status@pre, description = e.description@pre, shopName = e.shopName@pre, paymentMethod = e.paymentMethod@pre, amount = e.amount@pre, receiptId = e.receiptId@pre, createdAt = e.createdAt@pre})->asSet()
~~~
