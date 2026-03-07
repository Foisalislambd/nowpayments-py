"""
Example: Verify IPN webhook (use in your Flask/FastAPI handler)
Run: python examples/09_ipn_webhook.py

In real app (Flask):
    @app.post("/webhook")
    def webhook():
        sig = request.headers.get("x-nowpayments-sig", "")
        if not verify_ipn_signature(request.get_data(as_text=True), sig, os.environ["IPN_SECRET"]):
            return "", 400
        data = request.json
        if is_payment_complete(data.get("payment_status", "")):
            # Fulfill order
            pass
        return "", 200
"""
import os
from nowpayments import verify_ipn_signature, create_ipn_signature, is_payment_complete

ipn_secret = os.environ.get("IPN_SECRET", "your_ipn_secret")

# Simulated IPN payload (real one comes from NOWPayments POST)
mock_payload = {
    "payment_id": "123",
    "payment_status": "finished",
    "pay_address": "0x...",
    "price_amount": 29.99,
    "price_currency": "usd",
    "pay_amount": 0.001,
    "actually_paid": 0.001,
    "pay_currency": "btc",
    "order_id": "order-1",
}


def main():
    # For demo: create valid signature (in production NOWPayments sends it)
    sig = create_ipn_signature(mock_payload, ipn_secret)

    ok = verify_ipn_signature(mock_payload, sig, ipn_secret)
    print("IPN signature valid?", ok)

    if ok and is_payment_complete(mock_payload.get("payment_status", "")):
        print("Handle: fulfill order", mock_payload.get("order_id"))


if __name__ == "__main__":
    main()
