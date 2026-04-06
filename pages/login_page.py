from playwright.sync_api import Page, expect


class LoginPage:
    BASE_URL = "https://biletebi.ge"
    EMPTY_EMAIL_ERROR = "\u10e8\u10d4\u10d8\u10e7\u10d5\u10d0\u10dc\u10d4 \u10d4\u10da.\u10e4\u10dd\u10e1\u10e2\u10d0 \u10d0\u10dc \u10db\u10dd\u10d1\u10d8\u10da\u10e3\u10e0\u10d8\u10e1 \u10dc\u10dd\u10db\u10d4\u10e0\u10d8"
    EMPTY_PASSWORD_ERROR = "\u10e8\u10d4\u10d8\u10e7\u10d5\u10d0\u10dc\u10d4 \u10de\u10d0\u10e0\u10dd\u10da\u10d8"
    INVALID_EMAIL_OR_PHONE_ERROR = "\u10d2\u10d7\u10ee\u10dd\u10d5, \u10e8\u10d4\u10d8\u10e7\u10d5\u10d0\u10dc\u10dd \u10d5\u10d0\u10da\u10d8\u10d3\u10e3\u10e0\u10d8 \u10d4\u10da.\u10e4\u10dd\u10e1\u10e2\u10d0 \u10d0\u10dc \u10e2\u10d4\u10da\u10d4\u10e4\u10dd\u10dc\u10d8\u10e1 \u10dc\u10dd\u10db\u10d4\u10e0\u10d8"
    WRONG_PASSWORD_ERROR = "\u10d0\u10e0\u10d0\u10e1\u10ec\u10dd\u10e0\u10d8 \u10db\u10dd\u10dc\u10d0\u10ea\u10d4\u10db\u10d4\u10d1\u10d8"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.login_trigger = page.get_by_test_id("header_login_button")
        self.email_input = page.get_by_test_id("login_modal_email")
        self.password_input = page.get_by_test_id("login_modal_password")
        self.submit_button = page.get_by_test_id("login_modal_submit_button")
        self.my_tickets_button = page.get_by_test_id("header_my_tickets_button")
        self.error_message = page.locator(
            "[data-testid*='error'], .error-message, .invalid-feedback, .text-danger"
        )
        self.validation_messages = page.locator(".text-danger")

    def open(self) -> None:
        self.page.goto(self.BASE_URL, wait_until="domcontentloaded")

    def open_login_modal(self) -> None:
        self.login_trigger.click()
        expect(self.email_input).to_be_visible()
        expect(self.password_input).to_be_visible()

    def login(self, email: str, password: str) -> None:
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def expect_successful_login(self) -> None:
        expect(self.my_tickets_button).to_be_visible(timeout=10000)

    def expect_login_error(self) -> None:
        expect(self.error_message.first).to_be_visible(timeout=10000)
        expect(self.page.get_by_text(self.WRONG_PASSWORD_ERROR)).to_be_visible()

    def expect_empty_field_validation(self) -> None:
        expect(self.page.get_by_text(self.EMPTY_EMAIL_ERROR)).to_be_visible()
        expect(self.page.get_by_text(self.EMPTY_PASSWORD_ERROR)).to_be_visible()

    def expect_invalid_email_validation(self) -> None:
        expect(self.page.get_by_text(self.INVALID_EMAIL_OR_PHONE_ERROR)).to_be_visible()
