-- SQL dump generated using DBML (dbml.dbdiagram.io)
-- Database: MySQL
-- Generated at: 2026-09-27T13:58:48.378Z

CREATE TABLE `customers` (
  `id` varchar(255) PRIMARY KEY,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) UNIQUE NOT NULL,
  `phone` varchar(255)
);

CREATE TABLE `sessions` (
  `id` varchar(255) PRIMARY KEY,
  `customer_id` varchar(255) NOT NULL,
  `token_hash` varchar(255) UNIQUE NOT NULL,
  `csrf_hash` varchar(255) NOT NULL,
  `expires_at` datetime NOT NULL,
  `revoked` boolean NOT NULL DEFAULT false
);

CREATE TABLE `categories` (
  `id` varchar(255) PRIMARY KEY,
  `name` varchar(255) NOT NULL,
  `image_url` varchar(255) NOT NULL,
  `display_rank` integer UNIQUE NOT NULL
);

CREATE TABLE `products` (
  `id` varchar(255) PRIMARY KEY,
  `category_id` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `brand` varchar(255) NOT NULL,
  `image_url` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `rating` decimal(3,2) NOT NULL,
  `comment_count` integer NOT NULL DEFAULT 0,
  `question_count` integer NOT NULL DEFAULT 0,
  `style` varchar(255) NOT NULL,
  `published` boolean NOT NULL,
  `featured` boolean NOT NULL,
  `display_rank` integer UNIQUE NOT NULL,
  `recommendation_rank` integer UNIQUE NOT NULL,
  `created_at` datetime NOT NULL,
  `display_amount` decimal(14,2) NOT NULL,
  `currency` char(3) NOT NULL,
  CHECK (display_amount >= 0),
  CHECK (comment_count >= 0 AND question_count >= 0),
  CHECK (rating >= 0 AND rating <= 5)
);

CREATE TABLE `variants` (
  `id` varchar(255) PRIMARY KEY,
  `product_id` varchar(255) NOT NULL,
  `size` varchar(255) NOT NULL,
  `color` varchar(255) NOT NULL,
  `amount` decimal(14,2) NOT NULL,
  `currency` char(3) NOT NULL,
  `sellable` boolean NOT NULL,
  `stock` integer NOT NULL,
  `version` integer NOT NULL DEFAULT 0,
  CHECK (stock >= 0 AND amount >= 0 AND version >= 0)
);

CREATE TABLE `product_images` (
  `id` varchar(255) PRIMARY KEY,
  `product_id` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  `position` integer NOT NULL
);

CREATE TABLE `product_attributes` (
  `id` varchar(255) PRIMARY KEY,
  `product_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `value` varchar(255) NOT NULL
);

CREATE TABLE `promotions` (
  `id` varchar(255) PRIMARY KEY,
  `heading` varchar(255) NOT NULL,
  `image_url` varchar(255) NOT NULL,
  `target_category_id` varchar(255),
  `published` boolean NOT NULL,
  `display_rank` integer UNIQUE NOT NULL
);

CREATE TABLE `testimonials` (
  `id` varchar(255) PRIMARY KEY,
  `name` varchar(255) NOT NULL,
  `body` text NOT NULL,
  `rating` decimal(3,2) NOT NULL,
  `published` boolean NOT NULL,
  `display_rank` integer UNIQUE NOT NULL,
  CHECK (rating >= 0 AND rating <= 5)
);

CREATE TABLE `carts` (
  `id` varchar(255) PRIMARY KEY,
  `customer_id` varchar(255) UNIQUE NOT NULL,
  `version` integer NOT NULL DEFAULT 0,
  `currency` char(3) NOT NULL,
  CHECK (version >= 0)
);

CREATE TABLE `cart_lines` (
  `id` varchar(255) PRIMARY KEY,
  `cart_id` varchar(255) NOT NULL,
  `variant_id` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `image_url` varchar(255) NOT NULL,
  `size` varchar(255) NOT NULL,
  `color` varchar(255) NOT NULL,
  `quantity` integer NOT NULL,
  `unit_amount` decimal(14,2) NOT NULL,
  `currency` char(3) NOT NULL,
  CHECK (quantity > 0 AND unit_amount >= 0)
);

CREATE TABLE `address_books` (
  `customer_id` varchar(255) PRIMARY KEY,
  `version` integer NOT NULL DEFAULT 0,
  CHECK (version >= 0)
);

CREATE TABLE `addresses` (
  `id` varchar(255) PRIMARY KEY,
  `customer_id` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `country` varchar(255) NOT NULL,
  `company` varchar(255),
  `street` varchar(255) NOT NULL,
  `unit` varchar(255),
  `city` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `postal_code` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `instructions` text
);

CREATE TABLE `default_address_roles` (
  `customer_id` varchar(255) NOT NULL,
  `role` ENUM ('SHIPPING', 'BILLING') NOT NULL,
  `address_id` varchar(255) NOT NULL,
  PRIMARY KEY (`customer_id`, `role`)
);

CREATE TABLE `orders` (
  `id` varchar(255) PRIMARY KEY,
  `number` varchar(255) UNIQUE NOT NULL,
  `customer_id` varchar(255) NOT NULL,
  `placed_at` datetime NOT NULL,
  `estimated_delivery` date,
  `status` ENUM ('PLACED', 'IN_PROGRESS', 'SHIPPED', 'DELIVERED', 'CANCELLED') NOT NULL,
  `payment_method` ENUM ('COD') NOT NULL,
  `version` integer NOT NULL DEFAULT 0,
  `subtotal_amount` decimal(14,2) NOT NULL,
  `discount_amount` decimal(14,2) NOT NULL,
  `shipping_amount` decimal(14,2) NOT NULL,
  `total_amount` decimal(14,2) NOT NULL,
  `currency` char(3) NOT NULL,
  CHECK (total_amount = subtotal_amount - discount_amount + shipping_amount),
  CHECK (subtotal_amount >= 0 AND discount_amount >= 0 AND shipping_amount >= 0 AND total_amount >= 0 AND version >= 0)
);

CREATE TABLE `order_addresses` (
  `order_id` varchar(255) NOT NULL,
  `role` ENUM ('SHIPPING', 'BILLING') NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `country` varchar(255) NOT NULL,
  `company` varchar(255),
  `street` varchar(255) NOT NULL,
  `unit` varchar(255),
  `city` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `postal_code` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `instructions` text,
  PRIMARY KEY (`order_id`, `role`)
);

CREATE TABLE `order_lines` (
  `id` varchar(255) PRIMARY KEY,
  `order_id` varchar(255) NOT NULL,
  `variant_id` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `image_url` varchar(255) NOT NULL,
  `size` varchar(255) NOT NULL,
  `color` varchar(255) NOT NULL,
  `quantity` integer NOT NULL,
  `unit_amount` decimal(14,2) NOT NULL,
  `currency` char(3) NOT NULL,
  CHECK (quantity > 0 AND unit_amount >= 0)
);

CREATE TABLE `order_events` (
  `id` varchar(255) PRIMARY KEY,
  `order_id` varchar(255) NOT NULL,
  `status` ENUM ('PLACED', 'IN_PROGRESS', 'SHIPPED', 'DELIVERED', 'CANCELLED') NOT NULL,
  `occurred_at` datetime NOT NULL,
  `message` text NOT NULL
);

CREATE TABLE `checkout_receipts` (
  `id` varchar(255) PRIMARY KEY,
  `customer_id` varchar(255) NOT NULL,
  `request_key` varchar(255) NOT NULL,
  `request_digest` varchar(255) NOT NULL,
  `order_id` varchar(255) UNIQUE NOT NULL
);

CREATE TABLE `reset_deliveries` (
  `id` varchar(255) PRIMARY KEY,
  `customer_id` varchar(255) NOT NULL,
  `status` ENUM ('QUEUED', 'SENT', 'FAILED') NOT NULL,
  `provider_reference` varchar(255),
  `created_at` datetime NOT NULL
);

CREATE TABLE `wishlist_entries` (
  `id` varchar(255) PRIMARY KEY,
  `customer_id` varchar(255) NOT NULL,
  `product_id` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL
);

CREATE TABLE `viewed_products` (
  `id` varchar(255) PRIMARY KEY,
  `customer_id` varchar(255) NOT NULL,
  `product_id` varchar(255) NOT NULL,
  `viewed_at` datetime NOT NULL
);

CREATE INDEX `sessions_index_0` ON `sessions` (`customer_id`, `expires_at`);

CREATE INDEX `products_index_1` ON `products` (`published`, `category_id`, `style`);

CREATE INDEX `products_index_2` ON `products` (`published`, `created_at`);

CREATE UNIQUE INDEX `variants_index_3` ON `variants` (`product_id`, `size`, `color`);

CREATE INDEX `variants_index_4` ON `variants` (`size`, `color`);

CREATE UNIQUE INDEX `product_images_index_5` ON `product_images` (`product_id`, `position`);

CREATE UNIQUE INDEX `cart_lines_index_6` ON `cart_lines` (`cart_id`, `variant_id`);

CREATE UNIQUE INDEX `addresses_index_7` ON `addresses` (`customer_id`, `id`);

CREATE INDEX `orders_index_8` ON `orders` (`customer_id`, `status`, `placed_at`);

CREATE UNIQUE INDEX `orders_index_9` ON `orders` (`customer_id`, `id`);

CREATE UNIQUE INDEX `order_lines_index_10` ON `order_lines` (`order_id`, `variant_id`);

CREATE INDEX `order_events_index_11` ON `order_events` (`order_id`, `occurred_at`);

CREATE UNIQUE INDEX `checkout_receipts_index_12` ON `checkout_receipts` (`customer_id`, `request_key`);

CREATE INDEX `reset_deliveries_index_13` ON `reset_deliveries` (`status`, `created_at`);

CREATE UNIQUE INDEX `wishlist_entries_index_14` ON `wishlist_entries` (`customer_id`, `product_id`);

CREATE UNIQUE INDEX `viewed_products_index_15` ON `viewed_products` (`customer_id`, `product_id`);

CREATE INDEX `viewed_products_index_16` ON `viewed_products` (`customer_id`, `viewed_at`);

ALTER TABLE `sessions` ADD FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`);

ALTER TABLE `products` ADD FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`);

ALTER TABLE `variants` ADD FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

ALTER TABLE `product_images` ADD FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

ALTER TABLE `product_attributes` ADD FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

ALTER TABLE `promotions` ADD FOREIGN KEY (`target_category_id`) REFERENCES `categories` (`id`);

ALTER TABLE `carts` ADD FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`);

ALTER TABLE `cart_lines` ADD FOREIGN KEY (`cart_id`) REFERENCES `carts` (`id`);

ALTER TABLE `cart_lines` ADD FOREIGN KEY (`variant_id`) REFERENCES `variants` (`id`);

ALTER TABLE `address_books` ADD FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`);

ALTER TABLE `addresses` ADD FOREIGN KEY (`customer_id`) REFERENCES `address_books` (`customer_id`);

ALTER TABLE `default_address_roles` ADD FOREIGN KEY (`customer_id`) REFERENCES `address_books` (`customer_id`);

ALTER TABLE `default_address_roles` ADD FOREIGN KEY (`customer_id`, `address_id`) REFERENCES `addresses` (`customer_id`, `id`);

ALTER TABLE `orders` ADD FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`);

ALTER TABLE `order_addresses` ADD FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`);

ALTER TABLE `order_lines` ADD FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`);

ALTER TABLE `order_lines` ADD FOREIGN KEY (`variant_id`) REFERENCES `variants` (`id`);

ALTER TABLE `order_events` ADD FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`);

ALTER TABLE `checkout_receipts` ADD FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`);

ALTER TABLE `checkout_receipts` ADD FOREIGN KEY (`customer_id`, `order_id`) REFERENCES `orders` (`customer_id`, `id`);

ALTER TABLE `reset_deliveries` ADD FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`);

ALTER TABLE `wishlist_entries` ADD FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`);

ALTER TABLE `wishlist_entries` ADD FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

ALTER TABLE `viewed_products` ADD FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`);

ALTER TABLE `viewed_products` ADD FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);
