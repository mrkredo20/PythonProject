import os
import time

import pytest
from playwright.sync_api import Page

from pages.forgot_password_page import ForgotPasswordPage


pytestmark = [pytest.mark.guest, pytest.mark.forgot_password]


REGISTERED_EMAIL = os.getenv("BILETEBI_REGISTERED_EMAIL") or os.getenv("BILETEBI_EMAIL")


@pytest.fixture
def forgot_password_page(page: Page) -> ForgotPasswordPage:
    forgot_password = ForgotPasswordPage(page)
    forgot_password.open()
    forgot_password.open_forgot_password_modal()
    return forgot_password


@pytest.mark.skipif(
    not REGISTERED_EMAIL,
    reason="Set BILETEBI_REGISTERED_EMAIL or BILETEBI_EMAIL to run the registered-email forgot-password test.",
)
def test_submit_valid_registered_email_shows_success_message(
    forgot_password_page: ForgotPasswordPage,
) -> None:
    forgot_password_page.submit_email_or_phone(REGISTERED_EMAIL)
    forgot_password_page.expect_success_otp_step(REGISTERED_EMAIL)


def test_submit_unregistered_email_shows_error_message(
    forgot_password_page: ForgotPasswordPage,
) -> None:
    unregistered_email = f"forgot-{int(time.time() * 1000)}@example.com"

    forgot_password_page.submit_email_or_phone(unregistered_email)
    forgot_password_page.expect_no_account_error()


def test_submit_empty_field_shows_validation_error(
    forgot_password_page: ForgotPasswordPage,
) -> None:
    forgot_password_page.submit_empty()
    forgot_password_page.expect_empty_field_validation()
