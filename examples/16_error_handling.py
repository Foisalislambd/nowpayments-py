"""
Example: Error handling with NowPaymentsError
Run: python examples/16_error_handling.py
"""
import os
from nowpayments import NowPayments, NowPaymentsError

np = NowPayments({"api_key": os.environ.get("NOWPAYMENTS_API_KEY", ""), "sandbox": True})


def main():
    try:
        # Invalid payment ID
        np.get_payment_status("invalid-id-999999")
    except NowPaymentsError as e:
        print("Caught NowPaymentsError:")
        print("  Message:", e.message)
        print("  Status code:", e.status_code)
        print("  Code:", e.code)
        print("  str(e):", str(e))

    try:
        # Missing required params
        np.create_payment({"price_amount": 10})  # missing pay_currency, etc.
    except NowPaymentsError as e:
        print("\nAPI Error:", e.message)


if __name__ == "__main__":
    main()
