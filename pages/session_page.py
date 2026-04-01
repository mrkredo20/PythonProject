from playwright.sync_api import Page, expect


class SessionPage:
    BASE_URL = "https://biletebi.ge"
    PROTECTED_PATH = "/my-tickets"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.login_trigger = page.get_by_test_id("header_login_button")
        self.email_input = page.get_by_test_id("login_modal_email")
        self.password_input = page.get_by_test_id("login_modal_password")
        self.submit_button = page.get_by_test_id("login_modal_submit_button")
        self.my_tickets_button = page.get_by_test_id("header_my_tickets_button")
        self.profile_button = page.get_by_test_id("header_profile_button")
        self.logout_button = page.get_by_test_id("menu_item_settings_exit")
        self.accept_cookies_button = page.get_by_test_id("accept_cookies")

    def open(self, path: str = "") -> None:
        self.page.goto(f"{self.BASE_URL}{path}")

    def accept_cookies_if_needed(self) -> None:
        if self.accept_cookies_button.count() and self.accept_cookies_button.first.is_visible():
            self.accept_cookies_button.first.click()

    def login(self, email: str, password: str) -> None:
        self.accept_cookies_if_needed()
        self.login_trigger.click()
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def expect_logged_in_home(self) -> None:
        expect(self.my_tickets_button).to_be_visible(timeout=10000)
        expect(self.profile_button).to_be_visible(timeout=10000)
        assert self.page.url == f"{self.BASE_URL}/"

    def get_auth_cookie_names(self) -> list[str]:
        cookie_names = []
        for cookie in self.page.context.cookies():
            if cookie["name"] in {"token", "refreshToken"}:
                cookie_names.append(cookie["name"])
        return cookie_names

    def open_profile_menu(self) -> None:
        self.profile_button.click()
        expect(self.logout_button).to_be_visible(timeout=10000)

    def logout(self) -> None:
        self.open_profile_menu()
        self.logout_button.click(force=True)

    def expect_logged_out_state(self) -> None:
        expect(self.login_trigger).to_be_visible(timeout=10000)
        expect(self.profile_button).not_to_be_visible(timeout=10000)
        assert self.get_auth_cookie_names() == []

    def open_protected_page(self) -> None:
        self.open(self.PROTECTED_PATH)

    def expect_guest_on_protected_page(self) -> None:
        expect(self.login_trigger).to_be_visible(timeout=10000)
        assert self.my_tickets_button.count() == 0
