from create_user_dir import create_user_dir

import os
import random
import shutil
import string

import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

from bs4 import BeautifulSoup

def scrape_source(url):
    user_data_dir = create_user_dir()

    async def main():

        async with async_playwright() as p:
            browser = await p.firefox.launch_persistent_context(
                user_data_dir,
                headless=True,
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

                await page.evaluate("window.scrollTo(0,1);")

            async def scrape_content(url):
                print("\n")
                print(url)
                print("\n")
                new_page = await browser.new_page()
                await new_page.goto(url, wait_until="load")
                await scroll_document(new_page)
                source = await new_page.content()
                soup = BeautifulSoup(source, 'html.parser')

                product_name = soup.find("h1", {"itemprop": "name"}).get_text()

                print(product_name.strip())

                try:

                    content = soup.find("div", {"id": "ingredients"})
                    parts = content.find_all('p')

                    try:

                        for p in parts:
                            try:
                                headers = p.find_all('strong')
                                for h in headers:
                                    head = h.get_text()
                                    h.decompose()
                                    if "Zusammensetzung" in head:
                                        ingredients = p.get_text()
                                    if "Zusatzstoffe" in head:
                                        additives = p.get_text()
                                    if "Analytische Bestandteile" in head:
                                        analytical_components = p.get_text()
                            except:
                                pass

                        print("\n")
                        print(ingredients.strip())
                        print("\n")
                        print(additives.strip())
                        print("\n")
                        print(analytical_components.strip())

                    except:
                        print("no ingredients")

                except:
                    print("no food")



            async def scrape_products(page):
                await page.wait_for_timeout(1000)

                rows = page.locator(".col-md-4.col-sm-6.col-xs-12.text-center.productbox.v-offset-m")
                count = await rows.count()

                for i in range(0, count):
                    row = await rows.nth(i).evaluate("el => el.outerHTML")
                    soup = BeautifulSoup(row, 'html.parser')
                    product = soup.find("a").get("href")
                    await scrape_content(product)







            try:
                response = await page.goto(url, wait_until="networkidle")

            except PlaywrightTimeoutError:
                response = await page.goto(url, wait_until="load")

            # print(response.status)
            #
            # print(response.url)
            #
            # print(response.headers["content-type"])

            await scroll_document(page)

            await scrape_products(page)

            source = await page.content()



            await browser.close()

            shutil.rmtree(user_data_dir)

    asyncio.run(main())


urls = ["https://www.defu.de/shop/katzenfutter/nassfutter.html"]

for url in urls:
    scrape_source(url)
