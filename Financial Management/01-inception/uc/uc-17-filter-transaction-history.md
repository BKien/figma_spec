---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-17
uc_name: "Filter Transaction History"
---

# UC-17: Filter Transaction History

## Functional Use-Case Specification

### Use Case ID

UC-17

### Use Case Name

Filter Transaction History

### Description

Narrow transaction history to revenue or expenses and return to the combined view.

### Actor(s)

Primary: Account holder. Supporting: application client and application service.

### Priority

High.

### Trigger

The user selects a transaction type filter.

### Pre-Condition(s)

PRE-1: The application view is open in the client.

### Post-Condition(s)

POST-1: On success, the client replaces transaction rows and page controls for the selected filter.
POST-2: On failure, the client displays a recovery message in the current view.

### Basic Flow

1. The user selects a transaction type filter.
2. The client requests history for the selected filter.
3. The system returns the matching transaction page.
4. The client replaces the displayed rows and page controls.

### Alternative Flow

AF-1:

1. The user selects All.
2. The client requests and displays the combined transaction view.

### Exception Flow

EF-1:

1. The system returns an operation error.
2. The client displays the error message and keeps the current view open.
3. The actor revises the interaction or retries the request.

EF-2:

1. The system returns a rejected authentication context.
2. The client presents the login entry point.

### Related UI

- Product-source UI descriptions: [Use cases rows 45-62](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A45:B62). No Figma node identifier was supplied.

### Related API IDs

- [API-TRANSACTION-LIST](../api/api-transaction-list.md)

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
  +filter(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
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

~~~ocl
-- BR-UC-17-01
-- Source: Product source
context TransactionService::filter(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
pre BR_UC_17_01_AuthenticatedContext:
  ctx.authenticated and User.allInstances()->exists(u | u.id = ctx.userId)
~~~

~~~ocl
-- BR-UC-17-02
-- Source: Assumption
context TransactionService::filter(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
pre BR_UC_17_02_PageBounds:
  cmd.limit > 0 and cmd.limit <= 100 and cmd.offset >= 0
~~~

~~~ocl
-- BR-UC-17-03
-- Source: Product source
context TransactionService::filter(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
post BR_UC_17_03_ScopedPage:
  result.success implies result.data->forAll(t | Account.allInstances()->exists(a | a.id = t.accountId and a.userId = ctx.userId) and (cmd.type = TransactionFilter::All or (cmd.type = TransactionFilter::Revenue and t.type = TransactionType::Revenue) or (cmd.type = TransactionFilter::Expense and t.type = TransactionType::Expense)))
~~~

~~~ocl
-- BR-UC-17-04
-- Source: Product source
context TransactionService::filter(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
post BR_UC_17_04_ExactTotal:
  result.success implies result.total = Transaction.allInstances()->select(t | Account.allInstances()->exists(a | a.id = t.accountId and a.userId = ctx.userId) and (cmd.type = TransactionFilter::All or (cmd.type = TransactionFilter::Revenue and t.type = TransactionType::Revenue) or (cmd.type = TransactionFilter::Expense and t.type = TransactionType::Expense)))->size()
~~~

~~~ocl
-- BR-UC-17-05
-- Source: Assumption
context TransactionService::filter(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
post BR_UC_17_05_OrderedPage:
  result.data->size() <= 1 or Sequence{1..result.data->size()-1}->forAll(i | result.data->at(i).date.ordinal > result.data->at(i+1).date.ordinal or (result.data->at(i).date.ordinal = result.data->at(i+1).date.ordinal and result.data->at(i).id > result.data->at(i+1).id))
~~~

~~~ocl
-- BR-UC-17-06
-- Source: Assumption
context TransactionService::filter(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
post BR_UC_17_06_ExactPage:
  result.success implies let eligible : Set(Transaction) = Transaction.allInstances()->select(t | Account.allInstances()->exists(a | a.id = t.accountId and a.userId = ctx.userId) and (cmd.type = TransactionFilter::All or (cmd.type = TransactionFilter::Revenue and t.type = TransactionType::Revenue) or (cmd.type = TransactionFilter::Expense and t.type = TransactionType::Expense)))->asSet() in result.data->collect(id)->asSet() = eligible->select(t | eligible->select(other | other.date.ordinal > t.date.ordinal or (other.date.ordinal = t.date.ordinal and other.id > t.id))->size() >= cmd.offset and eligible->select(other | other.date.ordinal > t.date.ordinal or (other.date.ordinal = t.date.ordinal and other.id > t.id))->size() < cmd.offset + cmd.limit)->collect(id)->asSet()
~~~

~~~ocl
-- BR-UC-17-07
-- Source: Product source
context TransactionService::filter(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
post BR_UC_17_07_HasMore:
  result.success implies result.hasMore = (cmd.offset + result.data->size() < result.total)
~~~

~~~ocl
-- BR-UC-17-08
-- Source: Product source
context TransactionService::filter(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
post BR_UC_17_08_NoDuplicates:
  result.data->isUnique(id)
~~~

~~~ocl
-- BR-UC-17-09
-- Source: Product source
-- Equality denotes the complete persistent value snapshot, including every property, not object identity alone.
context TransactionService::filter(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
post BR_UC_17_09_TransactionUnchanged:
  Transaction.allInstances()->collect(e | Tuple{id = e.id, accountId = e.accountId, categoryId = e.categoryId, date = e.date, type = e.type, status = e.status, description = e.description, shopName = e.shopName, paymentMethod = e.paymentMethod, amount = e.amount, receiptId = e.receiptId, createdAt = e.createdAt})->asSet() = Transaction.allInstances()@pre->collect(e | Tuple{id = e.id@pre, accountId = e.accountId@pre, categoryId = e.categoryId@pre, date = e.date@pre, type = e.type@pre, status = e.status@pre, description = e.description@pre, shopName = e.shopName@pre, paymentMethod = e.paymentMethod@pre, amount = e.amount@pre, receiptId = e.receiptId@pre, createdAt = e.createdAt@pre})->asSet()
~~~

~~~ocl
-- BR-UC-17-10
-- Source: Product source
-- Equality denotes the complete persistent value snapshot, including every property, not object identity alone.
context TransactionService::filter(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
post BR_UC_17_10_AccountUnchanged:
  Account.allInstances()->collect(e | Tuple{id = e.id, userId = e.userId, bankName = e.bankName, accountType = e.accountType, branchName = e.branchName, numberCiphertext = e.numberCiphertext, numberFingerprint = e.numberFingerprint, last4 = e.last4, balance = e.balance, version = e.version, createdAt = e.createdAt})->asSet() = Account.allInstances()@pre->collect(e | Tuple{id = e.id@pre, userId = e.userId@pre, bankName = e.bankName@pre, accountType = e.accountType@pre, branchName = e.branchName@pre, numberCiphertext = e.numberCiphertext@pre, numberFingerprint = e.numberFingerprint@pre, last4 = e.last4@pre, balance = e.balance@pre, version = e.version@pre, createdAt = e.createdAt@pre})->asSet()
~~~

~~~ocl
-- BR-UC-17-11
-- Source: Assumption
-- Changing the type filter resets the initial page. Subsequent pages use View Transaction History.
context TransactionService::filter(ctx: RequestContext, cmd: TransactionQuery): TransactionListResult
pre BR_UC_17_11_ResetPagination:
  cmd.offset = 0
~~~
