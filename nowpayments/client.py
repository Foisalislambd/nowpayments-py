"""
NOWPayments Python SDK
Full-featured client for the NOWPayments cryptocurrency payment API.

@see https://documenter.getpostman.com/view/7907941/2s93JusNJt
"""

from typing import Any, Optional

from .http import create_http_client, NowPaymentsError, _get_api_key
from .ipn import verify_ipn_signature
from .types import (
    NowPaymentsConfig,
    CreatePaymentParams,
    CreateInvoiceParams,
    CreateInvoicePaymentParams,
    CreatePayoutParams,
    ValidateAddressParams,
    CreateSubPartnerPaymentParams,
    ListPaymentsParams,
    EstimateParams,
    MinAmountParams,
    GetSubscriptionPlansParams,
    GetSubscriptionsParams,
    GetFiatPayoutsParams,
)


class NowPayments:
    """Main NOWPayments API client."""

    def __init__(self, config: NowPaymentsConfig) -> None:
        _get_api_key(config)  # Validates api_key or apiKey
        self._config = config
        self._client = create_http_client(config)

    def get_status(self) -> dict[str, Any]:
        """Check if API is up and available."""
        r = self._client.get("/v1/status")
        return r.json()

    def get_currencies(self, fixed_rate: Optional[bool] = None) -> dict[str, list[str]]:
        """Get list of available crypto currencies (e.g. btc, eth, usdt)."""
        params = {}
        if fixed_rate is not None:
            params["fixed_rate"] = fixed_rate
        r = self._client.get("/v1/currencies", params=params)
        return r.json()

    def get_full_currencies(self) -> dict[str, list[dict[str, Any]]]:
        """Get full currency details (id, code, name, wallet_regex, network, etc.)."""
        r = self._client.get("/v1/full-currencies")
        return r.json()

    def get_merchant_coins(self, fixed_rate: Optional[bool] = None) -> dict[str, list[str]]:
        """Get merchant checked currencies (from coins settings)."""
        params = {}
        if fixed_rate is not None:
            params["fixed_rate"] = fixed_rate
        r = self._client.get("/v1/merchant/coins", params=params)
        return r.json()

    def get_auth_token(self, email: str, password: str) -> dict[str, str]:
        """
        Get JWT token (required for payouts, custody, etc.).
        Token expires in 5 minutes. Never log email/password.
        """
        r = self._client.post("/v1/auth", json={"email": email, "password": password})
        return r.json()

    def get_currency(self, currency: str) -> dict[str, Any]:
        """Get single currency details (limits, etc.)."""
        code = currency.strip() if currency else ""
        if not code:
            raise ValueError('Currency code is required (e.g. "btc", "eth")')
        from urllib.parse import quote

        r = self._client.get(f"/v1/currencies/{quote(str(code), safe='')}")
        return r.json()

    def get_estimate_price(self, params: EstimateParams) -> dict[str, Any]:
        """Get estimated price in crypto for a fiat amount."""
        r = self._client.get(
            "/v1/estimate",
            params={
                "amount": params["amount"],
                "currency_from": params["currency_from"],
                "currency_to": params["currency_to"],
            },
        )
        return r.json()

    def get_min_amount(self, params: MinAmountParams) -> dict[str, Any]:
        """Get minimum payment amount for currency pair."""
        query: dict[str, Any] = {
            "currency_from": params["currency_from"],
            "currency_to": params["currency_to"],
        }
        if params.get("fiat_equivalent") is not None:
            query["fiat_equivalent"] = params["fiat_equivalent"]
        if params.get("is_fixed_rate") is not None:
            query["is_fixed_rate"] = params["is_fixed_rate"]
        if params.get("is_fee_paid_by_user") is not None:
            query["is_fee_paid_by_user"] = params["is_fee_paid_by_user"]
        r = self._client.get("/v1/min-amount", params=query)
        return r.json()

    def create_payment(self, params: CreatePaymentParams) -> dict[str, Any]:
        """
        Create a new payment. Returns address + amount for customer to pay.
        """
        body = dict(params)
        if body.get("fixed_rate") is not None and body.get("is_fixed_rate") is None:
            body["is_fixed_rate"] = body.pop("fixed_rate")
        r = self._client.post("/v1/payment", json=body)
        return r.json()

    def get_payment_status(self, payment_id: int | str) -> dict[str, Any]:
        """Get payment status by ID."""
        if payment_id is None or str(payment_id).strip() == "":
            raise ValueError("Payment ID is required")
        r = self._client.get(f"/v1/payment/{payment_id}")
        return r.json()

    def get_payments(
        self,
        params: Optional[ListPaymentsParams] = None,
        jwt_token: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get paginated list of payments. JWT recommended per API docs."""
        headers = {}
        if jwt_token:
            headers["Authorization"] = f"Bearer {jwt_token}"
        r = self._client.get("/v1/payment/", params=params or {}, headers=headers)
        return r.json()

    def update_payment_estimate(self, payment_id: int | str) -> dict[str, Any]:
        """Update payment estimate (call before expiration)."""
        r = self._client.post(f"/v1/payment/{payment_id}/update-merchant-estimate")
        return r.json()

    def create_invoice(self, params: CreateInvoiceParams) -> dict[str, Any]:
        """Create an invoice (redirect flow)."""
        r = self._client.post("/v1/invoice", json=params)
        return r.json()

    def create_invoice_payment(self, params: CreateInvoicePaymentParams) -> dict[str, Any]:
        """Create payment for existing invoice."""
        r = self._client.post("/v1/invoice-payment", json=params)
        return r.json()

    # --- Recurring Payments (Subscriptions) ---

    def get_subscriptions(
        self, params: Optional[GetSubscriptionsParams] = None
    ) -> dict[str, Any]:
        """List all recurring payments."""
        r = self._client.get("/v1/subscriptions", params=params or {})
        return r.json()

    def get_subscription(self, id: str) -> dict[str, Any]:
        """Get single recurring payment."""
        r = self._client.get(f"/v1/subscriptions/{id}")
        return r.json()

    def delete_subscription(
        self, id: str, jwt_token: Optional[str] = None
    ) -> dict[str, Any]:
        """Cancel recurring payment. JWT required per API docs."""
        headers = {}
        if jwt_token:
            headers["Authorization"] = f"Bearer {jwt_token}"
        r = self._client.delete(f"/v1/subscriptions/{id}", headers=headers)
        return r.json()

    def get_subscription_plans(
        self, params: Optional[GetSubscriptionPlansParams] = None
    ) -> dict[str, Any]:
        """List subscription plans."""
        r = self._client.get("/v1/subscriptions/plans", params=params or {})
        return r.json()

    def get_subscription_plan(self, id: str) -> dict[str, Any]:
        """Get single subscription plan."""
        r = self._client.get(f"/v1/subscriptions/plans/{id}")
        return r.json()

    def update_subscription_plan(
        self, id: str, updates: dict[str, Any]
    ) -> dict[str, Any]:
        """Update subscription plan."""
        r = self._client.patch(f"/v1/subscriptions/plans/{id}", json=updates)
        return r.json()

    # --- Sub-Partner / Customer Management ---

    def get_sub_partners(
        self,
        params: Optional[dict[str, Any]] = None,
        jwt_token: Optional[str] = None,
    ) -> dict[str, Any]:
        """List sub-partners (users). JWT required for custody API."""
        headers = {}
        if jwt_token:
            headers["Authorization"] = f"Bearer {jwt_token}"
        r = self._client.get("/v1/sub-partner", params=params or {}, headers=headers)
        return r.json()

    def get_sub_partner_balance(self, sub_partner_id: str) -> dict[str, Any]:
        """Get sub-partner balance."""
        r = self._client.get(f"/v1/sub-partner/balance/{sub_partner_id}")
        return r.json()

    def get_transfers(
        self,
        params: Optional[dict[str, Any]] = None,
        jwt_token: Optional[str] = None,
    ) -> dict[str, Any]:
        """List transfers. JWT required for custody."""
        headers = {}
        if jwt_token:
            headers["Authorization"] = f"Bearer {jwt_token}"
        r = self._client.get(
            "/v1/sub-partner/transfers", params=params or {}, headers=headers
        )
        return r.json()

    def get_transfer(
        self, id: str, jwt_token: Optional[str] = None
    ) -> dict[str, Any]:
        """Get single transfer. JWT required for custody."""
        headers = {}
        if jwt_token:
            headers["Authorization"] = f"Bearer {jwt_token}"
        r = self._client.get(
            f"/v1/sub-partner/transfer/{id}", headers=headers
        )
        return r.json()

    # --- Payouts ---

    def create_payout(
        self, params: CreatePayoutParams, jwt_token: str
    ) -> dict[str, Any]:
        """Create mass payout. Requires JWT (call get_auth_token first)."""
        if not jwt_token or not str(jwt_token).strip():
            raise ValueError(
                "JWT token is required for create_payout. Call get_auth_token first."
            )
        r = self._client.post(
            "/v1/payout",
            json=params,
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        return r.json()

    def verify_payout(
        self, payout_id: str, verification_code: str, jwt_token: str
    ) -> Any:
        """Verify payout with 2FA code. Requires JWT."""
        if not jwt_token or not str(jwt_token).strip():
            raise ValueError(
                "JWT token is required for verify_payout. Call get_auth_token first."
            )
        r = self._client.post(
            f"/v1/payout/{payout_id}/verify",
            json={"verification_code": verification_code},
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        return r.json()

    def get_payout_status(
        self, payout_id: str, jwt_token: Optional[str] = None
    ) -> dict[str, Any]:
        """Get payout status."""
        headers = {}
        if jwt_token:
            headers["Authorization"] = f"Bearer {jwt_token}"
        r = self._client.get(f"/v1/payout/{payout_id}", headers=headers)
        return r.json()

    def get_payouts(
        self,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """List payouts."""
        r = self._client.get("/v1/payout", params=params or {})
        return r.json()

    def validate_payout_address(self, params: ValidateAddressParams) -> dict[str, Any]:
        """Validate payout address before creating payout."""
        r = self._client.post("/v1/payout/validate-address", json=params)
        return r.json()

    def get_payout_fee(self, currency: str, amount: float) -> dict[str, Any]:
        """Estimate network fee for a payout."""
        if not currency or not str(currency).strip():
            raise ValueError('Currency is required (e.g. "btc", "eth")')
        if amount is None:
            raise ValueError("Amount is required")
        r = self._client.get(
            "/v1/payout/fee",
            params={"currency": currency, "amount": amount},
        )
        return r.json()

    def cancel_payout(self, payout_id: str, jwt_token: str) -> None:
        """Cancel a scheduled payout. Requires JWT."""
        if not jwt_token or not str(jwt_token).strip():
            raise ValueError(
                "JWT token is required for cancel_payout. Call get_auth_token first."
            )
        self._client.post(
            "/v1/payout/w_id/cancel",
            json={"payout_id": payout_id},
            headers={"Authorization": f"Bearer {jwt_token}"},
        )

    # --- Fiat Payouts ---

    def get_fiat_payouts_crypto_currencies(
        self,
        params: Optional[dict[str, str]] = None,
        jwt_token: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get crypto currencies available for fiat cashout. Requires JWT."""
        headers = {}
        if jwt_token:
            headers["Authorization"] = f"Bearer {jwt_token}"
        r = self._client.get(
            "/v1/fiat-payouts/crypto-currencies",
            params=params or {},
            headers=headers,
        )
        return r.json()

    def get_fiat_payouts_payment_methods(
        self,
        params: Optional[dict[str, str]] = None,
        jwt_token: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get payment methods for fiat payout. Requires JWT."""
        headers = {}
        if jwt_token:
            headers["Authorization"] = f"Bearer {jwt_token}"
        r = self._client.get(
            "/v1/fiat-payouts/payment-methods",
            params=params or {},
            headers=headers,
        )
        return r.json()

    def get_fiat_payouts(
        self,
        params: Optional[GetFiatPayoutsParams] = None,
        jwt_token: Optional[str] = None,
    ) -> dict[str, Any]:
        """List fiat payouts with filters. Requires JWT."""
        headers = {}
        if jwt_token:
            headers["Authorization"] = f"Bearer {jwt_token}"
        r = self._client.get(
            "/v1/fiat-payouts",
            params=params or {},
            headers=headers,
        )
        return r.json()

    def get_balance(self, jwt_token: Optional[str] = None) -> dict[str, Any]:
        """Get custody balance (currencies + amount)."""
        headers = {}
        if jwt_token:
            headers["Authorization"] = f"Bearer {jwt_token}"
        r = self._client.get("/v1/balance", headers=headers)
        return r.json()

    # --- Custody / Sub-Partner (requires JWT) ---

    def create_sub_partner(
        self, name: str, jwt_token: str
    ) -> dict[str, Any]:
        """Create new user account (sub-partner)."""
        if not jwt_token or not str(jwt_token).strip():
            raise ValueError(
                "JWT token is required for create_sub_partner. Call get_auth_token first."
            )
        r = self._client.post(
            "/v1/sub-partner/balance",
            json={"name": name},
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        return r.json()

    def create_sub_partner_payment(
        self, params: CreateSubPartnerPaymentParams, jwt_token: str
    ) -> dict[str, Any]:
        """Deposit with payment – top up a sub-partner's balance via crypto payment."""
        if not jwt_token or not str(jwt_token).strip():
            raise ValueError(
                "JWT token is required for create_sub_partner_payment. Call get_auth_token first."
            )
        body = dict(params)
        if body.get("is_fixed_rate") is not None and body.get("fixed_rate") is None:
            body["fixed_rate"] = body.pop("is_fixed_rate")
        r = self._client.post(
            "/v1/sub-partner/payment",
            json=body,
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        return r.json()

    def create_subscription(
        self,
        params: dict[str, Any],
        jwt_token: str,
    ) -> dict[str, Any]:
        """Create subscription (email or custody). Requires JWT."""
        if not jwt_token or not str(jwt_token).strip():
            raise ValueError(
                "JWT token is required for create_subscription. Call get_auth_token first."
            )
        r = self._client.post(
            "/v1/subscriptions",
            json=params,
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        return r.json()

    def create_transfer(
        self,
        params: dict[str, Any],
        jwt_token: str,
    ) -> dict[str, Any]:
        """Transfer between user accounts. Requires JWT."""
        if not jwt_token or not str(jwt_token).strip():
            raise ValueError(
                "JWT token is required for create_transfer. Call get_auth_token first."
            )
        r = self._client.post(
            "/v1/sub-partner/transfer",
            json=params,
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        return r.json()

    def write_off(self, params: dict[str, Any], jwt_token: str) -> dict[str, Any]:
        """Write off from user to master account. Requires JWT."""
        if not jwt_token or not str(jwt_token).strip():
            raise ValueError(
                "JWT token is required for write_off. Call get_auth_token first."
            )
        r = self._client.post(
            "/v1/sub-partner/write-off",
            json=params,
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        return r.json()

    def deposit(
        self,
        params: dict[str, Any],
        jwt_token: str,
    ) -> dict[str, Any]:
        """Deposit from master to user account. Requires JWT."""
        if not jwt_token or not str(jwt_token).strip():
            raise ValueError(
                "JWT token is required for deposit. Call get_auth_token first."
            )
        r = self._client.post(
            "/v1/sub-partner/deposit",
            json=params,
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        return r.json()

    # --- Conversions (custody, requires JWT) ---

    def create_conversion(
        self,
        params: dict[str, Any],
        jwt_token: str,
    ) -> dict[str, Any]:
        """Create conversion within custody account."""
        if not jwt_token or not str(jwt_token).strip():
            raise ValueError(
                "JWT token is required for create_conversion. Call get_auth_token first."
            )
        r = self._client.post(
            "/v1/conversion",
            json=params,
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        return r.json()

    def get_conversion_status(
        self, conversion_id: str, jwt_token: str
    ) -> dict[str, Any]:
        """Get conversion status."""
        if not jwt_token or not str(jwt_token).strip():
            raise ValueError(
                "JWT token is required for get_conversion_status. Call get_auth_token first."
            )
        r = self._client.get(
            f"/v1/conversion/{conversion_id}",
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        return r.json()

    def get_conversions(
        self,
        params: Optional[dict[str, Any]] = None,
        jwt_token: Optional[str] = None,
    ) -> dict[str, Any]:
        """List conversions."""
        headers = {}
        if jwt_token:
            headers["Authorization"] = f"Bearer {jwt_token}"
        r = self._client.get(
            "/v1/conversion",
            params=params or {},
            headers=headers,
        )
        return r.json()

    def verify_ipn(
        self, payload: str | dict[str, Any], signature: str
    ) -> bool:
        """
        Verify IPN webhook signature. Use ipn_secret in config.
        """
        secret = self._config.get("ipn_secret") or self._config.get("ipnSecret")
        if not secret:
            raise ValueError(
                "IPN secret not configured. Pass ipn_secret in constructor or use "
                "verify_ipn_signature() with explicit secret."
            )
        return verify_ipn_signature(payload, signature, secret)
