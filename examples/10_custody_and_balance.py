"""
Example: Balance + custody (sub-partner, deposit with payment, transfer)
Run: python examples/10_custody_and_balance.py
Env: NOWPAYMENTS_API_KEY, EMAIL, PASSWORD, SUB_PARTNER_ID (for create_sub_partner_payment)
"""
import os
from nowpayments import NowPayments

np = NowPayments({"api_key": os.environ.get("NOWPAYMENTS_API_KEY", ""), "sandbox": True})


def main():
    # Balance
    balance = np.get_balance()
    print("Balance:", balance)

    # Sub-partners (if using custody)
    partners = np.get_sub_partners()
    print("Sub-partners:", partners)

    # Deposit with payment – top up sub-partner via crypto (requires JWT)
    email = os.environ.get("EMAIL")
    password = os.environ.get("PASSWORD")
    sub_partner_id = os.environ.get("SUB_PARTNER_ID")

    if email and password and sub_partner_id:
        auth = np.get_auth_token(email, password)
        token = auth["token"]
        result = np.create_sub_partner_payment(
            params={"currency": "trx", "amount": 50, "sub_partner_id": sub_partner_id},
            jwt_token=token,
        )
        res = result.get("result", {})
        print("Deposit payment:", res.get("pay_address"), res.get("pay_amount"), res.get("pay_currency"))
    else:
        print("Set EMAIL, PASSWORD, SUB_PARTNER_ID for create_sub_partner_payment")


if __name__ == "__main__":
    main()
