import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async


import time

url ="https://www.spiegel.de/"

user_data_dir = r"C:\Users\stahl\OneDrive\Dokumente\GitHub\playwright\tests\user-data-dir"

path_to_extension = r"C:\Users\stahl\OneDrive\Dokumente\GitHub\playwright\tests\dontcare"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            args=[
                f"--disable-extensions-except={path_to_extension}",
                f"--load-extension={path_to_extension}",
            ],
        )
        page = await browser.new_page()
        #await stealth_async(page)
        await page.goto(url, wait_until="networkidle")

        document_height = await page.evaluate("document.body.scrollHeight")

        document_width = await page.evaluate("document.body.scrollWidth")


        await page.evaluate("window.scrollTo(0,1);")

        document_height = 4000


        current_scroll_position, new_height= 0, 1
        speed = 10

        #sleeper in between scroll positions

        sleeper = 0


        while current_scroll_position <= new_height:
            current_scroll_position += speed
            print(current_scroll_position)

            sleeper += speed
            if sleeper > 1000:
                time.sleep(1)
                sleeper = 0

            await page.evaluate("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = await page.evaluate("document.body.scrollHeight")


            if current_scroll_position > document_height:
                await page.set_viewport_size({"width": document_width, "height": document_height})

                try:
                    await page.screenshot(path="scroll.png", full_page=True)
                except Exception as e:
                    print(str(e))

                await browser.close()
                break



asyncio.run(main())
