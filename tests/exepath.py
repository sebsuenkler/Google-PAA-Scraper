from playwright.sync_api import sync_playwright

def newPage(page):
   print("newPage() page title:", page.title())

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        executable_path ='C:\Program Files\Google\Chrome\Application\chrome.exe'
    )
    context = browser.new_context()
    page = context.new_page()

    context.on("page", lambda page: newPage(page))

    page.evaluate('''() => {
        window.open('https://google.com', '_blank')
    }''')

    page.wait_for_timeout(2000)
    browser.close()
