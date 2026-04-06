import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage


@pytest.mark.smoke
@pytest.mark.guest
# def test_search_event(page):
#     home = HomePage(page)
#
#     home.open()
#     home.search_event("Peggy Gou")
#
#     result = home.get_search_results().first
#
#     expect(result).to_be_visible()
#     expect(result).to_have_text("Peggy Gou")

def test_search_event(open_home):
    page = open_home
    search_input = page.get_by_test_id("header_search_input")
    search_input.wait_for(state="visible", timeout=15000)
    search_input.fill("Peggy Gou")