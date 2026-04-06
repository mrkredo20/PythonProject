from playwright.sync_api import Page, expect


class ForgotPasswordPage:
    BASE_URL = "https://biletebi.ge"
    OTP_STEP_TITLE = "\u10e8\u10d4\u10d8\u10e7\u10d5\u10d0\u10dc\u10d4 \u10d9\u10dd\u10d3\u10d8"
    EMPTY_FIELD_ERROR = "\u10e8\u10d4\u10d8\u10e7\u10d5\u10d0\u10dc\u10d4 \u10d4\u10da.\u10e4\u10dd\u10e1\u10e2\u10d0 \u10d0\u10dc \u10db\u10dd\u10d1\u10d8\u10da\u10e3\u10e0\u10d8\u10e1 \u10dc\u10dd\u10db\u10d4\u10e0\u10d8"
    NO_ACCOUNT_ERROR = "\u10d0\u10e0\u10d0\u10e1\u10ec\u10dd\u10e0\u10d8 \u10db\u10dd\u10dc\u10d0\u10ea\u10d4\u10db\u10d4\u10d1\u10d8"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.login_trigger = page.get_by_test_id("header_login_button")
        self.forgot_password_button = page.get_by_test_id("login_modal_forgot_password_button")
        self.email_or_phone_input = page.get_by_test_id("forgot_password_default_email_or_phone")
        self.get_code_button = page.get_by_test_id("forgot_password_default_get_code")
        self.otp_inputs = [page.get_by_test_id(f"otp_{index}") for index in range(5)]

    def open(self) -> None:
        self.page.goto(self.BASE_URL, wait_until="domcontentloaded")

    def open_forgot_password_modal(self) -> None:
        self.login_trigger.click()
        self.forgot_password_button.click()
        expect(self.email_or_phone_input).to_be_visible()
        expect(self.get_code_button).to_be_visible()

    def submit_email_or_phone(self, value: str) -> None:
        self.email_or_phone_input.fill(value)
        self.get_code_button.click()

    def submit_empty(self) -> None:
        self.get_code_button.click()

    def expect_success_otp_step(self, contact_value: str) -> None:
        expect(self.otp_inputs[0]).to_be_visible(timeout=10000)
        expect(self.page.get_by_text(self.OTP_STEP_TITLE)).to_be_visible()
        expect(self.page.get_by_text(contact_value)).to_be_visible()

    def expect_no_account_error(self) -> None:
        expect(self.page.get_by_text(self.NO_ACCOUNT_ERROR)).to_be_visible(timeout=10000)

    def expect_empty_field_validation(self) -> None:
        expect(self.page.get_by_text(self.EMPTY_FIELD_ERROR)).to_be_visible(timeout=10000)
