import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async



url ="https://www.rewe.de/angebote/nationale-angebote/?source=mc_offers"

urls = ["https://www.rewe.de/angebote/nationale-angebote/?source=mc_offers", "https://spiegel.de"]

user_data_dir = r"C:\Users\SearchLabAdmin\Documents\GitHub\playwright\tests\user-data-dir"

path_to_extension = r"C:\Users\SearchLabAdmin\Documents\GitHub\playwright\tests\dontcare.xpi"



async def main():

    i = 0

    for url in urls:
        print(url)
        async with async_playwright() as p:
            browser = await p.firefox.launch_persistent_context(
                user_data_dir
            )
            page = await browser.new_page()
            await page.goto(url, wait_until="load")
            document_height = await page.evaluate("document.body.scrollHeight")
            document_width = await page.evaluate("document.body.scrollWidth")

            await page.evaluate("window.scrollTo(0,1);")

            if document_height > 8192:
                document_height = 8192

            blocks = int(document_height / 500) + 1

            for b in range(0, blocks):
                c = b * 500
                print(c)
                await page.evaluate("window.scrollTo(0, {});".format(c))
                await page.wait_for_timeout(200)


            await page.set_viewport_size({"width": document_width, "height": document_height})


            print(document_width)
            print(document_height)

            await page.wait_for_timeout(5000)

            await page.evaluate("window.scrollTo(0,1);")

            i+=1

            file_name = str(i)+".png"

            await page.screenshot(path=file_name)
            await browser.close()



asyncio.run(main())
