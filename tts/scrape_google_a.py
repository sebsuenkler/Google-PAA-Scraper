urls = ["https://www.google.com/webhp?hl=en","https://www.google.com/search?q=what+is+a+cat&hl=en&source=hp&ei=B46MYr7dHLOTxc8P-byoqAE&iflsig=AJiK0e8AAAAAYoycF4BQI3WxGLqk03ZvvEbCW8OwqpJo&oq=&gs_lcp=Cgdnd3Mtd2l6EBJQAFgAYABoAHAAeACAAQCIAQCSAQCYAQCgAQY&gs_ivs=1&sclient=gws-wiz#tts=0", "https://www.google.com/search?q=how+old+do+they+get&hl=en&source=hp&ei=B46MYr7dHLOTxc8P-byoqAE&iflsig=AJiK0e8AAAAAYoycF4BQI3WxGLqk03ZvvEbCW8OwqpJo&oq=&gs_lcp=Cgdnd3Mtd2l6EBJQAFgAYABoAHAAeACAAQCIAQCSAQCYAQCgAQY&gs_ivs=1&sclient=gws-wiz#tts=0"]

from playwright.sync_api import sync_playwright


def run(playwright):
    chromium = playwright.chromium
    browser = chromium.launch(headless=False, executable_path ='C:\Program Files\Google\Chrome\Application\chrome.exe', args=['--use-fake-device-for-media-stream', '--use-fake-ui-for-media-stream'])
    context = browser.new_context(locale="en-US")
    context.grant_permissions(permissions=['microphone'])
    page = context.new_page()

    page.goto(urls[0])
    page.click('.QS5gu.sy4vM')

    def click_cookies(page):
        page.wait_for_timeout(1000)

        rows = page.locator(".VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-INsAgc.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.Rj2Mlf.OLiIxf.PDpWxe.P62QJc.qfvgSe.S82sre")
        count = round(rows.count() / 2)
        print(count)

        for i in range(0, count):
            try:
                row = rows.nth(i).click()
            except:
                pass

    click_cookies(page)
    page.click('.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.qfvgSe.XICXwf')

    page.wait_for_timeout(3000)

    page.goto(urls[1])

    

    page.wait_for_timeout(3000)

    page.goto(urls[2])

    page.pause()
    # other actions...

    browser.close()


with sync_playwright() as playwright:
    run(playwright)
