import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async



url ="https://www.rewe.de/angebote/nationale-angebote/?source=mc_offers"

user_data_dir = r"C:\Users\stahl\OneDrive\Dokumente\GitHub\playwright\tests\user-data-dir"

path_to_extension = r"C:\Users\stahl\OneDrive\Dokumente\GitHub\playwright\tests\dontcare.xpi"

async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch_persistent_context(
            user_data_dir,
            args=[
                f"--disable-extensions-except={path_to_extension}",
                f"--load-extension={path_to_extension}",
            ],
        )
        page = await browser.new_page()
        await page.goto(url, wait_until="load")
        document_height = await page.evaluate("document.body.scrollHeight")
        document_width = await page.evaluate("document.body.scrollWidth")

        if document_height > 8192:
            document_height = 8192

        blocks = int(document_height / 500) + 1

        for b in range(0, blocks):
            c = b * 500
            await page.evaluate("window.scrollTo(0, {});".format(c))
            await page.wait_for_timeout(200)


        #document_height = await page.evaluate("document.body.scrollHeight")
        #
        # await page.evaluate("window.scrollTo(0, {});".format(document_height))
        # await page.wait_for_timeout(1000)
        #
        await page.set_viewport_size({"width": document_width, "height": document_height})


        print(document_width)
        print(document_height)

        await page.wait_for_timeout(5000)

        await page.screenshot(path="dontcare.png")
        await browser.close()



asyncio.run(main())
