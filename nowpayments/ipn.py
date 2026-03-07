"""
IPN (Instant Payment Notification) verification utilities.
Matches official docs: sort keys recursively, then HMAC-SHA512.
@see https://nowpayments.io/help/payments/api
"""

import hmac
import json
import hashlib
from typing import Any


def _sort_object(obj: dict[str, Any]) -> dict[str, Any]:
    """Recursively sort object keys (matches NOWPayments IPN spec)."""
    result: dict[str, Any] = {}
    for key in sorted(obj.keys()):
        val = obj[key]
        if val is not None and isinstance(val, dict) and not isinstance(val, list):
            result[key] = _sort_object(val)
        else:
            result[key] = val
    return result


def verify_ipn_signature(
    payload: str | dict[str, Any],
    signature: str,
    ipn_secret: str,
) -> bool:
    """
    Verify IPN callback signature from NOWPayments.
    Safe to call – handles invalid input gracefully.

    Args:
        payload: Raw request body (string or parsed dict)
        signature: Value from x-nowpayments-sig header
        ipn_secret: Your IPN Secret from Dashboard → Store Settings

    Returns:
        True if signature is valid, False otherwise
    """
    if not signature or not signature.strip() or not ipn_secret or not ipn_secret.strip():
        return False

    try:
        if isinstance(payload, str):
            obj = json.loads(payload)
        elif isinstance(payload, dict):
            obj = payload
        else:
            return False

        sorted_obj = _sort_object(obj)
        json_string = json.dumps(sorted_obj, separators=(",", ":"))

        computed_sig = hmac.new(
            ipn_secret.strip().encode("utf-8"),
            json_string.encode("utf-8"),
            hashlib.sha512,
        ).hexdigest()

        if len(signature) != len(computed_sig):
            return False
        return hmac.compare_digest(signature, computed_sig)
    except (json.JSONDecodeError, TypeError, ValueError):
        return False


def create_ipn_signature(payload: dict[str, Any], ipn_secret: str) -> str:
    """Create IPN signature for testing (e.g., mocking callbacks)."""
    json_string = json.dumps(_sort_object(payload), separators=(",", ":"))
    return hmac.new(
        ipn_secret.strip().encode("utf-8"),
        json_string.encode("utf-8"),
        hashlib.sha512,
    ).hexdigest()
