import asyncio
from playwright.async_api import async_playwright

url ="https://www.spiegel.de/"

user_data_dir = r"C:\Users\SearchLabAdmin\Documents\GitHub\playwright\tests\user-data-dir"


async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(
            headless=False,

        )
        page = await browser.new_page()
        await page.goto(url, wait_until="load")
        await page.wait_for_timeout(5000)
        #await page.screenshot(path="helloworld.png", full_page=True)
        await browser.close()


asyncio.run(main())
