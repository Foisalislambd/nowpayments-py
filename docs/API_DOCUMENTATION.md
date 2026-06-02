# NOWPayments API Documentation

> Source: https://documenter.getpostman.com/view/7907941/2s93JusNJt
> Last Updated: March 2025

## Overview

NOWPayments is a non-custodial cryptocurrency payment processing platform. Accept payments in 300+ cryptos with auto-conversion to your preferred currency.

- **Base URL (Production)**: `https://api.nowpayments.io`
- **Base URL (Sandbox)**: `https://api-sandbox.nowpayments.io`
- **API Version**: v1

## Authentication

All API requests require the `x-api-key` header with your API key.

```
x-api-key: YOUR_API_KEY
```

## API Products

- **Payment API** - Integrate crypto payments into your service
- **Mass Payouts API** - Initiate thousands of transactions in a single call
- **Custody API** - Manage funds within custody balance
- **Customer Management API** - Manage customer accounts & balances
- **Recurring Payments API** - Crypto subscriptions & billing
- **Fiat Withdrawals API** - Accept crypto, settle in fiat

---

## Payment Endpoints

### GET /v1/status
Check API availability and status.

**Response**: API status object

---

### GET /v1/currencies
Get list of available payment currencies (crypto).

**Response**: `{ currencies: string[] }`

---

### GET /v1/currencies/{currency}
Get full list of currencies with payment limits (fiat + crypto).

---

### GET /v1/estimate
Get estimated price in selected cryptocurrency.

**Query Params**:
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| amount | number | yes | Amount in currency_from |
| currency_from | string | yes | From currency (usd, eur, etc) |
| currency_to | string | yes | To currency (btc, eth, etc) |

**Response**:
```json
{
  "amount_from": 3999.5,
  "currency_from": "usd",
  "currency_to": "btc",
  "estimated_amount": 0.17061637
}
```

---

### GET /v1/min-amount
Get minimum payment amount for currency pair.

**Query Params**:
| Param | Type | Required |
|-------|------|----------|
| currency_from | string | yes |
| currency_to | string | yes |

**Response**:
```json
{
  "currency_from": "eth",
  "currency_to": "trx",
  "fiat_equivalent": 35.40626584,
  "min_amount": 0.0078999
}
```

---

### POST /v1/payment
Create a payment.

**Body**:
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| price_amount | number | yes | Fiat amount to charge |
| price_currency | string | yes | Fiat currency (usd, eur, etc) |
| pay_amount | number | no | Crypto amount (auto-calculated if omitted) |
| pay_currency | string | yes | Crypto currency (btc, eth, etc) |
| ipn_callback_url | string | no | Callback URL for IPN |
| order_id | string | no | Your order ID |
| order_description | string | no | Order description |
| purchase_id | string | no | For partial payments continuation |
| payout_address | string | no | Custom payout address |
| payout_currency | string | no | Required if payout_address specified |
| payout_extra_id | string | no | Memo/tag for payout |
| fixed_rate | boolean | no | Use fixed exchange rate |

**Response**: Payment object with pay_address, pay_amount, etc.

---

### GET /v1/payment/{payment_id}
Get payment status.

**Response**: Payment status object with payment_status (waiting, confirming, confirmed, spending, partially_paid, finished, failed, refunded, expired)

---

### GET /v1/payment/
Get list of payments.

**Query Params**:
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| limit | number | 10 | Records per page |
| page | number | 0 | Page number |
| sortBy | string | created_at | Sort field |
| orderBy | string | asc | asc/desc |
| dateFrom | string | - | YYYY-MM-DD |
| dateTo | string | - | YYYY-MM-DD |

---

### POST /v1/payment/{payment_id}/update-merchant-estimate
Update payment estimate (call before expiration).

---

### POST /v1/invoice
Create an invoice (redirect flow).

**Body**:
| Param | Type | Required |
|-------|------|----------|
| price_amount | number | yes |
| price_currency | string | yes |
| pay_currency | string | no |
| ipn_callback_url | string | no |
| order_id | string | no |
| order_description | string | no |
| success_url | string | no |
| cancel_url | string | no |

**Response**: invoice_url for customer redirect

---

### POST /v1/invoice-payment
Create payment for existing invoice.

---

### POST /v1/payout
Create mass payout (requires JWT Bearer token).

### POST /v1/payout/{id}/verify
Verify payout with 2FA `verification_code`.

### POST /v1/payout/w_id/cancel
Cancel a scheduled payout (`payout_id` in body).

### GET /v1/payout/fee
Estimate network fee (`currency`, `amount` query params).

---

## Recurring Payments (Subscriptions)

### GET /v1/subscriptions
List recurring payments.

### GET /v1/subscriptions/{id}
Get single recurring payment.

### DELETE /v1/subscriptions/{id}
Cancel recurring payment.

### GET /v1/subscriptions/plans
List subscription plans.

### GET /v1/subscriptions/plans/{id}
Get subscription plan.

### PATCH /v1/subscriptions/plans/{id}
Update plan.

---

## Sub-Partner (Customer Management)

### GET /v1/sub-partner
List sub-partners.

### GET /v1/sub-partner/balance/{sub_partner_id}
Get sub-partner balance.

### GET /v1/sub-partner/transfers
List transfers.

### GET /v1/sub-partner/transfer/{id}
Get transfer details.

---

## IPN (Instant Payment Notifications)

1. Set ipn_callback_url in create_payment
2. Generate IPN Secret in Dashboard
3. Recursively sort object keys, then `JSON.stringify` and HMAC-SHA512 with IPN secret (see `src/utils/ipn.ts`)
4. Compare with x-nowpayments-sig header
5. Verify callback authenticity

**Payment Statuses**: waiting, confirming, confirmed, spending, partially_paid, finished, failed, refunded, expired

---

## References

- [Official API Docs](https://documenter.getpostman.com/view/7907941/2s93JusNJt)
- [Sandbox Docs](https://documenter.getpostman.com/view/7907941/T1LSCRHC)
- [Knowledge Base](https://nowpayments.io/help/payments/api)
