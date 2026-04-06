import os

import pytest

from tests.api.helpers import IdentityApiClient, make_unique_registration_email


@pytest.fixture
def identity_api_client() -> IdentityApiClient:
    return IdentityApiClient()


@pytest.fixture
def api_email() -> str:
    value = os.getenv("BILETEBI_EMAIL")
    if not value:
        pytest.skip("Set BILETEBI_EMAIL to run biletebi auth API tests.")
    return value


@pytest.fixture
def api_password() -> str:
    value = os.getenv("BILETEBI_PASSWORD")
    if not value:
        pytest.skip("Set BILETEBI_PASSWORD to run biletebi auth API tests.")
    return value


@pytest.fixture
def existing_registration_email(api_email: str) -> str:
    return os.getenv("BILETEBI_EXISTING_EMAIL") or api_email


@pytest.fixture
def fresh_registration_email() -> str:
    return make_unique_registration_email()


@pytest.fixture
def auth_token(identity_api_client: IdentityApiClient, api_email: str, api_password: str) -> str:
    response = identity_api_client.login(api_email, api_password)
    assert response.status_code == 200, response.text
    data = response.json()
    return data["result"]["accessToken"]
