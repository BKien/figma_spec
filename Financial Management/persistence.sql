-- Apply after compiling schema.dbml to MySQL; requires MySQL 8.0.16+.
-- These CHECK constraints supplement the source DBML, not a second schema.
ALTER TABLE accounts
  ADD CONSTRAINT ck_account_balance CHECK (balance >= 0),
  ADD CONSTRAINT ck_account_version CHECK (version >= 0),
  ADD CONSTRAINT ck_account_bank CHECK (CHAR_LENGTH(TRIM(bank_name)) > 0),
  ADD CONSTRAINT ck_account_last4 CHECK (last4 REGEXP '^[0-9]{4}$');

ALTER TABLE transactions
  ADD CONSTRAINT ck_transaction_amount CHECK (amount > 0),
  ADD CONSTRAINT ck_transaction_description CHECK (CHAR_LENGTH(TRIM(item_description)) > 0),
  ADD CONSTRAINT ck_transaction_shop CHECK (CHAR_LENGTH(TRIM(shop_name)) > 0),
  ADD CONSTRAINT ck_transaction_payment CHECK (CHAR_LENGTH(TRIM(payment_method)) > 0);

ALTER TABLE balance_adjustments
  ADD CONSTRAINT ck_adjustment_balances CHECK (old_balance >= 0 AND new_balance >= 0),
  ADD CONSTRAINT ck_adjustment_changed CHECK (old_balance <> new_balance),
  ADD CONSTRAINT ck_adjustment_version CHECK (account_version > 0);

ALTER TABLE bills
  ADD CONSTRAINT ck_bill_amount CHECK (amount >= 0);

ALTER TABLE goals
  ADD CONSTRAINT ck_goal_target CHECK (target_amount > 0),
  ADD CONSTRAINT ck_goal_dates CHECK (end_date > start_date AND DATEDIFF(end_date, start_date) <= 366),
  ADD CONSTRAINT ck_goal_version CHECK (version >= 0),
  ADD CONSTRAINT ck_goal_category CHECK (
    (goal_type = 'Saving' AND category_id IS NULL) OR
    (goal_type = 'Expense_Limit' AND category_id IS NOT NULL)
  );

-- Procedures must validate decimal scale before DECIMAL conversion: MySQL can
-- round inputs before CHECK evaluation. CHECK alone cannot reject extra scale.
-- Goal insertion: lock users.id FOR UPDATE, read conflicting inclusive intervals,
-- then insert within the same transaction. No unique index enforces interval overlap.
-- Transaction creation: lock accounts.id FOR UPDATE, compare expected_version,
-- check the Complete expense balance, insert, adjust balance, increment version, commit.
-- Manual edit/deletion and target adjustment perform their version comparison
-- and all writes within a transaction. Conflict and failure always roll back.
