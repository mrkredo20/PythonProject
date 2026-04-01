def search_event(self, text):
    search_input = self.page.locator('input[type="search"]')
    search_input.fill(text)
    search_input.press("Enter")

def get_search_results(self):
    return self.page.locator('.event-card')