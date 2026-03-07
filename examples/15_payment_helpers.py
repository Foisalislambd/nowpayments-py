"""
Example: Payment status helpers (is_payment_complete, get_status_label, etc.)
Run: python examples/15_payment_helpers.py
"""
from nowpayments import (
    is_payment_complete,
    is_payment_pending,
    get_status_label,
    get_payment_summary,
    PAYMENT_STATUS_LABELS,
    PAYMENT_STATUSES,
    PAYMENT_DONE_STATUSES,
    PAYMENT_PENDING_STATUSES,
)


def main():
    # All statuses
    print("All statuses:", list(PAYMENT_STATUSES))
    print("Done statuses:", list(PAYMENT_DONE_STATUSES))
    print("Pending statuses:", list(PAYMENT_PENDING_STATUSES))
    print()

    # Labels
    for status in ["waiting", "finished", "failed"]:
        print(f"  {status} -> {get_status_label(status)}")
    print()

    # Check helpers
    print("is_payment_complete('finished'):", is_payment_complete("finished"))
    print("is_payment_complete('waiting'):", is_payment_complete("waiting"))
    print("is_payment_pending('waiting'):", is_payment_pending("waiting"))
    print("is_payment_pending('finished'):", is_payment_pending("finished"))
    print()

    # Summary
    mock_payment = {
        "pay_amount": 0.001,
        "pay_currency": "btc",
        "pay_address": "bc1q...",
        "payment_status": "waiting",
    }
    print("get_payment_summary:", get_payment_summary(mock_payment))
    print()
    print("PAYMENT_STATUS_LABELS:", PAYMENT_STATUS_LABELS)


if __name__ == "__main__":
    main()
