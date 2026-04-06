import os

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage


VALID_EMAIL = os.getenv("BILETEBI_EMAIL")
VALID_PASSWORD = os.getenv("BILETEBI_PASSWORD")


pytestmark = [pytest.mark.auth, pytest.mark.smoke]


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    login = LoginPage(page)
    login.open()
    login.open_login_modal()
    return login


@pytest.mark.skipif(
    not VALID_EMAIL or not VALID_PASSWORD,
    reason="Set BILETEBI_EMAIL and BILETEBI_PASSWORD to run the successful login test.",
)
@pytest.mark.smoke
def test_successful_login_with_valid_credentials(login_page: LoginPage) -> None:
    login_page.login(VALID_EMAIL, VALID_PASSWORD)
    login_page.expect_successful_login()

@pytest.mark.smoke
def test_login_with_wrong_password_shows_error(login_page: LoginPage) -> None:
    email = VALID_EMAIL or "user@example.com"

    login_page.login(email, "WrongPassword123!")
    login_page.expect_login_error()

@pytest.mark.smoke
def test_login_with_empty_fields_shows_validation_errors(login_page: LoginPage) -> None:
    login_page.login("", "")
    login_page.expect_empty_field_validation()

@pytest.mark.smoke
def test_login_with_invalid_email_format_shows_validation(login_page: LoginPage) -> None:
    login_page.login("userATmail.com", "SomePassword123!")
    login_page.expect_invalid_email_validation()
