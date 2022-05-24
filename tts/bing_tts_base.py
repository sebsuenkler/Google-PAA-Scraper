import playsound

from playwright.sync_api import sync_playwright

url = "https://www.bing.com/?setlang=en"

def run(playwright):
    firefox = playwright.firefox
    browser = firefox.launch(headless=False, args=['--use-fake-device-for-media-stream', '--use-fake-ui-for-media-stream'], firefox_user_prefs={"permissions.default.microphone":1, "permissions.default.geo":1})
    context = browser.new_context(locale="en-US",  geolocation={'longitude': -73.935242, 'latitude':40.730610})

    page = context.new_page()

    page.goto(url)
    page.click('.bnp_btn_accept')

    page.click('.mic_cont.icon')

    page.wait_for_timeout(2000)

    playsound.playsound('cat_1.mp3', True)

    page.wait_for_timeout(15000)

    page.click('.mic_cont.icon')

    page.wait_for_timeout(2000)

    playsound.playsound('cat_2.mp3', True)

    page.wait_for_timeout(15000)

    page.click('.mic_cont.icon')

    page.wait_for_timeout(2000)

    playsound.playsound('cat_3.mp3', True)

    page.wait_for_timeout(15000)

    page.pause()
    # other actions...
    browser.close()




with sync_playwright() as playwright:
    run(playwright)
