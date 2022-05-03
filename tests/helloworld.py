import asyncio
from playwright.async_api import async_playwright

url ="https://www.spiegel.de/"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        await page.screenshot(path="helloworld.png", full_page=True)
        await browser.close()


asyncio.run(main())
