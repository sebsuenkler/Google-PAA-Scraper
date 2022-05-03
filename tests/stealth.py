import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

url = "https://www.rewe.de/angebote/nationale-angebote/?source=mc_offers"

async def main():
    async with async_playwright() as p:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            browser = await browser_type.launch()
            page = await browser.new_page()
            await stealth_async(page)
            await page.goto(url)
            await page.screenshot(path=f'example-{browser_type.name}.png')
            await browser.close()

asyncio.get_event_loop().run_until_complete(main())
