import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

url ="https://www.google.de"

user_data_dir = r"C:\Users\SearchLabAdmin\Documents\GitHub\playwright\tests\user-data-dir"

path_to_extension = r"C:\Users\SearchLabAdmin\Documents\GitHub\playwright\tests\dontcare.xpi"

async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch_persistent_context(
            user_data_dir,
            headless=False,
            args=[
                f"--disable-extensions-except={path_to_extension}",
                f"--load-extension={path_to_extension}",
            ],
        )
        page = await browser.new_page()
        await page.goto(url, wait_until="load")
        await page.wait_for_timeout(3000)
        await browser.close()



asyncio.run(main())
