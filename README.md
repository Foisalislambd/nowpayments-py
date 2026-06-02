# nowpayments-py

<p align="center">
  <strong>Full-featured Python SDK for NOWPayments Cryptocurrency Payment API</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/nowpayments-py/"><img src="https://img.shields.io/badge/pypi-nowpayments--py-blue" alt="PyPI"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.8+-green" alt="Python"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-yellow" alt="License"></a>
</p>

---

Python port of [nowpayments-node](https://github.com/Foisalislambd/nowpayments-node). Accept Bitcoin, Ethereum, USDT, and 300+ cryptocurrencies via [NOWPayments](https://nowpayments.io).

**API Docs:** [Postman](https://documenter.getpostman.com/view/7907941/2s93JusNJt)

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [API Reference (All Methods)](#api-reference-all-methods)
- [JWT Authentication](#jwt-authentication)
- [IPN Webhook](#ipn-webhook)
- [Payment Helpers](#payment-helpers)
- [Exports](#exports)
- [Upgrade Guide](#upgrade-guide)
- [License](#license)

---

## Installation

```bash
pip install nowpayments-py
```

**From source (editable):**

```bash
git clone https://github.com/Foisalislambd/nowpayments-py.git
cd nowpayments-py
pip install -e .
```

---

## Quick Start

```python
from nowpayments import NowPayments

np = NowPayments(api_key="YOUR_API_KEY", sandbox=True)

# Check API status
status = np.get_status()
print(status)

# Create payment
payment = np.create_payment({
    "price_amount": 29.99,
    "price_currency": "usd",
    "pay_currency": "btc",
    "order_id": "order-123",
})
print(f"Pay {payment['pay_amount']} BTC to {payment['pay_address']}")

# Check status
p = np.get_payment_status(payment["payment_id"])
print(p["payment_status"])
```

---

## Configuration

```python
np = NowPayments(
    api_key="YOUR_API_KEY",      # Required
    sandbox=True,                # Use sandbox (api-sandbox.nowpayments.io)
    base_url=None,               # Override base URL (overrides sandbox)
    timeout=30000,               # Request timeout in ms
    ipn_secret="YOUR_IPN_SECRET" # For webhook verification
)
```

**Config keys:** `api_key` or `apiKey`, `ipn_secret` or `ipnSecret` (both styles supported).

---

## API Reference (All Methods)

### Status & Auth

| Method | Description | JWT |
|--------|-------------|-----|
| `get_status()` | Check if API is up | No |
| `get_auth_token(email, password)` | Get JWT (expires ~5 min) | No |

### Currencies

| Method | Description | JWT |
|--------|-------------|-----|
| `get_currencies(fixed_rate=None)` | List available currencies (btc, eth, usdt...) | No |
| `get_full_currencies()` | Full currency details (network, regex, etc.) | No |
| `get_merchant_coins(fixed_rate=None)` | Merchant enabled currencies | No |
| `get_currency(currency)` | Single currency details | No |

### Price & Estimate

| Method | Description | JWT |
|--------|-------------|-----|
| `get_estimate_price(params)` | Estimate crypto amount for fiat | No |
| `get_min_amount(params)` | Min payment amount for pair | No |

### Payments

| Method | Description | JWT |
|--------|-------------|-----|
| `create_payment(params)` | Create payment, get address + amount | No |
| `get_payment_status(payment_id)` | Get payment by ID | No |
| `get_payments(params=None, jwt_token=None)` | Paginated list of payments | JWT recommended |
| `update_payment_estimate(payment_id)` | Refresh estimate before expiry | No |

### Invoices

| Method | Description | JWT |
|--------|-------------|-----|
| `create_invoice(params)` | Create invoice (redirect flow) | No |
| `create_invoice_payment(params)` | Create payment for existing invoice | No |

### Subscriptions

| Method | Description | JWT |
|--------|-------------|-----|
| `get_subscription_plans(params=None)` | List subscription plans | No |
| `get_subscription_plan(id)` | Get single plan | No |
| `update_subscription_plan(id, updates)` | Update plan | No |
| `get_subscriptions(params=None)` | List recurring payments | No |
| `get_subscription(id)` | Get single subscription | No |
| `create_subscription(params, jwt_token)` | Create subscription | Yes |
| `delete_subscription(id, jwt_token=None)` | Cancel subscription | Optional |

### Payouts

| Method | Description | JWT |
|--------|-------------|-----|
| `validate_payout_address(params)` | Validate address before payout | No |
| `create_payout(params, jwt_token)` | Mass payout | Yes |
| `verify_payout(payout_id, code, jwt_token)` | Verify with 2FA | Yes |
| `get_payout_status(payout_id, jwt_token=None)` | Get payout status | Optional |
| `get_payouts(params=None)` | List payouts | No |
| `cancel_payout(payout_id, jwt_token)` | Cancel scheduled payout | Yes |

### Fiat Payouts

| Method | Description | JWT |
|--------|-------------|-----|
| `get_fiat_payouts_crypto_currencies(params=None, jwt_token=None)` | Crypto options for fiat cashout | Optional |
| `get_fiat_payouts_payment_methods(params=None, jwt_token=None)` | Payment methods | Optional |
| `get_fiat_payouts(params=None, jwt_token=None)` | List fiat payouts | Optional |

### Balance

| Method | Description | JWT |
|--------|-------------|-----|
| `get_balance(jwt_token=None)` | Custody balance | Optional |

### Sub-Partners (Custody)

| Method | Description | JWT |
|--------|-------------|-----|
| `create_sub_partner(name, jwt_token)` | Create sub-partner account | Yes |
| `create_sub_partner_payment(params, jwt_token)` | Deposit to sub-partner via payment | Yes |
| `get_sub_partners(params=None, jwt_token=None)` | List sub-partners | Optional |
| `get_sub_partner_balance(sub_partner_id)` | Get balance | No |
| `create_transfer(params, jwt_token)` | Transfer between accounts | Yes |
| `deposit(params, jwt_token)` | Deposit from master to user | Yes |
| `write_off(params, jwt_token)` | Write off to master | JWT required |
| `get_transfers(params=None, jwt_token=None)` | List transfers | Optional |
| `get_transfer(id, jwt_token=None)` | Get single transfer | Optional |

### Conversions

| Method | Description | JWT |
|--------|-------------|-----|
| `create_conversion(params, jwt_token)` | Convert within custody | Yes |
| `get_conversion_status(conversion_id, jwt_token)` | Get conversion status | Yes |
| `get_conversions(params=None, jwt_token=None)` | List conversions | Optional |

### IPN

| Method | Description |
|--------|-------------|
| `verify_ipn(payload, signature)` | Verify webhook (uses config ipn_secret) |

**Total: 44 methods**

---

## JWT Authentication

Payouts, custody, and some subscription actions require JWT. Token expires in ~5 minutes.

```python
auth = np.get_auth_token(email="your@email.com", password="your_password")
token = auth["token"]

# Create payout
result = np.create_payout(
    params={
        "withdrawals": [
            {"address": "bc1q...", "currency": "btc", "amount": 0.001}
        ]
    },
    jwt_token=token,
)
```

---

## IPN Webhook

Verify webhook signature from `x-nowpayments-sig` header:

```python
from nowpayments import NowPayments, verify_ipn_signature, create_ipn_signature

# With client (uses ipn_secret from config)
np = NowPayments(api_key="...", ipn_secret="YOUR_IPN_SECRET")
if np.verify_ipn(request_body, request_headers.get("x-nowpayments-sig")):
    # Valid webhook
    process_payment(request_body)

# Standalone
if verify_ipn_signature(payload, signature, ipn_secret):
    # Valid
    pass

# Create signature (for testing)
sig = create_ipn_signature(payload_dict, ipn_secret)
```

---

## Payment Helpers

```python
from nowpayments import (
    is_payment_complete,
    is_payment_pending,
    get_status_label,
    get_payment_summary,
    PAYMENT_STATUS_LABELS,
    PAYMENT_STATUSES,
    PAYMENT_DONE_STATUSES,
    PAYMENT_PENDING_STATUSES,
)

status = payment["payment_status"]
if is_payment_complete(status):
    print("Done")  # finished, failed, refunded, expired
if is_payment_pending(status):
    print("Awaiting payment")  # waiting, confirming, etc.

label = get_status_label(status)  # "Awaiting payment", "Completed", etc.
summary = get_payment_summary(payment)  # "Awaiting payment: 0.001 BTC → bc1q..."
```

---

## Exports

```python
from nowpayments import (
    NowPayments,           # Main client
    NowPaymentsError,      # API error (message, status_code, code, response)
    verify_ipn_signature,  # IPN verification
    create_ipn_signature,  # IPN signature for tests
    is_payment_complete,
    is_payment_pending,
    get_status_label,
    get_payment_summary,
    PAYMENT_STATUS_LABELS,
    PAYMENT_STATUSES,
    PAYMENT_DONE_STATUSES,
    PAYMENT_PENDING_STATUSES,
)
```

---

## Upgrade Guide

### From 1.0.x to 1.0.y (patch)

No breaking changes. Update:

```bash
pip install --upgrade nowpayments-py
```

### Config keys

- `api_key` or `apiKey` — both work
- `ipn_secret` or `ipnSecret` — both work

### Error handling

```python
from nowpayments import NowPayments, NowPaymentsError

try:
    payment = np.create_payment(...)
except NowPaymentsError as e:
    print(e.message, e.status_code, e.code)
```

---

## License

MIT © [Foisalislambd](https://github.com/Foisalislambd)
