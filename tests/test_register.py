import os

import pytest
from playwright.sync_api import Page

from pages.register_page import RegisterPage


pytestmark = [pytest.mark.guest, pytest.mark.registration]


EXISTING_EMAIL = os.getenv("BILETEBI_EXISTING_EMAIL") or os.getenv("BILETEBI_EMAIL")
OTP_CODE = os.getenv("BILETEBI_REGISTRATION_OTP")
NEW_REGISTRATION_EMAIL = os.getenv("BILETEBI_NEW_REGISTRATION_EMAIL")
REGISTRATION_PASSWORD = os.getenv("BILETEBI_REGISTRATION_PASSWORD")


@pytest.fixture
def register_page(page: Page) -> RegisterPage:
    register = RegisterPage(page)
    register.open()
    register.open_registration_modal()
    return register


def test_successful_registration_with_all_valid_fields(register_page: RegisterPage) -> None:
    unique_email = NEW_REGISTRATION_EMAIL or register_page.generate_unique_email()

    register_page.start_registration(unique_email)
    register_page.expect_otp_step(unique_email)


@pytest.mark.skipif(
    not EXISTING_EMAIL,
    reason="Set BILETEBI_EXISTING_EMAIL or BILETEBI_EMAIL to run the duplicate-email registration test.",
)
def test_registration_with_already_existing_email_shows_error(register_page: RegisterPage) -> None:
    register_page.start_registration(EXISTING_EMAIL)
    register_page.expect_existing_user_error()


@pytest.mark.skipif(
    not OTP_CODE or not NEW_REGISTRATION_EMAIL or not REGISTRATION_PASSWORD,
    reason=(
        "Set BILETEBI_NEW_REGISTRATION_EMAIL, BILETEBI_REGISTRATION_OTP, and "
        "BILETEBI_REGISTRATION_PASSWORD after the OTP-enabled flow is available."
    ),
)
@pytest.mark.smoke
def test_registration_with_mismatched_passwords_shows_validation(register_page: RegisterPage) -> None:
    register_page.start_registration(NEW_REGISTRATION_EMAIL)
    register_page.expect_otp_step(NEW_REGISTRATION_EMAIL)
    register_page.fill_otp_code(OTP_CODE)
    register_page.complete_password_step(
        REGISTRATION_PASSWORD,
        f"{REGISTRATION_PASSWORD}x",
    )

    pytest.fail(
        "Map the post-OTP password form selectors and final validation assertion "
        "once staging or QA exposes that step."
    )


def test_registration_with_missing_required_fields_shows_form_errors(register_page: RegisterPage) -> None:
    register_page.submit_registration()
    register_page.expect_missing_required_field_errors()
