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

            async def scrape_questions(page, counter):
                await page.wait_for_timeout(1000)

                i = counter

                rows = page.locator(".r21Kzd")
                count = await rows.count()

                for i in range(i, count):
                    await rows.nth(i).click()

                rows = page.locator(".z9gcx.SVyP1c")
                count = await rows.count()

                i = counter

                #read questions and answers
                for i in range(i, count):
                    print("\n")
                    print(i)
                    row = await rows.nth(i).evaluate("el => el.outerHTML")
                    soup = BeautifulSoup(row, 'html.parser')
                    li = soup.find_all("div", class_="z9gcx SVyP1c")
                    for l in li:
                        print("\n")
                        try:
                            q = l.find("span").get_text()
                            print(q)
                        except:
                            print("no question")

                        try:
                            try:
                                a = l.find("div", class_="LGOjhe")
                                a2 = a.find("span", class_="hgKElc").get_text()
                            except:
                                try:
                                    a2 = l.find("div", class_="RqBzHd").get_text()
                                except:
                                    try:
                                        a2 = l.find("div", class_="NPb5dd").get_text()
                                    except:
                                        a2 = l.find("div", class_="Crs1tb").get_text()
                            print(a2)
                        except:
                            print("no answer")
                            print(soup)

                        try:
                            d = a.find("span", class_="kX21rb ZYHQ7e").get_text()
                            print(d)
                        except:
                            print("no source date")

                        try:
                            try:
                                s = l.find("div", class_="yuRUbf")
                                s2 = s.find("a").get("href")
                            except:
                                s2 = l.find("a", class_="b0bgab").get("href")

                            print(s2)
                        except:
                            print("no source")

                return count


            try:
                response = await page.goto(url, wait_until="networkidle")

            except PlaywrightTimeoutError:
                response = await page.goto(url, wait_until="load")

            print(response.status)

            print(response.url)

            print(response.headers["content-type"])

            #simulate google search
            await page.fill('input[name="q"]', 'cats')

            await page.keyboard.press("Enter")

            counter = 0

            try:
                counter = await scrape_questions(page, counter)
                counter = await scrape_questions(page, counter)
                counter = await scrape_questions(page, counter)
                counter = await scrape_questions(page, counter)
                counter = await scrape_questions(page, counter)
            except Exceptions as e:
                print(e)

            if counter > 0:
                pass

                # while counter < 5:
                #     counter = await scrape_questions(page, counter)
                #
                #
                # qa_content = await page.locator(".AuVD.cUnQKe").inner_html()
                #
                # soup = BeautifulSoup(qa_content, 'html.parser')
                #
                #



                title = await page.title()

                await page.wait_for_timeout(3000)

                # f = open("test.html", "w+")
                # f.write(str(qa_content))
                # f.close()

            else:
                print("no paa")

            await browser.close()

            shutil.rmtree(user_data_dir)


    asyncio.run(main())


#urls = ["https://www.rewe.de/angebote/nationale-angebote/?source=mc_offers", "https://spiegel.de", "https://bild.de", "https://haw-hamburg.de", "https://www.mediamarkt.de/de/product/_samsung-galaxy-a13-64-gb-black-dual-sim-2794341.html", "https://contabo.com/en/", "https://www.google.com/search?q=contabo", "https://www.handelsblatt.com/arts_und_style/literatur/interview-richard-david-precht-seit-corona-erodiert-in-deutschland-einiges/27006328.html", "https://twitter.com/richardprecht"]

#urls = ["https://twitter.com/richardprecht"]

urls = ["https://www.google.com/webhp?hl=en"]

for url in urls:
    scrape_source(url)
