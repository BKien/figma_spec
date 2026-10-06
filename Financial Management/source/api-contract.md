# Source snapshot: API contract

Spreadsheet: https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit

Retrieved: 2026-09-30 (Asia/Saigon)

## Row 1

Column A:

API CONTRACT

## Row 3

Column A:

API-AUTH-LOGIN - Login

## Row 4

Column A:

API ID

Column B:

API-AUTH-LOGIN

## Row 5

Column A:

API Name

Column B:

User Login

## Row 6

Column A:

Related Use Case IDs

Column B:

UC-02

## Row 7

Column A:

Method

Column B:

POST

## Row 8

Column A:

Path

Column B:

/api/auth/login

## Row 9

Column A:

Description

Column B:

Authenticate a registered user and issue a JWT access token.

## Row 10

Column A:

Authentication

Column B:

Public

## Row 11

Column A:

Authorization

Column B:

None

## Row 12

Column A:

Business Rules / Validation Constraints

Column B:

BR-LOG-01 - Valid login email:
The login email shall be defined, non-empty, and have a valid email format.

BR-LOG-02 - Non-empty login password:
The login password shall be defined and non-empty.

BR-LOG-03 - Existing login account:
Login can succeed only if a user account corresponding to the submitted email exists in the system.

BR-LOG-04 - Credential verification:
Login can succeed only if the submitted password matches the stored password hash of the user corresponding to the submitted email.

BR-LOG-05 - Invalid credential handling:
If the submitted email does not correspond to an existing user or the submitted password does not match the stored password hash, the login attempt shall be rejected.

BR-LOG-06 - Successful login:
When the submitted credentials are valid, the system shall authenticate the user, issue a JWT access token, and return the authenticated user's basic information.

## Row 13

Column A:

Request Header(s)

Column B:

• headers.Content-Type
  Type: string; Format: MIME type; Required: Yes; Nullable: No
  Default: application/json
  Allowed values: application/json
  Validation: Request body must be JSON.
  Trigger: Every request containing a JSON body.
  Description: Declares the request body format.
  Example: application/json

## Row 14

Column A:

Request Body

Column B:

• email
  Type: string; Format: email; Required: Yes; Nullable: No
  Validation: Must be a valid email address and must not be empty.
  Trigger: Login request.
  Description: Registered email address.
  Example: user@example.com

• password
  Type: string; Format: password; Required: Yes; Nullable: No
  Validation: Must be a non-empty string.
  Trigger: Login request.
  Description: User password.
  Example: P@ssw0rd!

## Row 15

Column A:

Success Response — HTTP 200

Column B:

• success
  Type: boolean; Required: Yes; Nullable: No
  Trigger: Credentials are valid.
  Description: Indicates whether authentication succeeded.
  Example: true

• message
  Type: string; Required: Yes; Nullable: No
  Trigger: Credentials are valid.
  Description: Human-readable success message.
  Example: Successful Login

• data.accessToken
  Type: string; Required: Yes; Nullable: No
  Trigger: Credentials are valid.
  Description: JWT access token.
  Example: eyJhbGciOiJIUzI1NiIs...

• data.user.id
  Type: integer; Required: Yes; Nullable: No
  Trigger: Credentials are valid.
  Description: Authenticated user identifier.
  Example: 1

• data.user.fullName
  Type: string; Required: Yes; Nullable: No
  Trigger: Credentials are valid.
  Description: Authenticated user's full name.
  Example: John Doe

• data.user.email
  Type: string; Required: Yes; Nullable: No
  Trigger: Credentials are valid.
  Description: Authenticated user's email address.
  Example: user@example.com

## Row 16

Column A:

Error Response — HTTP 400

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: Email is invalid, a required field is empty, or an undeclared field is supplied.
  Description: Error description returned by the global HTTP exception filter.
  Example: ["Email không hợp lệ"]
  Note: The error envelope also contains success=false and may contain an error field.

## Row 17

Column A:

Error Response — HTTP 401

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The email is not registered or the password is incorrect.
  Description: Error description returned by the global HTTP exception filter.
  Example: Email or password is incorrect.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 18

Column A:

Error Response — HTTP 500

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: An unexpected authentication or database error occurs.
  Description: Error description returned by the global HTTP exception filter.
  Example: Internal Server Error
  Note: The error envelope also contains success=false and may contain an error field.

## Row 19

Column A:

Notes

## Row 21

Column A:

API-AUTH-REGISTER - Register An Account

## Row 22

Column A:

API ID

Column B:

API-AUTH-REGISTER

## Row 23

Column A:

API Name

Column B:

User Registration

## Row 24

Column A:

Related Use Case IDs

Column B:

UC-01

## Row 25

Column A:

Method

Column B:

POST

## Row 26

Column A:

Path

Column B:

/api/auth/register

## Row 27

Column A:

Description

Column B:

Create a new user account and issue a JWT token.

## Row 28

Column A:

Authentication

Column B:

Public

## Row 29

Column A:

Authorization

Column B:

None

## Row 30

Column A:

Business Rules / Validation Constraints

Column B:

BR-REG-01 - Valid registration full name: `fullName` shall not be null, undefined, empty, or whitespace-only; it shall be normalized using Unicode NFC and `trim()`, contain between 4 and 25 characters, and contain only Unicode letters separated by single spaces.

BR-REG-02 - Valid registration email: `email` shall be non-empty, trimmed, no longer than 255 characters, and satisfy `class-validator` `IsEmail`; it shall be converted to lowercase before storage and comparison.

BR-REG-03 - Unique registration email: A registration email shall not already identify a stored User, regardless of letter case; uniqueness shall be enforced at both the service and database layers.

BR-REG-04 - Valid registration password: `password` shall be between 8 and 64 characters, contain no whitespace, and include at least one lowercase letter, one uppercase letter, one digit, and one permitted special character.

BR-REG-05 - Permitted password characters: A registration password shall contain only Latin letters, digits, and the permitted special characters `! @ # $ % ^ & * ( ) { } - _ + = [ ] , . / < > ? \\ | : ;`.

BR-REG-06 - Matching registration passwords: `confirmPassword` shall be non-empty and shall exactly equal `password`, including letter case.

BR-REG-07 - Confirm password handling: `confirmPassword` shall not be stored in the database or written to application logs.

BR-REG-08 - Invalid registration handling: If any registration field violates a validation or business rule, the system shall reject the request and shall not create a User record.

BR-REG-09 - Bcrypt password storage: A registered password shall be hashed with bcrypt using 10 salt rounds before the User record is saved; the plaintext password shall not be stored, logged, or returned.

BR-REG-10 - Concurrent registration conflict handling: If concurrent registration requests use the same normalized email, exactly one User record shall be created. Each conflicting request shall be rejected with HTTP 409 Conflict; no JWT shall be issued and no authenticated session shall be established for the rejected request.

BR-REG-11 - Successful registration: After successful registration, the system shall create the User, issue a JWT access token, establish an authenticated session, and redirect the user to the home page.

## Row 31

Column A:

Request Header(s)

Column B:

• headers.Content-Type
  Type: string; Format: MIME type; Required: Yes; Nullable: No
  Default: application/json
  Allowed values: application/json
  Validation: Request body must be JSON.
  Trigger: Every request containing a JSON body.
  Description: Declares the request body format.
  Example: application/json

## Row 32

Column A:

Request Body

Column B:

• fullName
  Type: string; Required: Yes; Nullable: No
  Validation: Must be a non-empty string.
  Trigger: Registration request.
  Description: User's full name.
  Example: John Doe

• email
  Type: string; Format: email; Required: Yes; Nullable: No
  Validation: Must be a valid, non-empty email address.
  Trigger: Registration request.
  Description: Unique email address.
  Example: user@example.com

• password
  Type: string; Format: password; Required: Yes; Nullable: No
  Validation: Must be a non-empty string.
  Trigger: Registration request.
  Description: New password.
  Example: P@ssw0rd!

• confirmPassword
  Type: string; Format: password; Required: Yes; Nullable: No
  Validation: Must be a non-empty string and equal password.
  Trigger: Registration request.
  Description: Password confirmation.
  Example: P@ssw0rd!

## Row 33

Column A:

Success Response - HTTP 201

Column B:

• success
  Type: boolean; Required: Yes; Nullable: No
  Trigger: The account is created successfully.
  Description: Indicates that registration succeeded.
  Example: true

• message
  Type: string; Required: Yes; Nullable: No
  Trigger: The account is created successfully.
  Description: Human-readable registration success message.
  Example: Registration successful

• data.accessToken
  Type: string; Required: Yes; Nullable: No
  Trigger: The account is created successfully.
  Description: JWT access token issued for the created user.
  Example: eyJhbGciOiJIUzI1NiIs...

• data.user.id
  Type: integer; Required: Yes; Nullable: No
  Trigger: The account is created successfully.
  Description: Created user identifier.
  Example: 1

• data.user.fullName
  Type: string; Required: Yes; Nullable: No
  Trigger: The account is created successfully.
  Description: Normalized full name of the created user.
  Example: John Doe

• data.user.email
  Type: string; Required: Yes; Nullable: No
  Trigger: The account is created successfully.
  Description: Normalized email address of the created user.
  Example: user@example.com

## Row 34

Column A:

Error Response - HTTP 400

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: Input validation fails or password and confirmPassword do not match.
  Description: Error description returned by the global HTTP exception filter.
  Example: Bad Request / Passwords do not match.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 35

Column A:

Error Response - HTTP 409

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The email address is already registered.
  Description: Error description returned by the global HTTP exception filter.
  Example: Conflict / This email is already registered.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 36

Column A:

Error Response - HTTP 500

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The user record or token cannot be created.
  Description: Error description returned by the global HTTP exception filter.
  Example: Internal Server Error
  Note: The error envelope also contains success=false and may contain an error field.

## Row 37

Column A:

Notes

## Row 39

Column A:

API-ACCOUNT-LIST — List User Accounts

## Row 40

Column A:

API ID

Column B:

API-ACCOUNT-LIST

## Row 41

Column A:

API Name

Column B:

List User Accounts

## Row 42

Column A:

Related Use Case IDs

Column B:

UC-05

## Row 43

Column A:

Method

Column B:

GET

## Row 44

Column A:

Path

Column B:

/api/v1/accounts

## Row 45

Column A:

Description

Column B:

Return all bank accounts owned by the authenticated user.

## Row 46

Column A:

Authentication

Column B:

Bearer JWT

## Row 47

Column A:

Authorization

Column B:

Authenticated user

## Row 48

Column A:

Request Header(s)

Column B:

• headers.Authorization
  Type: string; Format: Bearer <JWT>; Required: Yes; Nullable: No
  Trigger: Every protected request.
  Description: Authenticates the current user.
  Example: Bearer eyJhbGciOiJIUzI1NiIs...
  Note: Added by the frontend Axios interceptor.

## Row 49

Column A:

Request Body

Column B:

None

## Row 50

Column A:

Success Response — HTTP 200

Column B:

• success
  Type: boolean; Required: Yes; Nullable: No
  Trigger: The user is authenticated.
  Description: Indicates successful retrieval.
  Example: true

• message
  Type: string; Required: Yes; Nullable: No
  Trigger: The user is authenticated.
  Description: Human-readable success message.
  Example: Account list retrieved successfully.

• data.user_id
  Type: integer; Required: Yes; Nullable: No
  Trigger: The user is authenticated.
  Description: Authenticated user identifier.
  Example: 1

• data.accounts
  Type: array<object>; Required: Yes; Nullable: No
  Trigger: The user is authenticated.
  Description: Array of accounts. May be empty.
  Example: []

• data.accounts[].id
  Type: integer; Required: Yes; Nullable: No
  Trigger: The user is authenticated.
  Description: Account identifier.
  Example: 3

• data.accounts[].bank_name
  Type: string; Required: Yes; Nullable: No
  Trigger: The user is authenticated.
  Description: Bank or financial institution name.
  Example: Vietcombank

• data.accounts[].account_type
  Type: string; Required: Yes; Nullable: No
  Allowed values: Checking; Credit Card; Savings; Investment; Loan
  Trigger: The user is authenticated.
  Description: Account type.
  Example: Checking

• data.accounts[].branch_name
  Type: string; Required: Yes; Nullable: Yes
  Trigger: The user is authenticated.
  Description: Branch name.
  Example: Hanoi Branch

• data.accounts[].account_number_last_4
  Type: string; Required: Yes; Nullable: No
  Trigger: The user is authenticated.
  Description: Last four digits of the account number.
  Example: 0123

• data.accounts[].balance
  Type: number; Required: Yes; Nullable: No
  Trigger: The user is authenticated.
  Description: Current account balance.
  Example: 4500000

## Row 51

Column A:

Error Response — HTTP 401

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The JWT is missing, invalid, or expired.
  Description: Error description returned by the global HTTP exception filter.
  Example: Unauthorized
  Note: The error envelope also contains success=false and may contain an error field.

## Row 52

Column A:

Error Response — HTTP 500

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: Account retrieval fails.
  Description: Error description returned by the global HTTP exception filter.
  Example: system error occurred. Please try again later.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 53

Column A:

Notes

## Row 55

Column A:

API-ACCOUNT-CREATE — Create Bank Account

## Row 56

Column A:

API ID

Column B:

API-ACCOUNT-CREATE

## Row 57

Column A:

API Name

Column B:

Create Bank Account

## Row 58

Column A:

Related Use Case IDs

Column B:

UC-06

## Row 59

Column A:

Method

Column B:

POST

## Row 60

Column A:

Path

Column B:

/api/v1/accounts

## Row 61

Column A:

Description

Column B:

Create a new bank account owned by the authenticated user.

## Row 62

Column A:

Authentication

Column B:

Bearer JWT

## Row 63

Column A:

Authorization

Column B:

Authenticated user

## Row 64

Column A:

Request Header(s)

Column B:

• headers.Authorization
 Type: string; Format: Bearer <JWT>; Required: Yes; Nullable: No
 Trigger: Every protected request.
 Description: Authenticates the current user.
 Example: Bearer eyJhbGciOiJIUzI1NiIs...
 Note: Added by the frontend Axios interceptor.

• headers.Content-Type
 Type: string; Format: MIME type; Required: Yes; Nullable: No
 Default: application/json
 Allowed values: application/json
 Trigger: Every request containing a JSON body.
 Description: Declares the request body format.
 Example: application/json

## Row 65

Column A:

Request Body

Column B:

• bank_name
  Type: string; Required: Yes; Nullable: No
  Trigger: Account creation request.
  Description: Bank name.
  Example: Vietcombank

• account_type
  Type: string; Required: Yes; Nullable: No
  Allowed values: Checking; Credit Card; Savings; Investment; Loan
  Trigger: Account creation request.
  Description: Account type.
  Example: Checking

• branch_name
  Type: string; Required: No; Nullable: Yes
  Trigger: Account creation request.
  Description: Optional branch name.
  Example: Hanoi Branch

• account_number_full
  Type: string; Required: Yes; Nullable: No
  Trigger: Account creation request.
  Description: Full account number.
  Example: 9704221234567890123

• balance
  Type: number; Format: decimal; Required: Yes; Nullable: No
  Trigger: Account creation request.
  Description: Initial balance.
  Example: 4500000

## Row 66

Column A:

Success Response — HTTP 201

Column B:

• message
  Type: string; Required: Yes; Nullable: No
  Trigger: The account is created.
  Description: Creation success message.
  Example: Account created successfully

• account.id
  Type: integer; Required: Yes; Nullable: No
  Trigger: The account is created.
  Description: Created account identifier.
  Example: 3

• account.user_id
  Type: integer; Required: Yes; Nullable: No
  Trigger: The account is created.
  Description: Owner user identifier.
  Example: 1

• account.bank_name
  Type: string; Required: Yes; Nullable: No
  Trigger: The account is created.
  Description: Bank name.
  Example: Vietcombank

• account.account_type
  Type: string; Required: Yes; Nullable: No
  Allowed values: Checking; Credit Card; Savings; Investment; Loan
  Trigger: The account is created.
  Description: Account type.
  Example: Checking

• account.branch_name
  Type: string; Required: Yes; Nullable: Yes
  Trigger: The account is created.
  Description: Branch name.
  Example: Hanoi Branch

• account.account_number_last_4
  Type: string; Required: Yes; Nullable: No
  Trigger: The account is created.
  Description: Derived last four digits.
  Example: 0123

• account.balance
  Type: number; Required: Yes; Nullable: No
  Trigger: The account is created.
  Description: Stored account balance.
  Example: 4500000

## Row 67

Column A:

Error Response — HTTP 400

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: Request validation fails due to malformed payload or missing required fields.
  Description: Error description returned by the global HTTP exception filter.
  Example: Invalid input formatting or missing required parameters.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 68

Column A:

Error Response — HTTP 401

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The JWT is missing, invalid, or expired.
  Description: Error description returned by the global HTTP exception filter.
  Example: Unauthorized access. Please log in again.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 69

Column A:

Error Response — HTTP 403

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The authenticated user is denied access to perform the requested operation on this resource.
  Description: Error description returned by the global HTTP exception filter.
  Example: Forbidden. You do not have sufficient privileges to execute this action.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 70

Column A:

Error Response — HTTP 409

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: A unique constraint violation occurred during data insertion.
  Description: Error description returned by the global HTTP exception filter.
  Example: The submitted resource conflicts with an existing record in the system.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 71

Column A:

Error Response — HTTP 500

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: An unexpected server error prevents the resource from being saved.
  Description: Error description returned by the global HTTP exception filter.
  Example: An internal server error occurred while processing your request. Please try again later.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 72

Column A:

Notes

## Row 74

Column A:

API-ACCOUNT-DETAIL — Get Account Details

## Row 75

Column A:

API ID

Column B:

API-ACCOUNT-DETAIL

## Row 76

Column A:

API Name

Column B:

Get Account Details

## Row 77

Column A:

Related Use Case IDs

Column B:

UC-07

## Row 78

Column A:

Method

Column B:

GET

## Row 79

Column A:

Path

Column B:

/api/v1/accounts/:id

## Row 80

Column A:

Description

Column B:

Return one owned account and its five most recent transactions.

## Row 81

Column A:

Authentication

Column B:

Bearer JWT

## Row 82

Column A:

Authorization

Column B:

Account owner

## Row 83

Column A:

Business Rules / Validation Constraints

Column B:

BR-AUTH-01 — JWT-protected operation: Protected controllers require JwtAuthGuard and obtain userId from the validated JWT payload.

BR-ACC-15 — Account existence and ownership: Account detail operations shall succeed only when account.userId equals the authenticated userId.

BR-ACC-16 — Five most recent account transactions: Account detail shall include at most five transactions ordered by transaction_date descending.

BR-ACC-17 — Response rows map to persisted data with signed amounts: Response fields must exactly match the persisted Account and Transaction data. Expense amounts are negated (returned as negative) while Revenue amounts remain positive.

BR-ACC-18 — Viewing details is read-only: Listing account details shall not create, update, or delete any Account, Transaction, User, or Category records.

## Row 84

Column A:

Request Header(s)

Column B:

• headers.Authorization
  Type: string; Format: Bearer <JWT>; Required: Yes; Nullable: No
  Validation: Must contain a valid, unexpired JWT access token.
  Trigger: Every protected request.
  Description: Authenticates the current user.
  Example: Bearer eyJhbGciOiJIUzI1NiIs...
  Note: Added by the frontend Axios interceptor.

## Row 85

Column A:

Path Parameter(s)

Column B:

• path.id
  Type: integer; Required: Yes; Nullable: No
  Validation: Must parse as an integer account identifier.
  Trigger: Account detail request.
  Description: Account identifier.
  Example: 3

## Row 86

Column A:

Request Body

Column B:

None

## Row 87

Column A:

Success Response — HTTP 200

Column B:

• id
  Type: integer; Required: Yes; Nullable: No
  Trigger: The account exists and is owned by the user.
  Description: Account identifier.
  Example: 3

• bank_name
  Type: string; Required: Yes; Nullable: No
  Trigger: The account exists and is owned by the user.
  Description: Bank name.
  Example: Vietcombank

• account_type
  Type: string; Required: Yes; Nullable: No
  Allowed values: Checking; Credit Card; Savings; Investment; Loan
  Trigger: The account exists and is owned by the user.
  Description: Account type.
  Example: Checking

• branch_name
  Type: string; Required: Yes; Nullable: Yes
  Trigger: The account exists and is owned by the user.
  Description: Branch name.
  Example: Hanoi Branch

• account_number_full
  Type: string; Required: Yes; Nullable: No
  Trigger: The account exists and is owned by the user.
  Description: Full account number.
  Example: 9704221234567890123

• balance
  Type: number; Required: Yes; Nullable: No
  Trigger: The account exists and is owned by the user.
  Description: Current balance.
  Example: 4500000

• recent_transactions
  Type: array<object>; Required: Yes; Nullable: No
  Trigger: The account exists and is owned by the user.
  Description: Up to five most recent transactions.
  Example: []

• recent_transactions[].date
  Type: string; Required: Yes; Nullable: No
  Trigger: The account exists and is owned by the user.
  Description: Transaction date.
  Example: 2025-11-01

• recent_transactions[].amount
  Type: number; Required: Yes; Nullable: No
  Trigger: The account exists and is owned by the user.
  Description: Signed amount; expenses are returned as negative values.
  Example: -150000

• recent_transactions[].description
  Type: string; Required: Yes; Nullable: No
  Trigger: The account exists and is owned by the user.
  Description: Transaction description.
  Example: Movie Ticket

• recent_transactions[].status
  Type: string; Required: Yes; Nullable: No
  Allowed values: Complete; Pending; Failed
  Trigger: The account exists and is owned by the user.
  Description: Transaction status.
  Example: Complete

• recent_transactions[].receipt_id
  Type: string; Required: Yes; Nullable: Yes
  Trigger: The account exists and is owned by the user.
  Description: Receipt identifier.
  Example: null

• recent_transactions[].type
  Type: string; Required: Yes; Nullable: No
  Allowed values: Revenue; Expense
  Trigger: The account exists and is owned by the user.
  Description: Transaction type.
  Example: Expense

## Row 88

Column A:

Error Response — HTTP 400

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The path parameter is not a valid integer.
  Description: Error description returned by the global HTTP exception filter.
  Example: Invalid account ID.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 89

Column A:

Error Response — HTTP 401

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The JWT is missing, invalid, or expired.
  Description: Error description returned by the global HTTP exception filter.
  Example: Unable to authenticate the user. Please log in again.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 90

Column A:

Error Response — HTTP 403

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The account belongs to another user.
  Description: Error description returned by the global HTTP exception filter.
  Example: You are not authorized to view this account information.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 91

Column A:

Error Response — HTTP 404

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The account does not exist.
  Description: Error description returned by the global HTTP exception filter.
  Example: This account was not found.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 92

Column A:

Error Response — HTTP 500

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: Account or transaction retrieval fails.
  Description: Error description returned by the global HTTP exception filter.
  Example: A system error occurred while retrieving the account details. Please try again later.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 93

Column A:

Notes

## Row 95

Column A:

API-ACCOUNT-UPDATE — Update Bank Account

## Row 96

Column A:

API ID

Column B:

API-ACCOUNT-UPDATE

## Row 97

Column A:

API Name

Column B:

Update Bank Account

## Row 98

Column A:

Related Use Case IDs

Column B:

UC-08, UC-08.1

## Row 99

Column A:

Method

Column B:

PUT

## Row 100

Column A:

Path

Column B:

/api/v1/accounts/:id

## Row 101

Column A:

Description

Column B:

Update an account owned by the authenticated user.

## Row 102

Column A:

Authentication

Column B:

Bearer JWT

## Row 103

Column A:

Authorization

Column B:

Account owner

## Row 104

Column A:

Business Rules / Validation Constraints

Column B:

BR-AUTH-01 — JWT-protected operation: Protected controllers require JwtAuthGuard and obtain userId from the validated JWT payload.

BR-ACC-19 — Account ownership validation for update: The account must exist and belong to the authenticated user.
BR-ACC-20 — Allowed account types for update: The submitted account_type must strictly belong to the allowed enumeration.

BR-ACC-21 — Required account text fields for update: The payload must include non-empty strings for bank_name and account_number_full.

BR-ACC-22 — Account number format and length for update: The account_number_full must contain only numeric digits and its length must be between 8 and 34 characters.

BR-ACC-23 — Numeric non-negative account balance for update: The balance must be a valid numeric type and cannot be negative.

BR-ACC-24 — Optional branch name handling during update: The branch_name field is optional and may be saved as null or undefined.

BR-ACC-25 — Derive final four account characters for update: The backend MUST implicitly derive account_number_last_4 by taking the exact last 4 characters of the submitted account_number_full.

BR-ACC-26 — Account update persistence mapping: The submitted fields overwrite the existing account data and map directly to persisted database records.

## Row 105

Column A:

Request Header(s)

Column B:

• headers.Authorization
  Type: string; Format: Bearer <JWT>; Required: Yes; Nullable: No
  Validation: Must contain a valid, unexpired JWT access token.
  Trigger: Every protected request.
  Description: Authenticates the current user.
  Example: Bearer eyJhbGciOiJIUzI1NiIs...
  Note: Added by the frontend Axios interceptor.

• headers.Content-Type
  Type: string; Format: MIME type; Required: Yes; Nullable: No
  Default: application/json
  Allowed values: application/json
  Validation: Request body must be JSON.
  Trigger: Every request containing a JSON body.
  Description: Declares the request body format.
  Example: application/json

## Row 106

Column A:

Path Parameter(s)

Column B:

• path.id
  Type: integer; Required: Yes; Nullable: No
  Validation: Must parse as an integer account identifier.
  Trigger: Account update request.
  Description: Account identifier.
  Example: 3

## Row 107

Column A:

Request Body

Column B:

• bank_name
  Type: string; Required: Yes; Nullable: No
  Validation: Must be a non-empty string.
  Trigger: Account update request.
  Description: Updated bank name.
  Example: Vietcombank

• account_type
  Type: string; Required: Yes; Nullable: No
  Allowed values: Checking; Credit Card; Savings; Investment; Loan
  Validation: Must be an allowed account type.
  Trigger: Account update request.
  Description: Updated account type.
  Example: Checking

• branch_name
  Type: string; Required: No; Nullable: Yes
  Validation: If supplied, must be a string.
  Trigger: Account update request.
  Description: Updated branch name.
  Example: Hanoi Branch

• account_number_full
  Type: string; Required: Yes; Nullable: No
  Validation: Must be a non-empty string.
  Trigger: Account update request.
  Description: Updated full account number.
  Example: 9704221234567890123

• balance
  Type: number; Format: decimal; Required: Yes; Nullable: No
  Validation: Must be greater than or equal to 0.
  Trigger: Account update request.
  Description: Updated balance.
  Example: 4500000

## Row 108

Column A:

Success Response — HTTP 200

Column B:

• message
  Type: string; Required: Yes; Nullable: No
  Trigger: The account is updated.
  Description: Update success message.
  Example: Account updated successfully

• account.account_id
  Type: integer; Required: Yes; Nullable: No
  Trigger: The account is updated.
  Description: Updated account identifier.
  Example: 3

• account.user_id
  Type: integer; Required: Yes; Nullable: No
  Trigger: The account is updated.
  Description: Owner identifier.
  Example: 1

• account.bank_name
  Type: string; Required: Yes; Nullable: No
  Trigger: The account is updated.
  Description: Updated bank name.
  Example: Vietcombank

• account.account_type
  Type: string; Required: Yes; Nullable: No
  Allowed values: Checking; Credit Card; Savings; Investment; Loan
  Trigger: The account is updated.
  Description: Updated account type.
  Example: Checking

• account.branch_name
  Type: string; Required: Yes; Nullable: Yes
  Trigger: The account is updated.
  Description: Updated branch name.
  Example: Hanoi Branch

• account.account_number_full
  Type: string; Required: Yes; Nullable: No
  Trigger: The account is updated.
  Description: Updated full account number.
  Example: 9704221234567890123

• account.account_number_last_4
  Type: string; Required: Yes; Nullable: No
  Trigger: The account is updated.
  Description: Updated final four digits.
  Example: 0123

• account.balance
  Type: number; Required: Yes; Nullable: No
  Trigger: The account is updated.
  Description: Updated balance.
  Example: 4500000

## Row 109

Column A:

Error Response — HTTP 400

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The path ID or request body is invalid.
  Description: Error description returned by the global HTTP exception filter.
  Example: Balance must not be less than 0
  Note: The error envelope also contains success=false and may contain an error field.

## Row 110

Column A:

Error Response — HTTP 401

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The JWT is missing, invalid, or expired.
  Description: Error description returned by the global HTTP exception filter.
  Example: Unable to authenticate the user. Please log in again.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 111

Column A:

Error Response — HTTP 403

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The account belongs to another user.
  Description: Error description returned by the global HTTP exception filter.
  Example: You do not have permission to edit this account information.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 112

Column A:

Error Response — HTTP 404

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The account does not exist.
  Description: Error description returned by the global HTTP exception filter.
  Example: This account could not be found.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 113

Column A:

Error Response — HTTP 500

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The updated account cannot be stored.
  Description: Error description returned by the global HTTP exception filter.
  Example: An error occurred while saving the data. Please try again later.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 114

Column A:

Notes

## Row 116

Column A:

API-ACCOUNT-DELETE — Delete Bank Account

## Row 117

Column A:

API ID

Column B:

API-ACCOUNT-DELETE

## Row 118

Column A:

API Name

Column B:

Delete Bank Account

## Row 119

Column A:

Related Use Case IDs

Column B:

UC-09

## Row 120

Column A:

Method

Column B:

DELETE

## Row 121

Column A:

Path

Column B:

/api/v1/accounts/:id

## Row 122

Column A:

Description

Column B:

Delete an owned account and all transactions related to it.

## Row 123

Column A:

Authentication

Column B:

Bearer JWT

## Row 124

Column A:

Authorization

Column B:

Account owner

## Row 125

Column A:

Business Rules / Validation Constraints

Column B:

BR-AUTH-01 — JWT-protected operation: Protected controllers require JwtAuthGuard and obtain userId from the validated JWT payload.

BR-ACC-27 — Account deletion ownership validation: Delete succeeds only for an owned account. A missing account and a non-owned account both produce the same HTTP 404 exception.

BR-ACC-28 — Account deletion data integrity (Cascading): Related Transaction rows and the Account row shall be deleted within one TypeORM query-runner transaction.

## Row 126

Column A:

Request Header(s)

Column B:

• headers.Authorization
  Type: string; Format: Bearer <JWT>; Required: Yes; Nullable: No
  Validation: Must contain a valid, unexpired JWT access token.
  Trigger: Every protected request.
  Description: Authenticates the current user.
  Example: Bearer eyJhbGciOiJIUzI1NiIs...
  Note: Added by the frontend Axios interceptor.

## Row 127

Column A:

Path Parameter(s)

Column B:

• path.id
  Type: integer; Required: Yes; Nullable: No
  Validation: Must parse as an integer account identifier.
  Trigger: Account deletion request.
  Description: Account identifier.
  Example: 3

## Row 128

Column A:

Request Body

Column B:

None

## Row 129

Column A:

Success Response — HTTP 200

Column B:

• message
  Type: string; Required: Yes; Nullable: No
  Trigger: The account exists and is owned by the user.
  Description: Deletion success message.
  Example: Account deleted successfully

• deleted_account_id
  Type: integer; Required: Yes; Nullable: No
  Trigger: The account exists and is owned by the user.
  Description: Deleted account identifier.
  Example: 3

## Row 130

Column A:

Error Response — HTTP 400

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The path ID is not a valid integer.
  Description: Error description returned by the global HTTP exception filter.
  Example: Invalid account ID.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 131

Column A:

Error Response — HTTP 401

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The JWT is missing, invalid, or expired.
  Description: Error description returned by the global HTTP exception filter.
  Example: Unable to authenticate the user. Please log in again.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 132

Column A:

Error Response — HTTP 404

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The account does not exist or is not owned by the current user.
  Description: Error description returned by the global HTTP exception filter.
  Example: Account not found or not owned by current user
  Note: The error envelope also contains success=false and may contain an error field.

## Row 133

Column A:

Error Response — HTTP 500

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: Deleting the account or related transactions fails.
  Description: Error description returned by the global HTTP exception filter.
  Example: A system error occurred. The account and related transactions could not be deleted.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 134

Column A:

Notes

## Row 136

Column A:

API-TRANSACTION-LIST — List Transactions

## Row 137

Column A:

API ID

Column B:

API-TRANSACTION-LIST

## Row 138

Column A:

API Name

Column B:

List Transactions

## Row 139

Column A:

Related Use Case IDs

Column B:

UC-03

## Row 140

Column A:

Method

Column B:

GET

## Row 141

Column A:

Path

Column B:

/api/v1/transactions

## Row 142

Column A:

Description

Column B:

Return the authenticated user's transactions with filtering and pagination.

## Row 143

Column A:

Authentication

Column B:

Bearer JWT

## Row 144

Column A:

Authorization

Column B:

Authenticated user

## Row 145

Column A:

Business Rules / Validation Constraints

Column B:

BR-AUTH-01 — JWT-protected operation: JwtAuthGuard shall validate the bearer JWT and provide the authenticated identifier corresponding to Users.user_id.

BR-TXN-01 — Transaction ownership scope: Every returned Transactions row shall have account_id referencing an Accounts row whose user_id equals the authenticated Users.user_id.

BR-TXN-02 — Allowed transaction filter: query.type shall be All, Revenue, or Expense. All is a query/UI sentinel only and shall never be stored in Transactions.type; persisted type values are Revenue or Expense.

BR-TXN-03 — Pagination and ordering: limit defaults to 10 and must be > 0; offset defaults to 0 and must be >= 0; matching rows are ordered by Transactions.transaction_date descending; hasMore = offset + returnedCount < total.

BR-TXN-04 — Relationship integrity: Transactions.account_id shall reference Accounts.account_id. Transactions.category_id may be null; when present it shall reference Categories.category_id.

BR-TXN-05 — Empty result consistency: When no transaction matches the authenticated ownership scope and selected filter, data shall be [], total shall be 0, and hasMore shall be false.

BR-TXN-06 — Response persistence mapping: Every transaction DTO returned by the endpoint shall correspond to a persisted Transactions row with matching transaction_id, account_id, transaction_date, type, item_description, shop_name, amount, payment_method, and status.

BR-TXN-07 — Read-only operation: Listing transaction history shall not create, update, or delete Transactions or Accounts records.

## Row 146

Column A:

Request Header(s)

Column B:

• headers.Authorization
  Type: string; Format: Bearer <JWT>; Required: Yes; Nullable: No
  Validation: Must contain a valid, unexpired JWT access token.
  Trigger: Every protected request.
  Description: Authenticates the current user.
  Example: Bearer eyJhbGciOiJIUzI1NiIs...
  Note: Added by the frontend Axios interceptor.

## Row 147

Column A:

Query Parameter(s)

Column B:

• query.type
  Type: string; Required: Yes; Nullable: No
  Allowed values: All; Revenue; Expense
  Validation: Must be All, Revenue, or Expense. All is a filtering sentinel and is not a persisted Transactions.type value.
  Trigger: Transaction list request.
  Description: Transaction type filter.
  Example: All

• query.limit
  Type: integer; Required: No; Nullable: No
  Default: 10
  Validation: Must parse as an integer and must be greater than 0.
  Trigger: Transaction list request.
  Description: Maximum number of returned records.
  Example: 10

• query.offset
  Type: integer; Required: No; Nullable: No
  Default: 0
  Validation: Must parse as an integer and must be greater than or equal to 0.
  Trigger: Transaction list request.
  Description: Zero-based pagination offset.
  Example: 0

## Row 148

Column A:

Request Body

Column B:

None

## Row 149

Column A:

Success Response — HTTP 200

Column B:

• data
  Type: array<object>; Required: Yes; Nullable: No
  Trigger: The query is valid.
  Description: Transaction array. May be empty.
  Example: []

• data[].transaction_id
  Type: integer; Required: Yes; Nullable: No
  Trigger: The query is valid.
  Description: Transactions.transaction_id.
  Example: 8

• data[].account_id
  Type: integer; Required: Yes; Nullable: No
  Trigger: The query is valid.
  Description: Transactions.account_id; references an account owned by the authenticated user.
  Example: 3

• data[].transaction_date
  Type: string; Format: date; Required: Yes; Nullable: No
  Trigger: The query is valid.
  Description: Transactions.transaction_date.
  Example: 2025-11-01

• data[].type
  Type: string; Required: Yes; Nullable: No
  Allowed values: Revenue; Expense
  Trigger: The query is valid.
  Description: Transactions.type. All is never returned as a stored type.
  Example: Expense

• data[].item_description
  Type: string; Required: Yes; Nullable: No
  Trigger: The query is valid.
  Description: Transactions.item_description.
  Example: Movie Ticket

• data[].shop_name
  Type: string; Required: Yes; Nullable: No
  Trigger: The query is valid.
  Description: Transactions.shop_name.
  Example: Cinema

• data[].amount
  Type: number; Required: Yes; Nullable: No
  Trigger: The query is valid.
  Description: Transactions.amount.
  Example: 150000

• data[].payment_method
  Type: string; Required: Yes; Nullable: No
  Trigger: The query is valid.
  Description: Transactions.payment_method.
  Example: Credit Card

• data[].status
  Type: string; Required: Yes; Nullable: No
  Allowed values: Complete; Pending; Failed
  Trigger: The query is valid.
  Description: Transactions.status.
  Example: Complete

• total
  Type: integer; Required: Yes; Nullable: No
  Trigger: The query is valid.
  Description: Total records matching the ownership scope and selected filter.
  Example: 25

• hasMore
  Type: boolean; Required: Yes; Nullable: No
  Trigger: The query is valid.
  Description: Whether another page exists; computed as offset + returnedCount < total.
  Example: true

## Row 150

Column A:

Error Response — HTTP 400

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: type is not All, Revenue, or Expense; limit cannot be parsed or is less than or equal to 0; or offset cannot be parsed or is less than 0.
  Description: Error description returned by the global HTTP exception filter.
  Example: Invalid transaction query parameter
  Note: The error envelope also contains success=false and may contain an error field.

## Row 151

Column A:

Error Response — HTTP 401

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The JWT is missing, invalid, or expired.
  Description: Error description returned by the global HTTP exception filter.
  Example: Unauthorized
  Note: The error envelope also contains success=false and may contain an error field.

## Row 152

Column A:

Error Response — HTTP 500

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: Transaction retrieval fails.
  Description: Error description returned by the global HTTP exception filter.
  Example: Đã xảy ra lỗi hệ thống khi lấy danh sách giao dịch. Vui lòng thử lại sau.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 153

Column A:

Notes

## Row 155

Column A:

API-TRANSACTION-CREATE - Create Transaction

## Row 156

Column A:

API ID

Column B:

API-TRANSACTION-CREATE

## Row 157

Column A:

API Name

Column B:

Create Transaction

## Row 158

Column A:

Related Use Case IDs

Column B:

UC-04

## Row 159

Column A:

Method

Column B:

POST

## Row 160

Column A:

Path

Column B:

/api/v1/transactions

## Row 161

Column A:

Description

Column B:

Create a revenue or expense transaction and update the account balance atomically.

## Row 162

Column A:

Authentication

Column B:

Bearer JWT

## Row 163

Column A:

Authorization

Column B:

Owner of the referenced account

## Row 164

Column A:

Business Rules / Validation Constraints

Column B:

BR-AUTH-01 - JWT-protected operation
JwtAuthGuard shall validate the bearer JWT and provide the authenticated identifier corresponding to Users.user_id.

BR-TXN-08 - Required transaction data
accountId, transactionDate, type, itemDescription, shopName, paymentMethod, and amount shall be present. itemDescription, shopName, and paymentMethod shall be non-empty strings; amount shall be at least 0.01. shopName maps to Transactions.shop_name and paymentMethod maps to Transactions.payment_method; neither may be null or empty.

BR-TXN-09 - Allowed type and status 
Type shall be Revenue or Expense. status, when supplied, shall be Complete, Pending, or Failed; when omitted, the stored status shall default to Complete.

BR-TXN-10 - Optional category
category_id is optional/nullable. When supplied, it shall reference an existing Categories.category_id; when omitted, Transactions.category_id shall be null.

BR-TXN-11 - Account ownership
accountId shall reference an Accounts.account_id whose Accounts.user_id equals the authenticated Users.user_id.

BR-TXN-12 - Sufficient Expense balance
For type = Expense, the owned account's balance before creation shall be greater than or equal to amount.

BR-TXN-13 - Account balance adjustment
Revenue increases Accounts.balance by amount; Expense decreases Accounts.balance by amount.

BR-TXN-14 - Transaction persistence mapping
On success exactly one new Transactions row shall be created and shall map accountId -> account_id, transactionDate -> transaction_date, itemDescription -> item_description, shopName -> shop_name, paymentMethod -> payment_method, plus type, amount, status, and optional category_id.

BR-TXN-15 - Atomic creation
The Transactions insert and Accounts.balance update shall commit in one database transaction. If creation fails before commit, both changes shall be rolled back.

## Row 165

Column A:

Request Header(s)

Column B:

• headers.Authorization
  Type: string; Format: Bearer <JWT>; Required: Yes; Nullable: No
  Validation: Must contain a valid, unexpired JWT access token.
  Trigger: Every protected request.
  Description: Authenticates the current user.
  Example: Bearer eyJhbGciOiJIUzI1NiIs...
  Note: Added by the frontend Axios interceptor.

• headers.Content-Type
  Type: string; Format: MIME type; Required: Yes; Nullable: No
  Default: application/json
  Allowed values: application/json
  Validation: Request body must be JSON.
  Trigger: Every request containing a JSON body.
  Description: Declares the request body format.
  Example: application/json

## Row 166

Column A:

Request Body

Column B:

• accountId
  Type: integer; Required: Yes; Nullable: No
  Validation: Must reference Accounts.account_id owned by the authenticated Users.user_id.
  Trigger: Transaction creation request.
  Description: Account identifier.
  Example: 3

• transactionDate
  Type: string; Format: date; Required: Yes; Nullable: No
  Validation: Must be a valid ISO date string.
  Trigger: Transaction creation request.
  Description: Maps to Transactions.transaction_date.
  Example: 2025-11-01

• type
  Type: string; Required: Yes; Nullable: No
  Allowed values: Revenue; Expense
  Validation: Must be Revenue or Expense.
  Trigger: Transaction creation request.
  Description: Maps to Transactions.type.
  Example: Expense

• itemDescription
  Type: string; Required: Yes; Nullable: No
  Validation: Must be a non-empty string.
  Trigger: Transaction creation request.
  Description: Maps to Transactions.item_description.
  Example: Movie Ticket

• category_id
  Type: integer; Required: No; Nullable: Yes
  Validation: When supplied, must reference an existing Categories.category_id.
  Trigger: Transaction creation request.
  Description: Optional transaction category; maps to Transactions.category_id.
  Example: 3
  Note: The request is valid when category_id is omitted/null.

• shopName
  Type: string; Required: Yes; Nullable: No
  Validation: Must be a non-empty string.
  Trigger: Transaction creation request.
  Description: Maps to Transactions.shop_name.
  Example: Cinema

• amount
  Type: number; Format: decimal; Required: Yes; Nullable: No
  Validation: Must be at least 0.01. For Expense, must not exceed the selected account balance.
  Trigger: Transaction creation request.
  Description: Maps to Transactions.amount.
  Example: 150000

• paymentMethod
  Type: string; Required: Yes; Nullable: No
  Validation: Must be a non-empty string.
  Trigger: Transaction creation request.
  Description: Maps to Transactions.payment_method.
  Example: Credit Card

• status
  Type: string; Required: No; Nullable: No
  Default: Complete
  Allowed values: Complete; Pending; Failed
  Validation: When supplied, must be an allowed status.
  Trigger: Transaction creation request.
  Description: Maps to Transactions.status.
  Example: Complete

## Row 167

Column A:

Success Response — HTTP 201

Column B:

• message
  Type: string; Required: Yes; Nullable: No
  Trigger: The transaction and account balance are committed.
  Description: Creation success message.
  Example: Transaction created successfully

• data.transactionId
  Type: integer; Required: Yes; Nullable: No
  Trigger: The transaction and account balance are committed.
  Description: Created transaction identifier.
  Example: 8

• data.accountId
  Type: integer; Required: Yes; Nullable: No
  Trigger: The transaction and account balance are committed.
  Description: Related account identifier.
  Example: 3

• data.transactionDate
  Type: string; Format: date-time; Required: Yes; Nullable: No
  Trigger: The transaction and account balance are committed.
  Description: Stored transaction date.

• data.type
  Type: string; Required: Yes; Nullable: No
  Allowed values: Revenue; Expense
  Trigger: The transaction and account balance are committed.
  Description: Stored transaction type.
  Example: Expense

• data.itemDescription
  Type: string; Required: Yes; Nullable: No
  Trigger: The transaction and account balance are committed.
  Description: Stored description.
  Example: Movie Ticket

• data.shopName
  Type: string; Required: Yes; Nullable: No
  Trigger: The transaction and account balance are committed.
  Description: Stored merchant name from Transactions.shop_name.
  Example: Cinema

• data.amount
  Type: number; Required: Yes; Nullable: No
  Trigger: The transaction and account balance are committed.
  Description: Stored amount.
  Example: 150000

• data.paymentMethod
  Type: string; Required: Yes; Nullable: No
  Trigger: The transaction and account balance are committed.
  Description: Stored payment method from Transactions.payment_method.
  Example: Credit Card

• data.status
  Type: string; Required: Yes; Nullable: No
  Allowed values: Complete; Pending; Failed
  Trigger: The transaction and account balance are committed.
  Description: Stored status.
  Example: Complete

• data.receiptId
  Type: string; Required: Yes; Nullable: Yes
  Trigger: The transaction and account balance are committed.
  Description: Receipt identifier.
  Example: null

• data.createdAt
  Type: string; Format: date-time; Required: Yes; Nullable: No
  Trigger: The transaction and account balance are committed.
  Description: Response-time timestamp generated with new Date(); it is not read from a persisted Transaction entity column.

• data.category_id
  Type: integer; Required: Yes; Nullable: Yes
  Trigger: The transaction and account balance are committed.
  Description: Stored optional category identifier.
  Example: 3

## Row 168

Column A:

Error Response — HTTP 400

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: Required input is missing/invalid; shopName or paymentMethod is empty/missing; a supplied category_id does not exist; accountId is not owned by the authenticated user; type/status is invalid; or an Expense exceeds the account balance.
  Description: Error description returned by the global HTTP exception filter.
  Example: Invalid or missing transaction data
  Note: Omitting category_id by itself is not an error because Transactions.category_id is nullable. The error envelope also contains success=false and may contain an error field.

## Row 169

Column A:

Error Response — HTTP 401

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The JWT is missing, invalid, or expired.
  Description: Error description returned by the global HTTP exception filter.
  Example: Unauthorized
  Note: The error envelope also contains success=false and may contain an error field.

## Row 170

Column A:

Error Response — HTTP 500

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The database transaction fails.
  Description: Error description returned by the global HTTP exception filter.
  Example: Error when creating transaction. Try it again later.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 171

Column A:

Notes

## Row 173

Column A:

API-CATEGORY-LIST — List Categories

## Row 174

Column A:

API ID

Column B:

API-CATEGORY-LIST

## Row 175

Column A:

API Name

Column B:

List Categories

## Row 176

Column A:

Related Use Case IDs

Column B:

UC-04; UC-11; UC-14

## Row 177

Column A:

Method

Column B:

GET

## Row 178

Column A:

Path

Column B:

/api/categories

## Row 179

Column A:

Description

Column B:

Return all available transaction and goal categories.

## Row 180

Column A:

Authentication

Column B:

Public

## Row 181

Column A:

Authorization

Column B:

None

## Row 182

Column A:

Business Rules / Validation Constraints

Column B:

BR-CAT-01 — Alphabetical category list: Categories shall be returned ordered by categoryName ascending.

## Row 183

Column A:

Request Body

Column B:

None

## Row 184

Column A:

Success Response — HTTP 200

Column B:

• success
  Type: boolean; Required: Yes; Nullable: No
  Trigger: Categories are retrieved.
  Description: Indicates successful retrieval.
  Example: true

• message
  Type: string; Required: Yes; Nullable: No
  Trigger: Categories are retrieved.
  Description: Human-readable success message.
  Example: Lấy danh sách danh mục thành công

• data
  Type: array<object>; Required: Yes; Nullable: No
  Trigger: Categories are retrieved.
  Description: Category array. May be empty.
  Example: []

• data[].category_id
  Type: integer; Required: Yes; Nullable: No
  Trigger: Categories are retrieved.
  Description: Category identifier.
  Example: 3

• data[].category_name
  Type: string; Required: Yes; Nullable: No
  Trigger: Categories are retrieved.
  Description: Category name.
  Example: Entertainment

## Row 185

Column A:

Error Response — HTTP 500

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: Category retrieval fails.
  Description: Error description returned by the global HTTP exception filter.
  Example: Đã xảy ra lỗi hệ thống khi lấy danh sách danh mục. Vui lòng thử lại sau.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 186

Column A:

Notes

## Row 188

Column A:

API-CATEGORY-DETAIL — Get Category Details

## Row 189

Column A:

API ID

Column B:

API-CATEGORY-DETAIL

## Row 190

Column A:

API Name

Column B:

Get Category Details

## Row 191

Column A:

Related Use Case IDs

## Row 192

Column A:

Method

Column B:

GET

## Row 193

Column A:

Path

Column B:

/api/categories/:id

## Row 194

Column A:

Description

Column B:

Return one category by identifier.

## Row 195

Column A:

Authentication

Column B:

Public

## Row 196

Column A:

Authorization

Column B:

None

## Row 197

Column A:

Business Rules / Validation Constraints

Column B:

BR-CAT-02 — Unique category name: Category.categoryName is declared unique in the database entity mapping.

## Row 198

Column A:

Path Parameter(s)

Column B:

• path.id
  Type: integer; Required: Yes; Nullable: No
  Validation: Must parse as an integer.
  Trigger: Category detail request.
  Description: Category identifier.
  Example: 3

## Row 199

Column A:

Request Body

Column B:

None

## Row 200

Column A:

Success Response — HTTP 200

Column B:

• success
  Type: boolean; Required: Yes; Nullable: No
  Trigger: The category exists.
  Description: Indicates successful retrieval.
  Example: true

• message
  Type: string; Required: Yes; Nullable: No
  Trigger: The category exists.
  Description: Human-readable success message.
  Example: Lấy chi tiết danh mục thành công

• data.category_id
  Type: integer; Required: Yes; Nullable: No
  Trigger: The category exists.
  Description: Category identifier.
  Example: 3

• data.category_name
  Type: string; Required: Yes; Nullable: No
  Trigger: The category exists.
  Description: Category name.
  Example: Entertainment

## Row 201

Column A:

Error Response — HTTP 400

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The path ID cannot be parsed as an integer.
  Description: Error description returned by the global HTTP exception filter.
  Example: Validation failed
  Note: The error envelope also contains success=false and may contain an error field.

## Row 202

Column A:

Error Response — HTTP 404

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The category does not exist.
  Description: Error description returned by the global HTTP exception filter.
  Example: Category không tồn tại
  Note: The error envelope also contains success=false and may contain an error field.

## Row 203

Column A:

Error Response — HTTP 500

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: Category retrieval fails.
  Description: Error description returned by the global HTTP exception filter.
  Example: Đã xảy ra lỗi hệ thống khi lấy chi tiết danh mục. Vui lòng thử lại sau.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 204

Column A:

Notes

## Row 206

Column A:

API-EXPENSE-SUMMARY — Get Monthly Expense Summary

## Row 207

Column A:

API ID

Column B:

API-EXPENSE-SUMMARY

## Row 208

Column A:

API Name

Column B:

Get Monthly Expense Summary

## Row 209

Column A:

Related Use Case IDs

Column B:

UC-10

## Row 210

Column A:

Method

Column B:

GET

## Row 211

Column A:

Path

Column B:

/api/v1/expenses/summary

## Row 212

Column A:

Description

Column B:

Return a monthly expense summary for visualization.

## Row 213

Column A:

Authentication

Column B:

Bearer JWT

## Row 214

Column A:

Authorization

Column B:

Authenticated user

## Row 215

Column A:

Request Header(s)

Column B:

• headers.Authorization
  Type: string; Format: Bearer <JWT>; Required: Yes; Nullable: No
  Validation: Must contain a valid, unexpired JWT access token.
  Trigger: Every protected request.
  Description: Authenticates the current user.
  Example: Bearer eyJhbGciOiJIUzI1NiIs...
  Note: Added by the frontend Axios interceptor.

## Row 216

Column A:

Request Body

Column B:

None

## Row 217

Column A:

Success Response — HTTP 200

Column B:

{
  "success": true,
  "message": string,
  "data": [
    {
      "month": string,
      "totalExpense": number
    }
  ]
}

• data
  Type: array<object>; Required: Yes; Nullable: No
  Description: Monthly expense summary data.
  Example: []

• data[].month
  Type: string; Required: Yes; Nullable: No
  Example: Aug

• data[].totalExpense
  Type: number; Required: Yes; Nullable: No
  Description: Expense amount represented for the returned month.
  Example: 160000

## Row 218

Column A:

Error Response — HTTP 401

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The JWT is missing, invalid, or expired.
  Description: Error description returned by the global HTTP exception filter.
  Example: Unauthorized
  Note: The error envelope also contains success=false and may contain an error field.

## Row 219

Column A:

Error Response — HTTP 500

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: Expense aggregation fails.
  Description: Error description returned by the global HTTP exception filter.
  Example: Cannot get expenses data.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 220

Column A:

Notes

Column B:

Experiment classification:
- BR-EXP-01 through BR-EXP-07 are the treatment-sensitive Business Rules used for the core Business Rule effectiveness score.
- The current-month color treatment is a Figma-derived UI requirement and is not a core Business Rule.
- Read-only behavior is redundantly constrained by the GET method.
- The successful response envelope is project-constrained by PROJECT_CONTEXT.md and AGENTS.md.

## Row 222

Column A:

API-EXPENSE-BREAKDOWN — Get Expense Breakdown by Category

## Row 223

Column A:

API ID

Column B:

API-EXPENSE-BREAKDOWN

## Row 224

Column A:

API Name

Column B:

Get Expense Breakdown by Category

## Row 225

Column A:

Related Use Case IDs

Column B:

UC-11

## Row 226

Column A:

Method

Column B:

GET

## Row 227

Column A:

Path

Column B:

/api/v1/expenses/breakdown

## Row 228

Column A:

Description

Column B:

Return the authenticated user's expense breakdown by category for a selected month.

## Row 229

Column A:

Authentication

Column B:

Bearer JWT

## Row 230

Column A:

Authorization

Column B:

Authenticated user

## Row 231

Column A:

Business Rules / Validation Constraints

Column B:

BR-EXP-CAT-01: Authenticated ownership scope
Only transactions associated with accounts owned by the authenticated user may contribute to the breakdown. The userId used for the operation must come from the validated JWT and must not be supplied or overridden by the client.

BR-EXP-CAT-02: Eligible selected-month expenses
Only transactions with type = Expense and transactionDate within the selected calendar month are eligible. Transaction status is not used as an eligibility condition.

BR-EXP-CAT-03: Category classification
Eligible transactions are grouped by categoryId. A null categoryId is classified as Uncategorized; an unresolved non-null categoryId is classified as Unknown; a resolved categoryId uses the corresponding Category.categoryName.

BR-EXP-CAT-04: Category totals and detail mapping
For each category group, total equals the sum of the eligible transaction amounts in that group. Each returned detail maps itemDescription, amount, and transactionDate to item_description, numeric amount, and an ISO YYYY-MM-DD date.

BR-EXP-CAT-05: Previous-month comparison
changePercent compares the current category total with the immediately preceding calendar month using ((currentTotal - previousTotal) / previousTotal) * 100. If previousTotal = 0, changePercent is 100 when currentTotal > 0 and null otherwise. January compares with December of the preceding year.

BR-EXP-CAT-06: Rounding and deterministic ordering
Each total and non-null changePercent is rounded to two decimal places. Category groups are ordered by total descending, and transaction details within each category are ordered by transaction date ascending.

BR-EXP-CAT-07: No-data outcome
If the authenticated user owns no accounts or no eligible Expense transaction exists for the selected month, the endpoint produces its configured no-data response and the frontend displays its no-data state.

Interface validation (not a core treatment-sensitive BR):
- query.month is required and must use YYYY-MM format.
- Missing or syntactically invalid month values return HTTP 400.
- A syntactically valid month whose MM portion is outside 01..12 follows the endpoint's configured invalid-month/no-data handling.

## Row 232

Column A:

Request Header(s)

Column B:

• headers.Authorization
  Type: string; Format: Bearer <JWT>; Required: Yes; Nullable: No
  Validation: Must contain a valid, unexpired JWT access token.
  Trigger: Every protected request.
  Description: Authenticates the current user.
  Example: Bearer eyJhbGciOiJIUzI1NiIs...
  Note: Added by the frontend Axios interceptor.

## Row 233

Column A:

Query Parameter(s)

Column B:

• query.month
  Type: string; Format: YYYY-MM; Required: Yes; Nullable: No
  Validation: Must match YYYY-MM and identify the selected month for the breakdown request.
  Trigger: Expense breakdown request.
  Description: Month selected by the user.
  Example: 2025-11

## Row 234

Column A:

Request Body

Column B:

None

## Row 235

Column A:

Success Response — HTTP 200

Column B:

• success
  Type: boolean; Required: Yes; Nullable: No
  Description: Indicates a successful request.
  Example: true

• message
  Type: string; Required: Yes; Nullable: No
  Description: Success message following the project-wide API response convention.
  Example: Expense breakdown retrieved successfully

• data
  Type: array<object>; Required: Yes; Nullable: No
  Description: Expense breakdown results for the selected month.
  Example: []

• data[].category
  Type: string; Required: Yes; Nullable: No
  Description: Category label for the group.
  Example: Entertainment

• data[].total
  Type: number; Required: Yes; Nullable: No
  Description: Total expense amount for the category group.
  Example: 1500000

• data[].changePercent
  Type: number; Required: Yes; Nullable: Yes
  Description: Percentage change compared with the previous month.
  Example: 25.5

• data[].subCategories
  Type: array<object>; Required: Yes; Nullable: No
  Description: Underlying transaction details for the category group.
  Example: []

• data[].subCategories[].item_description
  Type: string; Required: Yes; Nullable: No
  Description: Transaction description.
  Example: Movie Ticket

• data[].subCategories[].amount
  Type: number; Required: Yes; Nullable: No
  Description: Transaction amount.
  Example: 150000

• data[].subCategories[].date
  Type: string; Format: date; Required: Yes; Nullable: No
  Description: Transaction date.
  Example: 2025-11-01

## Row 236

Column A:

Error Response — HTTP 400

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: month is missing or does not satisfy the request format.
  Description: Error description returned by the global HTTP exception filter.
  Example: Tham số month không hợp lệ. Vui lòng sử dụng định dạng YYYY-MM (ví dụ: 2025-11)
  Note: The project error envelope also contains success=false and may contain an error field.

## Row 237

Column A:

Error Response — HTTP 401

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The JWT is missing, invalid, or expired.
  Description: Error description returned by the global HTTP exception filter.
  Example: Unauthorized
  Note: The error envelope also contains success=false and may contain an error field.

## Row 238

Column A:

Error Response — HTTP 404

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: No expense-breakdown data is available for the selected month under the applicable business rules, or the endpoint applies its configured invalid-month/no-data handling.
  Description: Error description returned by the global HTTP exception filter.
  Example: Không có dữ liệu chi tiêu cho tháng này.
  Note: The project error envelope also contains success=false and may contain an error field.

## Row 239

Column A:

Error Response — HTTP 500

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: Breakdown calculation fails.
  Description: Error description returned by the global HTTP exception filter.
  Example: Không thể lấy dữ liệu breakdown chi tiêu.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 240

Column A:

Notes

Column B:

Experiment classification:
- BR-EXP-CAT-01 through BR-EXP-CAT-07 are the treatment-sensitive Business Rules used for UC-11's core Business Rule effectiveness score.
- Month input syntax is part of the API interface contract and is not a core treatment-sensitive BR.
- Figma presentation requirements are UI evidence and are not part of the core Business Rule score.
- Read-only behavior is redundantly constrained by the GET method.
- The standard successful/error response envelope is project-constrained by the project-level API convention.

## Row 242

Column A:

API-BILL-LIST — List Upcoming Bills

## Row 243

Column A:

API ID

Column B:

API-BILL-LIST

## Row 244

Column A:

API Name

Column B:

List Upcoming Bills

## Row 245

Column A:

Related Use Case IDs

Column B:

UC-12

## Row 246

Column A:

Method

Column B:

GET

## Row 247

Column A:

Path

Column B:

/api/v1/bills

## Row 248

Column A:

Description

Column B:

Return bill data for the authenticated user's Upcoming Bills view.

## Row 249

Column A:

Authentication

Column B:

Bearer JWT

## Row 250

Column A:

Authorization

Column B:

Authenticated user

## Row 251

Column A:

Request Header(s)

Column B:

• headers.Authorization
  Type: string; Format: Bearer <JWT>; Required: Yes; Nullable: No
  Validation: Must contain a valid, unexpired JWT access token.
  Trigger: Every protected request.
  Description: Authenticates the current user.
  Example: Bearer eyJhbGciOiJIUzI1NiIs...
  Note: Added by the frontend Axios interceptor.

## Row 252

Column A:

Request Body

Column B:

None

## Row 253

Column A:

Success Response — HTTP 200

Column B:

• success
  Type: boolean; Required: Yes; Nullable: No
  Description: Indicates a successful request.
  Example: true

• message
  Type: string; Required: Yes; Nullable: No
  Description: Success message following the project-wide API response convention.
  Example: Bills retrieved successfully

• data
  Type: array<object>; Required: Yes; Nullable: No
  Description: Bill items returned for the Upcoming Bills view.
  Example: []

• data[].billId
  Type: integer; Required: Yes; Nullable: No
  Description: Bill identifier.
  Example: 7

• data[].userId
  Type: integer; Required: Yes; Nullable: No
  Description: Owner user identifier.
  Example: 1

• data[].itemDescription
  Type: string; Required: Yes; Nullable: No
  Description: Bill description.
  Example: Netflix

• data[].logoUrl
  Type: string; Required: Yes; Nullable: Yes
  Description: Optional bill logo URL.
  Example: https://example.com/netflix.png

• data[].dueDate
  Type: string; Format: date; Required: Yes; Nullable: No
  Description: Bill due date.
  Example: 2025-11-15

• data[].lastChargeDate
  Type: string; Format: date; Required: Yes; Nullable: Yes
  Description: Most recent charge date when available.
  Example: 2025-10-15

• data[].amount
  Type: number; Required: Yes; Nullable: No
  Description: Bill amount.
  Example: 260000

## Row 254

Column A:

Error Response — HTTP 401

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The JWT is missing, invalid, or expired.
  Description: Error description returned by the global HTTP exception filter.
  Example: Unauthorized
  Note: The error envelope also contains success=false and may contain an error field.

## Row 255

Column A:

Error Response — HTTP 500

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: Bill retrieval or response processing fails.
  Description: Error description returned by the global HTTP exception filter.
  Example: Failed to fetch bills
  Note: The project error envelope also contains success=false and may contain an error field.

## Row 256

Column A:

Notes

Column B:

Experiment classification:
- The API contract intentionally contains only interface structure, authentication requirements, response fields, and error contracts.
- UC-12 Business Rules are defined only in the Use cases sheet and are intentionally omitted from this API contract for ablation isolation.
- The project-standard successful/error response envelope remains authoritative at the API level.

## Row 258

Column A:

API-GOAL-LIST — List Financial Goals

## Row 259

Column A:

API ID

Column B:

API-GOAL-LIST

## Row 260

Column A:

API Name

Column B:

List Financial Goals

## Row 261

Column A:

Related Use Case IDs

Column B:

UC-13

## Row 262

Column A:

Method

Column B:

GET

## Row 263

Column A:

Path

Column B:

/api/v1/goals

## Row 264

Column A:

Description

Column B:

Return financial-goal data for the authenticated user's Goals view.

## Row 265

Column A:

Authentication

Column B:

Bearer JWT

## Row 266

Column A:

Authorization

Column B:

Authenticated user

## Row 267

Column A:

Request Header(s)

Column B:

• headers.Authorization
  Type: string; Format: Bearer <JWT>; Required: Yes; Nullable: No
  Validation: Must contain a valid, unexpired JWT access token.
  Trigger: Every protected request.
  Description: Authenticates the current user.
  Example: Bearer eyJhbGciOiJIUzI1NiIs...
  Note: Added by the frontend Axios interceptor.

## Row 268

Column A:

Request Body

Column B:

None

## Row 269

Column A:

Success Response — HTTP 200

Column B:

• success
  Type: boolean; Required: Yes; Nullable: No
  Description: Indicates a successful request.
  Example: true

• message
  Type: string; Required: Yes; Nullable: No
  Description: Success message following the project-wide API response convention.
  Example: Lấy danh sách mục tiêu thành công

• data.savingGoal
  Type: object; Required: Yes; Nullable: Yes
  Description: Saving-goal data when available.
  Example: null

• data.savingGoal.goal_id
  Type: integer; Required: Yes; Nullable: No
  Description: Saving goal identifier.
  Example: 2

• data.savingGoal.goal_type
  Type: string; Required: Yes; Nullable: No
  Allowed values: Saving
  Description: Saving goal type.
  Example: Saving

• data.savingGoal.target_amount
  Type: number; Required: Yes; Nullable: No
  Description: Saving target amount.
  Example: 10000000

• data.savingGoal.target_achieved
  Type: number; Required: Yes; Nullable: No
  Description: Calculated achieved amount for the saving goal.
  Example: 3500000

• data.savingGoal.start_date
  Type: string; Format: date; Required: Yes; Nullable: No
  Description: Saving goal start date.
  Example: 2025-11-01

• data.savingGoal.end_date
  Type: string; Format: date; Required: Yes; Nullable: No
  Description: Saving goal end date.
  Example: 2025-11-30

• data.expenseGoals
  Type: array<object>; Required: Yes; Nullable: No
  Description: Expense-goal items returned for the Goals view.
  Example: []

• data.expenseGoals[].goal_id
  Type: integer; Required: Yes; Nullable: No
  Description: Expense goal identifier.
  Example: 5

• data.expenseGoals[].category
  Type: string; Required: Yes; Nullable: No
  Description: Category label for the expense goal.
  Example: Food

• data.expenseGoals[].target_amount
  Type: number; Required: Yes; Nullable: No
  Description: Expense-goal target amount.
  Example: 3000000

• data.expenseGoals[].current_expense
  Type: number; Required: Yes; Nullable: No
  Description: Calculated expense amount for the expense goal.
  Example: 1200000

## Row 270

Column A:

Error Response — HTTP 401

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The JWT is missing, invalid, or expired.
  Description: Error description returned by the global HTTP exception filter.
  Example: Unauthorized
  Note: The error envelope also contains success=false and may contain an error field.

## Row 271

Column A:

Error Response — HTTP 500

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: Goal retrieval or response processing fails.
  Description: Error description returned by the global HTTP exception filter.
  Example: Đã xảy ra lỗi hệ thống khi tải mục tiêu, vui lòng thử lại sau.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 272

Column A:

Notes

Column B:

Experiment classification:
- The API contract intentionally contains only interface structure, authentication requirements, response fields, and error contracts.
- UC-13 Business Rules are defined only in the Use cases sheet and are intentionally omitted from this API contract for ablation isolation.
- The project-standard successful/error response envelope remains authoritative at the API level.
- Response-field descriptions intentionally avoid restating calculation, selection, filtering, fallback, and ordering semantics defined by UC-13 Business Rules.

## Row 274

Column A:

API-GOAL-CREATE — Create Financial Goal

## Row 275

Column A:

API ID

Column B:

API-GOAL-CREATE

## Row 276

Column A:

API Name

Column B:

Create Financial Goal

## Row 277

Column A:

Related Use Case IDs

Column B:

UC-14

## Row 278

Column A:

Method

Column B:

POST

## Row 279

Column A:

Path

Column B:

/api/v1/goals

## Row 280

Column A:

Description

Column B:

Create financial-goal data for the authenticated user's Goals workflow.

## Row 281

Column A:

Authentication

Column B:

Bearer JWT

## Row 282

Column A:

Authorization

Column B:

Authenticated user

## Row 283

Column A:

Request Header(s)

Column B:

• headers.Authorization
  Type: string; Format: Bearer <JWT>; Required: Yes; Nullable: No
  Validation: Must contain a valid, unexpired JWT access token.
  Trigger: Every protected request.
  Description: Authenticates the current user.
  Example: Bearer eyJhbGciOiJIUzI1NiIs...
  Note: Added by the frontend Axios interceptor.

• headers.Content-Type
  Type: string; Format: MIME type; Required: Yes; Nullable: No
  Default: application/json
  Allowed values: application/json
  Validation: Request body must be JSON.
  Trigger: Every request containing a JSON body.
  Description: Declares the request body format.
  Example: application/json

## Row 284

Column A:

Request Body

Column B:

• goal_type
  Type: string; Required: Yes; Nullable: No
  Allowed values: Saving; Expense_Limit
  Description: Goal type supplied by the client.
  Example: Saving

• category_id
  Type: integer; Required: No; Nullable: Yes
  Description: Optional category identifier supplied with the goal request.
  Example: 3

• start_date
  Type: string; Format: YYYY-MM-DD; Required: Yes; Nullable: No
  Description: Goal start date supplied by the client.
  Example: 2025-11-01

• end_date
  Type: string; Format: YYYY-MM-DD; Required: Yes; Nullable: No
  Description: Goal end date supplied by the client.
  Example: 2025-11-30

• target_amount
  Type: number; Format: decimal; Required: Yes; Nullable: No
  Description: Goal target amount supplied by the client.
  Example: 10000000

## Row 285

Column A:

Success Response — HTTP 201

Column B:

• message
  Type: string; Required: Yes; Nullable: No
  Description: Creation success message.
  Example: Goal created successfully

• goal_id
  Type: integer; Required: Yes; Nullable: No
  Description: Identifier returned for the created goal.
  Example: 5

## Row 286

Column A:

Error Response — HTTP 400

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The submitted request is rejected as invalid under the applicable validation or business rules.
  Description: Error description returned by the global HTTP exception filter.
  Example: Invalid goal data.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 287

Column A:

Error Response — HTTP 401

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The JWT is missing, invalid, or expired.
  Description: Error description returned by the global HTTP exception filter.
  Example: Unauthorized
  Note: The error envelope also contains success=false and may contain an error field.

## Row 288

Column A:

Error Response — HTTP 500

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: Goal creation cannot be completed because of an unexpected server, repository, or database failure.
  Description: Error description returned by the global HTTP exception filter.
  Example: Không thể tạo mục tiêu lúc này. Vui lòng thử lại sau.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 289

Column A:

Notes

Column B:

Experiment classification:
- The API contract intentionally contains only endpoint structure, authentication requirements, request/response field shapes, and generic error contracts.
- UC-14 Business Rules are defined only in the Use cases sheet and are intentionally omitted from this API contract for ablation isolation.
- Request-field descriptions intentionally avoid restating category dependency, monetary precision, date-boundary, overlap-conflict, persistence, and atomicity semantics.
- The project-standard success/error response convention remains authoritative at the API level.

## Row 291

Column A:

API-GOAL-UPDATE — Update Financial Goal

## Row 292

Column A:

API ID

Column B:

API-GOAL-UPDATE

## Row 293

Column A:

API Name

Column B:

Update Financial Goal

## Row 294

Column A:

Related Use Case IDs

Column B:

UC-15

## Row 295

Column A:

Method

Column B:

PUT

## Row 296

Column A:

Path

Column B:

/api/v1/goals/:goalId

## Row 297

Column A:

Description

Column B:

Update the target amount of a goal owned by the authenticated user.

## Row 298

Column A:

Authentication

Column B:

Bearer JWT

## Row 299

Column A:

Authorization

Column B:

Goal owner

## Row 300

Column A:

Request Header(s)

Column B:

• headers.Authorization
  Type: string; Format: Bearer <JWT>; Required: Yes; Nullable: No
  Validation: Must contain a valid, unexpired JWT access token.
  Trigger: Every protected request.
  Description: Authenticates the current user.
  Example: Bearer eyJhbGciOiJIUzI1NiIs...
  Note: Added by the frontend Axios interceptor.

• headers.Content-Type
  Type: string; Format: MIME type; Required: Yes; Nullable: No
  Default: application/json
  Allowed values: application/json
  Validation: Request body must be JSON.
  Trigger: Every request containing a JSON body.
  Description: Declares the request body format.
  Example: application/json

## Row 301

Column A:

Path Parameter(s)

Column B:

• path.goalId
  Type: integer; Required: Yes; Nullable: No
  Validation: The controller applies parseInt(goalId, 10) and does not explicitly reject NaN before calling the service.
  Trigger: Every goal update request.
  Description: Goal identifier as parsed by the controller.
  Example: 5

## Row 302

Column A:

Request Body

Column B:

• target_amount
  Type: number; Format: decimal; Required: Yes; Nullable: No
  Validation: Must be greater than 0.
  Trigger: Goal update request.
  Description: New target amount.
  Example: 12000000

## Row 303

Column A:

Success Response — HTTP 200

Column B:

• message
  Type: string; Required: Yes; Nullable: No
  Trigger: The goal is updated.
  Description: Update success message.
  Example: Goal updated successfully

• updated_goal.goal_id
  Type: integer; Required: Yes; Nullable: No
  Trigger: The goal is updated.
  Description: Updated goal identifier.
  Example: 5

• updated_goal.target_amount
  Type: number; Required: Yes; Nullable: No
  Trigger: The goal is updated.
  Description: Updated target amount.
  Example: 12000000

## Row 304

Column A:

Error Response — HTTP 400

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: target_amount fails UpdateGoalDto validation.
  Description: Validation errors for the request body.
  Example: ["target_amount must be a positive number"]
  Note: The error envelope also contains success=false and may contain an error field.

## Row 305

Column A:

Error Response — HTTP 401

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The JWT is missing, invalid, or expired.
  Description: Error description returned by the global HTTP exception filter.
  Example: Unauthorized
  Note: The error envelope also contains success=false and may contain an error field.

## Row 306

Column A:

Error Response — HTTP 403

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The goal belongs to another user.
  Description: Error description returned by the global HTTP exception filter.
  Example: Bạn không có quyền chỉnh sửa mục tiêu này.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 307

Column A:

Error Response — HTTP 404

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The goal does not exist.
  Description: Error description returned by the global HTTP exception filter.
  Example: Mục tiêu không tồn tại.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 308

Column A:

Error Response — HTTP 500

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The goal update cannot be saved.
  Description: Error description returned by the global HTTP exception filter.
  Example: Không thể lưu thay đổi lúc này. Vui lòng thử lại sau.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 309

Column A:

Notes

## Row 311

Column A:

API-SAVINGS-SUMMARY - Get Savings Summary

## Row 312

Column A:

API ID

Column B:

API-SAVINGS-SUMMARY

## Row 313

Column A:

API Name

Column B:

Get Savings Summary

## Row 314

Column A:

Related Use Case IDs

Column B:

UC-16

## Row 315

Column A:

Method

Column B:

GET

## Row 316

Column A:

Path

Column B:

/api/v1/savings/summary

## Row 317

Column A:

Description

Column B:

Return monthly net savings for a selected year and the preceding year.

## Row 318

Column A:

Authentication

Column B:

Bearer JWT

## Row 319

Column A:

Authorization

Column B:

Authenticated user

## Row 320

Column A:

Business Rules / Validation Constraints

Column B:

BR-SAV-01: Authenticated User Data Scope
The savings summary shall be calculated only from transactions belonging to accounts owned by the authenticated user. The user identity shall be obtained from the validated JWT and not from client-supplied data.

BR-SAV-02: Savings Summary Year Resolution
The requested year shall be parsed as an integer. If the year is missing, cannot be parsed, is less than 1900, or is greater than 2100, the current year shall be used. Because the current implementation uses JavaScript parseInt, a value beginning with a valid numeric prefix, such as 2025abc, is resolved as 2025.

BR-SAV-03: Complete Monthly Summary
The response shall contain exactly 12 monthly entries for the resolved year and exactly 12 monthly entries for the preceding year. Months shall represent January through December in ascending order using two-digit values from 01 to 12.

BR-SAV-04: Monthly Net Savings Calculation
For each month, the savings amount shall equal the total Revenue minus the total Expense for that month across all accounts owned by the authenticated user.

BR-SAV-05: Previous-Year Comparison
The this_year series shall represent the resolved requested year, while the last_year series shall represent exactly the preceding year, calculated as resolvedYear - 1.

BR-SAV-06: Missing Transaction Data
If the authenticated user has no accounts, or if a month contains no matching transactions, the savings amount for that month shall be 0. Missing data shall not cause monthly entries to be omitted.

BR-SAV-07: Savings Amount Rounding
Each calculated monthly savings amount shall be rounded to two decimal places before being included in the API response.

BR-SAV-08: Savings Summary Response and Failure Handling
A successful response shall contain the authenticated user_id, the resolved year, and both 12-month savings series. If the savings calculation fails unexpectedly, the backend shall return HTTP 500. Retrieving the savings summary shall not create, update, or delete Account or Transaction records.

BR-SAV-09: Savings Chart Point Value Tooltip
When the savings chart is displayed, hovering the pointer over a data point in either the selected-year or previous-year series shall display a tooltip showing the savings amount represented by that point. The displayed value shall correspond exactly to the monthly savings amount returned for that month and series. The tooltip shall disappear when the pointer is no longer hovering over the data point.

## Row 321

Column A:

Request Header(s)

Column B:

• headers.Authorization
  Type: string; Format: Bearer <JWT>; Required: Yes; Nullable: No
  Validation: Must contain a valid, unexpired JWT access token.
  Trigger: Every protected request.
  Description: Authenticates the current user.
  Example: Bearer eyJhbGciOiJIUzI1NiIs...
  Note: Added by the frontend Axios interceptor.

## Row 322

Column A:

Query Parameter(s)

Column B:

• query.year
  Type: integer; Format: YYYY; Required: No; Nullable: No
  Default: Current year
  Validation: The controller applies parseInt(year, 10). Missing, NaN, <1900, or >2100 values use the current year. A leading numeric prefix is accepted by parseInt.
  Trigger: Savings summary request.
  Description: Optional target year resolved by the controller.
  Example: 2025

## Row 323

Column A:

Request Body

Column B:

None

## Row 324

Column A:

Success Response — HTTP 200

Column B:

• user_id
  Type: integer; Required: Yes; Nullable: No
  Trigger: The summary is calculated; missing data produces zero-valued months.
  Description: Authenticated user identifier.
  Example: 1

• year
  Type: integer; Required: Yes; Nullable: No
  Trigger: The summary is calculated; missing data produces zero-valued months.
  Description: Resolved target year.
  Example: 2025

• summary.this_year
  Type: array<object>; Required: Yes; Nullable: No
  Trigger: The summary is calculated; missing data produces zero-valued months.
  Description: Twelve monthly savings values for the selected year.
  Example: []

• summary.this_year[].month
  Type: string; Required: Yes; Nullable: No
  Trigger: The summary is calculated; missing data produces zero-valued months.
  Description: Two-digit month number.
  Example: 01

• summary.this_year[].amount
  Type: number; Required: Yes; Nullable: No
  Trigger: The summary is calculated; missing data produces zero-valued months.
  Description: Revenue minus expense for the month.
  Example: 1500000

• summary.last_year
  Type: array<object>; Required: Yes; Nullable: No
  Trigger: The summary is calculated; missing data produces zero-valued months.
  Description: Twelve monthly savings values for the previous year.
  Example: []

• summary.last_year[].month
  Type: string; Required: Yes; Nullable: No
  Trigger: The summary is calculated; missing data produces zero-valued months.
  Description: Two-digit month number.
  Example: 01

• summary.last_year[].amount
  Type: number; Required: Yes; Nullable: No
  Trigger: The summary is calculated; missing data produces zero-valued months.
  Description: Revenue minus expense for the month.
  Example: 1200000

## Row 325

Column A:

Error Response — HTTP 401

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: The JWT is missing, invalid, or expired.
  Description: Error description returned by the global HTTP exception filter.
  Example: Không thể xác thực người dùng. Vui lòng đăng nhập lại.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 326

Column A:

Error Response — HTTP 500

Column B:

• message
  Type: string | string[]; Required: Yes; Nullable: No
  Trigger: Savings calculation fails.
  Description: Error description returned by the global HTTP exception filter.
  Example: An internal server error occurred while processing the savings summary.
  Note: The error envelope also contains success=false and may contain an error field.

## Row 327

Column A:

Notes


