"""
Example: Create sub-partner (custody user account)
Run: python examples/14_create_sub_partner.py
Env: NOWPAYMENTS_API_KEY, EMAIL, PASSWORD
"""
import os
from nowpayments import NowPayments

np = NowPayments({"api_key": os.environ.get("NOWPAYMENTS_API_KEY", ""), "sandbox": True})


def main():
    email = os.environ.get("EMAIL")
    password = os.environ.get("PASSWORD")
    if not email or not password:
        print("Set EMAIL and PASSWORD env vars")
        return

    token_resp = np.get_auth_token(email, password)
    token = token_resp.get("token")

    result = np.create_sub_partner(name="Customer-001", jwt_token=token)
    print("Sub-partner created:", result.get("result"))


if __name__ == "__main__":
    main()
