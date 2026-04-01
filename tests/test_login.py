import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage

def test_login_success(page: Page):
    login = LoginPage(page)
    login.navigate()
    login.login("valid_user", "valid_pass")
    assert page.url != "https://biletebi.ge/login"

def test_login_invalid(page: Page):
    login = LoginPage(page)
    login.navigate()
    login.login("wrong_user", "wrong_pass")
    error = page.locator(".error-message")
    assert error.is_visible()