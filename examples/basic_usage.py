"""
Basic usage example for nowpayments Python SDK.
Run: python examples/basic_usage.py
Env: NOWPAYMENTS_API_KEY
"""

import os
from nowpayments import NowPayments

# Initialize with API key
api_key = os.environ.get("NOWPAYMENTS_API_KEY", "your-api-key-here")
np = NowPayments({"api_key": api_key, "sandbox": True})

# Check API status
status = np.get_status()
print("API Status:", status)

# Get available currencies
currencies = np.get_currencies()
print("Currencies:", currencies.get("currencies", [])[:5], "...")

# Get price estimate (USD to BTC)
estimate = np.get_estimate_price(
    {"amount": 100, "currency_from": "usd", "currency_to": "btc"}
)
print("Estimate (100 USD -> BTC):", estimate)
