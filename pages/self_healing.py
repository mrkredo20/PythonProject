import hashlib

from playwright.sync_api import Page


class SelfHealingPage:
    def __init__(self, page: Page):
        self.page = page

    def get_html_snapshot(self) -> str:
        return self.page.content()

    def get_snapshot_hash(self) -> str:
        content = self.get_html_snapshot()
        return hashlib.md5(content.encode()).hexdigest()

    def _resolve_selector(self, selector: str):
        if selector.startswith("testid="):
            return self.page.get_by_test_id(selector.split("=", 1)[1])
        return self.page.locator(selector)

    def find_element_smart(self, selectors: list):
        """Try multiple selectors and return the first working locator."""
        for selector in selectors:
            try:
                element = self._resolve_selector(selector)
                if element.count() > 0:
                    print(f"Found with: {selector}")
                    return element
            except Exception:
                continue
        raise Exception(f"No working selector found from: {selectors}")
