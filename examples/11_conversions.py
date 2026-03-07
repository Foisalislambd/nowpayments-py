"""
Example: Create conversion (custody) and check status
Run: python examples/11_conversions.py
Env: NOWPAYMENTS_API_KEY, EMAIL, PASSWORD (JWT required)
"""
import os
from nowpayments import NowPayments

np = NowPayments({"api_key": os.environ.get("NOWPAYMENTS_API_KEY", ""), "sandbox": True})


def main():
    email = os.environ.get("EMAIL")
    password = os.environ.get("PASSWORD")
    if not email or not password:
        print("Set EMAIL and PASSWORD (conversions require JWT)")
        return

    auth = np.get_auth_token(email, password)
    token = auth["token"]

    conv = np.create_conversion(
        params={"amount": 0.001, "from_currency": "btc", "to_currency": "usd"},
        jwt_token=token,
    )

    print("Conversion:", conv)
    deposit_id = conv.get("deposit_id")
    if deposit_id:
        status = np.get_conversion_status(deposit_id, token)
        print("Status:", status)


if __name__ == "__main__":
    main()
