---
artifact_type: business-use-case-specification
status: Frozen
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

AF-1: Display an Empty Account List

3a: The system returns an empty account list.

3b: The client displays the add-account entry point.

### Exception Flow

EF-1: Account List Operation Error

3c: The system returns an operation error.

3d: The client displays the error message and keeps the current view open.

3e: The actor revises the interaction or retries the request.

EF-2: Account List Authentication Rejected

3f: The system returns a rejected authentication context.

3g: The client presents the login entry point.

### Related UI

- Product-source UI descriptions: [Use cases rows 83-104](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A83:B104). No Figma node identifier was supplied.

### Related API IDs

- [API-ACCOUNT-LIST](../api/API-ACCOUNT-LIST.md)

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

~~~text
BR-BANK-ACCOUNTS-01 - Authenticated Context
Source: Product source
context AccountService::list(ctx: RequestContext): AccountListResult
pre BR_BANK_ACCOUNTS_01_AuthenticatedContext:
  ctx.authenticated and User.allInstances()->exists(u | u.id = ctx.userId)
~~~

~~~text
BR-BANK-ACCOUNTS-02 - User Identity
Source: Product source
context AccountService::list(ctx: RequestContext): AccountListResult
post BR_BANK_ACCOUNTS_02_UserIdentity:
  result.success implies result.userId = ctx.userId
~~~

~~~text
BR-BANK-ACCOUNTS-03 - Exact Coverage
Source: Product source
context AccountService::list(ctx: RequestContext): AccountListResult
post BR_BANK_ACCOUNTS_03_ExactCoverage:
  result.success implies result.accounts->collect(id)->asSet() = Account.allInstances()->select(a | a.userId = ctx.userId)->collect(id)->asSet()
~~~

~~~text
BR-BANK-ACCOUNTS-04 - Ordering
Source: Product source
context AccountService::list(ctx: RequestContext): AccountListResult
post BR_BANK_ACCOUNTS_04_Ordering:
  result.accounts->size() <= 1 or Sequence{1..result.accounts->size()-1}->forAll(i | result.accounts->at(i).id < result.accounts->at(i+1).id)
~~~

~~~text
BR-BANK-ACCOUNTS-05 - No Duplicates
Source: Product source
context AccountService::list(ctx: RequestContext): AccountListResult
post BR_BANK_ACCOUNTS_05_NoDuplicates:
  result.accounts->isUnique(id)
~~~

~~~text
BR-BANK-ACCOUNTS-06 - Projection
Source: Product source
context AccountService::list(ctx: RequestContext): AccountListResult
post BR_BANK_ACCOUNTS_06_Projection:
  result.accounts->forAll(v | Account.allInstances()->exists(a | a.id = v.id and a.userId = ctx.userId and a.bankName = v.bankName and a.accountType = v.accountType and a.branchName = v.branchName and a.last4 = v.last4 and a.balance = v.balance and a.version = v.version))
~~~

~~~text
BR-BANK-ACCOUNTS-07 - Number Exposure
Source: Product source
context AccountService::list(ctx: RequestContext): AccountListResult
post BR_BANK_ACCOUNTS_07_NumberExposure:
  result.accounts->forAll(v | v.fullNumber.oclIsUndefined() and v.displayNumber = '**** '.concat(v.last4))
~~~

~~~text
BR-BANK-ACCOUNTS-08 - Account Unchanged
Source: Product source
Note: Equality denotes the complete persistent value snapshot, including every property, not object identity alone.
context AccountService::list(ctx: RequestContext): AccountListResult
post BR_BANK_ACCOUNTS_08_AccountUnchanged:
  Account.allInstances()->collect(e | Tuple{id = e.id, userId = e.userId, bankName = e.bankName, accountType = e.accountType, branchName = e.branchName, numberCiphertext = e.numberCiphertext, numberFingerprint = e.numberFingerprint, last4 = e.last4, balance = e.balance, version = e.version, createdAt = e.createdAt})->asSet() = Account.allInstances()@pre->collect(e | Tuple{id = e.id@pre, userId = e.userId@pre, bankName = e.bankName@pre, accountType = e.accountType@pre, branchName = e.branchName@pre, numberCiphertext = e.numberCiphertext@pre, numberFingerprint = e.numberFingerprint@pre, last4 = e.last4@pre, balance = e.balance@pre, version = e.version@pre, createdAt = e.createdAt@pre})->asSet()
~~~
