from time import sleep

from playwright.sync_api import Page,expect,Route
import re
def test_welcome_page(page):
    page.goto("https://www.wikipedia.org/")
    page.get_by_role("link",name="English").click()
    expect(page.get_by_text("Welcome to Wikipedia")).to_be_visible()

def test_wiki_pages(page):
    page.goto("https://www.wikipedia.org/")
    page.get_by_role("link",name="English").click()
    page.locator("#ca-talk").click()
    expect(page.locator("#firstHeading")).to_have_text("Talk:Main Page")
#change request on the back
def test_login_back(page):
    def change_request(route:Route):
        data=route.request.post_data
        if data:
            data=data.replace("574045469","574")
        route.continue_(post_data=data)
    page.route(re.compile(r".*identity-api\.biletebi\.ge/AccessToken.*"),change_request)
    page.goto("https://biletebi.ge/")
    page.get_by_test_id("header_login_button").click()
    page.get_by_test_id("login_modal_email").fill("574045469")
    page.get_by_test_id("login_modal_password").fill("Mosetest1234!")
    page.get_by_test_id("login_modal_submit_button").click()
    expect(page.get_by_test_id("header_my_tickets_button")).to_be_visible()
def test_change_name(page):
    def change_request(route:Route):
        response=route.fetch()
        print("hi")
        data=response.text()
        data=data.replace("gio","giogio")
        route.fulfill(response=response, body=data)

    page.route(re.compile(r"identity-api\.biletebi\.ge/Users"),change_request)
    page.goto("https://biletebi.ge/")
    page.get_by_test_id("header_login_button").click()
    page.get_by_test_id("login_modal_email").fill("574045469")
    page.get_by_test_id("login_modal_password").fill("Mosetest1234!")
    page.get_by_test_id("login_modal_submit_button").click()
    sleep(3)
    expect(page.get_by_test_id("header_my_tickets_button")).to_be_visible()
    page.get_by_test_id("header_profile_button").click()
    sleep(10)
