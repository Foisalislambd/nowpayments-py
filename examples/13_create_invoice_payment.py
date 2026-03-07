"""
Example: Create payment for existing invoice
Run: python examples/13_create_invoice_payment.py INVOICE_ID
Env: NOWPAYMENTS_API_KEY
"""
import os
import sys
from nowpayments import NowPayments

np = NowPayments({"api_key": os.environ.get("NOWPAYMENTS_API_KEY", ""), "sandbox": True})

invoice_id = sys.argv[1] if len(sys.argv) > 1 else "PASTE_INVOICE_ID_HERE"


def main():
    payment = np.create_invoice_payment({
        "iid": invoice_id,
        "pay_currency": "btc",
        "order_description": "Payment for invoice",
    })
    print("Payment created for invoice!")
    print("  Pay:", payment.get("pay_amount"), payment.get("pay_currency", "").upper())
    print("  Address:", payment.get("pay_address"))
    print("  Payment ID:", payment.get("payment_id"))


if __name__ == "__main__":
    main()
