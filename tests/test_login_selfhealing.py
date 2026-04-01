import os

import pytest
from playwright.sync_api import expect

from pages.self_healing import SelfHealingPage


VALID_EMAIL = os.getenv("BILETEBI_EMAIL")
VALID_PASSWORD = os.getenv("BILETEBI_PASSWORD")


pytestmark = [pytest.mark.auth, pytest.mark.self_healing, pytest.mark.slow]


@pytest.mark.skipif(
    not VALID_EMAIL or not VALID_PASSWORD,
    reason="Set BILETEBI_EMAIL and BILETEBI_PASSWORD to run the self-healing login test.",
)
def test_biletebi_login_with_self_healing_selectors(page) -> None:
    healer = SelfHealingPage(page)

    page.goto("https://biletebi.ge")
    expect(page.get_by_test_id("header_login_button")).to_be_visible()

    login_button = healer.find_element_smart(
        [
            "testid=header_login_button",
            "button:has-text('\u10e8\u10d4\u10e1\u10d5\u10da\u10d0')",
            "button.sc-6ad6ee2f-0.jQxgh",
        ]
    )
    login_button.click()

    email_input = healer.find_element_smart(
        [
            "testid=login_modal_email",
            "input[placeholder*='\u10d4\u10da.\u10e4\u10dd\u10e1\u10e2\u10d0']",
            "input.sc-bb37486b-5.hijgGJ[name='emailOrPhoneNumber']",
        ]
    )
    email_input.fill(VALID_EMAIL)

    password_input = healer.find_element_smart(
        [
            "testid=login_modal_password",
            "input[placeholder='\u10de\u10d0\u10e0\u10dd\u10da\u10d8']",
            "input.sc-bb37486b-5.hijgGJ[type='password']",
        ]
    )
    password_input.fill(VALID_PASSWORD)

    submit_button = healer.find_element_smart(
        [
            "testid=login_modal_submit_button",
            "button[type='submit']:has-text('\u10e8\u10d4\u10e1\u10d5\u10da\u10d0')",
            "button.sc-6ad6ee2f-0.cSrGga",
        ]
    )
    submit_button.click()
    expect(page.get_by_test_id("header_my_tickets_button")).to_be_visible(timeout=10000)

    my_tickets_button = healer.find_element_smart(
        [
            "testid=header_my_tickets_button",
            "button:has-text('\u10e9\u10d4\u10db\u10d8 \u10d1\u10d8\u10da\u10d4\u10d7\u10d4\u10d1\u10d8')",
            "button[data-testid='header_my_tickets_button']",
        ]
    )

    expect(my_tickets_button).to_be_visible(timeout=10000)
