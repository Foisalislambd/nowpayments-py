"""
Example: Update payment estimate (refresh before expiration)
Run: python examples/12_update_payment_estimate.py PAYMENT_ID
Env: NOWPAYMENTS_API_KEY
"""
import os
import sys
from nowpayments import NowPayments

np = NowPayments({"api_key": os.environ.get("NOWPAYMENTS_API_KEY", ""), "sandbox": True})

payment_id = sys.argv[1] if len(sys.argv) > 1 else "PASTE_PAYMENT_ID_HERE"


def main():
    result = np.update_payment_estimate(payment_id)
    print("Updated estimate:")
    print("  Pay amount:", result.get("pay_amount"))
    print("  Expiration:", result.get("expiration_estimate_date"))
    print("  ID:", result.get("id"))


if __name__ == "__main__":
    main()
