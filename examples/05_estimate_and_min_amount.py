"""
Example: Get price estimate + minimum amount
Run: python examples/05_estimate_and_min_amount.py
Env: NOWPAYMENTS_API_KEY
"""
import os
from nowpayments import NowPayments

np = NowPayments({"api_key": os.environ.get("NOWPAYMENTS_API_KEY", ""), "sandbox": True})


def main():
    # How much is 100 USD in BTC?
    estimate = np.get_estimate_price({
        "amount": 100,
        "currency_from": "usd",
        "currency_to": "btc",
    })
    print("100 USD ≈", estimate["estimated_amount"], "BTC")

    # Minimum payment for USD → BTC
    min_amt = np.get_min_amount({
        "currency_from": "usd",
        "currency_to": "btc",
        "fiat_equivalent": "usd",
    })
    print("Min amount:", min_amt["min_amount"], "BTC")
    print("(≈", min_amt.get("fiat_equivalent"), "USD)")


if __name__ == "__main__":
    main()
