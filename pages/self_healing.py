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

    def find_element_smart(self, selectors: list):
        """Try multiple selectors — returns first working one"""
        for selector in selectors:
            try:
                el = self.page.locator(selector)
                if el.count() > 0:
                    print(f"✅ Found with: {selector}")
                    return el
            except:
                continue
        raise Exception(f"❌ No working selector found from: {selectors}")