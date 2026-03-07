"""
Example: Get available currencies
Run: python examples/06_get_currencies.py
Env: NOWPAYMENTS_API_KEY
"""
import os
from nowpayments import NowPayments

np = NowPayments({"api_key": os.environ.get("NOWPAYMENTS_API_KEY", ""), "sandbox": True})


def main():
    data = np.get_currencies()
    currencies = data.get("currencies", [])
    print("Supported:", ", ".join(currencies[:15]), "...")
    print("Total:", len(currencies))

    # Single currency info
    btc_info = np.get_currency("btc")
    print("\nBTC info:", btc_info)

    # Full currency details (id, name, wallet_regex, network, etc.)
    full_data = np.get_full_currencies()
    full_list = full_data.get("currencies", [])
    btc_full = next((c for c in full_list if (c.get("code") or "").lower() == "btc"), None)
    print("\nBTC full:", btc_full)


if __name__ == "__main__":
    main()
