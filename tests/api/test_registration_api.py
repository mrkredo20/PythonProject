import pytest


pytestmark = [pytest.mark.api, pytest.mark.registration]


def test_registration_init_with_new_email_returns_success(identity_api_client, fresh_registration_email):
    response = identity_api_client.init_registration(fresh_registration_email)

    assert response.status_code == 200
    assert response.json() == {}


def test_registration_init_with_existing_email_returns_user_exists_error(
    identity_api_client,
    existing_registration_email,
):
    response = identity_api_client.init_registration(existing_registration_email)

    assert response.status_code == 400
    data = response.json()
    assert data["type"] == "UserExistsException"
    assert existing_registration_email in data["detail"]


def test_registration_init_with_missing_email_returns_validation_error(identity_api_client):
    response = identity_api_client.init_registration()

    assert response.status_code == 400
    data = response.json()
    assert data["title"] == "One or more validation errors occurred."
    assert data["errors"]["EmailOrPhoneNumber"] == ["The EmailOrPhoneNumber field is required."]


def test_registration_init_with_invalid_email_format_returns_validation_error(identity_api_client):
    response = identity_api_client.init_registration("userATmail.com")

    assert response.status_code == 400
    data = response.json()
    assert data["type"] == "ApplicationValidationException"
    assert "EmailOrPhoneNumber" in data["extensions"]
