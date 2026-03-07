"""
NOWPayments API Type Definitions
"""

from typing import Any, Dict, List, Literal, Optional, TypedDict, Union

# Payment status values – API may return "sending" or "spending"
PaymentStatus = Literal[
    "waiting",
    "confirming",
    "confirmed",
    "spending",
    "sending",
    "partially_paid",
    "finished",
    "failed",
    "refunded",
    "expired",
]

PAYMENT_STATUSES: tuple[PaymentStatus, ...] = (
    "waiting",
    "confirming",
    "confirmed",
    "spending",
    "sending",
    "partially_paid",
    "finished",
    "failed",
    "refunded",
    "expired",
)

PAYMENT_DONE_STATUSES: tuple[PaymentStatus, ...] = (
    "finished",
    "failed",
    "refunded",
    "expired",
)

PAYMENT_PENDING_STATUSES: tuple[PaymentStatus, ...] = (
    "waiting",
    "confirming",
    "confirmed",
    "spending",
    "sending",
    "partially_paid",
)


class NowPaymentsConfig(TypedDict, total=False):
    """Client configuration options. Use api_key or apiKey, ipn_secret or ipnSecret."""

    api_key: str
    apiKey: str  # Alternative to api_key
    sandbox: bool
    base_url: Optional[str]
    timeout: Optional[int]
    ipn_secret: Optional[str]
    ipnSecret: Optional[str]  # Alternative to ipn_secret


class CreatePaymentParams(TypedDict, total=False):
    """Create payment request."""

    price_amount: float
    price_currency: str
    pay_currency: str
    pay_amount: Optional[float]
    ipn_callback_url: Optional[str]
    order_id: Optional[str]
    order_description: Optional[str]
    purchase_id: Optional[str]
    payout_address: Optional[str]
    payout_currency: Optional[str]
    payout_extra_id: Optional[str]
    fixed_rate: Optional[bool]
    is_fixed_rate: Optional[bool]
    is_fee_paid_by_user: Optional[bool]


class CreateInvoiceParams(TypedDict, total=False):
    """Create invoice request."""

    price_amount: float
    price_currency: str
    pay_currency: Optional[str]
    ipn_callback_url: Optional[str]
    order_id: Optional[str]
    order_description: Optional[str]
    success_url: Optional[str]
    cancel_url: Optional[str]
    partially_paid_url: Optional[str]
    is_fixed_rate: Optional[bool]
    is_fee_paid_by_user: Optional[bool]


class FullCurrency(TypedDict, total=False):
    """Full currency details from GET /v1/full-currencies."""

    id: int
    code: str
    name: str
    enable: bool
    wallet_regex: Optional[str]
    priority: Optional[int]
    extra_id_exists: Optional[bool]
    extra_id_regex: Optional[str]
    logo_url: Optional[str]
    track: Optional[bool]
    cg_id: Optional[str]
    is_maxlimit: Optional[bool]
    network: Optional[str]
    smart_contract: Optional[str]
    network_precision: Optional[int]


class FiatPayoutCryptoCurrency(TypedDict):
    """Fiat payout crypto currency option."""

    provider: str
    currencyCode: str
    currencyNetwork: str
    enabled: bool


class FiatPayoutField(TypedDict, total=False):
    """Field for fiat payout payment method."""

    name: str
    type: str
    mandatory: bool
    description: Optional[str]


class FiatPayoutPaymentMethod(TypedDict):
    """Fiat payout payment method."""

    name: str
    paymentCode: str
    fields: List[FiatPayoutField]
    provider: str


class FiatPayoutRecord(TypedDict, total=False):
    """Fiat payout record."""

    id: str
    provider: str
    requestId: str
    status: str
    fiatCurrencyCode: Optional[str]
    fiatAmount: Optional[str]
    cryptoCurrencyCode: Optional[str]
    cryptoCurrencyAmount: Optional[str]
    fiatAccountCode: Optional[str]
    fiatAccountNumber: Optional[str]
    payoutDescription: Optional[str]
    error: Optional[str]
    createdAt: Optional[str]
    updatedAt: Optional[str]


class GetSubscriptionPlansParams(TypedDict, total=False):
    """List subscription plans params."""

    limit: Optional[int]
    offset: Optional[int]


class GetSubscriptionsParams(TypedDict, total=False):
    """List subscriptions params."""

    status: Optional[str]
    subscription_plan_id: Optional[Union[str, int]]
    is_active: Optional[bool]
    limit: Optional[int]
    offset: Optional[int]


class GetFiatPayoutsParams(TypedDict, total=False):
    """List fiat payouts params."""

    id: Optional[str]
    provider: Optional[str]
    requestId: Optional[str]
    fiatCurrency: Optional[str]
    cryptoCurrency: Optional[str]
    status: Optional[str]
    filter: Optional[str]
    provider_payout_id: Optional[str]
    limit: Optional[int]
    page: Optional[int]
    orderBy: Optional[str]
    sortBy: Optional[str]
    dateFrom: Optional[str]
    dateTo: Optional[str]


class Payment(TypedDict, total=False):
    """Payment object from API."""

    payment_id: Union[int, str]
    payment_status: PaymentStatus
    pay_address: str
    pay_amount: float
    pay_currency: str
    price_amount: float
    price_currency: str
    actually_paid: Optional[float]
    outcome_amount: Optional[float]
    outcome_currency: Optional[str]
    order_id: Optional[str]
    order_description: Optional[str]
    purchase_id: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]


class PaymentsListResponse(TypedDict):
    """Paginated payments list."""

    data: List[Payment]
    limit: int
    page: int
    pagesCount: int
    total: int


class EstimatePriceResponse(TypedDict):
    """Estimate price response."""

    amount_from: float
    currency_from: str
    currency_to: str
    estimated_amount: float


class MinAmountResponse(TypedDict, total=False):
    """Minimum amount response."""

    currency_from: str
    currency_to: str
    min_amount: float
    fiat_equivalent: Optional[float]


class ListPaymentsParams(TypedDict, total=False):
    """List payments query params."""

    limit: Optional[int]
    page: Optional[int]
    sortBy: Optional[str]
    orderBy: Optional[Literal["asc", "desc"]]
    dateFrom: Optional[str]
    dateTo: Optional[str]


class EstimateParams(TypedDict):
    """Get estimate params."""

    amount: float
    currency_from: str
    currency_to: str


class MinAmountParams(TypedDict, total=False):
    """Get min amount params."""

    currency_from: str
    currency_to: str
    fiat_equivalent: Optional[Union[str, bool]]
    is_fixed_rate: Optional[bool]
    is_fee_paid_by_user: Optional[bool]


class InvoiceResponse(TypedDict, total=False):
    """Invoice response."""

    id: str
    invoice_id: Optional[str]
    invoice_url: str
    price_amount: float
    price_currency: str
    pay_currency: Optional[str]
    order_id: Optional[str]
    order_description: Optional[str]


class SubscriptionPlan(TypedDict, total=False):
    """Subscription plan."""

    id: str
    amount: float
    currency: str
    interval_day: str
    title: str
    created_at: Optional[str]
    updated_at: Optional[str]


class RecurringPayment(TypedDict, total=False):
    """Recurring payment/subscription."""

    id: str
    subscription_plan_id: str
    status: str
    is_active: bool
    created_at: Optional[str]
    updated_at: Optional[str]
    expire_date: Optional[str]
    subscriber: Optional[Dict[str, Any]]


class SubPartnerBalance(TypedDict):
    """Sub-partner balance."""

    subPartnerId: str
    balances: Dict[str, Dict[str, float]]


class PayoutWithdrawal(TypedDict, total=False):
    """Payout withdrawal item for createPayout."""

    address: str
    currency: str
    amount: float
    extra_id: Optional[str]
    ipn_callback_url: Optional[str]
    payout_description: Optional[str]
    unique_external_id: Optional[str]
    fiat_amount: Optional[float]
    fiat_currency: Optional[str]
    execute_at: Optional[str]


class CreatePayoutParams(TypedDict, total=False):
    """Create payout request body."""

    ipn_callback_url: Optional[str]
    payout_description: Optional[str]
    withdrawals: List[PayoutWithdrawal]


class PayoutWithdrawalResponse(TypedDict, total=False):
    """Single withdrawal in create payout response."""

    id: str
    address: str
    currency: str
    amount: str
    status: str
    batch_withdrawal_id: str


class CreatePayoutResponse(TypedDict):
    """Create payout response (batch)."""

    id: str
    withdrawals: List[PayoutWithdrawalResponse]


class AuthResponse(TypedDict):
    """Auth response (JWT token for payouts, etc.)."""

    token: str


class ValidateAddressParams(TypedDict, total=False):
    """Validate address params."""

    address: str
    currency: str
    extra_id: Optional[str]


class CreateSubPartnerPaymentParams(TypedDict, total=False):
    """Create sub-partner deposit payment."""

    currency: str
    amount: float
    sub_partner_id: Union[str, int]
    fixed_rate: Optional[bool]


class CreateInvoicePaymentParams(TypedDict, total=False):
    """Create payment for existing invoice."""

    iid: Union[int, str]
    pay_currency: Optional[str]
    purchase_id: Optional[str]
    order_description: Optional[str]
    customer_email: Optional[str]
    payout_address: Optional[str]
    payout_extra_id: Optional[str]
    payout_currency: Optional[str]


class ApiStatusResponse(TypedDict, total=False):
    """API status response (GET /v1/status)."""

    status: Optional[str]
    message: Optional[str]
