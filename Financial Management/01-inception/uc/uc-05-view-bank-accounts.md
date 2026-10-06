---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-05
uc_name: "View Bank Accounts"
---

# UC-05: View Bank Accounts

## Functional Use-Case Specification

### Use Case ID

UC-05

### Use Case Name

View Bank Accounts

### Description

Review financial account cards.

### Actor(s)

Primary: Account holder. Supporting: application client and application service.

### Priority

High.

### Trigger

The user opens the Accounts page.

### Pre-Condition(s)

PRE-1: The application view is open in the client.

### Post-Condition(s)

POST-1: On success, the client displays account cards or the empty-account view.
POST-2: On failure, the client displays a recovery message in the current view.

### Basic Flow

1. The user opens the Accounts page.
2. The client requests accounts.
3. The system returns account cards.
4. The client displays account names, types, number labels, and balances.

### Alternative Flow

AF-1:

1. The system returns an empty account list.
2. The client displays the add-account entry point.

### Exception Flow

EF-1:

1. The system returns an operation error.
2. The client displays the error message and keeps the current view open.
3. The actor revises the interaction or retries the request.

EF-2:

1. The system returns a rejected authentication context.
2. The client presents the login entry point.

### Related UI

- Product-source UI descriptions: [Use cases rows 83-104](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A83:B104). No Figma node identifier was supplied.

### Related API IDs

- [API-ACCOUNT-LIST](../api/api-account-list.md)

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

class AccountListResult {
  +success: Boolean
  +userId: Integer
  +accounts: Sequence(AccountView)
}

class AccountService {
  +list(ctx: RequestContext): AccountListResult
}

enum AccountType {
  Checking
  Credit_Card
  Savings
  Investment
  Loan
}

class AccountView {
  +id: Integer
  +bankName: String
  +accountType: AccountType
  +branchName: String [0..1]
  +fullNumber: String [0..1]
  +last4: String
  +displayNumber: String
  +balance: Real
  +version: Integer
}

class RequestContext {
  +userId: Integer
  +authenticated: Boolean
}

class User {
  +id: Integer
}

Account --> AccountType : accountType
AccountListResult --> AccountView : accounts
AccountView --> AccountType : accountType

@enduml
~~~

## Business Rules

~~~ocl
-- BR-UC-05-01
-- Source: Product source
context AccountService::list(ctx: RequestContext): AccountListResult
pre BR_UC_05_01_AuthenticatedContext:
  ctx.authenticated and User.allInstances()->exists(u | u.id = ctx.userId)
~~~

~~~ocl
-- BR-UC-05-02
-- Source: Product source
context AccountService::list(ctx: RequestContext): AccountListResult
post BR_UC_05_02_UserIdentity:
  result.success implies result.userId = ctx.userId
~~~

~~~ocl
-- BR-UC-05-03
-- Source: Product source
context AccountService::list(ctx: RequestContext): AccountListResult
post BR_UC_05_03_ExactCoverage:
  result.success implies result.accounts->collect(id)->asSet() = Account.allInstances()->select(a | a.userId = ctx.userId)->collect(id)->asSet()
~~~

~~~ocl
-- BR-UC-05-04
-- Source: Product source
context AccountService::list(ctx: RequestContext): AccountListResult
post BR_UC_05_04_Ordering:
  result.accounts->size() <= 1 or Sequence{1..result.accounts->size()-1}->forAll(i | result.accounts->at(i).id < result.accounts->at(i+1).id)
~~~

~~~ocl
-- BR-UC-05-05
-- Source: Product source
context AccountService::list(ctx: RequestContext): AccountListResult
post BR_UC_05_05_NoDuplicates:
  result.accounts->isUnique(id)
~~~

~~~ocl
-- BR-UC-05-06
-- Source: Product source
context AccountService::list(ctx: RequestContext): AccountListResult
post BR_UC_05_06_Projection:
  result.accounts->forAll(v | Account.allInstances()->exists(a | a.id = v.id and a.userId = ctx.userId and a.bankName = v.bankName and a.accountType = v.accountType and a.branchName = v.branchName and a.last4 = v.last4 and a.balance = v.balance and a.version = v.version))
~~~

~~~ocl
-- BR-UC-05-07
-- Source: Product source
context AccountService::list(ctx: RequestContext): AccountListResult
post BR_UC_05_07_NumberExposure:
  result.accounts->forAll(v | v.fullNumber.oclIsUndefined() and v.displayNumber = '**** '.concat(v.last4))
~~~

~~~ocl
-- BR-UC-05-08
-- Source: Product source
-- Equality denotes the complete persistent value snapshot, including every property, not object identity alone.
context AccountService::list(ctx: RequestContext): AccountListResult
post BR_UC_05_08_AccountUnchanged:
  Account.allInstances()->collect(e | Tuple{id = e.id, userId = e.userId, bankName = e.bankName, accountType = e.accountType, branchName = e.branchName, numberCiphertext = e.numberCiphertext, numberFingerprint = e.numberFingerprint, last4 = e.last4, balance = e.balance, version = e.version, createdAt = e.createdAt})->asSet() = Account.allInstances()@pre->collect(e | Tuple{id = e.id@pre, userId = e.userId@pre, bankName = e.bankName@pre, accountType = e.accountType@pre, branchName = e.branchName@pre, numberCiphertext = e.numberCiphertext@pre, numberFingerprint = e.numberFingerprint@pre, last4 = e.last4@pre, balance = e.balance@pre, version = e.version@pre, createdAt = e.createdAt@pre})->asSet()
~~~
