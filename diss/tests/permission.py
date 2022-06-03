from playwright.sync_api import sync_playwright


def run(playwright):
    chromium = playwright.chromium
    browser = chromium.launch(headless=False, args=['--use-fake-device-for-media-stream', '--use-fake-ui-for-media-stream'])
    context = browser.new_context()
    context.grant_permissions(permissions=['microphone'])
    page = context.new_page()
    page.goto("https://permission.site/")
    page.click('#microphone')
    page.pause()
    # other actions...
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
