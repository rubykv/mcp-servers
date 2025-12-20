from playwright.sync_api import Page


def test_valid_login(page: Page):
    # Navigate to login page
    page.goto("https://the-internet.herokuapp.com/login")

    # Enter credentials
    page.fill("#username", "tomsmith")
    page.fill("#password", "SuperSecretPassword!")

    # Submit login form
    page.click('button[type="submit"]')

    # Assert success message is visible
    flash = page.locator("#flash")
    assert flash.is_visible()
    assert "You logged into a secure area!" in flash.text_content()
