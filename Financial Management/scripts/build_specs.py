"""Build the package from preserved source and reviewed, explicit domain rules."""
from pathlib import Path
import json, re, hashlib

ROOT = Path(__file__).resolve().parents[1]
URL = 'https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit'
def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.rstrip() + '\n', encoding='utf-8')

# Declarations are emitted inside each individual use case, with dependency closure.
# This script is an authoring tool, not an external UML vocabulary for any rule.
CLASSES = {}
def model(name, fields='', operations='', kind='class'):
    CLASSES[name] = (kind, [s.strip() for s in fields.split(';') if s.strip()],
                     [s.strip() for s in operations.split(';') if s.strip()])
model('RequestContext', 'userId: Integer; authenticated: Boolean; today: CalendarDate; now: String')
model('CalendarDate', 'year: Integer; month: Integer; ordinal: Integer',
      '{static} parse(text: String): CalendarDate; {static} monthStart(date: CalendarDate): CalendarDate; {static} monthEnd(date: CalendarDate): CalendarDate; {static} previousMonth(date: CalendarDate): CalendarDate')
model('Text', operations='{static} trim(s: String): String; {static} nfc(s: String): String; {static} lower(s: String): String; {static} matches(s: String, pattern: String): Boolean; {static} email(s: String): Boolean; {static} last4(s: String): String; {static} username(email: String, taken: Set(String)): String')
model('Numeric', operations='{static} round2(x: Real): Real; {static} finite(x: Real): Boolean; {static} scale(x: Real): Integer')
model('PasswordHasher', operations='{static} matches(password: String, hash: String): Boolean; {static} cost(hash: String): Integer')
model('User', 'id: Integer; fullName: String; email: String; username: String; passwordHash: String; version: Integer')
model('PublicUser', 'id: Integer; fullName: String; email: String')
model('AuthCommand', 'fullName: String; email: String; password: String; confirmPassword: String')
model('AuthResult', 'success: Boolean; evaluated: Boolean; user: PublicUser [0..1]; accessToken: String [0..1]; secretFields: Set(String); loggedFields: Set(String)')
model('ClientSession','accessToken: String [0..1]; user: PublicUser [0..1]; storage: String; durableFields: Set(String)')
model('AuthClient',operations='establish(response: AuthResult): ClientSession')
model('AccountType', 'Checking; Credit_Card; Savings; Investment; Loan', kind='enum')
model('TransactionType', 'Revenue; Expense', kind='enum')
model('TransactionFilter', 'All; Revenue; Expense', kind='enum')
model('TransactionStatus', 'Complete; Pending; Failed', kind='enum')
model('GoalType', 'Saving; Expense_Limit', kind='enum')
model('Account', 'id: Integer; userId: Integer; bankName: String; accountType: AccountType; branchName: String [0..1]; numberCiphertext: String; numberFingerprint: String; last4: String; balance: Real; version: Integer; createdAt: String')
model('AccountView', 'id: Integer; userId: Integer; bankName: String; accountType: AccountType; branchName: String [0..1]; fullNumber: String [0..1]; last4: String; displayNumber: String; balance: Real; version: Integer')
model('AccountCommand', 'accountId: Integer; bankName: String; accountType: AccountType; branchName: String [0..1]; fullNumber: String; balance: Real; expectedVersion: Integer')
model('AccountResult', 'success: Boolean; account: AccountView [0..1]')
model('AccountListResult', 'success: Boolean; userId: Integer; accounts: Sequence(AccountView)')
model('AccountDetailResult', 'success: Boolean; account: AccountView [0..1]; recent: Sequence(RecentTransaction)')
model('RecentTransaction', 'id: Integer; date: CalendarDate; amount: Real; description: String; status: TransactionStatus; receiptId: String [0..1]; type: TransactionType')
model('AccountVault', operations='{static} fingerprint(number: String): String; {static} encrypt(number: String): String; {static} decrypt(ciphertext: String): String')
model('BalanceAdjustment', 'id: Integer; accountId: Integer; userId: Integer; oldBalance: Real; newBalance: Real; accountVersion: Integer; createdAt: String')
model('DeleteResult', 'success: Boolean; accountId: Integer')
model('Category', 'id: Integer; name: String')
model('Transaction', 'id: Integer; accountId: Integer; categoryId: Integer [0..1]; date: CalendarDate; type: TransactionType; status: TransactionStatus; description: String; shopName: String; paymentMethod: String; amount: Real; receiptId: String [0..1]; createdAt: String')
model('TransactionCommand', 'accountId: Integer; categoryId: Integer [0..1]; date: CalendarDate; type: TransactionType; status: TransactionStatus; description: String; shopName: String; paymentMethod: String; amount: Real; expectedVersion: Integer')
model('TransactionResult', 'success: Boolean; transaction: Transaction [0..1]')
model('TransactionQuery', 'type: TransactionFilter; limit: Integer; offset: Integer')
model('TransactionListResult', 'success: Boolean; data: Sequence(Transaction); total: Integer; hasMore: Boolean')
model('ExpenseMonth', 'month: Integer; totalExpense: Real')
model('ExpenseSummaryResult', 'success: Boolean; year: Integer; months: Sequence(ExpenseMonth)')
model('ExpenseGroup', 'categoryId: Integer [0..1]; category: String; total: Real; changePercent: Real [0..1]; details: Sequence(Transaction)')
model('BreakdownResult', 'success: Boolean; groups: Sequence(ExpenseGroup)')
model('Bill', 'id: Integer; userId: Integer; description: String; logoUrl: String [0..1]; dueDate: CalendarDate; lastChargeDate: CalendarDate [0..1]; amount: Real')
model('BillResult', 'success: Boolean; bills: Sequence(Bill)')
model('Goal', 'id: Integer; userId: Integer; goalType: GoalType; categoryId: Integer [0..1]; startDate: CalendarDate; endDate: CalendarDate; targetAmount: Real; version: Integer')
model('GoalCommand', 'goalId: Integer; goalType: GoalType; categoryId: Integer [0..1]; startDate: CalendarDate; endDate: CalendarDate; targetAmount: Real; expectedVersion: Integer')
model('GoalView', 'id: Integer; goalType: GoalType; categoryId: Integer [0..1]; category: String [0..1]; startDate: CalendarDate; endDate: CalendarDate; targetAmount: Real; progress: Real; version: Integer')
model('GoalResult', 'success: Boolean; goal: Goal [0..1]')
model('GoalListResult', 'success: Boolean; savingGoal: GoalView [0..1]; expenseGoals: Sequence(GoalView)')
model('SavingsMonth', 'month: Integer; amount: Real')
model('SavingsResult', 'success: Boolean; userId: Integer; year: Integer; thisYear: Sequence(SavingsMonth); lastYear: Sequence(SavingsMonth)')
model('CategoryResult', 'success: Boolean; categories: Sequence(Category); selected: Category [0..1]')

UCS = []
def uc(number, name, row_range, apis, service, operation, result, command=None, goal='', actions=None, alternative=None):
    u = dict(number=number, name=name, rows=row_range, apis=apis.split(), service=service,
             operation=operation, result=result, command=command, goal=goal, actions=actions,
             alternative=alternative, rules=[])
    UCS.append(u)
    return u
def rule(u, name, expression, kind='post', source='Product source', classifier=None, comment=''):
    u['rules'].append(dict(name=name, expression=expression, kind=kind, source=source,
                           classifier=classifier, comment=comment))
def auth(u):
    rule(u, 'AuthenticatedContext', 'ctx.authenticated and User.allInstances()->exists(u | u.id = ctx.userId)', 'pre')
def unchanged(u, entity):
    rule(u, entity+'Unchanged', f'{entity}.allInstances() = {entity}.allInstances()@pre', source='Product source',
         comment='Equality denotes the complete persistent value snapshot, including every property, not object identity alone.')
def money(u, value='cmd.amount', name='ExactAmount'):
    rule(u, name, f'Numeric::finite({value}) and {value} > 0 and Numeric::scale({value}) <= 2 and {value} < 10000000000000000',
         'pre', 'Assumption', comment='Exact decimal arithmetic; upper bound matches DECIMAL(18,2). Source positivity and precision are retained.')

u=uc(1,'Register an Account',(5,24),'API-AUTH-REGISTER','AuthService','register','AuthResult','AuthCommand',
     goal='Create an application identity and enter the signed-in application.',
     actions=['The visitor opens the registration page.','The client displays the registration form.','The visitor enters a full name, email, password, and password confirmation.','The visitor submits the form.','The client sends the registration request.','The system returns the account and session result.','The client opens the home page.'],
     alternative=['The visitor returns to the login link.','The client opens the login page.'])
rule(u,'Name', "let n : String = Text::trim(Text::nfc(cmd.fullName)) in n.size() >= 4 and n.size() <= 25 and Text::matches(n, '^[\\p{L}]+(?: [\\p{L}]+)*$')",'pre')
rule(u,'Email', 'Text::email(Text::lower(Text::trim(cmd.email))) and Text::trim(cmd.email).size() <= 255','pre')
rule(u,'UniqueEmail','User.allInstances()->isUnique(email)','inv',classifier='User')
rule(u,'Username','User.allInstances()->isUnique(username)','inv',classifier='User')
rule(u,'Password', "cmd.password.size() >= 8 and cmd.password.size() <= 64 and Text::matches(cmd.password, '^[A-Za-z0-9!@#$%^&*(){}_+=\\[\\],./<>?\\\\|:;\\-]+$') and Text::matches(cmd.password, '.*[a-z].*') and Text::matches(cmd.password, '.*[A-Z].*') and Text::matches(cmd.password, '.*[0-9].*') and Text::matches(cmd.password, '.*[^A-Za-z0-9].*')",'pre')
rule(u,'Confirmation','cmd.confirmPassword = cmd.password','pre')
rule(u,'CreatedIdentity','result.success implies User.allInstances()->one(u | u.id = result.user.id and u.email = Text::lower(Text::trim(cmd.email)) and u.fullName = Text::trim(Text::nfc(cmd.fullName)))')
rule(u,'PasswordStorage','result.success implies User.allInstances()->exists(u | u.id = result.user.id and PasswordHasher::matches(cmd.password, u.passwordHash) and PasswordHasher::cost(u.passwordHash) = 10)')
rule(u,'NoSecrets',"result.secretFields->intersection(Set{'password','passwordHash','confirmPassword'})->isEmpty() and result.loggedFields->intersection(Set{'password','passwordHash','confirmPassword','accessToken'})->isEmpty()")
rule(u,'Session','result.success implies not result.accessToken.oclIsUndefined() and result.accessToken.size() > 0')
rule(u,'AtomicFailure','not result.success implies User.allInstances() = User.allInstances()@pre and result.accessToken.oclIsUndefined()')
rule(u,'GeneratedUsername','result.success implies User.allInstances()->any(u | u.id = result.user.id).username = Text::username(Text::lower(Text::trim(cmd.email)), User.allInstances()@pre->collect(u | u.username@pre)->asSet())',comment='username uses the normalized email prefix, then the first free positive integer suffix on collision. Creation relies on database username/email uniqueness and retries a username collision within the operation.')
rule(u,'ExactlyOneUser','result.success implies User.allInstances()->size() = User.allInstances()@pre->size() + 1')
rule(u,'MemorySession',"response.success implies result.accessToken = response.accessToken and result.user = response.user and result.storage = 'Memory' and result.durableFields->intersection(Set{'accessToken','password','passwordHash','confirmPassword'})->isEmpty()",source='Assumption',classifier='AuthClient::establish(response: AuthResult): ClientSession')

u=uc(2,'Log In',(26,43),'API-AUTH-LOGIN','AuthService','login','AuthResult','AuthCommand',goal='Enter the application with an existing identity.',
     actions=['The visitor opens the login page.','The client displays the login form.','The visitor enters email and password.','The visitor submits the form.','The client sends the login request.','The system returns the session result.','The client opens the home page.'],
     alternative=['The visitor selects Create an account.','The client opens the registration page.'])
rule(u,'Email','Text::email(Text::lower(Text::trim(cmd.email)))','pre')
rule(u,'PasswordPresent','cmd.password.size() > 0','pre')
rule(u,'Credentials','result.evaluated implies result.success = User.allInstances()->exists(u | u.email = Text::lower(Text::trim(cmd.email)) and PasswordHasher::matches(cmd.password, u.passwordHash))',comment='evaluated distinguishes a completed credential evaluation from infrastructure failure; it is internal and not a wire field.')
rule(u,'CorrectIdentity','result.success implies User.allInstances()->exists(u | u.id = result.user.id and u.email = Text::lower(Text::trim(cmd.email)) and u.email = result.user.email and u.fullName = result.user.fullName)')
rule(u,'SessionIssued','result.success implies not result.accessToken.oclIsUndefined() and result.accessToken.size() > 0')
rule(u,'FailureSession','not result.success implies result.accessToken.oclIsUndefined() and result.user.oclIsUndefined()')
rule(u,'NoSecrets',"result.secretFields->intersection(Set{'password','passwordHash'})->isEmpty() and result.loggedFields->intersection(Set{'password','passwordHash','accessToken'})->isEmpty()")
unchanged(u,'User')
rule(u,'MemorySession',"response.success implies result.accessToken = response.accessToken and result.user = response.user and result.storage = 'Memory' and result.durableFields->intersection(Set{'accessToken','password','passwordHash'})->isEmpty()",source='Assumption',classifier='AuthClient::establish(response: AuthResult): ClientSession')

def owned_tx(expr='t', owner='ctx.userId'):
    return f'Account.allInstances()->exists(a | a.id = {expr}.accountId and a.userId = {owner})'
def matches_filter():
    return "(cmd.type = TransactionFilter::All or (cmd.type = TransactionFilter::Revenue and t.type = TransactionType::Revenue) or (cmd.type = TransactionFilter::Expense and t.type = TransactionType::Expense))"
def transaction_list_rules(u):
    auth(u)
    rule(u,'PageBounds','cmd.limit > 0 and cmd.limit <= 100 and cmd.offset >= 0','pre','Assumption')
    eligible=f'Transaction.allInstances()->select(t | {owned_tx()} and {matches_filter()})'
    rule(u,'ScopedPage',f'result.success implies result.data->forAll(t | {owned_tx()} and {matches_filter()})')
    rule(u,'ExactTotal',f'result.success implies result.total = {eligible}->size()')
    rule(u,'OrderedPage','result.data->size() <= 1 or Sequence{1..result.data->size()-1}->forAll(i | result.data->at(i).date.ordinal > result.data->at(i+1).date.ordinal or (result.data->at(i).date.ordinal = result.data->at(i+1).date.ordinal and result.data->at(i).id > result.data->at(i+1).id))',source='Assumption')
    rank='eligible->select(other | other.date.ordinal > t.date.ordinal or (other.date.ordinal = t.date.ordinal and other.id > t.id))->size()'
    rule(u,'ExactPage',f'result.success implies let eligible : Set(Transaction) = {eligible}->asSet() in result.data->collect(id)->asSet() = eligible->select(t | {rank} >= cmd.offset and {rank} < cmd.offset + cmd.limit)->collect(id)->asSet()',source='Assumption')
    rule(u,'HasMore','result.success implies result.hasMore = (cmd.offset + result.data->size() < result.total)')
    rule(u,'NoDuplicates','result.data->isUnique(id)')
    unchanged(u,'Transaction')
    unchanged(u,'Account')

u=uc(3,'View Transaction History',(45,62),'API-TRANSACTION-LIST','TransactionService','list','TransactionListResult','TransactionQuery',goal='Review the recorded transactions and open additional pages.',
     actions=['The user opens the Transactions page.','The client requests transaction history.','The system returns the transaction page.','The client displays transaction rows and page controls.','The user opens another page.','The client requests and displays the returned page.'],
     alternative=['The system returns an empty page.','The client displays the empty-history state.'])
transaction_list_rules(u)

u=uc(4,'Create a Transaction',(64,81),'API-TRANSACTION-CREATE API-ACCOUNT-LIST API-CATEGORY-LIST','TransactionService','create','TransactionResult','TransactionCommand',goal='Record income or an expense against a financial account.',
     actions=['The user opens the Add Transaction form.','The client requests accounts and categories.','The system returns the form choices.','The user enters transaction details and submits the form.','The client sends the transaction request.','The system returns the creation result.','The client displays confirmation and opens transaction history.'],
     alternative=['The user leaves the category selection empty.','The client submits the form and displays the returned result.'])
auth(u)
rule(u,'OwnedAccount',f'Account.allInstances()->exists(a | a.id = cmd.accountId and a.userId = ctx.userId)','pre')
money(u)
rule(u,'CompletedDate','cmd.status = TransactionStatus::Complete implies cmd.date.ordinal <= ctx.today.ordinal','pre','Assumption',comment='A future dated entry may be Pending/Failed; a realized cash flow cannot be future dated in this manually tracked ledger.')
rule(u,'Text',"Text::trim(cmd.description).size() > 0 and Text::trim(cmd.shopName).size() > 0 and Text::trim(cmd.paymentMethod).size() > 0 and Text::trim(cmd.description).size() <= 255 and Text::trim(cmd.shopName).size() <= 255 and Text::trim(cmd.paymentMethod).size() <= 100",'pre','Assumption')
rule(u,'Category','cmd.categoryId.oclIsUndefined() or Category.allInstances()->exists(c | c.id = cmd.categoryId)','pre')
rule(u,'CurrentVersion','Account.allInstances()->exists(a | a.id = cmd.accountId and a.version = cmd.expectedVersion)','pre','Assumption')
rule(u,'Funds','(cmd.type = TransactionType::Expense and cmd.status = TransactionStatus::Complete) implies Account.allInstances()->exists(a | a.id = cmd.accountId and a.balance >= cmd.amount)','pre','Assumption')
rule(u,'RevenueBalanceRange','(cmd.type = TransactionType::Revenue and cmd.status = TransactionStatus::Complete) implies Account.allInstances()->exists(a | a.id = cmd.accountId and a.balance + cmd.amount < 10000000000000000)','pre','Assumption',comment='Check the resulting balance before database conversion, preventing DECIMAL(18,2) overflow.')
rule(u,'BalanceEffect','result.success implies Account.allInstances()->exists(a | a.id = cmd.accountId and a.version = a.version@pre + 1 and a.balance = a.balance@pre + (if cmd.status <> TransactionStatus::Complete then 0 else if cmd.type = TransactionType::Revenue then cmd.amount else -cmd.amount endif endif))',source='Assumption')
rule(u,'ExactPersistence','result.success implies Transaction.allInstances()->one(t | t.id = result.transaction.id and t.accountId = cmd.accountId and t.categoryId = cmd.categoryId and t.date = cmd.date and t.type = cmd.type and t.status = cmd.status and t.description = Text::trim(cmd.description) and t.shopName = Text::trim(cmd.shopName) and t.paymentMethod = Text::trim(cmd.paymentMethod) and t.amount = cmd.amount and t.createdAt = ctx.now and t.receiptId.oclIsUndefined())',source='Assumption')
rule(u,'AtomicFailure','not result.success implies Transaction.allInstances() = Transaction.allInstances()@pre and Account.allInstances() = Account.allInstances()@pre',comment='Insertion and account version/balance write commit together; version comparison and expense balance check occur within the locked account transaction.')
rule(u,'ExactlyOne','result.success implies Transaction.allInstances()->size() = Transaction.allInstances()@pre->size() + 1')

u=uc(5,'View Bank Accounts',(83,104),'API-ACCOUNT-LIST','AccountService','list','AccountListResult',goal='Review financial account cards.',
     actions=['The user opens the Accounts page.','The client requests accounts.','The system returns account cards.','The client displays account names, types, number labels, and balances.'],
     alternative=['The system returns an empty account list.','The client displays the add-account entry point.'])
auth(u)
rule(u,'UserIdentity','result.success implies result.userId = ctx.userId')
rule(u,'ExactCoverage','result.success implies result.accounts->collect(id)->asSet() = Account.allInstances()->select(a | a.userId = ctx.userId)->collect(id)->asSet()')
rule(u,'Ordering','result.accounts->size() <= 1 or Sequence{1..result.accounts->size()-1}->forAll(i | result.accounts->at(i).id < result.accounts->at(i+1).id)')
rule(u,'NoDuplicates','result.accounts->isUnique(id)')
rule(u,'Projection','result.accounts->forAll(v | Account.allInstances()->exists(a | a.id = v.id and a.userId = ctx.userId and a.bankName = v.bankName and a.accountType = v.accountType and a.branchName = v.branchName and a.last4 = v.last4 and a.balance = v.balance and a.version = v.version))')
rule(u,'NumberExposure',"result.accounts->forAll(v | v.fullNumber.oclIsUndefined() and v.displayNumber = '**** '.concat(v.last4))")
unchanged(u,'Account')

def account_input(u, update=False):
    auth(u)
    rule(u,'Text', 'Text::trim(cmd.bankName).size() > 0 and Text::trim(cmd.bankName).size() <= 255 and (cmd.branchName.oclIsUndefined() or Text::trim(cmd.branchName).size() <= 255)','pre','Assumption')
    rule(u,'Number',"Text::matches(cmd.fullNumber, '^[0-9]{8,34}$')",'pre')
    rule(u,'Balance','Numeric::finite(cmd.balance) and cmd.balance >= 0 and Numeric::scale(cmd.balance) <= 2 and cmd.balance < 10000000000000000','pre','Assumption')
    rule(u,'UniqueNumber',f'not Account.allInstances()->exists(a | a.userId = ctx.userId and a.numberFingerprint = AccountVault::fingerprint(cmd.fullNumber){" and a.id <> cmd.accountId" if update else ""})','pre')
    rule(u,'LastFour','result.success implies result.account.last4 = Text::last4(cmd.fullNumber) and Account.allInstances()->any(a | a.id = result.account.id).last4 = Text::last4(cmd.fullNumber)')
    rule(u,'ProtectedStorage','result.success implies Account.allInstances()->exists(a | a.id = result.account.id and AccountVault::decrypt(a.numberCiphertext) = cmd.fullNumber and a.numberCiphertext <> cmd.fullNumber and a.numberFingerprint = AccountVault::fingerprint(cmd.fullNumber))',source='Assumption',comment='Ciphertext is authenticated encryption under an external key. The keyed HMAC identifies the exact number without requiring deterministic encryption.')
    rule(u,'Projection','result.success implies Account.allInstances()->exists(a | a.id = result.account.id and a.userId = ctx.userId and a.bankName = Text::trim(cmd.bankName) and a.accountType = cmd.accountType and a.branchName = (if cmd.branchName.oclIsUndefined() then null else Text::trim(cmd.branchName) endif) and a.balance = cmd.balance)')
    rule(u,'FailureRollback','not result.success implies Account.allInstances() = Account.allInstances()@pre and BalanceAdjustment.allInstances() = BalanceAdjustment.allInstances()@pre',source='Assumption')

u=uc(6,'Add a Bank Account',(106,131),'API-ACCOUNT-CREATE','AccountService','create','AccountResult','AccountCommand',goal='Add a manually tracked financial account and its opening balance.',
     actions=['The user opens the Add Account form.','The client displays account fields.','The user enters account details and submits the form.','The client sends the account creation request.','The system returns the account result.','The client displays confirmation and returns to Accounts.'],
     alternative=['The user cancels the form.','The client returns to Accounts.'])
account_input(u)
rule(u,'NewAccount','result.success implies Account.allInstances()->size() = Account.allInstances()@pre->size() + 1 and result.account.version = 0 and Account.allInstances()->any(a | a.id = result.account.id).version = 0')

u=uc(7,'View Bank Account Details',(133,152),'API-ACCOUNT-DETAIL','AccountService','detail','AccountDetailResult','AccountCommand',goal='Inspect a financial account and its recent transactions.',
     actions=['The user opens an account card.','The client requests account details.','The system returns the account and recent transaction data.','The client displays account details and recent transactions.'],
     alternative=['The system returns no recent transactions.','The client displays the account with an empty recent-activity panel.'])
auth(u)
rule(u,'Ownership','Account.allInstances()->exists(a | a.id = cmd.accountId and a.userId = ctx.userId)','pre')
rule(u,'AccountMapping','result.success implies Account.allInstances()->exists(a | a.id = result.account.id and a.id = cmd.accountId and a.userId = ctx.userId and a.bankName = result.account.bankName and a.accountType = result.account.accountType and a.branchName = result.account.branchName and a.balance = result.account.balance and a.version = result.account.version)')
rule(u,'FullNumber','result.success implies result.account.fullNumber = AccountVault::decrypt(Account.allInstances()->any(a | a.id = cmd.accountId).numberCiphertext)')
rule(u,'ExactRecent','result.success implies let eligible : Set(Transaction) = Transaction.allInstances()->select(t | t.accountId = cmd.accountId)->asSet() in result.recent->collect(id)->asSet() = eligible->select(t | eligible->select(other | other.date.ordinal > t.date.ordinal or (other.date.ordinal = t.date.ordinal and other.id > t.id))->size() < 5)->collect(id)->asSet() and result.recent->isUnique(id)',source='Assumption')
rule(u,'RecentOrder','result.recent->size() <= 1 or Sequence{1..result.recent->size()-1}->forAll(i | result.recent->at(i).date.ordinal > result.recent->at(i+1).date.ordinal or (result.recent->at(i).date.ordinal = result.recent->at(i+1).date.ordinal and result.recent->at(i).id > result.recent->at(i+1).id))',source='Assumption')
rule(u,'RecentProjection','result.recent->forAll(v | Transaction.allInstances()->exists(t | t.id = v.id and t.accountId = cmd.accountId and t.date = v.date and t.description = v.description and t.type = v.type and t.status = v.status and t.receiptId = v.receiptId and v.amount = (if t.type = TransactionType::Expense then -t.amount else t.amount endif)))')
unchanged(u,'Account')
unchanged(u,'Transaction')

u=uc(8,'Edit a Bank Account',(155,200),'API-ACCOUNT-DETAIL API-ACCOUNT-UPDATE','AccountService','update','AccountResult','AccountCommand',goal='Revise account details or reconcile a manually tracked balance.',
     actions=['The user opens an account and selects Edit.','The client requests account details and displays the edit form.','The user changes account fields and selects Save Changes.','The client sends the update request.','The system returns the account result.','The client displays confirmation and refreshes the account view.'],
     alternative=['The user selects Edit Accounts on the Accounts page.','The user opens the pencil action on an account card.','The client requests account details and opens the edit form.','The user submits changes.','The client displays the returned result and refreshes Accounts.'])
account_input(u,True)
rule(u,'OwnedVersion','Account.allInstances()->exists(a | a.id = cmd.accountId and a.userId = ctx.userId and a.version = cmd.expectedVersion)','pre','Assumption')
rule(u,'VersionAdvance','result.success implies result.account.id = cmd.accountId and Account.allInstances()->any(a | a.id = cmd.accountId).version = cmd.expectedVersion + 1',source='Assumption')
rule(u,'OtherAccountsPreserved','Account.allInstances()->select(a | a.id <> cmd.accountId) = Account.allInstances()@pre->select(a | a.id <> cmd.accountId)',source='Assumption')
rule(u,'BalanceAudit','result.success implies let old : Account = Account.allInstances()@pre->any(a | a.id = cmd.accountId) in (if old.balance = cmd.balance then BalanceAdjustment.allInstances() = BalanceAdjustment.allInstances()@pre else BalanceAdjustment.allInstances()->size() = BalanceAdjustment.allInstances()@pre->size() + 1 and BalanceAdjustment.allInstances()->exists(b | b.accountId = cmd.accountId and b.userId = ctx.userId and b.oldBalance = old.balance and b.newBalance = cmd.balance and b.accountVersion = cmd.expectedVersion + 1 and b.createdAt = ctx.now) endif)',source='Assumption',comment='Balance reconciliation is an audited correction; it is not revenue or an expense and never affects spending or savings reports.')
unchanged(u,'Transaction')

u=uc(9,'Delete a Bank Account',(202,219),'API-ACCOUNT-DELETE','AccountService','delete','DeleteResult','AccountCommand',goal='Remove a financial account and its recorded activity after confirmation.',
     actions=['The user selects Delete on an account.','The client displays a confirmation dialog with the account label and deletion warning.','The user confirms deletion.','The client sends the delete request.','The system returns the deletion result.','The client displays confirmation and refreshes Accounts.'],
     alternative=['The user cancels the confirmation dialog.','The client closes the dialog.'])
auth(u)
rule(u,'OwnedAccount','Account.allInstances()->exists(a | a.id = cmd.accountId and a.userId = ctx.userId)','pre')
rule(u,'Version','Account.allInstances()->exists(a | a.id = cmd.accountId and a.version = cmd.expectedVersion)','pre','Assumption')
rule(u,'AccountDeleted','result.success implies not Account.allInstances()->exists(a | a.id = cmd.accountId)')
rule(u,'TransactionsDeleted','result.success implies not Transaction.allInstances()->exists(t | t.accountId = cmd.accountId)')
rule(u,'AdjustmentDeletion','result.success implies not BalanceAdjustment.allInstances()->exists(b | b.accountId = cmd.accountId)',source='Assumption')
rule(u,'OtherAccountsPreserved','result.success implies Account.allInstances()->select(a | a.id <> cmd.accountId) = Account.allInstances()@pre->select(a | a.id <> cmd.accountId) and Transaction.allInstances()->select(t | t.accountId <> cmd.accountId) = Transaction.allInstances()@pre->select(t | t.accountId <> cmd.accountId)')
rule(u,'AtomicFailure','not result.success implies Account.allInstances() = Account.allInstances()@pre and Transaction.allInstances() = Transaction.allInstances()@pre and BalanceAdjustment.allInstances() = BalanceAdjustment.allInstances()@pre',comment='Delete uses one database transaction with account version comparison, child deletion and account deletion.')
rule(u,'ResponseIdentity','result.success implies result.accountId = cmd.accountId')

def period_tx(year='ctx.today.year', month='m.month', category=None, date_start=None, date_end=None, expense=True):
    terms=[owned_tx(), 't.status = TransactionStatus::Complete']
    if expense: terms.append('t.type = TransactionType::Expense')
    if year: terms.append(f't.date.year = {year}')
    if month: terms.append(f't.date.month = {month}')
    if category: terms.append(f't.categoryId = {category}')
    if date_start: terms.append(f't.date.ordinal >= {date_start}')
    if date_end: terms.append(f't.date.ordinal <= {date_end}')
    return 'Transaction.allInstances()->select(t | ' + ' and '.join(terms) + ')'

u=uc(10,'View Monthly Expense Summary',(221,239),'API-EXPENSE-SUMMARY','ExpenseService','summary','ExpenseSummaryResult',goal='Compare monthly spending in the current reporting year.',
     actions=['The user opens the Expenses page.','The client requests the monthly expense summary.','The system returns monthly totals.','The client displays the expense comparison chart.'],
     alternative=['The system returns an empty monthly result.','The client displays a chart with no recorded spending.'])
auth(u)
rule(u,'ReportingYear','result.success implies result.year = ctx.today.year',comment='today is resolved once per request in Asia/Saigon, independent of host timezone.')
eligible=period_tx()
rule(u,'ExactMonthCoverage',f'result.success implies result.months->collect(month)->asSet() = {period_tx(month=None)}->collect(t | t.date.month)->asSet()',source='Assumption')
rule(u,'MonthTotal',f'result.months->forAll(m | m.totalExpense = Numeric::round2({eligible}->collect(amount)->sum()))',source='Assumption')
rule(u,'MonthUniqueness','result.months->isUnique(month)')
rule(u,'MonthOrder','result.months->size() <= 1 or Sequence{1..result.months->size()-1}->forAll(i | result.months->at(i).month < result.months->at(i+1).month)')
rule(u,'ValidMonths','result.months->forAll(m | m.month >= 1 and m.month <= 12)')
unchanged(u,'Transaction')
unchanged(u,'Account')
model('ExpenseChart', 'months: Sequence(ExpenseMonth)', 'build(summary: ExpenseSummaryResult): ExpenseChart')
rule(u,'ChartNormalization','result.months->size() = 12 and Sequence{1..12}->forAll(i | result.months->at(i).month = i and result.months->at(i).totalExpense = (if summary.months->exists(m | m.month = i) then summary.months->any(m | m.month = i).totalExpense else 0 endif))',source='Assumption',classifier='ExpenseChart::build(summary: ExpenseSummaryResult): ExpenseChart',comment='Handles an empty summary as well as partial months; charts show every calendar month.')

model('BreakdownQuery', 'month: CalendarDate')
u=uc(11,'View Expenses by Category',(241,258),'API-EXPENSE-BREAKDOWN','ExpenseService','breakdown','BreakdownResult','BreakdownQuery',goal='Review spending distribution and the previous-month comparison.',
     actions=['The user opens Expenses and selects a month.','The client requests the category breakdown.','The system returns category groups and details.','The client displays category totals, comparison values, and transaction details.'],
     alternative=['The system returns an empty breakdown.','The client displays the no-data state.'])
auth(u)
current=period_tx('cmd.month.year','cmd.month.month')
rule(u,'ExactCoverage',f'result.success implies result.groups->collect(g | g.details)->flatten()->collect(id)->asSet() = {current}->collect(id)->asSet()',source='Assumption')
rule(u,'OneGroupPerCategory','result.groups->isUnique(categoryId) and result.groups->collect(g | g.details)->flatten()->isUnique(id)',source='Assumption')
rule(u,'GroupMembership','result.groups->forAll(g | g.details->notEmpty() and g.details->forAll(t | t.categoryId = g.categoryId))')
rule(u,'CategoryLabel',"result.groups->forAll(g | if g.categoryId.oclIsUndefined() then g.category = 'Uncategorized' else let c : Category = Category.allInstances()->any(c | c.id = g.categoryId) in if c.oclIsUndefined() or Text::trim(c.name).size() = 0 then g.category = 'Unknown' else g.category = Text::trim(c.name) endif endif)")
rule(u,'Totals','result.groups->forAll(g | g.total = Numeric::round2(g.details->collect(amount)->sum()))')
prev=period_tx('CalendarDate::previousMonth(cmd.month).year','CalendarDate::previousMonth(cmd.month).month',category='g.categoryId')
rule(u,'PreviousComparison',f'result.groups->forAll(g | let previous : Real = {prev}->collect(amount)->sum() in if previous = 0 then g.changePercent = (if g.total > 0 then 100 else null endif) else g.changePercent = Numeric::round2(((g.total - previous) / previous) * 100) endif)',source='Assumption',comment='January compares with December of the preceding year; category identity, not display name, is the grouping key.')
rule(u,'GroupOrder','result.groups->size() <= 1 or Sequence{1..result.groups->size()-1}->forAll(i | let a : ExpenseGroup = result.groups->at(i) in let b : ExpenseGroup = result.groups->at(i+1) in a.total > b.total or (a.total = b.total and (a.categoryId.oclIsUndefined() or (not b.categoryId.oclIsUndefined() and a.categoryId < b.categoryId))))',source='Assumption')
rule(u,'DetailOrder','result.groups->forAll(g | g.details->size() <= 1 or Sequence{1..g.details->size()-1}->forAll(i | g.details->at(i).date.ordinal < g.details->at(i+1).date.ordinal or (g.details->at(i).date.ordinal = g.details->at(i+1).date.ordinal and g.details->at(i).id < g.details->at(i+1).id)))',source='Assumption')
unchanged(u,'Transaction')

u=uc(12,'View Upcoming Bills',(260,277),'API-BILL-LIST','BillService','upcoming','BillResult',goal='Review upcoming recorded bill obligations.',
     actions=['The user opens the Bills page.','The client requests upcoming bills.','The system returns bill rows.','The client displays descriptions, due dates, logos, and amounts.'],
     alternative=['The system returns no bills.','The client displays the empty-bills state.'])
model('BillView','id: Integer; userId: Integer; description: String; logoUrl: String [0..1]; dueDate: CalendarDate; lastChargeDate: CalendarDate [0..1]; amount: Real')
model('BillResult','success: Boolean; bills: Sequence(BillView)')
auth(u)
rule(u,'OwnedBills','result.bills->forAll(b | b.userId = ctx.userId)')
rule(u,'Window','result.bills->forAll(b | b.dueDate.ordinal >= ctx.today.ordinal and b.dueDate.ordinal <= ctx.today.ordinal + 30)')
rule(u,'UnchargedCycle','result.bills->forAll(b | b.lastChargeDate.oclIsUndefined() or b.lastChargeDate.ordinal < b.dueDate.ordinal)')
eligible='Bill.allInstances()->select(b | b.userId = ctx.userId and b.dueDate.ordinal >= ctx.today.ordinal and b.dueDate.ordinal <= ctx.today.ordinal + 30 and (b.lastChargeDate.oclIsUndefined() or b.lastChargeDate.ordinal < b.dueDate.ordinal))'
rule(u,'ExactCoverage',f'result.success implies result.bills->collect(id)->asSet() = {eligible}->collect(id)->asSet()')
rule(u,'NoDuplicates','result.bills->isUnique(id)')
rule(u,'UrgencyOrder','result.bills->size() <= 1 or Sequence{1..result.bills->size()-1}->forAll(i | let a : BillView = result.bills->at(i) in let b : BillView = result.bills->at(i+1) in a.dueDate.ordinal < b.dueDate.ordinal or (a.dueDate.ordinal = b.dueDate.ordinal and (a.amount > b.amount or (a.amount = b.amount and a.id < b.id))))')
rule(u,'NormalizedMapping',"result.bills->forAll(v | Bill.allInstances()->exists(b | b.id = v.id and b.userId = v.userId and v.description = Text::trim(b.description) and v.amount = Numeric::round2(b.amount) and v.dueDate = b.dueDate and v.lastChargeDate = b.lastChargeDate and v.logoUrl = (if b.logoUrl.oclIsUndefined() or Text::trim(b.logoUrl).size() = 0 then null else Text::trim(b.logoUrl) endif)))")
rule(u,'Amounts','result.bills->forAll(b | Numeric::finite(b.amount) and b.amount >= 0 and b.amount = Numeric::round2(b.amount))',source='Assumption')
unchanged(u,'Bill')

u=uc(13,'View Financial Goals',(279,297),'API-GOAL-LIST','GoalService','list','GoalListResult',goal='Review saving progress and category spending limits.',
     actions=['The user opens the Goals page.','The client requests goals.','The system returns goal cards and progress values.','The client displays the saving goal and expense limit cards.'],
     alternative=['The system returns no goal cards.','The client displays the create-goal entry point.'])
auth(u)
overlap='g.startDate.ordinal <= g.endDate.ordinal and g.startDate.ordinal <= CalendarDate::monthEnd(ctx.today).ordinal and g.endDate.ordinal >= CalendarDate::monthStart(ctx.today).ordinal'
eligible=f'Goal.allInstances()->select(g | g.userId = ctx.userId and {overlap})'
rule(u,'SavingSelection',f'let candidates : Set(Goal) = {eligible}->select(g | g.goalType = GoalType::Saving)->asSet() in if candidates->isEmpty() then result.savingGoal.oclIsUndefined() else let latest : Integer = candidates->collect(g | g.startDate.ordinal)->max() in result.savingGoal.id = candidates->select(g | g.startDate.ordinal = latest)->collect(id)->max() endif')
rule(u,'ExactExpenseCoverage',f'result.expenseGoals->collect(id)->asSet() = {eligible}->select(g | g.goalType = GoalType::Expense_Limit)->collect(id)->asSet() and result.expenseGoals->isUnique(id)')
span_start='(if g.startDate.ordinal > CalendarDate::monthStart(ctx.today).ordinal then g.startDate.ordinal else CalendarDate::monthStart(ctx.today).ordinal endif)'
span_end='(if g.endDate.ordinal < CalendarDate::monthEnd(ctx.today).ordinal then g.endDate.ordinal else CalendarDate::monthEnd(ctx.today).ordinal endif)'
tx=period_tx(year=None,month=None,date_start=span_start,date_end=span_end,expense=False)
rule(u,'SavingProgress',f'not result.savingGoal.oclIsUndefined() implies let g : Goal = Goal.allInstances()->any(g | g.id = result.savingGoal.id) in let rows : Set(Transaction) = {tx}->asSet() in result.savingGoal.progress = Numeric::round2(rows->select(t | t.type = TransactionType::Revenue)->collect(amount)->sum() - rows->select(t | t.type = TransactionType::Expense)->collect(amount)->sum())',source='Assumption')
tx=period_tx(year=None,month=None,category='g.categoryId',date_start=span_start,date_end=span_end)
rule(u,'ExpenseProgress',f'result.expenseGoals->forAll(v | let g : Goal = Goal.allInstances()->any(g | g.id = v.id) in v.progress = Numeric::round2({tx}->collect(amount)->sum()))',source='Assumption')
rule(u,'CategoryLabel',"result.expenseGoals->forAll(v | if v.categoryId.oclIsUndefined() then v.category = 'Uncategorized' else let c : Category = Category.allInstances()->any(c | c.id = v.categoryId) in if c.oclIsUndefined() or Text::trim(c.name).size() = 0 then v.category = 'Unknown' else v.category = Text::trim(c.name) endif endif)")
rule(u,'GoalProjection','result.expenseGoals->including(result.savingGoal)->reject(v | v.oclIsUndefined())->forAll(v | Goal.allInstances()->exists(g | g.id = v.id and g.userId = ctx.userId and g.goalType = v.goalType and g.categoryId = v.categoryId and g.targetAmount = v.targetAmount and g.startDate = v.startDate and g.endDate = v.endDate and g.version = v.version))')
rule(u,'PriorityOrder','result.expenseGoals->size() <= 1 or Sequence{1..result.expenseGoals->size()-1}->forAll(i | let a : GoalView = result.expenseGoals->at(i) in let b : GoalView = result.expenseGoals->at(i+1) in (a.progress >= a.targetAmount and b.progress < b.targetAmount) or ((a.progress >= a.targetAmount) = (b.progress >= b.targetAmount) and (a.endDate.ordinal < b.endDate.ordinal or (a.endDate.ordinal = b.endDate.ordinal and (a.targetAmount < b.targetAmount or (a.targetAmount = b.targetAmount and a.id < b.id))))))')
unchanged(u,'Goal')
unchanged(u,'Transaction')

u=uc(14,'Create a Financial Goal',(299,316),'API-GOAL-CREATE API-CATEGORY-LIST','GoalService','create','GoalResult','GoalCommand',goal='Define a saving target or a category spending limit.',
     actions=['The user opens the Create Goal dialog.','The client requests category choices and displays the goal form.','The user enters goal details and submits the form.','The client sends the goal creation request.','The system returns the creation result.','The client closes the dialog and refreshes Goals.'],
     alternative=['The user cancels the dialog.','The client closes the dialog and shows Goals.'])
auth(u)
rule(u,'CategorySemantics','(cmd.goalType = GoalType::Saving implies cmd.categoryId.oclIsUndefined()) and (cmd.goalType = GoalType::Expense_Limit implies not cmd.categoryId.oclIsUndefined() and Category.allInstances()->exists(c | c.id = cmd.categoryId))','pre')
money(u,'cmd.targetAmount','TargetAmount')
rule(u,'ProspectiveInterval','cmd.startDate.ordinal >= ctx.today.ordinal and cmd.endDate.ordinal > cmd.startDate.ordinal and cmd.endDate.ordinal - cmd.startDate.ordinal <= 366','pre')
rule(u,'NoOverlap','not Goal.allInstances()->exists(g | g.userId = ctx.userId and g.goalType = cmd.goalType and (cmd.goalType = GoalType::Saving or g.categoryId = cmd.categoryId) and g.startDate.ordinal <= cmd.endDate.ordinal and g.endDate.ordinal >= cmd.startDate.ordinal)','pre',comment='Lock the owner User row, then check overlaps and insert within one transaction. MySQL has no exclusion constraint for date intervals.')
rule(u,'ExactPersistence','result.success implies Goal.allInstances()->one(g | g.id = result.goal.id and g.userId = ctx.userId and g.goalType = cmd.goalType and g.categoryId = cmd.categoryId and g.startDate = cmd.startDate and g.endDate = cmd.endDate and g.targetAmount = cmd.targetAmount and g.version = 0)')
rule(u,'ExactlyOne','result.success implies Goal.allInstances()->size() = Goal.allInstances()@pre->size() + 1')
rule(u,'ExistingGoalsPreserved','result.success implies Goal.allInstances()->select(g | g.id <> result.goal.id) = Goal.allInstances()@pre')
rule(u,'AtomicFailure','not result.success implies Goal.allInstances() = Goal.allInstances()@pre')

u=uc(15,'Adjust a Financial Goal',(318,334),'API-GOAL-LIST API-GOAL-UPDATE','GoalService','update','GoalResult','GoalCommand',goal='Change the target amount of a displayed goal.',
     actions=['The user selects Edit on a goal card.','The client displays the target adjustment dialog.','The user enters a new target and selects Save.','The client sends the update request.','The system returns the update result.','The client closes the dialog and refreshes Goals.'],
     alternative=['The user cancels the adjustment.','The client closes the dialog.'])
auth(u)
rule(u,'OwnedGoal','Goal.allInstances()->exists(g | g.id = cmd.goalId and g.userId = ctx.userId)','pre')
money(u,'cmd.targetAmount','TargetAmount')
rule(u,'Version','Goal.allInstances()->exists(g | g.id = cmd.goalId and g.version = cmd.expectedVersion)','pre','Assumption')
rule(u,'OnlyTargetChanged','result.success implies Goal.allInstances()->exists(g | g.id = cmd.goalId and g.targetAmount = cmd.targetAmount and g.version = g.version@pre + 1 and g.userId = g.userId@pre and g.goalType = g.goalType@pre and g.categoryId = g.categoryId@pre and g.startDate = g.startDate@pre and g.endDate = g.endDate@pre)',source='Assumption')
rule(u,'OtherGoalsPreserved','Goal.allInstances()->select(g | g.id <> cmd.goalId) = Goal.allInstances()@pre->select(g | g.id <> cmd.goalId)')
rule(u,'Identity','result.success implies result.goal.id = cmd.goalId and result.goal.targetAmount = cmd.targetAmount and result.goal.version = cmd.expectedVersion + 1',source='Assumption')
rule(u,'FailureRollback','not result.success implies Goal.allInstances() = Goal.allInstances()@pre')

model('SavingsQuery','year: Integer [0..1]')
u=uc(16,'View Savings Summary',(336,355),'API-SAVINGS-SUMMARY','SavingsService','summary','SavingsResult','SavingsQuery',goal='Compare monthly net savings across a selected year and the preceding year.',
     actions=['The user opens the savings chart on Goals.','The client requests the savings summary.','The system returns both yearly series.','The client displays the comparison chart.','The user selects a year.','The client requests and displays the returned series.'],
     alternative=['The system returns series with no recorded activity.','The client displays the returned chart.','The user points to a chart value.','The client displays its month and amount tooltip.'])
auth(u)
rule(u,'YearBounds','cmd.year.oclIsUndefined() or (cmd.year >= 1900 and cmd.year <= 2100)','pre','Assumption')
rule(u,'ResolvedYear','result.year = (if cmd.year.oclIsUndefined() then ctx.today.year else cmd.year endif)',source='Assumption')
rule(u,'UserIdentity','result.userId = ctx.userId')
rule(u,'CompleteSeries','result.thisYear->size() = 12 and result.lastYear->size() = 12')
rule(u,'MonthOrder','Sequence{1..12}->forAll(i | result.thisYear->at(i).month = i and result.lastYear->at(i).month = i)')
for name,year,series in [('ThisYear','result.year','thisYear'),('PreviousYear','result.year - 1','lastYear')]:
    tx=period_tx(year,expense=False)
    rule(u,name+'NetSavings',f'result.{series}->forAll(m | let rows : Set(Transaction) = {tx}->asSet() in m.amount = Numeric::round2(rows->select(t | t.type = TransactionType::Revenue)->collect(amount)->sum() - rows->select(t | t.type = TransactionType::Expense)->collect(amount)->sum()))',source='Assumption',comment='Empty sums are zero; negative savings are retained, without clamping.')
unchanged(u,'Transaction')
unchanged(u,'Account')
model('SavingsTooltip','month: Integer; amount: Real; visible: Boolean')
model('SavingsChart','summary: SavingsResult','hover(series: String, month: Integer): SavingsTooltip')
rule(u,'TooltipValue',"let points : Sequence(SavingsMonth) = if series = 'this_year' then self.summary.thisYear else self.summary.lastYear endif in result.visible and points->one(p | p.month = month and result.month = p.month and result.amount = p.amount)",classifier='SavingsChart::hover(series: String, month: Integer): SavingsTooltip',comment='The caller supplies this_year or last_year and a rendered point; leaving the point hides the tooltip.')

u=uc(17,'Filter Transaction History',(45,62),'API-TRANSACTION-LIST','TransactionService','filter','TransactionListResult','TransactionQuery',goal='Narrow transaction history to revenue or expenses and return to the combined view.',
     actions=['The user selects a transaction type filter.','The client requests history for the selected filter.','The system returns the matching transaction page.','The client replaces the displayed rows and page controls.'],
     alternative=['The user selects All.','The client requests and displays the combined transaction view.'])
transaction_list_rules(u)
rule(u,'ResetPagination','cmd.offset = 0','pre','Assumption',comment='Changing the type filter resets the initial page. Subsequent pages use View Transaction History.')

u=uc(18,'Choose a Category',(64,81),'API-CATEGORY-LIST API-CATEGORY-DETAIL','CategoryService','choose','CategoryResult',goal='Inspect category choices and select a category for a transaction or financial goal.',
     actions=['The user opens the category selector in a form.','The client requests categories.','The system returns category choices.','The user selects a category.','The client requests category details.','The system returns the selection.','The client displays the selected category in the form.'],
     alternative=['The user clears the category selector.','The client shows the form with no selected category.'])
model('CategoryQuery','selectedId: Integer [0..1]')
u['command']='CategoryQuery'
auth(u)
rule(u,'ExactList','result.success implies result.categories->collect(id)->asSet() = Category.allInstances()->collect(id)->asSet()',source='Assumption')
rule(u,'CategoryIdentity','Category.allInstances()->isUnique(id)','inv',classifier='Category',source='Assumption')
rule(u,'NoDuplicateChoices','result.categories->isUnique(id)',source='Assumption')
rule(u,'ChoiceMapping','result.categories->forAll(v | Category.allInstances()->exists(c | c.id = v.id and c.name = v.name))',source='Assumption')
rule(u,'DeterministicOrder','result.categories->size() <= 1 or Sequence{1..result.categories->size()-1}->forAll(i | result.categories->at(i).id < result.categories->at(i+1).id)',source='Assumption')
rule(u,'SelectedIdentity','result.success implies (if cmd.selectedId.oclIsUndefined() then result.selected.oclIsUndefined() else Category.allInstances()->one(c | c.id = cmd.selectedId and result.selected.id = c.id and result.selected.name = c.name) endif)',source='Assumption')
unchanged(u,'Category')

def signature(u):
    args='ctx: RequestContext' + (f', cmd: {u["command"]}' if u['command'] else '')
    return f'{u["service"]}::{u["operation"]}({args}): {u["result"]}'

def snapshot_expression(entity, select='', previous=False):
    # Object identity equality is insufficient for a frame condition. Capture
    # every persisted property into a value tuple, with @pre on old properties.
    collection=entity+'.allInstances()'+('@pre' if previous else '')+select
    props=[x.split(':',1)[0] for x in CLASSES[entity][1]]
    values=', '.join(f'{p} = e.{p}'+('@pre' if previous else '') for p in props)
    return collection+'->collect(e | Tuple{'+values+'})->asSet()'

def close_snapshots(expression):
    for name in ('User','Account','Transaction','BalanceAdjustment','Bill','Goal','Category'):
        name_rx=re.escape(name)
        pattern=name_rx+r'\.allInstances\(\)(->select\([^)]*\))? = '+name_rx+r'\.allInstances\(\)@pre(->select\([^)]*\))?'
        expression=re.sub(pattern,lambda m:snapshot_expression(name,m[1] or '')+' = '+snapshot_expression(name,m[2] or '',True),expression)
    return expression

def local_model(u):
    operation=signature(u).split('::',1)[1]
    model(u['service'], operations=operation)
    text='\n'.join(signature(u)+' '+r['expression']+' '+(r['classifier'] or '') for r in u['rules'])
    names={n for n in CLASSES if re.search(r'\b'+n+r'\b',text)}
    pending=list(names)
    while pending:
        name=pending.pop()
        k,f,o=CLASSES[name]
        refs=' '.join(f+o)
        for other in CLASSES:
            if other not in names and re.search(r'\b'+other+r'\b', refs):
                names.add(other); pending.append(other)
    body=['@startuml','hide empty members']
    for name in sorted(names):
        k,f,o=CLASSES[name]
        body.append(f'{k} {name} {{')
        body += ['  '+(s if k=='enum' else '+'+s) for s in f]
        body += ['  +'+s for s in o]
        body.append('}')
    for name in sorted(names):
        k,f,o=CLASSES[name]
        if k=='enum': continue
        for field in f:
            targets=[t for t in names if re.search(r'\b'+t+r'\b',field.split(':',1)[-1])]
            for t in targets:
                body.append(f'{name} --> {t} : {field.split(":",1)[0]}')
    for parent,child,label in [('Account','User','userId'),('Transaction','Account','accountId'),('Transaction','Category','categoryId'),('Goal','User','userId'),('Goal','Category','categoryId'),('Bill','User','userId'),('BalanceAdjustment','Account','accountId'),('BalanceAdjustment','User','userId')]:
        if parent in names and child in names: body.append(f'{parent} --> {child} : {label}')
    body+=['note "CalendarDate.ordinal is the calendar-day index in Asia/Saigon.\\nReal values denote exact decimals.\\nSnapshot tuples compare complete persistent values." as Semantics','@enduml']
    return '\n'.join(body)

def slug(text): return re.sub(r'[^a-z0-9]+','-',text.lower()).strip('-')
def ucfile(u): return f'uc-{u["number"]:02d}-{slug(u["name"])}.md'
def apifile(api): return 'api-'+api.removeprefix('API-').lower()+'.md'
def numbered(items): return '\n'.join(f'{i}. {s}' for i,s in enumerate(items,1))

def build_uc(u):
    n=f'{u["number"]:02d}'
    actor='Visitor' if u['number'] in (1,2) else 'Account holder'
    body=f'# UC-{n} — {u["name"]}\n\n'
    body+=f'### Description\n\n{u["goal"]}\n\n### Actors\n\nPrimary: {actor}. Supporting: application client and application service.\n\n### Priority\n\nHigh.\n\n'
    body+=f'### Trigger\n\n**TRG-UC-{n}-01** — {u["actions"][0]}\n\n'
    body+=f'### Preconditions\n\n- **PRE-UC-{n}-01** — The application view is open in the client.\n\n'
    outcomes={1:'The client opens the home page with the returned user session.',2:'The client opens the home page with the returned user session.',
              3:'The client displays the returned transaction rows and page controls.',4:'The client displays transaction confirmation and opens history.',
              5:'The client displays account cards or the empty-account view.',6:'The client displays account creation confirmation and returns to Accounts.',
              7:'The client displays the returned account details and recent activity.',8:'The client displays update confirmation and refreshes the account view.',
              9:'The client closes the deletion dialog and refreshes Accounts.',10:'The client displays the monthly expense chart.',
              11:'The client displays the returned category breakdown or no-data view.',12:'The client displays upcoming bills or the empty-bills view.',
              13:'The client displays the returned goal cards or create-goal entry point.',14:'The client closes the goal dialog and refreshes Goals.',
              15:'The client closes the adjustment dialog and refreshes goal cards.',16:'The client displays the returned savings comparison series.',
              17:'The client replaces transaction rows and page controls for the selected filter.',18:'The client displays the selected category in the requesting form.'}
    body+=f'### Postconditions\n\n- **POST-UC-{n}-01** — On success, {outcomes[u["number"]][0].lower()+outcomes[u["number"]][1:]}\n'
    body+=f'- **POST-UC-{n}-02** — On failure, the client displays a recovery message in the current view.\n\n'
    body+=f'### Basic Flow\n\n{numbered(u["actions"])}\n\n'
    body+=f'### Alternative Flows\n\n#### AF-UC-{n}-01\n\n{numbered(u["alternative"])}\n\n'
    body+=f'### Exception Flows\n\n#### EF-UC-{n}-01\n\n1. The system returns an operation error.\n2. The client displays the error message and keeps the current view open.\n3. The actor revises the interaction or retries the request.\n\n'
    if u['number']>2:
        body+=f'#### EF-UC-{n}-02\n\n1. The system returns a rejected authentication context.\n2. The client presents the login entry point.\n\n'
    if u['number'] in (4,8,9,15):
        body+=f'#### EF-UC-{n}-03\n\n1. The system returns an operation conflict.\n2. The client offers to reload the current resource.\n3. The user reloads the view and submits the interaction again.\n\n'
    body+='### UML Model\n\n```plantuml\n'+local_model(u)+'\n```\n\n### Business Rules\n\n'
    for i,r in enumerate(u['rules'],1):
        context=r['classifier'] or signature(u)
        comment=f'-- {r["comment"]}\n' if r['comment'] else ''
        body+=f'```ocl\n-- BR-UC-{n}-{i:02d}\n-- Source: {r["source"]}\n{comment}context {context}\n{r["kind"]} BR_UC_{n}_{i:02d}_{r["name"]}:\n  {close_snapshots(r["expression"])}\n```\n\n'
    a,b=u['rows']
    body+=f'### Related UI\n\n- Product-source UI descriptions: [Use cases rows {a}-{b}]({URL}#gid=0&range=A{a}:B{b}). No Figma node identifier was supplied.\n\n'
    if u['number']==18: body+='- Category detail presentation is a proposed extension grounded in the supplied category-detail endpoint, not a verified design screen.\n\n'
    if u['number']==18: body+=f'- Goal category selector: [Use cases rows 299-316]({URL}#gid=0&range=A299:B316). Category endpoint evidence: [API rows 173-205]({URL}#gid=439687549&range=A173:B205).\n\n'
    body+='### Related APIs\n\n'+'\n'.join(f'- [{api}](../api/{apifile(api)})' for api in u['apis'])+'\n\n'
    body+='### Notes\n\nSee [source mapping](../../coverage-report.md), [review decisions](../../consistency-review.md), and [assumptions](../../ASSUMPTIONS.md). The supplied spreadsheet is specification evidence; no running application or Figma interaction was verified.\n'
    write('01-inception/uc/'+ucfile(u),body)

def source_apis():
    rows=json.loads((ROOT/'source/api-contract.json').read_text(encoding='utf-8'))['rows']
    result=[]
    current=None
    for row in rows:
        cells=row['cells']; label=(cells[0] or '') if cells else ''
        if re.match(r'^API-[A-Z]+',label):
            if current: result.append(current)
            current={'row':row['row'],'sections':{}}
        elif current and label and len(cells)>1:
            current['sections'][label]=cells[1] or ''
    if current: result.append(current)
    return result

def parse_fields(text):
    fields=[]
    for chunk in re.split(r'(?:^|\n)•\s*',text)[1:]:
        lines=chunk.strip().splitlines(); name=lines[0].strip()
        meta={}
        for line in lines[1:]:
            for item in re.split(r';\s*(?=[A-Za-z ]+:)',line.strip()):
                match=re.match(r'([A-Za-z ]+):\s*(.*)',item)
                if match: meta[match[1]]=match[2]
        fields.append((name,meta))
    return fields

def field_text(name,meta,response=False):
    typ=meta.get('Type','string').replace('string | string[]','string')
    description=meta.get('Description',name.rsplit('.',1)[-1].replace('_',' ').capitalize()+'.')
    # Replace source policy explanations with literal wire descriptions.
    desc_overrides={
        'hasMore':'Boolean page continuation indicator.',
        'total':'Integer count associated with the response.',
        'data[].account_id':'Account identifier.',
        'data[].type':'Transaction type.',
        'data[].status':'Transaction status.',
        'data[].month':'Month label.',
        'data.recent_transactions':'Recent transaction array.',
        'data.recent_transactions[].amount':'Signed transaction amount.',
        'data.createdAt':'Creation timestamp.',
    }
    description=desc_overrides.get(name,description)
    description=re.sub(r'\s*Maps to .*|\s*All is never returned.*|\s*; references an account.*','',description)
    description=description.replace('Owner user identifier.','User identifier.').replace('Owner identifier.','User identifier.')
    example=meta.get('Example')
    if example and re.search(r'[ăâđêôơưàáạếụ]',example): example='Operation completed'
    if not example:
        example={'integer':'1','number':'1000','boolean':'true','array<object>':'[]','object':'{}'}.get(typ,'example')
    if 'timestamp' in description.lower() or name.endswith('createdAt'): example='2026-09-30T03:00:00Z'
    fmt=meta.get('Format')
    if not fmt and re.fullmatch(r'\d{4}-\d{2}-\d{2}',example):fmt='date'
    allowed=meta.get('Allowed values')
    syntax=('JSON '+typ+'.') if response else ('Matches the declared JSON type.' if typ not in ('integer','number') else 'JSON '+typ+'; query and path values use complete decimal text.')
    if fmt in ('date','YYYY-MM-DD'): syntax='Valid calendar date in YYYY-MM-DD representation.'
    if fmt=='YYYY-MM': syntax='Calendar month in YYYY-MM representation.'
    if fmt=='email': syntax='Email-address syntax.'
    if fmt=='date-time': syntax='RFC 3339 date-time representation.'
    if fmt=='YYYY': syntax='Exactly four decimal digits representing an integer year.'
    if allowed: syntax='Member of the declared public enum.'
    result=f'### `{name}`\n\n- Type: {typ}\n'
    if fmt: result+=f'- Format: {fmt}\n'
    result+=f'- Required: {meta.get("Required","Yes")}\n- Nullable: {meta.get("Nullable","No")}\n'
    if 'Default' in meta: result+=f'- Default: {meta["Default"]}\n'
    if allowed: result+=f'- Allowed values: {allowed}\n'
    result+=f'- Validation: {syntax}\n- Trigger: {"Response containing this field." if response else "Request containing this field."}\n- Description: {description}\n- Example: `{example}`\n\n'
    return result

def get_section(sections,*labels):
    return next((sections[l] for l in labels if l in sections),'')

def response_fields(api, sections):
    text=next((v for k,v in sections.items() if k.startswith('Success Response')),'')
    original=parse_fields(text)
    fields=[]
    envelope={'success':{'Type':'boolean','Required':'Yes','Nullable':'No','Example':'true','Description':'Response outcome flag.'},
              'message':{'Type':'string','Required':'Yes','Nullable':'No','Example':'Operation completed','Description':'Human-readable response message.'}}
    fields=list(envelope.items())
    # Already-enveloped endpoints retain their source payload keys. Legacy roots
    # move beneath data; transaction pagination remains at the envelope root.
    for name,meta in original:
        if name in envelope: continue
        if api=='API-TRANSACTION-LIST' and name in ('total','hasMore'):
            fields.append((name,meta)); continue
        if name=='data' or name.startswith('data.') or name.startswith('data['): dest=name
        else: dest='data.'+name
        if api in ('API-ACCOUNT-CREATE','API-ACCOUNT-UPDATE'):
            dest=dest.replace('data.account.','data.')
            if dest=='data.account_id': dest='data.id'
            if dest=='data.account_number_full': continue
        if api=='API-GOAL-UPDATE': dest=dest.replace('data.updated_goal.','data.')
        fields.append((dest,meta))
    if not any(n=='data' for n,m in fields):
        fields.insert(2,('data',{'Type':'object','Required':'Yes','Nullable':'No','Description':'Operation payload.','Example':'{}'}))
    # Make containers explicit, including nested object fields in authentication.
    present={n for n,m in fields}
    additions=[]
    for name,meta in fields:
        parts=name.split('.')
        for i in range(1,len(parts)):
            parent='.'.join(parts[:i])
            if parent.endswith('[]'): continue
            if parent not in present:
                present.add(parent)
                additions.append((parent,{'Type':'object','Required':'Yes','Nullable':'No','Description':'Nested response object.','Example':'{}'}))
    fields[3:3]=additions
    if api=='API-ACCOUNT-DETAIL':
        fields.append(('data.recent_transactions[].transaction_id',{'Type':'integer','Required':'Yes','Nullable':'No','Description':'Transaction identifier.','Example':'8'}))
    for name in ('API-ACCOUNT-LIST','API-ACCOUNT-CREATE','API-ACCOUNT-DETAIL','API-ACCOUNT-UPDATE'):
        if api==name:
            dest='data.accounts[].version' if api=='API-ACCOUNT-LIST' else 'data.version'
            fields.append((dest,{'Type':'integer','Required':'Yes','Nullable':'No','Description':'Resource version.','Example':'1'}))
    if api=='API-GOAL-LIST':
        fields.extend([(name,{'Type':'integer','Required':'Yes','Nullable':'No','Description':'Goal version.','Example':'1'})
                       for name in ['data.savingGoal.version','data.expenseGoals[].version']])
        # Fields needed to render/edit every returned goal without hidden lookups.
        for name,typ,example in [('goal_type','string','Expense_Limit'),('start_date','string','2026-10-01'),('end_date','string','2026-10-31')]:
            fields.append(('data.expenseGoals[].'+name,{'Type':typ,'Required':'Yes','Nullable':'No','Description':'Goal '+name.replace('_',' ')+'.','Example':example}))
        fields.append(('data.expenseGoals[].category_id',{'Type':'integer','Required':'Yes','Nullable':'Yes','Description':'Category identifier.','Example':'3'}))
    if api in ('API-GOAL-CREATE','API-GOAL-UPDATE'):
        fields.append(('data.version',{'Type':'integer','Required':'Yes','Nullable':'No','Description':'Goal version.','Example':'1' if api.endswith('UPDATE') else '0'}))
    if api=='API-EXPENSE-BREAKDOWN':
        fields.append(('data[].category_id',{'Type':'integer','Required':'Yes','Nullable':'Yes','Description':'Category group identifier.','Example':'3'}))
        fields.append(('data[].subCategories[].transaction_id',{'Type':'integer','Required':'Yes','Nullable':'No','Description':'Transaction identifier.','Example':'8'}))
    if api=='API-EXPENSE-SUMMARY':
        for name,meta in fields:
            if name=='data[].month': meta['Allowed values']='Jan; Feb; Mar; Apr; May; Jun; Jul; Aug; Sep; Oct; Nov; Dec'
    return fields

def build_api(source):
    s=source['sections']; api=s['API ID']; name=s.get('API Name',api)
    related=[f'UC-{u["number"]:02d}' for u in UCS if api in u['apis']]
    assert related,api
    method=s['Method']; path=re.sub(r':(\w+)',r'{\1}',s['Path'])
    public=api in ('API-AUTH-LOGIN','API-AUTH-REGISTER')
    text=f'# {api} — {name}\n\n## API ID\n\n`{api}`\n\n## API Name\n\n{name}\n\n## Related Use Case IDs\n\n'+', '.join(f'`{x}`' for x in related)+'\n\n'
    text+=f'## Method\n\n`{method}`\n\n## Path\n\n`{path}`\n\n## Description\n\n{s.get("Description",name+".")}\n\n'
    text+=f'## Authentication\n\n{"Public." if public else "Bearer JWT in the Authorization header."}\n\n## Authorization\n\n{"None." if public else "Authenticated request context."}\n\n'
    text+='## Request Headers\n\n'
    if not public: text+=field_text('Authorization',{'Type':'string','Required':'Yes','Nullable':'No','Description':'Bearer authentication header.','Example':'Bearer <access-token>'})
    if method in ('POST','PUT'):
        text+=field_text('Content-Type',{'Type':'string','Required':'Yes','Nullable':'No','Allowed values':'application/json','Description':'Body media type.','Example':'application/json'})
    if public and method not in ('POST','PUT'):text+='None.\n\n'
    paths=parse_fields(get_section(s,'Path Parameter(s)','Path Parameters'))
    if not paths:
        for param in re.findall(r'{(\w+)}',path): paths.append(('path.'+param,{'Type':'integer','Required':'Yes','Nullable':'No','Description':'Resource identifier.','Example':'3'}))
    if api=='API-ACCOUNT-DELETE':
        text+=field_text('If-Match',{'Type':'string','Required':'Yes','Nullable':'No','Format':'Quoted integer ETag','Description':'Resource version representation.','Example':'"1"'})
    text+='## Path Parameters\n\n'+(''.join(field_text(n,m) for n,m in paths) or 'None.\n\n')
    query=parse_fields(get_section(s,'Query Parameter(s)','Query Parameters'))
    if api=='API-TRANSACTION-LIST':
        for n,m in query:
            if n=='query.type':m['Required']='No';m['Default']='All'
    if api=='API-SAVINGS-SUMMARY':
        for n,m in query:
            if n=='query.year':m.pop('Default',None);m['Format']='YYYY';m['Example']='2026'
    text+='## Query Parameters\n\n'+(''.join(field_text(n,m) for n,m in query) or 'None.\n\n')
    body=parse_fields(get_section(s,'Request Body'))
    if api in ('API-ACCOUNT-UPDATE','API-TRANSACTION-CREATE','API-GOAL-UPDATE'):
        body.append(('expected_version',{'Type':'integer','Required':'Yes','Nullable':'No','Description':'Resource version supplied by the client.','Example':'1'}))
    text+='## Request Body\n\n'+(''.join(field_text(n,m) for n,m in body) or 'None.\n\n')
    status='201' if api in ('API-AUTH-REGISTER','API-ACCOUNT-CREATE','API-TRANSACTION-CREATE','API-GOAL-CREATE') else '200'
    text+=f'## Success Response — HTTP {status}\n\n'+''.join(field_text(n,m,True) for n,m in response_fields(api,s))
    if api=='API-ACCOUNT-DETAIL':text+='Response header: `ETag`, type string, required, non-null; example `"1"`.\n\n'
    errors={400:('MALFORMED_REQUEST','Malformed wire input or rejected operation.'),500:('INTERNAL_ERROR','Temporary service failure.')}
    if not public or api=='API-AUTH-LOGIN':errors[401]=('UNAUTHENTICATED','Rejected authentication context.')
    if api in ('API-ACCOUNT-DETAIL','API-ACCOUNT-UPDATE','API-ACCOUNT-DELETE','API-GOAL-UPDATE','API-CATEGORY-DETAIL','API-TRANSACTION-CREATE'):
        errors[404]=('NOT_FOUND','Unavailable resource response.')
    if api in ('API-AUTH-REGISTER','API-ACCOUNT-CREATE','API-ACCOUNT-UPDATE','API-ACCOUNT-DELETE','API-TRANSACTION-CREATE','API-GOAL-CREATE','API-GOAL-UPDATE'):
        errors[409]=('OPERATION_CONFLICT','Operation conflict.')
    for status,(code,trigger) in sorted(errors.items()):
        text+=f'## Error Response — HTTP {status}\n\nPublic outcome: {trigger}\n\n'
        for n,m in [('success',{'Type':'boolean','Required':'Yes','Nullable':'No','Example':'false','Description':'Error outcome flag.'}),
                    ('message',{'Type':'string','Required':'Yes','Nullable':'No','Description':'Human-readable error message.','Example':'Request could not be completed'}),
                    ('error',{'Type':'object','Required':'Yes','Nullable':'No','Description':'Error payload.','Example':'{}'}),
                    ('error.code',{'Type':'string','Required':'Yes','Nullable':'No','Allowed values':code,'Description':'Public error code.','Example':code})]:
            text+=field_text(n,m,True)
    text+='## Notes\n\n[Common wire contract](common-contract.md). '
    text+=f'Source: [API contract starting at row {source["row"]}]({URL}#gid=439687549&range=A{source["row"]}:B{source["row"]+16}). '
    text+='These are reviewed contracts; compatibility changes are recorded in the package review. Child fields under a nullable object apply when that object is present.\n'
    write('01-inception/api/'+apifile(api),text)

def main():
    command_names={1:'RegisterCommand',2:'LoginCommand',4:'CreateTransactionCommand',6:'CreateAccountCommand',7:'AccountDetailQuery',8:'UpdateAccountCommand',9:'DeleteAccountCommand',14:'CreateGoalCommand',15:'UpdateGoalCommand'}
    for u in UCS:
        if u['number'] not in command_names:continue
        fields=CLASSES[u['command']][1]
        used=set(re.findall(r'\bcmd\.(\w+)',' '.join(r['expression'] for r in u['rules'])))
        u['command']=command_names[u['number']]
        model(u['command'],';'.join(f for f in fields if f.split(':',1)[0] in used))
    for u in UCS: build_uc(u)
    write('01-inception/uc/README.md','# Use Case Index\n\n'+'\n'.join(f'- [UC-{u["number"]:02d} — {u["name"]}]({ucfile(u)})' for u in UCS))
    sources=source_apis()
    for source in sources:build_api(source)
    write('01-inception/api/README.md','# API Index\n\n- [Common wire contract](common-contract.md)\n\n'+'\n'.join(f'- [{s["sections"]["API ID"]} — {s["sections"].get("API Name","")}]({apifile(s["sections"]["API ID"])})' for s in sources))
    build_evidence(sources)
    print(f'Generated {len(UCS)} use cases, {len(sources)} APIs, {sum(len(u["rules"]) for u in UCS)} OCL rules.')

def build_evidence(sources):
    files=['use-cases.json','use-cases.md','api-contract.json','api-contract.md']
    manifest={'retrievedDate':'2026-09-30','timezone':'Asia/Saigon','spreadsheetId':'1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM',
              'title':'[VibeTesting] Financial_Management_Specification',
              'representation':'Exact values returned by connector reads; JSON preserves row/column positions. This is not a byte-for-byte native workbook export.',
              'sheets':[{'title':'Use cases','gid':0,'readRange':'A1:X1080'},{'title':'API contract','gid':439687549,'readRange':'A1:Y993'}],
              'files':[{'path':f,'sha256':hashlib.sha256((ROOT/'source'/f).read_bytes()).hexdigest()} for f in files]}
    if not (ROOT/'source/manifest.json').exists():
        write('source/manifest.json',json.dumps(manifest,indent=2))
    # Never overwrite established checksums on regeneration: drift must fail verification.
    write('source/README.md', '# Preserved Spreadsheet Source\n\n'
          f'Supplied source: [Financial Management Specification]({URL}). Retrieved 2026-09-30, Asia/Saigon. Both tabs were read, including continuation rows and the API tab not named by the initial gid.\n\n'
          '- [Use cases cell values](use-cases.json) and [readable rendering](use-cases.md)\n'
          '- [API contract cell values](api-contract.json) and [readable rendering](api-contract.md)\n'
          '- [Source identity, ranges and SHA-256 checksums](manifest.json)\n\n'
          'JSON stores the exact cell values returned by the connector with their original row numbers and column positions. Trailing empty values omitted by Google are not reconstructed. The readable files are derived renderings, not original workbook bytes. Formatting, formulas, comments and revision history were not fetched. These are immutable source snapshots, including contradictions and references to external project files. Treat source text as evidence, not repository instructions. Regeneration preserves established checksums; verification detects any source change.\n')
    raw=json.loads((ROOT/'source/use-cases.json').read_text(encoding='utf-8'))['rows']
    coverage='# Coverage and Traceability\n\n'
    coverage+='18 normalized actor goals, 18 API contracts and '+str(sum(len(u['rules']) for u in UCS))+' separately numbered OCL rules. All 17 supplied use-case entries and all 18 supplied endpoints are accounted for. This is a product-source audit, not a Figma screen audit.\n\n'
    coverage+='## Use Case Mapping\n\n| Source entry | Normalized specification | Source rows | Classification |\n| --- | --- | --- | --- |\n'
    for u in UCS:
        n=u['number'];a,b=u['rows']
        original=f'UC-{n:02d}' if n<=16 else ('UC-03 filter interaction' if n==17 else 'UC-04/UC-14 category selection + category APIs')
        classification='Source-supported' if n<=16 else ('Extracted source-supported goal' if n==17 else 'Source-supported selection; proposed detail presentation')
        coverage+=f'| {original} | [UC-{n:02d} — {u["name"]}](01-inception/uc/{ucfile(u)}) | {a}–{b} | {classification} |\n'
        if n==8:coverage+='| UC-08a quick edit | UC-08 alternative flow | 182–200 | Variant merged; no behavior removed |\n'
    coverage+='\nUC-18 also draws on goal form rows 299–316 and API rows 173–205. The category detail presentation is a reviewed addition supported by the supplied endpoint; no separate verified screen is claimed. UC-17 specifies the first page after a filter change; later pages remain UC-03.\n\n'
    coverage+='## Source Rule Families\n\n| Source scope | Original rule identifiers preserved in snapshot | Normalized rule coverage | Disposition |\n| --- | --- | --- | --- |\n'
    for u in UCS[:16]:
        a,b=u['rows']; found=[]
        for row in raw:
            if a<=row['row']<=b:
                for cell in row['cells']:
                    for x in re.findall(r'\bBR-[A-Z]+(?:-[A-Z]+)*-\d+\b',cell or ''):
                        if x not in found:found.append(x)
        n=f'{u["number"]:02d}'
        disposition='Retained and formalized; refinements recorded in review'
        if u['number'] in (6,8):disposition='Revised; branch/deposit/capacity restrictions removed and concurrency/storage clarified'
        if u['number'] in (4,10,11,13,16):disposition='Revised for Complete-only cash-flow accounting and exact mappings'
        coverage+=f'| Source UC-{n} | '+', '.join(found)+f' | BR-UC-{n}-01 through BR-UC-{n}-{len(u["rules"]):02d} | {disposition} |\n'
    coverage+='\nSource identifiers can be duplicated, embedded in multi-context blocks, or present only as prose. This table maps policy families rather than claiming one-to-one identity. Source variants and original rule text remain available under source/. Removed predicates and added assumptions have explicit decisions in [review](consistency-review.md) and [assumptions](ASSUMPTIONS.md).\n\n'
    coverage+='## Endpoint Mapping\n\n| Source API / start row | Normalized contract | Use cases |\n| --- | --- | --- |\n'
    for s in sources:
        api=s['sections']['API ID'];related=', '.join(f'UC-{u["number"]:02d}' for u in UCS if api in u['apis'])
        coverage+=f'| {api}, row {s["row"]} | [{api}](01-inception/api/{apifile(api)}) | {related} |\n'
    coverage+='\n## Persistence Mapping\n\n| Local persistent concept | MySQL table | Principal relationships |\n| --- | --- | --- |\n'
    coverage+='| User | users | Owner of accounts, goals and bills |\n| Account | accounts | user_id → users.id |\n| Transaction | transactions | account_id → accounts.id; optional category_id → categories.id |\n| Category | categories | Global catalogue; referenced by transactions and goals |\n| Bill | bills | user_id → users.id |\n| Goal | goals | user_id → users.id; optional category_id → categories.id |\n| BalanceAdjustment | balance_adjustments | (account_id, user_id) → accounts.(id, user_id) |\n\n'
    coverage+='Commands, queries, contexts, helpers, projected views, chart objects and result envelopes are transient concepts and have no separate persistence table. Goal progress and report totals are derived. Raw passwords, confirmations, JWTs and full account numbers have no plaintext columns.\n\n'
    coverage+='## Wire and Local Vocabulary Mapping\n\n| Local member | Database column | Wire field spelling |\n| --- | --- | --- |\n'
    for local,db,wire in [('User.id / fullName','users.id / full_name','data.user.id / fullName'),('Account.id / userId','accounts.id / user_id','id / user_id'),('Account.bankName / accountType / branchName','bank_name / account_type / branch_name','bank_name / account_type / branch_name'),('Account.numberCiphertext / last4','number_ciphertext / last4','account_number_full in detail; account_number_last_4 in projections'),('Transaction.id / accountId','transactions.id / account_id','transaction_id / account_id in history; transactionId / accountId in create'),('Transaction.date / description','transaction_date / item_description','transaction_date / item_description in history; transactionDate / itemDescription in create; date / description in recent activity'),('Transaction.shopName / paymentMethod / categoryId','shop_name / payment_method / category_id','shop_name / payment_method in history; shopName / paymentMethod in create; category_id in create'),('Category.id / name','categories.id / name','category_id / category_name'),('BillView.id / description','bills.id / item_description','billId / itemDescription'),('BillView.dueDate / lastChargeDate / logoUrl','due_date / last_charge_date / logo_url','dueDate / lastChargeDate / logoUrl'),('Goal.id / goalType / categoryId','goals.id / goal_type / category_id','goal_id / goal_type / category_id'),('Goal.startDate / endDate / targetAmount','start_date / end_date / target_amount','start_date / end_date / target_amount'),('GoalView.progress','Derived; no column','target_achieved for saving; current_expense for expense limits'),('CalendarDate','DATE column where persistent','YYYY-MM-DD string'),('ExpenseMonth.month','Derived; no column','Jan through Dec month labels'),('SavingsMonth.month','Derived; no column','01 through 12 two-digit month strings'),('AccountType::Credit_Card','Credit Card enum literal','Credit Card'),('Command.expectedVersion','Compares accounts.version or goals.version','expected_version; quoted If-Match for account delete')]:
        coverage+=f'| {local} | {db} | {wire} |\n'
    coverage+='\nFields in this table are shorthand for the endpoint-specific payload paths documented in the API contracts. Protected number storage is mapped through the local vault; the plaintext number is not a database column.\n\n'
    coverage+='## Unsupported and Unverified Scope\n\n'
    coverage+='| Candidate | Status | Boundary |\n| --- | --- | --- |\n'
    for name,status,gap in [('Figma pages and node IDs','Missing evidence','No Figma source was supplied.'),('Google login/sign-up','Excluded by source','No OAuth flow or contract.'),('Password recovery/change','Excluded by source','No supported recovery lifecycle.'),('Persistent sign-in, refresh, logout or revocation','Unsupported','Only registration and login are supplied.'),('Pay Now / execute bill payment','Excluded by source','Upcoming bills is read-only.'),('Create or update bills','Unsupported','Bill population is external to this package.'),('Bank synchronization / account transfer / multi-currency','Unsupported','Accounts and transactions are manually tracked.'),('Transaction update or status transition','Unsupported','No supplied endpoint or continuation.'),('Category administration','Unsupported','Catalogue is read-only.'),('Goal deletion or schedule changes','Unsupported','Source adjustment is target-only.'),('Historical report preservation after deletion','Unsupported','Source permanently deletes transactions.'),('Runtime implementation compliance','Unverified','No application code or database was supplied.')]:
        coverage+=f'| {name} | {status} | {gap} |\n'
    coverage+='\n## Validation Scope\n\n[Validation report](validation-report.md) distinguishes new-package structural checks, DBML compilation, source preservation, semantic scenario review and repository-wide failures in pre-existing packages. None of these establishes a live product implementation.\n'
    write('coverage-report.md',coverage)

if __name__ == '__main__': main()
