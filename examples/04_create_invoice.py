"""
Example: Create invoice (redirect customer to URL)
Run: python examples/04_create_invoice.py
Env: NOWPAYMENTS_API_KEY
"""
import os
import time
from nowpayments import NowPayments

np = NowPayments({"api_key": os.environ.get("NOWPAYMENTS_API_KEY", ""), "sandbox": True})


def main():
    invoice = np.create_invoice({
        "price_amount": 49.99,
        "price_currency": "usd",
        "pay_currency": "btc",
        "order_id": "inv-" + str(int(time.time())),
        "order_description": "Premium subscription",
        "success_url": "https://yoursite.com/success",
        "cancel_url": "https://yoursite.com/cancel",
    })

    print("Invoice created!")
    print("Redirect customer to:", invoice["invoice_url"])


if __name__ == "__main__":
    main()
