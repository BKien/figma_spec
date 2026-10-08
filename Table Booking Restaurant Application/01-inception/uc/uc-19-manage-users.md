---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-19
uc_name: "Manage Users"
---

# UC-19: Manage Users

## Functional Use-Case Specification

### Use Case ID

UC-19

### Use Case Name

Manage Users

### Description

A super admin reviews users and edits a user record.

### Actor(s)

Super Admin; client; system.

### Priority

P0.

### Trigger

The admin opens Users.

### Pre-Condition(s)

PRE-1: The user administration view is visible.

### Post-Condition(s)

POST-1: The client displays the updated user record.

### Basic Flow

1. The admin opens the Users table.
2. The client requests user rows.
3. The system returns user summaries.
4. The admin opens a user edit form and submits changes.
5. The client sends the update request.
6. The system returns the user outcome.
7. The client refreshes the user row.

### Alternative Flow

AF-1: Close User Edit Form

4a: The admin closes the edit form and returns to the Users table.

### Exception Flow

EF-1: User Update Error

6a: The client displays the returned update error and keeps the form available.

### Related UI

- [Users](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=1016-4816) (1016:4816)
- [User edit](https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=1000-4208) (1000:4208)

### Related API IDs

- [API-ADMIN-USER-UPDATE](../api/API-ADMIN-USER-UPDATE.md)
- [API-ADMIN-USER-LIST](../api/API-ADMIN-USER-LIST.md)

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

enum Role {
  CUSTOMER
  MANAGER
  SUPER_ADMIN
}

class Account {
  +id: String
  +emailCanonical: String
  +displayName: String
  +status: AccountStatus
  +version: Integer
}

class UserCommand {
  +accountId: String
  +displayName: String
  +status: AccountStatus
  +version: Integer
}

class AdminService {
  +updateUser(command: UserCommand): Account
  +users(): Sequence(Account)
}

class RequestContext <<utility>> {
  +{static} role: Role
}

Account --> "1" AccountStatus : status
UserCommand --> "1" AccountStatus : status
RequestContext --> "1" Role : role

@enduml
~~~

## Business Rules

~~~text
BR-MANAGE-USERS-01 - Only Super Admin May Edit User
Source: Assumption
context AdminService::updateUser(command: UserCommand): Account
pre BR_MANAGE_USERS_01_OnlySuperAdminMayEditUser:
  RequestContext::role = Role::SUPER_ADMIN
~~~
~~~text
BR-MANAGE-USERS-02 - User Version Matches
Source: Assumption
context AdminService::updateUser(command: UserCommand): Account
pre BR_MANAGE_USERS_02_UserVersionMatches:
  Account.allInstances()->exists(a | a.id = command.accountId and a.version = command.version)
~~~
~~~text
BR-MANAGE-USERS-03 - User Version Advances
Source: Assumption
context AdminService::updateUser(command: UserCommand): Account
post BR_MANAGE_USERS_03_UserVersionAdvances:
  result.id = command.accountId and result.version = command.version + 1
~~~
~~~text
BR-MANAGE-USERS-04 - Only Super Admin May List Users
Source: Assumption
context AdminService::users(): Sequence(Account)
pre BR_MANAGE_USERS_04_OnlySuperAdminMayListUsers:
  RequestContext::role = Role::SUPER_ADMIN
~~~
~~~text
BR-MANAGE-USERS-05 - Edited User Fields Are Saved
Source: Assumption
context AdminService::updateUser(command: UserCommand): Account
post BR_MANAGE_USERS_05_EditedUserFieldsAreSaved:
  result.displayName = command.displayName and result.status = command.status
~~~
~~~text
BR-MANAGE-USERS-06 - Edited Display Name Is Present
Source: Assumption
context AdminService::updateUser(command: UserCommand): Account
pre BR_MANAGE_USERS_06_EditedDisplayNameIsPresent:
  command.displayName.trim().size() > 0
~~~
~~~text
BR-MANAGE-USERS-07 - User Email Is Preserved
Source: Assumption
context AdminService::updateUser(command: UserCommand): Account
post BR_MANAGE_USERS_07_UserEmailIsPreserved:
  result.emailCanonical = result.emailCanonical@pre
~~~
