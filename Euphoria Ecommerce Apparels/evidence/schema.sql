-- SQL dump generated using DBML (dbml.dbdiagram.io)
-- Database: PostgreSQL
-- Generated at: 2026-09-24T02:33:16.780Z

CREATE TYPE "order_status" AS ENUM (
  'PLACED',
  'IN_PROGRESS',
  'SHIPPED',
  'DELIVERED',
  'CANCELLED'
);

CREATE TYPE "payment_method" AS ENUM (
  'COD'
);

CREATE TYPE "delivery_status" AS ENUM (
  'QUEUED',
  'SENT',
  'FAILED'
);

CREATE TYPE "address_role" AS ENUM (
  'SHIPPING',
  'BILLING'
);

CREATE TABLE "customers" (
  "id" varchar PRIMARY KEY,
  "name" varchar NOT NULL,
  "email" varchar UNIQUE NOT NULL,
  "phone" varchar
);

CREATE TABLE "sessions" (
  "id" varchar PRIMARY KEY,
  "customer_id" varchar NOT NULL,
  "token_hash" varchar UNIQUE NOT NULL,
  "csrf_hash" varchar NOT NULL,
  "expires_at" timestamptz NOT NULL,
  "revoked" boolean NOT NULL DEFAULT false
);

CREATE TABLE "categories" (
  "id" varchar PRIMARY KEY,
  "name" varchar NOT NULL,
  "image_url" varchar NOT NULL,
  "display_rank" integer UNIQUE NOT NULL
);

CREATE TABLE "products" (
  "id" varchar PRIMARY KEY,
  "category_id" varchar NOT NULL,
  "title" varchar NOT NULL,
  "brand" varchar NOT NULL,
  "image_url" varchar NOT NULL,
  "description" text NOT NULL,
  "rating" decimal(3,2) NOT NULL,
  "comment_count" integer NOT NULL DEFAULT 0,
  "question_count" integer NOT NULL DEFAULT 0,
  "style" varchar NOT NULL,
  "published" boolean NOT NULL,
  "featured" boolean NOT NULL,
  "display_rank" integer UNIQUE NOT NULL,
  "recommendation_rank" integer UNIQUE NOT NULL,
  "created_at" timestamptz NOT NULL,
  "display_amount" decimal(14,2) NOT NULL,
  "currency" char(3) NOT NULL,
  CHECK (display_amount >= 0),
  CHECK (comment_count >= 0 AND question_count >= 0),
  CHECK (rating >= 0 AND rating <= 5)
);

CREATE TABLE "variants" (
  "id" varchar PRIMARY KEY,
  "product_id" varchar NOT NULL,
  "size" varchar NOT NULL,
  "color" varchar NOT NULL,
  "amount" decimal(14,2) NOT NULL,
  "currency" char(3) NOT NULL,
  "sellable" boolean NOT NULL,
  "stock" integer NOT NULL,
  "version" integer NOT NULL DEFAULT 0,
  CHECK (stock >= 0 AND amount >= 0 AND version >= 0)
);

CREATE TABLE "product_images" (
  "id" varchar PRIMARY KEY,
  "product_id" varchar NOT NULL,
  "url" varchar NOT NULL,
  "position" integer NOT NULL
);

CREATE TABLE "product_attributes" (
  "id" varchar PRIMARY KEY,
  "product_id" varchar NOT NULL,
  "name" varchar NOT NULL,
  "value" varchar NOT NULL
);

CREATE TABLE "promotions" (
  "id" varchar PRIMARY KEY,
  "heading" varchar NOT NULL,
  "image_url" varchar NOT NULL,
  "target_category_id" varchar,
  "published" boolean NOT NULL,
  "display_rank" integer UNIQUE NOT NULL
);

CREATE TABLE "testimonials" (
  "id" varchar PRIMARY KEY,
  "name" varchar NOT NULL,
  "body" text NOT NULL,
  "rating" decimal(3,2) NOT NULL,
  "published" boolean NOT NULL,
  "display_rank" integer UNIQUE NOT NULL,
  CHECK (rating >= 0 AND rating <= 5)
);

CREATE TABLE "carts" (
  "id" varchar PRIMARY KEY,
  "customer_id" varchar UNIQUE NOT NULL,
  "version" integer NOT NULL DEFAULT 0,
  "currency" char(3) NOT NULL,
  CHECK (version >= 0)
);

CREATE TABLE "cart_lines" (
  "id" varchar PRIMARY KEY,
  "cart_id" varchar NOT NULL,
  "variant_id" varchar NOT NULL,
  "title" varchar NOT NULL,
  "image_url" varchar NOT NULL,
  "size" varchar NOT NULL,
  "color" varchar NOT NULL,
  "quantity" integer NOT NULL,
  "unit_amount" decimal(14,2) NOT NULL,
  "currency" char(3) NOT NULL,
  CHECK (quantity > 0 AND unit_amount >= 0)
);

CREATE TABLE "address_books" (
  "customer_id" varchar PRIMARY KEY,
  "version" integer NOT NULL DEFAULT 0,
  CHECK (version >= 0)
);

CREATE TABLE "addresses" (
  "id" varchar PRIMARY KEY,
  "customer_id" varchar NOT NULL,
  "first_name" varchar NOT NULL,
  "last_name" varchar NOT NULL,
  "country" varchar NOT NULL,
  "company" varchar,
  "street" varchar NOT NULL,
  "unit" varchar,
  "city" varchar NOT NULL,
  "state" varchar NOT NULL,
  "postal_code" varchar NOT NULL,
  "phone" varchar NOT NULL,
  "instructions" text
);

CREATE TABLE "default_address_roles" (
  "customer_id" varchar NOT NULL,
  "role" address_role NOT NULL,
  "address_id" varchar NOT NULL,
  PRIMARY KEY ("customer_id", "role")
);

CREATE TABLE "orders" (
  "id" varchar PRIMARY KEY,
  "number" varchar UNIQUE NOT NULL,
  "customer_id" varchar NOT NULL,
  "placed_at" timestamptz NOT NULL,
  "estimated_delivery" date,
  "status" order_status NOT NULL,
  "payment_method" payment_method NOT NULL,
  "version" integer NOT NULL DEFAULT 0,
  "subtotal_amount" decimal(14,2) NOT NULL,
  "discount_amount" decimal(14,2) NOT NULL,
  "shipping_amount" decimal(14,2) NOT NULL,
  "total_amount" decimal(14,2) NOT NULL,
  "currency" char(3) NOT NULL,
  CHECK (total_amount = subtotal_amount - discount_amount + shipping_amount),
  CHECK (subtotal_amount >= 0 AND discount_amount >= 0 AND shipping_amount >= 0 AND total_amount >= 0 AND version >= 0)
);

CREATE TABLE "order_addresses" (
  "order_id" varchar NOT NULL,
  "role" address_role NOT NULL,
  "first_name" varchar NOT NULL,
  "last_name" varchar NOT NULL,
  "country" varchar NOT NULL,
  "company" varchar,
  "street" varchar NOT NULL,
  "unit" varchar,
  "city" varchar NOT NULL,
  "state" varchar NOT NULL,
  "postal_code" varchar NOT NULL,
  "phone" varchar NOT NULL,
  "instructions" text,
  PRIMARY KEY ("order_id", "role")
);

CREATE TABLE "order_lines" (
  "id" varchar PRIMARY KEY,
  "order_id" varchar NOT NULL,
  "variant_id" varchar NOT NULL,
  "title" varchar NOT NULL,
  "image_url" varchar NOT NULL,
  "size" varchar NOT NULL,
  "color" varchar NOT NULL,
  "quantity" integer NOT NULL,
  "unit_amount" decimal(14,2) NOT NULL,
  "currency" char(3) NOT NULL,
  CHECK (quantity > 0 AND unit_amount >= 0)
);

CREATE TABLE "order_events" (
  "id" varchar PRIMARY KEY,
  "order_id" varchar NOT NULL,
  "status" order_status NOT NULL,
  "occurred_at" timestamptz NOT NULL,
  "message" text NOT NULL
);

CREATE TABLE "checkout_receipts" (
  "id" varchar PRIMARY KEY,
  "customer_id" varchar NOT NULL,
  "request_key" varchar NOT NULL,
  "request_digest" varchar NOT NULL,
  "order_id" varchar UNIQUE NOT NULL
);

CREATE TABLE "reset_deliveries" (
  "id" varchar PRIMARY KEY,
  "customer_id" varchar NOT NULL,
  "status" delivery_status NOT NULL,
  "provider_reference" varchar,
  "created_at" timestamptz NOT NULL
);

CREATE TABLE "wishlist_entries" (
  "id" varchar PRIMARY KEY,
  "customer_id" varchar NOT NULL,
  "product_id" varchar NOT NULL,
  "created_at" timestamptz NOT NULL
);

CREATE TABLE "viewed_products" (
  "id" varchar PRIMARY KEY,
  "customer_id" varchar NOT NULL,
  "product_id" varchar NOT NULL,
  "viewed_at" timestamptz NOT NULL
);

CREATE INDEX ON "sessions" ("customer_id", "expires_at");

CREATE INDEX ON "products" ("published", "category_id", "style");

CREATE INDEX ON "products" ("published", "created_at");

CREATE UNIQUE INDEX ON "variants" ("product_id", "size", "color");

CREATE INDEX ON "variants" ("size", "color");

CREATE UNIQUE INDEX ON "product_images" ("product_id", "position");

CREATE UNIQUE INDEX ON "cart_lines" ("cart_id", "variant_id");

CREATE UNIQUE INDEX ON "addresses" ("customer_id", "id");

CREATE INDEX ON "orders" ("customer_id", "status", "placed_at");

CREATE UNIQUE INDEX ON "orders" ("customer_id", "id");

CREATE UNIQUE INDEX ON "order_lines" ("order_id", "variant_id");

CREATE INDEX ON "order_events" ("order_id", "occurred_at");

CREATE UNIQUE INDEX ON "checkout_receipts" ("customer_id", "request_key");

CREATE INDEX ON "reset_deliveries" ("status", "created_at");

CREATE UNIQUE INDEX ON "wishlist_entries" ("customer_id", "product_id");

CREATE UNIQUE INDEX ON "viewed_products" ("customer_id", "product_id");

CREATE INDEX ON "viewed_products" ("customer_id", "viewed_at");

ALTER TABLE "sessions" ADD FOREIGN KEY ("customer_id") REFERENCES "customers" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "products" ADD FOREIGN KEY ("category_id") REFERENCES "categories" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "variants" ADD FOREIGN KEY ("product_id") REFERENCES "products" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "product_images" ADD FOREIGN KEY ("product_id") REFERENCES "products" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "product_attributes" ADD FOREIGN KEY ("product_id") REFERENCES "products" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "promotions" ADD FOREIGN KEY ("target_category_id") REFERENCES "categories" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "carts" ADD FOREIGN KEY ("customer_id") REFERENCES "customers" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "cart_lines" ADD FOREIGN KEY ("cart_id") REFERENCES "carts" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "cart_lines" ADD FOREIGN KEY ("variant_id") REFERENCES "variants" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "address_books" ADD FOREIGN KEY ("customer_id") REFERENCES "customers" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "addresses" ADD FOREIGN KEY ("customer_id") REFERENCES "address_books" ("customer_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "default_address_roles" ADD FOREIGN KEY ("customer_id") REFERENCES "address_books" ("customer_id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "default_address_roles" ADD FOREIGN KEY ("customer_id", "address_id") REFERENCES "addresses" ("customer_id", "id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "orders" ADD FOREIGN KEY ("customer_id") REFERENCES "customers" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "order_addresses" ADD FOREIGN KEY ("order_id") REFERENCES "orders" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "order_lines" ADD FOREIGN KEY ("order_id") REFERENCES "orders" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "order_lines" ADD FOREIGN KEY ("variant_id") REFERENCES "variants" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "order_events" ADD FOREIGN KEY ("order_id") REFERENCES "orders" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "checkout_receipts" ADD FOREIGN KEY ("customer_id") REFERENCES "customers" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "checkout_receipts" ADD FOREIGN KEY ("customer_id", "order_id") REFERENCES "orders" ("customer_id", "id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "reset_deliveries" ADD FOREIGN KEY ("customer_id") REFERENCES "customers" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "wishlist_entries" ADD FOREIGN KEY ("customer_id") REFERENCES "customers" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "wishlist_entries" ADD FOREIGN KEY ("product_id") REFERENCES "products" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "viewed_products" ADD FOREIGN KEY ("customer_id") REFERENCES "customers" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "viewed_products" ADD FOREIGN KEY ("product_id") REFERENCES "products" ("id") DEFERRABLE INITIALLY IMMEDIATE;
