"""
HTTP client for NOWPayments API
"""

from typing import Any, Dict, Optional

import requests

from .types import NowPaymentsConfig

PRODUCTION_URL = "https://api.nowpayments.io"
SANDBOX_URL = "https://api-sandbox.nowpayments.io"


class NowPaymentsError(Exception):
    """API error with status code and response details."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        code: Optional[str] = None,
        response: Optional[Any] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.response = response

    def __str__(self) -> str:
        parts = [self.message]
        if self.status_code is not None:
            parts.append(f"(status: {self.status_code})")
        if self.code:
            parts.append(f"[{self.code}]")
        return " ".join(parts)


def _get_api_key(config: NowPaymentsConfig) -> str:
    """Get API key from config (supports api_key or apiKey)."""
    key = config.get("api_key") or config.get("apiKey")
    if not key or not str(key).strip():
        raise ValueError(
            "NOWPayments API key is required. Get yours at https://account.nowpayments.io"
        )
    return str(key).strip()


class _HttpClient:
    """HTTP client wrapper with base URL and error handling."""

    def __init__(self, base_url: str, session: requests.Session, timeout: float):
        self._base_url = base_url.rstrip("/")
        self._session = session
        self._timeout = timeout

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = f"{self._base_url}{path}"
        timeout = kwargs.pop("timeout", self._timeout)
        return _request(self._session, method, url, timeout=timeout, **kwargs)

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request("POST", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request("DELETE", path, **kwargs)


def create_http_client(config: NowPaymentsConfig) -> _HttpClient:
    """Create a configured HTTP client for the NOWPayments API."""
    base_url = config.get("base_url") or (
        SANDBOX_URL if config.get("sandbox") else PRODUCTION_URL
    )
    timeout = config.get("timeout") or 30000
    timeout_sec = timeout / 1000.0  # Convert ms to seconds

    api_key = _get_api_key(config)

    session = requests.Session()
    session.headers.update(
        {
            "Content-Type": "application/json",
            "x-api-key": api_key,
        }
    )

    return _HttpClient(base_url, session, timeout_sec)


def _extract_error_message(response: requests.Response) -> str:
    """Extract error message from API response."""
    try:
        data = response.json()
        if isinstance(data, dict):
            for key in ("message", "msg", "error"):
                val = data.get(key)
                if isinstance(val, str):
                    return val
    except Exception:
        pass
    return response.reason or "Request failed"


def _request(
    session: requests.Session,
    method: str,
    url: str,
    **kwargs: Any,
) -> requests.Response:
    """
    Make HTTP request and handle errors.
    Raises NowPaymentsError on API errors.
    """
    timeout = kwargs.pop("timeout", 30.0)

    try:
        response = session.request(method, url, timeout=timeout, **kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as e:
        if e.response is not None:
            try:
                data = e.response.json() if e.response.content else {}
            except Exception:
                data = {}
            code = data.get("code") if isinstance(data, dict) else None
            raise NowPaymentsError(
                _extract_error_message(e.response),
                status_code=e.response.status_code,
                code=code,
                response=e.response,
            ) from e
        raise NowPaymentsError(str(e)) from e
    except requests.exceptions.Timeout:
        raise NowPaymentsError(
            "Request timed out. Check your connection or try again.",
            code="ECONNABORTED",
        )
    except requests.exceptions.RequestException as e:
        raise NowPaymentsError(
            str(e) or "Network error. Check your connection.",
            code=getattr(e, "errno", None),
        ) from e
