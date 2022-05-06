import asyncio
from playwright.async_api import async_playwright


url ="https://addons.mozilla.org/en-US/firefox/addon/i-dont-care-about-cookies/"

user_data_dir = r"user-data-dir"

path_to_extension = r'C:\Users\SearchLabAdmin\Documents\GitHub\playwright\tests\dontcare.xpi'

async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch_persistent_context(
            user_data_dir,
            headless=False,
            
        )
        page = await browser.new_page()
        await page.goto(url, wait_until="load")
        await page.wait_for_timeout(5000)
        await browser.close()



asyncio.run(main())
