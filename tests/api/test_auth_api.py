import pytest


pytestmark = [pytest.mark.api, pytest.mark.auth]


def test_login_with_valid_credentials_returns_tokens(identity_api_client, api_email, api_password):
    response = identity_api_client.login(api_email, api_password)

    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"]["role"] == "User"
    assert data["result"]["tokenType"] == "Bearer"
    assert data["result"]["expiresIn"] > 0
    assert data["result"]["accessToken"]
    assert data["result"]["refreshToken"]


def test_login_with_wrong_password_returns_invalid_credentials(identity_api_client, api_email):
    response = identity_api_client.login(api_email, "WrongPassword123!")

    assert response.status_code == 400
    data = response.json()
    assert data["type"] == "InvalidCredentialsException"
    assert data["status"] == 400


def test_login_with_missing_password_returns_validation_error(identity_api_client, api_email):
    response = identity_api_client.login(email_or_phone=api_email)

    assert response.status_code == 400
    data = response.json()
    assert data["title"] == "One or more validation errors occurred."
    assert data["errors"]["Password"] == ["The Password field is required."]


def test_login_with_missing_email_returns_validation_error(identity_api_client, api_password):
    response = identity_api_client.login(password=api_password)

    assert response.status_code == 400
    data = response.json()
    assert data["title"] == "One or more validation errors occurred."
    assert data["errors"]["EmailOrPhoneNumber"] == ["The EmailOrPhoneNumber field is required."]


def test_login_with_invalid_email_format_returns_invalid_email_error(identity_api_client, api_password):
    response = identity_api_client.login("userATmail.com", api_password)

    assert response.status_code == 400
    data = response.json()
    assert data["type"] == "InvalidEmailOrPhoneException"
    assert "invalid" in data["detail"].lower()


def test_current_user_with_valid_token_returns_profile(identity_api_client, auth_token, api_email):
    response = identity_api_client.get_current_user(auth_token)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == api_email
    assert data["id"]
    assert data["bidId"].startswith("BID-")
    assert data["qrCodeUrl"].startswith("https://")


def test_current_user_without_token_returns_unauthorized(identity_api_client):
    response = identity_api_client.get_current_user()

    assert response.status_code == 401
    data = response.json()
    assert data["title"] == "Unauthorized"
    assert data["status"] == 401


def test_current_user_with_invalid_token_returns_unauthorized(identity_api_client):
    response = identity_api_client.get_current_user("invalid-token")

    assert response.status_code == 401
    data = response.json()
    assert data["title"] == "Unauthorized"
    assert data["status"] == 401
