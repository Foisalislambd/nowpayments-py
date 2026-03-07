"""
Example: Check payment status + show friendly message
Run: python examples/02_check_payment_status.py [PAYMENT_ID]
Env: NOWPAYMENTS_API_KEY
"""
import os
import sys
from nowpayments import NowPayments, get_status_label, is_payment_complete

np = NowPayments({"api_key": os.environ.get("NOWPAYMENTS_API_KEY", ""), "sandbox": True})

payment_id = sys.argv[1] if len(sys.argv) > 1 else "PASTE_PAYMENT_ID_HERE"


def main():
    payment = np.get_payment_status(payment_id)

    print("Status:", get_status_label(payment["payment_status"]))
    print("Amount:", payment["pay_amount"], payment["pay_currency"])
    print("Paid:", payment.get("actually_paid", 0))

    if is_payment_complete(payment["payment_status"]):
        print("\n✅ Payment done! Fulfill the order.")
    else:
        print("\n⏳ Waiting for payment...")


if __name__ == "__main__":
    main()
