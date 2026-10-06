-- SQL dump generated using DBML (dbml.dbdiagram.io)
-- Database: MySQL
-- Generated at: 2026-09-30T08:19:11.562Z

CREATE TABLE `users` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(255) UNIQUE NOT NULL COMMENT 'Lowercase trimmed email; uniqueness checked on this stored representation.',
  `username` varchar(255) UNIQUE NOT NULL COMMENT 'Server-generated email-prefix name with collision suffix; no public username input.',
  `password_hash` varchar(100) NOT NULL COMMENT 'Bcrypt, cost 10. No plaintext or confirmation column.',
  `version` bigint NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `accounts` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `bank_name` varchar(255) NOT NULL,
  `account_type` ENUM ('Checking', 'Credit Card', 'Savings', 'Investment', 'Loan') NOT NULL,
  `branch_name` varchar(255),
  `number_ciphertext` varbinary(512) NOT NULL COMMENT 'Authenticated encryption under an external encryption key; never plain account number.',
  `number_fingerprint` binary(32) NOT NULL COMMENT 'Keyed HMAC-SHA-256 of the exact digit sequence; external HMAC key. Leading zeros retained.',
  `last4` char(4) NOT NULL,
  `balance` decimal(18,2) NOT NULL,
  `version` bigint NOT NULL DEFAULT 0 COMMENT 'Increment every account update or transaction creation, including Pending/Failed creation.',
  `created_at` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP),
  `updated_at` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `categories` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255) NOT NULL
);

CREATE TABLE `transactions` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `account_id` bigint NOT NULL,
  `category_id` bigint,
  `transaction_date` date NOT NULL,
  `type` ENUM ('Revenue', 'Expense') NOT NULL,
  `status` ENUM ('Complete', 'Pending', 'Failed') NOT NULL DEFAULT 'Complete',
  `item_description` varchar(255) NOT NULL,
  `shop_name` varchar(255) NOT NULL,
  `payment_method` varchar(100) NOT NULL,
  `amount` decimal(18,2) NOT NULL COMMENT 'Positive magnitude; type determines direction. Only Complete changes balances and contributes to reports.',
  `receipt_id` varchar(255),
  `created_at` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `balance_adjustments` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `account_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `old_balance` decimal(18,2) NOT NULL,
  `new_balance` decimal(18,2) NOT NULL,
  `account_version` bigint NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `bills` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `item_description` varchar(255) NOT NULL,
  `logo_url` varchar(2048),
  `due_date` date NOT NULL,
  `last_charge_date` date,
  `amount` decimal(18,2) NOT NULL
);

CREATE TABLE `goals` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `goal_type` ENUM ('Saving', 'Expense_Limit') NOT NULL,
  `category_id` bigint,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `target_amount` decimal(18,2) NOT NULL,
  `version` bigint NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP),
  `updated_at` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

CREATE UNIQUE INDEX `uq_account_owner_number` ON `accounts` (`user_id`, `number_fingerprint`);

CREATE INDEX `ix_accounts_owner` ON `accounts` (`user_id`, `id`);

CREATE UNIQUE INDEX `uq_account_owner_pair` ON `accounts` (`id`, `user_id`);

CREATE INDEX `ix_transactions_history` ON `transactions` (`account_id`, `transaction_date`, `id`);

CREATE INDEX `ix_transactions_reports` ON `transactions` (`account_id`, `type`, `status`, `transaction_date`);

CREATE INDEX `ix_transactions_category` ON `transactions` (`category_id`, `transaction_date`);

CREATE UNIQUE INDEX `uq_adjustment_version` ON `balance_adjustments` (`account_id`, `account_version`);

CREATE INDEX `ix_adjustment_owner_time` ON `balance_adjustments` (`user_id`, `created_at`);

CREATE INDEX `ix_bills_upcoming` ON `bills` (`user_id`, `due_date`, `id`);

CREATE INDEX `ix_goals_conflicts` ON `goals` (`user_id`, `goal_type`, `category_id`, `start_date`, `end_date`);

CREATE INDEX `ix_goals_month` ON `goals` (`user_id`, `start_date`, `end_date`);

ALTER TABLE `users` COMMENT = 'Lock this row to serialize goal interval conflict checks for this user. JWTs are issued externally and not persisted as raw tokens.';

ALTER TABLE `accounts` COMMENT = 'Manually tracked asset balance. Credit Card and Loan labels do not define debt/credit-limit semantics. No balance sign change or currency conversion is inferred.';

ALTER TABLE `categories` COMMENT = 'Global read-only catalogue managed outside this package; names are not identifiers. Do not delete referenced categories.';

ALTER TABLE `transactions` COMMENT = 'Append-only within this product boundary. Deleting the account cascades recorded transactions, so all derived reports change. No transaction edit, status transition, payment execution or transfer endpoint is specified.';

ALTER TABLE `balance_adjustments` COMMENT = 'Audit record created in the same transaction as a manual balance change. It is excluded from expense and savings reports. Deleted with its account, consistently with permanent deletion scope.';

ALTER TABLE `bills` COMMENT = 'Read-only obligation data populated externally; Pay Now and bill creation are outside scope. Due cycle is identified by the stored due_date.';

ALTER TABLE `goals` COMMENT = 'Date intervals are inclusive. Serialize check-plus-insert using a users row lock. MySQL cannot enforce non-overlap via this index. Progress is derived, never persisted.';

ALTER TABLE `accounts` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT;

ALTER TABLE `transactions` ADD FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`) ON DELETE CASCADE;

ALTER TABLE `transactions` ADD FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE RESTRICT;

ALTER TABLE `balance_adjustments` ADD FOREIGN KEY (`account_id`, `user_id`) REFERENCES `accounts` (`id`, `user_id`) ON DELETE CASCADE;

ALTER TABLE `bills` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT;

ALTER TABLE `goals` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT;

ALTER TABLE `goals` ADD FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE RESTRICT;
