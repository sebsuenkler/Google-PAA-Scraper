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

            try:
                response = await page.goto(url, wait_until="networkidle")

            except PlaywrightTimeoutError:
                response = await page.goto(url, wait_until="load")

            print(response.status)

            print(response.url)

            print(response.headers["content-type"])

            await page.fill('input[name="q"]', 'cats')

            await page.keyboard.press("Enter")

            await page.wait_for_timeout(1000)

            rows = page.locator(".r21Kzd")
            count = await rows.count()
            for i in range(count):
                print(i)
                await rows.nth(i).click()

            await page.wait_for_timeout(1000)

            rows = page.locator(".r21Kzd")
            count = await rows.count()
            for i in range(count):
                print(i)
                await rows.nth(i).click()

            source = await page.content()

            qa_content = await page.locator(".AuVD.cUnQKe").inner_html()

            print(qa_content)

            title = await page.title()

            print(title)

            #print(source)

            await page.wait_for_timeout(5000)

            await browser.close()

            shutil.rmtree(user_data_dir)


    asyncio.run(main())


#urls = ["https://www.rewe.de/angebote/nationale-angebote/?source=mc_offers", "https://spiegel.de", "https://bild.de", "https://haw-hamburg.de", "https://www.mediamarkt.de/de/product/_samsung-galaxy-a13-64-gb-black-dual-sim-2794341.html", "https://contabo.com/en/", "https://www.google.com/search?q=contabo", "https://www.handelsblatt.com/arts_und_style/literatur/interview-richard-david-precht-seit-corona-erodiert-in-deutschland-einiges/27006328.html", "https://twitter.com/richardprecht"]

#urls = ["https://twitter.com/richardprecht"]

urls = ["https://www.google.com/webhp?hl=en"]

for url in urls:
    scrape_source(url)
