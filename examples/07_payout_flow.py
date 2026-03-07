"""
Example: Payout flow (validate address → create → verify)
Run: python examples/07_payout_flow.py
Env: NOWPAYMENTS_API_KEY, EMAIL, PASSWORD, PAYOUT_ADDRESS, VERIFICATION_CODE (optional)
"""
import os
from nowpayments import NowPayments

np = NowPayments({"api_key": os.environ.get("NOWPAYMENTS_API_KEY", ""), "sandbox": True})

PAY_CURRENCY = "btc"
PAYOUT_ADDRESS = os.environ.get("PAYOUT_ADDRESS", "PASTE_BTC_ADDRESS_HERE")


def main():
    # 1. Validate payout address
    valid = np.validate_payout_address({"address": PAYOUT_ADDRESS, "currency": PAY_CURRENCY})
    print("Address valid?", valid)

    # 2. Get JWT (payouts require auth)
    email = os.environ.get("EMAIL")
    password = os.environ.get("PASSWORD")
    if not email or not password:
        print("Set EMAIL and PASSWORD to create payout")
        return

    auth = np.get_auth_token(email, password)
    token = auth["token"]

    # 3. Create payout
    payout = np.create_payout(
        params={
            "withdrawals": [
                {"address": PAYOUT_ADDRESS, "currency": PAY_CURRENCY, "amount": 0.0001}
            ],
            "ipn_callback_url": "https://yoursite.com/payout-webhook",
        },
        jwt_token=token,
    )

    print("Payout created:", payout.get("id"))
    withdrawals = payout.get("withdrawals", [])
    batch_id = withdrawals[0].get("batch_withdrawal_id", payout.get("id")) if withdrawals else payout.get("id")
    print("Batch withdrawal ID:", batch_id)

    # 4. Verify (requires verification_code from email)
    code = os.environ.get("VERIFICATION_CODE")
    if code:
        verified = np.verify_payout(payout["id"], code, token)
        print("Verified:", verified)
    else:
        print("Set VERIFICATION_CODE env to verify payout")


if __name__ == "__main__":
    main()
