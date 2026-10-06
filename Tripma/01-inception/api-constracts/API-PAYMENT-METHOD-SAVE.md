---
artifact_type: api-contract
status: Draft
api_id: API-PAYMENT-METHOD-SAVE
related_uc_id: UC-13
---

# API-PAYMENT-METHOD-SAVE: Save Payment Method

## General Information

### API ID

API-PAYMENT-METHOD-SAVE

### API Name

Save Payment Method

### Related Use Case IDs

UC-13

### Method

POST

### Path

/api/users/me/payment-methods

### Description

Creates an account-owned saved payment method from a completed Tripma booking payment.

### Authentication

Required session

### Authorization

Governed by UC-13.

## Request Header(s)

### headers.Content-Type

Type: string; Format: MIME type
Required: Yes
Nullable: No

### headers.Accept

Type: string; Format: MIME type
Required: No
Nullable: No

### headers.Idempotency-Key

Type: string
Required: Yes
Nullable: No

## Path Parameter(s)

None

## Query Parameter(s)

None

## Request Body

### bookingId

Type: string; Format: UUID
Required: Yes
Nullable: No

### makeDefault

Type: boolean
Required: Yes
Nullable: No

## Success Response — HTTP 201

### success

Type: boolean
Required: Yes
Nullable: No

### message

Type: string
Required: Yes
Nullable: No

### data

Type: object
Required: Yes
Nullable: No

### data.id

Type: string; Format: UUID
Required: Yes
Nullable: No

### data.paymentMethod

Type: string; Format: enum
Required: Yes
Nullable: No

### data.displayName

Type: string
Required: Yes
Nullable: No

### data.cardLastFour

Type: string
Required: Yes
Nullable: No

### data.expireDate

Type: string; Format: ISO 8601 date
Required: Yes
Nullable: No

### data.isDefault

Type: boolean
Required: Yes
Nullable: No

### data.createdAt

Type: string; Format: ISO 8601
Required: Yes
Nullable: No

## Error Response — HTTP 400

### message

Type: string
Required: Yes
Nullable: No

### issues

Type: array
Required: No
Nullable: No

### issues[].field

Type: string
Required: Yes
Nullable: No

### issues[].code

Type: string
Required: Yes
Nullable: No

## Error Response — HTTP 401

### message

Type: string
Required: Yes
Nullable: No

## Error Response — HTTP 404

### message

Type: string
Required: Yes
Nullable: No

## Error Response — HTTP 409

### message

Type: string
Required: Yes
Nullable: No

## Error Response — HTTP 500

### message

Type: string
Required: Yes
Nullable: No

### retryable

Type: boolean
Required: Yes
Nullable: No

## Notes

This contract saves a reusable payment-method reference after the successful booking payment described by UC-13.
