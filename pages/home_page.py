from playwright.sync_api import Page, expect


class HomePage:
    BASE_URL = "https://biletebi.ge"

    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self) -> None:
        self.page.goto(self.BASE_URL, wait_until="domcontentloaded")

    def search_event(self, text: str) -> None:
        search_input = self.page.get_by_test_id("header_search_input")
        search_input.fill(text)
        expect(search_input).to_have_value(text)

    def get_search_results(self):
        search_text = self.page.get_by_test_id("header_search_input").input_value()
        return self.page.locator("[data-testid^='event_card_title_']", has_text=search_text)
