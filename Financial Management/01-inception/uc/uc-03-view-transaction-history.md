---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-03
uc_name: "View Transaction History"
---

# UC-03: View Transaction History

## Functional Use-Case Specification

### Use Case ID

UC-03

### Use Case Name

View Transaction History

### Description

Review the recorded transactions and open additional pages.

### Actor(s)

Primary: Account holder. Supporting: application client and application service.

### Priority

High.

### Trigger

The user opens the Transactions page.

### Pre-Condition(s)

PRE-1: The application view is open in the client.

### Post-Condition(s)

POST-1: On success, the client displays the returned transaction rows and page controls.

POST-2: On failure, the client displays a recovery message in the current view.

### Basic Flow

1. The user opens the Transactions page.
2. The client requests transaction history.
3. The system returns the transaction page.
4. The client displays transaction rows and page controls.
5. The user opens another page.
6. The client requests and displays the returned page.

### Alternative Flow

AF-1: Display Empty Transaction History

3a: The system returns an empty page.

3b: The client displays the empty-history state.

### Exception Flow

EF-1: Transaction History Operation Error

3c: The system returns an operation error.

3d: The client displays the error message and keeps the current view open.

3e: The actor revises the interaction or retries the request.

EF-2: Transaction History Authentication Rejected

3f: The system returns a rejected authentication context.

3g: The client presents the login entry point.

### Related UI

- Product-source UI descriptions: [Use cases rows 45-62](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A45:B62). No Figma node identifier was supplied.

### Related API IDs

- [API-TRANSACTION-LIST](../api/API-TRANSACTION-LIST.md)

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

enum TransactionFilter {
  All
  Revenue
  Expense
}

class TransactionListResult {
  +success: Boolean
  +data: Sequence(Transaction)
  +total: Integer
  +hasMore: Boolean
}

class TransactionQuery {
  +type: TransactionFilter
  +limit: Integer
  +offset: Integer
}

class TransactionService {
  +list(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
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
TransactionListResult --> Transaction : data
TransactionQuery --> TransactionFilter : type

note right of CalendarDate
  ordinal is the calendar-day index in Asia/Saigon.
end note

@enduml
~~~

## Business Rules

~~~text
BR-TRANSACTION-HISTORY-01 - Authenticated Context
Source: Product source
context TransactionService::list(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
pre BR_TRANSACTION_HISTORY_01_AuthenticatedContext:
  ctx.authenticated and User.allInstances()->exists(u | u.id = ctx.userId)
~~~

~~~text
BR-TRANSACTION-HISTORY-02 - Page Bounds
Source: Assumption
context TransactionService::list(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
pre BR_TRANSACTION_HISTORY_02_PageBounds:
  cmd.limit > 0 and cmd.limit <= 100 and cmd.offset >= 0
~~~

~~~text
BR-TRANSACTION-HISTORY-03 - Scoped Page
Source: Product source
context TransactionService::list(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
post BR_TRANSACTION_HISTORY_03_ScopedPage:
  result.success implies result.data->forAll(t | Account.allInstances()->exists(a | a.id = t.accountId and a.userId = ctx.userId) and (cmd.type = TransactionFilter::All or (cmd.type = TransactionFilter::Revenue and t.type = TransactionType::Revenue) or (cmd.type = TransactionFilter::Expense and t.type = TransactionType::Expense)))
~~~

~~~text
BR-TRANSACTION-HISTORY-04 - Exact Total
Source: Product source
context TransactionService::list(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
post BR_TRANSACTION_HISTORY_04_ExactTotal:
  result.success implies result.total = Transaction.allInstances()->select(t | Account.allInstances()->exists(a | a.id = t.accountId and a.userId = ctx.userId) and (cmd.type = TransactionFilter::All or (cmd.type = TransactionFilter::Revenue and t.type = TransactionType::Revenue) or (cmd.type = TransactionFilter::Expense and t.type = TransactionType::Expense)))->size()
~~~

~~~text
BR-TRANSACTION-HISTORY-05 - Ordered Page
Source: Assumption
context TransactionService::list(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
post BR_TRANSACTION_HISTORY_05_OrderedPage:
  result.data->size() <= 1 or Sequence{1..result.data->size()-1}->forAll(i | result.data->at(i).date.ordinal > result.data->at(i+1).date.ordinal or (result.data->at(i).date.ordinal = result.data->at(i+1).date.ordinal and result.data->at(i).id > result.data->at(i+1).id))
~~~

~~~text
BR-TRANSACTION-HISTORY-06 - Exact Page
Source: Assumption
context TransactionService::list(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
post BR_TRANSACTION_HISTORY_06_ExactPage:
  result.success implies let eligible : Set(Transaction) = Transaction.allInstances()->select(t | Account.allInstances()->exists(a | a.id = t.accountId and a.userId = ctx.userId) and (cmd.type = TransactionFilter::All or (cmd.type = TransactionFilter::Revenue and t.type = TransactionType::Revenue) or (cmd.type = TransactionFilter::Expense and t.type = TransactionType::Expense)))->asSet() in result.data->collect(id)->asSet() = eligible->select(t | eligible->select(other | other.date.ordinal > t.date.ordinal or (other.date.ordinal = t.date.ordinal and other.id > t.id))->size() >= cmd.offset and eligible->select(other | other.date.ordinal > t.date.ordinal or (other.date.ordinal = t.date.ordinal and other.id > t.id))->size() < cmd.offset + cmd.limit)->collect(id)->asSet()
~~~

~~~text
BR-TRANSACTION-HISTORY-07 - Has More
Source: Product source
context TransactionService::list(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
post BR_TRANSACTION_HISTORY_07_HasMore:
  result.success implies result.hasMore = (cmd.offset + result.data->size() < result.total)
~~~

~~~text
BR-TRANSACTION-HISTORY-08 - No Duplicates
Source: Product source
context TransactionService::list(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
post BR_TRANSACTION_HISTORY_08_NoDuplicates:
  result.data->isUnique(id)
~~~

~~~text
BR-TRANSACTION-HISTORY-09 - Transaction Unchanged
Source: Product source
Note: Equality denotes the complete persistent value snapshot, including every property, not object identity alone.
context TransactionService::list(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
post BR_TRANSACTION_HISTORY_09_TransactionUnchanged:
  Transaction.allInstances()->collect(e | Tuple{id = e.id, accountId = e.accountId, categoryId = e.categoryId, date = e.date, type = e.type, status = e.status, description = e.description, shopName = e.shopName, paymentMethod = e.paymentMethod, amount = e.amount, receiptId = e.receiptId, createdAt = e.createdAt})->asSet() = Transaction.allInstances()@pre->collect(e | Tuple{id = e.id@pre, accountId = e.accountId@pre, categoryId = e.categoryId@pre, date = e.date@pre, type = e.type@pre, status = e.status@pre, description = e.description@pre, shopName = e.shopName@pre, paymentMethod = e.paymentMethod@pre, amount = e.amount@pre, receiptId = e.receiptId@pre, createdAt = e.createdAt@pre})->asSet()
~~~

~~~text
BR-TRANSACTION-HISTORY-10 - Account Unchanged
Source: Product source
Note: Equality denotes the complete persistent value snapshot, including every property, not object identity alone.
context TransactionService::list(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
post BR_TRANSACTION_HISTORY_10_AccountUnchanged:
  Account.allInstances()->collect(e | Tuple{id = e.id, userId = e.userId, bankName = e.bankName, accountType = e.accountType, branchName = e.branchName, numberCiphertext = e.numberCiphertext, numberFingerprint = e.numberFingerprint, last4 = e.last4, balance = e.balance, version = e.version, createdAt = e.createdAt})->asSet() = Account.allInstances()@pre->collect(e | Tuple{id = e.id@pre, userId = e.userId@pre, bankName = e.bankName@pre, accountType = e.accountType@pre, branchName = e.branchName@pre, numberCiphertext = e.numberCiphertext@pre, numberFingerprint = e.numberFingerprint@pre, last4 = e.last4@pre, balance = e.balance@pre, version = e.version@pre, createdAt = e.createdAt@pre})->asSet()
~~~
