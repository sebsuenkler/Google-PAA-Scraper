from create_user_dir import create_user_dir

import os
import random
import shutil
import string

import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

def scrape_source(url):
    user_data_dir = create_user_dir()

    async def main():

        async with async_playwright() as p:
            browser = await p.firefox.launch_persistent_context(
                user_data_dir,
                headless=False,
            )

            page = await browser.new_page()

            async def scroll_document(page):

                document_height = await page.evaluate("document.body.scrollHeight")
                document_width = await page.evaluate("document.body.scrollWidth")

                blocks = int(document_height / 500) - 1

                for b in range(0, blocks):
                    c = b * 300
                    await page.evaluate("window.scrollTo(0, {});".format(c))
                    await page.wait_for_timeout(500)

                    if c > 8192:
                        break;

                await page.evaluate("window.scrollTo(0,1);")

            try:
                response = await page.goto(url, wait_until="networkidle")

            except PlaywrightTimeoutError:
                response = await page.goto(url, wait_until="load")

            print(response.status)

            print(response.url)

            print(response.headers["content-type"])


            if not "pdf" in response.headers["content-type"]:

                await scroll_document(page)

                source = await page.content()

                title = await page.title()

                print(title)

                #print(source)

                await page.wait_for_timeout(5000)



                def id_generator(size=5, chars=string.ascii_uppercase + string.digits):
                    return ''.join(random.choice(chars) for _ in range(size))


                file_name = id_generator()+".png"
                print(file_name)

                document_height = await page.evaluate("document.body.scrollHeight")

                if document_height > 8192:
                    document_height = 8192

                document_width = await page.evaluate("document.body.scrollWidth")

                await page.set_viewport_size({"width": document_width, "height": document_height})

                await page.screenshot(path=file_name)

                await browser.close()


            else:
                await browser.close()
                print("PDF")
                from pathlib import Path
                import requests
                filename = Path('metadata.pdf')
                response = requests.get(url)
                filename.write_bytes(response.content)

            shutil.rmtree(user_data_dir)


    asyncio.run(main())


#urls = ["https://www.rewe.de/angebote/nationale-angebote/?source=mc_offers", "https://spiegel.de", "https://bild.de", "https://haw-hamburg.de", "https://www.mediamarkt.de/de/product/_samsung-galaxy-a13-64-gb-black-dual-sim-2794341.html", "https://contabo.com/en/", "https://www.google.com/search?q=contabo", "https://www.handelsblatt.com/arts_und_style/literatur/interview-richard-david-precht-seit-corona-erodiert-in-deutschland-einiges/27006328.html", "https://twitter.com/richardprecht"]

#urls = ["https://twitter.com/richardprecht"]

urls = ["https://www.defu.de/shop/katzenfutter/nassfutter/huhn-sensitiv-pate-fuer-katzen.html"]

for url in urls:
    scrape_source(url)
