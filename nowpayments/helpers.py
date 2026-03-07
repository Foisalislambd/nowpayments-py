"""
Human-friendly helpers for payment status and display.
"""

from typing import TYPE_CHECKING

from .types import (
    PAYMENT_DONE_STATUSES,
    PAYMENT_PENDING_STATUSES,
)

if TYPE_CHECKING:
    from .types import Payment, PaymentStatus

# User-friendly labels for payment statuses
PAYMENT_STATUS_LABELS: dict[str, str] = {
    "waiting": "Awaiting payment",
    "confirming": "Confirming",
    "confirmed": "Confirmed",
    "spending": "Processing",
    "sending": "Sending to wallet",
    "partially_paid": "Partially paid",
    "finished": "Completed",
    "failed": "Failed",
    "refunded": "Refunded",
    "expired": "Expired",
}


def is_payment_complete(status: str) -> bool:
    """Check if payment is complete (success or terminal state)."""
    return status in PAYMENT_DONE_STATUSES


def is_payment_pending(status: str) -> bool:
    """Check if payment is still pending (customer should pay)."""
    return status in PAYMENT_PENDING_STATUSES


def get_status_label(status: str) -> str:
    """Get human-readable status label."""
    return PAYMENT_STATUS_LABELS.get(status, status)


def get_payment_summary(payment: "Payment") -> str:
    """Build a short summary for displaying to users."""
    pay_amount = payment.get("pay_amount", 0)
    pay_currency = payment.get("pay_currency", "")
    pay_address = payment.get("pay_address", "")
    payment_status = payment.get("payment_status", "")
    label = PAYMENT_STATUS_LABELS.get(payment_status, payment_status)
    curr = (pay_currency or "").upper()
    return f"{label}: {pay_amount} {curr} -> {pay_address or '...'}"
