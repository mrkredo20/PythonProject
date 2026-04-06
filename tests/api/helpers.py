import os
from typing import Any
from uuid import uuid4

import requests


IDENTITY_API_BASE_URL = os.getenv(
    "BILETEBI_IDENTITY_API_BASE_URL",
    "https://identity-api.biletebi.ge",
)
DEFAULT_TIMEOUT = 15


class IdentityApiClient:
    def __init__(self, base_url: str = IDENTITY_API_BASE_URL, timeout: int = DEFAULT_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def login(self, email_or_phone: str | None = None, password: str | None = None) -> requests.Response:
        payload: dict[str, Any] = {}
        if email_or_phone is not None:
            payload["emailOrPhoneNumber"] = email_or_phone
        if password is not None:
            payload["password"] = password
        return self.session.post(
            self._url("/AccessToken"),
            json=payload,
            timeout=self.timeout,
        )

    def get_current_user(self, token: str | None = None) -> requests.Response:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return self.session.get(self._url("/Users"), headers=headers, timeout=self.timeout)

    def init_registration(self, email_or_phone: str | None = None) -> requests.Response:
        payload: dict[str, Any] = {}
        if email_or_phone is not None:
            payload["emailOrPhoneNumber"] = email_or_phone
        return self.session.post(
            self._url("/Users/with-otp/init"),
            json=payload,
            timeout=self.timeout,
        )

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"


def make_unique_registration_email() -> str:
    return f"api-registration-{uuid4().hex[:12]}@example.com"
