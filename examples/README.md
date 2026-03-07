# nowpayments-py Examples

All examples use sandbox mode. Set environment variables before running.

## Environment Variables

| Variable | Required For | Description |
|----------|--------------|-------------|
| `NOWPAYMENTS_API_KEY` | All | Your API key from [account.nowpayments.io](https://account.nowpayments.io) |
| `EMAIL` | Payout, Subscription, Custody, Conversions | Account email for JWT |
| `PASSWORD` | Payout, Subscription, Custody, Conversions | Account password for JWT |
| `PAYOUT_ADDRESS` | Payout flow | BTC/ETH address for payout |
| `VERIFICATION_CODE` | Payout verify | 2FA code from email |
| `SUB_PARTNER_ID` | Custody | Sub-partner ID for deposit |
| `IPN_SECRET` | IPN webhook | IPN secret from dashboard |

## Run Examples

```bash
# Set API key
export NOWPAYMENTS_API_KEY=your-api-key

# Basic
python examples/basic_usage.py

# Create payment
python examples/01_create_payment.py

# Check payment status (pass payment_id as arg)
python examples/02_check_payment_status.py 12345678

# List payments
python examples/03_list_payments.py

# Create invoice
python examples/04_create_invoice.py

# Estimate & min amount
python examples/05_estimate_and_min_amount.py

# Get currencies
python examples/06_get_currencies.py

# Payout flow (needs EMAIL, PASSWORD, PAYOUT_ADDRESS)
python examples/07_payout_flow.py

# Subscription (needs EMAIL, PASSWORD for create)
python examples/08_subscription.py

# IPN webhook verification
python examples/09_ipn_webhook.py

# Custody & balance (needs EMAIL, PASSWORD, SUB_PARTNER_ID for deposit)
python examples/10_custody_and_balance.py

# Conversions (needs EMAIL, PASSWORD)
python examples/11_conversions.py

# Update payment estimate
python examples/12_update_payment_estimate.py 12345678

# Create invoice payment (needs invoice iid)
python examples/13_create_invoice_payment.py 12345

# Create sub-partner (needs EMAIL, PASSWORD)
python examples/14_create_sub_partner.py

# Payment helpers
python examples/15_payment_helpers.py

# Error handling
python examples/16_error_handling.py
```

## Example Index

| # | File | Description |
|---|------|-------------|
| - | basic_usage.py | Quick start: status, currencies, estimate |
| 01 | 01_create_payment.py | Create payment, get address + amount |
| 02 | 02_check_payment_status.py | Check status with helpers |
| 03 | 03_list_payments.py | List payments with filters |
| 04 | 04_create_invoice.py | Create invoice (redirect URL) |
| 05 | 05_estimate_and_min_amount.py | Price estimate + min amount |
| 06 | 06_get_currencies.py | Currencies, full details, single currency |
| 07 | 07_payout_flow.py | Validate → create → verify payout |
| 08 | 08_subscription.py | Subscription plans + create |
| 09 | 09_ipn_webhook.py | IPN signature verify/create |
| 10 | 10_custody_and_balance.py | Balance, sub-partners, deposit |
| 11 | 11_conversions.py | Create conversion + status |
| 12 | 12_update_payment_estimate.py | Refresh payment estimate |
| 13 | 13_create_invoice_payment.py | Payment for existing invoice |
| 14 | 14_create_sub_partner.py | Create sub-partner account |
| 15 | 15_payment_helpers.py | is_payment_complete, get_status_label, etc. |
| 16 | 16_error_handling.py | NowPaymentsError handling |
