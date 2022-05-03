import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

url = "https://www.spiegel.de/"

max_height = 2000

speed = 3

block = 200

async def main():
    async with async_playwright() as p:
        print(p)
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            browser = await browser_type.launch()
            page = await browser.new_page()
            await stealth_async(page)
            await page.goto(url, wait_until="networkidle")
            document_height = await page.evaluate("document.body.scrollHeight")
            document_width = await page.evaluate("document.body.scrollWidth")

            print(document_height)
            print(document_width)


            current_scroll_position, new_height= 0, 1


            #sleeper in between scroll positions

            sleeper = 0


            while current_scroll_position <= max_height:
                current_scroll_position += speed
                print(current_scroll_position)

                sleeper += speed
                if sleeper > block:
                    await page.wait_for_timeout(1000)
                    await page.wait_for_load_state('networkidle')
                    await page.wait_for_load_state('domcontentloaded')
                    await page.wait_for_load_state('load')

                    sleeper = 0

                await page.evaluate("window.scrollTo(0, {});".format(current_scroll_position))
                new_height = await page.evaluate("document.body.scrollHeight")



                if current_scroll_position > max_height:
                    await page.set_viewport_size({"width": document_width, "height": max_height})

                    try:
                        await page.screenshot(path=f'example-{browser_type.name}.png')
                    except Exception as e:
                        print(str(e))

                    await browser.close()
                    break






asyncio.get_event_loop().run_until_complete(main())
