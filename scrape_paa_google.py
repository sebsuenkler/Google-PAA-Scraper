from create_user_dir import create_user_dir

import os
import random
import shutil
import string
import csv  # Hinzugefügt für das Schreiben von CSV-Dateien

import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

from bs4 import BeautifulSoup

def scrape_paa(url):
    user_data_dir = create_user_dir()
    ergebnisse = []  # Liste zum Speichern der Scraping-Ergebnisse

    # Funktion zum Schreiben der gesammelten Daten in eine CSV-Datei
    def schreibe_in_csv(daten, dateiname='ergebnisse.csv'):
        if not daten:
            print("Keine Daten zum Schreiben in die CSV-Datei vorhanden.")
            return

        # Die Feldnamen (Spaltenüberschriften) aus dem ersten Datensatz extrahieren
        feldnamen = daten[0].keys()

        with open(dateiname, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=feldnamen)

            writer.writeheader()  # Schreibt die Kopfzeile
            writer.writerows(daten) # Schreibt alle Datenzeilen

        print(f"Daten wurden erfolgreich in '{dateiname}' gespeichert.")


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

                # Fragen und Antworten lesen
                for i in range(i, count):
                    row_html = await rows.nth(i).evaluate("el => el.outerHTML")
                    soup = BeautifulSoup(row_html, 'html.parser')

                    # Temporäres Dictionary zum Speichern der Daten für die aktuelle Zeile
                    daten_zeile = {
                        "Frage": "Keine Frage gefunden",
                        "Antwort": "Keine Antwort gefunden",
                        "Quelle": "Keine Quelle gefunden",
                        "Datum": "Kein Datum gefunden"
                    }

                    # Extrahiere die Frage
                    try:
                        q = soup.find("span").get_text()
                        daten_zeile["Frage"] = q
                    except:
                        pass

                    # Extrahiere die Antwort
                    try:
                        a = soup.find("div", class_="LGOjhe")
                        if a:
                            a2 = a.find("span", class_="hgKElc").get_text()
                        else:
                            try:
                                a2 = soup.find("div", class_="RqBzHd").get_text()
                            except:
                                try:
                                    a2 = soup.find("div", class_="NPb5dd").get_text()
                                except:
                                    a2 = soup.find("div", class_="Crs1tb").get_text()
                        daten_zeile["Antwort"] = a2
                    except:
                        pass

                    # Extrahiere das Datum der Quelle
                    try:
                        d = a.find("span", class_="kX21rb ZYHQ7e").get_text()
                        daten_zeile["Datum"] = d
                    except:
                        pass

                    # Extrahiere die Quell-URL
                    try:
                        s = soup.find("div", class_="yuRUbf")
                        if s:
                            s2 = s.find("a").get("href")
                        else:
                            s2 = soup.find("a", class_="b0bgab").get("href")
                        daten_zeile["Quelle"] = s2
                    except:
                        pass

                    # Füge die extrahierten Daten der Ergebnisliste hinzu
                    ergebnisse.append(daten_zeile)

                return count

            try:
                await page.goto(url, wait_until="networkidle")
            except PlaywrightTimeoutError:
                await page.goto(url, wait_until="load")

            # Google-Suche simulieren
            await page.fill('input[name="q"]', 'cats')
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(2000) # Kurze Pause, damit die Seite laden kann

            counter = 0

            try:
                # Führe das Scraping mehrmals durch, um mehr "Ähnliche Fragen" zu öffnen
                counter = await scrape_questions(page, counter)
                counter = await scrape_questions(page, counter)
                counter = await scrape_questions(page, counter)
                counter = await scrape_questions(page, counter)
                counter = await scrape_questions(page, counter)
            except Exception as e:
                print(f"Ein Fehler ist aufgetreten: {e}")

            if counter > 0:
                print(f"{len(ergebnisse)} Einträge wurden gesammelt.")
                await page.wait_for_timeout(3000)
            else:
                print("Keine 'Ähnliche Fragen'-Box gefunden.")

            await browser.close()
            shutil.rmtree(user_data_dir)

    asyncio.run(main())

    # Nach dem Scraping die gesammelten Daten in die CSV-Datei schreiben
    schreibe_in_csv(ergebnisse)


# Start des Skripts
urls = ["https://www.google.com/webhp?hl=de"] # Sprache auf Deutsch geändert für relevantere Ergebnisse

for url in urls:
    scrape_paa(url)
