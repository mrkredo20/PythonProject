import os

import pytest
from playwright.sync_api import Page

from pages.session_page import SessionPage


VALID_EMAIL = os.getenv("BILETEBI_EMAIL")
VALID_PASSWORD = os.getenv("BILETEBI_PASSWORD")


pytestmark = [
    pytest.mark.auth,
    pytest.mark.session,
    pytest.mark.slow,
    pytest.mark.skipif(
        not VALID_EMAIL or not VALID_PASSWORD,
        reason="Set BILETEBI_EMAIL and BILETEBI_PASSWORD to run session tests.",
    ),
]


@pytest.fixture
def session_page(page: Page) -> SessionPage:
    session = SessionPage(page)
    session.open()
    return session


@pytest.fixture
def authenticated_session_page(auth_page: Page) -> SessionPage:
    session = SessionPage(auth_page)
    session.open()
    session.expect_logged_in_home()
    return session


def test_after_login_user_is_redirected_to_home(authenticated_session_page: SessionPage) -> None:
    authenticated_session_page.expect_logged_in_home()


def test_after_login_auth_cookie_exists(authenticated_session_page: SessionPage) -> None:
    cookie_names = authenticated_session_page.get_auth_cookie_names()

    assert "token" in cookie_names
    assert "refreshToken" in cookie_names


@pytest.mark.xfail(
    reason="Known biletebi issue: the logout menu item does not clear auth cookies in the current live flow.",
    strict=False,
)
def test_logout_clears_session_and_returns_guest_state(
    authenticated_session_page: SessionPage,
) -> None:
    authenticated_session_page.logout()
    authenticated_session_page.expect_logged_out_state()


@pytest.mark.xfail(
    reason="Known biletebi issue: logout does not terminate the session, so protected pages remain accessible.",
    strict=False,
)
def test_after_logout_protected_page_shows_guest_state(
    authenticated_session_page: SessionPage,
) -> None:
    authenticated_session_page.logout()
    authenticated_session_page.open_protected_page()
    authenticated_session_page.expect_guest_on_protected_page()
