# Source snapshot: Use cases

Spreadsheet: https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit

Retrieved: 2026-09-30 (Asia/Saigon)

## Row 1

Column A:

USE CASE SPECIFICATIONS

## Row 2

Column A:

Utility Function Definitions (for Business Rules):

StringNormalizer.trim(s):
- Removes leading and trailing whitespace characters from s.
- Internal whitespace characters remain unchanged.

StringNormalizer.nfc(s):
- Returns the Unicode NFC-normalized representation of s.
- Used to normalize user-provided text before validation and persistence.

StringNormalizer.lower(s):
- Returns the lowercase representation of s.
- Used for case-insensitive comparison, especially email normalization.


StringValidator.matches(s, pattern):
- Returns true if s fully matches the specified regular expression pattern.
- Partial matching is not allowed.


EmailValidator.isEmail(email):
- Returns true if the input value follows a valid email format.
- Used to validate email fields before processing.


PasswordHasher.matches(password, hash):
- Returns true if the provided plaintext password matches the stored password hash.
- Plaintext password shall never be stored or returned.

PasswordHasher.cost(hash):
- Returns the cost factor used to generate the password hash.
- Used to validate password hashing configuration.


DateUtility.toIsoDate(date):
- Converts a date value into ISO date string format (YYYY-MM-DD).
- Used for date comparison and API response formatting.

NumericUtility.round2(value):
- Returns value rounded to exactly two decimal places.
- Rounding uses HALF_UP semantics.
- Used to normalize monetary values, percentages, and other decimal values before comparison or inclusion in API responses.

' =========================
' Utility Classes
' =========================

class StringNormalizer <<Utility>> {
  +trim(s: String): String
  +nfc(s: String): String
  +lower(s: String): String
}


class StringValidator <<Utility>> {
  +matches(s: String, pattern: String): Boolean
}


class EmailValidator <<Utility>> {
  +isEmail(email: String): Boolean
}


class DateUtility <<Utility>> {
  +toIsoDate(date: Date): String
  +isWithinInclusiveMonth(
      date: Date,
      month: String
  ): Boolean
}


class NumericUtility <<Utility>> {
  +round2(value: Real): Real
}


class PasswordHasher <<Service>> {
  +hash(
      password: String,
      rounds: Integer
  ): String

  +matches(
      password: String,
      hash: String
  ): Boolean

  +cost(
      hash: String
  ): Integer
}

DateUtility.isWithinInclusiveMonth(date, month):
- Returns true if the date belongs to the specified month.
- The target month follows the YYYY-MM format.

## Row 5

Column A:

UC-01 - Register an Account

## Row 6

Column A:

Use Case ID

Column B:

UC-01

## Row 7

Column A:

Use Case Name

Column B:

Register an Account

## Row 8

Column A:

Description

Column B:

As a visitor, I want to register with my full name, email address, password, and password confirmation so that the application creates an authenticated user session.

## Row 9

Column A:

Actor(s)

Column B:

Visitor

## Row 10

Column A:

Priority

Column B:

Not Specified

## Row 11

Column A:

Trigger

Column B:

The visitor opens the registration page or selects the Create an account link.

## Row 12

Column A:

Pre-Condition(s)

Column B:

PRE-1: The frontend registration route /register is accessible.
PRE-2: The backend and database are available.

## Row 13

Column A:

Post-Condition(s)

Column B:

POST-1: On success, a new user record is stored with a generated unique username, a bcrypt password hash, and totalBalance = 0.
POST-2: A JWT and mapped user object are stored in localStorage.
POST-3: The frontend authentication context contains the new user and navigates to /.
POST-4: On failure, no authenticated frontend state is created.

## Row 14

Column A:

Basic Flow

Column B:

1. The visitor opens /register.
2. The frontend displays SignUpForm.
3. The visitor enters fullName, email, password, and confirmPassword.
4. The visitor selects Sign Up.
5. The frontend validates the submitted data according to BR-REG-01, BR-REG-02, BR-REG-04, BR-REG-05, and BR-REG-06.
6. The frontend sends POST /api/auth/register.
7. The backend normalizes the input and independently enforces all applicable registration rules.
8. AuthService verifies password equality and checks whether the email already exists.
9. AuthService generates a unique username from the email prefix, hashes the password with bcrypt using 10 salt rounds, and stores the user with totalBalance = 0.
10. AuthService creates the registered user result and signs a JWT. The backend returns success, message, and a data object containing accessToken and the created user's id, fullName, and email.
11. AuthContext reads data.accessToken and data.user, maps the returned user, stores the token and user in localStorage, and updates its user state.
12. The frontend navigates to /.

## Row 15

Column A:

Alternative Flow

Column B:

AF-1: Client-side validation failure
5a. If any required field is empty, the email format is invalid, or the passwords differ, the frontend displays a field-level error and does not call the API.

AF-2: Duplicate email
8a. If the email already exists, the backend returns HTTP 409 and the frontend displays the returned error.

## Row 16

Column A:

Exception Flow

Column B:

EF-1: Registration request failure
6a. If the request fails for another reason, SignUpForm displays the API error value or a general registration failure message and remains on the form.

## Row 17

Column A:

UML Model

Column B:

@startuml

class RegisterDto <<DTO>> {
  fullName: String [0..1]
  email: String [0..1]
  password: String [0..1]
  confirmPassword: String [0..1]
}

class User <<Entity>> {
  id: Integer [1]
  fullName: String [1]
  email: String [1]
  passwordHash: String [1]
}

class RegisteredUserDto <<DTO>> {
  id: Integer [1]
  fullName: String [1]
  email: String [1]
}

class RegisterDataDto <<DTO>> {
  accessToken: String [1]
  user: RegisteredUserDto [1]
}

class RegisterResponseDto <<DTO>> {
  success: Boolean [1]
  message: String [1]
  data: RegisterDataDto [0..1]
}

class AuthResponse <<DTO>> {
  success: Boolean
  user: User [0..1]
  accessToken: String [0..1]
}

class PasswordHasher <<Service>> {
  hash(password: String, rounds: Integer): String
  matches(password: String, hash: String): Boolean {query}
  cost(hash: String): Integer {query}
}

class AuthService <<Service>> {
  register(dto: RegisterDto): RegisterResponseDto
  isRegistrationInputValid(dto: RegisterDto): Boolean {query}
}

AuthService ..> RegisterDto
AuthService ..> RegisterResponseDto
AuthService ..> PasswordHasher

RegisterResponseDto --> RegisterDataDto
RegisterDataDto --> RegisteredUserDto
RegisteredUserDto ..> User : maps from

@enduml

Column C:

s

## Row 18

Column A:

Business Rules

Column B:

BR-REG-01: Valid registration full name:
context AuthService::register(
  dto : RegisterDto
) : AuthResponse

pre BR_REG_01_Defined:
  not dto.fullName.oclIsUndefined()

pre BR_REG_01_Length:
  let normalizedName : String = trim(nfc(dto.fullName))
  in
    normalizedName.size() >= 4 and
    normalizedName.size() <= 25

pre BR_REG_01_Pattern:
  let normalizedName : String = trim(nfc(dto.fullName))
  in
    matches(
      normalizedName,
      '^[\p{L}]+(?: [\p{L}]+)*$'
    )

post BR_REG_01_Normalized:
  let normalizedName : String = trim(nfc(dto.fullName))
  in
    result.success implies
      not result.data.oclIsUndefined() and
      not result.data.user.oclIsUndefined() and
      result.data.user.fullName = normalizedName

BR-REG-02: Valid registration email:
context AuthService::register(
  dto : RegisterDto
) : AuthResponse

pre BR_REG_02_Defined:
  not dto.email.oclIsUndefined()

pre BR_REG_02_NotEmpty:
  trim(dto.email).size() > 0

pre BR_REG_02_MaxLength:
  let normalizedEmail : String = lower(trim(dto.email))
  in
    normalizedEmail.size() <= 255

pre BR_REG_02_ValidFormat:
  let normalizedEmail : String = lower(trim(dto.email))
  in
    isEmail(normalizedEmail)

post BR_REG_02_Normalized:
  let normalizedEmail : String = lower(trim(dto.email))
  in
    result.success implies
      not result.data.oclIsUndefined() and
      not result.data.user.oclIsUndefined() and
      result.data.user.email = normalizedEmail

BR-REG-03: Unique registration email:
context User

inv BR_REG_03_UniqueNormalizedEmail:
  User.allInstances()->isUnique(
    user | lower(trim(user.email))
  )

context AuthService::register(
  dto : RegisterDto
) : AuthResponse

pre BR_REG_03_EmailNotRegistered:
  not User.allInstances()->exists(
    user |
      lower(trim(user.email)) =
      lower(trim(dto.email))
  )

## Row 19

Column B:

BR-REG-04: Valid registration password
context AuthService::register(
  dto : RegisterDto
) : AuthResponse

pre BR_REG_04_Defined:
  not dto.password.oclIsUndefined()

pre BR_REG_04_Length:
  dto.password.size() >= 8 and
  dto.password.size() <= 64

pre BR_REG_04_NoWhitespace:
  not matches(
    dto.password,
    '.*\s.*'
  )

pre BR_REG_04_ContainsLowercase:
  matches(
    dto.password,
    '.*[a-z].*'
  )

pre BR_REG_04_ContainsUppercase:
  matches(
    dto.password,
    '.*[A-Z].*'
  )

pre BR_REG_04_ContainsDigit:
  matches(
    dto.password,
    '.*[0-9].*'
  )

pre BR_REG_04_ContainsSpecialCharacter:
  matches(
    dto.password,
    '.*[!@#$%^&*(){}\-_+=\[\],./<>?\\|:;].*'
  )

BR-REG-05: Permitted password characters
context AuthService::register(
  dto : RegisterDto
) : AuthResponse

pre BR_REG_05_AllowedCharacters:
  matches(
    dto.password,
    '^[A-Za-z0-9!@#$%^&*(){}_=+\[\],./<>?\\|:;\-]+$'
  )

## Row 20

Column B:

BR-REG-06: Matching registration passwords
context AuthService::register(
  dto : RegisterDto
) : AuthResponse

pre BR_REG_06_ConfirmPasswordDefined:
  not dto.confirmPassword.oclIsUndefined()

pre BR_REG_06_PasswordsMatch:
  dto.confirmPassword = dto.password

BR-REG-07: Confirm password handling
confirmPassword shall not be persisted or written to application logs.

BR-REG-08: Invalid registration handling
context AuthService::register(
  dto : RegisterDto
) : AuthResponse

post BR_REG_08_InvalidRequestRejected:
  not self.isRegistrationInputValid(dto)
  implies
    result.success = false

post BR_REG_08_NoUserCreated:
  not self.isRegistrationInputValid(dto)
  implies
    User.allInstances()->size() =
    User.allInstances()@pre->size()

## Row 21

Column B:

BR-REG-09: Bcrypt password storage
context AuthService::register(
  dto : RegisterDto
) : AuthResponse

post BR_REG_09_PasswordHashed:
  result.success implies
    let createdUser : User =
      User.allInstances()->any(
        user |
          lower(trim(user.email)) =
          lower(trim(dto.email))
      )
    in
      not createdUser.oclIsUndefined() and
      createdUser.passwordHash <> dto.password and
      bcryptMatches(
        dto.password,
        createdUser.passwordHash
      ) and
      bcryptCost(createdUser.passwordHash) = 10
Technical constraints:
- The plaintext password shall not be persisted or logged.
- Neither the plaintext password nor passwordHash shall be included in the API response.
- The bcrypt hash shall be generated before the User record is persisted.

BR-REG-10: Concurrent registration conflict handling
context User

inv BR_REG_10_AtMostOneUserPerNormalizedEmail:
  User.allInstances()->forAll(user |
    User.allInstances()
      ->select(other |
        lower(trim(other.email)) =
        lower(trim(user.email))
      )
      ->size() = 1
  )
Technical constraints:
- User.email shall be protected by the database unique constraint defined in BR-REG-03.
- If multiple concurrent registration requests contain the same normalized email, exactly one User creation shall succeed.
- Each conflicting request shall be rejected with HTTP 409 Conflict.
- A rejected request shall not issue a JWT or establish an authenticated session.
- After all concurrent requests complete, exactly one User shall exist for the normalized email.

BR-REG-11: Successful registration
context AuthService::register(
  dto : RegisterDto
) : RegisterResponseDto

post BR_REG_11_SuccessResponse:
  result.success implies
    result.message.size() > 0 and
    not result.data.oclIsUndefined() and
    not result.data.user.oclIsUndefined() and
    not result.data.accessToken.oclIsUndefined() and
    result.data.accessToken.size() > 0

post BR_REG_11_UserCreated:
  result.success implies
    User.allInstances()->one(user |
      user.id = result.data.user.id and
      lower(trim(user.email)) =
        lower(trim(dto.email))
    )
Technical constraints:
- After the User has been successfully persisted, the backend shall issue a signed JWT access token identifying that User.
- The successful response shall contain the created user information and access token inside the data object.
- After receiving the successful response, the client shall establish an authenticated session using the returned token.
- The client shall redirect the authenticated user to the home page.
- A session shall not be established and navigation shall not occur when registration fails.

## Row 22

Column A:

Related UI

Column B:

Register page; SignUpForm; route /register; AuthContext

## Row 23

Column A:

Related API IDs

Column B:

API-AUTH-REGISTER

## Row 24

Column A:

Notes

Column B:

Scope clarification: This use case covers email/password registration only. Google sign-up is outside scope.

## Row 26

Column A:

UC-02 - Log In

## Row 27

Column A:

Use Case ID

Column B:

UC-02

## Row 28

Column A:

Use Case Name

Column B:

Log In

## Row 29

Column A:

Description

Column B:

As a registered visitor, I want to log in with my email address and password so that the application creates an authenticated session.

## Row 30

Column A:

Actor(s)

Column B:

Visitor

## Row 31

Column A:

Priority

Column B:

Not Specified

## Row 32

Column A:

Trigger

Column B:

The visitor opens the login page or selects the Login link.

## Row 33

Column A:

Pre-Condition(s)

Column B:

PRE-1: A user record with the submitted email exists for successful authentication.
PRE-2: The frontend login route /login is accessible.
PRE-3: The backend and database are available.

## Row 34

Column A:

Post-Condition(s)

Column B:

POST-1: On success, a JWT and mapped user object are stored in localStorage.
POST-2: AuthContext contains the authenticated user.
POST-3: The frontend navigates to /.
POST-4: On failure, the visitor remains on the login page and no new authenticated state is created.

## Row 35

Column A:

Basic Flow

Column B:

1. The visitor clicks login button.
2. The frontend displays LoginForm.
3. The visitor enters email and password.
4. The visitor selects Login.
5. The frontend verifies that email is non-empty and matches its email pattern and that password is non-empty.
6. The frontend sends POST /api/auth/login.
7. The backend ValidationPipe validates LoginDto.
8. AuthService finds the user by email and compares the submitted password with the stored bcrypt hash.
9. AuthService signs a JWT whose payload contains sub and email.
10. The backend returns success, message, accessToken, and basic user information.
11. AuthContext maps the user, stores token and user in localStorage, and updates its user state.
12. The frontend navigates to /.

## Row 36

Column A:

Alternative Flow

Column B:

AF-1: Client-side validation failure
5a. If email or password is invalid or empty, the frontend displays a field-level error and does not call the API.

## Row 37

Column A:

Exception Flow

Column B:

EF-1: Invalid credentials
8a. If the user does not exist or bcrypt comparison fails, the backend returns HTTP 401 and the frontend displays the authentication error.

EF-2: Other request failure
6a. LoginForm displays the returned message or a general login failure message.

## Row 38

Column A:

UML Model

Column B:

@startuml

class LoginDto <<DTO>> {
  email: String [0..1]
  password: String [0..1]
}

class User <<Entity>> {
  id: Integer [1]
  fullName: String [1]
  email: String [1]
  passwordHash: String [1]
}

class LoginUserDto <<DTO>> {
  id: Integer [1]
  fullName: String [1]
  email: String [1]
}

class LoginDataDto <<DTO>> {
  accessToken: String [1]
  user: LoginUserDto [1]
}

class LoginResponseDto <<DTO>> {
  success: Boolean [1]
  message: String [1]
  data: LoginDataDto [0..1]
}

class PasswordHasher <<Service>> {
  matches(password: String, hash: String): Boolean {query}
}

class AuthService <<Service>> {
  login(dto: LoginDto): LoginResponseDto
  isLoginInputValid(dto: LoginDto): Boolean {query}
}

AuthService ..> LoginDto
AuthService ..> LoginResponseDto
AuthService ..> PasswordHasher

LoginResponseDto --> LoginDataDto
LoginDataDto --> LoginUserDto
LoginUserDto ..> User : maps from

@enduml

## Row 39

Column A:

Business Rules

Column B:

BR-LOG-01 - Valid login email

context AuthService::login(
  dto : LoginDto
) : LoginResponseDto

pre BR_LOG_01_Defined:
  not dto.email.oclIsUndefined()

pre BR_LOG_01_NotEmpty:
  trim(dto.email).size() > 0

pre BR_LOG_01_ValidFormat:
  let normalizedEmail : String =
    lower(trim(dto.email))
  in
    isEmail(normalizedEmail)

BR-LOG-02 - Non-empty login password

context AuthService::login(
  dto : LoginDto
) : LoginResponseDto

pre BR_LOG_02_Defined:
  not dto.password.oclIsUndefined()

pre BR_LOG_02_NotEmpty:
  dto.password.size() > 0

BR-LOG-03 - Existing login account

context AuthService::login(
  dto : LoginDto
) : LoginResponseDto

post BR_LOG_03_SuccessRequiresExistingUser:
  result.success implies
    User.allInstances()->exists(
      user |
        lower(trim(user.email)) =
        lower(trim(dto.email))
    )

## Row 40

Column A:

Business Rules

Column B:

BR-LOG-04 - Credential verification

context AuthService::login(
  dto : LoginDto
) : LoginResponseDto

post BR_LOG_04_SuccessRequiresValidCredentials:
  result.success implies
    User.allInstances()->exists(
      user |
        lower(trim(user.email)) =
          lower(trim(dto.email))
        and
        self.passwordHasher.matches(
          dto.password,
          user.passwordHash
        )
    )

BR-LOG-05 - Invalid credential handling

context AuthService::login(
  dto : LoginDto
) : LoginResponseDto

post BR_LOG_05_InvalidCredentialsRejected:
  let credentialsValid : Boolean =
    User.allInstances()->exists(
      user |
        lower(trim(user.email)) =
          lower(trim(dto.email))
        and
        self.passwordHasher.matches(
          dto.password,
          user.passwordHash
        )
    )
  in
    result.success = credentialsValid

Technical constraints:

If credentialsValid = false, the backend shall return HTTP 401 Unauthorized.
The same authentication error shall be returned when the email does not exist or when the password is incorrect.

BR-LOG-06 - Successful login

context AuthService::login(
  dto : LoginDto
) : LoginResponseDto

post BR_LOG_06_SuccessResponse:
  result.success implies
    not result.data.oclIsUndefined() and
    not result.data.accessToken.oclIsUndefined() and
    result.data.accessToken.size() > 0 and
    not result.data.user.oclIsUndefined()

post BR_LOG_06_CorrectAuthenticatedUser:
  result.success implies
    User.allInstances()->exists(
      user |
        user.id = result.data.user.id and
        lower(trim(user.email)) =
          lower(trim(dto.email)) and
        result.data.user.fullName = user.fullName and
        result.data.user.email = user.email
    )

Technical constraints:

The backend shall issue a signed JWT access token after successful authentication.
Neither the submitted plaintext password nor the stored password hash shall be included in the API response.
After receiving a successful response, the client shall establish the authenticated session using the returned access token and user information.

## Row 41

Column A:

Related UI

Column B:

Login page; LoginForm; route /login; AuthContext

## Row 42

Column A:

Related API IDs

Column B:

API-AUTH-LOGIN

## Row 43

Column A:

Notes

Column B:

Scope clarification: Authentication data is persisted in localStorage regardless of the “Keep me signed in” selection. Password recovery and Google login are outside scope.

## Row 45

Column A:

UC-03 - View Transaction History

## Row 46

Column A:

Use Case ID

Column B:

UC-03

## Row 47

Column A:

Use Case Name

Column B:

View Transaction History

## Row 48

Column A:

Description

Column B:

As an authenticated user, I want to view, filter, and paginate transactions belonging to my accounts.

## Row 49

Column A:

Actor(s)

Column B:

Authenticated User

## Row 50

Column A:

Priority

Column B:

Not Specified

## Row 51

Column A:

Trigger

Column B:

The user opens the Transactions page.

## Row 52

Column A:

Pre-Condition(s)

Column B:

PRE-1: The user is authenticated.
PRE-2: The protected route /transactions is accessible to the authenticated user.

## Row 53

Column A:

Post-Condition(s)

Column B:

POST-1: The frontend stores the current offset and hasMore state for pagination.
POST-2: If the returned transaction list is empty, the page displays an empty state.

## Row 54

Column A:

Basic Flow

Column B:

1. The user opens /transactions.
2. The frontend requests transaction history from GET /api/v1/transactions using the current filter and pagination state.
3. The system validates the authenticated session and identifies the current user.
4. The system retrieves the transaction history according to the applicable business rules.
5. The backend returns the transaction-list response.
6. The frontend displays the returned transaction history.

## Row 55

Column A:

Alternative Flow

Column B:

AF-1: Change transaction filter
2a. The user changes the transaction filter.
2b. The frontend clears the current list and requests the first page using the selected filter.
2c. The frontend displays the returned filtered results.

AF-2: Load more
6a. The user selects Load More.
6b. The frontend requests the next page using the current view state and appends the returned rows.

## Row 56

Column A:

Exception Flow

Column B:

EF-1: Unauthorized request
3a. If the JWT is missing, invalid, expired, or cannot resolve the authenticated user identity, the backend returns HTTP 401.
3b. The Axios response interceptor removes token and user from localStorage and redirects to /login.

EF-2: Invalid transaction-history request
4a. If the request violates the applicable transaction-history business rules, the backend returns HTTP 400.
4b. The frontend displays the returned message and an error toast.

EF-3: Retrieval failure
4c. If transaction retrieval fails, the backend returns HTTP 500.
4d. The frontend displays the returned message and an error toast.

## Row 57

Column A:

UML Model

Column B:

@startuml

class User <<Entity>> {
  user_id: Integer [1]
  full_name: String [1]
  email: String [1]
  username: String [1]
  password: String [1]
  phone_number: String [1]
  profile_picture_url: String [1]
  total_balance: Decimal [1]
}

class Account <<Entity>> {
  account_id: Integer [1]
  user_id: Integer [1]
  bank_name: String [1]
  account_type: AccountType [1]
  branch_name: String [1]
  account_number_full: String [1]
  account_number_last_4: String [1]
  balance: Decimal [1]
}

class Category <<Entity>> {
  category_id: Integer [1]
  category_name: String [1]
}

class Transaction <<Entity>> {
  transaction_id: Integer [1]
  account_id: Integer [1]
  transaction_date: Date [1]
  type: TransactionType [1]
  item_description: String [1]
  shop_name: String [1]
  amount: Decimal [1]
  payment_method: String [1]
  status: TransactionStatus [1]
  receipt_id: Integer [1]
  category_id: Integer [0..1]
}

enum AccountType {
  Checking
  Credit_Card
  Savings
  Investment
  Loan
}
note right of AccountType
  Credit_Card maps to database literal 'Credit Card'.
end note

enum TransactionType {
  Revenue
  Expense
}

enum TransactionStatus {
  Complete
  Pending
  Failed
}

enum TransactionFilterType {
  All
  Revenue
  Expense
}

class TransactionListQueryDto <<DTO>> {
  type: TransactionFilterType [1]
  limit: Integer [0..1]
  offset: Integer [0..1]
}

class TransactionDto <<DTO>> {
  transaction_id: Integer [1]
  account_id: Integer [1]
  transaction_date: Date [1]
  type: TransactionType [1]
  item_description: String [1]
  shop_name: String [1]
  amount: Decimal [1]
  payment_method: String [1]
  status: TransactionStatus [1]
}

class TransactionListResponseDto <<DTO>> {
  data: TransactionDto [*]
  total: Integer [1]
  hasMore: Boolean [1]
}

class TransactionService <<Service>> {
  findAllByUserId(user_id: Integer, type: TransactionFilterType, limit: Integer, offset: Integer): TransactionListResponseDto
}

User "1" -- "0..*" Account : owns
Account "1" -- "0..*" Transaction : contains
Category "0..1" -- "0..*" Transaction : classifies

TransactionService ..> TransactionListQueryDto
TransactionService ..> TransactionListResponseDto
TransactionListResponseDto --> TransactionDto
TransactionDto ..> Transaction : maps from

@enduml

## Row 58

Column A:

Business Rules

Column B:

BR-TXN-01: Transaction ownership scope
context TransactionService::findAllByUserId(
  user_id : Integer,
  type : TransactionFilterType,
  limit : Integer,
  offset : Integer
) : TransactionListResponseDto

pre BR_TXN_01_UserExists:
  User.allInstances()->exists(u |
    u.user_id = user_id
  )

post BR_TXN_01_OwnedAccountsOnly:
  result.data->forAll(t |
    Account.allInstances()->exists(a |
      a.account_id = t.account_id and
      a.user_id = user_id
    )
  )

BR-TXN-02: Allowed transaction filter and stored transaction type
context TransactionService::findAllByUserId(
  user_id : Integer,
  type : TransactionFilterType,
  limit : Integer,
  offset : Integer
) : TransactionListResponseDto

pre BR_TXN_02_AllowedFilter:
  Set{TransactionFilterType::All,
      TransactionFilterType::Revenue,
      TransactionFilterType::Expense}->includes(type)

post BR_TXN_02_FilterApplied:
  (type = TransactionFilterType::Revenue implies
    result.data->forAll(t |
      t.type = TransactionType::Revenue
    )) and
  (type = TransactionFilterType::Expense implies
    result.data->forAll(t |
      t.type = TransactionType::Expense
    ))

context Transaction
inv BR_TXN_02_StoredType:
  type = TransactionType::Revenue or
  type = TransactionType::Expense

Technical constraint:
- All is a query/UI filter only. It shall never be stored in Transactions.type.

BR-TXN-03: Pagination and ordering
context TransactionService::findAllByUserId(
  user_id : Integer,
  type : TransactionFilterType,
  limit : Integer,
  offset : Integer
) : TransactionListResponseDto

pre BR_TXN_03_LimitPositive:
  limit > 0

pre BR_TXN_03_OffsetNonNegative:
  offset >= 0

post BR_TXN_03_PageSize:
  result.data->size() <= limit

post BR_TXN_03_HasMore:
  result.hasMore =
    (offset + result.data->size() < result.total)

post BR_TXN_03_DescendingTransactionDate:
  result.data->size() <= 1 or
  Sequence{1..result.data->size()-1}->forAll(i |
    result.data->at(i).transaction_date >=
    result.data->at(i + 1).transaction_date
  )

Technical constraints:
- If limit is omitted, the endpoint shall use limit = 10.
- If offset is omitted, the endpoint shall use offset = 0.

BR-TXN-04: Database relationship integrity
context Account
inv BR_TXN_04_AccountOwnerExists:
  User.allInstances()->exists(u |
    u.user_id = self.user_id
  )

context Transaction
inv BR_TXN_04_TransactionAccountExists:
  Account.allInstances()->exists(a |
    a.account_id = self.account_id
  )

inv BR_TXN_04_OptionalCategoryValid:
  self.category_id.oclIsUndefined() or
  Category.allInstances()->exists(c |
    c.category_id = self.category_id
  )

## Row 59

Column B:

BR-TXN-05: Empty transaction result
context TransactionService::findAllByUserId(
  user_id : Integer,
  type : TransactionFilterType,
  limit : Integer,
  offset : Integer
) : TransactionListResponseDto

post BR_TXN_05_EmptyResultConsistency:
  result.total = 0 implies
    result.data->isEmpty() and
    result.hasMore = false

BR-TXN-06: Response rows map to persisted Transactions
context TransactionService::findAllByUserId(
  user_id : Integer,
  type : TransactionFilterType,
  limit : Integer,
  offset : Integer
) : TransactionListResponseDto

post BR_TXN_06_ResponseBackedByTransaction:
  result.data->forAll(dto |
    Transaction.allInstances()->exists(t |
      t.transaction_id = dto.transaction_id and
      t.account_id = dto.account_id and
      t.transaction_date = dto.transaction_date and
      t.type = dto.type and
      t.item_description = dto.item_description and
      t.shop_name = dto.shop_name and
      t.amount = dto.amount and
      t.payment_method = dto.payment_method and
      t.status = dto.status
    )
  )

BR-TXN-07: Viewing transaction history is read-only
context TransactionService::findAllByUserId(
  user_id : Integer,
  type : TransactionFilterType,
  limit : Integer,
  offset : Integer
) : TransactionListResponseDto

post BR_TXN_07_TransactionIdentityUnchanged:
  Transaction.allInstances()->collect(t | t.transaction_id)->asSet() =
  Transaction.allInstances()@pre->collect(t | t.transaction_id)->asSet()

post BR_TXN_07_TransactionDataUnchanged:
  Transaction.allInstances()->forAll(t |
    Transaction.allInstances()@pre->exists(old |
      old.transaction_id = t.transaction_id and
      old.account_id = t.account_id and
      old.transaction_date = t.transaction_date and
      old.type = t.type and
      old.item_description = t.item_description and
      old.shop_name = t.shop_name and
      old.amount = t.amount and
      old.payment_method = t.payment_method and
      old.status = t.status and
      old.receipt_id = t.receipt_id and
      old.category_id = t.category_id
    )
  )

post BR_TXN_07_AccountIdentityUnchanged:
  Account.allInstances()->collect(a | a.account_id)->asSet() =
  Account.allInstances()@pre->collect(a | a.account_id)->asSet()

Technical constraint:
- Listing transaction history shall not create, update, or delete Transactions or Accounts records.

## Row 60

Column A:

Related UI

Column B:

TransactionsPage; route /transactions

## Row 61

Column A:

Related API IDs

Column B:

API-TRANSACTION-LIST

## Row 62

Column A:

Notes

## Row 64

Column A:

UC-04 - Create a Transaction

## Row 65

Column A:

Use Case ID

Column B:

UC-04

## Row 66

Column A:

Use Case Name

Column B:

Create a Transaction

## Row 67

Column A:

Description

Column B:

As an authenticated user, I want to create a revenue or expense transaction for one of my accounts.

## Row 68

Column A:

Actor(s)

Column B:

Authenticated User

## Row 69

Column A:

Priority

Column B:

Not Specified

## Row 70

Column A:

Trigger

Column B:

The user selects Add Transaction from the Transactions page.

## Row 71

Column A:

Pre-Condition(s)

Column B:

PRE-1: The user is authenticated and the validated JWT identifies an existing Users.user_id.
PRE-2: At least one Accounts row exists with Accounts.user_id equal to the authenticated user_id.
PRE-3: The selected account exists and is owned by the authenticated user.
PRE-4: A category is optional. If category_id is supplied, it must reference an existing Categories.category_id.

## Row 72

Column A:

Post-Condition(s)

Column B:

POST-1: On success, exactly one new Transactions row is stored for the selected account.
POST-2: The stored transaction has type Revenue or Expense, amount > 0, and non-empty item_description, shop_name, and payment_method. category_id may be null.
POST-3: For Revenue, the selected Accounts.balance increases by amount; for Expense, it decreases by amount.
POST-4: The Transactions insert and Accounts.balance update are committed atomically; on failure neither partial change remains.
POST-5: The frontend shows a success toast, resets the form, and navigates to /transactions after 1.5 seconds.

## Row 73

Column A:

Basic Flow

Column B:

1. The user opens /transactions/add.
2. AddTransactionForm loads the user's accounts and loads categories for optional classification.
3. The user enters itemDescription, amount, transaction type, account, transaction date, shopName, and paymentMethod; the user may optionally select a category.
4. The form defaults type to Expense, transactionDate to today, and submitted status to Complete.
5. The user selects Save.
6. The frontend validates accountId, transactionDate, type, non-empty itemDescription, non-empty shopName, non-empty paymentMethod, and amount >= 0.01. category_id is not required.
7. The frontend sends POST /api/v1/transactions.
8. JwtAuthGuard validates the JWT and supplies the authenticated identifier corresponding to Users.user_id.
9. The backend validates CreateTransactionDto, verifies category_id only when supplied, and verifies that accountId references an Accounts row owned by the authenticated user_id.
10. For Expense, the backend verifies Accounts.balance >= amount.
11. The backend creates the Transactions row, mapping accountId -> account_id, transactionDate -> transaction_date, itemDescription -> item_description, shopName -> shop_name, and paymentMethod -> payment_method. If status is omitted, Complete is used.
12. In the same database transaction, the backend updates Accounts.balance by +amount for Revenue or -amount for Expense and commits both changes.
13. The frontend displays a success toast, resets fields, and navigates to /transactions after 1.5 seconds.

## Row 74

Column A:

Alternative Flow

Column B:

AF-1: Create Revenue
4a. The user selects Revenue.
10a. The insufficient-balance check is not applied.
12a. The backend increases Accounts.balance by amount.

AF-2: Create transaction without category
3a. The user leaves category unselected.
9a. The backend does not require a category lookup and stores Transactions.category_id = null.

AF-3: Category list unavailable
2a. If categories cannot be loaded, the frontend shows a warning but still allows creation without category because category_id is optional.

AF-4: Cancel
5a. The user selects Cancel and the frontend navigates to /transactions without submitting.

## Row 75

Column A:

Exception Flow

Column B:

EF-1: Accounts cannot be loaded
2a. If the user's accounts cannot be loaded, the frontend displays an error and cannot submit because accountId is required.

EF-2: Client-side validation failure
6a. If accountId, transactionDate, type, itemDescription, shopName, or paymentMethod is missing/empty, or amount < 0.01, the frontend displays field errors and does not send the request.

EF-3: Unauthorized request
8a. If the JWT is missing, invalid, or expired, the backend returns HTTP 401.

EF-4: Backend validation or business-rule failure
9a. Invalid required input, an invalid supplied category_id, a non-owned account, or insufficient Expense balance produces HTTP 400; the frontend displays the returned error.

EF-5: Database failure
12a. The backend rolls back the database transaction so neither the Transactions row nor Accounts.balance is partially changed, and returns HTTP 500.

## Row 76

Column A:

UML Model

Column B:

@startuml

class User <<Entity>> {
  user_id: Integer [1]
  full_name: String [1]
  email: String [1]
  username: String [1]
  password: String [1]
  phone_number: String [1]
  profile_picture_url: String [1]
  total_balance: Decimal [1]
}

class Account <<Entity>> {
  account_id: Integer [1]
  user_id: Integer [1]
  bank_name: String [1]
  account_type: AccountType [1]
  branch_name: String [1]
  account_number_full: String [1]
  account_number_last_4: String [1]
  balance: Decimal [1]
}

class Category <<Entity>> {
  category_id: Integer [1]
  category_name: String [1]
}

class Transaction <<Entity>> {
  transaction_id: Integer [1]
  account_id: Integer [1]
  transaction_date: Date [1]
  type: TransactionType [1]
  item_description: String [1]
  shop_name: String [1]
  amount: Decimal [1]
  payment_method: String [1]
  status: TransactionStatus [1]
  receipt_id: Integer [1]
  category_id: Integer [0..1]
}

enum AccountType {
  Checking
  Credit_Card
  Savings
  Investment
  Loan
}
note right of AccountType
  Credit_Card maps to database literal 'Credit Card'.
end note

enum TransactionType {
  Revenue
  Expense
}

enum TransactionStatus {
  Complete
  Pending
  Failed
}

class CreateTransactionDto <<DTO>> {
  accountId: Integer [1]
  transactionDate: Date [1]
  type: TransactionType [1]
  itemDescription: String [1]
  category_id: Integer [0..1]
  shopName: String [1]
  amount: Decimal [1]
  paymentMethod: String [1]
  status: TransactionStatus [0..1]
}

class CreateTransactionDataDto <<DTO>> {
  transactionId: Integer [1]
  accountId: Integer [1]
  transactionDate: Date [1]
  type: TransactionType [1]
  itemDescription: String [1]
  shopName: String [1]
  amount: Decimal [1]
  paymentMethod: String [1]
  status: TransactionStatus [1]
  receiptId: Integer [0..1]
  category_id: Integer [0..1]
}

class CreateTransactionResponseDto <<DTO>> {
  message: String [1]
  data: CreateTransactionDataDto [1]
}

class TransactionService <<Service>> {
  create(user_id: Integer, dto: CreateTransactionDto): CreateTransactionResponseDto
}

User "1" -- "0..*" Account : owns
Account "1" -- "0..*" Transaction : contains
Category "0..1" -- "0..*" Transaction : classifies

TransactionService ..> CreateTransactionDto
TransactionService ..> CreateTransactionResponseDto
CreateTransactionResponseDto --> CreateTransactionDataDto
CreateTransactionDataDto ..> Transaction : maps from

@enduml

## Row 77

Column A:

Business Rules

Column B:

BR-TXN-08: Required transaction data
context TransactionService::create(
  user_id : Integer,
  dto : CreateTransactionDto
) : CreateTransactionResponseDto

pre BR_TXN_08_RequiredFields:
  not dto.accountId.oclIsUndefined() and
  not dto.transactionDate.oclIsUndefined() and
  not dto.type.oclIsUndefined() and
  not dto.itemDescription.oclIsUndefined() and
  trim(dto.itemDescription).size() > 0 and
  not dto.shopName.oclIsUndefined() and
  trim(dto.shopName).size() > 0 and
  not dto.paymentMethod.oclIsUndefined() and
  trim(dto.paymentMethod).size() > 0 and
  not dto.amount.oclIsUndefined() and
  dto.amount >= 0.01

BR-TXN-09: Allowed transaction type and status
context TransactionService::create(
  user_id : Integer,
  dto : CreateTransactionDto
) : CreateTransactionResponseDto

pre BR_TXN_09_AllowedType:
  dto.type = TransactionType::Revenue or
  dto.type = TransactionType::Expense

pre BR_TXN_09_AllowedStatus:
  dto.status.oclIsUndefined() or
  Set{TransactionStatus::Complete,
      TransactionStatus::Pending,
      TransactionStatus::Failed}->includes(dto.status)

post BR_TXN_09_DefaultStatus:
  (dto.status.oclIsUndefined() implies
    result.data.status = TransactionStatus::Complete) and
  (not dto.status.oclIsUndefined() implies
    result.data.status = dto.status)

BR-TXN-10: Optional category must be valid when supplied
context TransactionService::create(
  user_id : Integer,
  dto : CreateTransactionDto
) : CreateTransactionResponseDto

pre BR_TXN_10_CategoryOptionalAndValid:
  dto.category_id.oclIsUndefined() or
  Category.allInstances()->exists(c |
    c.category_id = dto.category_id
  )

post BR_TXN_10_CategoryStored:
  (dto.category_id.oclIsUndefined() implies
    result.data.category_id.oclIsUndefined()) and
  (not dto.category_id.oclIsUndefined() implies
    result.data.category_id = dto.category_id)

## Row 78

Column B:

BR-TXN-11: Account ownership
context TransactionService::create(
  user_id : Integer,
  dto : CreateTransactionDto
) : CreateTransactionResponseDto

pre BR_TXN_11_AccountOwnedByUser:
  Account.allInstances()->exists(a |
    a.account_id = dto.accountId and
    a.user_id = user_id
  )

BR-TXN-12: Sufficient balance for Expense
context TransactionService::create(
  user_id : Integer,
  dto : CreateTransactionDto
) : CreateTransactionResponseDto

pre BR_TXN_12_SufficientExpenseBalance:
  dto.type = TransactionType::Expense implies
    Account.allInstances()->exists(a |
      a.account_id = dto.accountId and
      a.user_id = user_id and
      a.balance >= dto.amount
    )

BR-TXN-13: Account balance adjustment
context TransactionService::create(
  user_id : Integer,
  dto : CreateTransactionDto
) : CreateTransactionResponseDto

post BR_TXN_13_BalanceAdjusted:
  Account.allInstances()->exists(a |
    a.account_id = dto.accountId and
    ((dto.type = TransactionType::Revenue and
      a.balance = a.balance@pre + dto.amount) or
     (dto.type = TransactionType::Expense and
      a.balance = a.balance@pre - dto.amount))
  )

BR-TXN-14: Created transaction maps to the request and database
context TransactionService::create(
  user_id : Integer,
  dto : CreateTransactionDto
) : CreateTransactionResponseDto

post BR_TXN_14_OneNewTransaction:
  Transaction.allInstances()->size() =
    Transaction.allInstances()@pre->size() + 1

post BR_TXN_14_PersistedTransaction:
  Transaction.allInstances()->exists(t |
    t.transaction_id = result.data.transactionId and
    t.account_id = dto.accountId and
    t.transaction_date = dto.transactionDate and
    t.type = dto.type and
    t.item_description = trim(dto.itemDescription) and
    t.shop_name = trim(dto.shopName) and
    t.amount = dto.amount and
    t.payment_method = trim(dto.paymentMethod) and
    t.status = result.data.status and
    ((dto.category_id.oclIsUndefined() and
      t.category_id.oclIsUndefined()) or
     (not dto.category_id.oclIsUndefined() and
      t.category_id = dto.category_id))
  )

BR-TXN-15: Atomic transaction creation
Technical constraints:
- The Transactions insert and Accounts.balance update shall execute in one database transaction.
- If any validation, persistence, or balance-update step fails before commit, the operation shall roll back and leave both Transactions and Accounts unchanged by this request.
- shopName maps to Transactions.shop_name and paymentMethod maps to Transactions.payment_method; both are mandatory and shall not be null or empty.
- category_id maps to Transactions.category_id and remains optional/nullable.

## Row 79

Column A:

Related UI

Column B:

AddTransactionPage; AddTransactionForm; route /transactions/add

## Row 80

Column A:

Related API IDs

Column B:

API-TRANSACTION-CREATE; API-ACCOUNT-LIST; API-CATEGORY-LIST

## Row 81

Column A:

Notes

Column B:

Specification alignment: Transaction ownership follows Users → Accounts → Transactions. category_id is optional/nullable; shopName and paymentMethod are required and must be non-empty. BR-TXN-08..15 belong to UC-04 and are intentionally distinct from UC-03 rules BR-TXN-01..07.

## Row 83

Column A:

UC-05 - View Bank Accounts

## Row 84

Column A:

Use Case ID

Column B:

UC-05

## Row 85

Column A:

Use Case Name

Column B:

View Bank Accounts

## Row 86

Column A:

Description

Column B:

As an authenticated user, I want to view the bank accounts linked to my user identifier.

## Row 87

Column A:

Actor(s)

Column B:

Authenticated User

## Row 88

Column A:

Priority

Column B:

Not Specified

## Row 89

Column A:

Trigger

Column B:

The user opens the Accounts page.

## Row 90

Column A:

Pre-Condition(s)

Column B:

PRE-1: The user is authenticated.

## Row 91

Column A:

Post-Condition(s)

Column B:

POST-1: The frontend displays accounts.
POST-2: If no accounts exist, the page displays an empty state and an Add Account action.

## Row 92

Column A:

Basic Flow

Column B:

1. The user opens /accounts.
2. The frontend sends GET /api/v1/accounts.
3. JwtAuthGuard authenticates the request and supplies userId.
4. AccountService processes the request to retrieve the account data.
5. The backend returns success, message, and a data object containing user_id and accounts.
6. The frontend displays account cards containing bank name, account type, account number, and balance.

## Row 93

Column A:

Alternative Flow

Column B:

AF-1: No linked accounts
4a. The query returns an empty array.
6a. The frontend displays its no-account message and an action that navigates to /accounts/add.

## Row 94

Column A:

Exception Flow

Column B:

EF-1: Unauthorized request
3a. HTTP 401 is handled by the Axios interceptor, which clears local authentication data and redirects to /login.

EF-2: Retrieval failure
4a. The page displays the returned error message or a general loading error.

## Row 95

Column A:

UML Model

Column B:

@startuml

class User <<Entity>> {
  user_id: Integer [1]
  full_name: String [1]
  email: String [1]
  username: String [1]
  password: String [1]
  phone_number: String [1]
  profile_picture_url: String [1]
  total_balance: Decimal [1]
}

class Account <<Entity>> {
  account_id: Integer [1]
  user_id: Integer [1]
  bank_name: String [1]
  account_type: AccountType [1]
  branch_name: String [0..1]
  account_number_full: String [1]
  account_number_last_4: String [1]
  balance: Decimal [1]
}

enum AccountType {
  Checking
  Credit_Card
  Savings
  Investment
  Loan
}
note right of AccountType
  Credit_Card maps to database literal 'Credit Card'.
end note

class AccountDto <<DTO>> {
  id: Integer [1]
  bank_name: String [1]
  account_type: AccountType [1]
  branch_name: String [0..1]
  account_number_last_4: String [1]
  balance: Decimal [1]
}

class AccountListDataDto <<DTO>> {
  user_id: Integer [1]
  accounts: AccountDto [0..*]
}

class AccountListResponseDto <<DTO>> {
  success: Boolean [1]
  message: String [1]
  data: AccountListDataDto [1]
}

class AccountService <<Service>> {
  findAllByUserId(user_id: Integer): AccountListResponseDto
}

User "1" -- "0..*" Account : owns

AccountService ..> AccountListResponseDto
AccountListResponseDto --> AccountListDataDto
AccountListDataDto "1" -- "0..*" AccountDto : contains
AccountDto ..> Account : maps from

@enduml

## Row 96

Column A:

Business Rules

Column B:

BR-ACC-01: Account ownership scope
context AccountService::findAllByUserId(
  user_id : Integer
) : AccountListResponseDto

pre BR_ACC_01_UserDefined:
  not user_id.oclIsUndefined()

post BR_ACC_01_OwnedAccountsOnly:
  result.success implies
    result.data.accounts->forAll(dto |
      Account.allInstances()->exists(a |
        a.account_id = dto.id and
        a.user_id = user_id
      )
    )

## Row 97

Column B:

BR-ACC-02: Ordering
context AccountService::findAllByUserId(
  user_id : Integer
) : AccountListResponseDto

post BR_ACC_02_OrderedByAccountIdAsc:
  result.success implies
    result.data.accounts->size() <= 1 or
    Sequence{1..result.data.accounts->size()-1}->forAll(i |
      result.data.accounts->at(i).id < result.data.accounts->at(i + 1).id
    )

## Row 98

Column B:

BR-ACC-03: Response rows map to persisted Accounts
context AccountService::findAllByUserId(
  user_id : Integer
) : AccountListResponseDto

post BR_ACC_03_ResponseBackedByAccount:
  result.success implies
    result.data.accounts->forAll(dto |
      Account.allInstances()->exists(a |
        a.account_id = dto.id and
        a.bank_name = dto.bank_name and
        a.account_type = dto.account_type and
        a.branch_name = dto.branch_name and
        a.account_number_last_4 = dto.account_number_last_4 and
        a.balance = dto.balance
      )
    )


## Row 99

Column B:

BR-ACC-04: Account number exposure restriction
context AccountService::findAllByUserId(
  user_id : Integer
) : AccountListResponseDto
post BR_ACC_04_NoFullAccountNumber:
  result.success implies
    result.data.accounts->forAll(dto |
      dto.account_number_full.oclIsUndefined()
    )

Technical constraints:
- The backend shall only query the necessary columns to optimize performance.
- The backend shall not return the full account number (account_number_full) in the list response to prevent exposing sensitive data over the network.
- The backend shall return only the stored account_number_last_4.
- The frontend shall mask the account number by prefixing these 4 digits with exactly four asterisks (e.g., ""**** 1234""), regardless of the original account number's length."

## Row 100

Column B:

BR-ACC-05: Empty account result
context AccountService::findAllByUserId(
  user_id : Integer
) : AccountListResponseDto
post BR_ACC_05_EmptyResultConsistency:
  not Account.allInstances()->exists(a | a.user_id = user_id)
  implies
    result.success and
    result.data.accounts->isEmpty()


## Row 101

Column B:

BR-ACC-06: Viewing accounts is read-only
context AccountService::findAllByUserId(
  user_id : Integer
) : AccountListResponseDto

post BR_ACC_06_AccountIdentityUnchanged:
  Account.allInstances()->collect(a | a.account_id)->asSet() =
  Account.allInstances()@pre->collect(a | a.account_id)->asSet()

post BR_ACC_06_AccountDataUnchanged:
  Account.allInstances()->forAll(a |
    Account.allInstances()@pre->exists(old |
      old.account_id = a.account_id and
      old.user_id = a.user_id and
      old.bank_name = a.bank_name and
      old.account_type = a.account_type and
      old.branch_name = a.branch_name and
      old.account_number_full = a.account_number_full and
      old.account_number_last_4 = a.account_number_last_4 and
      old.balance = a.balance
    )
  )

Technical constraint:
- Listing accounts shall not create, update, or delete any Account or Transaction records.

## Row 102

Column A:

Related UI

Column B:

AccountListPage; AccountCard; route /accounts

## Row 103

Column A:

Related API IDs

Column B:

API-ACCOUNT-LIST

## Row 104

Column A:

Notes

## Row 106

Column A:

UC-06 - Add a Bank Account

## Row 107

Column A:

Use Case ID

Column B:

UC-06

## Row 108

Column A:

Use Case Name

Column B:

Add a Bank Account

## Row 109

Column A:

Description

Column B:

As an authenticated user, I want to add a bank account with its current balance.

## Row 110

Column A:

Actor(s)

Column B:

Authenticated User

## Row 111

Column A:

Priority

Column B:

Not Specified

## Row 112

Column A:

Trigger

Column B:

The user selects an Add Account action.

## Row 113

Column A:

Pre-Condition(s)

Column B:

PRE-1: The user is authenticated.
PRE-2: The Add Account route /accounts/add is accessible.

## Row 114

Column A:

Post-Condition(s)

Column B:

POST-1: On success, an account row is stored with userId from the JWT and account_number_last_4 derived from account_number_full.
POST-2: The frontend shows a success toast and navigates to /accounts after 1.5 seconds.
POST-3: On failure, the account is not added by the request.

## Row 115

Column A:

Basic Flow

Column B:

1. The user opens /accounts/add.
2. The frontend displays AddAccountForm with accountType defaulted to Checking.
3. The user enters bank_name, account_type, optional branch_name, account_number_full, and balance.
4. The user selects Add Account.
5. The frontend validates the input fields before submission.
6. The frontend sends POST /api/v1/accounts.
7. The backend ValidationPipe validates CreateAccountDto.
8. AccountService validates the creation request.
9. AccountService creates the account using userId from the JWT and stores it.
10. The frontend shows a success toast and navigates to /accounts after 1.5 seconds.

## Row 116

Column A:

Alternative Flow

Column B:

AF-1: Optional branch omitted
3a. The user leaves branch_name empty.
6a. The frontend omits branch_name and the backend stores it appropriately.

AF-2: Cancel
4a. The user selects Cancel and returns to /accounts without submitting.

## Row 117

Column A:

Exception Flow

Column B:

EF-1: Client-side validation failure
5a. The form displays field errors and does not call the API.

EF-2: Account creation conflict
8a. The backend returns HTTP 409 and the frontend displays the conflict message.

EF-3: Backend validation failure
7a. The frontend maps returned validation messages to fields when possible.

EF-4: Storage failure
9a. The backend returns HTTP 500 and the frontend displays its create-account failure message.

## Row 118

Column A:

UML Model

Column B:

@startuml

class User <<Entity>> {
  user_id: Integer [1]
  full_name: String [1]
  email: String [1]
  username: String [1]
  password: String [1]
  phone_number: String [1]
  profile_picture_url: String [1]
  total_balance: Decimal [1]
}

class Account <<Entity>> {
  account_id: Integer [1]
  user_id: Integer [1]
  bank_name: String [1]
  account_type: AccountType [1]
  branch_name: String [0..1]
  account_number_full: String [1]
  account_number_last_4: String [1]
  balance: Decimal [1]
}

enum AccountType {
  Checking
  Credit_Card
  Savings
  Investment
  Loan
}
note right of AccountType
  Credit_Card maps to database literal 'Credit Card'.
end note

class CreateAccountDto <<DTO>> {
  bank_name: String [1]
  account_type: AccountType [1]
  branch_name: String [0..1]
  account_number_full: String [1]
  balance: Decimal [1]
}

class AccountResponseDto <<DTO>> {
  id: Integer [1]
  user_id: Integer [1]
  bank_name: String [1]
  account_type: AccountType [1]
  branch_name: String [0..1]
  account_number_last_4: String [1]
  balance: Decimal [1]
}

class AccountService <<Service>> {
  create(userId: Integer, dto: CreateAccountDto): AccountResponseDto
}

User "1" -- "0..*" Account : owns
AccountService ..> AccountResponseDto
AccountService ..> CreateAccountDto
CreateAccountDto ..> Account : mapped to
AccountResponseDto ..> Account : mapped from

@enduml

## Row 119

Column A:

Business Rules

Column B:

BR-ACC-07: Allowed account type
context AccountService::create(
  userId : Integer,
  dto : CreateAccountDto
) : AccountResponseDto

pre BR_ACC_07_ValidType:
  Set{'Checking', 'Credit Card', 'Savings', 'Investment', 'Loan'}->includes(dto.account_type)

## Row 120

Column B:

BR-ACC-08: Required account text fields
context AccountService::create(
  userId : Integer,
  dto : CreateAccountDto
) : AccountResponseDto

pre BR_ACC_08_RequiredText:
  not dto.bank_name.oclIsUndefined() and dto.bank_name.trim().size() > 0 and
  not dto.account_number_full.oclIsUndefined() and dto.account_number_full.trim().size() > 0

## Row 121

Column B:

BR-ACC-09: Numeric non-negative account balance
context AccountService::create(
  userId : Integer,
  dto : CreateAccountDto
) : AccountResponseDto

pre BR_ACC_09_IsNumeric:
  dto.balance.oclIsTypeOf(Real) or dto.balance.oclIsTypeOf(Integer)

pre BR_ACC_09_NonNegativeBalance:
  not dto.balance.oclIsUndefined() and dto.balance >= 0
Technical constraint:
- The balance must be a valid numeric type (not a string), and must be greater than or equal to zero.

## Row 122

Column B:

BR-ACC-10: Unique account number per owner
context AccountService::create(
  userId : Integer,
  dto : CreateAccountDto
) : AccountResponseDto

pre BR_ACC_10_UniqueAccount:
  not Account.allInstances()->exists(a | 
    a.user_id = userId and 
    a.account_number_full = dto.account_number_full
  )

## Row 123

Column B:

BR-ACC-11: Derive final four account characters
context AccountService::create(
  userId : Integer,
  dto : CreateAccountDto
) : AccountResponseDto

post BR_ACC_11_DeriveLast4:
  let newAcc = Account.allInstances()->any(a | a.account_id = result.id) in
  newAcc.account_number_last_4 = dto.account_number_full.substring(dto.account_number_full.size() - 3, dto.account_number_full.size())

Technical constraint:
- The backend derives account_number_last_4 by taking the exact last 4 characters of the submitted account_number_full (e.g., via .slice(-4)).

## Row 124

Column B:

BR-ACC-12: Account creation persistence mapping
context AccountService::create(
  userId : Integer,
  dto : CreateAccountDto
) : AccountResponseDto

post BR_ACC_12_StorageMapping:
  Account.allInstances()->exists(a |
    a.account_id = result.id and
    a.user_id = userId and
    a.bank_name = dto.bank_name and
    a.account_type = dto.account_type and
    a.branch_name = dto.branch_name and
    a.account_number_full = dto.account_number_full and
    a.balance = dto.balance
  )

post BR_ACC_12_ResponseMapping:
  result.id = Account.allInstances()->any(a | a.account_number_full = dto.account_number_full).account_id

## Row 125

Column B:

BR-ACC-13: Account number format and length
context AccountService::create(
  userId : Integer,
  dto : CreateAccountDto
) : AccountResponseDto

pre BR_ACC_13_NumericCharactersOnly:
  not dto.account_number_full.oclIsUndefined() and 
  matches(dto.account_number_full, '^[0-9]+$')
pre BR_ACC_13_LengthConstraints:
  dto.account_number_full.size() >= 8 and dto.account_number_full.size() <= 34

Technical constraint:
- account_number_full must contain only numeric digits.
- The length must be between 8 and 34 characters (to safely derive the last 4 digits and reflect real-world bank account numbers).

## Row 126

Column B:

BR-ACC-14: Conditional branch name requirement
context AccountService::create(
  userId : Integer,
  dto : CreateAccountDto
) : AccountResponseDto

pre BR_ACC_14_BranchNameConditional:
  if Set{'Loan', 'Investment'}->includes(dto.account_type) then
    not dto.branch_name.oclIsUndefined() and dto.branch_name.trim().size() > 0
  else
    dto.branch_name.oclIsUndefined() or dto.branch_name.oclIsTypeOf(String)
  endif

Technical constraint:
- This rule overrides the base optional branch rule. If the account_type is 'Loan' or 'Investment', the branch_name field is strictly required and cannot be empty.
- For all other account types, branch_name is optional. If omitted, it shall be processed and stored as null or undefined.

## Row 127

Column B:

BR-ACC-15: Minimum initial deposit for specific types
context AccountService::create(
  userId : Integer,
  dto : CreateAccountDto
) : AccountResponseDto

pre BR_ACC_15_MinInitialDeposit:
  if Set{'Savings', 'Investment'}->includes(dto.account_type) then
    not dto.balance.oclIsUndefined() and dto.balance >= 50000
  else
    not dto.balance.oclIsUndefined() and dto.balance >= 0
  endif

Technical constraint:
- If the user creates a 'Savings' or 'Investment' account, the initial balance must be at least 50,000.
- For other account types, the balance can be 0 or more.

## Row 128

Column B:

BR-ACC-16: Financial capacity proof for Investment accounts
context AccountService::create(
  userId : Integer,
  dto : CreateAccountDto
) : AccountResponseDto

pre BR_ACC_16_InvestmentCapacity:
  dto.account_type = 'Investment' implies
    Account.allInstances()
      ->select(a | a.user_id = userId and (a.account_type = 'Checking' or a.account_type = 'Savings'))
      ->collect(balance)
      ->sum() >= 100000
      
Technical constraint:
- If a user attempts to create an 'Investment' account, the backend must query the user's existing accounts.
- The creation is only allowed if the sum of the balances of all the user's existing 'Checking' and 'Savings' accounts is greater than or equal to 100,000.
- If the user does not meet this financial capacity requirement, the request must be rejected.

## Row 129

Column A:

Related UI

Column B:

AddAccountPage; AddAccountForm; route /accounts/add

## Row 130

Column A:

Related API IDs

Column B:

API-ACCOUNT-CREATE

## Row 131

Column A:

Notes

## Row 133

Column A:

UC-07 - View Bank Account Details

## Row 134

Column A:

Use Case ID

Column B:

UC-07

## Row 135

Column A:

Use Case Name

Column B:

View Bank Account Details

## Row 136

Column A:

Description

Column B:

As an authenticated account owner, I want to view one account and its five most recent transactions.

## Row 137

Column A:

Actor(s)

Column B:

Authenticated User

## Row 138

Column A:

Priority

Column B:

Not Specified

## Row 139

Column A:

Trigger

Column B:

The user selects an account card.

## Row 140

Column A:

Pre-Condition(s)

Column B:

PRE-1: The user is authenticated.
PRE-2: The path contains an account identifier.

## Row 141

Column A:

Post-Condition(s)

Column B:

POST-1: On success, the page displays account information and at most five recent transactions.
POST-2: Expense amounts in recent_transactions are returned as negative values.
POST-3: Unauthorized account data is not returned.

## Row 142

Column A:

Basic Flow

Column B:

1. The user selects an account card and opens /accounts/:id.
2. AccountDetailPage requests GET /api/v1/accounts/:id.
3. The controller validates authentication and parses id as an integer.
4. AccountService loads the account by accountId.
5. AccountService verifies account.userId equals the authenticated userId.
6. AccountService loads at most five transactions for the account, ordered by transactionDate descending.
7. AccountService maps transaction dates to YYYY-MM-DD and makes Expense amounts negative.
8. The frontend displays bank name, type, branch, full account number, balance, and recent transactions.

## Row 143

Column A:

Alternative Flow

Column B:

AF-1: No recent transactions
6a. The query returns an empty array.
8a. The account information remains visible with an empty recent-transactions section.

## Row 144

Column A:

Exception Flow

Column B:

EF-1: Invalid account ID
3a. The controller returns HTTP 400.

EF-2: Account not found
4a. The backend returns HTTP 404.

EF-3: Account belongs to another user
5a. The backend returns HTTP 403.

EF-4: Retrieval failure
6a. The backend returns HTTP 500 and the frontend displays its error state.

## Row 145

Column A:

UML Model

Column B:

@startuml

class User <<Entity>> {
  user_id: Integer [1]
  full_name: String [1]
  email: String [1]
  username: String [1]
  password: String [1]
  phone_number: String [0..1]
  profile_picture_url: String [0..1]
  total_balance: Decimal [1]
}

class Account <<Entity>> {
  account_id: Integer [1]
  user_id: Integer [1]
  bank_name: String [1]
  account_type: AccountType [1]
  branch_name: String [0..1]
  account_number_full: String [1]
  account_number_last_4: String [1]
  balance: Decimal [1]
}

enum AccountType {
  Checking
  Credit_Card
  Savings
  Investment
  Loan
}

class Transaction <<Entity>> {
  transaction_id: Integer [1]
  account_id: Integer [1]
  category_id: Integer [0..1]
  transaction_date: Date [1]
  type: TransactionTypeEnum [1]
  item_description: String [1]
  shop_name: String [0..1]
  amount: Decimal [1]
  payment_method: String [0..1]
  status: TransactionStatus [1]
  receipt_id: String [0..1]
}

enum TransactionTypeEnum {
  Revenue
  Expense
}

enum TransactionStatus {
  Complete
  Pending
  Failed
}

class TransactionDto <<DTO>> {
  date: String [1]
  amount: Decimal [1]
  description: String [1]
  status: TransactionStatus [1]
  receipt_id: String [0..1]
  type: TransactionTypeEnum [1]
}

class AccountDetailResponseDto <<DTO>> {
  id: Integer [1]
  bank_name: String [1]
  account_type: AccountType [1]
  branch_name: String [0..1]
  account_number_full: String [1]
  balance: Decimal [1]
  recent_transactions: TransactionDto [0..5]
}

class AccountService <<Service>> {
  findOneWithTransactions(accountId: Integer, userId: Integer): AccountDetailResponseDto
}

User "1" -- "0..*" Account : owns
Account "1" -- "0..*" Transaction : has
AccountService ..> AccountDetailResponseDto
AccountDetailResponseDto *-- "0..5" TransactionDto : contains
AccountDetailResponseDto ..> Account : maps from
TransactionDto ..> Transaction : maps from

@enduml

## Row 146

Column A:

Business Rules

Column B:

BR-ACC-15: Account existence and ownership
context AccountService::findOneWithTransactions(
  accountId : Integer,
  userId : Integer
) : AccountDetailResponseDto
pre BR_ACC_15_AccountMustBeOwned:
  Account.allInstances()->exists(a | 
    a.account_id = accountId and 
    a.user_id = userId
  )

## Row 147

Column B:

BR-ACC-16: Five most recent account transactions
context AccountService::findOneWithTransactions(
  accountId : Integer,
  userId : Integer
) : AccountDetailResponseDto
post BR_ACC_16_MaxFiveRecentTransactions:
  result.recent_transactions->size() <= 5
post BR_ACC_16_OrderedByDateDescending:
  result.recent_transactions->size() <= 1 or
  Sequence{1..result.recent_transactions->size()-1}->forAll(i |
    result.recent_transactions->at(i).date >= result.recent_transactions->at(i + 1).date
  )
Technical constraint:
- The backend shall return at most five transactions ordered by transaction_date descending.

## Row 148

Column B:

BR-ACC-17: Response rows map to persisted data with signed amounts
context AccountService::findOneWithTransactions(
  accountId : Integer,
  userId : Integer
) : AccountDetailResponseDto
post BR_ACC_17_ResponseBackedByAccount:
  Account.allInstances()->exists(a |
    a.account_id = result.id and
    a.user_id = userId and
    a.bank_name = result.bank_name and
    a.account_type = result.account_type and
    (a.branch_name.oclIsUndefined() implies result.branch_name.oclIsUndefined()) and
    (not a.branch_name.oclIsUndefined() implies a.branch_name = result.branch_name) and
    a.account_number_full = result.account_number_full and
    a.balance = result.balance
  )
post BR_ACC_17_ResponseBackedByTransaction:
  result.recent_transactions->forAll(tDto |
    Transaction.allInstances()->exists(t |
      t.account_id = accountId and
      t.item_description = tDto.description and
      ((t.type = TransactionTypeEnum::Expense and tDto.amount = -(t.amount)) or
       (t.type = TransactionTypeEnum::Revenue and tDto.amount = t.amount)) and
      t.status = tDto.status and
      (t.receipt_id.oclIsUndefined() implies tDto.receipt_id.oclIsUndefined()) and
      (not t.receipt_id.oclIsUndefined() implies t.receipt_id = tDto.receipt_id) and
      t.type = tDto.type and
      tDto.date = toIsoDate(t.transaction_date)
    )
  )
Technical constraint:
- In the account-detail mapping, Expense amounts are negated (returned as negative) and Revenue amounts remain positive.
- Unused persisted fields in Transaction (e.g., shop_name, payment_method, category_id) are intentionally excluded from the returned TransactionDto.

## Row 149

Column B:

post BR_ACC_18_AccountIdentityUnchanged:
  Account.allInstances()->collect(a | a.account_id)->asSet() =
  Account.allInstances()@pre->collect(a | a.account_id)->asSet()
post BR_ACC_18_AccountDataUnchanged:
  Account.allInstances()->forAll(a |
    Account.allInstances()@pre->exists(old |
      old.account_id = a.account_id and
      old.user_id = a.user_id and
      old.bank_name = a.bank_name and
      old.account_type = a.account_type and
      old.branch_name = a.branch_name and
      old.account_number_full = a.account_number_full and
      old.account_number_last_4 = a.account_number_last_4 and
      old.balance = a.balance
    )
  )
post BR_ACC_18_TransactionIdentityUnchanged:
  Transaction.allInstances()->collect(t | t.transaction_id)->asSet() =
  Transaction.allInstances()@pre->collect(t | t.transaction_id)->asSet()
post BR_ACC_18_TransactionDataUnchanged:
  Transaction.allInstances()->forAll(t |
    Transaction.allInstances()@pre->exists(old |
      old.transaction_id = t.transaction_id and
      old.account_id = t.account_id and
      old.category_id = t.category_id and
      old.transaction_date = t.transaction_date and
      old.type = t.type and
      old.item_description = t.item_description and
      old.shop_name = t.shop_name and
      old.amount = t.amount and
      old.payment_method = t.payment_method and
      old.status = t.status and
      old.receipt_id = t.receipt_id
    )
  )
Technical constraint:
- Viewing account details shall not create, update, or delete any Account or Transaction records.

## Row 150

Column A:

Related UI

Column B:

AccountDetailPage; route /accounts/:id

## Row 151

Column A:

Related API IDs

Column B:

API-ACCOUNT-DETAIL

## Row 152

Column A:

Notes

## Row 155

Column A:

UC-08 - Edit a Bank Account

## Row 156

Column A:

Use Case ID

Column B:

Use Case ID

## Row 157

Column A:

Use Case Name

Column B:

Edit a Bank Account

## Row 158

Column A:

Description

Column B:

As an authenticated account owner, I want to edit an account's bank name, type, branch, full account number, and balance.

## Row 159

Column A:

Actor(s)

Column B:

Authenticated User

## Row 160

Column A:

Priority

Column B:

Not Specified

## Row 161

Column A:

Trigger

Column B:

The user selects Edit on an account detail page.

## Row 162

Column A:

Pre-Condition(s)

Column B:

PRE-1: The user is authenticated.
PRE-2: The account exists and is owned by the authenticated user.
PRE-3: Account details have been loaded.

## Row 163

Column A:

Post-Condition(s)

Column B:

POST-1: On success, the account fields are overwritten with the submitted values.
POST-2: account_number_last_4 is implicitly derived by the backend from the submitted account_number_full.
POST-3: On success, the system displays a success toast notification ("Update successful"), waits 1500 ms, closes the edit form, and reloads the account details to reflect the updated data.
POST-4: On failure, the stored account remains unchanged by the failed request.

## Row 164

Column A:

Basic Flow

Column B:

1. The user opens an account detail page and selects Edit.
2. AccountEditForm is populated from loaded AccountDetail data.
3. The user changes bank_name, account_type, optional branch_name, account_number_full, or balance.
4. The user selects Save Changes.
5. The frontend validates required fields (bank_name, account_number_full), allowed account_type, valid account_number_full format (8-34 digits), and numeric non-negative balance.
6. The frontend sends PUT /api/v1/accounts/:id with all update fields (excluding account_number_last_4).
7. The controller validates that id parses to an integer.
8. AccountService verifies that the account exists and belongs to userId.
9. ValidationPipe and AccountService validate the submitted fields.
10. AccountService derives account_number_last_4, overwrites the account fields, and saves the row.
11. The frontend displays a success toast, waits 1500ms, and invokes its success callback; AccountDetailPage reloads account data and exits edit mode.

## Row 165

Column A:

Alternative Flow

Column B:

AF-1: Optional branch omitted
3a. The user clears branch_name.
10a. The backend stores branchName as undefined/null.

AF-2: Cancel
4a. The user selects Cancel and the detail page exits edit mode without sending an update request.

## Row 166

Column A:

Exception Flow

Column B:

EF-1: Client-side or DTO validation failure
5a. The frontend displays field errors, or the backend returns HTTP 400.

EF-2: Account not found
8a. The backend returns HTTP 404.

EF-3: Account belongs to another user
8a. The backend returns HTTP 403 and the frontend displays its permission error.

EF-4: Storage failure
10a. The backend returns HTTP 500 and the frontend displays its save failure message.

## Row 167

Column A:

UML Model

Column B:

@startuml

class User <<Entity>> {
  user_id: Integer [1]
  full_name: String [1]
  email: String [1]
  username: String [1]
  password: String [1]
  phone_number: String [1]
  profile_picture_url: String [1]
  total_balance: Decimal [1]
}

class Account <<Entity>> {
  account_id: Integer [1]
  user_id: Integer [1]
  bank_name: String [1]
  account_type: AccountType [1]
  branch_name: String [0..1]
  account_number_full: String [1]
  account_number_last_4: String [1]
  balance: Decimal [1]
}

enum AccountType {
  Checking
  Credit_Card
  Savings
  Investment
  Loan
}
note right of AccountType
  Credit_Card maps to database literal 'Credit Card'.
end note

class UpdateAccountDto <<DTO>> {
  bank_name: String [1]
  account_type: AccountType [1]
  branch_name: String [0..1]
  account_number_full: String [1]
  balance: Decimal [1]
}
note left of UpdateAccountDto
  account_number_last_4 is deliberately omitted 
  from input to enforce backend derivation.
end note

class UpdatedAccountDto <<DTO>> {
  account_id: Integer [1]
  user_id: Integer [1]
  bank_name: String [1]
  account_type: AccountType [1]
  branch_name: String [0..1]
  account_number_full: String [1]
  account_number_last_4: String [1]
  balance: Decimal [1]
}

class UpdateAccountResponseDto <<DTO>> {
  message: String [1]
  account: UpdatedAccountDto [1]
}

class AccountService <<Service>> {
  update(accountId: Integer, userId: Integer, dto: UpdateAccountDto): UpdatedAccountDto
}

User "1" -- "0..*" Account : owns
AccountService ..> UpdatedAccountDto
AccountService ..> UpdateAccountDto
UpdateAccountDto ..> Account : mapped to
UpdatedAccountDto ..> Account : mapped from
UpdateAccountResponseDto *-- "1" UpdatedAccountDto : contains

@enduml

## Row 168

Column A:

Business Rules

Column B:

BR-ACC-19: Account ownership validation for update
context AccountService::update(
  accountId : Integer,
  userId : Integer,
  dto : UpdateAccountDto
) : UpdatedAccountDto
pre BR_ACC_19_MustOwnAccount:
  Account.allInstances()->exists(a |
    a.account_id = accountId and
    a.user_id = userId
  )

## Row 169

Column B:

BR-ACC-20: Allowed account types for update
context AccountService::update(
  accountId : Integer,
  userId : Integer,
  dto : UpdateAccountDto
) : UpdatedAccountDto
pre BR_ACC_20_ValidType:
  Set{AccountType::Checking, AccountType::Credit_Card, AccountType::Savings, AccountType::Investment, AccountType::Loan}->includes(dto.account_type)

## Row 170

Column B:

BR-ACC-21: Required account text fields for update
context AccountService::update(
  accountId : Integer,
  userId : Integer,
  dto : UpdateAccountDto
) : UpdatedAccountDto
pre BR_ACC_21_RequiredText:
  not dto.bank_name.oclIsUndefined() and dto.bank_name.trim().size() > 0 and
  not dto.account_number_full.oclIsUndefined() and dto.account_number_full.trim().size() > 0

## Row 171

Column B:

BR-ACC-22: Account number format and length for update
context AccountService::update(
  accountId : Integer,
  userId : Integer,
  dto : UpdateAccountDto
) : UpdatedAccountDto
pre BR_ACC_22_NumericCharactersOnly:
  not dto.account_number_full.oclIsUndefined() and 
  matches(dto.account_number_full, '^[0-9]+$')
pre BR_ACC_22_LengthConstraints:
  dto.account_number_full.size() >= 8 and dto.account_number_full.size() <= 34

## Row 172

Column B:

BR-ACC-23: Numeric non-negative account balance for update
context AccountService::update(
  accountId : Integer,
  userId : Integer,
  dto : UpdateAccountDto
) : UpdatedAccountDto
pre BR_ACC_23_IsNumeric:
  dto.balance.oclIsTypeOf(Real) or dto.balance.oclIsTypeOf(Integer)
pre BR_ACC_23_NonNegativeBalance:
  not dto.balance.oclIsUndefined() and dto.balance >= 0

## Row 173

Column B:

BR-ACC-24: Optional branch name handling during update
context AccountService::update(
  accountId : Integer,
  userId : Integer,
  dto : UpdateAccountDto
) : UpdatedAccountDto
pre BR_ACC_24_BranchNameOptional:
  dto.branch_name.oclIsUndefined() or dto.branch_name.oclIsTypeOf(String)

## Row 174

Column B:

BR-ACC-25: Derive final four account characters for update
context AccountService::update(
  accountId : Integer,
  userId : Integer,
  dto : UpdateAccountDto
) : UpdatedAccountDto
post BR_ACC_25_DeriveLast4:
  let updatedAcc = Account.allInstances()->any(a | a.account_id = accountId) in
  updatedAcc.account_number_last_4 = dto.account_number_full.substring(
    dto.account_number_full.size() - 3, 
    dto.account_number_full.size()
  )
Technical constraint:
- The backend MUST implicitly derive account_number_last_4 by taking the exact last 4 characters of the submitted account_number_full.

## Row 175

Column B:

BR-ACC-26: Account update persistence mapping
context AccountService::update(
  accountId : Integer,
  userId : Integer,
  dto : UpdateAccountDto
) : UpdatedAccountDto
post BR_ACC_26_StorageMapping:
  Account.allInstances()->exists(a |
    a.account_id = accountId and
    a.bank_name = dto.bank_name and
    a.account_type = dto.account_type and
    (dto.branch_name.oclIsUndefined() implies a.branch_name.oclIsUndefined()) and
    (not dto.branch_name.oclIsUndefined() implies a.branch_name = dto.branch_name) and
    a.account_number_full = dto.account_number_full and
    a.balance = dto.balance
  )

## Row 176

Column A:

Related UI

Column B:

AccountDetailPage; AccountEditForm; route /accounts/:id

## Row 177

Column A:

Related API IDs

Column B:

API-ACCOUNT-UPDATE

## Row 178

Column A:

Notes

Column B:

Clarification: When account_number_full is changed, the new value must remain unique among the authenticated user's accounts.

## Row 182

Column A:

UC-08a - Quick edit a bank account

## Row 183

Column A:

Use Case ID

Column B:

UC-08a

## Row 184

Column A:

Use Case Name

Column B:

Quick Edit Account

## Row 185

Column A:

Description

Column B:

As an authenticated account owner, I want to quickly enter an edit mode directly from the Accounts page to modify account details without navigating to the account detail page.

## Row 186

Column A:

Actor(s)

Column B:

Authenticated User

## Row 187

Column A:

Priority

Column B:

Medium

## Row 188

Column A:

Trigger

Column B:

The user selects "Edit Accounts" on the Account List (Balances) page.

## Row 189

Column A:

Pre-Condition(s)

Column B:

PRE-1: The user is authenticated.
PRE-2: The Accounts page has been loaded and displays at least one account card.

## Row 190

Column A:

Post-Condition(s)

Column B:

POST-1: On success, the selected account's fields are overwritten with the submitted values.
POST-2: account_number_last_4 is implicitly derived by the backend from the submitted account_number_full.
POST-3: On success, the system displays a success toast notification (""Update successful""), waits 1500 ms, closes the edit form, and reloads the account list to reflect the updated data.
POST-4: On failure or cancellation, the stored account remains unchanged.

## Row 191

Column A:

Basic Flow

Column B:

1. The user opens /accounts and selects ""Edit Accounts"".
2. The frontend switches the Accounts page into Edit Mode, displaying a pencil icon on each account card.
3. The user selects the pencil icon for a specific account.
4. AccountEditForm is loaded and populated from the loaded account card data.
5. The user changes bank_name, account_type, optional branch_name, account_number_full, or balance.
6. The user selects Save Changes.
7. The frontend validates required fields (bank_name, account_number_full), allowed account_type, valid account_number_full format (8-34 digits), and numeric non-negative balance.
8. The frontend sends PUT /api/v1/accounts/:id with all update fields (excluding account_number_last_4).
9. The controller validates that id parses to an integer.
10. AccountService verifies that the account exists and belongs to userId.
11. ValidationPipe and AccountService validate the submitted fields.
12. AccountService derives account_number_last_4, overwrites the account fields, and saves the row.
13. The frontend displays a success toast, waits 1500ms, and invokes its success callback; the Accounts page reloads account data and exits edit mode.

## Row 192

Column A:

Alternative Flow

Column B:

AF-1: Cancel Edit Mode
2a. The user toggles ""Edit Accounts"" again to exit edit mode.
2b. The frontend hides the pencil icons and exits edit mode.

AF-2: Optional branch omitted
5a. The user clears branch_name.
12a. The backend stores branchName as undefined/null.

AF-3: Cancel Form
6a. The user selects Cancel on the AccountEditForm.
6b. The frontend closes the form without sending an update request, and the Accounts page remains in Edit Mode.

## Row 193

Column A:

Exception Flow

Column B:

Identical to UC-08 (EF-1 through EF-4)

## Row 194

Column A:

UML Model

Column B:

Identical to UC-08

## Row 195

Column A:

Business Rules

Column B:

Identical to UC-08 (BR-ACC-19 through BR-ACC-26).

## Row 196

Column A:

Related UI

Column B:

AccountListPage; AccountEditForm; route /accounts

## Row 197

Column A:

Related API IDs

Column B:

API-ACCOUNT-UPDATE

## Row 198

Column A:

Notes

Column B:

Rationale: This is a UI-level quick-edit variant of UC-08. It reuses the UC-08 account-update API and renders AccountEditForm within AccountListPage; no separate backend operation is required.

## Row 202

Column A:

UC-09 - Delete a Bank Account

## Row 203

Column A:

Use Case ID

Column B:

UC-09

## Row 204

Column A:

Use Case Name

Column B:

Delete a Bank Account

## Row 205

Column A:

Description

Column B:

As an authenticated account owner, I want to permanently delete an account and its related transactions.

## Row 206

Column A:

Actor(s)

Column B:

Authenticated User

## Row 207

Column A:

Priority

Column B:

Not Specified

## Row 208

Column A:

Trigger

Column B:

The user selects Delete from an account card or account detail page.

## Row 209

Column A:

Pre-Condition(s)

Column B:

PRE-1: The user is authenticated.
PRE-2: The account exists and is owned by the authenticated user.

## Row 210

Column A:

Post-Condition(s)

Column B:

POST-1: On confirmed success, all Transaction rows with the accountId and the Account row are deleted in one database transaction.
POST-2: On confirmed success, the system displays a success dialog, waits 1500ms, and then refreshes the account list or navigates to /accounts.
POST-3: On cancellation or rollback, no deletion is committed.

## Row 211

Column A:

Basic Flow

Column B:

1. The user selects Delete for an account.
2. Delete Account Modal displays the bank name, final four account digits, and a warning that all related transactions will be deleted.
3. The user selects Confirm Delete.
4. The frontend sends DELETE /api/v1/accounts/:id.
5. The controller validates that id parses to an integer.
6. AccountService starts a database transaction, loads the account, and verifies ownership.
7. AccountService deletes related Transaction rows.
8. AccountService deletes the Account row and commits the transaction.
9. The frontend closes the modal, displays a success dialog, waits 1500ms, and then refreshes the list or navigates to /accounts.

## Row 212

Column A:

Alternative Flow

Column B:

AF-1: Cancel deletion
3a. The user selects Cancel or closes the modal.
3b. No API request is sent and no data changes.

## Row 213

Column A:

Exception Flow

Column B:

EF-1: Invalid account ID
5a. The controller returns HTTP 400.

EF-2: Missing or non-owned account
6a. The service rolls back and returns HTTP 404 using the same message for both cases.

EF-3: Database deletion failure
7a. The service rolls back the transaction and returns HTTP 500.

## Row 214

Column A:

UML Model

Column B:

@startuml

class User <<Entity>> {
  user_id: Integer [1]
  full_name: String [1]
  email: String [1]
  username: String [1]
  password: String [1]
  phone_number: String [1]
  profile_picture_url: String [1]
  total_balance: Decimal [1]
}

class Account <<Entity>> {
  account_id: Integer [1]
  user_id: Integer [1]
  bank_name: String [1]
  account_type: AccountType [1]
  branch_name: String [0..1]
  account_number_full: String [1]
  account_number_last_4: String [1]
  balance: Decimal [1]
}

class Transaction <<Entity>> {
  transaction_id: Integer [1]
  account_id: Integer [1]
  transaction_date: Date [1]
  type: TransactionType [1]
  item_description: String [1]
  shop_name: String [0..1]
  amount: Decimal [1]
  payment_method: String [0..1]
  status: TransactionStatus [1]
  receipt_id: String [0..1]
  category_id: Integer [0..1]
}

enum AccountType {
  Checking
  Credit_Card
  Savings
  Investment
  Loan
}

enum TransactionType {
  Revenue
  Expense
}

enum TransactionStatus {
  Complete
  Pending
  Failed
}

class DeleteAccountResponseDto <<DTO>> {
  message: String [1]
  deleted_account_id: Integer [1]
}

class AccountService <<Service>> {
  delete(accountId: Integer, userId: Integer): DeleteAccountResponseDto
}

User "1" -- "0..*" Account : owns
Account "1" -- "0..*" Transaction : contains
AccountService ..> DeleteAccountResponseDto
AccountService ..> Account : deletes
AccountService ..> Transaction : deletes cascade

@enduml

Column C:

  

## Row 215

Column A:

Business Rules

Column B:

BR-ACC-27: Account deletion ownership validation
context AccountService::delete(accountId : Integer, userId : Integer) : DeleteAccountResponseDto
pre BR_ACC_27_MustOwnAccount:
  Account.allInstances()->exists(a | a.account_id = accountId and a.user_id = userId)
Technical constraint:
- If the account does not exist or does not belong to the user, the backend intentionally throws a 404 NotFoundException to prevent data 
enumeration.

## Row 216

Column B:

BR-ACC-28: Account deletion data integrity (Cascading)
context AccountService::delete(accountId : Integer, userId : Integer) : DeleteAccountResponseDto
post BR_ACC_28_AtomicDeletion:
  not Account.allInstances()->exists(a | a.account_id = accountId) and
  not Transaction.allInstances()->exists(t | t.account_id = accountId)
Technical constraint:
- The backend MUST execute the deletion of all related Transaction rows and the Account row within a single atomic database transaction (using QueryRunner). If any step fails, the entire transaction rolls back.

## Row 217

Column A:

Related UI

Column B:

AccountListPage; AccountDetailPage; DeleteAccountModal

## Row 218

Column A:

Related API IDs

Column B:

API-ACCOUNT-DELETE

## Row 219

Column A:

Notes

Column B:

Security rationale: An account that does not exist and an account not owned by the authenticated user are both reported as HTTP 404, rather than 403, to avoid disclosing the existence of another user's account.

## Row 221

Column A:

UC-10 - View Monthly Expense Summary

## Row 222

Column A:

Use Case ID

Column B:

UC-10

## Row 223

Column A:

Use Case Name

Column B:

View Monthly Expense Summary

## Row 224

Column A:

Description

Column B:

As an authenticated user, I want to view a monthly expense comparison so that I can understand my spending over time.

## Row 225

Column A:

Actor(s)

Column B:

Authenticated User

## Row 226

Column A:

Priority

Column B:

Not Specified

## Row 227

Column A:

Trigger

Column B:

The user opens the Expenses page.

## Row 228

Column A:

Pre-Condition(s)

Column B:

PRE-1: The user is authenticated.

## Row 229

Column A:

Post-Condition(s)

Column B:

POST-1: If expense summary data is available, the monthly expense comparison is displayed.

POST-2: If no expense summary data is available, the no-data state is displayed.

POST-3: The operation does not intentionally modify financial data.

## Row 230

Column A:

Basic Flow

Column B:

1. The user opens the Expenses page.
2. The frontend requests the user's monthly expense summary.
3. The backend authenticates the request.
4. The backend retrieves and aggregates the relevant expense data.
5. The backend returns the monthly expense summary.
6. The frontend prepares the returned data for visualization.
7. The frontend displays the monthly expense comparison chart.

## Row 231

Column A:

Alternative Flow

Column B:

AF-1: No expense summary data
5a. The backend returns an empty summary.
6a. The frontend does not prepare chart data.
7a. The frontend displays the no-data state.

AF-2: Partial monthly data
5b. The backend returns the available monthly summary data.
6b. The frontend prepares the data according to the applicable business rules.
7b. The frontend displays the resulting chart.

## Row 232

Column A:

Exception Flow

Column B:

EF-1: Authentication failure
3a. Authentication fails.
3b. The backend returns HTTP 401.
3c. The frontend applies the application's authentication-error handling.

EF-2: Retrieval or aggregation failure
4a. An unexpected retrieval or aggregation error occurs.
4b. The backend returns HTTP 500.
4c. The frontend displays its expense-loading error state.

## Row 233

Column A:

UML Model

Column B:

@startuml

class Account <<Entity>> {
  accountId: Integer [1]
  userId: Integer [1]
}

class Transaction <<Entity>> {
  transactionId: Integer [1]
  accountId: Integer [1]
  transactionDate: Date [1]
  type: TransactionType [1]
  amount: Decimal [1]
  status: TransactionStatus [1]
}

enum TransactionType {
  Revenue
  Expense
}

class AuthenticatedRequest <<DTO>> {
  userId: Integer [1]
}

class ExpenseSummaryItem <<DTO>> {
  month: String [1]
  totalExpense: Decimal [1]
}

class ExpenseSummaryResponseDto <<DTO>> {
  data: ExpenseSummaryItem [0..*]
}

class JwtAuthGuard <<Guard>> {
  validate(token: BearerJWT): AuthenticatedRequest
}

class ExpensesController <<Controller>> {
  getExpenseSummary(request: AuthenticatedRequest): ExpenseSummaryResponseDto
}

class ExpensesService <<Service>> {
  getExpenseSummary(userId: Integer): Sequence(ExpenseSummaryItem)
}

Account "1" -- "0..*" Transaction : contains
ExpensesController ..> JwtAuthGuard : protected by
ExpensesController ..> ExpensesService
ExpensesController ..> ExpenseSummaryResponseDto : returns
ExpensesService ..> Account
ExpensesService ..> Transaction
ExpenseSummaryResponseDto --> ExpenseSummaryItem

@enduml

## Row 234

Column A:

Business Rules

Column B:

BR-EXP-01: Ownership scope

context ExpensesService::getExpenseSummary(
  userId : Integer
) : Sequence(ExpenseSummaryItem)

pre BR_EXP_01_AuthenticatedIdentity:
  not userId.oclIsUndefined()

post BR_EXP_01_OwnedTransactionsOnly:
  let ownedAccountIds : Set(Integer) =
    Account.allInstances()
      ->select(a |
        a.userId = userId
      )
      ->collect(a |
        a.accountId
      )
      ->asSet()
  in
    result->forAll(item |
      Transaction.allInstances()->forAll(t |
        contributesTo(t, item)
        implies
        ownedAccountIds->includes(t.accountId)
      )
    )

Technical constraints:
- Only transactions associated with accounts owned by the authenticated user may contribute to the expense summary.
- The aggregation userId shall come from the validated JWT and shall not be supplied or overridden by the client.

BR-EXP-02: Expense eligibility

context ExpensesService::getExpenseSummary(
  userId : Integer
) : Sequence(ExpenseSummaryItem)

post BR_EXP_02_ExpenseOnly:
  result->forAll(item |
    Transaction.allInstances()
      ->select(t |
        monthOf(t.transactionDate) =
          monthNumber(item.month)
      )
      ->forAll(t |
        contributesTo(t, item)
        implies
        t.type = TransactionType::Expense
      )
  )

Technical constraints:
- Only transactions with `type = Expense` contribute to the summary.
- Revenue transactions shall not contribute to any monthly expense total.

BR-EXP-03: Reporting period

context ExpensesService::getExpenseSummary(
  userId : Integer
) : Sequence(ExpenseSummaryItem)

post BR_EXP_03_CurrentCalendarYearOnly:
  result->forAll(item |
    Transaction.allInstances()
      ->select(t |
        monthOf(t.transactionDate) =
          monthNumber(item.month)
      )
      ->forAll(t |
        contributesTo(t, item)
        implies
        yearOf(t.transactionDate) = currentYear()
      )
  )

Technical constraints:
- Only transactions whose `transactionDate` falls in the backend server's current calendar year are included.
- The endpoint does not accept a year parameter.

## Row 235

Column B:

BR-EXP-04: Monthly attribution

context ExpensesService::getExpenseSummary(
  userId : Integer
) : Sequence(ExpenseSummaryItem)

post BR_EXP_04_TransactionDateDeterminesMonth:
  result->forAll(item |
    Transaction.allInstances()->forAll(t |
      contributesTo(t, item)
      implies
      monthOf(t.transactionDate) =
        monthNumber(item.month)
    )
  )

Technical constraints:
- A transaction belongs to the month represented by its `transactionDate`, not another system timestamp.

BR-EXP-05: Monthly aggregation

context ExpensesService::getExpenseSummary(
  userId : Integer
) : Sequence(ExpenseSummaryItem)

post BR_EXP_05_MonthlyExpenseTotal:
  let ownedAccountIds : Set(Integer) =
    Account.allInstances()
      ->select(a |
        a.userId = userId
      )
      ->collect(a |
        a.accountId
      )
      ->asSet()
  in
    result->forAll(item |
      item.totalExpense =
        Transaction.allInstances()
          ->select(t |
            ownedAccountIds->includes(t.accountId) and
            t.type = TransactionType::Expense and
            yearOf(t.transactionDate) = currentYear() and
            monthOf(t.transactionDate) =
              monthNumber(item.month)
          )
          ->collect(t |
            t.amount
          )
          ->sum()
    )

Technical constraints:
- A month's `totalExpense` equals the sum of `amount` for all eligible transactions assigned to that month.

## Row 236

Column B:

BR-EXP-06: Backend result semantics

context ExpensesService::getExpenseSummary(
  userId : Integer
) : Sequence(ExpenseSummaryItem)

post BR_EXP_06_UniqueMonth:
  result->isUnique(item |
    item.month
  )

post BR_EXP_06_ValidMonth:
  result->forAll(item |
    monthNumber(item.month) >= 1 and
    monthNumber(item.month) <= 12
  )

post BR_EXP_06_ChronologicalOrder:
  result->size() <= 1 or
  Sequence{1..result->size() - 1}->forAll(i |
    monthNumber(result->at(i).month) <
    monthNumber(result->at(i + 1).month)
  )

Technical constraints:
- The backend returns only months containing eligible expense data.
- Each returned month shall appear at most once and results shall be ordered chronologically.
- `month` shall use Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, or Dec.
- The backend shall not generate zero-valued entries solely to fill missing calendar months.

BR-EXP-07: Missing-month normalization

context ExpenseSummaryChart::buildChartData(
  summaryData : Sequence(ExpenseSummaryItem)
) : Sequence(ExpenseChartItem)

pre BR_EXP_07_HasSummaryData:
  summaryData->notEmpty()

post BR_EXP_07_TwelveMonths:
  result->size() = 12

post BR_EXP_07_UniqueMonth:
  result->isUnique(item |
    item.month
  )

post BR_EXP_07_AllCalendarMonths:
  Set{'Jan', 'Feb', 'Mar', 'Apr',
      'May', 'Jun', 'Jul', 'Aug',
      'Sep', 'Oct', 'Nov', 'Dec'}
  =
  result->collect(item |
    item.month
  )->asSet()

post BR_EXP_07_PreserveReturnedTotals:
  summaryData->forAll(source |
    result->one(item |
      item.month = source.month and
      item.totalExpense = source.totalExpense
    )
  )

post BR_EXP_07_MissingMonthIsZero:
  result->forAll(item |
    summaryData->forAll(source |
      source.month <> item.month
    )
    implies
      item.totalExpense = 0
  )

Technical constraints:
- When at least one monthly result exists, the frontend constructs Jan–Dec and assigns `0` to missing months.

## Row 237

Column A:

Related UI

Column B:

ExpensesPage; ExpenseSummaryChart; route /expenses

## Row 238

Column A:

Related API IDs

Column B:

API-EXPENSE-SUMMARY

## Row 239

Column A:

Notes

Column B:

Experiment classification:
- BR-EXP-01 through BR-EXP-07 are the treatment-sensitive Business Rules used for the core Business Rule effectiveness score.
- The current-month color treatment is a Figma-derived UI requirement and is not a core Business Rule.
- Read-only behavior is redundantly constrained by the GET method.
- The successful response envelope is project-constrained by PROJECT_CONTEXT.md and AGENTS.md.

## Row 241

Column A:

UC-11 - View Expenses by Category

## Row 242

Column A:

Use Case ID

Column B:

UC-11

## Row 243

Column A:

Use Case Name

Column B:

View Expenses by Category

## Row 244

Column A:

Description

Column B:

As an authenticated user, I want to view my expenses by category for a selected month so that I can understand how my spending is distributed.

## Row 245

Column A:

Actor(s)

Column B:

Authenticated User

## Row 246

Column A:

Priority

Column B:

Not Specified

## Row 247

Column A:

Trigger

Column B:

The user opens the Expenses page or selects another month.

## Row 248

Column A:

Pre-Condition(s)

Column B:

PRE-1: The user is authenticated.
PRE-2: A selected month is available for the expense-breakdown request.

## Row 249

Column A:

Post-Condition(s)

Column B:

POST-1: After processing, the expense breakdown for the selected month is displayed on /expenses.
POST-2: If no breakdown data is available, the page displays its no-data state.
POST-3: The operation does not modify stored financial data.

## Row 250

Column A:

Basic Flow

Column B:

1. The user opens the Expenses page.
2. The frontend determines the selected month for the breakdown request.
3. The frontend requests the user's expense breakdown for the selected month.
4. The backend authenticates the request.
5. The backend retrieves and processes the relevant expense data according to the applicable business rules.
6. The backend returns the expense breakdown.
7. The frontend displays the category breakdown on the Expenses page.

## Row 251

Column A:

Alternative Flow

Column B:

AF-1: Select another month
2a. The user selects a different month.
3a. The frontend requests the expense breakdown for the new selected month.
4a. The flow continues from Step 4.

AF-2: No breakdown data
6a. The backend reports that no breakdown data is available for the selected month.
7a. The frontend displays its no-data state instead of the category breakdown.

## Row 252

Column A:

Exception Flow

Column B:

EF-1: Authentication failure
4a. The backend cannot authenticate the request.
4b. The backend returns HTTP 401.
4c. The frontend applies the application's authentication-error handling.

EF-2: Invalid month request
5a. The backend rejects an invalid month request with HTTP 400.
5b. The frontend displays its request-error state.

EF-3: Retrieval or processing failure
5a. An unexpected error occurs while retrieving or processing the breakdown data.
5b. The backend returns HTTP 500.
5c. The frontend displays its expense-breakdown error state.

## Row 253

Column A:

UML Model

Column B:

@startuml

class AuthenticatedRequest <<DTO>> {
  userId: Integer [1]
}

class Account <<Entity>> {
  accountId: Integer [1]
  userId: Integer [1]
}

class Transaction <<Entity>> {
  transactionId: Integer [1]
  accountId: Integer [1]
  transactionDate: Date [1]
  type: TransactionType [1]
  itemDescription: String [1]
  amount: Decimal [1]
  status: TransactionStatus [1]
  categoryId: Integer [0..1]
}

class Category <<Entity>> {
  categoryId: Integer [1]
  categoryName: String [1]
}

enum TransactionType {
  Revenue
  Expense
}

enum TransactionStatus {
  Complete
  Pending
  Failed
}

class ExpenseSubCategory <<DTO>> {
  item_description: String [1]
  amount: Number [1]
  date: String [1]
}

class BreakdownResult <<DTO>> {
  category: String [1]
  total: Number [1]
  changePercent: Number [0..1]
  subCategories: ExpenseSubCategory [1..*] {ordered}
}

class ExpenseBreakdownResponse <<DTO>> {
  success: Boolean [1]
  message: String [1]
  data: BreakdownResult [0..*] {ordered}
}

class JwtAuthGuard <<Guard>> {
  validate(token: BearerJWT): AuthenticatedRequest
}

class ExpensesController <<Controller>> {
  getExpensesBreakdown(request: AuthenticatedRequest, month: String): ExpenseBreakdownResponse
}

class ExpensesService <<Service>> {
  getExpensesBreakdown(userId: Integer, month: String): Sequence(BreakdownResult)
}

class ExpensesPage <<UI>> {
  selectedMonth: String [1]
}

class ExpensesBreakdown <<UI>> {
  month: String [1]
  expensesData: BreakdownResult [*]
  fetchExpensesBreakdown(month: String)
}

Account "1" -- "0..*" Transaction
Category "0..1" -- "0..*" Transaction
ExpensesController ..> JwtAuthGuard
ExpensesController ..> ExpensesService
ExpensesController ..> ExpenseBreakdownResponse
ExpensesService ..> Account
ExpensesService ..> Transaction
ExpensesService ..> Category
ExpenseBreakdownResponse --> BreakdownResult
BreakdownResult --> ExpenseSubCategory
ExpensesPage --> ExpensesBreakdown
ExpensesBreakdown ..> ExpenseBreakdownResponse

@enduml

## Row 254

Column A:

Business Rules

Column B:

BR-EXP-CAT-01: Authenticated ownership scope

context ExpensesService::getExpensesBreakdown(userId : Integer, month : String) : Sequence(BreakdownResult)
pre BR_EXP_CAT_01_AuthenticatedIdentity:
  not userId.oclIsUndefined()
post BR_EXP_CAT_01_OwnedTransactionsOnly:
  result->forAll(item |
    item.subCategories->forAll(detail |
      Transaction.allInstances()->exists(t |
        Account.allInstances()->exists(a |
          a.accountId = t.accountId and a.userId = userId
        ) and
        t.itemDescription = detail.item_description and
        t.amount = detail.amount and
        toIsoDate(t.transactionDate) = detail.date
      )
    )
  )

Technical constraints:
- The userId used for the breakdown shall come from the validated JWT.
- Transactions belonging to accounts owned by another user shall not contribute to the breakdown.

BR-EXP-CAT-02: Eligible selected-month expenses

context ExpensesService::getExpensesBreakdown(userId : Integer, month : String) : Sequence(BreakdownResult)
post BR_EXP_CAT_02_EligibleRowsOnly:
  result->forAll(item |
    item.subCategories->forAll(detail |
      Transaction.allInstances()->exists(t |
        Account.allInstances()->exists(a |
          a.accountId = t.accountId and a.userId = userId
        ) and
        t.type = TransactionType::Expense and
        isWithinInclusiveMonth(t.transactionDate, month) and
        t.itemDescription = detail.item_description and
        t.amount = detail.amount and
        toIsoDate(t.transactionDate) = detail.date
      )
    )
  )

Technical constraint:
- Transaction status is not an eligibility predicate; a row is eligible when the ownership, type, and selected-month conditions are satisfied.

BR-EXP-CAT-03: Category classification

context ExpensesService::getExpensesBreakdown(userId : Integer, month : String) : Sequence(BreakdownResult)
post BR_EXP_CAT_03_CategoryDefined:
  result->forAll(item | not item.category.oclIsUndefined())

Technical constraints:
- Eligible transactions shall be grouped by categoryId.
- A null categoryId shall be classified as Uncategorized.
- A non-null categoryId that cannot be resolved to a Category shall be classified as Unknown.
- A resolved categoryId shall use the corresponding Category.categoryName.

BR-EXP-CAT-04: Category totals and detail mapping

context ExpensesService::getExpensesBreakdown(userId : Integer, month : String) : Sequence(BreakdownResult)
post BR_EXP_CAT_04_CategoryTotal:
  result->forAll(item |
    item.total = item.subCategories->collect(detail | detail.amount)->sum()
  )
post BR_EXP_CAT_04_DetailDefined:
  result->forAll(item |
    item.subCategories->forAll(detail |
      not detail.item_description.oclIsUndefined() and
      not detail.amount.oclIsUndefined() and
      not detail.date.oclIsUndefined()
    )
  )

Technical constraint:
- Each detail item shall map Transaction.itemDescription, amount, and transactionDate to item_description, numeric amount, and an ISO YYYY-MM-DD date string.

## Row 255

Column B:

BR-EXP-CAT-05: Previous-month comparison

context ExpensesService::getExpensesBreakdown(userId : Integer, month : String) : Sequence(BreakdownResult)
post BR_EXP_CAT_05_ChangePercent:
  result->forAll(item |
    let previousTotal : Decimal = previousMonthExpenseTotal(userId, month, item.category)
    in
      if previousTotal = 0 then
        if item.total > 0 then item.changePercent = 100
        else item.changePercent.oclIsUndefined()
        endif
      else
        item.changePercent = ((item.total - previousTotal) / previousTotal) * 100
      endif
  )

Technical constraints:
- The comparison period is the immediately preceding calendar month.
- January shall compare with December of the preceding year.
- Previous-month totals shall use the same ownership, Expense eligibility, selected-period, and category-classification rules as the current month.

BR-EXP-CAT-06: Rounding and deterministic ordering

context ExpensesService::getExpensesBreakdown(userId : Integer, month : String) : Sequence(BreakdownResult)
post BR_EXP_CAT_06_RoundedValues:
  result->forAll(item |
    item.total = NumericUtility.round2(item.total) and
    (item.changePercent.oclIsUndefined() or item.changePercent = NumericUtility.round2(item.changePercent))
  )
post BR_EXP_CAT_06_GroupsSortedDescending:
  Sequence{1..result->size()}->forAll(i |
    i < result->size() implies result->at(i).total >= result->at(i + 1).total
  )
post BR_EXP_CAT_06_DetailsSortedAscending:
  result->forAll(item |
    Sequence{1..item.subCategories->size()}->forAll(i |
      i < item.subCategories->size() implies
      item.subCategories->at(i).date <= item.subCategories->at(i + 1).date
    )
  )

BR-EXP-CAT-07: No-data outcome

Technical constraints:
- If the authenticated user owns no accounts, the breakdown has no data for the selected month.
- If no eligible current-month Expense transaction exists, the breakdown has no data for the selected month.
- The backend shall return the API's configured no-data response, and the frontend shall display its no-data state.

## Row 256

Column A:

Related UI

Column B:

ExpensesPage; ExpensesBreakdown; month input; route /expenses

## Row 257

Column A:

Related API IDs

Column B:

API-EXPENSE-BREAKDOWN

## Row 258

Column A:

Notes

Column B:

Experiment isolation:
- BR-EXP-CAT-01 through BR-EXP-CAT-07 are the treatment-sensitive Business Rules for UC-11.
- Description, pre/post-conditions, flows, UML, and non-BR API fields intentionally avoid restating these business semantics.
- Month syntax/format validation is part of the API interface contract, not a treatment-sensitive Business Rule.
- Figma layout/styling requirements are UI evidence and are not part of the core Business Rule effectiveness score.
- Read-only HTTP semantics and the standard success/error response envelope are project-constrained and are not core treatment-sensitive BRs.

## Row 260

Column A:

UC-12 - View Upcoming Bills

## Row 261

Column A:

Use Case ID

Column B:

UC-12

## Row 262

Column A:

Use Case Name

Column B:

View Upcoming Bills

## Row 263

Column A:

Description

Column B:

As an authenticated user, I want to view upcoming bills so that I can review bills that require attention in the near term.

## Row 264

Column A:

Actor(s)

Column B:

Authenticated User

## Row 265

Column A:

Priority

Column B:

Not Specified

## Row 266

Column A:

Trigger

Column B:

The user opens the Bills page.

## Row 267

Column A:

Pre-Condition(s)

Column B:

PRE-1: The user is authenticated.

## Row 268

Column A:

Post-Condition(s)

Column B:

POST-1: After processing, the applicable upcoming-bill information is displayed on /bills.
POST-2: If no applicable bill data is available, the page displays its empty state.
POST-3: The operation does not modify stored bill data.

## Row 269

Column A:

Basic Flow

Column B:

1. The user opens the Bills page.
2. The frontend requests the user's upcoming-bill data.
3. The backend authenticates the request.
4. The backend retrieves and processes the relevant bill data according to the applicable business rules.
5. The backend returns the resulting bill list.
6. The frontend prepares the returned bill data for display.
7. The frontend displays the resulting upcoming-bill view on the Bills page.

## Row 270

Column A:

Alternative Flow

Column B:

AF-1: No applicable upcoming bills
5a. The backend returns an empty bill list.
6a. The frontend does not prepare bill cards.
7a. The frontend displays its no-upcoming-bills state.

AF-2: Retry loading
7b. After a loading error, the user selects the retry action.
2b. The frontend sends the upcoming-bill request again and the flow continues from Step 3.

## Row 271

Column A:

Exception Flow

Column B:

EF-1: Authentication failure
3a. The backend cannot authenticate the request.
3b. The backend returns HTTP 401.
3c. The frontend applies the application's authentication-error handling.

EF-2: Retrieval or processing failure
4a. An unexpected error occurs while retrieving or processing bill data.
4b. The backend returns HTTP 500.
4c. The frontend displays its bill-loading error state.

## Row 272

Column A:

UML Model

Column B:

@startuml

class AuthenticatedRequest <<SecurityContext>> {
  userId: Integer [1]
}

class Bill <<Entity>> {
  billId: Integer [1]
  userId: Integer [1]
  dueDate: Date [1]
  logoUrl: String [0..1]
  itemDescription: String [1]
  lastChargeDate: Date [0..1]
  amount: Decimal [1]
}

class BillDto <<DTO>> {
  billId: Integer [1]
  userId: Integer [1]
  itemDescription: String [1]
  logoUrl: String [0..1]
  dueDate: String [1]
  lastChargeDate: String [0..1]
  amount: Decimal [1]
}

class BillsResponseDto <<DTO>> {
  success: Boolean [1]
  message: String [1]
  data: BillDto [*]
}

class BillController <<Controller>> {
  getBills(request: AuthenticatedRequest): BillsResponseDto
}

class BillService <<Service>> {
  findUpcomingBillsByUserId(userId: Integer): Sequence(BillDto)
}

class BillsPage <<UI>>
class UpcomingBills <<UI>>

BillController ..> AuthenticatedRequest
BillController ..> BillsResponseDto
BillController ..> BillService
BillService ..> Bill
BillService ..> BillDto
BillsResponseDto --> BillDto
BillDto ..> Bill
BillsPage --> UpcomingBills
UpcomingBills ..> BillsResponseDto

@enduml

## Row 273

Column A:

Business Rules

Column B:

BR-BILL-UP-01: Authenticated ownership scope

context BillService::findUpcomingBillsByUserId(userId : Integer) : Sequence(BillDto)

pre BR_BILL_UP_01_AuthenticatedIdentity:
  not userId.oclIsUndefined()

post BR_BILL_UP_01_OwnedBillsOnly:
  result->forAll(dto |
    Bill.allInstances()->exists(bill |
      bill.billId = dto.billId and
      bill.userId = userId
    )
  )

Technical constraints:
- The userId used for bill retrieval shall come from the validated authenticated request context.
- A client-supplied user identifier shall not override the authenticated userId.
- Bills owned by another user shall never contribute to the result.

BR-BILL-UP-02: Near-term eligibility window

context BillService::findUpcomingBillsByUserId(userId : Integer) : Sequence(BillDto)

post BR_BILL_UP_02_WithinWindow:
  result->forAll(dto |
    Bill.allInstances()->exists(bill |
      bill.billId = dto.billId and
      bill.userId = userId and
      bill.dueDate >= currentDateAtMidnight() and
      bill.dueDate <= addDays(currentDateAtMidnight(), 30)
    )
  )

Technical constraints:
- Upcoming eligibility is evaluated against an inclusive 31-day calendar window: today through 30 calendar days after today.
- currentDateAtMidnight() represents the backend system's current calendar date with hour, minute, second, and millisecond set to zero.
- Bills due before today are overdue and shall be excluded.
- Bills due more than 30 calendar days after today shall not appear in the Upcoming Bills result.

BR-BILL-UP-03: Already-charged cycle exclusion

context BillService::findUpcomingBillsByUserId(userId : Integer) : Sequence(BillDto)

post BR_BILL_UP_03_NotAlreadyChargedForDueCycle:
  result->forAll(dto |
    Bill.allInstances()->exists(bill |
      bill.billId = dto.billId and
      (
        bill.lastChargeDate.oclIsUndefined() or
        bill.lastChargeDate < bill.dueDate
      )
    )
  )

Technical constraint:
- A bill whose lastChargeDate is equal to or later than its dueDate is treated as already charged for that due cycle and shall be excluded from the Upcoming Bills result.

## Row 274

Column B:

BR-BILL-UP-04: Deterministic urgency ordering

context BillService::findUpcomingBillsByUserId(userId : Integer) : Sequence(BillDto)

post BR_BILL_UP_04_Ordered:
  result->size() <= 1 or
  Sequence{1..result->size() - 1}->forAll(i |
    let a : BillDto = result->at(i),
        b : BillDto = result->at(i + 1)
    in
      a.dueDate < b.dueDate or
      (
        a.dueDate = b.dueDate and
        (
          a.amount > b.amount or
          (a.amount = b.amount and a.billId < b.billId)
        )
      )
  )

Technical constraints:
- Bills shall be ordered by dueDate ascending.
- Bills sharing the same dueDate shall be ordered by amount descending.
- Bills sharing both dueDate and amount shall be ordered by billId ascending.

BR-BILL-UP-05: Response normalization

context BillService::findUpcomingBillsByUserId(userId : Integer) : Sequence(BillDto)

post BR_BILL_UP_05_NormalizedMapping:
  result->forAll(dto |
    Bill.allInstances()->exists(bill |
      bill.billId = dto.billId and
      dto.userId = bill.userId and
      dto.itemDescription = trim(bill.itemDescription) and
      dto.amount = NumericUtility.round2(bill.amount) and
      dto.dueDate = formatDate(bill.dueDate) and
      (
        bill.lastChargeDate.oclIsUndefined()
        implies dto.lastChargeDate.oclIsUndefined()
      ) and
      (
        not bill.lastChargeDate.oclIsUndefined()
        implies dto.lastChargeDate = formatDate(bill.lastChargeDate)
      ) and
      (
        (bill.logoUrl.oclIsUndefined() or trim(bill.logoUrl).size() = 0)
        implies dto.logoUrl.oclIsUndefined()
      ) and
      (
        (not bill.logoUrl.oclIsUndefined() and trim(bill.logoUrl).size() > 0)
        implies dto.logoUrl = trim(bill.logoUrl)
      )
    )
  )

Technical constraints:
- itemDescription shall be trimmed before it is returned.
- amount shall be rounded to two decimal places.
- dueDate shall be formatted as YYYY-MM-DD.
- lastChargeDate shall be formatted as YYYY-MM-DD when present and returned as null when absent.
- logoUrl shall be trimmed; a missing or blank value shall be returned as null.

BR-BILL-UP-06: Exact coverage, uniqueness, and empty result

context BillService::findUpcomingBillsByUserId(userId : Integer) : Sequence(BillDto)

post BR_BILL_UP_06_UniqueBills:
  result->isUnique(dto | dto.billId)

post BR_BILL_UP_06_AllAndOnlyEligibleBills:
  let eligible : Set(Bill) =
    Bill.allInstances()
      ->select(bill |
        bill.userId = userId and
        bill.dueDate >= currentDateAtMidnight() and
        bill.dueDate <= addDays(currentDateAtMidnight(), 30) and
        (
          bill.lastChargeDate.oclIsUndefined() or
          bill.lastChargeDate < bill.dueDate
        )
      )
      ->asSet()
  in
    result->size() = eligible->size() and
    result->forAll(dto |
      eligible->exists(bill | bill.billId = dto.billId)
    )

Technical constraint:
- If no eligible bill exists after all business rules are applied, the successful result shall contain an empty data array.

## Row 275

Column A:

Related UI

Column B:

BillsPage; UpcomingBills; route /bills

## Row 276

Column A:

Related API IDs

Column B:

API-BILL-LIST

## Row 277

Column A:

Notes

Column B:

Experiment isolation:
- BR-BILL-UP-01 through BR-BILL-UP-06 are the treatment-sensitive Business Rules for UC-12.
- Description, pre/post-conditions, flows, UML, and non-BR API fields intentionally avoid restating the eligibility window, charged-cycle exclusion, tie-break ordering, normalization, and exact-coverage semantics.
- Read-only behavior is redundantly constrained by the GET operation and is not a core treatment-sensitive Business Rule.
- Authentication failure, retrieval failure, and the project-standard response envelope are API/project concerns rather than core Business Rules.
- Figma layout/styling requirements remain UI evidence and are not part of the core Business Rule score.
- "Pay Now" behavior remains outside the scope of UC-12.

## Row 279

Column A:

UC-13 - View Financial Goals

## Row 280

Column A:

Use Case ID

Column B:

UC-13

## Row 281

Column A:

Use Case Name

Column B:

View Financial Goals

## Row 282

Column A:

Description

Column B:

As an authenticated user, I want to view my financial goals and their progress so that I can understand my current goal status.

## Row 283

Column A:

Actor(s)

Column B:

Authenticated User

## Row 284

Column A:

Priority

Column B:

Not Specified

## Row 285

Column A:

Trigger

Column B:

The user opens the Goals page.

## Row 286

Column A:

Pre-Condition(s)

Column B:

PRE-1: The user is authenticated.

## Row 287

Column A:

Post-Condition(s)

Column B:

POST-1: After processing, the applicable financial-goal information and calculated progress are displayed on /goals.
POST-2: If no applicable goal data is available, the page displays its no-goals state.
POST-3: The operation does not modify stored goal, account, category, or transaction data.

## Row 288

Column A:

Basic Flow

Column B:

1. The user opens the Goals page.
2. The frontend requests the user's financial-goal data.
3. The backend authenticates the request.
4. The backend retrieves and processes the relevant goal and financial data according to the applicable business rules.
5. The backend returns the resulting goal data.
6. The frontend prepares the returned data for presentation.
7. The frontend displays the financial-goal view on the Goals page.

## Row 289

Column A:

Alternative Flow

Column B:

AF-1: No applicable goal data
5a. The backend returns goal data with no applicable goal items.
6a. The frontend does not prepare goal cards.
7a. The frontend displays its no-goals state and the available Create Goal action.

AF-2: Partial goal data
5b. The backend returns the applicable subset of goal data.
6b. The frontend prepares only the returned goal sections.
7b. The frontend displays the available goal sections.

## Row 290

Column A:

Exception Flow

Column B:

EF-1: Authentication failure
3a. The backend cannot authenticate the request.
3b. The backend returns HTTP 401.
3c. The frontend applies the application's authentication-error handling.

EF-2: Retrieval or processing failure
4a. An unexpected error occurs while retrieving or processing goal data.
4b. The backend returns HTTP 500.
4c. The frontend displays its retryable goal-loading error state.

## Row 291

Column A:

UML Model

Column B:

@startuml

enum GoalType {
  SAVING
  EXPENSE_LIMIT
}

enum TransactionType {
  REVENUE
  EXPENSE
}

class AuthenticatedRequest <<SecurityContext>> {
  userId: Integer [1]
}

class Goal <<Entity>> {
  goalId: Integer [1]
  userId: Integer [1]
  goalType: GoalType [1]
  categoryId: Integer [0..1]
  startDate: Date [1]
  endDate: Date [1]
  targetAmount: Decimal [1]
}

class Account <<Entity>> {
  accountId: Integer [1]
  userId: Integer [1]
}

class Transaction <<Entity>> {
  transactionId: Integer [1]
  accountId: Integer [1]
  categoryId: Integer [0..1]
  transactionDate: Date [1]
  type: TransactionType [1]
  amount: Decimal [1]
}

class Category <<Entity>> {
  categoryId: Integer [1]
  categoryName: String [1]
}

class SavingGoalDto <<DTO>> {
  goalId: Integer [1]
  goalType: GoalType [1]
  targetAmount: Decimal [1]
  targetAchieved: Decimal [1]
  startDate: String [1]
  endDate: String [1]
}

class ExpenseGoalDto <<DTO>> {
  goalId: Integer [1]
  category: String [1]
  targetAmount: Decimal [1]
  currentExpense: Decimal [1]
}

class GoalDataDto <<DTO>> {
  savingGoal: SavingGoalDto [0..1]
  expenseGoals: ExpenseGoalDto [*] {ordered}
}

class GoalListResponseDto <<DTO>> {
  success: Boolean [1]
  message: String [1]
  data: GoalDataDto [1]
}

class GoalController <<Controller>> {
  getGoals(request: AuthenticatedRequest): GoalListResponseDto
}

class GoalService <<Service>> {
  getGoals(userId: Integer): GoalListResponseDto
}

class GoalsPage <<UI>>

GoalController ..> AuthenticatedRequest
GoalController ..> GoalService
GoalController ..> GoalListResponseDto
GoalService ..> Goal
GoalService ..> Account
GoalService ..> Transaction
GoalService ..> Category
GoalListResponseDto --> GoalDataDto
GoalDataDto --> SavingGoalDto
GoalDataDto --> ExpenseGoalDto
SavingGoalDto ..> Goal
ExpenseGoalDto ..> Goal
Transaction --> Account
Goal --> Category : category [0..1]
Transaction --> Category : category [0..1]
GoalsPage ..> GoalListResponseDto

@enduml

## Row 292

Column A:

Business Rules

Column B:

BR-GOAL-VIEW-01: Authenticated ownership scope

context GoalService::getGoals(userId : Integer) : GoalListResponseDto

pre BR_GOAL_VIEW_01_AuthenticatedIdentity:
  not userId.oclIsUndefined()

post BR_GOAL_VIEW_01_OwnedGoalsOnly:
  result.success implies
    (
      result.data.savingGoal.oclIsUndefined() or
      Goal.allInstances()->exists(g |
        g.goalId = result.data.savingGoal.goalId and
        g.userId = userId
      )
    ) and
    result.data.expenseGoals->forAll(dto |
      Goal.allInstances()->exists(g |
        g.goalId = dto.goalId and
        g.userId = userId
      )
    )

Technical constraints:
- The userId used by GoalService shall come from the validated authenticated request context.
- A client-supplied user identifier shall not override the authenticated userId.
- Goals, accounts, and transactions owned by another user shall not contribute to any returned goal or calculated progress value.

BR-GOAL-VIEW-02: Deterministic saving-goal selection

context GoalService::getGoals(userId : Integer) : GoalListResponseDto

post BR_GOAL_VIEW_02_SavingSelection:
  let candidates : Set(Goal) =
    Goal.allInstances()
      ->select(g |
        g.userId = userId and
        g.goalType = GoalType::SAVING and
        g.startDate <= g.endDate and
        g.startDate <= currentMonthEnd() and
        g.endDate >= currentMonthStart()
      )
      ->asSet()
  in
    if candidates->isEmpty() then
      result.data.savingGoal.oclIsUndefined()
    else
      let latestStart : Date = candidates->collect(g | g.startDate)->max() in
      let latestStartCandidates : Set(Goal) = candidates->select(g | g.startDate = latestStart)->asSet() in
      let selectedId : Integer = latestStartCandidates->collect(g | g.goalId)->max() in
        not result.data.savingGoal.oclIsUndefined() and
        result.data.savingGoal.goalId = selectedId
    endif

Technical constraints:
- A Saving goal is eligible only when its persisted date range is valid and overlaps the current calendar month.
- If multiple eligible Saving goals exist, select the one with the latest startDate; if multiple candidates share that startDate, select the one with the highest goalId.
- For the OCL in UC-13, currentMonthStart() and currentMonthEnd() denote the first and last instants of the backend server's current calendar month.

BR-GOAL-VIEW-03: Expense-limit goal eligibility and exact coverage

context GoalService::getGoals(userId : Integer) : GoalListResponseDto

post BR_GOAL_VIEW_03_AllAndOnlyEligibleExpenseGoals:
  let eligible : Set(Goal) =
    Goal.allInstances()
      ->select(g |
        g.userId = userId and
        g.goalType = GoalType::EXPENSE_LIMIT and
        g.startDate <= g.endDate and
        g.startDate <= currentMonthEnd() and
        g.endDate >= currentMonthStart()
      )
      ->asSet()
  in
    result.data.expenseGoals->size() = eligible->size() and
    result.data.expenseGoals->isUnique(dto | dto.goalId) and
    result.data.expenseGoals->forAll(dto |
      eligible->exists(g | g.goalId = dto.goalId)
    )

Technical constraints:
- Expired, not-yet-active, invalid-range, or other-user Expense_Limit goals shall not be returned.
- Every eligible Expense_Limit goal shall appear exactly once.

## Row 293

Column B:

BR-GOAL-VIEW-04: Saving progress uses the goal/month overlap interval

context GoalService::getGoals(userId : Integer) : GoalListResponseDto

post BR_GOAL_VIEW_04_SavingTargetAchieved:
  not result.data.savingGoal.oclIsUndefined()
  implies
    let goal : Goal = Goal.allInstances()->any(g | g.goalId = result.data.savingGoal.goalId) in
    let periodStart : Date = if goal.startDate > currentMonthStart() then goal.startDate else currentMonthStart() endif in
    let periodEnd : Date = if goal.endDate < currentMonthEnd() then goal.endDate else currentMonthEnd() endif in
    let ownedAccountIds : Set(Integer) =
      Account.allInstances()
        ->select(a | a.userId = userId)
        ->collect(a | a.accountId)
        ->asSet()
    in
    let periodTransactions : Set(Transaction) =
      Transaction.allInstances()
        ->select(t |
          ownedAccountIds->includes(t.accountId) and
          t.transactionDate >= periodStart and
          t.transactionDate <= periodEnd
        )
        ->asSet()
    in
    let revenue : Decimal =
      periodTransactions
        ->select(t | t.type = TransactionType::REVENUE)
        ->collect(t | t.amount)
        ->sum()
    in
    let expense : Decimal =
      periodTransactions
        ->select(t | t.type = TransactionType::EXPENSE)
        ->collect(t | t.amount)
        ->sum()
    in
      result.data.savingGoal.targetAchieved = revenue - expense

Technical constraints:
- Saving progress is calculated only for the intersection between the selected Saving goal's date interval and the current calendar month.
- Transactions outside that intersection shall not contribute even if they are in the same calendar month.
- If no owned account or no matching transaction exists, the corresponding sum is treated as 0.
- Negative targetAchieved values are allowed and shall not be clamped to zero.

BR-GOAL-VIEW-05: Expense-limit progress uses category and goal/month overlap

context GoalService::getGoals(userId : Integer) : GoalListResponseDto

post BR_GOAL_VIEW_05_CurrentExpense:
  result.data.expenseGoals->forAll(dto |
    let goal : Goal = Goal.allInstances()->any(g | g.goalId = dto.goalId) in
    let periodStart : Date = if goal.startDate > currentMonthStart() then goal.startDate else currentMonthStart() endif in
    let periodEnd : Date = if goal.endDate < currentMonthEnd() then goal.endDate else currentMonthEnd() endif in
    let ownedAccountIds : Set(Integer) =
      Account.allInstances()
        ->select(a | a.userId = userId)
        ->collect(a | a.accountId)
        ->asSet()
    in
    let expectedExpense : Decimal =
      Transaction.allInstances()
        ->select(t |
          ownedAccountIds->includes(t.accountId) and
          t.type = TransactionType::EXPENSE and
          t.categoryId = goal.categoryId and
          t.transactionDate >= periodStart and
          t.transactionDate <= periodEnd
        )
        ->collect(t | t.amount)
        ->sum()
    in
      dto.currentExpense = expectedExpense
  )

Technical constraints:
- Revenue transactions never contribute to currentExpense.
- Expense progress is calculated only for the intersection between each Expense_Limit goal's date interval and the current calendar month.
- Only transactions whose categoryId equals the goal's categoryId contribute.
- If no owned account or no matching transaction exists, currentExpense is 0.

## Row 294

Column B:

BR-GOAL-VIEW-06: Category resolution and numeric normalization

context GoalService::getGoals(userId : Integer) : GoalListResponseDto

post BR_GOAL_VIEW_06_CategoryAndAmounts:
  result.data.expenseGoals->forAll(dto |
    let goal : Goal = Goal.allInstances()->any(g | g.goalId = dto.goalId) in
      dto.targetAmount = NumericUtility.round2(goal.targetAmount) and
      dto.currentExpense = NumericUtility.round2(dto.currentExpense) and
      (
        (goal.categoryId.oclIsUndefined() and dto.category = 'Uncategorized') or
        (not goal.categoryId.oclIsUndefined() and
          Category.allInstances()->exists(c |
            c.categoryId = goal.categoryId and
            StringNormalizer.trim(c.categoryName).size() > 0 and
            dto.category = StringNormalizer.trim(c.categoryName)
          )) or
        (not goal.categoryId.oclIsUndefined() and
          not Category.allInstances()->exists(c |
            c.categoryId = goal.categoryId and
            StringNormalizer.trim(c.categoryName).size() > 0
          ) and
          dto.category = 'Unknown')
      )
  )

Technical constraints:
- A null categoryId is represented as Uncategorized.
- A non-null categoryId with no resolvable non-blank category name is represented as Unknown.
- A resolved category name is trimmed before being returned.
- Saving and expense monetary values returned by this use case shall be rounded to two decimal places.

BR-GOAL-VIEW-07: Deterministic expense-goal priority ordering

context GoalService::getGoals(userId : Integer) : GoalListResponseDto

post BR_GOAL_VIEW_07_ExpenseGoalOrder:
  result.data.expenseGoals->size() <= 1 or
  Sequence{1..result.data.expenseGoals->size() - 1}->forAll(i |
    let a : ExpenseGoalDto = result.data.expenseGoals->at(i),
        b : ExpenseGoalDto = result.data.expenseGoals->at(i + 1),
        ga : Goal = Goal.allInstances()->any(g | g.goalId = a.goalId),
        gb : Goal = Goal.allInstances()->any(g | g.goalId = b.goalId),
        aExceeded : Boolean = a.currentExpense >= a.targetAmount,
        bExceeded : Boolean = b.currentExpense >= b.targetAmount
    in
      (aExceeded and not bExceeded) or
      (aExceeded = bExceeded and ga.endDate < gb.endDate) or
      (aExceeded = bExceeded and ga.endDate = gb.endDate and a.targetAmount < b.targetAmount) or
      (aExceeded = bExceeded and ga.endDate = gb.endDate and a.targetAmount = b.targetAmount and a.goalId < b.goalId)
  )

Technical constraints:
- Goals that have reached or exceeded their target amount shall be listed before goals still below their limit.
- Within the same exceeded/not-exceeded group, order by endDate ascending, then targetAmount ascending, then goalId ascending.
- The ordering shall be deterministic for the same persisted data and calculation date.

## Row 295

Column A:

Related UI

Column B:

GoalsPage; saving and expense goal cards; route /goals

## Row 296

Column A:

Related API IDs

Column B:

API-GOAL-LIST

## Row 297

Column A:

Notes

Column B:

Experiment isolation:
- BR-GOAL-VIEW-01 through BR-GOAL-VIEW-07 are the treatment-sensitive Business Rules for UC-13.
- Description, pre/post-conditions, flows, UML, and the non-BR API contract intentionally avoid restating saving-goal selection, date-overlap calculation, category fallback, exact-coverage, and priority-ordering semantics.
- The API contract defines only interface structure, authentication requirements, response fields, and error contracts.
- Read-only behavior is redundantly constrained by the GET operation and is not a core treatment-sensitive Business Rule.
- Authentication failure, retrieval failure, and the project-standard response envelope are project/API concerns rather than core Business Rules.
- Figma layout/styling requirements are UI evidence and are not part of the core Business Rule score.

## Row 299

Column A:

UC-14 - Create a Financial Goal

## Row 300

Column A:

Use Case ID

Column B:

UC-14

## Row 301

Column A:

Use Case Name

Column B:

Create a Financial Goal

## Row 302

Column A:

Description

Column B:

As an authenticated user, I want to create a financial goal so that I can track a desired financial outcome.

## Row 303

Column A:

Actor(s)

Column B:

Authenticated User

## Row 304

Column A:

Priority

Column B:

Not Specified

## Row 305

Column A:

Trigger

Column B:

The user selects Create Goal on the Goals page.

## Row 306

Column A:

Pre-Condition(s)

Column B:

PRE-1: The user is authenticated.

## Row 307

Column A:

Post-Condition(s)

Column B:

POST-1: After successful processing, the new financial goal is persisted in the database.
POST-2: After the goal is created successfully, the Create Goal modal closes and the user remains on /goals with the goal list refreshed.
POST-3: The page displays the successful creation feedback.

## Row 308

Column A:

Basic Flow

Column B:

1. The user opens the Create Goal modal.
2. The frontend prepares the information required by the goal-creation form.
3. The user enters the financial-goal information.
4. The user submits the form.
5. The frontend sends a goal-creation request.
6. The backend authenticates the request and validates the submitted data according to the applicable business rules.
7. The backend creates and persists the new goal.
8. The backend returns the creation result.
9. The frontend closes the modal, refreshes the goal list, and displays the updated Goals page.

## Row 309

Column A:

Alternative Flow

Column B:

AF-1: Select a different goal type
3a. The user selects another supported goal type.
3b. The frontend updates the form fields applicable to the selected type.
3c. The flow continues from Step 3.

AF-2: Cancel creation
4a. The user closes or cancels the modal.
4b. No goal-creation request is sent and the use case ends.

## Row 310

Column A:

Exception Flow

Column B:

EF-1: Submitted data is rejected
6a. The submitted goal data does not satisfy the applicable validation or business rules.
6b. The backend returns HTTP 400.
6c. The modal displays the returned validation message and remains open.

EF-2: Authentication failure
6a. The backend cannot authenticate the request.
6b. The backend returns HTTP 401.
6c. The frontend applies the application's authentication-error handling.

EF-3: Persistence or processing failure
7a. An unexpected error occurs while creating the goal.
7b. The backend returns HTTP 500.
7c. The modal displays its create-goal failure state.

## Row 311

Column A:

UML Model

Column B:

@startuml

enum GoalType {
  SAVING
  EXPENSE_LIMIT
}

class AuthenticatedRequest <<SecurityContext>> {
  userId: Integer [1]
}

class User <<Entity>> {
  userId: Integer [1]
}

class Category <<Entity>> {
  categoryId: Integer [1]
  categoryName: String [1]
}

class Goal <<Entity>> {
  goalId: Integer [1]
  userId: Integer [1]
  goalType: GoalType [1]
  categoryId: Integer [0..1]
  startDate: Date [1]
  endDate: Date [1]
  targetAmount: Decimal [1]
}

class CreateGoalDto <<DTO>> {
  goal_type: GoalType [1]
  category_id: Integer [0..1]
  start_date: String [1]
  end_date: String [1]
  target_amount: Decimal [1]
}

class CreateGoalResponseDto <<DTO>> {
  message: String [1]
  goal_id: Integer [1]
}

class GoalController <<Controller>> {
  createGoal(request: AuthenticatedRequest, dto: CreateGoalDto): CreateGoalResponseDto
}

class GoalService <<Service>> {
  createGoal(userId: Integer, dto: CreateGoalDto): Goal
}

class GoalsPage <<UI>>
class CreateGoalModal <<UI>>

User "1" -- "0..*" Goal : owns
Category "0..1" -- "0..*" Goal : categorizes
GoalController ..> AuthenticatedRequest
GoalController ..> CreateGoalDto
GoalController ..> CreateGoalResponseDto
GoalController ..> GoalService
GoalService ..> Goal
GoalService ..> Category
GoalsPage --> CreateGoalModal
CreateGoalModal ..> CreateGoalResponseDto

@enduml

## Row 312

Column A:

Business Rules

Column B:

Specification helper semantics used only by the UC-14 Business Rules:
- parseIsoDate(s): parses s only when s is a valid calendar date written exactly as YYYY-MM-DD.
- todayAtMidnight(): returns the backend server's current calendar date with the time component normalized to 00:00:00.000.
- calendarDaysBetween(a, b): returns the number of calendar-day boundaries from a to b.
- decimalScale(x): returns the number of fractional decimal digits in x after removing insignificant trailing zeros.

BR-GOAL-CREATE-01: Authenticated ownership is authoritative

context GoalService::createGoal(userId : Integer, dto : CreateGoalDto) : Goal

pre BR_GOAL_CREATE_01_AuthenticatedIdentity:
  not userId.oclIsUndefined()

post BR_GOAL_CREATE_01_Ownership:
  result.userId = userId

Technical constraints:
- userId shall come from the validated authentication context.
- The client shall not provide, select, or override the owner of the created goal.
- No goal belonging to another user may be modified as part of this operation.

BR-GOAL-CREATE-02: Goal type determines category semantics

context GoalService::createGoal(userId : Integer, dto : CreateGoalDto) : Goal

pre BR_GOAL_CREATE_02_AllowedType:
  Set{GoalType::SAVING, GoalType::EXPENSE_LIMIT}->includes(dto.goal_type)

pre BR_GOAL_CREATE_02_CategorySemantics:
  (dto.goal_type = GoalType::SAVING implies dto.category_id.oclIsUndefined()) and
  (dto.goal_type = GoalType::EXPENSE_LIMIT implies
    not dto.category_id.oclIsUndefined() and
    Category.allInstances()->exists(c | c.categoryId = dto.category_id))

post BR_GOAL_CREATE_02_CategoryPersisted:
  (dto.goal_type = GoalType::SAVING implies result.categoryId.oclIsUndefined()) and
  (dto.goal_type = GoalType::EXPENSE_LIMIT implies result.categoryId = dto.category_id)

Technical constraints:
- A Saving goal request containing a non-null category_id is invalid; the category value shall not be silently discarded.
- An Expense_Limit goal requires a category_id that resolves to an existing Category.

BR-GOAL-CREATE-03: Target amount precision and positivity

context GoalService::createGoal(userId : Integer, dto : CreateGoalDto) : Goal

pre BR_GOAL_CREATE_03_TargetDefined:
  not dto.target_amount.oclIsUndefined()

pre BR_GOAL_CREATE_03_TargetPositive:
  dto.target_amount > 0

pre BR_GOAL_CREATE_03_TargetScale:
  decimalScale(dto.target_amount) <= 2

post BR_GOAL_CREATE_03_TargetPreserved:
  result.targetAmount = dto.target_amount

Technical constraints:
- target_amount shall be a finite decimal value greater than zero.
- More than two significant fractional decimal digits shall be rejected rather than silently rounded.

## Row 313

Column B:

BR-GOAL-CREATE-04: Prospective bounded date interval

context GoalService::createGoal(userId : Integer, dto : CreateGoalDto) : Goal

pre BR_GOAL_CREATE_04_StrictDates:
  parseIsoDate(dto.start_date) is defined and
  parseIsoDate(dto.end_date) is defined

pre BR_GOAL_CREATE_04_ProspectiveInterval:
  parseIsoDate(dto.start_date) >= todayAtMidnight() and
  parseIsoDate(dto.end_date) > parseIsoDate(dto.start_date)

pre BR_GOAL_CREATE_04_MaxDuration:
  calendarDaysBetween(parseIsoDate(dto.start_date), parseIsoDate(dto.end_date)) <= 366

Technical constraints:
- start_date and end_date shall be valid calendar dates written exactly as YYYY-MM-DD.
- A goal may start today or in the future, but shall not start before the backend server's current calendar date.
- end_date shall be strictly later than start_date.
- A single goal interval shall not exceed 366 calendar days.

BR-GOAL-CREATE-05: Conflicting goal intervals are prohibited

context GoalService::createGoal(userId : Integer, dto : CreateGoalDto) : Goal

pre BR_GOAL_CREATE_05_NoConflictingOverlap:
  let newStart : Date = parseIsoDate(dto.start_date),
      newEnd : Date = parseIsoDate(dto.end_date)
  in
    if dto.goal_type = GoalType::SAVING then
      Goal.allInstances()
        ->select(g | g.userId = userId and g.goalType = GoalType::SAVING)
        ->forAll(g | not (g.startDate <= newEnd and g.endDate >= newStart))
    else
      Goal.allInstances()
        ->select(g |
          g.userId = userId and
          g.goalType = GoalType::EXPENSE_LIMIT and
          g.categoryId = dto.category_id
        )
        ->forAll(g | not (g.startDate <= newEnd and g.endDate >= newStart))
    endif

Technical constraints:
- Date intervals are inclusive for conflict detection.
- Two Saving goals owned by the same user shall not have overlapping intervals.
- Two Expense_Limit goals owned by the same user for the same category shall not have overlapping intervals.
- Expense_Limit goals for different categories may overlap.
- Because interval boundaries are inclusive, an existing goal ending on the requested start_date is considered conflicting.

BR-GOAL-CREATE-06: Exact persistence with existing-goal preservation

context GoalService::createGoal(userId : Integer, dto : CreateGoalDto) : Goal

post BR_GOAL_CREATE_06_ExactlyOneCreated:
  Goal.allInstances()->size() = Goal.allInstances()@pre->size() + 1

post BR_GOAL_CREATE_06_PersistedValues:
  Goal.allInstances()->one(g |
    g.goalId = result.goalId and
    g.userId = userId and
    g.goalType = dto.goal_type and
    g.startDate = parseIsoDate(dto.start_date) and
    g.endDate = parseIsoDate(dto.end_date) and
    g.targetAmount = dto.target_amount and
    ((dto.goal_type = GoalType::SAVING and g.categoryId.oclIsUndefined()) or
     (dto.goal_type = GoalType::EXPENSE_LIMIT and g.categoryId = dto.category_id))
  )

Technical constraints:
- A successful operation shall insert exactly one new Goal record.
- Existing Goal records shall not be updated or deleted by creation.
- The returned goal_id shall identify the newly persisted Goal record.

BR-GOAL-CREATE-07: Validation, conflict, and persistence failures are atomic

Technical constraints:
- Any violation of BR-GOAL-CREATE-01 through BR-GOAL-CREATE-05 shall reject the request with HTTP 400 and shall not persist a Goal record.
- An unexpected repository or database failure shall return HTTP 500 and shall not leave a partially persisted Goal record.
- The conflict check in BR-GOAL-CREATE-05 and insertion of the new Goal shall be executed atomically, transactionally, or with an equivalent concurrency-safe mechanism so that two concurrent conflicting requests cannot both succeed.
- Success shall be reported only after persistence has completed.

## Row 314

Column A:

Related UI

Column B:

GoalsPage; CreateGoalModal

## Row 315

Column A:

Related API IDs

Column B:

API-GOAL-CREATE; API-CATEGORY-LIST

## Row 316

Column A:

Notes

Column B:

Experiment isolation:
- BR-GOAL-CREATE-01 through BR-GOAL-CREATE-07 are the treatment-sensitive Business Rules for UC-14.
- Description, pre/post-conditions, flows, UML, and the non-BR API contract intentionally avoid restating ownership authority, category semantics, target precision, prospective date limits, overlap conflicts, exact persistence, and atomicity semantics.
- The API contract defines only endpoint structure, authentication, request/response field shapes, and generic error contracts.
- The standard response envelope and HTTP transport behavior are project/API concerns and are not part of the core Business Rule effectiveness score.
- Figma layout/styling requirements are UI evidence and are not part of the core Business Rule score.

## Row 318

Column A:

UC-15 - Adjust a Financial Goal

## Row 319

Column A:

Use Case ID

Column B:

UC-15

## Row 320

Column A:

Use Case Name

Column B:

Adjust a Financial Goal

## Row 321

Column A:

Description

Column B:

As an authenticated goal owner, I want to change an existing goal's target amount.

## Row 322

Column A:

Actor(s)

Column B:

Authenticated User

## Row 323

Column A:

Priority

Column B:

Not Specified

## Row 324

Column A:

Trigger

Column B:

The user selects Edit on a displayed Saving or Expense_Limit goal.

## Row 325

Column A:

Pre-Condition(s)

Column B:

PRE-1: The user is authenticated.
PRE-2: The selected goal exists and belongs to the authenticated user.

## Row 326

Column A:

Post-Condition(s)

Column B:

POST-1: On success, only targetAmount is changed.
POST-2: The modal closes, a success toast appears, and GoalsPage refreshes.
POST-3: On failure, the previous target amount remains stored.

## Row 327

Column A:

Basic Flow

Column B:

1. The user selects Edit for a displayed goal.
2. AdjustGoalModal opens with the current target amount.
3. The user enters a new target amount and selects Save.
4. The frontend requires a numeric amount greater than zero.
5. The frontend sends PUT /api/v1/goals/:goalId with target_amount.
6. ValidationPipe validates UpdateGoalDto.
7. GoalService finds the goal, verifies that goal.userId equals the authenticated userId, and overwrites only targetAmount.
8. The backend returns the goal ID and updated target amount.
9. The frontend displays a success toast, closes the modal, and refreshes goals.

## Row 328

Column A:

Alternative Flow

Column B:

AF-1: Cancel
3a. The user closes or cancels the modal and no update request is sent.

## Row 329

Column A:

Exception Flow

Column B:

EF-1: Invalid target amount
4a. The frontend displays an input error, or the backend returns HTTP 400.

EF-2: Goal not found
7a. The backend returns HTTP 404.

EF-3: Goal belongs to another user
7a. The backend returns HTTP 403.

EF-4: Storage failure
7a. The backend returns HTTP 500 and the modal displays its save failure message.

## Row 330

Column A:

UML Model

Column B:

@startuml

enum GoalType {
  SAVING
  EXPENSE_LIMIT
}

note right of GoalType
  SAVING maps to "Saving".
  EXPENSE_LIMIT maps to "Expense_Limit".
end note

class AuthenticatedRequest <<SecurityContext>> {
  userId: Integer [1]
}

class User <<Entity>> {
  userId: Integer [1]
}

class Goal <<Entity>> {
  goalId: Integer [1]
  userId: Integer [1]
  goalType: GoalType [1]
  categoryId: Integer [0..1]
  startDate: Date [1]
  endDate: Date [1]
  targetAmount: Decimal [1]
}

class UpdateGoalDto <<DTO>> {
  target_amount: Decimal [1]
}

class UpdatedGoalDto <<DTO>> {
  goal_id: Integer [1]
  target_amount: Decimal [1]
}

class UpdateGoalResponseDto <<DTO>> {
  message: String [1]
  updated_goal: UpdatedGoalDto [1]
}

class GoalController <<Controller>> {
  updateGoal(
    request: AuthenticatedRequest,
    goalId: Integer,
    dto: UpdateGoalDto
  ): UpdateGoalResponseDto
}

class GoalService <<Service>> {
  updateGoal(
    userId: Integer,
    goalId: Integer,
    dto: UpdateGoalDto
  ): Goal
}

User "1" -- "0..*" Goal : owns

GoalController ..> AuthenticatedRequest
GoalController ..> UpdateGoalDto
GoalController ..> UpdateGoalResponseDto
GoalController ..> GoalService

GoalService ..> Goal
GoalService ..> UpdateGoalDto

UpdateGoalResponseDto --> UpdatedGoalDto
UpdatedGoalDto ..> Goal : maps from

@enduml

## Row 331

Column A:

Business Rules

Column B:

BR-GOAL-12: Positive updated target amount

context GoalService::updateGoal(
  userId : Integer,
  goalId : Integer,
  dto : UpdateGoalDto
) : Goal

pre BR_GOAL_12_TargetDefined:
  not dto.target_amount.oclIsUndefined()

pre BR_GOAL_12_TargetPositive:
  dto.target_amount > 0


BR-GOAL-13: Existing goal required

context GoalService::updateGoal(
  userId : Integer,
  goalId : Integer,
  dto : UpdateGoalDto
) : Goal

pre BR_GOAL_13_GoalExists:
  Goal.allInstances()->exists(g |
    g.goalId = goalId
  )

Technical constraint:
- If no Goal exists with goalId, the backend shall return HTTP 404 Not Found with message "Goal does not exist."


BR-GOAL-14: Authenticated goal ownership

context GoalService::updateGoal(
  userId : Integer,
  goalId : Integer,
  dto : UpdateGoalDto
) : Goal

pre BR_GOAL_14_OwnedByAuthenticatedUser:
  Goal.allInstances()->exists(g |
    g.goalId = goalId and
    g.userId = userId
  )

Technical constraints:
- userId shall be obtained from the validated JWT.
- If the goal belongs to another user, the backend shall return HTTP 403 Forbidden with message "You do not have permission to edit this goal."


BR-GOAL-15: Target-only goal update

context GoalService::updateGoal(
  userId : Integer,
  goalId : Integer,
  dto : UpdateGoalDto
) : Goal

post BR_GOAL_15_NoGoalCreatedOrDeleted:
  Goal.allInstances()->size() =
    Goal.allInstances()@pre->size()

post BR_GOAL_15_OnlyTargetAmountChanged:
  let original : Goal =
    Goal.allInstances()@pre->any(g |
      g.goalId = goalId
    )
  in
  let updated : Goal =
    Goal.allInstances()->any(g |
      g.goalId = goalId
    )
  in
    updated.targetAmount = dto.target_amount and
    updated.userId = original.userId and
    updated.goalType = original.goalType and
    updated.startDate = original.startDate and
    updated.endDate = original.endDate and
    updated.categoryId.oclIsUndefined() =
      original.categoryId.oclIsUndefined() and
    (
      not original.categoryId.oclIsUndefined()
      implies updated.categoryId = original.categoryId
    )


BR-GOAL-16: Successful update response

context GoalController::updateGoal(
  request : AuthenticatedRequest,
  goalId : Integer,
  dto : UpdateGoalDto
) : UpdateGoalResponseDto

post BR_GOAL_16_Response:
  result.message = 'Goal updated successfully' and
  result.updated_goal.goal_id = goalId and
  result.updated_goal.target_amount = dto.target_amount and
  Goal.allInstances()->exists(g |
    g.goalId = goalId and
    g.userId = request.userId and
    g.targetAmount = dto.target_amount
  )


BR-GOAL-17: Update failure handling

Technical constraints:
- An invalid or non-positive target_amount shall result in HTTP 400 Bad Request.
- A failed or rejected update shall not persist a changed targetAmount.
- If the goal does not exist, the backend shall return HTTP 404 Not Found.
- If the goal belongs to another user, the backend shall return HTTP 403 Forbidden.
- An unexpected repository/database failure while saving shall result in HTTP 500 Internal Server Error with message "Unable to save changes at this time. Please try again later."
- The controller parses goalId with parseInt(goalId, 10) and does not explicitly reject NaN before calling the service.

## Row 332

Column A:

Related UI

Column B:

GoalsPage; AdjustGoalModal

## Row 333

Column A:

Related API IDs

Column B:

API-GOAL-UPDATE

## Row 334

Column A:

Notes

## Row 336

Column A:

UC-16 - View Savings Summary

## Row 337

Column A:

Use Case ID

Column B:

UC-16

## Row 338

Column A:

Use Case Name

Column B:

View Savings Summary

## Row 339

Column A:

Description

Column B:

As an authenticated user, I want to compare monthly net savings for a selected year with the previous year.

## Row 340

Column A:

Actor(s)

Column B:

Authenticated User

## Row 341

Column A:

Priority

Column B:

Not Specified

## Row 342

Column A:

Trigger

Column B:

The user opens the Goals page or changes the year selector in Saving Summary.

## Row 343

Column A:

Pre-Condition(s)

Column B:

PRE-1: The user is authenticated.
PRE-2: The frontend initializes selectedYear to the current year.

## Row 344

Column A:

Post-Condition(s)

Column B:

POST-1: The API returns exactly 12 monthly rows for the selected year and 12 for the preceding year.
POST-2: Each amount equals monthly Revenue minus monthly Expense across the user's accounts.
POST-3: The frontend displays a two-line chart when either yearly series contains a non-zero value.

## Row 345

Column A:

Basic Flow

Column B:

1. GoalsPage renders SavingsSummaryChart.
2. The component initializes selectedYear to the current year and sends GET /api/v1/savings/summary?year=selectedYear.
3. The controller parses year with parseInt; missing, NaN, less than 1900, or greater than 2100 resolves to the current year.
4. SavingsService loads account IDs owned by userId.
5. For each month 01-12 in the selected year, the service sums Revenue, sums Expense, and calculates amount = Revenue - Expense.
6. The service repeats the calculation for selectedYear - 1.
7. Monthly amounts are rounded to two decimals and returned in ordered 12-row arrays.
8. The frontend maps month numbers to Jan-Dec and displays this year and last year as two lines.

## Row 346

Column A:

Alternative Flow

Column B:

AF-1: Select another year
2a. The user selects one of the current year and previous ten years.
2b. The component requests the selected year again.

AF-2: No owned accounts
4a. The service returns zero-valued 12-month arrays for both years.

AF-3: Both returned series contain only zero
8a. The frontend displays its no-transaction-data message instead of the chart.

## Row 347

Column A:

Exception Flow

Column B:

EF-1: Unauthorized request
2a. HTTP 401 is handled by the Axios interceptor.

EF-2: Calculation failure
5a. The backend returns HTTP 500 and the chart displays its general load error.

## Row 348

Column A:

UML Model

Column B:

@startuml

enum TransactionType {
  REVENUE
  EXPENSE
}

enum SavingsSeries {
  THIS_YEAR
  LAST_YEAR
}

class AuthenticatedRequest <<SecurityContext>> {
  userId: Integer [1]
}

class User <<Entity>> {
  userId: Integer [1]
}

class Account <<Entity>> {
  accountId: Integer [1]
  userId: Integer [1]
}

class Transaction <<Entity>> {
  transactionId: Integer [1]
  accountId: Integer [1]
  transactionDate: Date [1]
  type: TransactionType [1]
  amount: Decimal [1]
}

class SavingsSummaryQueryDto <<DTO>> {
  year: String [0..1]
}

class MonthlySavingsDto <<DTO>> {
  month: String [1]
  amount: Decimal [1]
}

class SavingsSummaryDataDto <<DTO>> {
  this_year: MonthlySavingsDto [12]
  last_year: MonthlySavingsDto [12]
}

class SavingsSummaryResponseDto <<DTO>> {
  user_id: Integer [1]
  year: Integer [1]
  summary: SavingsSummaryDataDto [1]
}

class SavingsController <<Controller>> {
  getSavingsSummary(
    request: AuthenticatedRequest,
    year: String
  ): SavingsSummaryResponseDto

  resolveYear(year: String): Integer
}

class SavingsService <<Service>> {
  getSavingsSummary(
    userId: Integer,
    year: Integer
  ): SavingsSummaryResponseDto

  calculateMonthlySavings(
    userId: Integer,
    year: Integer
  ): MonthlySavingsDto [12]
}

class SavingsTooltip <<UIModel>> {
  visible: Boolean [1]
  month: String [0..1]
  amount: Decimal [0..1]
}

class SavingsSummaryChart <<UIComponent>> {
  isChartVisible: Boolean [1]
  hoverPoint(
    series: SavingsSeries,
    month: String
  ): SavingsTooltip
  leavePoint(): void
}

User "1" -- "0..*" Account : owns
Account "1" -- "0..*" Transaction : contains

SavingsSummaryChart ..> SavingsSummaryResponseDto
SavingsSummaryChart ..> SavingsTooltip
SavingsSummaryChart ..> SavingsSeries

SavingsController ..> AuthenticatedRequest
SavingsController ..> SavingsSummaryQueryDto
SavingsController ..> SavingsService
SavingsController ..> SavingsSummaryResponseDto

SavingsService ..> Account
SavingsService ..> Transaction
SavingsService ..> SavingsSummaryResponseDto

SavingsSummaryResponseDto --> SavingsSummaryDataDto
SavingsSummaryDataDto --> MonthlySavingsDto

@enduml

## Row 349

Column A:

Business Rules

Column B:

BR-SAV-01: Authenticated user data scope

context SavingsService::getSavingsSummary(
  userId : Integer,
  year : Integer
) : SavingsSummaryResponseDto

post BR_SAV_01_UserIdentity:
  result.user_id = userId

post BR_SAV_01_OwnedAccountsOnly:
  Transaction.allInstances()
    ->select(t |
      Account.allInstances()->exists(a |
        a.accountId = t.accountId and
        a.userId = userId
      )
    )
    ->includesAll(
      Transaction.allInstances()
        ->select(t |
          Account.allInstances()->exists(a |
            a.accountId = t.accountId and
            a.userId = userId
          )
        )
    )

Technical constraints:
- userId shall be obtained from the validated JWT.
- Transactions from accounts owned by other users shall not contribute to the savings summary.


BR-SAV-02: Savings summary year resolution

context SavingsController::getSavingsSummary(
  request : AuthenticatedRequest,
  year : String
) : SavingsSummaryResponseDto

post BR_SAV_02_ValidYearUsed:
  let parsedYear : Integer = parseInt(year, 10)
  in
    (
      not isNaN(parsedYear) and
      parsedYear >= 1900 and
      parsedYear <= 2100
    )
    implies
      result.year = parsedYear

post BR_SAV_02_InvalidYearDefaultsToCurrentYear:
  let parsedYear : Integer = parseInt(year, 10)
  in
    (
      year.oclIsUndefined() or
      isNaN(parsedYear) or
      parsedYear < 1900 or
      parsedYear > 2100
    )
    implies
      result.year = currentYear()

Technical constraint:
- The implementation uses JavaScript parseInt(year, 10).
- Therefore, a value such as "2025abc" resolves to 2025 rather than defaulting to the current year.

## Row 350

Column B:

BR-SAV-03: Complete monthly summary

context SavingsService::getSavingsSummary(
  userId : Integer,
  year : Integer
) : SavingsSummaryResponseDto

post BR_SAV_03_TwelveMonthsThisYear:
  result.summary.this_year->size() = 12

post BR_SAV_03_TwelveMonthsLastYear:
  result.summary.last_year->size() = 12

post BR_SAV_03_ThisYearMonthOrder:
  Sequence{1..12}->forAll(i |
    result.summary.this_year->at(i).month =
      padTwoDigits(i)
  )

post BR_SAV_03_LastYearMonthOrder:
  Sequence{1..12}->forAll(i |
    result.summary.last_year->at(i).month =
      padTwoDigits(i)
  )

Technical constraint:
- Month values shall be returned as two-digit strings from "01" through "12" in ascending order.


BR-SAV-04: Monthly net savings calculation

context SavingsService::getSavingsSummary(
  userId : Integer,
  year : Integer
) : SavingsSummaryResponseDto

post BR_SAV_04_ThisYearAmounts:
  result.summary.this_year->forAll(dto |
    let monthNumber : Integer =
      dto.month.toInteger()
    in
    let ownedAccountIds : Set(Integer) =
      Account.allInstances()
        ->select(a | a.userId = userId)
        ->collect(a | a.accountId)
        ->asSet()
    in
    let monthlyTransactions : Set(Transaction) =
      Transaction.allInstances()
        ->select(t |
          ownedAccountIds->includes(t.accountId) and
          yearOf(t.transactionDate) = year and
          monthOf(t.transactionDate) = monthNumber
        )
        ->asSet()
    in
    let revenue : Decimal =
      monthlyTransactions
        ->select(t |
          t.type = TransactionType::REVENUE
        )
        ->collect(t | t.amount)
        ->sum()
    in
    let expense : Decimal =
      monthlyTransactions
        ->select(t |
          t.type = TransactionType::EXPENSE
        )
        ->collect(t | t.amount)
        ->sum()
    in
      dto.amount = roundToTwoDecimals(
        revenue - expense
      )
  )

Technical constraint:
- Monthly savings equals total Revenue minus total Expense across all accounts owned by the authenticated user.

## Row 351

Column B:

BR-SAV-05: Previous-year comparison

context SavingsService::getSavingsSummary(
  userId : Integer,
  year : Integer
) : SavingsSummaryResponseDto

post BR_SAV_05_LastYearAmounts:
  result.summary.last_year->forAll(dto |
    let monthNumber : Integer =
      dto.month.toInteger()
    in
    let ownedAccountIds : Set(Integer) =
      Account.allInstances()
        ->select(a | a.userId = userId)
        ->collect(a | a.accountId)
        ->asSet()
    in
    let monthlyTransactions : Set(Transaction) =
      Transaction.allInstances()
        ->select(t |
          ownedAccountIds->includes(t.accountId) and
          yearOf(t.transactionDate) = year - 1 and
          monthOf(t.transactionDate) = monthNumber
        )
        ->asSet()
    in
    let revenue : Decimal =
      monthlyTransactions
        ->select(t |
          t.type = TransactionType::REVENUE
        )
        ->collect(t | t.amount)
        ->sum()
    in
    let expense : Decimal =
      monthlyTransactions
        ->select(t |
          t.type = TransactionType::EXPENSE
        )
        ->collect(t | t.amount)
        ->sum()
    in
      dto.amount = roundToTwoDecimals(
        revenue - expense
      )
  )

Technical constraint:
- this_year represents the resolved target year.
- last_year represents exactly resolvedYear - 1.


BR-SAV-06: Missing transaction data

context SavingsService::getSavingsSummary(
  userId : Integer,
  year : Integer
) : SavingsSummaryResponseDto

post BR_SAV_06_ZeroForMissingThisYearData:
  result.summary.this_year->forAll(dto |
    let monthNumber : Integer =
      dto.month.toInteger()
    in
    let matchingTransactions : Set(Transaction) =
      Transaction.allInstances()
        ->select(t |
          Account.allInstances()->exists(a |
            a.accountId = t.accountId and
            a.userId = userId
          ) and
          yearOf(t.transactionDate) = year and
          monthOf(t.transactionDate) = monthNumber
        )
        ->asSet()
    in
      matchingTransactions->isEmpty()
      implies
        dto.amount = 0
  )

post BR_SAV_06_ZeroForMissingLastYearData:
  result.summary.last_year->forAll(dto |
    let monthNumber : Integer =
      dto.month.toInteger()
    in
    let matchingTransactions : Set(Transaction) =
      Transaction.allInstances()
        ->select(t |
          Account.allInstances()->exists(a |
            a.accountId = t.accountId and
            a.userId = userId
          ) and
          yearOf(t.transactionDate) = year - 1 and
          monthOf(t.transactionDate) = monthNumber
        )
        ->asSet()
    in
      matchingTransactions->isEmpty()
      implies
        dto.amount = 0
  )

Technical constraint:
- If the user owns no accounts, both returned series shall still contain 12 entries with amount = 0.

## Row 352

Column B:

BR-SAV-07: Savings amount rounding

context SavingsService::getSavingsSummary(
  userId : Integer,
  year : Integer
) : SavingsSummaryResponseDto

post BR_SAV_07_ThisYearRounded:
  result.summary.this_year->forAll(dto |
    dto.amount =
      roundToTwoDecimals(dto.amount)
  )

post BR_SAV_07_LastYearRounded:
  result.summary.last_year->forAll(dto |
    dto.amount =
      roundToTwoDecimals(dto.amount)
  )

Technical constraint:
- Every calculated monthly amount shall be rounded to two decimal places before being returned.


BR-SAV-08: Response consistency and read-only behavior

context SavingsService::getSavingsSummary(
  userId : Integer,
  year : Integer
) : SavingsSummaryResponseDto

post BR_SAV_08_ResponseConsistency:
  result.user_id = userId and
  result.year = year and
  not result.summary.oclIsUndefined() and
  result.summary.this_year->size() = 12 and
  result.summary.last_year->size() = 12

post BR_SAV_08_AccountIdentityUnchanged:
  Account.allInstances()
    ->collect(a | a.accountId)
    ->asSet()
  =
  Account.allInstances()@pre
    ->collect(a | a.accountId)
    ->asSet()

post BR_SAV_08_TransactionIdentityUnchanged:
  Transaction.allInstances()
    ->collect(t | t.transactionId)
    ->asSet()
  =
  Transaction.allInstances()@pre
    ->collect(t | t.transactionId)
    ->asSet()

Technical constraints:
- Retrieving the savings summary shall not create, update, or delete Account or Transaction records.
- If the savings calculation fails unexpectedly, the backend shall return HTTP 500 Internal Server Error.

BR-SAV-09: Savings chart point value tooltip

context SavingsSummaryChart::hoverPoint(
  series : SavingsSeries,
  month : String
) : SavingsTooltip

pre BR_SAV_09_ChartDisplayed:
  self.isChartVisible = true

pre BR_SAV_09_PointExists:
  (
    series = SavingsSeries::THIS_YEAR
    implies
      self.summary.this_year->exists(p |
        p.month = month
      )
  )
  and
  (
    series = SavingsSeries::LAST_YEAR
    implies
      self.summary.last_year->exists(p |
        p.month = month
      )
  )

post BR_SAV_09_TooltipVisible:
  result.visible = true

post BR_SAV_09_CorrectThisYearValue:
  series = SavingsSeries::THIS_YEAR
  implies
    self.summary.this_year->exists(p |
      p.month = month and
      result.month = p.month and
      result.amount = p.amount
    )

post BR_SAV_09_CorrectLastYearValue:
  series = SavingsSeries::LAST_YEAR
  implies
    self.summary.last_year->exists(p |
      p.month = month and
      result.month = p.month and
      result.amount = p.amount
    )

context SavingsSummaryChart::leavePoint()

post BR_SAV_09_TooltipHidden:
  self.tooltip.visible = false

Technical constraints:
- Each rendered data point in both yearly series shall be hoverable.
- The tooltip amount shall exactly match the amount of the hovered monthly data point.
- Moving the pointer away from the data point shall hide the tooltip.

## Row 353

Column A:

Related UI

Column B:

GoalsPage; SavingsSummaryChart; year selector

## Row 354

Column A:

Related API IDs

Column B:

API-SAVINGS-SUMMARY

## Row 355

Column A:

Notes

Column B:

Parsing clarification: The year is resolved from its leading base-10 numeric prefix; for example, “2025abc” resolves to 2025. The current year is used only when the resolved value is missing, non-numeric, below 1900, or above 2100.


