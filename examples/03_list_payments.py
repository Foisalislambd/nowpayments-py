"""
Example: List payments with filters
Run: python examples/03_list_payments.py
Env: NOWPAYMENTS_API_KEY
"""
import os
from nowpayments import NowPayments

np = NowPayments({"api_key": os.environ.get("NOWPAYMENTS_API_KEY", ""), "sandbox": True})


def main():
    result = np.get_payments({
        "limit": 5,
        "page": 0,
        "sortBy": "created_at",
        "orderBy": "desc",
        "dateFrom": "2024-01-01",
        "dateTo": "2024-12-31",
    })

    print("Total:", result["total"])
    print("Page:", result["page"] + 1, "of", result["pagesCount"])
    print("\nPayments:")
    for i, p in enumerate(result.get("data", []), 1):
        print(f"{i}. {p['payment_id']} | {p['payment_status']} | {p['price_amount']} {p['price_currency']}")


if __name__ == "__main__":
    main()
