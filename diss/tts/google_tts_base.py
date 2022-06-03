mp3_path = r"C:\Users\stahl\OneDrive\Dokumente\GitHub\playwright\diss\tts\mp3"

from playwright.sync_api import sync_playwright

url = "https://www.google.com/webhp?hl=en"

def run(playwright):
    chromium = playwright.chromium
    browser = chromium.launch(headless=False, executable_path ='C:\Program Files\Google\Chrome\Application\chrome.exe', args=['--use-fake-device-for-media-stream', '--use-fake-ui-for-media-stream'])
    context = browser.new_context(locale="en-US")
    context.grant_permissions(permissions=['microphone'])
    page = context.new_page()

    page.goto(url)
    page.click('.QS5gu.sy4vM')

    def click_cookies(page):
        page.wait_for_timeout(1000)

        rows = page.locator(".VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-INsAgc.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.Rj2Mlf.OLiIxf.PDpWxe.P62QJc.qfvgSe.S82sre")
        count = round(rows.count() / 2)
        print(count)

        for i in range(0, count):
            try:
                row = rows.nth(i).click()
            except:
                pass

    click_cookies(page)
    page.click('.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.qfvgSe.XICXwf')
    page.click('.XDyW0e')

    import pygame
    import pygame._sdl2 as sdl2
    from pygame import mixer
    import time

    mixer.init() # Initialize the mixer, this will allow the next command to work
    print(sdl2.audio.get_audio_device_names(False)) # Returns playback devices, Boolean value determines whether they are Input or Output devices.
    mixer.quit() # Quit the mixer as it's initialized on your main playback device

    page.wait_for_timeout(1000)

    mixer.init(devicename = 'Line (2- AG06/AG03)') # Initialize it with the correct device
    mixer.music.load(mp3_path+'\cat_1.mp3') # Load the mp3
    mixer.music.play() # Play it


    while mixer.music.get_busy():
        time.sleep(1)

    page.wait_for_timeout(30000)

    page.click('.XDyW0e')

    mixer.init(devicename = 'Line (2- AG06/AG03)') # Initialize it with the correct device
    mixer.music.load(mp3_path+'\cat_2.mp3') # Load the mp3
    mixer.music.play() # Play it


    while mixer.music.get_busy():
        time.sleep(1)

    page.wait_for_timeout(30000)

    page.click('.XDyW0e')

    mixer.init(devicename = 'Line (2- AG06/AG03)') # Initialize it with the correct device
    mixer.music.load(mp3_path+'\cat_3.mp3') # Load the mp3
    mixer.music.play() # Play it


    while mixer.music.get_busy():
        time.sleep(1)

    page.pause()
    # other actions...
    mixer.quit() # Quit the mixer as it's initialized on your main playback device
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
