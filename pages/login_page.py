from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://biletebi.ge"  # replace with your project
        self.username_field = page.locator("#username")
        self.password_field = page.locator("#password")
        self.login_button = page.locator("button[type='submit']")

    def navigate(self):
        self.page.goto(self.url)

    def login(self, username: str, password: str):
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.login_button.click()