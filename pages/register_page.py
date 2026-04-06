import time

from playwright.sync_api import Locator, Page, expect


class RegisterPage:
    BASE_URL = "https://biletebi.ge"
    OTP_STEP_TITLE = "\u10e8\u10d4\u10d8\u10e7\u10d5\u10d0\u10dc\u10d4 \u10d9\u10dd\u10d3\u10d8"
    EXISTING_USER_ERROR = "\u10d0\u10e1\u10d4\u10d7\u10d8 \u10db\u10dd\u10db\u10ee\u10db\u10d0\u10e0\u10d4\u10d1\u10d4\u10da\u10d8 \u10e3\u10d9\u10d5\u10d4 \u10d0\u10e0\u10e1\u10d4\u10d1\u10dd\u10d1\u10e1"
    MISSING_CONTACT_ERROR = "\u10e8\u10d4\u10d8\u10e7\u10d5\u10d0\u10dc\u10d4 \u10d4\u10da.\u10e4\u10dd\u10e1\u10e2\u10d0 \u10d0\u10dc \u10db\u10dd\u10d1\u10d8\u10da\u10e3\u10e0\u10d8\u10e1 \u10dc\u10dd\u10db\u10d4\u10e0\u10d8"
    TERMS_REQUIRED_ERROR = "\u10d3\u10d0\u10d4\u10d7\u10d0\u10dc\u10ee\u10db\u10d4 \u10ec\u10d4\u10e1\u10d4\u10d1\u10e1 \u10d3\u10d0 \u10de\u10d8\u10e0\u10dd\u10d1\u10d4\u10d1\u10e1 \u10d3\u10d0 \u10d9\u10dd\u10dc\u10e4\u10d8\u10d3\u10d4\u10dc\u10ea\u10d8\u10d0\u10da\u10e3\u10e0\u10dd\u10d1\u10d8\u10e1 \u10de\u10dd\u10da\u10d8\u10e2\u10d8\u10d9\u10d0\u10e1"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.login_trigger = page.get_by_test_id("header_login_button")
        self.open_registration_button = page.get_by_test_id("login_modal_registration_button")
        self.email_or_phone_input = page.get_by_test_id("register_email_or_phone_number")
        self.agree_terms_checkbox = page.get_by_test_id("register_default_agree_terms")
        self.submit_button = page.get_by_test_id("register_default_submit")
        self.otp_inputs = [page.get_by_test_id(f"otp_{index}") for index in range(5)]

    def open(self) -> None:
        self.page.goto(self.BASE_URL, wait_until="domcontentloaded")

    def open_registration_modal(self) -> None:
        self.login_trigger.click()
        self.open_registration_button.click()
        expect(self.email_or_phone_input).to_be_visible()
        expect(self.submit_button).to_be_visible()

    def enter_email_or_phone(self, value: str) -> None:
        self.email_or_phone_input.fill(value)

    def agree_to_terms(self) -> None:
        self.page.locator('label[for="hasAgreedTermsAndPrivacy"]').click()
        assert self.agree_terms_checkbox.is_checked(), "Terms checkbox should be checked."

    def submit_registration(self) -> None:
        self.submit_button.click()

    def start_registration(self, email_or_phone: str, agree_terms: bool = True) -> None:
        self.enter_email_or_phone(email_or_phone)
        if agree_terms:
            self.agree_to_terms()
        self.submit_registration()

    def generate_unique_email(self) -> str:
        return f"playwright-{int(time.time() * 1000)}@example.com"

    def expect_otp_step(self, contact_value: str) -> None:
        expect(self.otp_inputs[0]).to_be_visible(timeout=10000)
        expect(self.page.get_by_text(self.OTP_STEP_TITLE)).to_be_visible()
        expect(self.page.get_by_text(contact_value)).to_be_visible()

    def fill_otp_code(self, otp_code: str) -> None:
        if len(otp_code) != len(self.otp_inputs) or not otp_code.isdigit():
            raise ValueError("OTP code must be a 5-digit string.")

        for index, digit in enumerate(otp_code):
            self.otp_inputs[index].fill(digit)

    def expect_existing_user_error(self) -> None:
        expect(self.page.get_by_text(self.EXISTING_USER_ERROR)).to_be_visible(timeout=10000)

    def expect_missing_required_field_errors(self) -> None:
        expect(self.page.get_by_text(self.TERMS_REQUIRED_ERROR)).to_be_visible()
        expect(self.page.get_by_text(self.MISSING_CONTACT_ERROR)).to_be_visible()

    def get_post_otp_password_locators(self) -> tuple[Locator, Locator, Locator]:
        """
        Placeholder for the password step after OTP verification.

        Replace these locators once staging exposes the post-OTP registration form
        or the product team provides the final selectors.
        """
        raise NotImplementedError(
            "Map the post-OTP password form selectors once the flow is available."
        )

    def complete_password_step(self, password: str, confirm_password: str) -> None:
        password_input, confirm_password_input, continue_button = (
            self.get_post_otp_password_locators()
        )
        password_input.fill(password)
        confirm_password_input.fill(confirm_password)
        continue_button.click()
