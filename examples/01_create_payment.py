"""
Example: Create a payment
Run: python examples/01_create_payment.py
Env: NOWPAYMENTS_API_KEY
"""
import os
import time
from nowpayments import NowPayments

np = NowPayments({"api_key": os.environ.get("NOWPAYMENTS_API_KEY", ""), "sandbox": True})


def main():
    payment = np.create_payment({
        "price_amount": 29.99,
        "price_currency": "usd",
        "pay_currency": "btc",
        "order_id": "order-" + str(int(time.time())),
        "order_description": "Premium Plan",
        "ipn_callback_url": "https://yoursite.com/webhook",
    })

    print("Payment created!")
    print("Pay:", payment["pay_amount"], payment["pay_currency"].upper())
    print("Address:", payment["pay_address"])
    print("Payment ID:", payment["payment_id"])


if __name__ == "__main__":
    main()
